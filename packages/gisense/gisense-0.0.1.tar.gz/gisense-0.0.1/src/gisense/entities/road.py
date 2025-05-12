"""
道路模块 - 提供道路的定义和操作
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from uuid import uuid4

from .coordinate import Coordinate


@dataclass
class Road:
    """
    道路类，表示地图上的道路或路段
    
    属性:
        road_id: 道路的唯一标识符
        name: 道路名称
        start_node_id: 起始节点ID
        end_node_id: 终止节点ID
        coordinates: 道路的坐标点列表，表示道路的形状
        road_type: 道路类型 (如主干道、次干道、街道等)
        properties: 道路的其他属性
        length: 道路长度 (米)
        speed_limit: 速度限制 (km/h)
        bidirectional: 是否为双向道路
    """
    start_node_id: str  # 格式应为 node_{经度}_{纬度}
    end_node_id: str    # 格式应为 node_{经度}_{纬度}
    coordinates: List[Coordinate]
    road_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    road_type: str = "street"
    properties: Dict[str, Any] = field(default_factory=dict)
    length: Optional[float] = None
    speed_limit: float = 50.0  # 默认速度限制为50km/h
    bidirectional: bool = True
    
    def __post_init__(self):
        """初始化后的处理"""
        # 确保name不为None
        if self.name is None:
            self.name = ""
        
        # 确保road_type不为None
        if self.road_type is None:
            self.road_type = "street"
        
        # 确保properties不为None
        if self.properties is None:
            self.properties = {}
        
        # 确保coordinates不为None且至少有两个点
        if self.coordinates is None or len(self.coordinates) < 2:
            raise ValueError("道路必须至少包含两个坐标点")
        
        # 如果未提供长度，则计算长度
        if self.length is None:
            self.length = self._calculate_length()
    
    def _calculate_length(self) -> float:
        """
        计算道路长度 (米)
        
        返回:
            道路长度 (米)
        """
        from ..utils.distance import haversine_distance
        
        total_length = 0.0
        for i in range(len(self.coordinates) - 1):
            total_length += haversine_distance(
                self.coordinates[i], self.coordinates[i + 1]
            )
        
        return total_length
    
    def get_start_coordinate(self) -> Coordinate:
        """
        获取道路的起始坐标
        
        返回:
            起始坐标
        """
        return self.coordinates[0]
    
    def get_end_coordinate(self) -> Coordinate:
        """
        获取道路的终止坐标
        
        返回:
            终止坐标
        """
        return self.coordinates[-1]
    
    def get_node_ids(self) -> Tuple[str, str]:
        """
        获取道路连接的节点ID
        
        返回:
            (起始节点ID, 终止节点ID)
        """
        return (self.start_node_id, self.end_node_id)
    
    def get_travel_time(self) -> float:
        """
        计算道路的理论通行时间 (小时)
        
        返回:
            通行时间 (小时)
        """
        # 长度单位为米，速度单位为km/h，需要进行单位转换
        return self.length / 1000 / self.speed_limit
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """
        获取道路的属性值
        
        参数:
            key: 属性键
            default: 如果属性不存在，返回的默认值
            
        返回:
            属性值或默认值
        """
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """
        设置道路的属性值
        
        参数:
            key: 属性键
            value: 属性值
        """
        self.properties[key] = value
    
    def __str__(self) -> str:
        """返回人类可读的道路字符串"""
        if self.name:
            return f"{self.name} ({self.road_type}, {self.length:.1f}m)"
        return f"{self.road_type} road ({self.length:.1f}m)"
    
    def __eq__(self, other) -> bool:
        """判断两条道路是否相等"""
        if not isinstance(other, Road):
            return False
        return self.road_id == other.road_id
    
    def __hash__(self) -> int:
        """计算道路的哈希值，使其可以用作字典键"""
        return hash(self.road_id)


def create_road_from_dict(data: Dict[str, Any]) -> Road:
    """
    从字典创建Road对象
    
    参数:
        data: 包含道路数据的字典
        
    返回:
        Road对象
    """
    # 提取必要的节点ID
    start_node_id = data.get('start_node_id')
    end_node_id = data.get('end_node_id')
    
    if not start_node_id or not end_node_id:
        raise ValueError("道路数据缺少起始或终止节点ID")
    
    # 提取坐标列表
    coordinates = []
    if 'coordinates' in data and isinstance(data['coordinates'], list):
        for coord_data in data['coordinates']:
            if isinstance(coord_data, dict):
                lat = coord_data.get('latitude')
                lon = coord_data.get('longitude')
                elev = coord_data.get('elevation')
                
                if lat is not None and lon is not None:
                    coordinates.append(Coordinate(lat, lon, elev))
            elif isinstance(coord_data, (list, tuple)) and len(coord_data) >= 2:
                lat, lon = coord_data[0], coord_data[1]
                elev = coord_data[2] if len(coord_data) > 2 else None
                coordinates.append(Coordinate(lat, lon, elev))
    
    if len(coordinates) < 2:
        raise ValueError("道路必须至少包含两个坐标点")
    
    # 提取其他道路属性
    road_id = data.get('id') or data.get('road_id', str(uuid4()))
    name = data.get('name', "")
    road_type = data.get('type') or data.get('road_type', "street")
    length = data.get('length')
    speed_limit = data.get('speed_limit', 50.0)
    bidirectional = data.get('bidirectional', True)
    
    # 处理properties字段
    properties = {}
    if 'properties' in data and isinstance(data['properties'], dict):
        properties = data['properties']
    else:
        # 提取属性字典，排除已处理的键
        properties = {k: v for k, v in data.items() 
                     if k not in ('id', 'road_id', 'name', 'type', 'road_type', 
                                 'start_node_id', 'end_node_id', 'coordinates',
                                 'length', 'speed_limit', 'bidirectional',
                                 'properties')}
    
    # 创建Road对象
    road = Road(
        road_id=road_id,
        name=name,
        start_node_id=start_node_id,
        end_node_id=end_node_id,
        coordinates=coordinates,
        road_type=road_type,
        properties=properties,
        length=length,
        speed_limit=speed_limit,
        bidirectional=bidirectional
    )
    
    return road