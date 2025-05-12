"""
Shapefile读取器模块 - 提供从Shapefile文件读取地理数据的功能
"""
from typing import Dict, List, Any, Tuple, Optional
import os
import warnings

from ..entities.coordinate import Coordinate
from ..entities.poi import POI
from ..entities.road import Road
from ..core.graph import LocationGraph
from ..core.exceptions import DataFormatError, IOError


class ShapefileReader:
    """
    Shapefile读取器，用于从Shapefile文件读取地理数据
    
    注意：此类依赖于geopandas库，需要先安装：
    pip install geopandas
    """
    
    @staticmethod
    def read_file(file_path: str) -> Any:
        """
        读取Shapefile文件
        
        参数:
            file_path: Shapefile文件路径
            
        返回:
            GeoDataFrame对象
            
        异常:
            IOError: 如果文件读取失败
            ImportError: 如果未安装geopandas
        """
        try:
            import geopandas as gpd
        except ImportError:
            raise ImportError("未安装geopandas库，请先安装: pip install geopandas")
        
        try:
            # 读取Shapefile
            gdf = gpd.read_file(file_path)
            return gdf
        
        except Exception as e:
            raise IOError(f"读取Shapefile失败: {str(e)}")
    
    @staticmethod
    def parse_point(geometry, properties: Dict[str, Any]) -> POI:
        """
        解析点几何体为POI对象
        
        参数:
            geometry: 点几何体
            properties: 属性字典
            
        返回:
            POI对象
        """
        try:
            import shapely
        except ImportError:
            raise ImportError("未安装shapely库，请先安装: pip install shapely")
        
        # 获取坐标
        lon, lat = geometry.x, geometry.y
        
        # 创建坐标对象
        coord = Coordinate(lat, lon)
        
        # 创建POI对象
        poi_data = {
            'coordinate': coord,
            'poi_id': properties.get('id') or properties.get('poi_id'),
            'name': properties.get('name', ''),
            'poi_type': properties.get('type') or properties.get('poi_type', 'generic'),
            'properties': properties
        }
        
        # 如果没有提供ID，使用坐标的哈希值作为ID
        if not poi_data['poi_id']:
            poi_data['poi_id'] = f"poi_{hash(coord)}"
        
        return POI(
            coordinate=coord,
            poi_id=poi_data['poi_id'],
            name=poi_data['name'],
            poi_type=poi_data['poi_type'],
            properties=poi_data['properties']
        )
    
    @staticmethod
    def parse_linestring(geometry, properties: Dict[str, Any]) -> Road:
        """
        解析线几何体为Road对象
        
        参数:
            geometry: 线几何体
            properties: 属性字典
            
        返回:
            Road对象
        """
        try:
            import shapely
        except ImportError:
            raise ImportError("未安装shapely库，请先安装: pip install shapely")
        
        # 获取坐标
        coords = []
        for point in geometry.coords:
            lon, lat = point[0], point[1]
            elevation = point[2] if len(point) > 2 else None
            coords.append(Coordinate(lat, lon, elevation))
        
        # 创建Road对象
        road_data = {
            'road_id': properties.get('id') or properties.get('road_id'),
            'name': properties.get('name', ''),
            'start_node_id': properties.get('start_node_id'),
            'end_node_id': properties.get('end_node_id'),
            'coordinates': coords,
            'road_type': properties.get('type') or properties.get('road_type', 'street'),
            'length': properties.get('length'),
            'speed_limit': properties.get('speed_limit', 50.0),
            'bidirectional': properties.get('bidirectional', True),
            'properties': properties
        }
        
        # 如果没有提供ID，使用坐标的哈希值作为ID
        if not road_data['road_id']:
            road_data['road_id'] = f"road_{hash(tuple(coords))}"
        
        # 如果没有提供节点ID，使用坐标的哈希值作为节点ID
        if not road_data['start_node_id']:
            road_data['start_node_id'] = f"node_{hash(coords[0])}"
        
        if not road_data['end_node_id']:
            road_data['end_node_id'] = f"node_{hash(coords[-1])}"
        
        return Road(
            road_id=road_data['road_id'],
            name=road_data['name'],
            start_node_id=road_data['start_node_id'],
            end_node_id=road_data['end_node_id'],
            coordinates=road_data['coordinates'],
            road_type=road_data['road_type'],
            length=road_data['length'],
            speed_limit=road_data['speed_limit'],
            bidirectional=road_data['bidirectional'],
            properties=road_data['properties']
        )
    
    @classmethod
    def load_graph(cls, file_path: str) -> LocationGraph:
        """
        从Shapefile文件加载地理空间图
        
        参数:
            file_path: Shapefile文件路径
            
        返回:
            LocationGraph对象
            
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确
        """
        try:
            import shapely
        except ImportError:
            raise ImportError("未安装shapely库，请先安装: pip install shapely")
        
        # 读取Shapefile
        gdf = cls.read_file(file_path)
        
        # 创建图
        graph = LocationGraph()
        
        # 解析几何体
        for _, row in gdf.iterrows():
            geometry = row.geometry
            properties = {col: row[col] for col in gdf.columns if col != 'geometry'}
            
            try:
                # 解析点几何体
                if geometry.geom_type == 'Point':
                    poi = cls.parse_point(geometry, properties)
                    graph.add_node(poi)
                
                # 解析线几何体
                elif geometry.geom_type == 'LineString':
                    road = cls.parse_linestring(geometry, properties)
                    
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
                
                # 其他几何类型暂不支持
                else:
                    warnings.warn(f"不支持的几何类型: {geometry.geom_type}")
            
            except Exception as e:
                warnings.warn(f"解析几何体失败: {str(e)}")
        
        return graph
    
    @classmethod
    def load_pois(cls, file_path: str) -> List[POI]:
        """
        从Shapefile文件加载POI列表
        
        参数:
            file_path: Shapefile文件路径
            
        返回:
            POI对象列表
            
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确
        """
        try:
            import shapely
        except ImportError:
            raise ImportError("未安装shapely库，请先安装: pip install shapely")
        
        # 读取Shapefile
        gdf = cls.read_file(file_path)
        
        pois = []
        
        # 解析几何体
        for _, row in gdf.iterrows():
            geometry = row.geometry
            properties = {col: row[col] for col in gdf.columns if col != 'geometry'}
            
            try:
                # 解析点几何体
                if geometry.geom_type == 'Point':
                    poi = cls.parse_point(geometry, properties)
                    pois.append(poi)
                
                # 其他几何类型暂不支持
                else:
                    warnings.warn(f"不支持的几何类型: {geometry.geom_type}")
            
            except Exception as e:
                warnings.warn(f"解析几何体失败: {str(e)}")
        
        return pois
    
    @classmethod
    def load_roads(cls, file_path: str) -> List[Road]:
        """
        从Shapefile文件加载Road列表
        
        参数:
            file_path: Shapefile文件路径
            
        返回:
            Road对象列表
            
        异常:
            IOError: 如果文件读取失败
            DataFormatError: 如果文件格式不正确
        """
        try:
            import shapely
        except ImportError:
            raise ImportError("未安装shapely库，请先安装: pip install shapely")
        
        # 读取Shapefile
        gdf = cls.read_file(file_path)
        
        roads = []
        
        # 解析几何体
        for _, row in gdf.iterrows():
            geometry = row.geometry
            properties = {col: row[col] for col in gdf.columns if col != 'geometry'}
            
            try:
                # 解析线几何体
                if geometry.geom_type == 'LineString':
                    road = cls.parse_linestring(geometry, properties)
                    roads.append(road)
                
                # 其他几何类型暂不支持
                else:
                    warnings.warn(f"不支持的几何类型: {geometry.geom_type}")
            
            except Exception as e:
                warnings.warn(f"解析几何体失败: {str(e)}")
        
        return roads
    
    @staticmethod
    def save_graph(graph: LocationGraph, file_path: str) -> None:
        """
        将地理空间图保存为Shapefile文件
        
        参数:
            graph: LocationGraph对象
            file_path: 保存路径
            
        异常:
            IOError: 如果文件保存失败
            ImportError: 如果未安装geopandas
        """
        try:
            import geopandas as gpd
            from shapely.geometry import Point, LineString
        except ImportError:
            raise ImportError("未安装geopandas或shapely库，请先安装: pip install geopandas shapely")
        
        # 创建POI的GeoDataFrame
        poi_data = []
        for node in graph.nodes.values():
            geometry = Point(node.coordinate.longitude, node.coordinate.latitude)
            properties = {
                'id': node.poi_id,
                'name': node.name,
                'type': node.poi_type
            }
            
            # 添加其他属性
            for key, value in node.properties.items():
                properties[key] = value
            
            poi_data.append({**properties, 'geometry': geometry})
        
        # 创建Road的GeoDataFrame
        road_data = []
        for edge in graph.edges.values():
            # 转换坐标
            coords = [(coord.longitude, coord.latitude) for coord in edge.coordinates]
            geometry = LineString(coords)
            
            properties = {
                'id': edge.road_id,
                'name': edge.name,
                'type': edge.road_type,
                'start_node_id': edge.start_node_id,
                'end_node_id': edge.end_node_id,
                'length': edge.length,
                'speed_limit': edge.speed_limit,
                'bidirectional': edge.bidirectional
            }
            
            # 添加其他属性
            for key, value in edge.properties.items():
                properties[key] = value
            
            road_data.append({**properties, 'geometry': geometry})
        
        # 创建GeoDataFrame
        if poi_data and road_data:
            # 如果同时有POI和Road，分别保存
            poi_gdf = gpd.GeoDataFrame(poi_data)
            road_gdf = gpd.GeoDataFrame(road_data)
            
            # 获取文件名和目录
            file_dir = os.path.dirname(file_path)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # 保存POI
            poi_path = os.path.join(file_dir, f"{file_name}_poi.shp")
            poi_gdf.to_file(poi_path)
            
            # 保存Road
            road_path = os.path.join(file_dir, f"{file_name}_road.shp")
            road_gdf.to_file(road_path)
        
        elif poi_data:
            # 只有POI
            poi_gdf = gpd.GeoDataFrame(poi_data)
            poi_gdf.to_file(file_path)
        
        elif road_data:
            # 只有Road
            road_gdf = gpd.GeoDataFrame(road_data)
            road_gdf.to_file(file_path)
        
        else:
            # 没有数据
            warnings.warn("没有数据可保存")
    
    @staticmethod
    def save_pois(pois: List[POI], file_path: str) -> None:
        """
        将POI列表保存为Shapefile文件
        
        参数:
            pois: POI对象列表
            file_path: 保存路径
            
        异常:
            IOError: 如果文件保存失败
            ImportError: 如果未安装geopandas
        """
        try:
            import geopandas as gpd
            from shapely.geometry import Point
        except ImportError:
            raise ImportError("未安装geopandas或shapely库，请先安装: pip install geopandas shapely")
        
        # 创建POI的GeoDataFrame
        poi_data = []
        for poi in pois:
            geometry = Point(poi.coordinate.longitude, poi.coordinate.latitude)
            properties = {
                'id': poi.poi_id,
                'name': poi.name,
                'type': poi.poi_type
            }
            
            # 添加其他属性
            for key, value in poi.properties.items():
                properties[key] = value
            
            poi_data.append({**properties, 'geometry': geometry})
        
        # 创建GeoDataFrame
        if poi_data:
            poi_gdf = gpd.GeoDataFrame(poi_data)
            poi_gdf.to_file(file_path)
        else:
            warnings.warn("没有POI数据可保存")
    
    @staticmethod
    def save_roads(roads: List[Road], file_path: str) -> None:
        """
        将Road列表保存为Shapefile文件
        
        参数:
            roads: Road对象列表
            file_path: 保存路径
            
        异常:
            IOError: 如果文件保存失败
            ImportError: 如果未安装geopandas
        """
        try:
            import geopandas as gpd
            from shapely.geometry import LineString
        except ImportError:
            raise ImportError("未安装geopandas或shapely库，请先安装: pip install geopandas shapely")
        
        # 创建Road的GeoDataFrame
        road_data = []
        for road in roads:
            # 转换坐标
            coords = [(coord.longitude, coord.latitude) for coord in road.coordinates]
            geometry = LineString(coords)
            
            properties = {
                'id': road.road_id,
                'name': road.name,
                'type': road.road_type,
                'start_node_id': road.start_node_id,
                'end_node_id': road.end_node_id,
                'length': road.length,
                'speed_limit': road.speed_limit,
                'bidirectional': road.bidirectional
            }
            
            # 添加其他属性
            for key, value in road.properties.items():
                properties[key] = value
            
            road_data.append({**properties, 'geometry': geometry})
        
        # 创建GeoDataFrame
        if road_data:
            road_gdf = gpd.GeoDataFrame(road_data)
            road_gdf.to_file(file_path)
        else:
            warnings.warn("没有Road数据可保存")