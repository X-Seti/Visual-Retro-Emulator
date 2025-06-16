"""
X-Seti - June16 2025 - Fixed Canvas with Enhanced Grid Patterns
Enhanced PCB Canvas with FIXED grid patterns and background colors
"""

#this belongs in ui/canvas.py

import os
import sys
from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, 
                           QGraphicsItem, QGraphicsTextItem, QMessageBox)
from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal, QMimeData
from PyQt6.QtGui import (QPainter, QPen, QBrush, QColor, QPixmap, QFont, 
                        QPainterPath, QTransform, QDrag)

# Try to import layer manager
try:
    from core.layer_manager import LayerManager
    print("✓ Layer manager imported successfully")
except ImportError:
    print("⚠️ Layer manager not available, using fallback")
    
    class LayerManager:
        """Fallback layer manager"""
        def __init__(self):
            self.current_layer = "default"
        
        def get_current_layer(self):
            return self.current_layer

def find_component_image_unified(component_name, component_type, package_type=None):
    """Unified function to find component images with multiple search patterns"""
    search_paths = ["images", "images/components", "assets", "assets/components"]
    
    # Generate multiple filename patterns
    base_name = component_name.lower().replace(' ', '_').replace('-', '_')
    patterns = [
        f"{base_name}.png",
        f"{component_type.lower()}_{base_name}.png",
        f"{base_name}_{package_type.lower()}.png" if package_type else f"{base_name}_dip.png",
        f"{component_type.lower()}_{base_name}_{package_type.lower()}.png" if package_type else f"{component_type.lower()}_{base_name}_dip.png"
    ]
    
    # Search in all paths with all patterns
    for search_path in search_paths:
        if os.path.exists(search_path):
            for pattern in patterns:
                full_path = os.path.join(search_path, pattern)
                if os.path.exists(full_path):
                    print(f"✓ Found component image: {full_path}")
                    return full_path
    
    print(f"⚠️ No image found for {component_name} ({component_type})")
    return None

class VisibleBaseComponent(QGraphicsPixmapItem):
    """Enhanced base component with image loading and visual representation"""
    
    def __init__(self, component_name, component_type, package_type="DIP", parent=None):
        super().__init__(parent)
        
        self.component_name = component_name
        self.component_type = component_type
        self.package_type = package_type
        
        # Set item properties
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Load component image
        self._load_component_image()
    
    def _load_component_image(self):
        """Load component image with fallback"""
        image_path = find_component_image_unified(
            self.component_name, 
            self.component_type, 
            self.package_type
        )
        
        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale to reasonable size
                if pixmap.width() > 100 or pixmap.height() > 100:
                    pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, 
                                         Qt.TransformationMode.SmoothTransformation)
                self.setPixmap(pixmap)
                return
        
        # Create fallback rectangle
        fallback_pixmap = QPixmap(80, 60)
        fallback_pixmap.fill(QColor(200, 200, 255))
        self.setPixmap(fallback_pixmap)
    
    def itemChange(self, change, value):
        """Handle item changes"""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Emit position changed signal if parent canvas has it
            if hasattr(self.scene(), 'views') and self.scene().views():
                canvas = self.scene().views()[0]
                if hasattr(canvas, 'component_moved'):
                    canvas.component_moved.emit(self, value, self.pos())
        return super().itemChange(change, value)
    
    def paint(self, painter, option, widget):
        """Custom painting with selection highlight"""
        super().paint(painter, option, widget)
        
        if self.isSelected():
            # Draw selection border
            painter.setPen(QPen(QColor(255, 165, 0), 3))  # Orange selection
            painter.drawRect(self.boundingRect())
    
    def shape(self):
        """Return the shape for selection"""
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

# Import fallbacks for core components
try:
    from core.components import BaseComponent as CoreBaseComponent, ProcessorComponent, HardwareComponent as CoreHardwareComponent
    BaseComponent = CoreBaseComponent
    HardwareComponent = CoreHardwareComponent
    print("✓ Core components imported successfully")
except ImportError:
    BaseComponent = VisibleBaseComponent
    HardwareComponent = VisibleBaseComponent
    ProcessorComponent = VisibleBaseComponent
    print("⚠️ Using fallback components")

# === ENHANCED PCB CANVAS ===
class EnhancedPCBCanvas(QGraphicsView):
    """
    Enhanced PCB Canvas with FIXED Grid Patterns

        TODO:
        No Paper Cut pattern shows?
        Add size adjucted breadboard - Width and Height options, maybe a ruler on the edge of the canvas (adjustable)
        Add size adjusted pinboard - Width and Height - uploaded images DIY-PCB-PinBoard.jpg and DIY-PCB-PinBoard-colors.jpg

        Canvas color options, just shows a black background? (background white or gray and foreground black or some other color options)

        FIXED: Lines, Dots, Crosses

        NEEDS WORK: Proper zoom status does not show in the indecator on the bottum bar.
        Component management - no components can be drag and dropped, i've added how I want the backup components to look if the images/ *.png images don't load or are missing.
        look at the "bp-components.jpg" image needs to be replicated.
    """
    
    # Signals
    component_selected = pyqtSignal(object)
    component_moved = pyqtSignal(object, QPointF, QPointF)
    component_added = pyqtSignal(object)
    component_removed = pyqtSignal(object)
    connection_created = pyqtSignal(object, object, str, str)
    selection_changed = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Initialize managers
        self.layer_manager = LayerManager()
        
        # Component tracking
        self.selected_components = []
        self.components = {}  # id -> component mapping
        self.connections = []
        
        # Canvas settings - FIXED with proper defaults
        self.grid_size = 20
        self.grid_visible = True
        self.snap_to_grid = True
        self.zoom_factor = 1.0
        self.grid_style = "lines"  # lines, dots, crosses, paper cut, paper cut + crosses, breadboard
        self.grid_color = QColor(100, 140, 100)  # Default green
        self.background_color = QColor(25, 25, 35)  # Default dark background
        
        # Interaction state
        self.drag_mode = False
        self.drag_start_pos = None
        self.current_tool = "select"  # select, place, connect, delete
        self.component_to_place = None
        
        # Connection state
        self.connection_start_component = None
        self.connection_start_port = None
        self.temp_connection_line = None
        
        # Setup canvas
        self._setup_canvas()
        self._setup_interactions()
        
        print("✓ Enhanced PCB Canvas initialized with FIXED grid patterns")
    
    def _setup_canvas(self):
        """Setup canvas properties"""
        # Set scene size
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        
        # Configure view
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setRenderHint(QPainter.RenderHint.LosslessImageRendering)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Set background
        self.setBackgroundBrush(QBrush(self.background_color))
    
    def _setup_interactions(self):
        """Setup mouse and keyboard interactions"""
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
    
    # === FIXED GRID DRAWING METHODS ===
    def drawBackground(self, painter, rect):
        """Draw background with FIXED grid patterns"""
        # Draw background color first
        painter.fillRect(rect, self.background_color)
        
        if not self.grid_visible:
            return
        
        style_lower = self.grid_style.lower()
        
        if style_lower == "dots":
            self._draw_dots_pattern(painter, rect)
        elif style_lower == "lines":
            self._draw_lines_pattern(painter, rect)
        elif style_lower == "crosses":
            self._draw_crosses_pattern(painter, rect)
        elif style_lower == "paper cut":
            self._draw_paper_cut_pattern(painter, rect)
        elif style_lower == "paper cut + crosses":
            self._draw_paper_cut_crosses_pattern(painter, rect)
        elif style_lower == "breadboard":
            self._draw_breadboard_pattern(painter, rect)
    
    def _draw_dots_pattern(self, painter, rect):
        """Draw dots at grid intersections"""
        painter.setPen(QPen(self.grid_color, 2))
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        x = left
        while x < rect.right():
            y = top
            while y < rect.bottom():
                painter.drawPoint(x, y)
                y += self.grid_size
            x += self.grid_size
    
    def _draw_lines_pattern(self, painter, rect):
        """FIXED: Draw solid grid lines with proper type conversion"""
        painter.setPen(QPen(self.grid_color, 0.5))
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        # FIXED: Convert all coordinates to int to avoid type errors
        rect_left = int(rect.left())
        rect_right = int(rect.right())
        rect_top = int(rect.top())
        rect_bottom = int(rect.bottom())
        
        # Vertical lines
        x = left
        while x < rect_right:
            painter.drawLine(x, rect_top, x, rect_bottom)
            x += self.grid_size
        
        # Horizontal lines
        y = top
        while y < rect_bottom:
            painter.drawLine(rect_left, y, rect_right, y)
            y += self.grid_size
    
    def _draw_crosses_pattern(self, painter, rect):
        """Draw cross marks at grid intersections"""
        painter.setPen(QPen(self.grid_color, 1))
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        cross_size = 4
        x = left
        while x < rect.right():
            y = top
            while y < rect.bottom():
                # Draw cross
                painter.drawLine(x - cross_size, y, x + cross_size, y)
                painter.drawLine(x, y - cross_size, x, y + cross_size)
                y += self.grid_size
            x += self.grid_size
    
    def _draw_paper_cut_pattern(self, painter, rect):
        """Draw paper cut pattern with dotted lines (like graph paper)"""
        # Create dotted line pen
        pen = QPen(self.grid_color, 1)
        pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)
        
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        # FIXED: Convert coordinates to int
        rect_left = int(rect.left())
        rect_right = int(rect.right())
        rect_top = int(rect.top())
        rect_bottom = int(rect.bottom())
        
        # Vertical dotted lines
        x = left
        while x < rect_right:
            painter.drawLine(x, rect_top, x, rect_bottom)
            x += self.grid_size
        
        # Horizontal dotted lines
        y = top
        while y < rect_bottom:
            painter.drawLine(rect_left, y, rect_right, y)
            y += self.grid_size
    
    def _draw_paper_cut_crosses_pattern(self, painter, rect):
        """Draw paper cut pattern with crosses at intersections"""
        # First draw the dotted lines
        self._draw_paper_cut_pattern(painter, rect)
        
        # Then add crosses at intersections
        painter.setPen(QPen(self.grid_color, 1.5))
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        cross_size = 3
        x = left
        while x < rect.right():
            y = top
            while y < rect.bottom():
                # Draw small cross at intersection
                painter.drawLine(x - cross_size, y, x + cross_size, y)
                painter.drawLine(x, y - cross_size, x, y + cross_size)
                y += self.grid_size
            x += self.grid_size
    
    def _draw_breadboard_pattern(self, painter, rect):
        """Draw realistic breadboard pattern with 0.1" (2.54mm) spacing"""
        # Breadboard spacing: 0.1 inches = 2.54mm = 10 pixels at standard zoom
        hole_spacing = 10
        hole_radius = 1.5
        
        # Calculate grid bounds
        left = int(rect.left()) - (int(rect.left()) % hole_spacing)
        top = int(rect.top()) - (int(rect.top()) % hole_spacing)
        
        # Power rail colors
        power_rail_color = QColor(220, 100, 100)  # Red for power
        ground_rail_color = QColor(100, 100, 220)  # Blue for ground
        tie_point_color = QColor(80, 80, 80)      # Dark gray for tie points
        
        # Draw power rails (top and bottom)
        rail_height = 60
        center_gap = 30
        
        # Top power rails
        top_power_y = top + 20
        top_ground_y = top + 35
        
        # Bottom power rails  
        bottom_power_y = top + rail_height + center_gap + 80
        bottom_ground_y = bottom_power_y + 15
        
        x = left
        while x < rect.right():
            # Top power rail (red line)
            painter.setPen(QPen(power_rail_color, 2))
            painter.drawLine(x - 5, top_power_y, x + 5, top_power_y)
            painter.setBrush(power_rail_color)
            painter.drawEllipse(int(x - hole_radius), int(top_power_y - hole_radius), 
                              int(hole_radius * 2), int(hole_radius * 2))
            
            # Top ground rail (blue line)
            painter.setPen(QPen(ground_rail_color, 2))
            painter.drawLine(x - 5, top_ground_y, x + 5, top_ground_y)
            painter.setBrush(ground_rail_color)
            painter.drawEllipse(int(x - hole_radius), int(top_ground_y - hole_radius),
                              int(hole_radius * 2), int(hole_radius * 2))
            
            # Bottom power rail (red line)
            painter.setPen(QPen(power_rail_color, 2))
            painter.drawLine(x - 5, bottom_power_y, x + 5, bottom_power_y)
            painter.setBrush(power_rail_color)
            painter.drawEllipse(int(x - hole_radius), int(bottom_power_y - hole_radius),
                              int(hole_radius * 2), int(hole_radius * 2))
            
            # Bottom ground rail (blue line)
            painter.setPen(QPen(ground_rail_color, 2))
            painter.drawLine(x - 5, bottom_ground_y, x + 5, bottom_ground_y)
            painter.setBrush(ground_rail_color)
            painter.drawEllipse(int(x - hole_radius), int(bottom_ground_y - hole_radius),
                              int(hole_radius * 2), int(hole_radius * 2))
            
            x += hole_spacing
        
        # Draw main tie point area
        painter.setPen(QPen(tie_point_color, 1))
        painter.setBrush(tie_point_color)
        
        # Top tie point section
        tie_start_y = top + 50
        tie_rows = 5
        
        row = 0
        while row < tie_rows:
            y = tie_start_y + (row * hole_spacing)
            if y > rect.bottom():
                break
                
            col = 0
            x = left
            while x < rect.right():
                # Draw tie point hole
                painter.drawEllipse(int(x - hole_radius), int(y - hole_radius),
                                  int(hole_radius * 2), int(hole_radius * 2))
                
                # Draw connection lines every 5 holes (tie point groups)
                if col % 5 == 0 and col > 0:
                    # Draw separator line
                    painter.setPen(QPen(QColor(150, 150, 150), 0.5))
                    painter.drawLine(int(x - hole_spacing/2), int(y - hole_spacing*2), 
                                   int(x - hole_spacing/2), int(y + hole_spacing*2))
                    painter.setPen(QPen(tie_point_color, 1))
                
                x += hole_spacing
                col += 1
            row += 1
        
        # Center divider channel
        center_y = tie_start_y + (tie_rows * hole_spacing) + center_gap/2
        painter.setPen(QPen(QColor(200, 200, 200), 3))
        painter.drawLine(int(rect.left()), int(center_y), int(rect.right()), int(center_y))
        
        # Bottom tie point section
        bottom_tie_start_y = center_y + center_gap/2
        
        row = 0
        while row < tie_rows:
            y = bottom_tie_start_y + (row * hole_spacing)
            if y > rect.bottom() - 60:  # Leave space for bottom power rails
                break
                
            col = 0
            x = left
            while x < rect.right():
                # Draw tie point hole
                painter.setBrush(tie_point_color)
                painter.setPen(QPen(tie_point_color, 1))
                painter.drawEllipse(int(x - hole_radius), int(y - hole_radius),
                                  int(hole_radius * 2), int(hole_radius * 2))
                
                # Draw connection lines every 5 holes (tie point groups)
                if col % 5 == 0 and col > 0:
                    # Draw separator line
                    painter.setPen(QPen(QColor(150, 150, 150), 0.5))
                    painter.drawLine(int(x - hole_spacing/2), int(y - hole_spacing*2),
                                   int(x - hole_spacing/2), int(y + hole_spacing*2))
                    painter.setPen(QPen(tie_point_color, 1))
                
                x += hole_spacing
                col += 1
            row += 1
    
    # === GRID CONTROL METHODS ===
    def set_grid_visible(self, visible):
        """Set grid visibility"""
        self.grid_visible = visible
        self.viewport().update()
        print(f"🔧 Grid visibility: {visible}")
    
    def set_grid_style(self, style):
        """Set grid style"""
        self.grid_style = style.lower()
        self.viewport().update()
        print(f"🎨 Grid style: {style}")
    
    def set_grid_color(self, color_name):
        """Set grid color by name"""
        color_map = {
            "green": QColor(100, 140, 100),
            "gray": QColor(128, 128, 128),
            "blue": QColor(100, 100, 200),
            "red": QColor(200, 100, 100),
            "custom": QColor(150, 150, 150)  # Default custom
        }
        self.grid_color = color_map.get(color_name.lower(), QColor(100, 140, 100))
        self.viewport().update()
        print(f"🎨 Grid color changed to: {color_name}")
    
    def set_background_color(self, color_name):
        """Set background color by name"""
        color_map = {
            "white": QColor(255, 255, 255),
            "light gray": QColor(240, 240, 240),
            "dark gray": QColor(64, 64, 64),
            "black": QColor(0, 0, 0),
            "cream": QColor(255, 253, 240),
            "custom": QColor(25, 25, 35)  # Default custom
        }
        self.background_color = color_map.get(color_name.lower(), QColor(25, 25, 35))
        self.setBackgroundBrush(QBrush(self.background_color))
        self.viewport().update()
        print(f"🎨 Background color changed to: {color_name}")
    
    def set_grid_spacing(self, spacing):
        """Set grid spacing"""
        if isinstance(spacing, str):
            if "Fine" in spacing:
                self.grid_size = 10
            elif "Medium" in spacing:
                self.grid_size = 20
            elif "Coarse" in spacing:
                self.grid_size = 40
        else:
            self.grid_size = int(spacing) if spacing else 20
        self.viewport().update()
        print(f"🔧 Grid size: {self.grid_size}")
    
    def set_snap_to_grid(self, enabled):
        """Set snap to grid"""
        self.snap_to_grid = enabled
        print(f"🔧 Snap to grid: {enabled}")
    
    # === COMPONENT MANAGEMENT ===
    def add_component(self, component_id: str, component_name: str, component_type: str, 
                     position: QPointF, package_type: str = "DIP"):
        """Add component to canvas"""
        try:
            # Create component instance
            component = VisibleBaseComponent(component_name, component_type, package_type)
            
            # Set position (snap to grid if enabled)
            if self.snap_to_grid:
                snapped_pos = self._snap_to_grid(position)
                component.setPos(snapped_pos)
            else:
                component.setPos(position)
            
            # Add to scene and tracking
            self.scene.addItem(component)
            self.components[component_id] = component
            
            # Emit signal
            self.component_added.emit(component)
            
            print(f"✅ Component added: {component_name} at {component.pos()}")
            return component
            
        except Exception as e:
            print(f"❌ Error adding component: {e}")
            return None
    
    def remove_component(self, component_id: str):
        """Remove component from canvas"""
        if component_id in self.components:
            component = self.components[component_id]
            self.scene.removeItem(component)
            del self.components[component_id]
            self.component_removed.emit(component)
            print(f"🗑️ Component removed: {component_id}")
    
    def clear_all_components(self):
        """Clear all components"""
        for component_id in list(self.components.keys()):
            self.remove_component(component_id)
        self.connections.clear()
        print("🧹 All components cleared")
    
    def get_components(self):
        """Get all components"""
        return dict(self.components)
    
    # === UTILITY METHODS ===
    def _snap_to_grid(self, point: QPointF) -> QPointF:
        """Snap point to grid"""
        if not self.snap_to_grid:
            return point
        
        snapped_x = round(point.x() / self.grid_size) * self.grid_size
        snapped_y = round(point.y() / self.grid_size) * self.grid_size
        return QPointF(snapped_x, snapped_y)
    
    # === MOUSE EVENTS ===
    def wheelEvent(self, event):
        """Handle mouse wheel for zooming"""
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        
        self.scale(zoom_factor, zoom_factor)
        self.zoom_factor *= zoom_factor
    
    def dragEnterEvent(self, event):
        """Handle drag enter"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            print("✅ Drag accepted")
    
    def dropEvent(self, event):
        """Handle drop event"""
        if event.mimeData().hasText():
            drop_data = event.mimeData().text()
            drop_pos = self.mapToScene(event.position().toPoint())
            
            print(f"📦 Drop event: {drop_data} at {drop_pos}")
            
            # Parse drop data (category:component format)
            if ":" in drop_data:
                category, component = drop_data.split(":", 1)
                component_id = f"{component}_{len(self.components)}"
                self.add_component(component_id, component, category, drop_pos)
            
            event.acceptProposedAction()
    
    # === PROJECT MANAGEMENT ===
    def save_to_project_data(self):
        """Save canvas state to project data"""
        return {
            'components': [
                {
                    'id': comp_id,
                    'name': comp.component_name,
                    'type': comp.component_type,
                    'position': {'x': comp.pos().x(), 'y': comp.pos().y()}
                }
                for comp_id, comp in self.components.items()
            ],
            'connections': self.connections,
            'grid_settings': {
                'size': self.grid_size,
                'visible': self.grid_visible,
                'style': self.grid_style,
                'snap_to_grid': self.snap_to_grid,
                'grid_color': self.grid_color.name(),
                'background_color': self.background_color.name()
            }
        }
    
    def load_from_project_data(self, data):
        """Load canvas state from project data"""
        try:
            # Clear existing components
            self.clear_all_components()
            
            # Load components
            if 'components' in data:
                for comp_data in data['components']:
                    position = QPointF(comp_data['position']['x'], comp_data['position']['y'])
                    self.add_component(
                        comp_data['id'],
                        comp_data['name'], 
                        comp_data['type'], 
                        position
                    )
            
            # Load connections
            if 'connections' in data:
                self.connections = data['connections']
            
            # Load grid settings
            if 'grid_settings' in data:
                grid_settings = data['grid_settings']
                self.grid_size = grid_settings.get('size', 20)
                self.grid_visible = grid_settings.get('visible', True)
                self.grid_style = grid_settings.get('style', 'lines')
                self.snap_to_grid = grid_settings.get('snap_to_grid', True)
                
                if 'grid_color' in grid_settings:
                    self.grid_color = QColor(grid_settings['grid_color'])
                if 'background_color' in grid_settings:
                    self.background_color = QColor(grid_settings['background_color'])
                    self.setBackgroundBrush(QBrush(self.background_color))
                
                self.viewport().update()
            
            print(f"✅ Project loaded: {len(self.components)} components")
            
        except Exception as e:
            print(f"❌ Project load error: {e}")

# Backward compatibility alias
PCBCanvas = EnhancedPCBCanvas

# Export
__all__ = ['EnhancedPCBCanvas', 'PCBCanvas', 'VisibleBaseComponent', 'find_component_image_unified']
