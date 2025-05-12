"""
几何操作模块 - 提供各种几何计算和坐标匹配功能
"""
import math
from typing import List, Tuple, Optional, Dict, Any
import heapq

from ..entities.coordinate import Coordinate
from ..entities.road import Road
from .distance import haversine_distance, euclidean_distance


def point_to_line_distance(point: Coordinate, line_start: Coordinate, line_end: Coordinate) -> float:
    """
    计算点到线段的最短距离
    
    参数:
        point: 点坐标
        line_start: 线段起点坐标
        line_end: 线段终点坐标
        
    返回:
        点到线段的最短距离 (米)
    """
    # 使用欧几里得距离进行近似计算
    # 将经纬度转换为平面坐标系中的近似值
    # 这种方法在小范围区域内效果较好
    
    # 地球平均半径 (米)
    EARTH_RADIUS = 6371000
    
    # 计算参考点的纬度（弧度）
    ref_lat = math.radians((line_start.latitude + line_end.latitude) / 2)
    
    # 将经纬度转换为近似的米数
    x0 = math.radians(point.longitude) * EARTH_RADIUS * math.cos(ref_lat)
    y0 = math.radians(point.latitude) * EARTH_RADIUS
    
    x1 = math.radians(line_start.longitude) * EARTH_RADIUS * math.cos(ref_lat)
    y1 = math.radians(line_start.latitude) * EARTH_RADIUS
    
    x2 = math.radians(line_end.longitude) * EARTH_RADIUS * math.cos(ref_lat)
    y2 = math.radians(line_end.latitude) * EARTH_RADIUS
    
    # 计算线段长度的平方
    line_length_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
    
    # 如果线段长度为0，则直接返回点到起点的距离
    if line_length_sq == 0:
        return euclidean_distance(point, line_start)
    
    # 计算投影比例
    t = max(0, min(1, ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / line_length_sq))
    
    # 计算投影点坐标
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)
    
    # 计算点到投影点的距离
    distance = math.sqrt((x0 - proj_x) ** 2 + (y0 - proj_y) ** 2)
    
    return distance


def project_point_to_line(point: Coordinate, line_start: Coordinate, line_end: Coordinate) -> Tuple[Coordinate, float]:
    """
    将点投影到线段上，并返回投影点和投影比例
    
    参数:
        point: 点坐标
        line_start: 线段起点坐标
        line_end: 线段终点坐标
        
    返回:
        (投影点坐标, 投影比例t)，其中t在[0,1]范围内表示投影点在线段上的位置
    """
    # 地球平均半径 (米)
    EARTH_RADIUS = 6371000
    
    # 计算参考点的纬度（弧度）
    ref_lat = math.radians((line_start.latitude + line_end.latitude) / 2)
    
    # 将经纬度转换为近似的米数
    x0 = math.radians(point.longitude) * EARTH_RADIUS * math.cos(ref_lat)
    y0 = math.radians(point.latitude) * EARTH_RADIUS
    
    x1 = math.radians(line_start.longitude) * EARTH_RADIUS * math.cos(ref_lat)
    y1 = math.radians(line_start.latitude) * EARTH_RADIUS
    
    x2 = math.radians(line_end.longitude) * EARTH_RADIUS * math.cos(ref_lat)
    y2 = math.radians(line_end.latitude) * EARTH_RADIUS
    
    # 计算线段长度的平方
    line_length_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
    
    # 如果线段长度为0，则直接返回起点和0
    if line_length_sq == 0:
        return line_start, 0.0
    
    # 计算投影比例
    t = max(0, min(1, ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / line_length_sq))
    
    # 计算投影点在平面坐标系中的坐标
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)
    
    # 将平面坐标转换回经纬度
    proj_lon = math.degrees(proj_x / (EARTH_RADIUS * math.cos(ref_lat)))
    proj_lat = math.degrees(proj_y / EARTH_RADIUS)
    
    # 计算海拔（如果有）
    elevation = None
    if line_start.elevation is not None and line_end.elevation is not None:
        elevation = line_start.elevation + t * (line_end.elevation - line_start.elevation)
    
    proj_coord = Coordinate(proj_lat, proj_lon, elevation)
    
    return proj_coord, t


def point_to_polyline_distance(point: Coordinate, polyline: List[Coordinate]) -> Tuple[float, int, float]:
    """
    计算点到折线的最短距离
    
    参数:
        point: 点坐标
        polyline: 折线的坐标点列表
        
    返回:
        (最短距离, 最近线段的索引, 投影比例t)
    """
    if len(polyline) < 2:
        raise ValueError("折线必须至少包含两个点")
    
    min_distance = float('inf')
    min_segment_index = 0
    min_t = 0.0
    
    for i in range(len(polyline) - 1):
        line_start = polyline[i]
        line_end = polyline[i + 1]
        
        proj_point, t = project_point_to_line(point, line_start, line_end)
        distance = haversine_distance(point, proj_point)
        
        if distance < min_distance:
            min_distance = distance
            min_segment_index = i
            min_t = t
    
    return min_distance, min_segment_index, min_t


def interpolate_position(polyline: List[Coordinate], segment_index: int, t: float) -> Coordinate:
    """
    在折线上插值计算位置
    
    参数:
        polyline: 折线的坐标点列表
        segment_index: 线段索引
        t: 插值比例 (0-1)
        
    返回:
        插值位置的坐标
    """
    if segment_index < 0 or segment_index >= len(polyline) - 1:
        raise ValueError(f"线段索引超出范围: {segment_index}")
    
    if not (0 <= t <= 1):
        raise ValueError(f"插值比例必须在0到1之间: {t}")
    
    start = polyline[segment_index]
    end = polyline[segment_index + 1]
    
    # 线性插值经纬度
    lat = start.latitude + t * (end.latitude - start.latitude)
    lon = start.longitude + t * (end.longitude - start.longitude)
    
    # 如果有海拔信息，也进行插值
    elevation = None
    if start.elevation is not None and end.elevation is not None:
        elevation = start.elevation + t * (end.elevation - start.elevation)
    
    return Coordinate(lat, lon, elevation)


def simplify_polyline(polyline: List[Coordinate], tolerance: float = 10.0) -> List[Coordinate]:
    """
    使用Douglas-Peucker算法简化折线
    
    参数:
        polyline: 原始折线的坐标点列表
        tolerance: 简化容差 (米)
        
    返回:
        简化后的折线坐标点列表
    """
    if len(polyline) <= 2:
        return polyline.copy()
    
    def douglas_peucker(points: List[Coordinate], start_idx: int, end_idx: int, tolerance: float) -> List[int]:
        """递归实现Douglas-Peucker算法"""
        # 如果只有两个点，直接返回
        if end_idx - start_idx <= 1:
            return [start_idx, end_idx]
        
        # 找到距离起点和终点连线最远的点
        max_dist = 0
        max_idx = start_idx
        
        for i in range(start_idx + 1, end_idx):
            dist = point_to_line_distance(points[i], points[start_idx], points[end_idx])
            if dist > max_dist:
                max_dist = dist
                max_idx = i
        
        # 如果最大距离小于容差，则直接返回起点和终点
        if max_dist <= tolerance:
            return [start_idx, end_idx]
        
        # 否则递归处理两个子段
        left_indices = douglas_peucker(points, start_idx, max_idx, tolerance)
        right_indices = douglas_peucker(points, max_idx, end_idx, tolerance)
        
        # 合并结果，去除重复的max_idx
        return left_indices[:-1] + right_indices
    
    # 执行Douglas-Peucker算法
    indices = douglas_peucker(polyline, 0, len(polyline) - 1, tolerance)
    
    # 根据保留的索引构建简化后的折线
    return [polyline[i] for i in sorted(indices)]


def is_point_in_polygon(point: Coordinate, polygon: List[Coordinate]) -> bool:
    """
    判断点是否在多边形内部 (使用射线法)
    
    参数:
        point: 点坐标
        polygon: 多边形的顶点坐标列表 (首尾点应相同以闭合多边形)
        
    返回:
        如果点在多边形内部则返回True，否则返回False
    """
    if len(polygon) < 3:
        return False
    
    # 确保多边形是闭合的
    if polygon[0] != polygon[-1]:
        polygon = polygon + [polygon[0]]
    
    # 射线法
    inside = False
    x, y = point.longitude, point.latitude
    
    for i in range(len(polygon) - 1):
        x1, y1 = polygon[i].longitude, polygon[i].latitude
        x2, y2 = polygon[i + 1].longitude, polygon[i + 1].latitude
        
        # 检查点是否在边的y范围内
        if ((y1 <= y < y2) or (y2 <= y < y1)) and \
           (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside
    
    return inside


def convex_hull(points: List[Coordinate]) -> List[Coordinate]:
    """
    计算点集的凸包 (使用Graham扫描算法)
    
    参数:
        points: 点坐标列表
        
    返回:
        凸包顶点坐标列表 (按逆时针排序)
    """
    if len(points) <= 2:
        return points.copy()
    
    # 找到y坐标最小的点（如果有多个，选择x最小的）
    pivot = min(points, key=lambda p: (p.latitude, p.longitude))
    
    # 计算其他点相对于pivot的极角
    def polar_angle(p):
        if p == pivot:
            return -math.pi
        return math.atan2(p.latitude - pivot.latitude, p.longitude - pivot.longitude)
    
    # 按极角排序
    sorted_points = sorted(points, key=polar_angle)
    
    # Graham扫描算法
    hull = [sorted_points[0], sorted_points[1]]
    
    for i in range(2, len(sorted_points)):
        while len(hull) > 1:
            # 检查是否形成左转
            p1, p2, p3 = hull[-2], hull[-1], sorted_points[i]
            
            # 计算叉积
            cross_product = (p2.longitude - p1.longitude) * (p3.latitude - p1.latitude) - \
                           (p2.latitude - p1.latitude) * (p3.longitude - p1.longitude)
            
            # 如果不是左转，则弹出最后一个点
            if cross_product <= 0:
                hull.pop()
            else:
                break
        
        hull.append(sorted_points[i])
    
    return hull


class CoordinateMatcher:
    """
    坐标匹配工具，用于将GPS坐标匹配到道路网络上
    """
    
    def __init__(self, roads: List[Road], max_distance: float = 50.0):
        """
        初始化坐标匹配器
        
        参数:
            roads: 道路列表
            max_distance: 最大匹配距离 (米)
        """
        self.roads = roads
        self.max_distance = max_distance
        self._build_spatial_index()
    
    def _build_spatial_index(self):
        """构建空间索引以加速匹配"""
        # 简单的网格索引
        self.grid_size = 0.001  # 约100米的网格大小
        self.grid_index = {}
        
        for road_idx, road in enumerate(self.roads):
            # 对道路的每个线段进行索引
            for i in range(len(road.coordinates) - 1):
                start = road.coordinates[i]
                end = road.coordinates[i + 1]
                
                # 计算线段的边界框
                min_lat = min(start.latitude, end.latitude)
                max_lat = max(start.latitude, end.latitude)
                min_lon = min(start.longitude, end.longitude)
                max_lon = max(start.longitude, end.longitude)
                
                # 扩展边界框以包含max_distance
                # 粗略估计：0.001度约等于100米
                padding = self.max_distance / 100000
                min_lat -= padding
                max_lat += padding
                min_lon -= padding
                max_lon += padding
                
                # 将线段添加到相交的所有网格中
                min_grid_lat = int(min_lat / self.grid_size)
                max_grid_lat = int(max_lat / self.grid_size)
                min_grid_lon = int(min_lon / self.grid_size)
                max_grid_lon = int(max_lon / self.grid_size)
                
                for grid_lat in range(min_grid_lat, max_grid_lat + 1):
                    for grid_lon in range(min_grid_lon, max_grid_lon + 1):
                        grid_key = (grid_lat, grid_lon)
                        if grid_key not in self.grid_index:
                            self.grid_index[grid_key] = []
                        self.grid_index[grid_key].append((road_idx, i))
    
    def match_coordinate(self, coord: Coordinate) -> Dict[str, Any]:
        """
        将单个坐标匹配到最近的道路上
        
        参数:
            coord: 要匹配的坐标
            
        返回:
            包含匹配结果的字典:
            {
                'road_id': 匹配的道路ID,
                'road': 匹配的道路对象,
                'distance': 到道路的距离 (米),
                'matched_coordinate': 匹配到的道路上的坐标,
                'segment_index': 匹配的道路线段索引,
                'segment_ratio': 在线段上的位置比例 (0-1)
            }
            如果没有找到匹配，则返回None
        """
        # 查询可能的候选道路
        grid_lat = int(coord.latitude / self.grid_size)
        grid_lon = int(coord.longitude / self.grid_size)
        
        candidates = set()
        
        # 检查当前网格和周围的网格
        for lat_offset in [-1, 0, 1]:
            for lon_offset in [-1, 0, 1]:
                grid_key = (grid_lat + lat_offset, grid_lon + lon_offset)
                if grid_key in self.grid_index:
                    candidates.update(self.grid_index[grid_key])
        
        # 如果没有候选道路，返回None
        if not candidates:
            return None
        
        # 找到最近的道路线段
        min_distance = float('inf')
        best_match = None
        
        for road_idx, segment_idx in candidates:
            road = self.roads[road_idx]
            start = road.coordinates[segment_idx]
            end = road.coordinates[segment_idx + 1]
            
            # 计算点到线段的距离和投影点
            proj_coord, t = project_point_to_line(coord, start, end)
            distance = haversine_distance(coord, proj_coord)
            
            if distance < min_distance and distance <= self.max_distance:
                min_distance = distance
                best_match = {
                    'road_id': road.road_id,
                    'road': road,
                    'distance': distance,
                    'matched_coordinate': proj_coord,
                    'segment_index': segment_idx,
                    'segment_ratio': t
                }
        
        return best_match
    
    def match_coordinates(self, coords: List[Coordinate], max_gap: int = 5) -> List[Dict[str, Any]]:
        """
        将一系列坐标匹配到道路上，考虑轨迹的连续性
        
        参数:
            coords: 要匹配的坐标列表
            max_gap: 允许的最大连续未匹配点数
            
        返回:
            匹配结果列表，每个元素是一个字典或None
        """
        if not coords:
            return []
        
        # 首先进行单点匹配
        initial_matches = [self.match_coordinate(coord) for coord in coords]
        
        # 如果点太少，直接返回单点匹配结果
        if len(coords) <= 2:
            return initial_matches
        
        # 使用隐马尔可夫模型进行轨迹匹配
        # 这里使用简化版本的Viterbi算法
        
        # 定义转移概率函数
        def transition_prob(match1, match2, time_diff=1):
            if match1 is None or match2 is None:
                return 0.0
            
            # 如果是同一条道路，概率较高
            if match1['road_id'] == match2['road_id']:
                return 0.8
            
            # 检查道路是否相连
            road1 = match1['road']
            road2 = match2['road']
            
            if road2.start_node_id in [road1.start_node_id, road1.end_node_id] or \
               road2.end_node_id in [road1.start_node_id, road1.end_node_id]:
                return 0.6
            
            # 默认较低概率
            return 0.2
        
        # 定义发射概率函数
        def emission_prob(match):
            if match is None:
                return 0.0
            
            # 距离越近，概率越高
            distance = match['distance']
            if distance <= 5:
                return 0.9
            elif distance <= 15:
                return 0.7
            elif distance <= 30:
                return 0.5
            else:
                return 0.3
        
        # Viterbi算法
        # 对于每个时间步，计算到达每个状态的最大概率路径
        
        # 初始化
        candidates = []
        for i, coord in enumerate(coords):
            # 为每个坐标找到top-k个候选匹配
            grid_lat = int(coord.latitude / self.grid_size)
            grid_lon = int(coord.longitude / self.grid_size)
            
            local_candidates = set()
            for lat_offset in [-1, 0, 1]:
                for lon_offset in [-1, 0, 1]:
                    grid_key = (grid_lat + lat_offset, grid_lon + lon_offset)
                    if grid_key in self.grid_index:
                        local_candidates.update(self.grid_index[grid_key])
            
            time_candidates = []
            for road_idx, segment_idx in local_candidates:
                road = self.roads[road_idx]
                start = road.coordinates[segment_idx]
                end = road.coordinates[segment_idx + 1]
                
                proj_coord, t = project_point_to_line(coord, start, end)
                distance = haversine_distance(coord, proj_coord)
                
                if distance <= self.max_distance:
                    match = {
                        'road_id': road.road_id,
                        'road': road,
                        'distance': distance,
                        'matched_coordinate': proj_coord,
                        'segment_index': segment_idx,
                        'segment_ratio': t
                    }
                    time_candidates.append(match)
            
            # 如果没有候选，添加None
            if not time_candidates:
                time_candidates.append(None)
            
            candidates.append(time_candidates)
        
        # 动态规划表
        dp = [{} for _ in range(len(coords))]
        
        # 初始化第一个时间步
        for match in candidates[0]:
            if match is None:
                dp[0][None] = (emission_prob(None), None)
            else:
                key = (match['road_id'], match['segment_index'])
                dp[0][key] = (emission_prob(match), None)
        
        # 填充动态规划表
        for t in range(1, len(coords)):
            for curr_match in candidates[t]:
                if curr_match is None:
                    curr_key = None
                else:
                    curr_key = (curr_match['road_id'], curr_match['segment_index'])
                
                max_prob = -float('inf')
                best_prev = None
                
                for prev_match in candidates[t-1]:
                    if prev_match is None:
                        prev_key = None
                    else:
                        prev_key = (prev_match['road_id'], prev_match['segment_index'])
                    
                    if prev_key in dp[t-1]:
                        prev_prob, _ = dp[t-1][prev_key]
                        trans_prob = transition_prob(prev_match, curr_match)
                        emis_prob = emission_prob(curr_match)
                        
                        prob = prev_prob + math.log(trans_prob + 1e-10) + math.log(emis_prob + 1e-10)
                        
                        if prob > max_prob:
                            max_prob = prob
                            best_prev = prev_key
                
                if best_prev is not None:
                    dp[t][curr_key] = (max_prob, best_prev)
        
        # 回溯找出最佳路径
        path = [None] * len(coords)
        
        # 找到最后一个时间步的最佳状态
        if not dp[-1]:
            # 如果最后一步没有有效匹配，使用单点匹配结果
            return initial_matches
        
        best_last_key = max(dp[-1].items(), key=lambda x: x[1][0])[0]
        
        # 回溯
        for t in range(len(coords) - 1, -1, -1):
            if best_last_key is None:
                path[t] = None
            else:
                # 找到对应的匹配对象
                for match in candidates[t]:
                    if match is None:
                        if best_last_key is None:
                            path[t] = None
                            break
                    else:
                        key = (match['road_id'], match['segment_index'])
                        if key == best_last_key:
                            path[t] = match
                            break
            
            if t > 0:
                _, best_last_key = dp[t][best_last_key]
        
        return path