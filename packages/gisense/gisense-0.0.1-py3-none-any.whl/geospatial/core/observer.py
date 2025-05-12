"""
观察者模块 - 提供地理空间环境中的观察者实现
"""
from typing import List, Dict, Any, Optional, Set, Tuple
import math
import time

from ..entities.coordinate import Coordinate
from ..entities.poi import POI
from ..entities.road import Road
from ..utils.distance import haversine_distance, bearing
from .exceptions import ObserverError


class Observer:
    """
    观察者类，代表在地理空间环境中的一个智能体，
    能够感知周围的环境并与地理空间图交互
    """
    
    def __init__(self, location: Coordinate, heading: float = 0.0, 
                 perception_range: float = 100.0, fov: float = 120.0):
        """
        初始化观察者
        
        参数:
            location: 观察者的当前位置坐标
            heading: 观察者的朝向 (度，北为0度，顺时针增加)
            perception_range: 感知范围 (米)
            fov: 视野角度 (度)
        """
        self.location = location
        self.heading = heading
        self.perception_range = perception_range
        self.fov = fov
        self.speed = 0.0  # 当前速度 (米/秒)
        self.last_update_time = time.time()
        self.path_history: List[Coordinate] = [location]  # 历史轨迹
        self.matched_road: Optional[Dict[str, Any]] = None  # 当前匹配的道路信息
        self.visible_pois: List[POI] = []  # 当前可见的POI
        self.visible_roads: List[Road] = []  # 当前可见的道路
    
    def update_location(self, new_location: Coordinate, new_heading: Optional[float] = None) -> None:
        """
        更新观察者的位置和朝向
        
        参数:
            new_location: 新的位置坐标
            new_heading: 新的朝向 (度)，如果为None则根据移动方向计算
        """
        # 计算移动距离
        distance = haversine_distance(self.location, new_location)
        
        # 计算时间差
        current_time = time.time()
        time_diff = current_time - self.last_update_time
        
        # 更新速度 (如果时间差大于0)
        if time_diff > 0:
            self.speed = distance / time_diff
        
        # 如果没有提供新的朝向，则根据移动方向计算
        if new_heading is None and distance > 0.1:  # 只有当移动距离足够大时才更新朝向
            self.heading = bearing(self.location, new_location)
        elif new_heading is not None:
            self.heading = new_heading
        
        # 更新位置和时间
        self.location = new_location
        self.last_update_time = current_time
        
        # 记录历史轨迹
        self.path_history.append(new_location)
    
    def is_poi_visible(self, poi: POI) -> bool:
        """
        判断POI是否在观察者的视野范围内
        
        参数:
            poi: 要检查的POI
            
        返回:
            如果POI在视野范围内则返回True，否则返回False
        """
        # 计算距离
        distance = haversine_distance(self.location, poi.coordinate)
        
        # 如果距离超出感知范围，则不可见
        if distance > self.perception_range:
            return False
        
        # 如果视野角度为360度，则可见
        if self.fov >= 360:
            return True
        
        # 计算POI相对于观察者的方位角
        poi_bearing = bearing(self.location, poi.coordinate)
        
        # 计算方位角差值
        angle_diff = abs((poi_bearing - self.heading + 180) % 360 - 180)
        
        # 如果在视野角度内，则可见
        return angle_diff <= self.fov / 2
    
    def is_road_visible(self, road: Road) -> bool:
        """
        判断道路是否在观察者的视野范围内
        
        参数:
            road: 要检查的道路
            
        返回:
            如果道路在视野范围内则返回True，否则返回False
        """
        # 检查道路的每个线段
        for i in range(len(road.coordinates) - 1):
            start = road.coordinates[i]
            end = road.coordinates[i + 1]
            
            # 计算线段中点
            mid_lat = (start.latitude + end.latitude) / 2
            mid_lon = (start.longitude + end.longitude) / 2
            mid_elev = None
            if start.elevation is not None and end.elevation is not None:
                mid_elev = (start.elevation + end.elevation) / 2
            mid_point = Coordinate(mid_lat, mid_lon, mid_elev)
            
            # 计算到中点的距离
            distance = haversine_distance(self.location, mid_point)
            
            # 如果距离在感知范围内
            if distance <= self.perception_range:
                # 如果视野角度为360度，则可见
                if self.fov >= 360:
                    return True
                
                # 计算中点相对于观察者的方位角
                mid_bearing = bearing(self.location, mid_point)
                
                # 计算方位角差值
                angle_diff = abs((mid_bearing - self.heading + 180) % 360 - 180)
                
                # 如果在视野角度内，则可见
                if angle_diff <= self.fov / 2:
                    return True
        
        return False
    
    def update_perception(self, pois: List[POI], roads: List[Road]) -> Dict[str, Any]:
        """
        更新观察者对周围环境的感知
        
        参数:
            pois: 环境中的所有POI
            roads: 环境中的所有道路
            
        返回:
            包含感知结果的字典
        """
        # 更新可见的POI
        self.visible_pois = [poi for poi in pois if self.is_poi_visible(poi)]
        
        # 更新可见的道路
        self.visible_roads = [road for road in roads if self.is_road_visible(road)]
        
        # 返回感知结果
        return {
            'visible_pois': self.visible_pois,
            'visible_roads': self.visible_roads,
            'location': self.location,
            'heading': self.heading,
            'speed': self.speed,
            'matched_road': self.matched_road
        }
    
    def set_matched_road(self, matched_road: Optional[Dict[str, Any]]) -> None:
        """
        设置观察者当前匹配的道路
        
        参数:
            matched_road: 匹配的道路信息，如果为None表示未匹配到道路
        """
        self.matched_road = matched_road
    
    def get_path_history(self, max_points: Optional[int] = None) -> List[Coordinate]:
        """
        获取观察者的历史轨迹
        
        参数:
            max_points: 最大返回点数，如果为None则返回所有点
            
        返回:
            历史轨迹坐标列表
        """
        if max_points is None or max_points >= len(self.path_history):
            return self.path_history.copy()
        
        # 返回最近的max_points个点
        return self.path_history[-max_points:]
    
    def clear_path_history(self) -> None:
        """清空历史轨迹，但保留当前位置"""
        current_location = self.path_history[-1] if self.path_history else self.location
        self.path_history = [current_location]
    
    def get_nearby_pois(self, max_distance: Optional[float] = None) -> List[Tuple[POI, float]]:
        """
        获取观察者附近的POI及其距离
        
        参数:
            max_distance: 最大距离 (米)，如果为None则使用感知范围
            
        返回:
            (POI, 距离) 元组的列表，按距离升序排序
        """
        if max_distance is None:
            max_distance = self.perception_range
        
        result = []
        for poi in self.visible_pois:
            distance = haversine_distance(self.location, poi.coordinate)
            if distance <= max_distance:
                result.append((poi, distance))
        
        # 按距离排序
        return sorted(result, key=lambda x: x[1])
    
    def get_nearby_roads(self, max_distance: Optional[float] = None) -> List[Tuple[Road, float]]:
        """
        获取观察者附近的道路及其距离
        
        参数:
            max_distance: 最大距离 (米)，如果为None则使用感知范围
            
        返回:
            (Road, 距离) 元组的列表，按距离升序排序
        """
        if max_distance is None:
            max_distance = self.perception_range
        
        result = []
        for road in self.visible_roads:
            # 计算到道路的最小距离
            min_distance = float('inf')
            for i in range(len(road.coordinates) - 1):
                start = road.coordinates[i]
                end = road.coordinates[i + 1]
                
                # 使用点到线段的距离
                from ..utils.geometry import point_to_line_distance
                distance = point_to_line_distance(self.location, start, end)
                min_distance = min(min_distance, distance)
            
            if min_distance <= max_distance:
                result.append((road, min_distance))
        
        # 按距离排序
        return sorted(result, key=lambda x: x[1])
    
    def __str__(self) -> str:
        """返回人类可读的观察者字符串"""
        return f"Observer at {self.location}, heading: {self.heading:.1f}°, speed: {self.speed:.1f} m/s"


class MultiObserverManager:
    """
    多观察者管理器，用于管理和更新多个观察者
    """
    
    def __init__(self):
        """初始化多观察者管理器"""
        self.observers: Dict[str, Observer] = {}
    
    def add_observer(self, observer_id: str, observer: Observer) -> None:
        """
        添加观察者
        
        参数:
            observer_id: 观察者ID
            observer: 观察者对象
        """
        if observer_id in self.observers:
            raise ObserverError(f"观察者ID已存在: {observer_id}")
        
        self.observers[observer_id] = observer
    
    def remove_observer(self, observer_id: str) -> bool:
        """
        移除观察者
        
        参数:
            observer_id: 观察者ID
            
        返回:
            如果成功移除则返回True，否则返回False
        """
        if observer_id in self.observers:
            del self.observers[observer_id]
            return True
        return False
    
    def get_observer(self, observer_id: str) -> Observer:
        """
        获取观察者
        
        参数:
            observer_id: 观察者ID
            
        返回:
            观察者对象
            
        异常:
            ObserverError: 如果观察者不存在
        """
        if observer_id not in self.observers:
            raise ObserverError(f"观察者不存在: {observer_id}")
        
        return self.observers[observer_id]
    
    def update_all_perceptions(self, pois: List[POI], roads: List[Road]) -> Dict[str, Dict[str, Any]]:
        """
        更新所有观察者的感知
        
        参数:
            pois: 环境中的所有POI
            roads: 环境中的所有道路
            
        返回:
            观察者ID到感知结果的映射
        """
        results = {}
        for observer_id, observer in self.observers.items():
            results[observer_id] = observer.update_perception(pois, roads)
        
        return results
    
    def get_observers_in_range(self, location: Coordinate, max_distance: float) -> List[Tuple[str, Observer, float]]:
        """
        获取指定位置附近的观察者
        
        参数:
            location: 位置坐标
            max_distance: 最大距离 (米)
            
        返回:
            (观察者ID, 观察者对象, 距离) 元组的列表，按距离升序排序
        """
        result = []
        for observer_id, observer in self.observers.items():
            distance = haversine_distance(location, observer.location)
            if distance <= max_distance:
                result.append((observer_id, observer, distance))
        
        # 按距离排序
        return sorted(result, key=lambda x: x[2])
    
    def __len__(self) -> int:
        """返回观察者数量"""
        return len(self.observers)
    
    def __contains__(self, observer_id: str) -> bool:
        """检查观察者ID是否存在"""
        return observer_id in self.observers
    
    def __iter__(self):
        """迭代所有观察者ID"""
        return iter(self.observers)
    
    def items(self):
        """迭代所有(观察者ID, 观察者对象)对"""
        return self.observers.items()