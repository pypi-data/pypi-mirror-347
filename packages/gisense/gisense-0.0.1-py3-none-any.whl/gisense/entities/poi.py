"""
POI模块 - 提供兴趣点(Point of Interest)的定义和操作
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from uuid import uuid4

from .coordinate import Coordinate


@dataclass
class POI:
    """
    兴趣点类，表示地图上的特定位置点
    
    属性:
        coordinate: 兴趣点的地理坐标
        poi_id: 兴趣点的唯一标识符
        name: 兴趣点名称
        poi_type: 兴趣点类型 (如餐厅、商店、公园等)
        properties: 兴趣点的其他属性
        connected_road_ids: 与该兴趣点相连的道路ID列表
    """
    coordinate: Coordinate
    poi_id: str = field(default_factory=lambda: f"node_{self.coordinate.longitude:.6f}_{self.coordinate.latitude:.6f}")
    name: str = ""
    poi_type: str = "generic"
    properties: Dict[str, Any] = field(default_factory=dict)
    connected_road_ids: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """初始化后的处理"""
        # 确保name不为None
        if self.name is None:
            self.name = ""
        
        # 确保poi_type不为None
        if self.poi_type is None:
            self.poi_type = "generic"
        
        # 确保properties不为None
        if self.properties is None:
            self.properties = {}
        
        # 确保connected_road_ids不为None
        if self.connected_road_ids is None:
            self.connected_road_ids = []
    
    def add_connected_road(self, road_id: str) -> None:
        """
        添加与该兴趣点相连的道路ID
        
        参数:
            road_id: 道路ID
        """
        if road_id not in self.connected_road_ids:
            self.connected_road_ids.append(road_id)
    
    def remove_connected_road(self, road_id: str) -> bool:
        """
        移除与该兴趣点相连的道路ID
        
        参数:
            road_id: 道路ID
            
        返回:
            如果成功移除则返回True，否则返回False
        """
        if road_id in self.connected_road_ids:
            self.connected_road_ids.remove(road_id)
            return True
        return False
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """
        获取兴趣点的属性值
        
        参数:
            key: 属性键
            default: 如果属性不存在，返回的默认值
            
        返回:
            属性值或默认值
        """
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """
        设置兴趣点的属性值
        
        参数:
            key: 属性键
            value: 属性值
        """
        self.properties[key] = value
    
    def __str__(self) -> str:
        """返回人类可读的兴趣点字符串"""
        if self.name:
            return f"{self.name} ({self.poi_type}) at {self.coordinate}"
        return f"{self.poi_type} at {self.coordinate}"
    
    def __eq__(self, other) -> bool:
        """判断两个兴趣点是否相等"""
        if not isinstance(other, POI):
            return False
        return self.poi_id == other.poi_id
    
    def __hash__(self) -> int:
        """计算兴趣点的哈希值，使其可以用作字典键"""
        return hash(self.poi_id)


def create_poi_from_dict(data: Dict[str, Any]) -> POI:
    """
    从字典创建POI对象
    
    参数:
        data: 包含POI数据的字典
        
    返回:
        POI对象
    """
    # 提取必要的坐标信息
    if 'coordinate' in data and isinstance(data['coordinate'], dict):
        coord_data = data['coordinate']
        lat = coord_data.get('latitude')
        lon = coord_data.get('longitude')
        elev = coord_data.get('elevation')
        
        if lat is not None and lon is not None:
            coordinate = Coordinate(lat, lon, elev)
        else:
            raise ValueError("坐标数据缺少纬度或经度")
    elif 'latitude' in data and 'longitude' in data:
        lat = data.get('latitude')
        lon = data.get('longitude')
        elev = data.get('elevation')
        coordinate = Coordinate(lat, lon, elev)
    else:
        raise ValueError("无法从数据中提取坐标信息")
    
    # 提取其他POI属性
    poi_id = data.get('id') or data.get('poi_id', str(uuid4()))
    name = data.get('name', "")
    poi_type = data.get('type') or data.get('poi_type', "generic")
    
    # 提取属性字典，排除已处理的键
    properties = {k: v for k, v in data.items() 
                 if k not in ('coordinate', 'latitude', 'longitude', 'elevation', 
                             'id', 'poi_id', 'name', 'type', 'poi_type', 
                             'connected_road_ids')}
    
    # 提取连接的道路ID
    connected_road_ids = data.get('connected_road_ids', [])
    
    return POI(
        coordinate=coordinate,
        poi_id=poi_id,
        name=name,
        poi_type=poi_type,
        properties=properties,
        connected_road_ids=connected_road_ids
    )