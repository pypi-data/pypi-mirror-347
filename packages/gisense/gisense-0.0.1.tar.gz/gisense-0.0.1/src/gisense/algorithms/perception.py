"""
地理感知模块 - 提供地理空间环境感知功能
"""
from typing import List, Dict, Any, Tuple, Set, Optional
import math
from collections import defaultdict

from ..entities.coordinate import Coordinate
from ..entities.poi import POI
from ..entities.road import Road
from ..core.graph import LocationGraph
from ..core.observer import Observer
from ..utils.distance import haversine_distance, bearing
from ..utils.geometry import point_to_polyline_distance


class PerceptionEngine:
    """
    地理感知引擎，提供地理空间环境感知功能
    """
    
    def __init__(self, graph: LocationGraph):
        """
        初始化地理感知引擎
        
        参数:
            graph: 地理空间图
        """
        self.graph = graph
    
    def detect_nearby_pois(self, location: Coordinate, radius: float, 
                          poi_types: Optional[List[str]] = None) -> List[Tuple[POI, float]]:
        """
        检测指定位置附近的POI
        
        参数:
            location: 位置坐标
            radius: 搜索半径 (米)
            poi_types: POI类型列表，如果为None则检测所有类型
            
        返回:
            (POI, 距离) 元组的列表，按距离升序排序
        """
        result = []
        
        for poi in self.graph.nodes.values():
            # 如果指定了POI类型，则只检测指定类型
            if poi_types and poi.poi_type not in poi_types:
                continue
            
            distance = haversine_distance(location, poi.coordinate)
            if distance <= radius:
                result.append((poi, distance))
        
        # 按距离排序
        return sorted(result, key=lambda x: x[1])
    
    def detect_nearby_roads(self, location: Coordinate, radius: float, 
                           road_types: Optional[List[str]] = None) -> List[Tuple[Road, float]]:
        """
        检测指定位置附近的道路
        
        参数:
            location: 位置坐标
            radius: 搜索半径 (米)
            road_types: 道路类型列表，如果为None则检测所有类型
            
        返回:
            (Road, 距离) 元组的列表，按距离升序排序
        """
        result = []
        
        for road in self.graph.edges.values():
            # 如果指定了道路类型，则只检测指定类型
            if road_types and road.road_type not in road_types:
                continue
            
            # 计算点到道路的最短距离
            min_distance, _, _ = point_to_polyline_distance(location, road.coordinates)
            
            if min_distance <= radius:
                result.append((road, min_distance))
        
        # 按距离排序
        return sorted(result, key=lambda x: x[1])
    
    def match_coordinate(self, location: Coordinate, max_distance: float = 50.0) -> Dict[str, Any]:
        """
        将位置匹配到最近的道路上
        
        参数:
            location: 位置坐标
            max_distance: 最大匹配距离 (米)
            
        返回:
            包含匹配结果的字典，如果没有匹配到则返回None
        """
        return self.graph.match_coordinate(location)
    
    def match_trajectory(self, trajectory: List[Coordinate], max_gap: int = 5) -> List[Dict[str, Any]]:
        """
        将轨迹匹配到道路上
        
        参数:
            trajectory: 轨迹坐标列表
            max_gap: 允许的最大连续未匹配点数
            
        返回:
            匹配结果列表
        """
        return self.graph.match_coordinates(trajectory, max_gap)
    
    def detect_turn_events(self, trajectory: List[Coordinate], 
                          angle_threshold: float = 30.0) -> List[Dict[str, Any]]:
        """
        检测轨迹中的转弯事件
        
        参数:
            trajectory: 轨迹坐标列表
            angle_threshold: 转弯角度阈值 (度)
            
        返回:
            转弯事件列表，每个事件是一个字典:
            {
                'index': 转弯点在轨迹中的索引,
                'coordinate': 转弯点坐标,
                'angle': 转弯角度 (度),
                'direction': 转弯方向 ('left' 或 'right')
            }
        """
        if len(trajectory) < 3:
            return []
        
        turn_events = []
        
        for i in range(1, len(trajectory) - 1):
            prev_coord = trajectory[i - 1]
            curr_coord = trajectory[i]
            next_coord = trajectory[i + 1]
            
            # 计算前一段和后一段的方位角
            bearing1 = bearing(prev_coord, curr_coord)
            bearing2 = bearing(curr_coord, next_coord)
            
            # 计算转弯角度
            angle_diff = abs((bearing2 - bearing1 + 180) % 360 - 180)
            
            # 如果角度大于阈值，则认为是转弯
            if angle_diff > angle_threshold:
                # 判断转弯方向
                direction = 'right' if (bearing2 - bearing1 + 360) % 360 < 180 else 'left'
                
                turn_events.append({
                    'index': i,
                    'coordinate': curr_coord,
                    'angle': angle_diff,
                    'direction': direction
                })
        
        return turn_events
    
    def detect_stop_events(self, trajectory: List[Coordinate], timestamps: List[float], 
                         speed_threshold: float = 0.5, duration_threshold: float = 60.0) -> List[Dict[str, Any]]:
        """
        检测轨迹中的停止事件
        
        参数:
            trajectory: 轨迹坐标列表
            timestamps: 对应的时间戳列表 (秒)
            speed_threshold: 速度阈值 (米/秒)，低于此值视为停止
            duration_threshold: 持续时间阈值 (秒)，超过此值视为有效停止
            
        返回:
            停止事件列表，每个事件是一个字典:
            {
                'start_index': 停止开始点在轨迹中的索引,
                'end_index': 停止结束点在轨迹中的索引,
                'coordinate': 停止位置坐标 (取平均值),
                'duration': 停止持续时间 (秒),
                'nearby_pois': 附近的POI列表
            }
        """
        if len(trajectory) != len(timestamps):
            raise ValueError("轨迹坐标列表和时间戳列表长度不一致")
        
        if len(trajectory) < 2:
            return []
        
        stop_events = []
        current_stop = None
        
        for i in range(1, len(trajectory)):
            prev_coord = trajectory[i - 1]
            curr_coord = trajectory[i]
            
            # 计算距离和时间差
            distance = haversine_distance(prev_coord, curr_coord)
            time_diff = timestamps[i] - timestamps[i - 1]
            
            # 计算速度
            speed = distance / time_diff if time_diff > 0 else 0
            
            # 如果速度低于阈值，可能是停止
            if speed < speed_threshold:
                if current_stop is None:
                    # 开始新的停止事件
                    current_stop = {
                        'start_index': i - 1,
                        'coordinates': [prev_coord, curr_coord],
                        'timestamps': [timestamps[i - 1], timestamps[i]]
                    }
                else:
                    # 继续当前停止事件
                    current_stop['coordinates'].append(curr_coord)
                    current_stop['timestamps'].append(timestamps[i])
            else:
                # 如果当前有停止事件，检查其持续时间
                if current_stop is not None:
                    duration = current_stop['timestamps'][-1] - current_stop['timestamps'][0]
                    
                    if duration >= duration_threshold:
                        # 计算停止位置的平均坐标
                        avg_lat = sum(c.latitude for c in current_stop['coordinates']) / len(current_stop['coordinates'])
                        avg_lon = sum(c.longitude for c in current_stop['coordinates']) / len(current_stop['coordinates'])
                        avg_coord = Coordinate(avg_lat, avg_lon)
                        
                        # 查找附近的POI
                        nearby_pois = self.detect_nearby_pois(avg_coord, 100.0)
                        
                        stop_events.append({
                            'start_index': current_stop['start_index'],
                            'end_index': i - 1,
                            'coordinate': avg_coord,
                            'duration': duration,
                            'nearby_pois': nearby_pois
                        })
                    
                    current_stop = None
        
        # 检查最后一个可能的停止事件
        if current_stop is not None:
            duration = current_stop['timestamps'][-1] - current_stop['timestamps'][0]
            
            if duration >= duration_threshold:
                # 计算停止位置的平均坐标
                avg_lat = sum(c.latitude for c in current_stop['coordinates']) / len(current_stop['coordinates'])
                avg_lon = sum(c.longitude for c in current_stop['coordinates']) / len(current_stop['coordinates'])
                avg_coord = Coordinate(avg_lat, avg_lon)
                
                # 查找附近的POI
                nearby_pois = self.detect_nearby_pois(avg_coord, 100.0)
                
                stop_events.append({
                    'start_index': current_stop['start_index'],
                    'end_index': len(trajectory) - 1,
                    'coordinate': avg_coord,
                    'duration': duration,
                    'nearby_pois': nearby_pois
                })
        
        return stop_events
    
    def detect_junction_crossings(self, trajectory: List[Coordinate], 
                                junction_radius: float = 20.0) -> List[Dict[str, Any]]:
        """
        检测轨迹中的路口穿越事件
        
        参数:
            trajectory: 轨迹坐标列表
            junction_radius: 路口半径 (米)
            
        返回:
            路口穿越事件列表，每个事件是一个字典:
            {
                'index': 穿越点在轨迹中的索引,
                'coordinate': 穿越点坐标,
                'junction': 路口POI对象,
                'connected_roads': 连接的道路列表
            }
        """
        if len(trajectory) < 2:
            return []
        
        # 找出所有类型为"junction"的POI
        junctions = [poi for poi in self.graph.nodes.values() if poi.poi_type == "junction"]
        
        # 如果没有显式标记为junction的POI，则将所有连接多条道路的POI视为路口
        if not junctions:
            junctions = [poi for poi in self.graph.nodes.values() 
                       if len(poi.connected_road_ids) > 2]
        
        junction_crossings = []
        visited_junctions = set()
        
        for i, coord in enumerate(trajectory):
            for junction in junctions:
                junction_id = junction.poi_id
                
                # 如果已经访问过该路口，跳过
                if junction_id in visited_junctions:
                    continue
                
                distance = haversine_distance(coord, junction.coordinate)
                
                if distance <= junction_radius:
                    # 获取连接的道路
                    connected_roads = []
                    for road_id in junction.connected_road_ids:
                        if road_id in self.graph.edges:
                            connected_roads.append(self.graph.edges[road_id])
                    
                    junction_crossings.append({
                        'index': i,
                        'coordinate': coord,
                        'junction': junction,
                        'connected_roads': connected_roads
                    })
                    
                    # 标记为已访问
                    visited_junctions.add(junction_id)
        
        return junction_crossings
    
    def detect_road_changes(self, matched_trajectory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        检测轨迹中的道路变更事件
        
        参数:
            matched_trajectory: 匹配到道路上的轨迹列表
            
        返回:
            道路变更事件列表，每个事件是一个字典:
            {
                'index': 变更点在轨迹中的索引,
                'coordinate': 变更点坐标,
                'from_road': 变更前的道路对象,
                'to_road': 变更后的道路对象
            }
        """
        if not matched_trajectory or len(matched_trajectory) < 2:
            return []
        
        road_changes = []
        current_road_id = None
        
        for i, match in enumerate(matched_trajectory):
            if match is None:
                continue
            
            road_id = match.get('road_id')
            
            if road_id is not None and road_id != current_road_id and current_road_id is not None:
                road_changes.append({
                    'index': i,
                    'coordinate': match.get('matched_coordinate'),
                    'from_road': self.graph.edges.get(current_road_id),
                    'to_road': self.graph.edges.get(road_id)
                })
            
            current_road_id = road_id
        
        return road_changes
    
    def analyze_trajectory(self, trajectory: List[Coordinate], timestamps: Optional[List[float]] = None) -> Dict[str, Any]:
        """
        综合分析轨迹，检测各种事件
        
        参数:
            trajectory: 轨迹坐标列表
            timestamps: 对应的时间戳列表 (秒)，如果为None则不检测与时间相关的事件
            
        返回:
            包含分析结果的字典:
            {
                'matched_trajectory': 匹配到道路上的轨迹,
                'turn_events': 转弯事件列表,
                'junction_crossings': 路口穿越事件列表,
                'road_changes': 道路变更事件列表,
                'stop_events': 停止事件列表 (如果提供了timestamps)
            }
        """
        # 匹配轨迹到道路上
        matched_trajectory = self.match_trajectory(trajectory)
        
        # 检测转弯事件
        turn_events = self.detect_turn_events(trajectory)
        
        # 检测路口穿越事件
        junction_crossings = self.detect_junction_crossings(trajectory)
        
        # 检测道路变更事件
        road_changes = self.detect_road_changes(matched_trajectory)
        
        result = {
            'matched_trajectory': matched_trajectory,
            'turn_events': turn_events,
            'junction_crossings': junction_crossings,
            'road_changes': road_changes
        }
        
        # 如果提供了时间戳，检测停止事件
        if timestamps is not None:
            if len(timestamps) != len(trajectory):
                raise ValueError("轨迹坐标列表和时间戳列表长度不一致")
            
            stop_events = self.detect_stop_events(trajectory, timestamps)
            result['stop_events'] = stop_events
        
        return result
    
    def update_observer(self, observer: Observer) -> Dict[str, Any]:
        """
        更新观察者的感知
        
        参数:
            observer: 观察者对象
            
        返回:
            包含感知结果的字典
        """
        # 匹配观察者位置到道路上
        matched_road = self.match_coordinate(observer.location)
        observer.set_matched_road(matched_road)
        
        # 获取可见的POI和道路
        visible_pois = []
        visible_roads = []
        
        for poi in self.graph.nodes.values():
            if observer.is_poi_visible(poi):
                visible_pois.append(poi)
        
        for road in self.graph.edges.values():
            if observer.is_road_visible(road):
                visible_roads.append(road)
        
        # 更新观察者的感知
        perception_result = observer.update_perception(visible_pois, visible_roads)
        
        return perception_result
    
    def get_navigation_instructions(self, path: List[str]) -> List[Dict[str, Any]]:
        """
        根据路径生成导航指令
        
        参数:
            path: 路径上的节点ID列表
            
        返回:
            导航指令列表，每个指令是一个字典:
            {
                'type': 指令类型 ('start', 'continue', 'turn', 'arrive'),
                'road_name': 道路名称,
                'distance': 距离 (米),
                'direction': 方向 (对于转弯指令),
                'angle': 转弯角度 (度，对于转弯指令),
                'coordinate': 指令位置坐标
            }
        """
        if len(path) < 2:
            return []
        
        # 获取路径上的边
        edges = self.graph.get_path_edges(path)
        
        instructions = []
        current_road_name = None
        current_road_type = None
        accumulated_distance = 0.0
        
        # 添加起点指令
        start_node = self.graph.get_node(path[0])
        start_edge = edges[0]
        
        instructions.append({
            'type': 'start',
            'road_name': start_edge.name or f"{start_edge.road_type} road",
            'road_type': start_edge.road_type,
            'distance': 0.0,
            'coordinate': start_node.coordinate
        })
        
        current_road_name = start_edge.name
        current_road_type = start_edge.road_type
        
        # 处理路径上的每条边
        for i in range(len(edges)):
            edge = edges[i]
            accumulated_distance += edge.length
            
            # 如果道路名称或类型发生变化，添加转弯指令
            if edge.name != current_road_name or edge.road_type != current_road_type:
                # 获取转弯节点
                turn_node_id = path[i]
                turn_node = self.graph.get_node(turn_node_id)
                
                # 计算转弯角度和方向
                if i > 0:
                    prev_edge = edges[i - 1]
                    
                    # 获取前一条边和当前边的方向
                    prev_bearing = bearing(prev_edge.coordinates[-2], prev_edge.coordinates[-1])
                    curr_bearing = bearing(edge.coordinates[0], edge.coordinates[1])
                    
                    # 计算转弯角度
                    angle_diff = abs((curr_bearing - prev_bearing + 180) % 360 - 180)
                    
                    # 判断转弯方向
                    if angle_diff < 10:
                        direction = 'straight'
                    elif angle_diff < 45:
                        direction = 'slight right' if (curr_bearing - prev_bearing + 360) % 360 < 180 else 'slight left'
                    elif angle_diff < 135:
                        direction = 'right' if (curr_bearing - prev_bearing + 360) % 360 < 180 else 'left'
                    else:
                        direction = 'sharp right' if (curr_bearing - prev_bearing + 360) % 360 < 180 else 'sharp left'
                    
                    instructions.append({
                        'type': 'turn',
                        'road_name': edge.name or f"{edge.road_type} road",
                        'road_type': edge.road_type,
                        'distance': accumulated_distance,
                        'direction': direction,
                        'angle': angle_diff,
                        'coordinate': turn_node.coordinate
                    })
                    
                    # 重置累计距离
                    accumulated_distance = 0.0
                
                current_road_name = edge.name
                current_road_type = edge.road_type
            
            # 如果是最后一条边，添加到达指令
            if i == len(edges) - 1:
                end_node = self.graph.get_node(path[-1])
                
                instructions.append({
                    'type': 'arrive',
                    'road_name': current_road_name or f"{current_road_type} road",
                    'road_type': current_road_type,
                    'distance': accumulated_distance,
                    'coordinate': end_node.coordinate
                })
        
        return instructions