"""
地图可视化模块 - 提供地理空间数据的可视化功能
"""
from typing import List, Dict, Any, Tuple, Optional, Union
import math
import os
import warnings

from ..entities.coordinate import Coordinate
from ..entities.poi import POI
from ..entities.road import Road
from ..core.graph import LocationGraph
from ..core.observer import Observer
from ..core.exceptions import VisualizationError


class MapVisualizer:
    """
    地图可视化器，用于可视化地理空间数据
    
    注意：此类依赖于matplotlib库，需要先安装：
    pip install matplotlib
    """
    
    def __init__(self, figsize: Tuple[int, int] = (10, 8), dpi: int = 100):
        """
        初始化地图可视化器
        
        参数:
            figsize: 图形大小 (宽, 高)，单位为英寸
            dpi: 图像分辨率 (每英寸点数)
        """
        try:
            import matplotlib.pyplot as plt
            self.plt = plt
        except ImportError:
            raise ImportError("未安装matplotlib库，请先安装: pip install matplotlib")
        
        self.figsize = figsize
        self.dpi = dpi
        self.fig = None
        self.ax = None
        self.colormap = {
            'motorway': '#FF6347',      # 红色
            'trunk': '#FF8C00',         # 深橙色
            'primary': '#FFA500',       # 橙色
            'secondary': '#FFD700',     # 金色
            'tertiary': '#FFFF00',      # 黄色
            'residential': '#ADFF2F',   # 绿黄色
            'service': '#98FB98',       # 淡绿色
            'pedestrian': '#87CEFA',    # 淡蓝色
            'footway': '#1E90FF',       # 道奇蓝
            'cycleway': '#9370DB',      # 中紫色
            'path': '#D3D3D3',          # 淡灰色
            'junction': '#A9A9A9',      # 深灰色
            'generic': '#808080'        # 灰色
        }
        self.node_colors = {
            'restaurant': '#FF6347',    # 红色
            'cafe': '#8B4513',          # 棕色
            'shop': '#FF8C00',          # 深橙色
            'supermarket': '#FFA500',   # 橙色
            'school': '#FFD700',        # 金色
            'hospital': '#FF0000',      # 鲜红色
            'pharmacy': '#FF69B4',      # 粉红色
            'bank': '#32CD32',          # 酸橙绿
            'park': '#228B22',          # 森林绿
            'cinema': '#4B0082',        # 靛青色
            'hotel': '#1E90FF',         # 道奇蓝
            'fuel': '#B8860B',          # 暗金色
            'parking': '#708090',       # 板岩灰
            'bus_stop': '#9370DB',      # 中紫色
            'railway_station': '#800000', # 栗色
            'junction': '#A9A9A9',      # 深灰色
            'generic': '#808080'        # 灰色
        }
    
    def create_figure(self) -> None:
        """创建新的图形"""
        self.fig, self.ax = self.plt.subplots(figsize=self.figsize, dpi=self.dpi)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.7)
    
    def plot_graph(self, graph: LocationGraph, show_node_labels: bool = False, 
                  show_edge_labels: bool = False, node_size: int = 30, 
                  edge_width: float = 1.0) -> None:
        """
        绘制地理空间图
        
        参数:
            graph: 地理空间图
            show_node_labels: 是否显示节点标签
            show_edge_labels: 是否显示边标签
            node_size: 节点大小
            edge_width: 边宽度
        """
        if self.fig is None or self.ax is None:
            self.create_figure()
        
        # 清除现有图形元素
        self.ax.clear()
        
        # 绘制边 (道路)
        edge_lines = []
        for edge in graph.edges.values():
            # 提取坐标
            lons = [coord.longitude for coord in edge.coordinates]
            lats = [coord.latitude for coord in edge.coordinates]
            
            # 确定颜色
            color = self.colormap.get(edge.road_type, self.colormap['generic'])
            
            # 绘制线段
            line = self.ax.plot(lons, lats, color=color, linewidth=edge_width, alpha=0.8)
            edge_lines.append(line[0])
            
            # 显示边标签
            if show_edge_labels and edge.name:
                # 计算线段中点
                mid_idx = len(edge.coordinates) // 2
                mid_lon = edge.coordinates[mid_idx].longitude
                mid_lat = edge.coordinates[mid_idx].latitude
                
                self.ax.text(mid_lon, mid_lat, edge.name, fontsize=8, 
                           ha='center', va='center', alpha=0.7,
                           bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))
        
        # 绘制节点 (POI)
        node_points = []
        for node in graph.nodes.values():
            # 提取坐标
            lon = node.coordinate.longitude
            lat = node.coordinate.latitude
            
            # 确定颜色
            color = self.node_colors.get(node.poi_type, self.node_colors['generic'])
            
            # 绘制点
            point = self.ax.scatter(lon, lat, color=color, s=node_size, alpha=0.8, zorder=2)
            node_points.append(point)
            
            # 显示节点标签
            if show_node_labels and node.name:
                self.ax.text(lon, lat + 0.0001, node.name, fontsize=8, 
                           ha='center', va='bottom', alpha=0.9,
                           bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7))
        
        # 设置标题和轴标签
        self.ax.set_title('Geographic Network Visualization')
        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('Latitude')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_aspect('equal')
    
    def plot_path(self, path_coords: List[Coordinate], color: str = 'blue', 
                linewidth: float = 2.0, alpha: float = 1.0, label: str = 'Path') -> None:
        """
        绘制路径
        
        参数:
            path_coords: 路径坐标列表
            color: 路径颜色
            linewidth: 线宽
            alpha: 透明度
            label: 图例标签
        """
        if self.fig is None or self.ax is None:
            self.create_figure()
        
        # 提取坐标
        lons = [coord.longitude for coord in path_coords]
        lats = [coord.latitude for coord in path_coords]
        
        # 绘制路径
        self.ax.plot(lons, lats, color=color, linewidth=linewidth, alpha=alpha, label=label, zorder=3)
        
        # 绘制起点和终点
        if path_coords:
            # 起点 (绿色三角形)
            self.ax.scatter(path_coords[0].longitude, path_coords[0].latitude, 
                          color='green', marker='^', s=100, alpha=0.8, zorder=4)
            
            # 终点 (红色星形)
            self.ax.scatter(path_coords[-1].longitude, path_coords[-1].latitude, 
                          color='red', marker='*', s=150, alpha=0.8, zorder=4)
    
    def plot_multiple_paths(self, paths: List[List[Coordinate]], 
                          colors: Optional[List[str]] = None, 
                          labels: Optional[List[str]] = None) -> None:
        """
        绘制多条路径
        
        参数:
            paths: 路径坐标列表的列表
            colors: 路径颜色列表
            labels: 图例标签列表
        """
        if not paths:
            return
        
        if colors is None:
            # 默认颜色列表
            default_colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
            colors = [default_colors[i % len(default_colors)] for i in range(len(paths))]
        
        if labels is None:
            labels = [f'Path {i+1}' for i in range(len(paths))]
        
        for i, path in enumerate(paths):
            color = colors[i % len(colors)]
            label = labels[i] if i < len(labels) else f'Path {i+1}'
            self.plot_path(path, color=color, label=label)
    
    def plot_observer(self, observer: Union[Observer, Coordinate], color: str = 'blue',
                    marker: str = 'o', size: int = 100) -> None:
        """
        绘制观察者或坐标点
        
        参数:
            observer: 观察者对象或坐标对象
            color: 颜色
            marker: 标记
            size: 大小
        """
        if self.fig is None or self.ax is None:
            self.create_figure()
        
        # 处理Coordinate输入
        if isinstance(observer, Coordinate):
            self.ax.scatter(observer.longitude, observer.latitude,
                          color=color, marker=marker, s=size, alpha=0.8, zorder=5)
            return
            
        # 处理Observer输入
        # 绘制观察者位置
        self.ax.scatter(observer.location.longitude, observer.location.latitude,
                      color=color, marker=marker, s=size, alpha=0.8, zorder=5)
        
        # 绘制观察者朝向
        heading_rad = math.radians(observer.heading)
        arrow_length = 0.0005  # 箭头长度
        dx = arrow_length * math.sin(heading_rad)
        dy = arrow_length * math.cos(heading_rad)
        
        self.ax.arrow(observer.location.longitude, observer.location.latitude,
                    dx, dy, head_width=0.0001, head_length=0.0002,
                    fc=color, ec=color, zorder=5)
        
        # 绘制观察者视野范围
        if observer.fov < 360:
            # 计算视野扇形的起始和结束角度
            start_angle = observer.heading - observer.fov / 2
            end_angle = observer.heading + observer.fov / 2
            
            # 生成扇形点
            theta = [math.radians(angle) for angle in range(int(start_angle), int(end_angle) + 1)]
            
            # 计算扇形边缘点的坐标
            edge_x = [observer.location.longitude + observer.perception_range * 0.00001 * math.sin(angle) for angle in theta]
            edge_y = [observer.location.latitude + observer.perception_range * 0.00001 * math.cos(angle) for angle in theta]
            
            # 添加观察者位置作为扇形的起点
            x = [observer.location.longitude] + edge_x
            y = [observer.location.latitude] + edge_y
            
            # 绘制扇形
            self.ax.fill(x, y, color=color, alpha=0.2, zorder=4)
        else:
            # 绘制圆形感知范围
            circle = self.plt.Circle((observer.location.longitude, observer.location.latitude),
                                   observer.perception_range * 0.00001,
                                   color=color, alpha=0.2, zorder=4)
            self.ax.add_patch(circle)
    
    def plot_trajectory(self, trajectory: List[Coordinate], color: str = 'blue', 
                      linewidth: float = 1.5, alpha: float = 0.8, 
                      show_points: bool = True, point_size: int = 20) -> None:
        """
        绘制轨迹
        
        参数:
            trajectory: 轨迹坐标列表
            color: 轨迹颜色
            linewidth: 线宽
            alpha: 透明度
            show_points: 是否显示轨迹点
            point_size: 轨迹点大小
        """
        if self.fig is None or self.ax is None:
            self.create_figure()
        
        # 提取坐标
        lons = [coord.longitude for coord in trajectory]
        lats = [coord.latitude for coord in trajectory]
        
        # 绘制轨迹线
        self.ax.plot(lons, lats, color=color, linewidth=linewidth, alpha=alpha, zorder=3)
        
        # 绘制轨迹点
        if show_points:
            self.ax.scatter(lons, lats, color=color, s=point_size, alpha=alpha, zorder=3)
    
    def plot_heatmap(self, points: List[Coordinate], intensity: Optional[List[float]] = None, 
                    radius: int = 10) -> None:
        """
        绘制热力图
        
        参数:
            points: 点坐标列表
            intensity: 点强度列表，如果为None则所有点强度相同
            radius: 热力图半径
        """
        try:
            from matplotlib.colors import LinearSegmentedColormap
        except ImportError:
            raise ImportError("未安装matplotlib库，请先安装: pip install matplotlib")
        
        if self.fig is None or self.ax is None:
            self.create_figure()
        
        # 提取坐标
        lons = [point.longitude for point in points]
        lats = [point.latitude for point in points]
        
        # 如果没有提供强度，则所有点强度相同
        if intensity is None:
            intensity = [1.0] * len(points)
        
        # 创建热力图
        heatmap = self.ax.hexbin(lons, lats, C=intensity, gridsize=50, cmap='hot', alpha=0.6, zorder=1)
        
        # 添加颜色条
        self.fig.colorbar(heatmap, ax=self.ax, label='Intensity')
    
    def plot_area(self, polygon: List[Coordinate], color: str = 'blue', 
                alpha: float = 0.3, label: Optional[str] = None) -> None:
        """
        绘制区域
        
        参数:
            polygon: 多边形顶点坐标列表
            color: 填充颜色
            alpha: 透明度
            label: 图例标签
        """
        if self.fig is None or self.ax is None:
            self.create_figure()
        
        # 提取坐标
        lons = [point.longitude for point in polygon]
        lats = [point.latitude for point in polygon]
        
        # 确保多边形闭合
        if polygon[0] != polygon[-1]:
            lons.append(polygon[0].longitude)
            lats.append(polygon[0].latitude)
        
        # 绘制多边形
        self.ax.fill(lons, lats, color=color, alpha=alpha, label=label, zorder=2)
        self.ax.plot(lons, lats, color=color, alpha=alpha+0.2, zorder=2)
    
    def plot_events(self, events: List[Dict[str, Any]], event_type: str, 
                  marker: str = 'o', color: str = 'red', size: int = 100) -> None:
        """
        绘制事件
        
        参数:
            events: 事件列表
            event_type: 事件类型 ('turn', 'stop', 'junction_crossing')
            marker: 事件标记
            color: 事件颜色
            size: 事件大小
        """
        if self.fig is None or self.ax is None:
            self.create_figure()
        
        for event in events:
            if 'coordinate' in event:
                coord = event['coordinate']
                self.ax.scatter(coord.longitude, coord.latitude, 
                              color=color, marker=marker, s=size, alpha=0.8, zorder=5)
                
                # 添加事件标签
                if event_type == 'turn' and 'direction' in event:
                    label = f"{event['direction']} ({event['angle']:.1f}°)"
                    self.ax.text(coord.longitude, coord.latitude + 0.0001, label, 
                               fontsize=8, ha='center', va='bottom', alpha=0.9,
                               bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7))
                
                elif event_type == 'stop' and 'duration' in event:
                    label = f"Stop ({event['duration']:.1f}s)"
                    self.ax.text(coord.longitude, coord.latitude + 0.0001, label, 
                               fontsize=8, ha='center', va='bottom', alpha=0.9,
                               bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7))
                
                elif event_type == 'junction_crossing' and 'junction' in event:
                    junction = event['junction']
                    label = f"Junction: {junction.name or junction.poi_id}"
                    self.ax.text(coord.longitude, coord.latitude + 0.0001, label, 
                               fontsize=8, ha='center', va='bottom', alpha=0.9,
                               bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7))
    
    def add_legend(self) -> None:
        """添加图例"""
        if self.fig is None or self.ax is None:
            return
        
        self.ax.legend(loc='best')
    
    def add_scale_bar(self, length_km: float = 1.0, location: str = 'lower right') -> None:
        """
        添加比例尺
        
        参数:
            length_km: 比例尺长度 (千米)
            location: 比例尺位置
        """
        if self.fig is None or self.ax is None:
            return
        
        # 获取当前坐标范围
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        
        # 计算比例尺在经度上的长度
        # 在赤道上，1度经度约等于111.32千米
        # 在纬度lat上，1度经度约等于111.32 * cos(lat)千米
        lat_avg = (ymin + ymax) / 2
        lon_length = length_km / (111.32 * math.cos(math.radians(lat_avg)))
        
        # 计算比例尺位置
        if location == 'lower right':
            x_start = xmax - lon_length - (xmax - xmin) * 0.05
            y_pos = ymin + (ymax - ymin) * 0.05
        elif location == 'lower left':
            x_start = xmin + (xmax - xmin) * 0.05
            y_pos = ymin + (ymax - ymin) * 0.05
        elif location == 'upper right':
            x_start = xmax - lon_length - (xmax - xmin) * 0.05
            y_pos = ymax - (ymax - ymin) * 0.05
        elif location == 'upper left':
            x_start = xmin + (xmax - xmin) * 0.05
            y_pos = ymax - (ymax - ymin) * 0.05
        else:
            x_start = xmin + (xmax - xmin) * 0.05
            y_pos = ymin + (ymax - ymin) * 0.05
        
        # 绘制比例尺
        x_end = x_start + lon_length
        self.ax.plot([x_start, x_end], [y_pos, y_pos], 'k-', linewidth=2)
        self.ax.plot([x_start, x_start], [y_pos - (ymax - ymin) * 0.005, y_pos + (ymax - ymin) * 0.005], 'k-', linewidth=2)
        self.ax.plot([x_end, x_end], [y_pos - (ymax - ymin) * 0.005, y_pos + (ymax - ymin) * 0.005], 'k-', linewidth=2)
        
        # 添加标签
        self.ax.text((x_start + x_end) / 2, y_pos + (ymax - ymin) * 0.01, f'{length_km} km', 
                   ha='center', va='bottom', fontsize=8)
    
    def add_north_arrow(self, location: str = 'upper right') -> None:
        """
        添加指北针
        
        参数:
            location: 指北针位置
        """
        if self.fig is None or self.ax is None:
            return
        
        # 获取当前坐标范围
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        
        # 计算指北针位置
        if location == 'upper right':
            x_pos = xmax - (xmax - xmin) * 0.05
            y_pos = ymax - (ymax - ymin) * 0.05
        elif location == 'upper left':
            x_pos = xmin + (xmax - xmin) * 0.05
            y_pos = ymax - (ymax - ymin) * 0.05
        elif location == 'lower right':
            x_pos = xmax - (xmax - xmin) * 0.05
            y_pos = ymin + (ymax - ymin) * 0.05
        elif location == 'lower left':
            x_pos = xmin + (xmax - xmin) * 0.05
            y_pos = ymin + (ymax - ymin) * 0.05
        else:
            x_pos = xmax - (xmax - xmin) * 0.05
            y_pos = ymax - (ymax - ymin) * 0.05
        
        # 绘制指北针
        arrow_length = (ymax - ymin) * 0.05
        self.ax.arrow(x_pos, y_pos - arrow_length, 0, arrow_length, 
                    head_width=(xmax - xmin) * 0.01, head_length=arrow_length * 0.3, 
                    fc='k', ec='k')
        
        # 添加标签
        self.ax.text(x_pos, y_pos + arrow_length * 0.1, 'N', 
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    def save_figure(self, file_path: str, dpi: Optional[int] = None) -> None:
        """
        保存图形到文件
        
        参数:
            file_path: 文件路径
            dpi: 图像分辨率，如果为None则使用初始化时设置的dpi
        """
        if self.fig is None:
            raise VisualizationError("没有可保存的图形")
        
        if dpi is None:
            dpi = self.dpi
        
        try:
            # 创建目录（如果不存在）
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 保存图形
            self.fig.savefig(file_path, dpi=dpi, bbox_inches='tight')
            print(f"图形已保存到: {file_path}")
        
        except Exception as e:
            raise VisualizationError(f"保存图形失败: {str(e)}")
    
    def show(self) -> None:
        """显示图形"""
        if self.fig is None:
            raise VisualizationError("没有可显示的图形")
        
        self.plt.show()
    
    def close(self) -> None:
        """关闭图形"""
        if self.fig is not None:
            self.plt.close(self.fig)
            self.fig = None
            self.ax = None


class InteractiveMapVisualizer(MapVisualizer):
    """
    交互式地图可视化器，提供交互式地图可视化功能
    
    注意：此类依赖于ipywidgets库，需要先安装：
    pip install ipywidgets
    """
    
    def __init__(self, figsize: Tuple[int, int] = (10, 8), dpi: int = 100):
        """
        初始化交互式地图可视化器
        
        参数:
            figsize: 图形大小 (宽, 高)，单位为英寸
            dpi: 图像分辨率 (每英寸点数)
        """
        super().__init__(figsize, dpi)
        
        try:
            import ipywidgets as widgets
            self.widgets = widgets
        except ImportError:
            warnings.warn("未安装ipywidgets库，交互功能将不可用。请安装: pip install ipywidgets")
            self.widgets = None
    
    def create_interactive_map(self, graph: LocationGraph) -> Any:
        """
        创建交互式地图
        
        参数:
            graph: 地理空间图
            
        返回:
            交互式地图小部件
        """
        if self.widgets is None:
            raise ImportError("未安装ipywidgets库，请先安装: pip install ipywidgets")
        
        # 创建图形
        self.create_figure()
        
        # 绘制图
        self.plot_graph(graph, show_node_labels=False, show_edge_labels=False)
        
        # 创建控件
        show_nodes = self.widgets.Checkbox(value=True, description='显示节点')
        show_node_labels = self.widgets.Checkbox(value=False, description='显示节点标签')
        show_edges = self.widgets.Checkbox(value=True, description='显示边')
        show_edge_labels = self.widgets.Checkbox(value=False, description='显示边标签')
        node_size = self.widgets.IntSlider(value=30, min=5, max=100, step=5, description='节点大小')
        edge_width = self.widgets.FloatSlider(value=1.0, min=0.5, max=5.0, step=0.5, description='边宽度')
        
        # 更新函数
        def update(show_nodes, show_node_labels, show_edges, show_edge_labels, node_size, edge_width):
            self.ax.clear()
            
            # 绘制边
            if show_edges:
                for edge in graph.edges.values():
                    lons = [coord.longitude for coord in edge.coordinates]
                    lats = [coord.latitude for coord in edge.coordinates]
                    color = self.colormap.get(edge.road_type, self.colormap['generic'])
                    self.ax.plot(lons, lats, color=color, linewidth=edge_width, alpha=0.8)
                    
                    if show_edge_labels and edge.name:
                        mid_idx = len(edge.coordinates) // 2
                        mid_lon = edge.coordinates[mid_idx].longitude
                        mid_lat = edge.coordinates[mid_idx].latitude
                        self.ax.text(mid_lon, mid_lat, edge.name, fontsize=8, 
                                   ha='center', va='center', alpha=0.7,
                                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))
            
            # 绘制节点
            if show_nodes:
                for node in graph.nodes.values():
                    lon = node.coordinate.longitude
                    lat = node.coordinate.latitude
                    color = self.node_colors.get(node.poi_type, self.node_colors['generic'])
                    self.ax.scatter(lon, lat, color=color, s=node_size, alpha=0.8, zorder=2)
                    
                    if show_node_labels and node.name:
                        self.ax.text(lon, lat + 0.0001, node.name, fontsize=8, 
                                   ha='center', va='bottom', alpha=0.9,
                                   bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7))
            
            # 设置标题和轴标签
            self.ax.set_title('Interactive Geographic Network Visualization')
            self.ax.set_xlabel('Longitude')
            self.ax.set_ylabel('Latitude')
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.set_aspect('equal')
            
            # 刷新图形
            self.fig.canvas.draw_idle()
        
        # 创建交互式小部件
        interactive_map = self.widgets.interactive(
            update,
            show_nodes=show_nodes,
            show_node_labels=show_node_labels,
            show_edges=show_edges,
            show_edge_labels=show_edge_labels,
            node_size=node_size,
            edge_width=edge_width
        )
        
        return interactive_map
    
    def create_path_explorer(self, graph: LocationGraph, pathfinder) -> Any:
        """
        创建路径探索器
        
        参数:
            graph: 地理空间图
            pathfinder: 路径规划器对象
            
        返回:
            路径探索器小部件
        """
        if self.widgets is None:
            raise ImportError("未安装ipywidgets库，请先安装: pip install ipywidgets")
        
        # 创建图形
        self.create_figure()
        
        # 绘制图
        self.plot_graph(graph, show_node_labels=False, show_edge_labels=False)
        
        # 获取所有节点ID和名称
        node_options = [(f"{node.name} ({node.poi_id})" if node.name else node.poi_id) for node in graph.nodes.values()]
        node_ids = [node.poi_id for node in graph.nodes.values()]
        
        # 创建控件
        start_dropdown = self.widgets.Dropdown(options=node_options, description='起点:')
        end_dropdown = self.widgets.Dropdown(options=node_options, description='终点:')
        algorithm_dropdown = self.widgets.Dropdown(
            options=['dijkstra', 'a_star', 'bfs'],
            value='dijkstra',
            description='算法:'
        )
        weight_dropdown = self.widgets.Dropdown(
            options=['distance', 'time', 'custom'],
            value='distance',
            description='权重:'
        )
        find_button = self.widgets.Button(description='查找路径')
        clear_button = self.widgets.Button(description='清除路径')
        output = self.widgets.Output()
        
        # 更新函数
        def on_find_button_clicked(b):
            with output:
                output.clear_output()
                
                try:
                    start_idx = start_dropdown.index
                    end_idx = end_dropdown.index
                    start_id = node_ids[start_idx]
                    end_id = node_ids[end_idx]
                    algorithm = algorithm_dropdown.value
                    weight_type = weight_dropdown.value
                    
                    print(f"查找从 {start_id} 到 {end_id} 的路径，使用 {algorithm} 算法和 {weight_type} 权重...")
                    
                    # 查找路径
                    path_result = pathfinder.find_shortest_path(start_id, end_id, weight_type)
                    
                    # 清除之前的路径
                    for line in self.ax.lines[:]:
                        if line.get_label() == 'Path':
                            line.remove()
                    
                    # 绘制新路径
                    self.plot_path(path_result['coordinates'])
                    
                    # 显示路径信息
                    print(f"路径长度: {path_result['total_distance']:.1f} 米")
                    print(f"预计时间: {path_result['total_time'] * 60:.1f} 分钟")
                    print(f"节点数量: {len(path_result['path'])}")
                    print(f"边数量: {len(path_result['edges'])}")
                    
                    # 刷新图形
                    self.fig.canvas.draw_idle()
                
                except Exception as e:
                    print(f"错误: {str(e)}")
        
        def on_clear_button_clicked(b):
            with output:
                output.clear_output()
                
                # 清除路径
                for line in self.ax.lines[:]:
                    if line.get_label() == 'Path':
                        line.remove()
                
                # 刷新图形
                self.fig.canvas.draw_idle()
                
                print("路径已清除")
        
        # 绑定按钮事件
        find_button.on_click(on_find_button_clicked)
        clear_button.on_click(on_clear_button_clicked)
        
        # 创建布局
        controls = self.widgets.VBox([
            self.widgets.HBox([start_dropdown, end_dropdown]),
            self.widgets.HBox([algorithm_dropdown, weight_dropdown]),
            self.widgets.HBox([find_button, clear_button]),
            output
        ])
        
        return controls