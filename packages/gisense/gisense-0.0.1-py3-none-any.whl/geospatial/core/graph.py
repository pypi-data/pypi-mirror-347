"""
图模块 - 提供地理空间网络的图表示
"""
from typing import Dict, List, Set, Tuple, Optional, Any, Iterator, Union
import json
import math
from collections import defaultdict, deque

from ..entities.coordinate import Coordinate
from ..entities.poi import POI
from ..entities.road import Road
from ..utils.distance import haversine_distance
from ..utils.geometry import CoordinateMatcher
from .exceptions import NodeNotFoundError, EdgeNotFoundError, PathNotFoundError


class LocationGraph:
    """
    位置图类，表示地理空间网络
    
    这是系统的核心类，用于存储和管理地理空间网络的节点（POI）和边（道路）
    """
    
    def __init__(self):
        """初始化位置图"""
        # 存储节点 (POI)
        self.nodes: Dict[str, POI] = {}
        
        # 存储边 (Road)
        self.edges: Dict[str, Road] = {}
        
        # 邻接表，用于快速查找与节点相连的边
        self.adjacency: Dict[str, Dict[str, str]] = defaultdict(dict)
        
        # 坐标匹配器
        self.matcher: Optional[CoordinateMatcher] = None
        
        # 边的权重缓存 (用于路径规划)
        self._edge_weights: Dict[Tuple[str, str], float] = {}
    
    def add_node(self, node: POI) -> None:
        """
        添加节点到图中
        
        参数:
            node: POI对象
        """
        self.nodes[node.poi_id] = node
    
    def add_edge(self, edge: Road) -> None:
        """
        添加边到图中
        
        参数:
            edge: Road对象
        """
        # 存储边
        self.edges[edge.road_id] = edge
        
        # 更新邻接表
        start_node_id = edge.start_node_id
        end_node_id = edge.end_node_id
        
        # 添加正向边
        self.adjacency[start_node_id][end_node_id] = edge.road_id
        
        # 如果是双向道路，添加反向边
        if edge.bidirectional:
            self.adjacency[end_node_id][start_node_id] = edge.road_id
        
        # 更新节点的连接道路信息
        if start_node_id in self.nodes:
            self.nodes[start_node_id].add_connected_road(edge.road_id)
        
        if end_node_id in self.nodes:
            self.nodes[end_node_id].add_connected_road(edge.road_id)
        
        # 清除权重缓存
        self._edge_weights = {}
    
    def remove_node(self, node_id: str) -> bool:
        """
        从图中移除节点
        
        参数:
            node_id: 节点ID
            
        返回:
            如果成功移除则返回True，否则返回False
            
        注意:
            移除节点会同时移除与该节点相连的所有边
        """
        if node_id not in self.nodes:
            return False
        
        # 找出与该节点相连的所有边
        connected_edges = set()
        
        # 查找以该节点为起点的边
        for end_id, edge_id in list(self.adjacency[node_id].items()):
            connected_edges.add(edge_id)
        
        # 查找以该节点为终点的边
        for start_id, adj in list(self.adjacency.items()):
            if node_id in adj:
                connected_edges.add(adj[node_id])
        
        # 移除所有相连的边
        for edge_id in connected_edges:
            self.remove_edge(edge_id)
        
        # 移除节点
        del self.nodes[node_id]
        
        # 清除邻接表中的节点
        if node_id in self.adjacency:
            del self.adjacency[node_id]
        
        for start_id in list(self.adjacency.keys()):
            if node_id in self.adjacency[start_id]:
                del self.adjacency[start_id][node_id]
        
        return True
    
    def remove_edge(self, edge_id: str) -> bool:
        """
        从图中移除边
        
        参数:
            edge_id: 边ID
            
        返回:
            如果成功移除则返回True，否则返回False
        """
        if edge_id not in self.edges:
            return False
        
        edge = self.edges[edge_id]
        start_node_id = edge.start_node_id
        end_node_id = edge.end_node_id
        
        # 更新邻接表
        if start_node_id in self.adjacency and end_node_id in self.adjacency[start_node_id]:
            del self.adjacency[start_node_id][end_node_id]
        
        if edge.bidirectional and end_node_id in self.adjacency and start_node_id in self.adjacency[end_node_id]:
            del self.adjacency[end_node_id][start_node_id]
        
        # 更新节点的连接道路信息
        if start_node_id in self.nodes:
            self.nodes[start_node_id].remove_connected_road(edge_id)
        
        if end_node_id in self.nodes:
            self.nodes[end_node_id].remove_connected_road(edge_id)
        
        # 移除边
        del self.edges[edge_id]
        
        # 清除权重缓存
        self._edge_weights = {}
        
        return True
    
    def get_node(self, node_id: str) -> POI:
        """
        获取节点
        
        参数:
            node_id: 节点ID
            
        返回:
            POI对象
            
        异常:
            NodeNotFoundError: 如果节点不存在
        """
        if node_id not in self.nodes:
            raise NodeNotFoundError(node_id)
        
        return self.nodes[node_id]
    
    def get_edge(self, edge_id: str) -> Road:
        """
        获取边
        
        参数:
            edge_id: 边ID
            
        返回:
            Road对象
            
        异常:
            EdgeNotFoundError: 如果边不存在
        """
        if edge_id not in self.edges:
            raise EdgeNotFoundError(None, None, f"边不存在: {edge_id}")
        
        return self.edges[edge_id]
    
    def get_edge_between(self, start_node_id: str, end_node_id: str) -> Road:
        """
        获取连接两个节点的边
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            
        返回:
            Road对象
            
        异常:
            EdgeNotFoundError: 如果边不存在
        """
        if start_node_id not in self.adjacency or end_node_id not in self.adjacency[start_node_id]:
            raise EdgeNotFoundError(start_node_id, end_node_id)
        
        edge_id = self.adjacency[start_node_id][end_node_id]
        return self.edges[edge_id]
    
    def has_node(self, node_id: str) -> bool:
        """
        检查节点是否存在
        
        参数:
            node_id: 节点ID
            
        返回:
            如果节点存在则返回True，否则返回False
        """
        return node_id in self.nodes
    
    def has_edge(self, edge_id: str) -> bool:
        """
        检查边是否存在
        
        参数:
            edge_id: 边ID
            
        返回:
            如果边存在则返回True，否则返回False
        """
        return edge_id in self.edges
    
    def has_edge_between(self, start_node_id: str, end_node_id: str) -> bool:
        """
        检查两个节点之间是否存在边
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            
        返回:
            如果存在边则返回True，否则返回False
        """
        return start_node_id in self.adjacency and end_node_id in self.adjacency[start_node_id]
    
    def get_neighbors(self, node_id: str) -> Dict[str, str]:
        """
        获取节点的邻居节点
        
        参数:
            node_id: 节点ID
            
        返回:
            邻居节点ID到边ID的映射
            
        异常:
            NodeNotFoundError: 如果节点不存在
        """
        if node_id not in self.nodes:
            raise NodeNotFoundError(node_id)
        
        return dict(self.adjacency[node_id])
    
    def get_connected_edges(self, node_id: str) -> List[Road]:
        """
        获取与节点相连的所有边
        
        参数:
            node_id: 节点ID
            
        返回:
            Road对象列表
            
        异常:
            NodeNotFoundError: 如果节点不存在
        """
        if node_id not in self.nodes:
            raise NodeNotFoundError(node_id)
        
        connected_edges = []
        
        # 查找以该节点为起点的边
        for end_id, edge_id in self.adjacency[node_id].items():
            connected_edges.append(self.edges[edge_id])
        
        # 查找以该节点为终点的边 (单向边)
        for start_id, adj in self.adjacency.items():
            if start_id != node_id and node_id in adj:
                edge_id = adj[node_id]
                edge = self.edges[edge_id]
                if not edge.bidirectional:  # 只添加单向边，双向边已在上面添加
                    connected_edges.append(edge)
        
        return connected_edges
    
    def get_edge_weight(self, start_node_id: str, end_node_id: str, weight_type: str = 'distance') -> float:
        """
        获取边的权重
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            weight_type: 权重类型 ('distance', 'time', 'custom')
            
        返回:
            边的权重
            
        异常:
            EdgeNotFoundError: 如果边不存在
        """
        if start_node_id not in self.adjacency or end_node_id not in self.adjacency[start_node_id]:
            raise EdgeNotFoundError(start_node_id, end_node_id)
        
        # 检查缓存
        cache_key = (start_node_id, end_node_id, weight_type)
        if cache_key in self._edge_weights:
            return self._edge_weights[cache_key]
        
        edge_id = self.adjacency[start_node_id][end_node_id]
        edge = self.edges[edge_id]
        
        # 根据权重类型计算权重
        if weight_type == 'distance':
            weight = edge.length
        elif weight_type == 'time':
            weight = edge.get_travel_time() * 3600  # 转换为秒
        elif weight_type == 'custom':
            # 自定义权重，可以根据需要实现
            # 这里使用距离和时间的加权组合
            weight = edge.length + edge.get_travel_time() * 3600 * 0.1
        else:
            raise ValueError(f"未知的权重类型: {weight_type}")
        
        # 缓存权重
        self._edge_weights[cache_key] = weight
        
        return weight
    
    def find_path(self, start_node_id: str, end_node_id: str, 
                  algorithm: str = 'dijkstra', weight_type: str = 'distance') -> List[str]:
        """
        查找从起点到终点的最短路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            algorithm: 路径规划算法 ('dijkstra', 'a_star', 'bfs')
            weight_type: 权重类型 ('distance', 'time', 'custom')
            
        返回:
            路径上的节点ID列表
            
        异常:
            NodeNotFoundError: 如果起点或终点不存在
            PathNotFoundError: 如果无法找到路径
        """
        if start_node_id not in self.nodes:
            raise NodeNotFoundError(start_node_id)
        
        if end_node_id not in self.nodes:
            raise NodeNotFoundError(end_node_id)
        
        # 如果起点和终点相同，直接返回
        if start_node_id == end_node_id:
            return [start_node_id]
        
        # 根据算法选择路径规划方法
        if algorithm == 'dijkstra':
            return self._dijkstra(start_node_id, end_node_id, weight_type)
        elif algorithm == 'a_star':
            return self._a_star(start_node_id, end_node_id, weight_type)
        elif algorithm == 'bfs':
            return self._bfs(start_node_id, end_node_id)
        else:
            raise ValueError(f"未知的路径规划算法: {algorithm}")
    
    def _dijkstra(self, start_node_id: str, end_node_id: str, weight_type: str = 'distance') -> List[str]:
        """
        使用Dijkstra算法查找最短路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            weight_type: 权重类型
            
        返回:
            路径上的节点ID列表
            
        异常:
            PathNotFoundError: 如果无法找到路径
        """
        # 初始化
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[start_node_id] = 0
        previous = {node_id: None for node_id in self.nodes}
        unvisited = set(self.nodes.keys())
        
        while unvisited:
            # 找到距离最小的未访问节点
            current = min(unvisited, key=lambda node_id: distances[node_id])
            
            # 如果当前节点是终点，或者当前节点的距离是无穷大（无法到达），则结束
            if current == end_node_id or distances[current] == float('inf'):
                break
            
            # 移除当前节点
            unvisited.remove(current)
            
            # 更新邻居节点的距离
            for neighbor, edge_id in self.adjacency[current].items():
                if neighbor in unvisited:
                    weight = self.get_edge_weight(current, neighbor, weight_type)
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
            node = self.nodes[node_id]
            end_node = self.nodes[end_node_id]
            return haversine_distance(node.coordinate, end_node.coordinate)
        
        # 初始化
        open_set = {start_node_id}
        closed_set = set()
        
        g_score = {node_id: float('inf') for node_id in self.nodes}
        g_score[start_node_id] = 0
        
        f_score = {node_id: float('inf') for node_id in self.nodes}
        f_score[start_node_id] = heuristic(start_node_id)
        
        previous = {node_id: None for node_id in self.nodes}
        
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
            for neighbor, edge_id in self.adjacency[current].items():
                if neighbor in closed_set:
                    continue
                
                weight = self.get_edge_weight(current, neighbor, weight_type)
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
    
    def _bfs(self, start_node_id: str, end_node_id: str) -> List[str]:
        """
        使用广度优先搜索查找路径
        
        参数:
            start_node_id: 起始节点ID
            end_node_id: 终止节点ID
            
        返回:
            路径上的节点ID列表
            
        异常:
            PathNotFoundError: 如果无法找到路径
        """
        # 初始化
        queue = deque([start_node_id])
        visited = {start_node_id}
        previous = {start_node_id: None}
        
        while queue:
            current = queue.popleft()
            
            # 如果当前节点是终点，则结束
            if current == end_node_id:
                break
            
            # 遍历邻居节点
            for neighbor in self.adjacency[current]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    previous[neighbor] = current
        
        # 如果终点不可达
        if end_node_id not in previous:
            raise PathNotFoundError(start_node_id, end_node_id)
        
        # 构建路径
        path = []
        current = end_node_id
        
        while current:
            path.append(current)
            current = previous[current]
        
        # 反转路径，使其从起点到终点
        return path[::-1]
    
    def get_path_edges(self, path: List[str]) -> List[Road]:
        """
        获取路径上的边
        
        参数:
            path: 路径上的节点ID列表
            
        返回:
            路径上的Road对象列表
            
        异常:
            EdgeNotFoundError: 如果路径上的某两个节点之间不存在边
        """
        if len(path) < 2:
            return []
        
        edges = []
        
        for i in range(len(path) - 1):
            start_node_id = path[i]
            end_node_id = path[i + 1]
            
            if not self.has_edge_between(start_node_id, end_node_id):
                raise EdgeNotFoundError(start_node_id, end_node_id)
            
            edge_id = self.adjacency[start_node_id][end_node_id]
            edges.append(self.edges[edge_id])
        
        return edges
    
    def get_path_coordinates(self, path: List[str]) -> List[Coordinate]:
        """
        获取路径上的坐标点
        
        参数:
            path: 路径上的节点ID列表
            
        返回:
            路径上的坐标点列表
        """
        if not path:
            return []
        
        coordinates = []
        
        # 添加起点坐标
        start_node = self.nodes[path[0]]
        coordinates.append(start_node.coordinate)
        
        # 添加路径上的边的坐标
        for i in range(len(path) - 1):
            start_node_id = path[i]
            end_node_id = path[i + 1]
            
            edge_id = self.adjacency[start_node_id][end_node_id]
            edge = self.edges[edge_id]
            
            # 添加边上的中间点（不包括起点）
            coordinates.extend(edge.coordinates[1:])
        
        return coordinates
    
    def get_path_length(self, path: List[str]) -> float:
        """
        计算路径的总长度
        
        参数:
            path: 路径上的节点ID列表
            
        返回:
            路径总长度 (米)
        """
        if len(path) < 2:
            return 0.0
        
        total_length = 0.0
        
        for i in range(len(path) - 1):
            start_node_id = path[i]
            end_node_id = path[i + 1]
            
            edge_id = self.adjacency[start_node_id][end_node_id]
            edge = self.edges[edge_id]
            
            total_length += edge.length
        
        return total_length
    
    def get_path_travel_time(self, path: List[str]) -> float:
        """
        计算路径的理论通行时间
        
        参数:
            path: 路径上的节点ID列表
            
        返回:
            通行时间 (小时)
        """
        if len(path) < 2:
            return 0.0
        
        total_time = 0.0
        
        for i in range(len(path) - 1):
            start_node_id = path[i]
            end_node_id = path[i + 1]
            
            edge_id = self.adjacency[start_node_id][end_node_id]
            edge = self.edges[edge_id]
            
            total_time += edge.get_travel_time()
        
        return total_time
    
    def find_nodes_in_range(self, center: Coordinate, radius: float) -> List[Tuple[POI, float]]:
        """
        查找指定范围内的节点
        
        参数:
            center: 中心坐标
            radius: 半径 (米)
            
        返回:
            (POI, 距离) 元组的列表，按距离升序排序
        """
        result = []
        
        for node in self.nodes.values():
            distance = haversine_distance(center, node.coordinate)
            if distance <= radius:
                result.append((node, distance))
        
        # 按距离排序
        return sorted(result, key=lambda x: x[1])
    
    def find_nearest_node(self, coord: Coordinate) -> Tuple[POI, float]:
        """
        查找最近的节点
        
        参数:
            coord: 坐标
            
        返回:
            (最近的POI, 距离) 元组
            
        异常:
            ValueError: 如果图中没有节点
        """
        if not self.nodes:
            raise ValueError("图中没有节点")
        
        min_distance = float('inf')
        nearest_node = None
        
        for node in self.nodes.values():
            distance = haversine_distance(coord, node.coordinate)
            if distance < min_distance:
                min_distance = distance
                nearest_node = node
        
        return nearest_node, min_distance
    
    def match_coordinate(self, coord: Coordinate) -> Dict[str, Any]:
        """
        将坐标匹配到最近的道路上
        
        参数:
            coord: 要匹配的坐标
            
        返回:
            包含匹配结果的字典，如果没有匹配到则返回None
        """
        # 如果没有初始化匹配器，则初始化
        if self.matcher is None:
            self.matcher = CoordinateMatcher(list(self.edges.values()))
        
        return self.matcher.match_coordinate(coord)
    
    def match_coordinates(self, coords: List[Coordinate], max_gap: int = 5) -> List[Dict[str, Any]]:
        """
        将一系列坐标匹配到道路上
        
        参数:
            coords: 要匹配的坐标列表
            max_gap: 允许的最大连续未匹配点数
            
        返回:
            匹配结果列表
        """
        # 如果没有初始化匹配器，则初始化
        if self.matcher is None:
            self.matcher = CoordinateMatcher(list(self.edges.values()))
        
        return self.matcher.match_coordinates(coords, max_gap)
    
    def rebuild_matcher(self) -> None:
        """重建坐标匹配器"""
        self.matcher = CoordinateMatcher(list(self.edges.values()))
    
    def get_subgraph(self, node_ids: Set[str]) -> 'LocationGraph':
        """
        获取子图
        
        参数:
            node_ids: 子图中包含的节点ID集合
            
        返回:
            LocationGraph对象
        """
        subgraph = LocationGraph()
        
        # 添加节点
        for node_id in node_ids:
            if node_id in self.nodes:
                subgraph.add_node(self.nodes[node_id])
        
        # 添加边
        for node_id in node_ids:
            if node_id in self.adjacency:
                for end_id, edge_id in self.adjacency[node_id].items():
                    if end_id in node_ids:
                        subgraph.add_edge(self.edges[edge_id])
        
        return subgraph
    
    def get_connected_components(self) -> List[Set[str]]:
        """
        获取图的连通分量
        
        返回:
            连通分量列表，每个连通分量是一个节点ID集合
        """
        components = []
        visited = set()
        
        for node_id in self.nodes:
            if node_id not in visited:
                # 使用BFS查找连通分量
                component = set()
                queue = deque([node_id])
                component.add(node_id)
                visited.add(node_id)
                
                while queue:
                    current = queue.popleft()
                    
                    for neighbor in self.adjacency[current]:
                        if neighbor not in visited:
                            queue.append(neighbor)
                            component.add(neighbor)
                            visited.add(neighbor)
                
                components.append(component)
        
        return components
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取图的统计信息
        
        返回:
            包含统计信息的字典
        """
        # 计算总道路长度
        total_length = sum(edge.length for edge in self.edges.values())
        
        # 计算节点的度分布
        degree_dist = defaultdict(int)
        for node_id in self.nodes:
            degree = len(self.adjacency[node_id])
            degree_dist[degree] += 1
        
        # 计算连通分量
        components = self.get_connected_components()
        
        return {
            'node_count': len(self.nodes),
            'edge_count': len(self.edges),
            'total_length': total_length,
            'degree_distribution': dict(degree_dist),
            'component_count': len(components),
            'largest_component_size': max(len(comp) for comp in components) if components else 0
        }