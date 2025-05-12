"""
GeoJSON读取器模块 - 提供从GeoJSON文件读取地理数据的功能
"""
import json
import logging
from typing import Dict, List, Any, Tuple, Optional
import os

logger = logging.getLogger(__name__)

from ..entities.coordinate import Coordinate
from ..entities.poi import POI, create_poi_from_dict
from ..entities.road import Road, create_road_from_dict
from ..core.graph import LocationGraph
from ..core.exceptions import DataFormatError, IOError


class GeoJSONReader:
    """
    GeoJSON读取器，用于从GeoJSON文件读取地理数据
    """
    
    def __init__(self):
        """初始化GeoJSON读取器"""
        self._error_stats = {
            'road': {'invalid_geometry': 0, 'total': 0},
            'poi': {'invalid_geometry': 0, 'total': 0}
        }
        self._feature_idx = 0
    
    @staticmethod
    def read_file(file_path: str) -> Dict[str, Any]:
        """
        读取GeoJSON文件
        
        参数:
            file_path: GeoJSON文件路径
            
        返回:
            GeoJSON数据字典
            
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, dict) or 'type' not in data:
                raise DataFormatError(f"无效的GeoJSON格式: {file_path}")
            
            return data
        
        except json.JSONDecodeError as e:
            raise DataFormatError(f"JSON解析错误: {str(e)}")
        
        except Exception as e:
            raise IOError(f"读取文件失败: {str(e)}")
    
    def parse_feature(self, feature: Dict[str, Any], skip_invalid=True) -> Tuple[Optional[POI], Optional[Road]]:
        """
        解析GeoJSON特征
        
        参数:
            feature: GeoJSON特征字典
            
        返回:
            (POI对象, Road对象) 元组，如果不是POI或Road则相应位置为None
            
        异常:
            DataFormatError: 如果特征格式不正确
        """
        if not isinstance(feature, dict) or 'type' not in feature or feature['type'] != 'Feature':
            raise DataFormatError("无效的GeoJSON特征")
        
        if 'geometry' not in feature or 'properties' not in feature:
            raise DataFormatError("特征缺少几何或属性")
        
        geometry = feature['geometry']
        properties = feature['properties'] or {}
        
        if not isinstance(geometry, dict) or 'type' not in geometry or 'coordinates' not in geometry:
            raise DataFormatError("无效的几何格式")
        
        geometry_type = geometry['type']
        coordinates = geometry['coordinates']
        
        # 解析POI (Point类型)
        if geometry_type == 'Point':
            if not isinstance(coordinates, list) or len(coordinates) < 2:
                raise DataFormatError("无效的点坐标")
            
            # GeoJSON坐标顺序是[经度, 纬度, 高度]
            lon, lat = coordinates[0], coordinates[1]
            elevation = coordinates[2] if len(coordinates) > 2 else None
            
            # 创建坐标对象
            coord = Coordinate(lat, lon, elevation)
            
            # 创建POI对象 - 确保所有属性正确传递
            poi_data = {
                'coordinate': coord,
                'poi_id': str(properties.get('id') or properties.get('poi_id') or f"node_{coord.longitude:.6f}_{coord.latitude:.6f}"),
                'name': str(properties.get('name', '')),
                'poi_type': str(properties.get('type') or properties.get('poi_type', 'generic')),
                'properties': {k: v for k, v in properties.items() 
                              if k not in ['id', 'poi_id', 'name', 'type', 'poi_type']}
            }
            
            return create_poi_from_dict(poi_data), None
        
        # 解析Road (LineString类型)
        elif geometry_type == 'LineString':
            if not isinstance(coordinates, list):
                raise DataFormatError("坐标必须是列表")
            
            # 过滤无效坐标点
            valid_coords = []
            for coord in coordinates:
                try:
                    if isinstance(coord, (list, tuple)) and len(coord) >= 2:
                        lon = float(coord[0])
                        lat = float(coord[1])
                        elevation = float(coord[2]) if len(coord) > 2 else None
                        valid_coords.append(Coordinate(lat, lon, elevation))
                except (TypeError, ValueError):
                    continue
            
            if len(valid_coords) < 2:
                raise DataFormatError("道路必须包含至少两个有效坐标点")
            
            # 创建Road对象 - 确保所有属性正确传递
            # 获取起点和终点坐标
            start_coord = valid_coords[0]
            end_coord = valid_coords[-1]
            
            road_data = {
                'road_id': str(properties.get('id') or properties.get('road_id') or f"road_{hash(tuple(valid_coords))}"),
                'name': str(properties.get('name', '')),
                'start_node_id': str(properties.get('start_node_id') or f"node_{start_coord.longitude:.6f}_{start_coord.latitude:.6f}"),
                'end_node_id': str(properties.get('end_node_id') or f"node_{end_coord.longitude:.6f}_{end_coord.latitude:.6f}"),
                'coordinates': valid_coords,
                'road_type': str(properties.get('type') or properties.get('road_type', 'street')),
                'length': float(properties.get('length')) if properties.get('length') is not None else None,
                'speed_limit': float(properties.get('speed_limit', 50.0)),
                'bidirectional': bool(properties.get('bidirectional', True)),
                'properties': {k: v for k, v in properties.items() 
                             if k not in ['id', 'road_id', 'name', 'start_node_id', 
                                        'end_node_id', 'type', 'road_type', 
                                        'length', 'speed_limit', 'bidirectional']}
            }
            
            return None, create_road_from_dict(road_data)
        
        # 其他几何类型暂不支持
        else:
            return None, None
    
    def load_graph(self, file_path: str, skip_invalid=True) -> LocationGraph:
        """
        从GeoJSON文件加载地理空间图
    
        参数:
            file_path: GeoJSON文件路径
            skip_invalid: 是否跳过无效特征，默认True
    
        返回:
            LocationGraph对象
    
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确且skip_invalid=False
        """
        # 读取GeoJSON文件
        data = self.read_file(file_path)
        
        # 创建图
        graph = LocationGraph()
        
        # 解析特征
        if data['type'] == 'FeatureCollection' and 'features' in data:
            features = data['features']
            
            # 首先添加所有POI
            for feature in features:
                try:
                    poi, _ = cls.parse_feature(feature)
                    if poi:
                        graph.add_node(poi)
                except Exception as e:
                    print(f"警告: 解析POI失败: {str(e)}")
            
            # 然后添加所有Road
            for feature in features:
                try:
                    _, road = cls.parse_feature(feature)
                    if road:
                        # 检查起点和终点是否存在，如果不存在则创建
                        if not graph.has_node(road.start_node_id):
                            start_coord = road.get_start_coordinate()
                            start_poi = POI(
                                coordinate=start_coord,
                                poi_id=road.start_node_id,
                                name=f"Junction {road.start_node_id}",
                                poi_type="junction"
                            )
                            graph.add_node(start_poi)
                        
                        if not graph.has_node(road.end_node_id):
                            end_coord = road.get_end_coordinate()
                            end_poi = POI(
                                coordinate=end_coord,
                                poi_id=road.end_node_id,
                                name=f"Junction {road.end_node_id}",
                                poi_type="junction"
                            )
                            graph.add_node(end_poi)
                        
                        graph.add_edge(road)
                except Exception as e:
                    print(f"警告: 解析Road失败: {str(e)}")
        
        elif data['type'] == 'Feature':
            try:
                poi, road = cls.parse_feature(data)
                
                if poi:
                    graph.add_node(poi)
                
                if road:
                    # 检查起点和终点是否存在，如果不存在则创建
                    if not graph.has_node(road.start_node_id):
                        start_coord = road.get_start_coordinate()
                        start_poi = POI(
                            coordinate=start_coord,
                            poi_id=road.start_node_id,
                            name=f"Junction {road.start_node_id}",
                            poi_type="junction"
                        )
                        graph.add_node(start_poi)
                    
                    if not graph.has_node(road.end_node_id):
                        end_coord = road.get_end_coordinate()
                        end_poi = POI(
                            coordinate=end_coord,
                            poi_id=road.end_node_id,
                            name=f"Junction {road.end_node_id}",
                            poi_type="junction"
                        )
                        graph.add_node(end_poi)
                    
                    graph.add_edge(road)
            except Exception as e:
                print(f"警告: 解析特征失败: {str(e)}")
        
        else:
            raise DataFormatError(f"不支持的GeoJSON类型: {data['type']}")
        
        return graph
    
    @classmethod
    def load_pois(cls, file_path: str) -> List[POI]:
        """
        从GeoJSON文件加载POI列表
        
        参数:
            file_path: GeoJSON文件路径
            
        返回:
            POI对象列表
            
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确
        """
        import warnings
        
        # 读取GeoJSON文件
        data = cls.read_file(file_path)
        
        pois = []
        error_count = 0
        
        # 解析特征
        if data['type'] == 'FeatureCollection' and 'features' in data:
            features = data['features']
            
            for idx, feature in enumerate(features):
                try:
                    if not isinstance(feature, dict):
                        logger.info(f"特征#{idx}不是字典类型，跳过")
                        continue
                        
                    geometry = feature.get('geometry', {})
                    if not isinstance(geometry, dict):
                        logger.info(f"特征#{idx}的几何信息无效，跳过")
                        continue
                        
                    if geometry.get('type') == 'Point':
                        try:
                            poi, _ = cls.parse_feature(feature)
                            if poi:
                                pois.append(poi)
                        except DataFormatError as e:
                            logger.info(f"特征#{idx} POI格式错误: {str(e)}")
                            error_count += 1
                except Exception as e:
                    logger.info(f"特征#{idx} 解析POI失败: {str(e)}")
                    error_count += 1
        
        elif data['type'] == 'Feature':
            try:
                poi, _ = cls.parse_feature(data)
                if poi:
                    pois.append(poi)
            except Exception as e:
                logger.info(f"解析POI失败: {str(e)}")
                error_count += 1
        
        else:
            raise DataFormatError(f"不支持的GeoJSON类型: {data['type']}")
        
        if error_count > 0:
            logger.info(f"共遇到{error_count}个POI解析错误")
        
        return pois
    
    def load_roads(self, file_path: str, skip_invalid=True) -> List[Road]:
        """
        从GeoJSON文件加载Road列表
    
        参数:
            file_path: GeoJSON文件路径
            skip_invalid: 是否跳过无效特征，默认True
    
        返回:
            Road对象列表
    
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确且skip_invalid=False
        """
        import warnings
    
        # 初始化错误计数器
        error_count = 0
        
        # 读取GeoJSON文件
        data = self.read_file(file_path)
        
        roads = []
        
        # 解析特征
        if data['type'] == 'FeatureCollection' and 'features' in data:
            features = data['features']
            
            for idx, feature in enumerate(features):
                try:
                    if not isinstance(feature, dict):
                        logger.info(f"特征#{idx}不是字典类型，跳过")
                        self._error_stats['road']['invalid_geometry'] += 1
                        continue
                        
                    geometry = feature.get('geometry', {})
                    if not isinstance(geometry, dict):
                        logger.info(f"特征#{idx}的几何信息无效，跳过")
                        self._error_stats['road']['invalid_geometry'] += 1
                        continue
                        
                    if geometry.get('type') == 'LineString':
                        _, road = self.parse_feature(feature, skip_invalid)
                        if road:
                            roads.append(road)
                except Exception as e:
                    if not skip_invalid:
                        raise
                    logger.info(f"特征#{idx} 解析Road失败: {str(e)}")
                    self._error_stats['road']['invalid_geometry'] += 1
        
        elif data['type'] == 'Feature':
            try:
                _, road = cls.parse_feature(data)
                if road:
                    roads.append(road)
            except Exception as e:
                logger.info(f"解析Road失败: {str(e)}")
                error_count += 1
        
        else:
            raise DataFormatError(f"不支持的GeoJSON类型: {data['type']}")
        
        if error_count > 0:
            warnings.warn(f"共遇到{error_count}个Road解析错误")
        
        return roads
    
    @staticmethod
    def save_graph(graph: LocationGraph, file_path: str) -> None:
        """
        将地理空间图保存为GeoJSON文件
        
        参数:
            graph: LocationGraph对象
            file_path: 保存路径
            
        异常:
            IOError: 如果文件保存失败
        """
        features = []
        
        # 添加所有POI
        for node in graph.nodes.values():
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [node.coordinate.longitude, node.coordinate.latitude]
                },
                'properties': {
                    'id': node.poi_id,
                    'name': node.name,
                    'type': node.poi_type
                }
            }
            
            # 添加海拔信息（如果有）
            if node.coordinate.elevation is not None:
                feature['geometry']['coordinates'].append(node.coordinate.elevation)
            
            # 添加其他属性（确保properties是字典）
            if hasattr(node, 'properties') and isinstance(node.properties, dict):
                for key, value in node.properties.items():
                    feature['properties'][key] = value
            
            features.append(feature)
        
        # 添加所有Road
        for edge in graph.edges.values():
            # 转换坐标
            coordinates = []
            for coord in edge.coordinates:
                coord_list = [coord.longitude, coord.latitude]
                if coord.elevation is not None:
                    coord_list.append(coord.elevation)
                coordinates.append(coord_list)
            
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coordinates
                },
                'properties': {
                    'id': edge.road_id,
                    'name': edge.name,
                    'type': edge.road_type,
                    'start_node_id': edge.start_node_id,
                    'end_node_id': edge.end_node_id,
                    'length': edge.length,
                    'speed_limit': edge.speed_limit,
                    'bidirectional': edge.bidirectional
                }
            }
            
            # 添加其他属性（确保properties是字典）
            if hasattr(edge, 'properties') and isinstance(edge.properties, dict):
                for key, value in edge.properties.items():
                    feature['properties'][key] = value
            
            features.append(feature)
        
        # 创建GeoJSON对象
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        # 保存到文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(geojson, f, indent=2)
        except Exception as e:
            raise IOError(f"保存文件失败: {str(e)}")
    
    @staticmethod
    def save_pois(pois: List[POI], file_path: str) -> None:
        """
        将POI列表保存为GeoJSON文件
        
        参数:
            pois: POI对象列表
            file_path: 保存路径
            
        异常:
            IOError: 如果文件保存失败
        """
        features = []
        
        for poi in pois:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [poi.coordinate.longitude, poi.coordinate.latitude]
                },
                'properties': {
                    'id': poi.poi_id,
                    'name': poi.name,
                    'type': poi.poi_type
                }
            }
            
            # 添加海拔信息（如果有）
            if poi.coordinate.elevation is not None:
                feature['geometry']['coordinates'].append(poi.coordinate.elevation)
            
            # 添加其他属性
            for key, value in poi.properties.items():
                feature['properties'][key] = value
            
            features.append(feature)
        
        # 创建GeoJSON对象
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        # 保存到文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(geojson, f, indent=2)
        except Exception as e:
            raise IOError(f"保存文件失败: {str(e)}")
    
    @staticmethod
    def save_roads(roads: List[Road], file_path: str) -> None:
        """
        将Road列表保存为GeoJSON文件
        
        参数:
            roads: Road对象列表
            file_path: 保存路径
            
        异常:
            IOError: 如果文件保存失败
        """
        features = []
        
        for road in roads:
            # 转换坐标
            coordinates = []
            for coord in road.coordinates:
                coord_list = [coord.longitude, coord.latitude]
                if coord.elevation is not None:
                    coord_list.append(coord.elevation)
                coordinates.append(coord_list)
            
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coordinates
                },
                'properties': {
                    'id': road.road_id,
                    'name': road.name,
                    'type': road.road_type,
                    'start_node_id': road.start_node_id,
                    'end_node_id': road.end_node_id,
                    'length': road.length,
                    'speed_limit': road.speed_limit,
                    'bidirectional': road.bidirectional
                }
            }
            
            # 添加其他属性（确保properties是字典）
            if hasattr(road, 'properties') and isinstance(road.properties, dict):
                for key, value in road.properties.items():
                    feature['properties'][key] = value
            
            features.append(feature)
        
        # 创建GeoJSON对象
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        # 保存到文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(geojson, f, indent=2)
        except Exception as e:
            raise IOError(f"保存文件失败: {str(e)}")