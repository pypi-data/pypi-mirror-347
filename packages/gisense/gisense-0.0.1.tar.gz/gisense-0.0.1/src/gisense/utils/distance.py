"""
距离计算模块 - 提供各种地理距离计算函数
"""
import math
from typing import Tuple, List, Optional

from ..entities.coordinate import Coordinate


def haversine_distance(coord1: Coordinate, coord2: Coordinate) -> float:
    """
    使用Haversine公式计算两个地理坐标之间的距离
    
    参数:
        coord1: 第一个坐标
        coord2: 第二个坐标
        
    返回:
        两点之间的距离 (米)
    """
    # 地球平均半径 (米)
    EARTH_RADIUS = 6371000
    
    # 将经纬度转换为弧度
    lat1 = math.radians(coord1.latitude)
    lon1 = math.radians(coord1.longitude)
    lat2 = math.radians(coord2.latitude)
    lon2 = math.radians(coord2.longitude)
    
    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = EARTH_RADIUS * c
    
    # 如果两个点都有海拔信息，考虑海拔差异
    if coord1.elevation is not None and coord2.elevation is not None:
        elevation_diff = coord2.elevation - coord1.elevation
        distance = math.sqrt(distance**2 + elevation_diff**2)
    
    return distance


def vincenty_distance(coord1: Coordinate, coord2: Coordinate, iterations: int = 100, epsilon: float = 1e-12) -> float:
    """
    使用Vincenty公式计算两个地理坐标之间的距离 (更精确但计算更复杂)
    
    参数:
        coord1: 第一个坐标
        coord2: 第二个坐标
        iterations: 最大迭代次数
        epsilon: 收敛阈值
        
    返回:
        两点之间的距离 (米)
    """
    # WGS-84椭球体参数
    a = 6378137.0  # 赤道半径 (米)
    f = 1/298.257223563  # 扁率
    b = (1 - f) * a  # 极半径
    
    # 将经纬度转换为弧度
    lat1 = math.radians(coord1.latitude)
    lon1 = math.radians(coord1.longitude)
    lat2 = math.radians(coord2.latitude)
    lon2 = math.radians(coord2.longitude)
    
    # Vincenty公式
    U1 = math.atan((1 - f) * math.tan(lat1))
    U2 = math.atan((1 - f) * math.tan(lat2))
    L = lon2 - lon1
    
    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)
    
    # 初始化lambda
    lmbda = L
    
    for _ in range(iterations):
        sin_lambda = math.sin(lmbda)
        cos_lambda = math.cos(lmbda)
        
        sin_sigma = math.sqrt((cosU2 * sin_lambda) ** 2 + 
                             (cosU1 * sinU2 - sinU1 * cosU2 * cos_lambda) ** 2)
        
        # 如果两点重合
        if sin_sigma == 0:
            return 0.0
        
        cos_sigma = sinU1 * sinU2 + cosU1 * cosU2 * cos_lambda
        sigma = math.atan2(sin_sigma, cos_sigma)
        
        sin_alpha = cosU1 * cosU2 * sin_lambda / sin_sigma
        cos_sq_alpha = 1 - sin_alpha ** 2
        
        # 避免除以零
        if cos_sq_alpha == 0:
            cos_2sigma_m = 0
        else:
            cos_2sigma_m = cos_sigma - 2 * sinU1 * sinU2 / cos_sq_alpha
        
        C = f / 16 * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))
        
        lambda_prev = lmbda
        lmbda = L + (1 - C) * f * sin_alpha * (sigma + C * sin_sigma * 
                (cos_2sigma_m + C * cos_sigma * (-1 + 2 * cos_2sigma_m ** 2)))
        
        # 检查是否收敛
        if abs(lmbda - lambda_prev) < epsilon:
            break
    
    # 计算椭球面距离
    u_sq = cos_sq_alpha * (a ** 2 - b ** 2) / b ** 2
    A = 1 + u_sq / 16384 * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
    B = u_sq / 1024 * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))
    
    delta_sigma = B * sin_sigma * (cos_2sigma_m + B / 4 * (cos_sigma * (-1 + 2 * cos_2sigma_m ** 2) - 
                                  B / 6 * cos_2sigma_m * (-3 + 4 * sin_sigma ** 2) * 
                                  (-3 + 4 * cos_2sigma_m ** 2)))
    
    distance = b * A * (sigma - delta_sigma)
    
    # 如果两个点都有海拔信息，考虑海拔差异
    if coord1.elevation is not None and coord2.elevation is not None:
        elevation_diff = coord2.elevation - coord1.elevation
        distance = math.sqrt(distance**2 + elevation_diff**2)
    
    return distance


def euclidean_distance(coord1: Coordinate, coord2: Coordinate) -> float:
    """
    计算两个坐标的欧几里得距离 (适用于小范围区域的近似计算)
    
    参数:
        coord1: 第一个坐标
        coord2: 第二个坐标
        
    返回:
        两点之间的近似距离 (米)
    """
    # 地球平均半径 (米)
    EARTH_RADIUS = 6371000
    
    # 将经纬度差转换为近似的米数
    # 这是一个简化的计算，仅适用于小范围区域
    lat_diff = math.radians(coord2.latitude - coord1.latitude) * EARTH_RADIUS
    lon_diff = math.radians(coord2.longitude - coord1.longitude) * EARTH_RADIUS * math.cos(math.radians((coord1.latitude + coord2.latitude) / 2))
    
    # 计算平面距离
    distance = math.sqrt(lat_diff**2 + lon_diff**2)
    
    # 如果两个点都有海拔信息，考虑海拔差异
    if coord1.elevation is not None and coord2.elevation is not None:
        elevation_diff = coord2.elevation - coord1.elevation
        distance = math.sqrt(distance**2 + elevation_diff**2)
    
    return distance


def path_length(coordinates: List[Coordinate], method: str = 'haversine') -> float:
    """
    计算路径的总长度
    
    参数:
        coordinates: 路径上的坐标点列表
        method: 距离计算方法 ('haversine', 'vincenty', 'euclidean')
        
    返回:
        路径总长度 (米)
    """
    if len(coordinates) < 2:
        return 0.0
    
    total_length = 0.0
    
    for i in range(len(coordinates) - 1):
        if method == 'vincenty':
            total_length += vincenty_distance(coordinates[i], coordinates[i + 1])
        elif method == 'euclidean':
            total_length += euclidean_distance(coordinates[i], coordinates[i + 1])
        else:  # 默认使用haversine
            total_length += haversine_distance(coordinates[i], coordinates[i + 1])
    
    return total_length


def bearing(coord1: Coordinate, coord2: Coordinate) -> float:
    """
    计算从一个坐标点到另一个坐标点的方位角
    
    参数:
        coord1: 起始坐标
        coord2: 目标坐标
        
    返回:
        方位角 (度，北为0度，顺时针增加)
    """
    # 将经纬度转换为弧度
    lat1 = math.radians(coord1.latitude)
    lon1 = math.radians(coord1.longitude)
    lat2 = math.radians(coord2.latitude)
    lon2 = math.radians(coord2.longitude)
    
    # 计算方位角
    dlon = lon2 - lon1
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing_rad = math.atan2(y, x)
    
    # 转换为度数并确保在0-360范围内
    bearing_deg = math.degrees(bearing_rad)
    bearing_deg = (bearing_deg + 360) % 360
    
    return bearing_deg


def midpoint(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    """
    计算两个坐标的中点
    
    参数:
        coord1: 第一个坐标
        coord2: 第二个坐标
        
    返回:
        中点坐标
    """
    # 将经纬度转换为弧度
    lat1 = math.radians(coord1.latitude)
    lon1 = math.radians(coord1.longitude)
    lat2 = math.radians(coord2.latitude)
    lon2 = math.radians(coord2.longitude)
    
    # 计算中点
    Bx = math.cos(lat2) * math.cos(lon2 - lon1)
    By = math.cos(lat2) * math.sin(lon2 - lon1)
    
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2),
                     math.sqrt((math.cos(lat1) + Bx) ** 2 + By ** 2))
    lon3 = lon1 + math.atan2(By, math.cos(lat1) + Bx)
    
    # 转换回度数
    lat3_deg = math.degrees(lat3)
    lon3_deg = math.degrees(lon3)
    
    # 计算海拔中点（如果有）
    elevation = None
    if coord1.elevation is not None and coord2.elevation is not None:
        elevation = (coord1.elevation + coord2.elevation) / 2
    
    return Coordinate(lat3_deg, lon3_deg, elevation)


def destination_point(start: Coordinate, bearing_deg: float, distance: float) -> Coordinate:
    """
    计算从起点出发，沿指定方位角行进指定距离后的终点坐标
    
    参数:
        start: 起始坐标
        bearing_deg: 方位角 (度，北为0度，顺时针增加)
        distance: 距离 (米)
        
    返回:
        终点坐标
    """
    # 地球平均半径 (米)
    EARTH_RADIUS = 6371000
    
    # 将输入转换为弧度
    lat1 = math.radians(start.latitude)
    lon1 = math.radians(start.longitude)
    bearing_rad = math.radians(bearing_deg)
    
    # 计算角距离
    angular_distance = distance / EARTH_RADIUS
    
    # 计算终点坐标
    lat2 = math.asin(math.sin(lat1) * math.cos(angular_distance) + 
                    math.cos(lat1) * math.sin(angular_distance) * math.cos(bearing_rad))
    
    lon2 = lon1 + math.atan2(math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat1),
                           math.cos(angular_distance) - math.sin(lat1) * math.sin(lat2))
    
    # 转换回度数
    lat2_deg = math.degrees(lat2)
    lon2_deg = math.degrees(lon2)
    
    # 保持经度在-180到180度之间
    lon2_deg = ((lon2_deg + 180) % 360) - 180
    
    return Coordinate(lat2_deg, lon2_deg, start.elevation)