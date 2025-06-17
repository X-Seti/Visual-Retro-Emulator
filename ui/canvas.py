#this belongs in ui/canvas.py

"""
X-Seti - June16 2025 - Enhanced PCB Canvas - Visual Retro Emulator
COMPLETE canvas implementation with ALL original functionality + new features
"""

# Essential imports
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import os
import sys
import json
from pathlib import Path

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

# ============================================================================
# COMPONENT IMAGE LOADING SYSTEM
# ============================================================================

def find_component_image_unified(component_name, component_type="Generic", package_type="DIP"):
    """
    Unified component image finder with comprehensive fallback system
    
    Search Strategy:
    1. Exact component name matches
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
# ENHANCED COMPONENT CLASSES
# ============================================================================

class VisibleBaseComponent(QGraphicsPixmapItem):
    """Base component with enhanced visual features"""
    
    def __init__(self, component_name="Unknown", component_type="Generic", package_type="DIP"):
        super().__init__()
        
        # Component data
        self.component_name = component_name
        self.component_type = component_type
        self.package_type = package_type
        self.component_id = f"{component_name}_{id(self)}"
        
        # Visual properties
        self.selected_color = QColor(255, 165, 0)  # Orange
        self.pin_count = 8  # Default
        self.pins = []
        
        # Load component image
        self._load_component_image()
        
        # Make selectable and movable
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        
        # Set default size if no image loaded
        if self.pixmap().isNull():
            self._create_fallback_visual()
    
    def _load_component_image(self):
        """Load component image using unified system"""
        image_path = find_component_image_unified(
            self.component_name, 
            self.component_type, 
            self.package_type
        )
        
        if image_path and os.path.exists(image_path):
            try:
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    # Scale to reasonable size
                    if pixmap.width() > 200 or pixmap.height() > 200:
                        pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.setPixmap(pixmap)
                    print(f"✓ Loaded image for {self.component_name}: {image_path}")
                    return
            except Exception as e:
                print(f"⚠️ Error loading image {image_path}: {e}")
        
        print(f"⚠️ No image found for {self.component_name}, using fallback")
    
    def _create_fallback_visual(self):
        """Create fallback visual representation"""
        # Create a simple colored rectangle as fallback
        fallback_size = QSize(60, 30)
        pixmap = QPixmap(fallback_size)
        pixmap.fill(QColor(70, 70, 70))  # Dark gray
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.drawRect(pixmap.rect())
        
        # Draw component name
        painter.setPen(QColor(255, 255, 255))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, self.component_name[:8])
        painter.end()
        
        self.setPixmap(pixmap)
    
    def itemChange(self, change, value):
        """Handle item changes"""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Emit position change signal if canvas exists
            canvas = self.scene().views()[0] if self.scene() and self.scene().views() else None
            if canvas and hasattr(canvas, 'component_moved'):
                canvas.component_moved.emit(self, value, self.pos())
        return super().itemChange(change, value)
    
    def paint(self, painter, option, widget):
        """Custom painting with selection highlight"""
        super().paint(painter, option, widget)
        
        if self.isSelected():
            # Draw selection border
            painter.setPen(QPen(self.selected_color, 3))
            painter.drawRect(self.boundingRect())

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

# ============================================================================
# COMPLETE ENHANCED PCB CANVAS
# ============================================================================

class EnhancedPCBCanvas(QGraphicsView):
    """
    COMPLETE Enhanced PCB Canvas with ALL original functionality + new features
    
    PRESERVED ORIGINAL FEATURES:
    - ALL component management methods
    - ALL grid drawing methods  
    - ALL zoom and view methods
    - ALL connection management
    - ALL mouse/keyboard events
    - ALL project save/load
    - Background transparency processing
    - Layer management integration
    - Drag and drop functionality
    - Selection management
    - Tool modes
    - Connection creation
    
    NEW FEATURES:
    - Paper Cut pattern fixed
    - Background color options (Dark, Light, Gray, White, Black)
    - Size-adjusted breadboard/pinboard patterns
    - Ruler on canvas edge
    - Enhanced backup components
    - Zoom status signal
    """
    
    # Signals (ALL ORIGINAL + NEW)
    component_added = pyqtSignal(object)
    component_removed = pyqtSignal(object)
    component_selected = pyqtSignal(object)
    component_moved = pyqtSignal(object, QPointF, QPointF)
    connection_created = pyqtSignal(object, object, str, str)
    selection_changed = pyqtSignal(list)
    zoom_changed = pyqtSignal(float)  # NEW: For status bar
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Initialize layer manager
        self.layer_manager = LayerManager()
        
        # Component tracking (ALL ORIGINAL)
        self.selected_components = []
        self.components = {}  # id -> component mapping
        self.connections = []
        
        # Canvas settings (ORIGINAL + NEW)
        self.grid_size = 20
        self.grid_visible = True
        self.snap_to_grid = True
        self.zoom_factor = 1.0
        self.grid_color = QColor(100, 140, 100)  # Brighter green grid color
        self._debug_grid = True  # Enable debug output once
        self.grid_style = "lines"  # dots, lines, crosses, paper cut, breadboard
        self.background_color = QColor(25, 25, 35)  # NEW: Default dark background
        
        # NEW: Enhanced canvas options
        self.breadboard_width = 30  # holes
        self.breadboard_height = 20  # holes
        self.pinboard_width = 40    # holes
        self.pinboard_height = 30   # holes
        self.ruler_visible = True
        self.ruler_units = "mm"     # mm, inches, pixels
        self.show_ruler = False
        
        # NEW: Color presets
        self.background_presets = {
            "Dark": QColor(25, 25, 35),
            "Light": QColor(245, 245, 245),
            "Gray": QColor(128, 128, 128),
            "White": QColor(255, 255, 255),
            "Black": QColor(0, 0, 0)
        }
        
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
        
        print("✅ COMPLETE Enhanced PCB Canvas initialized with ALL features")
    
    def _setup_canvas(self):
        """Setup canvas properties (ORIGINAL + NEW)"""
        # Set scene size (ORIGINAL)
        self.scene.setSceneRect(-3000, -3000, 6000, 6000)  # NEW: Larger scene
        
        # Configure view (ORIGINAL)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)  # High-quality image scaling
        self.setRenderHint(QPainter.RenderHint.LosslessImageRendering)  # Preserve image quality
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Set background (ORIGINAL + NEW)
        self.setBackgroundBrush(QBrush(self.background_color))
    
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
                    
                    # Make pixel transparent if it matches
                    if should_be_transparent:
                        image.setPixelColor(x, y, QColor(0, 0, 0, 0))  # Transparent
            
            # Convert back to pixmap
            return QPixmap.fromImage(image)
            
        except Exception as e:
            print(f"⚠️ Background transparency processing failed: {e}")
            return pixmap
    
    # === DRAWING METHODS ===
    def drawBackground(self, painter, rect):
        """Draw background with proper coordinate types (ORIGINAL + NEW)"""
        # Draw background color first
        painter.fillRect(rect, self.background_color)
        
        # Draw ruler if enabled
        try:
            if self.ruler_visible or self.show_ruler:
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
        elif style_lower == "pinboard":
            self._draw_pinboard_pattern(painter, rect)
    
    def _draw_ruler(self, painter, rect):
        """FIXED: Draw ruler marks with proper coordinate types"""
        if not hasattr(self, 'show_ruler') or not getattr(self, 'show_ruler', False):
            if not self.ruler_visible:
                return

        # FIXED: Convert all float coordinates to int for PyQt6 compatibility
        painter.setPen(QPen(QColor(100, 100, 100), 1))

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
        """Draw dots at grid intersections (ORIGINAL)"""
        painter.setPen(QPen(self.grid_color, 2))
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        x = left
        while x < rect.right():
            y = top
            while y < rect.bottom():
                painter.drawPoint(int(x), int(y))
                y += self.grid_size
            x += self.grid_size
    
    def _draw_lines_pattern(self, painter, rect):
        """FIXED: Draw solid grid lines with proper type conversion (ORIGINAL + FIXED)"""
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
            painter.drawLine(int(x), rect_top, int(x), rect_bottom)
            x += self.grid_size
        
        # Horizontal lines
        y = top
        while y < rect_bottom:
            painter.drawLine(rect_left, int(y), rect_right, int(y))
            y += self.grid_size
    
    def _draw_crosses_pattern(self, painter, rect):
        """Draw crosses at grid intersections (ORIGINAL)"""
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
        """FIXED: Draw paper cut pattern with proper coordinates (ORIGINAL + FIXED)"""
        pen = QPen(self.grid_color, 1)
        pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)
        
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        # FIXED: Convert all coordinates to int
        rect_left = int(rect.left())
        rect_right = int(rect.right())
        rect_top = int(rect.top())
        rect_bottom = int(rect.bottom())
        
        # Vertical lines
        x = left
        while x < rect_right:
            painter.drawLine(int(x), rect_top, int(x), rect_bottom)
            x += self.grid_size
        
        # Horizontal lines
        y = top
        while y < rect_bottom:
            painter.drawLine(rect_left, int(y), rect_right, int(y))
            y += self.grid_size
    
    def _draw_breadboard_pattern(self, painter, rect):
        """Draw breadboard pattern with size adjustment (ORIGINAL + NEW)"""
        hole_spacing = max(8, self.grid_size // 2)
        
        painter.setPen(QPen(self.grid_color.darker(120), 1))
        painter.setBrush(QBrush(self.background_color.lighter(110)))
        
        left = int(rect.left()) - (int(rect.left()) % hole_spacing)
        top = int(rect.top()) - (int(rect.top()) % hole_spacing)
        
        # Draw breadboard holes
        hole_radius = 1.5
        
        x = left
        col = 0
        while x < rect.right() and col < self.breadboard_width:
            y = top
            row = 0
            while y < rect.bottom() and row < self.breadboard_height:
                painter.drawEllipse(QPointF(x, y), hole_radius, hole_radius)
                y += hole_spacing
                row += 1
            x += hole_spacing
            col += 1
        
        # Draw power rails
        painter.setPen(QPen(QColor(200, 100, 100), 2))  # Red for positive
        painter.drawLine(left, top + 5, left + (self.breadboard_width * hole_spacing), top + 5)
        painter.setPen(QPen(QColor(100, 100, 200), 2))  # Blue for negative  
        painter.drawLine(left, top - 5, left + (self.breadboard_width * hole_spacing), top - 5)
    
    def _draw_pinboard_pattern(self, painter, rect):
        """NEW: Draw pinboard/perfboard pattern with size adjustment"""
        hole_spacing = max(6, self.grid_size // 3)
        
        painter.setPen(QPen(self.grid_color.darker(120), 1))
        painter.setBrush(QBrush(self.background_color.lighter(120)))
        
        left = int(rect.left()) - (int(rect.left()) % hole_spacing)
        top = int(rect.top()) - (int(rect.top()) % hole_spacing)
        
        # Draw background grid
        pen = QPen(self.grid_color.lighter(160), 0.5)
        painter.setPen(pen)
        
        # Draw perfboard holes
        painter.setBrush(QBrush(self.grid_color.darker(150)))
        hole_radius = 1.5
        
        x = left
        col = 0
        while x < rect.right() and col < self.pinboard_width:
            y = top
            row = 0
            while y < rect.bottom() and row < self.pinboard_height:
                painter.drawEllipse(QPointF(x, y), hole_radius, hole_radius)
                y += hole_spacing
                row += 1
            x += hole_spacing
            col += 1
    
    # === COMPONENT MANAGEMENT (ALL ORIGINAL + NEW) ===
    def _create_component(self, component_name: str, component_type: str, position: QPointF = None):
        """Create component instance (ORIGINAL)"""
        if position is None:
            position = QPointF(0, 0)
        
        try:
            # Create component with enhanced visuals
            component = VisibleBaseComponent(component_name, component_type)
            component.setPos(position)
            self.scene.addItem(component)
            return component
        except Exception as e:
            print(f"❌ Error creating component: {e}")
            return None
    
    def add_component(self, component_id: str, component_name: str, component_type: str, 
                     position: QPointF, package_type: str = "DIP"):
        """Add component to canvas (ORIGINAL + NEW)"""
        if component_id in self.components:
            print(f"⚠️ Component {component_id} already exists")
            return None
        
        try:
            # Create enhanced visual component
            component = VisibleBaseComponent(component_name, component_type, package_type)
            
            # Set position (snap to grid if enabled)
            if self.snap_to_grid:
                position = self._snap_to_grid(position)
            
            component.setPos(position)
            
            # Add to scene and tracking
            self.scene.addItem(component)
            self.components[component_id] = component
            
            # Emit signal
            self.component_added.emit(component)
            print(f"✓ Component added: {component_id} at {position}")
            
            return component
            
        except Exception as e:
            print(f"❌ Error adding component: {e}")
            return None
    
    def remove_component(self, component_id: str):
        """Remove component from canvas (ORIGINAL)"""
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
    
    def _snap_to_grid(self, point: QPointF) -> QPointF:
        """Snap point to grid (ORIGINAL)"""
        if not self.snap_to_grid:
            return point
        
        x = round(point.x() / self.grid_size) * self.grid_size
        y = round(point.y() / self.grid_size) * self.grid_size
        return QPointF(x, y)
    
    # === GRID METHODS (ALL ORIGINAL + NEW) ===
    def set_grid_visible(self, visible):
        """Toggle grid visibility (ORIGINAL)"""
        self.grid_visible = visible
        self.viewport().update()
        print(f"✓ Grid visible: {visible}")
    
    def set_grid_style(self, style):
        """Set grid style (ORIGINAL)"""
        self.grid_style = style
        self.viewport().update()
        print(f"✓ Grid style: {style}")
    
    def set_grid_spacing(self, spacing):
        """Set grid spacing (ORIGINAL)"""
        if isinstance(spacing, (int, float)):
            self.grid_size = int(spacing)
        else:
            # Handle enum or string values
            spacing_map = {
                "Small": 10,
                "Medium": 20,
                "Large": 40,
                "Extra Large": 80
            }
            self.grid_size = spacing_map.get(str(spacing), 20)
        
        self.viewport().update()
        print(f"✓ Grid spacing: {self.grid_size}")
    
    def set_snap_to_grid(self, enabled):
        """Enable/disable snap to grid (ORIGINAL)"""
        self.snap_to_grid = enabled
        print(f"✓ Snap to grid: {enabled}")
    
    def debug_grid_settings(self):
        """Debug grid settings (ORIGINAL)"""
        print("🔍 Grid Settings Debug:")
        print(f"  Visible: {self.grid_visible}")
        print(f"  Size: {self.grid_size}")
        print(f"  Style: {self.grid_style}")
        print(f"  Color: {self.grid_color.name()}")
        print(f"  Snap: {self.snap_to_grid}")
    
    # === ZOOM METHODS (ALL ORIGINAL + NEW) ===
    def zoom_in(self):
        """Zoom in (ORIGINAL + NEW)"""
        self.scale(1.25, 1.25)
        self.zoom_factor *= 1.25
        self.zoom_changed.emit(self.zoom_factor)
        print("🔍 Zoomed in")
    
    def zoom_out(self):
        """Zoom out (ORIGINAL + NEW)"""
        self.scale(0.8, 0.8)
        self.zoom_factor *= 0.8
        self.zoom_changed.emit(self.zoom_factor)
        print("🔍 Zoomed out")
    
    def reset_zoom(self):
        """Reset zoom to 100% (ORIGINAL + NEW)"""
        self.resetTransform()
        self.zoom_factor = 1.0
        self.zoom_changed.emit(self.zoom_factor)
        print("🔍 Zoom reset to 100%")
    
    def zoom_to_fit(self):
        """Zoom to fit all components (ORIGINAL)"""
        if self.components:
            self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            # Calculate approximate zoom factor
            view_rect = self.viewport().rect()
            scene_rect = self.scene.itemsBoundingRect()
            if not scene_rect.isEmpty():
                zoom_x = view_rect.width() / scene_rect.width()
                zoom_y = view_rect.height() / scene_rect.height()
                self.zoom_factor = min(zoom_x, zoom_y)
                self.zoom_changed.emit(self.zoom_factor)
            print("🔍 Zoomed to fit all components")
    
    def fit_in_view(self):
        """Fit all content in view (ORIGINAL)"""
        if self.components:
            self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.zoom_factor = 1.0  # Reset zoom factor tracking
            print("🔍 Fitted all content in view")
        else:
            self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            print("🔍 Fitted scene in view")
    
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
    
    def finish_connection(self, target_component, target_port="in"):
        """Finish creating a connection (ORIGINAL)"""
        if self.connection_start_component and target_component:
            # Create connection data
            connection = {
                'source': self.connection_start_component,
                'source_port': self.connection_start_port,
                'target': target_component,
                'target_port': target_port
            }
            
            self.connections.append(connection)
            
            # Emit signal
            self.connection_created.emit(
                self.connection_start_component,
                target_component, 
                self.connection_start_port,
                target_port
            )
            
            print(f"🔗 Connection created: {self.connection_start_component.component_name} -> {target_component.component_name}")
            
            # Clean up temporary connection line
            if self.temp_connection_line:
                self.scene.removeItem(self.temp_connection_line)
                self.temp_connection_line = None
            self.connection_start_component = None
    
    def clear_connections(self):
        """Clear all connections (ORIGINAL)"""
        self.connections.clear()
        # Remove connection graphics if any
        print("🧹 All connections cleared")
    
    def get_connections(self):
        """Get all connections (ORIGINAL)"""
        return list(self.connections)
    
    # === MOUSE EVENTS (ALL ORIGINAL + NEW) ===
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for selection (ORIGINAL)"""
        if event.button() == Qt.MouseButton.LeftButton:
            scene_pos = self.mapToScene(event.position().toPoint())
            
            # Check if clicking on a component
            item = self.scene.itemAt(scene_pos, self.transform())
            if isinstance(item, VisibleBaseComponent):
                # Select component
                self.scene.clearSelection()
                item.setSelected(True)
                self.component_selected.emit(item)
                self.selected_components = [item]
                self.selection_changed.emit([item])
            else:
                # Clear selection
                self.scene.clearSelection()
                self.selected_components.clear()
                self.selection_changed.emit([])
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for dragging and interactions (ORIGINAL)"""
        super().mouseMoveEvent(event)
        
        # Update any temporary visual elements (like connection lines)
        if self.temp_connection_line:
            scene_pos = self.mapToScene(event.position().toPoint())
            # Update temporary connection line end point
            line = self.temp_connection_line.line()
            line.setP2(scene_pos)
            self.temp_connection_line.setLine(line)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release for completing interactions (ORIGINAL)"""
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
    
    def mouseDoubleClickEvent(self, event):
        """Handle double-click events (ORIGINAL)"""
        scene_pos = self.mapToScene(event.position().toPoint())
        item = self.scene.itemAt(scene_pos, self.transform())
        
        if isinstance(item, VisibleBaseComponent):
            print(f"Double-clicked component: {item.component_name}")
            # Emit signal for component properties dialog
            self.component_selected.emit(item)
        
        super().mouseDoubleClickEvent(event)
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel for zooming (ORIGINAL + NEW)"""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Zoom with Ctrl + wheel
            zoom_factor = 1.25 if event.angleDelta().y() > 0 else 0.8
            self.scale(zoom_factor, zoom_factor)
            self.zoom_factor *= zoom_factor
            self.zoom_changed.emit(self.zoom_factor)
            print(f"🔍 Zoom: {self.zoom_factor:.2f}")
        else:
            super().wheelEvent(event)
    
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
        """Handle component drop with unified image loading (ORIGINAL + NEW)"""
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
    
    # === KEYBOARD EVENTS (ALL ORIGINAL) ===
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events (ORIGINAL)"""
        key = event.key()
        modifiers = event.modifiers()
        
        if key == Qt.Key.Key_Delete:
            # Delete selected components
            selected_items = list(self.selected_components)
            for item in selected_items:
                if isinstance(item, VisibleBaseComponent):
                    # Find component ID
                    component_id = None
                    for comp_id, comp in self.components.items():
                        if comp == item:
                            component_id = comp_id
                            break
                    
                    if component_id:
                        self.remove_component(component_id)
            
            self.selected_components.clear()
            self.selection_changed.emit([])
            
        elif key == Qt.Key.Key_G and modifiers & Qt.KeyboardModifier.ControlModifier:
            # Toggle grid with Ctrl+G
            self.set_grid_visible(not self.grid_visible)
            
        elif key == Qt.Key.Key_Plus and modifiers & Qt.KeyboardModifier.ControlModifier:
            # Zoom in with Ctrl++
            self.zoom_in()
            
        elif key == Qt.Key.Key_Minus and modifiers & Qt.KeyboardModifier.ControlModifier:
            # Zoom out with Ctrl+-
            self.zoom_out()
            
        elif key == Qt.Key.Key_0 and modifiers & Qt.KeyboardModifier.ControlModifier:
            # Reset zoom with Ctrl+0
            self.reset_zoom()
        
        elif key == Qt.Key.Key_Escape:
            # Clear selection
            self.selected_components.clear()
            self.selection_changed.emit([])
            self.scene.clearSelection()
            print("↩️ Selection cleared")
        
        super().keyPressEvent(event)
    
    # === PROJECT SAVE/LOAD (ALL ORIGINAL + NEW) ===
    def save_project_data(self):
        """Save canvas state to project data (ORIGINAL + NEW)"""
        return {
            'components': [
                {
                    'id': comp_id,
                    'name': comp.component_name,
                    'type': comp.component_type,
                    'package': comp.package_type,
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
            },
            'canvas_settings': {  # NEW
                'breadboard_width': self.breadboard_width,
                'breadboard_height': self.breadboard_height,
                'pinboard_width': self.pinboard_width,
                'pinboard_height': self.pinboard_height,
                'ruler_visible': self.ruler_visible,
                'ruler_units': self.ruler_units
            }
        }
    
    def save_to_project_data(self):
        """Alternative method name for compatibility (ORIGINAL)"""
        return self.save_project_data()
    
    def load_project_data(self, data):
        """Load canvas state from project data (ORIGINAL + NEW)"""
        try:
            # Clear existing components
            self.clear_all_components()
            
            # Load components
            if 'components' in data:
                for comp_data in data['components']:
                    position = QPointF(comp_data['position']['x'], comp_data['position']['y'])
                    package = comp_data.get('package', 'DIP')
                    self.add_component(
                        comp_data['id'],
                        comp_data['name'], 
                        comp_data['type'], 
                        position,
                        package
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
            
            # Load canvas settings (NEW)
            if 'canvas_settings' in data:
                canvas_settings = data['canvas_settings']
                self.breadboard_width = canvas_settings.get('breadboard_width', 30)
                self.breadboard_height = canvas_settings.get('breadboard_height', 20)
                self.pinboard_width = canvas_settings.get('pinboard_width', 40)
                self.pinboard_height = canvas_settings.get('pinboard_height', 30)
                self.ruler_visible = canvas_settings.get('ruler_visible', True)
                self.ruler_units = canvas_settings.get('ruler_units', 'mm')
                
            self.viewport().update()
            print(f"✅ Project loaded: {len(self.components)} components")
            
        except Exception as e:
            print(f"❌ Project load error: {e}")
    
    def load_from_project_data(self, data):
        """Alternative method name for compatibility (ORIGINAL)"""
        self.load_project_data(data)
    
    # === NEW ENHANCED METHODS ===
    def set_background_color(self, color_name_or_color):
        """Set background color by name or QColor (NEW)"""
        if isinstance(color_name_or_color, str):
            if color_name_or_color in self.background_presets:
                self.background_color = self.background_presets[color_name_or_color]
            else:
                self.background_color = QColor(color_name_or_color)
        elif isinstance(color_name_or_color, QColor):
            self.background_color = color_name_or_color
        
        self.setBackgroundBrush(QBrush(self.background_color))
        self.viewport().update()
        print(f"✓ Background color set to: {self.background_color.name()}")
    
    def set_grid_color(self, color):
        """Set grid color (NEW)"""
        if isinstance(color, str):
            self.grid_color = QColor(color)
        elif isinstance(color, QColor):
            self.grid_color = color
        
        self.viewport().update()
        print(f"✓ Grid color set to: {self.grid_color.name()}")
    
    def apply_theme(self, theme_name):
        """Apply color theme (NEW)"""
        themes = {
            "Dark": {
                "background": QColor(25, 25, 35),
                "grid": QColor(100, 140, 100)
            },
            "Light": {
                "background": QColor(245, 245, 245),
                "grid": QColor(100, 100, 100)
            },
            "High Contrast": {
                "background": QColor(0, 0, 0),
                "grid": QColor(255, 255, 255)
            }
        }
        
        if theme_name in themes:
            theme = themes[theme_name]
            self.set_background_color(theme["background"])
            self.set_grid_color(theme["grid"])
            print(f"✓ Applied theme: {theme_name}")
    
    def get_available_themes(self):
        """Get list of available themes (NEW)"""
        return ["Dark", "Light", "High Contrast"]
    
    def set_breadboard_size(self, width, height):
        """Set breadboard pattern size (NEW)"""
        self.breadboard_width = width
        self.breadboard_height = height
        self.viewport().update()
        print(f"✓ Breadboard size: {width}x{height}")
    
    def set_pinboard_size(self, width, height):
        """Set pinboard pattern size (NEW)"""
        self.pinboard_width = width
        self.pinboard_height = height
        self.viewport().update()
        print(f"✓ Pinboard size: {width}x{height}")
    
    def set_ruler_visible(self, visible):
        """Set ruler visibility (NEW)"""
        self.ruler_visible = visible
        self.show_ruler = visible
        self.viewport().update()
        print(f"✓ Ruler visible: {visible}")

# Backward compatibility aliases (ORIGINAL)
PCBCanvas = EnhancedPCBCanvas
FixedPCBCanvas = EnhancedPCBCanvas

# Enhanced Visual Component alias (NEW)
EnhancedVisualComponent = VisibleBaseComponent

# Export (ORIGINAL + NEW)
__all__ = ['EnhancedPCBCanvas', 'PCBCanvas', 'FixedPCBCanvas', 'VisibleBaseComponent', 'EnhancedVisualComponent', 'find_component_image_unified']