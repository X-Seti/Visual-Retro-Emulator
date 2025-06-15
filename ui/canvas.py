"""
X-Seti June 12 2025 - Enhanced PCB Canvas with ALL functionality
Visual Retro System Emulator Builder - Complete Canvas Implementation
"""

#this belongs in ui/canvas.py

import os
import sys
from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem, 
                           QGraphicsPixmapItem, QGraphicsTextItem, QWidget, 
                           QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                           QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
                           QMessageBox, QApplication)
from PyQt6.QtCore import (Qt, QPointF, QRectF, QTimer, pyqtSignal, QObject,
                        QPropertyAnimation, QEasingCurve, QParallelAnimationGroup)
from PyQt6.QtGui import (QPainter, QPen, QBrush, QColor, QPixmap, QFont,
                       QPainterPath, QMouseEvent, QWheelEvent, QKeyEvent,
                       QDragEnterEvent, QDropEvent, QTransform)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def find_component_image_unified(component_name, component_type="", package_type=""):
    """
    UNIFIED component image finder with comprehensive search paths and fallbacks
    
    Search order:
    1. Exact name match in multiple directories
    2. Package-type specific images  
    3. Component type fallbacks
    4. Generic fallbacks
    """
    
    # Define comprehensive search paths
    search_paths = [
        "images/components",
        "images/chips", 
        "images/retro_chips",
        "images",
        "assets/components",
        "assets/chips",
        "assets/images",
        "components/images",
        "chips/images",
        "../images",
        "../images/components",
        "../images/chips"
    ]
    
    # Generate possible filenames
    name_clean = component_name.replace(' ', '_').replace('-', '_').lower()
    type_clean = component_type.replace(' ', '_').replace('-', '_').lower()
    package_clean = package_type.replace('-', '_').lower()
    
    possible_filenames = [
        # Exact matches
        f"{component_name}.png",
        f"{component_name}.jpg", 
        f"{name_clean}.png",
        f"{name_clean}.jpg",
        
        # With package type
        f"{name_clean}_{package_clean}.png",
        f"{component_name}_{package_type}.png",
        
        # Type-based
        f"{type_clean}.png",
        f"{component_type}.png",
        
        # Generic fallbacks
        "generic_ic.png",
        "generic_chip.png", 
        "default_component.png",
        "chip_generic.png"
    ]
    
    # Search in all paths
    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue
            
        for filename in possible_filenames:
            full_path = os.path.join(search_path, filename)
            if os.path.exists(full_path):
                return full_path
    
    return None

# ============================================================================
# BASE COMPONENT CLASSES
# ============================================================================

class VisibleBaseComponent(QGraphicsPixmapItem):
    """Base component with enhanced visual features"""
    
    def __init__(self, component_name="Unknown", component_type="Generic", package_type="DIP"):
        super().__init__()
        
        # Component data
        self.component_name = component_name
        self.component_type = component_type
        self.package_type = package_type
        self.pins = []
        self.selected = False
        
        # Visual properties
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Load image
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

# Try to import enhanced components
try:
    from hardware.components import EnhancedHardwareComponent as HWEnhancedComponent
    EnhancedHardwareComponent = HWEnhancedComponent
    print("✓ Hardware components imported successfully")
except ImportError:
    EnhancedHardwareComponent = VisibleBaseComponent
    print("⚠️ Using fallback for enhanced components")

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

# === ENHANCED PCB CANVAS ===
class EnhancedPCBCanvas(QGraphicsView):
    """
    COMPLETE Enhanced PCB Canvas with ALL original functionality
    
    Features:
    - ALL original methods preserved
    - Unified image loading system
    - Complete project save/load
    - Robust error handling
    - Background transparency processing
    - Grid controls, zoom, pan, selection
    - Connection management
    - Mouse/keyboard interactions
    """
    
    # Signals (ALL ORIGINAL)
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
        
        # Component tracking (ALL ORIGINAL)
        self.selected_components = []
        self.components = {}  # id -> component mapping
        self.connections = []
        
        # Canvas settings (ALL ORIGINAL)
        self.grid_size = 20
        self.grid_visible = True
        self.snap_to_grid = True
        self.zoom_factor = 1.0
        self.grid_color = QColor(100, 140, 100)  # Brighter green grid color
        self._debug_grid = True  # Enable debug output once
        self.grid_style = "lines"  # dots, lines, crosses, breadboard
        
        # Interaction state (ALL ORIGINAL)
        self.drag_mode = False
        self.drag_start_pos = None
        self.current_tool = "select"  # select, place, connect, delete
        self.component_to_place = None
        
        # Connection state (ALL ORIGINAL)
        self.connection_start_component = None
        self.connection_start_port = None
        self.temp_connection_line = None
        
        # Setup canvas
        self._setup_canvas()
        self._setup_interactions()
        
        print("✓ COMPLETE Enhanced PCB Canvas initialized with ALL features")
    
    def _setup_canvas(self):
        """Setup canvas properties (ORIGINAL)"""
        # Set scene size
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        
        # Configure view
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)  # High-quality image scaling
        self.setRenderHint(QPainter.RenderHint.LosslessImageRendering)  # Preserve image quality
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Set background
        self.setBackgroundBrush(QBrush(QColor(20, 20, 30)))  # Dark background
        
        # Grid drawing will be handled in drawBackground
    
    def _setup_interactions(self):
        """Setup mouse and keyboard interactions (ORIGINAL)"""
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
    
    def _make_background_transparent(self, pixmap: QPixmap) -> QPixmap:
        """Convert white/light backgrounds to transparent (ORIGINAL COMPLETE)"""
        try:
            # Convert to QImage for pixel manipulation
            image = pixmap.toImage()
            if image.isNull():
                return pixmap
            
            # Convert to ARGB32 format for transparency
            if image.format() != image.Format.Format_ARGB32:
                image = image.convertToFormat(image.Format.Format_ARGB32)
            
            # Define colors to make transparent (white and light gray backgrounds)
            transparent_colors = [
                QColor(255, 255, 255, 255),  # Pure white
                QColor(254, 254, 254, 255),  # Near white
                QColor(253, 253, 253, 255),  # Light gray
                QColor(252, 252, 252, 255),  # Very light gray
                QColor(240, 240, 240, 255),  # Light background
                QColor(248, 248, 248, 255),  # Another light variant
            ]
            
            # Create transparency threshold
            transparency_threshold = 10  # Tolerance for color matching
            
            # Process each pixel
            for y in range(image.height()):
                for x in range(image.width()):
                    pixel_color = QColor(image.pixel(x, y))
                    
                    # Check if pixel matches any transparent color
                    should_be_transparent = False
                    for transparent_color in transparent_colors:
                        if (abs(pixel_color.red() - transparent_color.red()) <= transparency_threshold and
                            abs(pixel_color.green() - transparent_color.green()) <= transparency_threshold and
                            abs(pixel_color.blue() - transparent_color.blue()) <= transparency_threshold):
                            should_be_transparent = True
                            break
                    
                    if should_be_transparent:
                        image.setPixelColor(x, y, QColor(0, 0, 0, 0))  # Fully transparent
            
            # Convert back to pixmap
            return QPixmap.fromImage(image)
            
        except Exception as e:
            print(f"⚠️ Background transparency failed: {e}")
            return pixmap
    
    # === GRID DRAWING (ORIGINAL COMPLETE) ===
    def drawBackground(self, painter: QPainter, rect: QRectF):
        """Draw enhanced grid background with multiple styles (ORIGINAL COMPLETE)"""
        super().drawBackground(painter, rect)
        
        if not self.grid_visible:
            return
        
        painter.save()
        
        # Grid settings
        pen = QPen(self.grid_color, 0.5)
        painter.setPen(pen)
        
        # Calculate grid bounds
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        if self.grid_style == "dots":
            # Dot grid
            painter.setPen(QPen(self.grid_color, 1))
            y = top
            while y < rect.bottom():
                x = left
                while x < rect.right():
                    painter.drawPoint(x, y)
                    x += self.grid_size
                y += self.grid_size
        
        elif self.grid_style == "lines":
            # Line grid (default)
            # Vertical lines
            x = left
            while x < rect.right():
                painter.drawLine(x, rect.top(), x, rect.bottom())
                x += self.grid_size
            
            # Horizontal lines
            y = top
            while y < rect.bottom():
                painter.drawLine(rect.left(), y, rect.right(), y)
                y += self.grid_size
        
        elif self.grid_style == "crosses":
            # Cross grid
            cross_size = 3
            y = top
            while y < rect.bottom():
                x = left
                while x < rect.right():
                    painter.drawLine(x - cross_size, y, x + cross_size, y)
                    painter.drawLine(x, y - cross_size, x, y + cross_size)
                    x += self.grid_size
                y += self.grid_size
        
        elif self.grid_style == "breadboard":
            # Breadboard-style grid with connection points
            painter.setPen(QPen(self.grid_color, 2))
            y = top
            while y < rect.bottom():
                x = left
                while x < rect.right():
                    painter.drawEllipse(x - 2, y - 2, 4, 4)
                    x += self.grid_size
                y += self.grid_size
        
        painter.restore()
    
    # === DRAG AND DROP (ORIGINAL COMPLETE) ===
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter for component placement (ORIGINAL)"""
        if event.mimeData().hasText():
            component_data = event.mimeData().text()
            if component_data.startswith("component:"):
                event.accept()
                print(f"🎯 Drag enter accepted: {component_data}")
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """Handle drag move (ORIGINAL)"""
        if event.mimeData().hasText():
            event.accept()
    
    def dropEvent(self, event: QDropEvent):
        """Handle component drop with unified image loading (ENHANCED)"""
        if event.mimeData().hasText():
            component_data = event.mimeData().text()
            if component_data.startswith("component:"):
                try:
                    # Parse component data
                    _, comp_type, comp_name = component_data.split(":", 2)
                    
                    # Get drop position in scene coordinates
                    scene_pos = self.mapToScene(event.position().toPoint())
                    
                    # Snap to grid if enabled
                    if self.snap_to_grid:
                        scene_pos.setX(round(scene_pos.x() / self.grid_size) * self.grid_size)
                        scene_pos.setY(round(scene_pos.y() / self.grid_size) * self.grid_size)
                    
                    # Create component
                    component = self._create_component(comp_name, comp_type, scene_pos)
                    
                    if component:
                        # Add to tracking
                        component_id = f"{comp_name}_{len(self.components)}"
                        self.components[component_id] = component
                        
                        # Emit signals
                        self.component_added.emit(component)
                        
                        print(f"✅ Component placed: {comp_name} at {scene_pos}")
                        event.accept()
                    else:
                        print(f"❌ Failed to create component: {comp_name}")
                        event.ignore()
                except Exception as e:
                    print(f"❌ Drop error: {e}")
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def _create_component(self, name: str, comp_type: str, position: QPointF):
        """Create component with unified image loading (ENHANCED)"""
        try:
            # Create component instance
            component = VisibleBaseComponent(name, comp_type)
            component.setPos(position)
            
            # Add to scene
            self.scene.addItem(component)
            
            return component
            
        except Exception as e:
            print(f"❌ Component creation failed: {e}")
            return None
    
    # === MOUSE EVENTS (ENHANCED WITH MISSING METHODS) ===
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for selection (ORIGINAL)"""
        super().mousePressEvent(event)
        
        item = self.itemAt(event.position().toPoint())
        if item and hasattr(item, 'component_type'):
            # Component selected
            self.selected_components.clear()
            self.selected_components.append(item)
            self.component_selected.emit(item)
            self.selection_changed.emit(list(self.selected_components))
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for dragging and interactions (ADDED)"""
        super().mouseMoveEvent(event)
        
        # Update any temporary visual elements (like connection lines)
        if self.temp_connection_line:
            scene_pos = self.mapToScene(event.position().toPoint())
            # Update temporary connection line end point
            line = self.temp_connection_line.line()
            line.setP2(scene_pos)
            self.temp_connection_line.setLine(line)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release for completing interactions (ADDED)"""
        super().mouseReleaseEvent(event)
        
        # Handle connection completion
        if self.temp_connection_line:
            item = self.itemAt(event.position().toPoint())
            if item and hasattr(item, 'component_type') and item != self.connection_start_component:
                # Complete connection
                self.connection_created.emit(self.connection_start_component, item, "out", "in")
                print(f"🔗 Connection created between {self.connection_start_component.component_name} and {item.component_name}")
            
            # Clean up temporary connection line
            self.scene.removeItem(self.temp_connection_line)
            self.temp_connection_line = None
            self.connection_start_component = None
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel for zooming (ORIGINAL)"""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Zoom with Ctrl + wheel
            zoom_factor = 1.25 if event.angleDelta().y() > 0 else 0.8
            self.scale(zoom_factor, zoom_factor)
            self.zoom_factor *= zoom_factor
            print(f"🔍 Zoom: {self.zoom_factor:.2f}")
        else:
            super().wheelEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events (ORIGINAL)"""
        if event.key() == Qt.Key.Key_Delete:
            # Delete selected components
            for component in self.selected_components:
                self.scene.removeItem(component)
                # Remove from tracking
                for comp_id, comp in list(self.components.items()):
                    if comp == component:
                        del self.components[comp_id]
                        break
                self.component_removed.emit(component)
            self.selected_components.clear()
            self.selection_changed.emit([])
            print("🗑️ Selected components deleted")
        
        elif event.key() == Qt.Key.Key_Escape:
            # Clear selection
            self.selected_components.clear()
            self.selection_changed.emit([])
            self.scene.clearSelection()
            print("↩️ Selection cleared")
        
        else:
            super().keyPressEvent(event)
    
    # === COMPONENT MANAGEMENT (ALL ORIGINAL) ===
    def add_component(self, component_type: str, component_name: str, position: QPointF = None):
        """Add component to canvas programmatically (ORIGINAL)"""
        if position is None:
            position = QPointF(0, 0)
        
        component = self._create_component(component_name, component_type, position)
        if component:
            component_id = f"{component_name}_{len(self.components)}"
            self.components[component_id] = component
            self.component_added.emit(component)
            return component_id
        return None
    
    def remove_component(self, component_id: str):
        """Remove component by ID (ORIGINAL)"""
        if component_id in self.components:
            component = self.components[component_id]
            self.scene.removeItem(component)
            del self.components[component_id]
            self.component_removed.emit(component)
            print(f"🗑️ Component removed: {component_id}")
    
    def get_component_at(self, position: QPointF):
        """Get component at position (ORIGINAL)"""
        view_pos = self.mapFromScene(position)
        item = self.itemAt(view_pos.toPoint())
        return item if item and hasattr(item, 'component_type') else None
    
    def clear_all_components(self):
        """Clear all components from canvas (ORIGINAL)"""
        for component in list(self.components.values()):
            self.scene.removeItem(component)
        self.components.clear()
        self.selected_components.clear()
        self.connections.clear()
        self.selection_changed.emit([])
        print("🧹 All components cleared")
    
    def get_all_components(self):
        """Get all components (ORIGINAL)"""
        return list(self.components.values())
    
    def select_component(self, component):
        """Select a specific component (ORIGINAL)"""
        self.selected_components.clear()
        self.selected_components.append(component)
        component.setSelected(True)
        self.component_selected.emit(component)
        self.selection_changed.emit(list(self.selected_components))
    
    # === GRID CONTROL METHODS (for layer controls integration) ===
    def set_grid_visible(self, visible: bool):
        """Set grid visibility"""
        self.grid_visible = visible
        self.viewport().update()
        print(f"🔧 Grid {'visible' if visible else 'hidden'}")
    
    def set_grid_style(self, style):
        """Set grid style (from GridStyle enum or string)"""
        if hasattr(style, 'value'):
            self.grid_style = style.value
        else:
            self.grid_style = str(style).lower()
        self.viewport().update()
        print(f"🔧 Grid style set to: {self.grid_style}")
    
    def set_grid_spacing(self, spacing, custom_value=None):
        """Set grid spacing (from GridSpacing enum or custom value)"""
        if custom_value and custom_value > 0:
            # Use custom value (convert mm to pixels, assuming ~2.83 pixels per mm)
            self.grid_size = int(custom_value * 2.83)
        elif hasattr(spacing, 'value'):
            # Use enum value
            spacing_map = {
                "Fine (2.54mm)": int(2.54 * 2.83),  # ~7 pixels
                "Medium (5.08mm)": int(5.08 * 2.83),  # ~14 pixels
                "Coarse (10.16mm)": int(10.16 * 2.83)  # ~29 pixels
            }
            self.grid_size = spacing_map.get(spacing.value, 20)
        else:
            # Fallback
            self.grid_size = 20
        
        self.viewport().update()
        print(f"🔧 Grid size set to: {self.grid_size} pixels")
    
    def set_snap_to_grid(self, enabled: bool):
        """Set snap to grid"""
        self.snap_to_grid = enabled
        print(f"🔧 Snap to grid {'enabled' if enabled else 'disabled'}")
    
    # === VIEW CONTROL METHODS (ENHANCED WITH MISSING METHODS) ===
    def zoom_to_fit(self):
        """Zoom to fit all components"""
        if self.components:
            self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            print("🔍 Zoomed to fit all components")
    
    def fit_in_view(self):
        """Fit all content in view (ADDED)"""
        if self.components:
            self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.zoom_factor = 1.0  # Reset zoom factor tracking
            print("🔍 Fitted all content in view")
        else:
            self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            print("🔍 Fitted scene in view")
    
    def fit_to_window(self):
        """Fit content to window (ADDED)"""
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom_factor = 1.0
        print("🔍 Fitted to window")
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.resetTransform()
        self.zoom_factor = 1.0
        print("🔍 Zoom reset to 100%")
    
    def zoom_in(self):
        """Zoom in"""
        self.scale(1.25, 1.25)
        self.zoom_factor *= 1.25
        print("🔍 Zoomed in")
    
    def zoom_out(self):
        """Zoom out"""
        self.scale(0.8, 0.8)
        self.zoom_factor *= 0.8
        print("🔍 Zoomed out")
    
    # === CONNECTION MANAGEMENT (ALL ORIGINAL) ===
    def start_connection(self, component, port="out"):
        """Start creating a connection (ORIGINAL)"""
        self.connection_start_component = component
        self.connection_start_port = port
        
        # Create temporary connection line
        start_pos = component.scenePos()
        self.temp_connection_line = QGraphicsLineItem(
            start_pos.x(), start_pos.y(),
            start_pos.x(), start_pos.y()
        )
        self.temp_connection_line.setPen(QPen(QColor(255, 255, 0), 2))  # Yellow line
        self.scene.addItem(self.temp_connection_line)
        print(f"🔗 Starting connection from {component.component_name}")
    
    def clear_connections(self):
        """Clear all connections (ORIGINAL)"""
        self.connections.clear()
        # Remove connection graphics if any
        print("🧹 All connections cleared")
    
    def get_connections(self):
        """Get all connections (ORIGINAL)"""
        return list(self.connections)
    
    # === PROJECT MANAGEMENT (ALL ORIGINAL) ===
    def save_to_project_data(self):
        """Save canvas state to project data (ORIGINAL)"""
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
                'snap_to_grid': self.snap_to_grid
            }
        }
    
    def load_from_project_data(self, data):
        """Load canvas state from project data (ORIGINAL)"""
        try:
            # Clear existing components
            self.clear_all_components()
            
            # Load components
            if 'components' in data:
                for comp_data in data['components']:
                    position = QPointF(comp_data['position']['x'], comp_data['position']['y'])
                    component = self._create_component(
                        comp_data['name'], 
                        comp_data['type'], 
                        position
                    )
                    if component:
                        self.components[comp_data['id']] = component
            
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
                self.viewport().update()
            
            print(f"✅ Project loaded: {len(self.components)} components")
            
        except Exception as e:
            print(f"❌ Project load error: {e}")

# Backward compatibility alias
PCBCanvas = EnhancedPCBCanvas

# Export
__all__ = ['EnhancedPCBCanvas', 'PCBCanvas', 'VisibleBaseComponent', 'find_component_image_unified']