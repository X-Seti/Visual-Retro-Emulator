"""
X-Seti - June16 2025 - Enhanced PCB Canvas System
Complete canvas implementation with FIXED drawing coordinate issues
"""

#this belongs in ui/ canvas.py
from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsPixmapItem,
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QCheckBox,
    QSlider, QSpinBox, QPushButton, QColorDialog, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF, QTimer, QObject
from PyQt6.QtGui import (
    QPainter, QPen, QBrush, QColor, QPixmap, QFont, QPainterPath,
    QTransform, QCursor, QImage
)
import os
import math
from pathlib import Path
from typing import Dict, List, Optional, Any

# === VISUAL COMPONENT CLASS ===
class VisibleBaseComponent(QGraphicsPixmapItem):
    """Visual component with fallback rendering"""
    
    def __init__(self, name: str, component_type: str, package_type: str = "DIP", parent=None):
        super().__init__(parent)
        
        self.name = name
        self.component_type = component_type
        self.package_type = package_type
        self.pins = []
        
        # Component properties
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        
        # Try to load component image
        self._load_component_image()
    
    def _load_component_image(self):
        """Load component image with fallback"""
        # Try different image paths
        image_paths = [
            f"images/{self.component_type}_{self.package_type.lower()}.png",
            f"images/{self.name.lower().replace(' ', '_')}.png",
            f"images/components/{self.component_type}.png"
        ]
        
        loaded = False
        for image_path in image_paths:
            if os.path.exists(image_path):
                try:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        # Scale to reasonable size
                        if pixmap.width() > 100 or pixmap.height() > 60:
                            pixmap = pixmap.scaled(80, 50, Qt.AspectRatioMode.KeepAspectRatio, 
                                                 Qt.TransformationMode.SmoothTransformation)
                        self.setPixmap(pixmap)
                        loaded = True
                        break
                except Exception as e:
                    print(f"⚠️ Error loading {image_path}: {e}")
        
        if not loaded:
            # Create fallback pixmap
            self._create_fallback_pixmap()
    
    def _create_fallback_pixmap(self):
        """Create fallback visual representation"""
        width, height = self._get_package_size()
        
        # Create pixmap
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(40, 40, 60))  # Dark blue-gray
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw component body
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.setBrush(QBrush(QColor(60, 60, 80)))
        painter.drawRect(2, 2, width-4, height-4)
        
        # Draw notch or pin 1 indicator
        if self.package_type.upper() in ['DIP', 'PLCC']:
            # Draw notch for DIP packages
            painter.setBrush(QBrush(QColor(40, 40, 60)))
            painter.drawEllipse(width//2 - 3, 2, 6, 6)
        
        # Draw component name/type
        painter.setPen(QPen(QColor(255, 255, 255)))
        font = QFont("Arial", 8)
        painter.setFont(font)
        
        # Truncate text to fit
        text = self.component_type.upper()
        if len(text) > 8:
            text = text[:8]
        
        text_rect = painter.fontMetrics().boundingRect(text)
        x = (width - text_rect.width()) // 2
        y = (height + text_rect.height()) // 2
        painter.drawText(x, y, text)
        
        painter.end()
        self.setPixmap(pixmap)
    
    def _get_package_size(self):
        """Get package dimensions based on type"""
        package_sizes = {
            'DIP': (80, 30),
            'PLCC': (60, 60),
            'QFP': (50, 50),
            'BGA': (40, 40),
            'SOIC': (70, 25),
            'TQFP': (45, 45),
            'LQFP': (50, 50)
        }
        return package_sizes.get(self.package_type.upper(), (80, 40))
    
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
    """Enhanced PCB Canvas with FIXED coordinate type issues"""
    
    # Signals
    component_added = pyqtSignal(object)
    component_removed = pyqtSignal(object)
    component_selected = pyqtSignal(object)
    component_moved = pyqtSignal(object, QPointF, QPointF)
    zoom_changed = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Canvas properties
        self.grid_visible = True
        self.grid_size = 20
        self.grid_style = "lines"  # lines, dots, crosses, paper cut, breadboard
        self.grid_color = QColor(100, 140, 100, 180)
        self.background_color = QColor(255, 255, 255)  # White background
        self.snap_to_grid = True
        
        # Ruler properties  
        self.show_ruler = False
        self.ruler_color = QColor(100, 100, 100)
        
        # Component tracking
        self.components = {}
        self.selected_components = set()
        self.zoom_factor = 1.0
        
        # Setup canvas
        self._setup_canvas()
        self._setup_interactions()
        
        print("✅ Enhanced PCB Canvas initialized with FIXED drawing")
    
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
        
        # Set background brush
        self.setBackgroundBrush(QBrush(self.background_color))
    
    def _setup_interactions(self):
        """Setup mouse and keyboard interactions"""
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
    
    # === FIXED DRAWING METHODS ===
    def drawBackground(self, painter, rect):
        """FIXED: Draw background with proper coordinate types"""
        # Draw background color first
        painter.fillRect(rect, self.background_color)
        
        # Draw ruler if enabled
        try:
            self._draw_ruler(painter, rect)
        except Exception as e:
            print(f"⚠️ Ruler drawing error: {e}")
        
        # Draw grid if enabled
        if not self.grid_visible:
            return
            
        # Grid drawing with FIXED coordinates
        style_lower = self.grid_style.lower()
        
        if style_lower == "dots":
            self._draw_dots_pattern(painter, rect)
        elif style_lower == "lines":
            self._draw_lines_pattern(painter, rect)
        elif style_lower == "crosses":
            self._draw_crosses_pattern(painter, rect)
        elif style_lower == "paper cut":
            self._draw_paper_cut_pattern(painter, rect)
        elif style_lower == "breadboard":
            self._draw_breadboard_pattern(painter, rect)
    
    def _draw_ruler(self, painter, rect):
        """FIXED: Draw ruler marks with proper coordinate types"""
        if not self.show_ruler:
            return
        
        # FIXED: Convert all float coordinates to int for PyQt6 compatibility
        painter.setPen(QPen(self.ruler_color, 1))
        
        # Ruler settings
        major_tick = 50  # Major tick every 50 pixels
        minor_tick = 10  # Minor tick every 10 pixels
        
        # FIXED: Convert rect boundaries to int to avoid TypeError
        rect_left = int(rect.left())
        rect_right = int(rect.right())
        rect_top = int(rect.top())
        rect_bottom = int(rect.bottom())
        
        # Horizontal ruler (top edge)
        if rect_top <= 20:  # Only show if top edge is visible
            y_pos = max(rect_top, 0)
            
            # Calculate starting position aligned to grid
            start_x = (rect_left // minor_tick) * minor_tick
            
            x = start_x
            while x <= rect_right:
                screen_pos = int(x)  # FIXED: Convert float to int
                
                if x % major_tick == 0:
                    # Major tick mark - FIXED: All coordinates are int
                    painter.drawLine(screen_pos, y_pos, screen_pos, y_pos + 15)
                    # Add measurement text for major ticks
                    if x > rect_left + 20:  # Avoid overlapping with edge
                        painter.drawText(screen_pos + 2, y_pos + 12, f"{int(x)}")
                elif x % minor_tick == 0:
                    # Minor tick mark - FIXED: All coordinates converted to int
                    painter.drawLine(screen_pos, rect_top, screen_pos, rect_top + 10)
                
                x += minor_tick
        
        # Vertical ruler (left edge) 
        if rect_left <= 20:  # Only show if left edge is visible
            x_pos = max(rect_left, 0)
            
            # Calculate starting position aligned to grid
            start_y = (rect_top // minor_tick) * minor_tick
            
            y = start_y
            while y <= rect_bottom:
                screen_pos = int(y)  # FIXED: Convert float to int
                
                if y % major_tick == 0:
                    # Major tick mark - FIXED: All coordinates are int
                    painter.drawLine(x_pos, screen_pos, x_pos + 15, screen_pos)
                    # Add measurement text for major ticks
                    if y > rect_top + 20:  # Avoid overlapping with edge
                        painter.drawText(x_pos + 2, screen_pos - 2, f"{int(y)}")
                elif y % minor_tick == 0:
                    # Minor tick mark - FIXED: All coordinates converted to int
                    painter.drawLine(rect_left, screen_pos, rect_left + 10, screen_pos)
                
                y += minor_tick

    def _draw_dots_pattern(self, painter, rect):
        """FIXED: Draw dots with proper coordinates"""
        painter.setPen(QPen(self.grid_color, 2))
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        x = left
        while x < rect.right():
            y = top
            while y < rect.bottom():
                painter.drawPoint(int(x), int(y))  # FIXED: Convert to int
                y += self.grid_size
            x += self.grid_size

    def _draw_lines_pattern(self, painter, rect):
        """FIXED: Draw lines with proper coordinates"""
        painter.setPen(QPen(self.grid_color, 0.5))
        
        # FIXED: Convert ALL coordinates to int
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        rect_left = int(rect.left())
        rect_right = int(rect.right())
        rect_top = int(rect.top())
        rect_bottom = int(rect.bottom())
        
        # Vertical lines
        x = left
        while x < rect_right:
            painter.drawLine(int(x), rect_top, int(x), rect_bottom)  # FIXED
            x += self.grid_size
        
        # Horizontal lines
        y = top
        while y < rect_bottom:
            painter.drawLine(rect_left, int(y), rect_right, int(y))  # FIXED
            y += self.grid_size

    def _draw_crosses_pattern(self, painter, rect):
        """FIXED: Draw crosses with proper coordinates"""
        painter.setPen(QPen(self.grid_color, 1))
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        cross_size = 4
        x = left
        while x < rect.right():
            y = top
            while y < rect.bottom():
                # FIXED: All coordinates converted to int
                ix, iy = int(x), int(y)
                painter.drawLine(ix - cross_size, iy, ix + cross_size, iy)
                painter.drawLine(ix, iy - cross_size, ix, iy + cross_size)
                y += self.grid_size
            x += self.grid_size

    def _draw_paper_cut_pattern(self, painter, rect):
        """FIXED: Draw paper cut pattern with proper coordinates"""
        pen = QPen(self.grid_color, 1)
        pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)
        
        # FIXED: Convert ALL coordinates to int
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        rect_left = int(rect.left())
        rect_right = int(rect.right())
        rect_top = int(rect.top())
        rect_bottom = int(rect.bottom())
        
        # Vertical dotted lines
        x = left
        while x < rect_right:
            painter.drawLine(int(x), rect_top, int(x), rect_bottom)  # FIXED
            x += self.grid_size
        
        # Horizontal dotted lines
        y = top
        while y < rect_bottom:
            painter.drawLine(rect_left, int(y), rect_right, int(y))  # FIXED
            y += self.grid_size

    def _draw_breadboard_pattern(self, painter, rect):
        """FIXED: Draw breadboard pattern with proper coordinates"""
        hole_spacing = 10
        hole_radius = 1.5
        
        # FIXED: Convert ALL coordinates to int
        left = int(rect.left()) - (int(rect.left()) % hole_spacing)
        top = int(rect.top()) - (int(rect.top()) % hole_spacing)
        
        # Colors
        power_color = QColor(220, 100, 100)
        ground_color = QColor(100, 100, 220)
        tie_point_color = QColor(80, 80, 80)
        
        # Draw power rails (simplified)
        painter.setPen(QPen(power_color, 2))
        painter.setBrush(QBrush(power_color))
        
        x = left
        while x < rect.right():
            y = top
            # Draw power rail holes at top
            if y + 20 < rect.bottom():
                ix, iy = int(x), int(y + 20)
                painter.drawEllipse(ix - int(hole_radius), iy - int(hole_radius),
                                  int(hole_radius * 2), int(hole_radius * 2))
            
            # Draw main tie points
            painter.setPen(QPen(tie_point_color, 1))
            painter.setBrush(QBrush(tie_point_color))
            
            y = top + 40
            while y < rect.bottom() - 40:
                ix, iy = int(x), int(y)
                painter.drawEllipse(ix - int(hole_radius), iy - int(hole_radius),
                                  int(hole_radius * 2), int(hole_radius * 2))
                y += hole_spacing
            
            x += hole_spacing

    # === GRID AND DISPLAY CONTROLS ===
    def set_grid_visible(self, visible: bool):
        """Set grid visibility"""
        self.grid_visible = visible
        self.viewport().update()
        print(f"🔧 Grid visible: {visible}")
    
    def set_grid_style(self, style: str):
        """Set grid style"""
        self.grid_style = style
        self.viewport().update()
        print(f"🔧 Grid style: {style}")
    
    def set_grid_color(self, color: QColor):
        """Set grid color"""
        self.grid_color = color
        self.viewport().update()
        print(f"🎨 Grid color: {color.name()}")
    
    def set_background_color(self, color: QColor):
        """Set background color"""
        self.background_color = color
        self.setBackgroundBrush(QBrush(color))
        self.viewport().update()
        print(f"🎨 Background color: {color.name()}")
    
    def set_grid_size(self, size: int):
        """Set grid size"""
        self.grid_size = max(5, min(100, size))  # Clamp between 5 and 100
        self.viewport().update()
        print(f"🔧 Grid size: {self.grid_size}")
    
    def set_snap_to_grid(self, enabled: bool):
        """Set snap to grid"""
        self.snap_to_grid = enabled
        print(f"🔧 Snap to grid: {enabled}")
    
    def set_rulers_visible(self, visible: bool):
        """Set ruler visibility"""
        self.show_ruler = visible
        self.viewport().update()
        print(f"📏 Rulers visible: {visible}")

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
        print("🧹 All components cleared")
    
    def _snap_to_grid(self, point: QPointF) -> QPointF:
        """Snap point to grid"""
        if not self.snap_to_grid:
            return point
        
        x = round(point.x() / self.grid_size) * self.grid_size
        y = round(point.y() / self.grid_size) * self.grid_size
        return QPointF(x, y)

    # === ZOOM CONTROLS ===
    def zoom_in(self):
        """Zoom in"""
        self.scale(1.25, 1.25)
        self.zoom_factor *= 1.25
        self.zoom_changed.emit(self.zoom_factor)
        print(f"🔍 Zoom in: {self.zoom_factor:.2f}")
    
    def zoom_out(self):
        """Zoom out"""
        self.scale(0.8, 0.8)
        self.zoom_factor *= 0.8
        self.zoom_changed.emit(self.zoom_factor)
        print(f"🔍 Zoom out: {self.zoom_factor:.2f}")
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.resetTransform()
        self.zoom_factor = 1.0
        self.zoom_changed.emit(self.zoom_factor)
        print("🔍 Zoom reset")
    
    def fit_in_view(self):
        """Fit all items in view"""
        if self.scene.items():
            self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            # Calculate new zoom factor (approximate)
            transform = self.transform()
            self.zoom_factor = transform.m11()  # Horizontal scale factor
            self.zoom_changed.emit(self.zoom_factor)
            print("🔍 Fit in view")

    # === EVENT HANDLERS ===
    def wheelEvent(self, event):
        """Handle mouse wheel for zooming"""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Zoom with Ctrl+Wheel
            zoom_in_factor = 1.25
            zoom_out_factor = 1 / zoom_in_factor
            
            if event.angleDelta().y() > 0:
                zoom_factor = zoom_in_factor
            else:
                zoom_factor = zoom_out_factor
            
            self.scale(zoom_factor, zoom_factor)
            self.zoom_factor *= zoom_factor
            self.zoom_changed.emit(self.zoom_factor)
        else:
            # Normal scrolling
            super().wheelEvent(event)
    
    def dragEnterEvent(self, event):
        """Handle drag enter for component drops"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            print("✅ Drag enter accepted")
    
    def dropEvent(self, event):
        """Handle component drops"""
        if event.mimeData().hasText():
            # Get drop data
            component_data = event.mimeData().text()
            drop_pos = self.mapToScene(event.position().toPoint())
            
            # Parse component data (simplified)
            try:
                # Expected format: "component_type:component_name:package_type"
                parts = component_data.split(':')
                if len(parts) >= 2:
                    component_type = parts[0]
                    component_name = parts[1]
                    package_type = parts[2] if len(parts) > 2 else "DIP"
                    
                    # Generate unique ID
                    component_id = f"{component_type}_{len(self.components)}"
                    
                    # Add component
                    self.add_component(component_id, component_name, component_type, drop_pos, package_type)
                    
                    event.acceptProposedAction()
                    print(f"📦 Component dropped: {component_name}")
                    
            except Exception as e:
                print(f"❌ Error handling drop: {e}")
    
    def mousePressEvent(self, event):
        """Handle mouse press for component selection"""
        super().mousePressEvent(event)
        
        # Check for component selection
        item = self.itemAt(event.position().toPoint())
        if isinstance(item, VisibleBaseComponent):
            self.component_selected.emit(item)
            print(f"🖱️ Component selected: {item.name}")

# === BACKWARD COMPATIBILITY ALIASES ===
PCBCanvas = EnhancedPCBCanvas
FixedPCBCanvas = EnhancedPCBCanvas

# Export
__all__ = [
    'EnhancedPCBCanvas', 'PCBCanvas', 'FixedPCBCanvas', 
    'VisibleBaseComponent', 'BaseComponent', 'HardwareComponent'
]