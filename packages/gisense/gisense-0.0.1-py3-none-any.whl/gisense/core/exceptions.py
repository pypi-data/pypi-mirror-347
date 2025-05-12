"""
异常模块 - 定义地理空间感知系统中使用的自定义异常
"""


class GisenseError(Exception):
    """地理空间感知系统的基础异常类"""
    pass


class NodeNotFoundError(GisenseError):
    """当请求的节点在图中不存在时抛出"""
    
    def __init__(self, node_id, message=None):
        self.node_id = node_id
        self.message = message or f"节点不存在: {node_id}"
        super().__init__(self.message)


class EdgeNotFoundError(GisenseError):
    """当请求的边在图中不存在时抛出"""
    
    def __init__(self, start_node_id, end_node_id, message=None):
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.message = message or f"边不存在: {start_node_id} -> {end_node_id}"
        super().__init__(self.message)


class PathNotFoundError(GisenseError):
    """当无法找到从起点到终点的路径时抛出"""
    
    def __init__(self, start_node_id, end_node_id, message=None):
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.message = message or f"无法找到从 {start_node_id} 到 {end_node_id} 的路径"
        super().__init__(self.message)


class DataFormatError(GisenseError):
    """当输入数据格式不正确时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "数据格式错误"
        super().__init__(self.message)


class CoordinateError(GisenseError):
    """当坐标值无效或操作无效时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "坐标错误"
        super().__init__(self.message)


class MatchingError(GisenseError):
    """当坐标匹配失败时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "坐标匹配失败"
        super().__init__(self.message)


class VisualizationError(GisenseError):
    """当可视化操作失败时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "可视化错误"
        super().__init__(self.message)


class ConfigurationError(GisenseError):
    """当系统配置错误时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "配置错误"
        super().__init__(self.message)


class ObserverError(GisenseError):
    """当观察者操作失败时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "观察者错误"
        super().__init__(self.message)


class AlgorithmError(GisenseError):
    """当算法执行失败时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "算法执行错误"
        super().__init__(self.message)


class IOError(GisenseError):
    """当IO操作失败时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "IO错误"
        super().__init__(self.message)


class ValidationError(GisenseError):
    """当数据验证失败时抛出"""
    
    def __init__(self, message=None):
        self.message = message or "数据验证错误"
        super().__init__(self.message)