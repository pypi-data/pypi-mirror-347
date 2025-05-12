"""
GeoJSON读取器模块 - 提供从GeoJSON文件读取地理数据的功能
"""
import json
from typing import Dict, List, Any, Tuple, Optional
import os

from ..entities.coordinate import Coordinate
from ..entities.poi import POI, create_poi_from_dict
from ..entities.road import Road, create_road_from_dict
from ..core.graph import LocationGraph
from ..core.exceptions import DataFormatError, IOError


class GeoJSONReader:
    """
    GeoJSON读取器，用于从GeoJSON文件读取地理数据
    """
    
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
    
    @staticmethod
    def parse_feature(feature: Dict[str, Any]) -> Tuple[Optional[POI], Optional[Road]]:
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
            
            # 创建POI对象
            poi_data = {
                'coordinate': coord,
                'poi_id': properties.get('id') or properties.get('poi_id'),
                'name': properties.get('name', ''),
                'poi_type': properties.get('type') or properties.get('poi_type', 'generic'),
                'properties': properties
            }
            
            return create_poi_from_dict(poi_data), None
        
        # 解析Road (LineString类型)
        elif geometry_type == 'LineString':
            if not isinstance(coordinates, list) or len(coordinates) < 2:
                raise DataFormatError("无效的线坐标")
            
            # 转换坐标
            road_coords = []
            for coord in coordinates:
                if not isinstance(coord, list) or len(coord) < 2:
                    raise DataFormatError("无效的线坐标点")
                
                lon, lat = coord[0], coord[1]
                elevation = coord[2] if len(coord) > 2 else None
                road_coords.append(Coordinate(lat, lon, elevation))
            
            # 创建Road对象
            road_data = {
                'road_id': properties.get('id') or properties.get('road_id'),
                'name': properties.get('name', ''),
                'start_node_id': properties.get('start_node_id'),
                'end_node_id': properties.get('end_node_id'),
                'coordinates': road_coords,
                'road_type': properties.get('type') or properties.get('road_type', 'street'),
                'length': properties.get('length'),
                'speed_limit': properties.get('speed_limit', 50.0),
                'bidirectional': properties.get('bidirectional', True),
                'properties': properties
            }
            
            # 如果没有提供节点ID，使用坐标的哈希值作为节点ID
            if not road_data['start_node_id']:
                road_data['start_node_id'] = f"node_{hash(road_coords[0])}"
            
            if not road_data['end_node_id']:
                road_data['end_node_id'] = f"node_{hash(road_coords[-1])}"
            
            return None, create_road_from_dict(road_data)
        
        # 其他几何类型暂不支持
        else:
            return None, None
    
    @classmethod
    def load_graph(cls, file_path: str) -> LocationGraph:
        """
        从GeoJSON文件加载地理空间图
        
        参数:
            file_path: GeoJSON文件路径
            
        返回:
            LocationGraph对象
            
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确
        """
        # 读取GeoJSON文件
        data = cls.read_file(file_path)
        
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
        # 读取GeoJSON文件
        data = cls.read_file(file_path)
        
        pois = []
        
        # 解析特征
        if data['type'] == 'FeatureCollection' and 'features' in data:
            features = data['features']
            
            for feature in features:
                try:
                    poi, _ = cls.parse_feature(feature)
                    if poi:
                        pois.append(poi)
                except Exception as e:
                    print(f"警告: 解析POI失败: {str(e)}")
        
        elif data['type'] == 'Feature':
            try:
                poi, _ = cls.parse_feature(data)
                if poi:
                    pois.append(poi)
            except Exception as e:
                print(f"警告: 解析POI失败: {str(e)}")
        
        else:
            raise DataFormatError(f"不支持的GeoJSON类型: {data['type']}")
        
        return pois
    
    @classmethod
    def load_roads(cls, file_path: str) -> List[Road]:
        """
        从GeoJSON文件加载Road列表
        
        参数:
            file_path: GeoJSON文件路径
            
        返回:
            Road对象列表
            
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确
        """
        # 读取GeoJSON文件
        data = cls.read_file(file_path)
        
        roads = []
        
        # 解析特征
        if data['type'] == 'FeatureCollection' and 'features' in data:
            features = data['features']
            
            for feature in features:
                try:
                    _, road = cls.parse_feature(feature)
                    if road:
                        roads.append(road)
                except Exception as e:
                    print(f"警告: 解析Road失败: {str(e)}")
        
        elif data['type'] == 'Feature':
            try:
                _, road = cls.parse_feature(data)
                if road:
                    roads.append(road)
            except Exception as e:
                print(f"警告: 解析Road失败: {str(e)}")
        
        else:
            raise DataFormatError(f"不支持的GeoJSON类型: {data['type']}")
        
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
            
            # 添加其他属性
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
            
            # 添加其他属性
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
            
            # 添加其他属性
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