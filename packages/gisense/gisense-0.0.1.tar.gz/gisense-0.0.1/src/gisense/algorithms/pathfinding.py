"""
路径规划模块 - 提供各种路径规划算法
"""
from typing import List, Dict, Any, Tuple, Set, Optional, Callable
import heapq
import math
from collections import defaultdict, deque

from ..entities.coordinate import Coordinate
from ..entities.poi import POI
from ..entities.road import Road
from ..core.graph import LocationGraph
from ..core.exceptions import PathNotFoundError, NodeNotFoundError
from ..utils.distance import haversine_distance


class PathFinder:
    """
    路径规划器，提供各种路径规划算法
    """
    
    def __init__(self, graph: LocationGraph):
        """
        初始化路径规划器
        
        参数:
            graph: 地理空间图
        """
        self.graph = graph
    
    def find_shortest_path(self, start_node_id: str, end_node_id: str, 
                          weight_type: str = 'distance', weight_func=None) -> Dict[str, Any]:
        """
        使用Dijkstra算法查找最短路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            weight_type: 权重类型 ('distance', 'time', 'custom')
            
        返回:
            包含路径信息的字典:
            {
                'path': 路径上的节点ID列表,
                'edges': 路径上的边对象列表,
                'total_distance': 路径总长度 (米),
                'total_time': 路径总时间 (小时),
                'coordinates': 路径上的坐标点列表
            }
            
        异常:
            NodeNotFoundError: 如果起点或终点不存在
            PathNotFoundError: 如果无法找到路径
        """
        # 检查节点是否存在
        if not self.graph.has_node(start_node_id):
            raise NodeNotFoundError(start_node_id)
        
        if not self.graph.has_node(end_node_id):
            raise NodeNotFoundError(end_node_id)
        
        # 如果起点和终点相同，直接返回
        if start_node_id == end_node_id:
            start_node = self.graph.get_node(start_node_id)
            return {
                'path': [start_node_id],
                'edges': [],
                'total_distance': 0.0,
                'total_time': 0.0,
                'coordinates': [start_node.coordinate]
            }
        
        # 使用Dijkstra算法查找最短路径
        path = self._dijkstra(start_node_id, end_node_id, weight_type, weight_func)
        
        # 获取路径上的边
        edges = self.graph.get_path_edges(path)
        
        # 计算路径总长度和时间
        total_distance = sum(edge.length for edge in edges)
        total_time = sum(edge.get_travel_time() for edge in edges)
        
        # 获取路径上的坐标点
        coordinates = self.graph.get_path_coordinates(path)
        
        return {
            'path': path,
            'edges': edges,
            'total_distance': total_distance,
            'total_time': total_time,
            'coordinates': coordinates
        }
    
    def find_fastest_path(self, start_node_id: str, end_node_id: str) -> Dict[str, Any]:
        """
        查找最快路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            
        返回:
            包含路径信息的字典
            
        异常:
            NodeNotFoundError: 如果起点或终点不存在
            PathNotFoundError: 如果无法找到路径
        """
        return self.find_shortest_path(start_node_id, end_node_id, 'time')
    
    def find_path_with_waypoints(self, waypoints: List[str], 
                               weight_type: str = 'distance') -> Dict[str, Any]:
        """
        查找经过多个途经点的路径
        
        参数:
            waypoints: 途经点ID列表 (包括起点和终点)
            weight_type: 权重类型 ('distance', 'time', 'custom')
            
        返回:
            包含路径信息的字典
            
        异常:
            NodeNotFoundError: 如果任何途经点不存在
            PathNotFoundError: 如果无法找到路径
        """
        if len(waypoints) < 2:
            raise ValueError("至少需要提供起点和终点")
        
        # 检查所有途经点是否存在
        for node_id in waypoints:
            if not self.graph.has_node(node_id):
                raise NodeNotFoundError(node_id)
        
        # 如果只有两个点，直接调用find_shortest_path
        if len(waypoints) == 2:
            return self.find_shortest_path(waypoints[0], waypoints[1], weight_type)
        
        # 分段查找路径
        path_segments = []
        edges_segments = []
        total_distance = 0.0
        total_time = 0.0
        coordinates_segments = []
        
        for i in range(len(waypoints) - 1):
            start = waypoints[i]
            end = waypoints[i + 1]
            
            segment_result = self.find_shortest_path(start, end, weight_type)
            
            # 如果不是第一段，去掉重复的起点
            if i > 0:
                path_segments.extend(segment_result['path'][1:])
            else:
                path_segments.extend(segment_result['path'])
            
            edges_segments.extend(segment_result['edges'])
            total_distance += segment_result['total_distance']
            total_time += segment_result['total_time']
            
            # 如果不是第一段，去掉重复的起点坐标
            if i > 0:
                coordinates_segments.extend(segment_result['coordinates'][1:])
            else:
                coordinates_segments.extend(segment_result['coordinates'])
        
        return {
            'path': path_segments,
            'edges': edges_segments,
            'total_distance': total_distance,
            'total_time': total_time,
            'coordinates': coordinates_segments
        }
    
    def find_alternative_paths(self, start_node_id: str, end_node_id: str, 
                              num_alternatives: int = 3, 
                              weight_type: str = 'distance') -> List[Dict[str, Any]]:
        """
        查找多条备选路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            num_alternatives: 备选路径数量
            weight_type: 权重类型 ('distance', 'time', 'custom')
            
        返回:
            路径信息字典列表
            
        异常:
            NodeNotFoundError: 如果起点或终点不存在
        """
        # 检查节点是否存在
        if not self.graph.has_node(start_node_id):
            raise NodeNotFoundError(start_node_id)
        
        if not self.graph.has_node(end_node_id):
            raise NodeNotFoundError(end_node_id)
        
        # 如果起点和终点相同，直接返回
        if start_node_id == end_node_id:
            start_node = self.graph.get_node(start_node_id)
            return [{
                'path': [start_node_id],
                'edges': [],
                'total_distance': 0.0,
                'total_time': 0.0,
                'coordinates': [start_node.coordinate]
            }]
        
        # 使用Yen's K-最短路径算法查找备选路径
        paths = self._k_shortest_paths(start_node_id, end_node_id, num_alternatives, weight_type)
        
        results = []
        for path in paths:
            try:
                # 获取路径上的边
                edges = self.graph.get_path_edges(path)
                
                # 计算路径总长度和时间
                total_distance = sum(edge.length for edge in edges)
                total_time = sum(edge.get_travel_time() for edge in edges)
                
                # 获取路径上的坐标点
                coordinates = self.graph.get_path_coordinates(path)
                
                results.append({
                    'path': path,
                    'edges': edges,
                    'total_distance': total_distance,
                    'total_time': total_time,
                    'coordinates': coordinates
                })
            except Exception as e:
                # 如果处理某条路径时出错，跳过该路径
                continue
        
        return results
    
    def find_path_avoiding_areas(self, start_node_id: str, end_node_id: str, 
                               avoid_areas: List[List[Coordinate]], 
                               weight_type: str = 'distance') -> Dict[str, Any]:
        """
        查找避开特定区域的路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            avoid_areas: 要避开的区域列表，每个区域是一个坐标点列表，表示多边形
            weight_type: 权重类型 ('distance', 'time', 'custom')
            
        返回:
            包含路径信息的字典
            
        异常:
            NodeNotFoundError: 如果起点或终点不存在
            PathNotFoundError: 如果无法找到路径
        """
        # 检查节点是否存在
        if not self.graph.has_node(start_node_id):
            raise NodeNotFoundError(start_node_id)
        
        if not self.graph.has_node(end_node_id):
            raise NodeNotFoundError(end_node_id)
        
        # 如果起点和终点相同，直接返回
        if start_node_id == end_node_id:
            start_node = self.graph.get_node(start_node_id)
            return {
                'path': [start_node_id],
                'edges': [],
                'total_distance': 0.0,
                'total_time': 0.0,
                'coordinates': [start_node.coordinate]
            }
        
        # 找出在避开区域内的节点
        from ..utils.geometry import is_point_in_polygon
        
        avoid_nodes = set()
        for node_id, node in self.graph.nodes.items():
            for area in avoid_areas:
                if is_point_in_polygon(node.coordinate, area):
                    avoid_nodes.add(node_id)
                    break
        
        # 使用修改后的Dijkstra算法查找路径，避开特定节点
        path = self._dijkstra_with_avoid(start_node_id, end_node_id, avoid_nodes, weight_type)
        
        # 获取路径上的边
        edges = self.graph.get_path_edges(path)
        
        # 计算路径总长度和时间
        total_distance = sum(edge.length for edge in edges)
        total_time = sum(edge.get_travel_time() for edge in edges)
        
        # 获取路径上的坐标点
        coordinates = self.graph.get_path_coordinates(path)
        
        return {
            'path': path,
            'edges': edges,
            'total_distance': total_distance,
            'total_time': total_time,
            'coordinates': coordinates
        }
    
    def find_path_with_constraints(self, start_node_id: str, end_node_id: str, 
                                 constraints: Dict[str, Any], 
                                 weight_type: str = 'distance') -> Dict[str, Any]:
        """
        查找满足特定约束条件的路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            constraints: 约束条件字典，可包含以下键:
                - max_distance: 最大距离 (米)
                - max_time: 最大时间 (小时)
                - avoid_road_types: 要避开的道路类型列表
                - prefer_road_types: 优先选择的道路类型列表
                - avoid_node_ids: 要避开的节点ID列表
                - must_visit_node_ids: 必须经过的节点ID列表
            weight_type: 权重类型 ('distance', 'time', 'custom')
            
        返回:
            包含路径信息的字典
            
        异常:
            NodeNotFoundError: 如果起点或终点不存在
            PathNotFoundError: 如果无法找到路径
        """
        # 检查节点是否存在
        if not self.graph.has_node(start_node_id):
            raise NodeNotFoundError(start_node_id)
        
        if not self.graph.has_node(end_node_id):
            raise NodeNotFoundError(end_node_id)
        
        # 如果起点和终点相同，直接返回
        if start_node_id == end_node_id:
            start_node = self.graph.get_node(start_node_id)
            return {
                'path': [start_node_id],
                'edges': [],
                'total_distance': 0.0,
                'total_time': 0.0,
                'coordinates': [start_node.coordinate]
            }
        
        # 处理必须经过的节点
        must_visit = constraints.get('must_visit_node_ids', [])
        if must_visit:
            # 添加起点和终点
            waypoints = [start_node_id] + must_visit + [end_node_id]
            return self.find_path_with_waypoints(waypoints, weight_type)
        
        # 处理要避开的节点
        avoid_nodes = set(constraints.get('avoid_node_ids', []))
        
        # 处理要避开的道路类型
        avoid_road_types = set(constraints.get('avoid_road_types', []))
        
        # 处理优先选择的道路类型
        prefer_road_types = set(constraints.get('prefer_road_types', []))
        
        # 自定义边权重函数
        def edge_weight_func(start_id: str, end_id: str) -> float:
            edge_id = self.graph.adjacency[start_id][end_id]
            edge = self.graph.edges[edge_id]
            
            # 基础权重
            if weight_type == 'distance':
                weight = edge.length
            elif weight_type == 'time':
                weight = edge.get_travel_time() * 3600  # 转换为秒
            else:  # 'custom'
                weight = edge.length + edge.get_travel_time() * 3600 * 0.1
            
            # 如果是要避开的道路类型，增加权重
            if edge.road_type in avoid_road_types:
                weight *= 10.0
            
            # 如果是优先选择的道路类型，减少权重
            if edge.road_type in prefer_road_types:
                weight *= 0.5
            
            return weight
        
        # 使用修改后的Dijkstra算法查找路径
        path = self._dijkstra_with_custom_weight(start_node_id, end_node_id, avoid_nodes, edge_weight_func)
        
        # 获取路径上的边
        edges = self.graph.get_path_edges(path)
        
        # 计算路径总长度和时间
        total_distance = sum(edge.length for edge in edges)
        total_time = sum(edge.get_travel_time() for edge in edges)
        
        # 检查是否满足最大距离和时间约束
        max_distance = constraints.get('max_distance')
        if max_distance is not None and total_distance > max_distance:
            raise PathNotFoundError(start_node_id, end_node_id, 
                                   f"无法找到满足最大距离约束的路径 (当前: {total_distance:.1f}m, 最大: {max_distance:.1f}m)")
        
        max_time = constraints.get('max_time')
        if max_time is not None and total_time > max_time:
            raise PathNotFoundError(start_node_id, end_node_id, 
                                   f"无法找到满足最大时间约束的路径 (当前: {total_time:.2f}h, 最大: {max_time:.2f}h)")
        
        # 获取路径上的坐标点
        coordinates = self.graph.get_path_coordinates(path)
        
        return {
            'path': path,
            'edges': edges,
            'total_distance': total_distance,
            'total_time': total_time,
            'coordinates': coordinates
        }
    
    def _dijkstra(self, start_node_id: str, end_node_id: str, 
                 weight_type: str = 'distance', weight_func=None) -> List[str]:
        """
        使用Dijkstra算法查找最短路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            weight_type: 权重类型
            weight_func: 自定义权重函数 (start_node_id, end_node_id) -> weight
            
        返回:
            路径上的节点ID列表
            
        异常:
            PathNotFoundError: 如果无法找到路径
        """
        # 初始化
        distances = {node_id: float('inf') for node_id in self.graph.nodes}
        distances[start_node_id] = 0
        previous = {node_id: None for node_id in self.graph.nodes}
        unvisited = set(self.graph.nodes.keys())
        
        while unvisited:
            # 找到距离最小的未访问节点
            current = min(unvisited, key=lambda node_id: distances[node_id])
            
            # 如果当前节点是终点，或者当前节点的距离是无穷大（无法到达），则结束
            if current == end_node_id or distances[current] == float('inf'):
                break
            
            # 移除当前节点
            unvisited.remove(current)
            
            # 更新邻居节点的距离
            for neighbor, edge_id in self.graph.adjacency[current].items():
                if neighbor in unvisited:
                    # 优先使用自定义权重函数
                    if weight_func is not None:
                        weight = weight_func(current, neighbor)
                    else:
                        weight = self.graph.get_edge_weight(current, neighbor, weight_type)
                    
                    new_distance = distances[current] + weight
                    
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
        
        # 如果终点不可达
        if distances[end_node_id] == float('inf'):
            raise PathNotFoundError(start_node_id, end_node_id)
        
        # 构建路径
        path = []
        current = end_node_id
        
        while current:
            path.append(current)
            current = previous[current]
        
        # 反转路径，使其从起点到终点
        return path[::-1]
    
    def _a_star(self, start_node_id: str, end_node_id: str, weight_type: str = 'distance') -> List[str]:
        """
        使用A*算法查找最短路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            weight_type: 权重类型
            
        返回:
            路径上的节点ID列表
            
        异常:
            PathNotFoundError: 如果无法找到路径
        """
        # 启发式函数：估计从当前节点到终点的距离
        def heuristic(node_id):
            # 使用直线距离作为启发式函数
            node = self.graph.nodes[node_id]
            end_node = self.graph.nodes[end_node_id]
            return haversine_distance(node.coordinate, end_node.coordinate)
        
        # 初始化
        open_set = {start_node_id}
        closed_set = set()
        
        g_score = {node_id: float('inf') for node_id in self.graph.nodes}
        g_score[start_node_id] = 0
        
        f_score = {node_id: float('inf') for node_id in self.graph.nodes}
        f_score[start_node_id] = heuristic(start_node_id)
        
        previous = {node_id: None for node_id in self.graph.nodes}
        
        while open_set:
            # 找到f_score最小的节点
            current = min(open_set, key=lambda node_id: f_score[node_id])
            
            # 如果当前节点是终点，则结束
            if current == end_node_id:
                break
            
            # 移动当前节点
            open_set.remove(current)
            closed_set.add(current)
            
            # 更新邻居节点
            for neighbor, edge_id in self.graph.adjacency[current].items():
                if neighbor in closed_set:
                    continue
                
                weight = self.graph.get_edge_weight(current, neighbor, weight_type)
                tentative_g_score = g_score[current] + weight
                
                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue
                
                previous[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor)
        
        # 如果终点不可达
        if previous[end_node_id] is None and start_node_id != end_node_id:
            raise PathNotFoundError(start_node_id, end_node_id)
        
        # 构建路径
        path = []
        current = end_node_id
        
        while current:
            path.append(current)
            current = previous[current]
        
        # 反转路径，使其从起点到终点
        return path[::-1]
    
    def _dijkstra_with_avoid(self, start_node_id: str, end_node_id: str, 
                           avoid_nodes: Set[str], weight_type: str = 'distance') -> List[str]:
        """
        使用修改后的Dijkstra算法查找路径，避开特定节点
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            avoid_nodes: 要避开的节点ID集合
            weight_type: 权重类型
            
        返回:
            路径上的节点ID列表
            
        异常:
            PathNotFoundError: 如果无法找到路径
        """
        # 如果起点或终点在避开节点中，则无法找到路径
        if start_node_id in avoid_nodes or end_node_id in avoid_nodes:
            raise PathNotFoundError(start_node_id, end_node_id, "起点或终点在避开区域内")
        
        # 初始化
        distances = {node_id: float('inf') for node_id in self.graph.nodes if node_id not in avoid_nodes}
        distances[start_node_id] = 0
        previous = {node_id: None for node_id in self.graph.nodes if node_id not in avoid_nodes}
        unvisited = set(node_id for node_id in self.graph.nodes.keys() if node_id not in avoid_nodes)
        
        while unvisited:
            # 找到距离最小的未访问节点
            current = min(unvisited, key=lambda node_id: distances[node_id])
            
            # 如果当前节点是终点，或者当前节点的距离是无穷大（无法到达），则结束
            if current == end_node_id or distances[current] == float('inf'):
                break
            
            # 移除当前节点
            unvisited.remove(current)
            
            # 更新邻居节点的距离
            for neighbor, edge_id in self.graph.adjacency[current].items():
                if neighbor in unvisited:
                    weight = self.graph.get_edge_weight(current, neighbor, weight_type)
                    new_distance = distances[current] + weight
                    
                    if new_distance < distances.get(neighbor, float('inf')):
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
        
        # 如果终点不可达
        if end_node_id not in distances or distances[end_node_id] == float('inf'):
            raise PathNotFoundError(start_node_id, end_node_id)
        
        # 构建路径
        path = []
        current = end_node_id
        
        while current:
            path.append(current)
            current = previous[current]
        
        # 反转路径，使其从起点到终点
        return path[::-1]
    
    def _dijkstra_with_custom_weight(self, start_node_id: str, end_node_id: str, 
                                   avoid_nodes: Set[str], 
                                   weight_func: Callable[[str, str], float]) -> List[str]:
        """
        使用修改后的Dijkstra算法查找路径，使用自定义权重函数
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            avoid_nodes: 要避开的节点ID集合
            weight_func: 自定义权重函数，接受起点和终点ID，返回权重
            
        返回:
            路径上的节点ID列表
            
        异常:
            PathNotFoundError: 如果无法找到路径
        """
        # 如果起点或终点在避开节点中，则无法找到路径
        if start_node_id in avoid_nodes or end_node_id in avoid_nodes:
            raise PathNotFoundError(start_node_id, end_node_id, "起点或终点在避开区域内")
        
        # 初始化
        distances = {node_id: float('inf') for node_id in self.graph.nodes if node_id not in avoid_nodes}
        distances[start_node_id] = 0
        previous = {node_id: None for node_id in self.graph.nodes if node_id not in avoid_nodes}
        unvisited = set(node_id for node_id in self.graph.nodes.keys() if node_id not in avoid_nodes)
        
        while unvisited:
            # 找到距离最小的未访问节点
            current = min(unvisited, key=lambda node_id: distances[node_id])
            
            # 如果当前节点是终点，或者当前节点的距离是无穷大（无法到达），则结束
            if current == end_node_id or distances[current] == float('inf'):
                break
            
            # 移除当前节点
            unvisited.remove(current)
            
            # 更新邻居节点的距离
            for neighbor, edge_id in self.graph.adjacency[current].items():
                if neighbor in unvisited:
                    weight = weight_func(current, neighbor)
                    new_distance = distances[current] + weight
                    
                    if new_distance < distances.get(neighbor, float('inf')):
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
        
        # 如果终点不可达
        if end_node_id not in distances or distances[end_node_id] == float('inf'):
            raise PathNotFoundError(start_node_id, end_node_id)
        
        # 构建路径
        path = []
        current = end_node_id
        
        while current:
            path.append(current)
            current = previous[current]
        
        # 反转路径，使其从起点到终点
        return path[::-1]
    
    def _k_shortest_paths(self, start_node_id: str, end_node_id: str, 
                        k: int, weight_type: str = 'distance') -> List[List[str]]:
        """
        使用Yen's K-最短路径算法查找k条最短路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            k: 路径数量
            weight_type: 权重类型
            
        返回:
            路径列表，每个路径是节点ID列表
        """
        # 找到第一条最短路径
        try:
            shortest_path = self._dijkstra(start_node_id, end_node_id, weight_type)
        except PathNotFoundError:
            return []
        
        # 初始化结果列表和候选路径优先队列
        A = [shortest_path]
        B = []
        
        # 如果只需要一条路径，直接返回
        if k <= 1:
            return A
        
        for i in range(1, k):
            # 对上一条路径的每个节点，尝试找到备选路径
            prev_path = A[i-1]
            
            for j in range(len(prev_path) - 1):
                # 分叉节点
                spur_node = prev_path[j]
                # 从起点到分叉节点的路径
                root_path = prev_path[:j+1]
                
                # 临时移除已有路径中的边，以便找到新的路径
                removed_edges = []
                
                for path in A:
                    if len(path) > j + 1 and path[:j+1] == root_path:
                        u = path[j]
                        v = path[j+1]
                        if self.graph.has_edge_between(u, v):
                            edge_id = self.graph.adjacency[u][v]
                            removed_edges.append((u, v, edge_id))
                            self.graph.remove_edge(edge_id)
                
                # 临时移除根路径中的节点，以避免环路
                removed_nodes = []
                for node in root_path[:-1]:  # 不包括分叉节点
                    if node != spur_node and self.graph.has_node(node):
                        removed_nodes.append(node)
                        self.graph.remove_node(node)
                
                # 从分叉节点到终点查找路径
                try:
                    spur_path = self._dijkstra(spur_node, end_node_id, weight_type)
                    # 组合根路径和分叉路径
                    candidate_path = root_path[:-1] + spur_path
                    
                    # 检查是否已经存在
                    if candidate_path not in A and candidate_path not in [p for _, p in B]:
                        # 计算路径长度
                        path_length = 0.0
                        for i in range(len(candidate_path) - 1):
                            u = candidate_path[i]
                            v = candidate_path[i+1]
                            if self.graph.has_edge_between(u, v):
                                path_length += self.graph.get_edge_weight(u, v, weight_type)
                        
                        heapq.heappush(B, (path_length, candidate_path))
                
                except PathNotFoundError:
                    pass
                
                # 恢复移除的边
                for u, v, edge_id in removed_edges:
                    edge = self.graph.edges[edge_id]
                    self.graph.add_edge(edge)
                
                # 恢复移除的节点
                for node_id in removed_nodes:
                    node = self.graph.nodes[node_id]
                    self.graph.add_node(node)
            
            # 如果没有更多候选路径，结束
            if not B:
                break
            
            # 添加最短的候选路径到结果中
            _, next_path = heapq.heappop(B)
            A.append(next_path)
        
        return A