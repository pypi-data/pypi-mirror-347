"""
坐标模块 - 提供经纬度坐标的封装和操作
"""
from dataclasses import dataclass
from typing import Tuple, Optional
import math


@dataclass
class Coordinate:
    """
    经纬度坐标类，封装了地理坐标的基本操作
    
    属性:
        latitude: 纬度 (度)
        longitude: 经度 (度)
        elevation: 海拔高度 (米)，可选
    """
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    
    def __post_init__(self):
        """验证坐标值是否在有效范围内"""
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"纬度必须在 -90 到 90 度之间，当前值: {self.latitude}")
        
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"经度必须在 -180 到 180 度之间，当前值: {self.longitude}")
    
    def to_tuple(self) -> Tuple[float, float]:
        """返回经纬度坐标元组 (longitude, latitude)"""
        return (self.longitude, self.latitude)
    
    def to_tuple_lat_lon(self) -> Tuple[float, float]:
        """返回纬经度坐标元组 (latitude, longitude)"""
        return (self.latitude, self.longitude)
    
    def __str__(self) -> str:
        """返回人类可读的坐标字符串"""
        if self.elevation is not None:
            return f"({self.latitude:.6f}°, {self.longitude:.6f}°, {self.elevation:.1f}m)"
        return f"({self.latitude:.6f}°, {self.longitude:.6f}°)"
    
    def __eq__(self, other) -> bool:
        """判断两个坐标是否相等"""
        if not isinstance(other, Coordinate):
            return False
        
        # 比较经纬度，考虑浮点数精度
        lat_equal = abs(self.latitude - other.latitude) < 1e-10
        lon_equal = abs(self.longitude - other.longitude) < 1e-10
        
        # 如果两个坐标都有海拔信息，则也比较海拔
        if self.elevation is not None and other.elevation is not None:
            elev_equal = abs(self.elevation - other.elevation) < 1e-3
            return lat_equal and lon_equal and elev_equal
        
        # 如果只有一个坐标有海拔信息，则认为不相等
        elif (self.elevation is None) != (other.elevation is None):
            return False
        
        # 如果都没有海拔信息，只比较经纬度
        return lat_equal and lon_equal
    
    def __hash__(self) -> int:
        """计算坐标的哈希值，使其可以用作字典键"""
        # 将经纬度四舍五入到固定精度，以避免浮点数精度问题
        lat_rounded = round(self.latitude, 10)
        lon_rounded = round(self.longitude, 10)
        
        if self.elevation is not None:
            elev_rounded = round(self.elevation, 3)
            return hash((lat_rounded, lon_rounded, elev_rounded))
        
        return hash((lat_rounded, lon_rounded))


def parse_coordinate(coord_str: str) -> Coordinate:
    """
    从字符串解析坐标
    
    支持的格式:
    - "latitude,longitude"
    - "latitude,longitude,elevation"
    
    参数:
        coord_str: 坐标字符串
        
    返回:
        Coordinate 对象
    """
    parts = coord_str.strip().split(',')
    
    if len(parts) < 2:
        raise ValueError(f"无效的坐标格式: {coord_str}，需要至少包含纬度和经度")
    
    try:
        latitude = float(parts[0])
        longitude = float(parts[1])
        
        if len(parts) > 2:
            elevation = float(parts[2])
            return Coordinate(latitude, longitude, elevation)
        
        return Coordinate(latitude, longitude)
    
    except ValueError as e:
        raise ValueError(f"无法解析坐标值: {coord_str}") from e