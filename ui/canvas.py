"""
X-Seti - June11 2025 - Enhanced PCB Canvas
Visual Retro Emulator - Canvas Module
"""

#This goes in ui/
import os
import sys
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ============================================================================
# GUARANTEED FALLBACK COMPONENT - DEFINED FIRST, BEFORE ANY RISKY IMPORTS
# ============================================================================

class VisibleBaseComponent(QGraphicsPixmapItem):
    """Guaranteed visible fallback component using QGraphicsPixmapItem"""
    
    def __init__(self, component_type: str = "unknown", name: str = None):
        # Create a simple pixmap first
        pixmap = QPixmap(150, 100)
        pixmap.fill(QColor(100, 150, 200))  # Blue background
        
        super().__init__(pixmap)
        
        # Generate unique ID
        import uuid
        self.id = str(uuid.uuid4())
        
        # Basic properties
        self.component_type = component_type
        self.name = name or f"{component_type}_{self.id[:8]}"
        
        # Visual properties
        self.width = 150
        self.height = 100
        self.pinout_pixmap = None
        
        # Force visibility and proper flags
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setVisible(True)
        self.setOpacity(1.0)
        self.setZValue(1000)  # Bring to front
        
        # Create the visible pixmap
        self._create_visible_pixmap()
        
        print(f"🔧 Created VisibleBaseComponent: {self.name}")
        print(f"🔧 Initial rect: {self.boundingRect()}")
        print(f"🔧 Initial visibility: {self.isVisible()}")
    
    def _create_visible_pixmap(self):
        """Create a highly visible pixmap"""
        pixmap = QPixmap(self.width, self.height)
        pixmap.fill(QColor(100, 150, 200))  # Blue background
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw yellow border
        painter.setPen(QPen(QColor(255, 255, 0), 4))
        painter.drawRect(2, 2, self.width-4, self.height-4)
        
        # Draw component name
        painter.setPen(QPen(QColor(255, 255, 255)))
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(QRect(0, 0, self.width, self.height), 
                       Qt.AlignmentFlag.AlignCenter, self.name)
        
        # Draw "CHIP" at top
        painter.setPen(QPen(QColor(255, 0, 0)))
        small_font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(small_font)
        painter.drawText(QRect(5, 5, self.width-10, 20), 
                       Qt.AlignmentFlag.AlignCenter, "CHIP")
        
        painter.end()
        
        # Set this as our pixmap
        self.setPixmap(pixmap)
        print(f"🎨 Created visible pixmap for {self.name}: {pixmap.size()}")
    
    def update_with_image(self, image_pixmap):
        """Update with actual chip image"""
        if image_pixmap and not image_pixmap.isNull():
            print(f"🖼️ Updating {self.name} with chip image: {image_pixmap.size()}")
            # Scale image to reasonable size
            scaled = image_pixmap.scaled(200, 150, 
                                       Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(scaled)
            self.pinout_pixmap = scaled
        else:
            print(f"⚠️ Failed to update {self.name} with image, keeping default")
    
    def shape(self):
        """Return the shape for selection"""
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

# ============================================================================
# NOW TRY TO IMPORT OTHER COMPONENTS WITH FALLBACKS
# ============================================================================

# Set the guaranteed fallback as the default
BaseComponent = VisibleBaseComponent
HardwareComponent = VisibleBaseComponent
CORE_COMPONENTS_AVAILABLE = False

# Try to import core components
try:
    from core.components import BaseComponent as CoreBaseComponent, ProcessorComponent, HardwareComponent as CoreHardwareComponent
    # Only override if import succeeds
    BaseComponent = CoreBaseComponent
    HardwareComponent = CoreHardwareComponent
    CORE_COMPONENTS_AVAILABLE = True
    print("✓ Core components imported successfully")
except ImportError as e:
    print(f"⚠️ Core components not available, using fallback: {e}")

# Try to import hardware components (optional)
EnhancedHardwareComponent = VisibleBaseComponent
HARDWARE_COMPONENTS_AVAILABLE = False

try:
    from hardware.components import EnhancedHardwareComponent as HWEnhancedComponent
    EnhancedHardwareComponent = HWEnhancedComponent
    HARDWARE_COMPONENTS_AVAILABLE = True
    print("✓ Hardware components imported successfully")
except ImportError as e:
    print(f"⚠️ Hardware components not available, using fallback: {e}")

# Try to import layer manager
try:
    from core.layer_manager import LayerManager
    LAYER_MANAGER_AVAILABLE = True
    print("✓ Layer manager imported successfully")
except ImportError as e:
    print(f"⚠️ Layer manager not available, using fallback: {e}")
    
    class LayerManager:
        """Fallback layer manager"""
        def __init__(self):
            self.current_layer = "default"
        
        def get_current_layer(self):
            return self.current_layer
    
    LAYER_MANAGER_AVAILABLE = False

# ============================================================================
# MAIN CANVAS CLASS
# ============================================================================

class EnhancedPCBCanvas(QGraphicsView):
    """Enhanced PCB Canvas with robust error handling"""
    
    # Signals
    component_selected = pyqtSignal(object)
    component_moved = pyqtSignal(object, QPointF, QPointF)
    component_added = pyqtSignal(object)
    component_removed = pyqtSignal(object)
    connection_created = pyqtSignal(object, object, str, str)
    
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
        
        # Canvas settings
        self.grid_size = 20
        self.grid_visible = True
        self.snap_to_grid = True
        self.zoom_factor = 1.0
        self.grid_color = QColor(100, 140, 100)  # Brighter green grid color
        self._debug_grid = True  # Enable debug output once
        
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
        
        print("✓ Enhanced PCB Canvas initialized")
    
    def _make_background_transparent(self, pixmap: QPixmap) -> QPixmap:
        """Convert white/light backgrounds to transparent"""
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
                QColor(254, 254, 254, 255),  # Almost white
                QColor(253, 253, 253, 255),  # Light gray
                QColor(240, 240, 240, 255),  # Light gray
                QColor(220, 220, 220, 255),  # Gray
            ]
            
            # Get image dimensions
            width = image.width()
            height = image.height()
            
            # Check corner pixels to determine background color
            corner_colors = [
                image.pixelColor(0, 0),           # Top-left
                image.pixelColor(width-1, 0),     # Top-right
                image.pixelColor(0, height-1),    # Bottom-left
                image.pixelColor(width-1, height-1)  # Bottom-right
            ]
            
            # Find the most common corner color (likely background)
            background_color = None
            for corner_color in corner_colors:
                if corner_color.lightness() > 200:  # Light color
                    background_color = corner_color
                    break
            
            if background_color:
                print(f"🎨 Making background transparent: {background_color.name()}")
                
                # Make similar colors transparent
                for y in range(height):
                    for x in range(width):
                        pixel_color = image.pixelColor(x, y)
                        
                        # Calculate color difference
                        r_diff = abs(pixel_color.red() - background_color.red())
                        g_diff = abs(pixel_color.green() - background_color.green())
                        b_diff = abs(pixel_color.blue() - background_color.blue())
                        
                        # If color is very similar to background, make it transparent
                        if r_diff < 30 and g_diff < 30 and b_diff < 30:
                            # Set alpha to 0 (transparent)
                            transparent_color = QColor(pixel_color.red(), pixel_color.green(), 
                                                     pixel_color.blue(), 0)
                            image.setPixelColor(x, y, transparent_color)
            
            # Convert back to QPixmap
            result_pixmap = QPixmap.fromImage(image)
            print(f"🎨 Background transparency applied")
            return result_pixmap
            
        except Exception as e:
            print(f"⚠️ Error applying transparency: {e}")
            return pixmap  # Return original if processing fails
    
    def _setup_canvas(self):
        """Setup canvas properties"""
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
        """Setup mouse and keyboard interactions"""
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
    
    def set_grid_color(self, color: QColor):
        """Set the grid color"""
        self.grid_color = color
        self._debug_grid = True  # Enable debug for next draw
        self.viewport().update()  # Force redraw
        print(f"🎨 Grid color changed to: {color.name()}")
    
    def drawBackground(self, painter: QPainter, rect: QRectF):
        """Draw grid background with proper completion"""
        super().drawBackground(painter, rect)
        
        if not self.grid_visible:
            return
        
        # Set grid pen with customizable color - make it more visible
        grid_pen = QPen(self.grid_color, 1, Qt.PenStyle.SolidLine)
        painter.setPen(grid_pen)
        
        # Get the visible area
        left = int(rect.left())
        top = int(rect.top())
        right = int(rect.right())
        bottom = int(rect.bottom())
        
        # Align to grid
        left = left - (left % self.grid_size)
        top = top - (top % self.grid_size)
        
        # Draw vertical lines
        x = left
        while x <= right:
            line = QLineF(x, top, x, bottom)
            painter.drawLine(line)
            x += self.grid_size
        
        # Draw horizontal lines  
        y = top
        while y <= bottom:
            line = QLineF(left, y, right, y)
            painter.drawLine(line)
            y += self.grid_size
        
        # Debug output
        if hasattr(self, '_debug_grid') and self._debug_grid:
            print(f"🔍 Grid drawn: visible={self.grid_visible}, color={self.grid_color.name()}, size={self.grid_size}")
            print(f"🔍 Grid area: {left},{top} to {right},{bottom}")
            self._debug_grid = False
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle zoom with mouse wheel"""
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        
        # Save the scene pos
        old_pos = self.mapToScene(event.position().toPoint())
        
        # Zoom
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        
        self.scale(zoom_factor, zoom_factor)
        self.zoom_factor *= zoom_factor
        
        # Get the new position
        new_pos = self.mapToScene(event.position().toPoint())
        
        # Move scene to old position
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            print(f"🎯 Drag entered with: {event.mimeData().text()}")
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        """Handle drag move events"""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Handle drop events for adding components"""
        try:
            # Get component data
            component_data = event.mimeData()
            if not component_data.hasText():
                event.ignore()
                return
            
            # Parse component info from drag data
            try:
                # Try to parse as JSON first
                import json
                drag_data = json.loads(component_data.text())
                component_name = drag_data.get('name', 'Unknown Component')
                component_type = drag_data.get('type', 'unknown')
                print(f"🎯 Parsed JSON drag data: name={component_name}, type={component_type}")
            except:
                # Fallback - try to extract from the data or use a default
                data_str = str(component_data.text())
                if "68000" in data_str.lower():
                    component_name = "68000 CPU"
                    component_type = "cpu"
                elif "6502" in data_str.lower():
                    component_name = "6502 CPU"
                    component_type = "cpu"
                elif "z80" in data_str.lower():
                    component_name = "Z80 CPU"
                    component_type = "cpu"
                elif "paula" in data_str.lower():
                    component_name = "Paula"
                    component_type = "audio"
                elif "denise" in data_str.lower():
                    component_name = "Denise"
                    component_type = "video"
                elif "agnus" in data_str.lower():
                    component_name = "Agnus"
                    component_type = "video"
                else:
                    component_name = "68000 CPU"  # Default for testing
                    component_type = "cpu"
                print(f"🎯 Using pattern-matched component name: {component_name}")
            
            # Add component at drop position
            scene_pos = self.mapToScene(event.position().toPoint())
            snap_pos = self._snap_to_grid(scene_pos)
            
            self.add_component(component_type, component_name, snap_pos)
            event.acceptProposedAction()
            
        except Exception as e:
            print(f"⚠️ Error handling drop: {e}")
            import traceback
            traceback.print_exc()
            event.ignore()
    
    def add_component(self, component_type: str, name: str = None, position: QPointF = None) -> Optional[BaseComponent]:
        """Add component with improved image loading"""
        try:
            print(f"🔧 Adding component: {component_type}, name: {name}")
            
            # ALWAYS use the guaranteed visible component
            component = VisibleBaseComponent(component_type, name)
            
            # Position the component
            if position:
                snap_pos = self._snap_to_grid(position)
                component.setPos(snap_pos)
                print(f"🔧 Positioned component at: {snap_pos}")
            
            # Store in tracking dict
            self.components[component.id] = component
            
            # Add to scene
            self.scene.addItem(component)
            print(f"📦 Added to scene, total items: {len(self.scene.items())}")
            print(f"📦 Scene rect: {self.scene.sceneRect()}")
            print(f"📦 View rect: {self.rect()}")
            print(f"📦 Viewport rect: {self.viewport().rect()}")
            
            # Debug all scene items
            for i, item in enumerate(self.scene.items()):
                print(f"📦 Scene item {i}: pos={item.pos()}, rect={item.boundingRect()}, visible={item.isVisible()}")
            
            # Make selectable and movable
            component.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            component.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            
            # Force component to front and make fully visible
            component.setZValue(1000)  # Bring to front
            component.setOpacity(1.0)  # Full opacity
            component.setVisible(True)  # Explicitly visible
            
            # Debug component state after creation
            print(f"🔍 Component created - Name: {component.name}")
            print(f"🔍 Component rect: {component.boundingRect()}")
            print(f"🔍 Component visibility: {component.isVisible()}")
            print(f"🔍 Component opacity: {component.opacity()}")
            print(f"🔍 Component z-value: {component.zValue()}")
            print(f"🔍 Component flags: {component.flags()}")
            print(f"🔍 Has pinout_pixmap: {hasattr(component, 'pinout_pixmap')}")
            if hasattr(component, 'pinout_pixmap') and component.pinout_pixmap:
                print(f"🔍 Pixmap size: {component.pinout_pixmap.size()}")
                print(f"🔍 Pixmap is null: {component.pinout_pixmap.isNull()}")
            
            # Load actual chip image from your images directory
            self._load_chip_image(component, name)
            
            # Debug component state after image loading
            print(f"🔍 After image loading:")
            print(f"🔍 Component rect: {component.boundingRect()}")
            if hasattr(component, 'pinout_pixmap') and component.pinout_pixmap:
                print(f"🔍 Final pixmap size: {component.pinout_pixmap.size()}")
            
            # Force immediate visual update
            component.update()
            self.scene.update()
            self.viewport().update()
            
            # Emit signal
            self.component_added.emit(component)
            
            print(f"✓ Added component: {component.name} at {component.pos()}")
            return component
            
        except Exception as e:
            print(f"⚠️ Error adding component: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _load_chip_image(self, component, name: str):
        """Load actual chip image with high-quality scaling"""
        if not name:
            return
        
        # Clean name for filename matching
        clean_name = name.lower().replace(" ", "_").replace("-", "_")
        
        # Map component names to your actual image files - COMPLETE AMIGA COLLECTION
        image_mappings = {
            # 68000 CPU - A500 uses DIP-64, later models use different packages
            "68000_cpu": "images/components/cpu_68000_dip_64.png",  # A500 standard
            "68000": "images/components/cpu_68000_dip_64.png",
            "mc68000": "images/components/cpu_68000_dip_64.png",
            "68020": "images/components/cpu_68020_pga_68.png",
            "68030": "images/components/cpu_68030_pga_68.png", 
            "68040": "images/components/cpu_68040_pga_100.png",
            
            # Other CPUs
            "6502_cpu": "images/components/cpu-6502_dip_40.png",
            "6502": "images/components/cpu-6502_dip_40.png",
            "mos6502": "images/components/cpu-6502_dip_40.png",
            "z80_cpu": "images/components/cpu-z80_dip_40.png",
            "z80": "images/components/cpu-z80_dip_40.png",
            
            # Original Amiga Chips (OCS - A1000/A500)
            "paula": "images/components/amiga_paula_dip_48.png",
            "paula_8364": "images/components/amiga_paula_dip_48.png",
            "denise": "images/components/amiga_denise_plcc_48.png",
            "denise_8362": "images/components/amiga_denise_plcc_48.png",
            "agnus": "images/components/amiga_agnus_plcc_84.png",
            "agnus_8370": "images/components/amiga_agnus_plcc_84.png",
            "agnus_8371": "images/components/amiga_agnus_plcc_84.png",
            
            # Enhanced Amiga Chips (ECS - A500+/A600/A3000)
            "fat_agnus": "images/components/amiga_fat_agnus_plcc_84.png",
            "fat_agnus_8372a": "images/components/amiga_fat_agnus_plcc_84.png",
            "super_denise": "images/components/amiga_super_denise_plcc_48.png",
            "super_denise_8373": "images/components/amiga_super_denise_plcc_48.png",
            
            # Advanced Amiga Chips (AGA - A1200/A4000)
            "alice": "images/components/amiga_alice_plcc_84.png",
            "alice_8374": "images/components/amiga_alice_plcc_84.png",
            "aga_alice": "images/components/amiga_alice_plcc_84.png",
            "lisa": "images/components/amiga_lisa_plcc_68.png",
            "lisa_8375": "images/components/amiga_lisa_plcc_68.png",
            "aga_lisa": "images/components/amiga_lisa_plcc_68.png",
            
            # Amiga Support Chips
            "gary": "images/components/amiga_gary_plcc_68.png",
            "gary_8364": "images/components/amiga_gary_plcc_68.png",
            "ramsey": "images/components/amiga_ramsey_plcc_68.png",
            "ramsey_8372": "images/components/amiga_ramsey_plcc_68.png",
            "buster": "images/components/amiga_buster_plcc_52.png",
            "buster_8364": "images/components/amiga_buster_plcc_52.png",
            
            # CIA Chips
            "8520_cia": "images/components/c64_cia_dip_40.png",
            "8520": "images/components/c64_cia_dip_40.png",
            "cia": "images/components/c64_cia_dip_40.png",
            
            # C64 Chips
            "vic_ii": "images/components/c64_vic2_dip_40.png",
            "vic2": "images/components/c64_vic2_dip_40.png",
            "6567": "images/components/c64_vic2_dip_40.png",
            "sid": "images/components/c64_sid_dip_28.png",
            "6581": "images/components/c64_sid_dip_28.png",
            "6526": "images/components/c64_cia_dip_40.png",
            "mc68000": "images/components/cpu_68000_dip_64.png",    # A500 uses DIP-64 - CORRECTED FILENAME
            "6502_cpu": "images/components/cpu-6502_dip_40.png",
            "6502": "images/components/cpu-6502_dip_40.png",
            "mos6502": "images/components/cpu-6502_dip_40.png",
            "z80_cpu": "images/components/cpu-z80_dip_40.png",
            "z80": "images/components/cpu-z80_dip_40.png",
            "paula": "images/components/amiga_paula_dip_48.png",
            "denise": "images/components/amiga_denise_plcc_84.png",
            "agnus": "images/components/amiga_agnus_plcc_84.png",
            "vic_ii": "images/components/c64_vic2_dip_40.png",
            "vic2": "images/components/c64_vic2_dip_40.png",
            "sid": "images/components/c64_sid_dip_28.png",
            "6526": "images/components/c64_cia_dip_40.png",
            "cia": "images/components/c64_cia_dip_40.png"
        }
        
        # First try exact match
        image_path = image_mappings.get(clean_name)
        
        # Apply special package preference
        if not image_path:
            # For 68000, prefer DIP-64 (A500 standard) over PLCC
            if "68000" in clean_name:
                # Look for DIP-64 version first (Amiga A500 standard)
                for dip_key in ["cpu_68000_dip_64.png", "cpu-68000_dip_64.png", "cpu-68000_dip_40.png", "cpu-68000_plcc_68.png"]:
                    test_path = f"images/components/{dip_key}"
                    if os.path.exists(test_path):
                        image_path = test_path
                        print(f"🎯 Found 68000 variant: {test_path}")
                        break
            
            # General pattern matching for other chips
            if not image_path:
                for key, path in image_mappings.items():
                    if key in clean_name or clean_name in key:
                        image_path = path
                        break
        
        # Debug the matching process
        print(f"🔍 Looking for image for: '{name}' -> cleaned: '{clean_name}'")
        print(f"🔍 Exact match result: {image_path}")
        
        # Try loading the image with high-quality scaling
        if image_path and os.path.exists(image_path):
            try:
                print(f"📁 Found image file: {image_path}")
                original_pixmap = QPixmap(image_path)
                if not original_pixmap.isNull():
                    print(f"📏 Original image size: {original_pixmap.width()}x{original_pixmap.height()}")
                    
                    # Don't scale down high-quality images - use original size or scale up only
                    original_width = original_pixmap.width()
                    original_height = original_pixmap.height()
                    
                    # Use original size if it's reasonable, or scale to a good viewing size
                    if original_width >= 200 and original_height >= 150:
                        # Image is already good size, use it directly
                        scaled_pixmap = original_pixmap
                        target_width = original_width
                        target_height = original_height
                    else:
                        # Scale up smaller images to be more visible
                        scale_factor = max(2.0, 200.0 / max(original_width, original_height))
                        target_width = int(original_width * scale_factor)
                        target_height = int(original_height * scale_factor)
                        
                        # Scale with highest quality
                        scaled_pixmap = original_pixmap.scaled(
                            target_width,
                            target_height,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                    
                    print(f"📏 Final image size: {target_width}x{target_height}")
                    
                    # Update component with the image using new method
                    if hasattr(component, 'update_with_image'):
                        component.update_with_image(scaled_pixmap)
                    else:
                        # Fallback for other component types
                        component.pinout_pixmap = scaled_pixmap
                        if hasattr(component, 'setRect'):
                            component.setRect(0, 0, target_width, target_height)
                    
                    print(f"🖼️ Loaded high-quality chip image: {image_path} for {name}")
                    print(f"🔍 Component rect after image load: {component.boundingRect()}")
                    print(f"🔍 Component position: {component.pos()}")
                    print(f"🔍 Component Z-value: {component.zValue()}")
                    print(f"🔍 Component visible: {component.isVisible()}")
                    return
                else:
                    print(f"⚠️ Pixmap is null for: {image_path}")
            except Exception as e:
                print(f"⚠️ Error loading image {image_path}: {e}")
                import traceback
                traceback.print_exc()
        else:
            if image_path:
                print(f"📁 Image file not found: {image_path}")
                # Try fallback to DIP-64 version for A500 accuracy
                if "68000" in clean_name and ("plcc" in image_path or "dip_40" in image_path):
                    fallback_path = "images/components/cpu_68000_dip_64.png"
                    if os.path.exists(fallback_path):
                        print(f"📁 Trying DIP-64 fallback for A500: {fallback_path}")
                        # Load the fallback image directly instead of recursing
                        try:
                            fallback_pixmap = QPixmap(fallback_path)
                            if not fallback_pixmap.isNull():
                                # Scale the image to a reasonable size
                                scaled_pixmap = fallback_pixmap.scaled(200, 150, 
                                                     Qt.AspectRatioMode.KeepAspectRatio,
                                                     Qt.TransformationMode.SmoothTransformation)
                                
                                if hasattr(component, 'update_with_image'):
                                    component.update_with_image(scaled_pixmap)
                                
                                print(f"🖼️ Loaded A500 DIP-64 fallback: {fallback_path} (size: {scaled_pixmap.width()}x{scaled_pixmap.height()})")
                                return
                        except Exception as e:
                            print(f"⚠️ Error loading fallback image: {e}")
            else:
                print(f"📁 No mapping found for: {clean_name}")
        
        print(f"📷 No chip image found for {name}, using default visible component")
    
    def remove_component(self, component) -> bool:
        """Remove a component from the canvas"""
        try:
            if hasattr(component, 'id') and component.id in self.components:
                # Remove connections
                self._remove_component_connections(component)
                
                # Remove from scene and tracking
                self.scene.removeItem(component)
                del self.components[component.id]
                
                # Remove from selection
                if component in self.selected_components:
                    self.selected_components.remove(component)
                
                # Emit signal
                self.component_removed.emit(component)
                
                print(f"✓ Removed component: {component.name}")
                return True
        except Exception as e:
            print(f"⚠️ Error removing component: {e}")
        
        return False
    
    def _remove_component_connections(self, component):
        """Remove all connections for a component"""
        connections_to_remove = []
        
        for connection in self.connections:
            if (hasattr(connection, 'start_component') and connection.start_component == component) or \
               (hasattr(connection, 'end_component') and connection.end_component == component):
                connections_to_remove.append(connection)
        
        for connection in connections_to_remove:
            self.remove_connection(connection)
    
    def add_connection(self, start_component, start_port: str, end_component, end_port: str):
        """Add connection between components"""
        try:
            # Create connection object (simplified for now)
            connection = {
                'start_component': start_component,
                'start_port': start_port,
                'end_component': end_component,
                'end_port': end_port
            }
            
            self.connections.append(connection)
            self.connection_created.emit(start_component, end_component, start_port, end_port)
            
            print(f"✓ Connected {start_component.name}:{start_port} to {end_component.name}:{end_port}")
            return connection
            
        except Exception as e:
            print(f"⚠️ Error creating connection: {e}")
            return None
    
    def remove_connection(self, connection) -> bool:
        """Remove a connection"""
        try:
            if connection in self.connections:
                self.connections.remove(connection)
                
                # Remove visual representation if exists
                if hasattr(connection, 'graphics_item'):
                    self.scene.removeItem(connection.graphics_item)
                
                print("✓ Connection removed")
                return True
        except Exception as e:
            print(f"⚠️ Error removing connection: {e}")
        
        return False
    
    def _snap_to_grid(self, point: QPointF) -> QPointF:
        """Snap point to grid"""
        if not self.snap_to_grid:
            return point
        
        x = round(point.x() / self.grid_size) * self.grid_size
        y = round(point.y() / self.grid_size) * self.grid_size
        return QPointF(x, y)
    
    def get_component_at_position(self, position: QPointF):
        """Get component at given position"""
        items = self.scene.items(position)
        for item in items:
            if isinstance(item, (BaseComponent, EnhancedHardwareComponent, VisibleBaseComponent)):
                return item
        return None
    
    def clear_canvas(self):
        """Clear all components and connections"""
        try:
            if self.scene:
                self.scene.clear()
            self.components.clear()
            self.connections.clear()
            self.selected_components.clear()
            print("✓ Canvas cleared")
        except Exception as e:
            print(f"⚠️ Error clearing canvas: {e}")
    
    def cleanup(self):
        """Clean up canvas resources"""
        try:
            # Disconnect signals
            if self.scene:
                self.scene.deleteLater()
            print("✓ Canvas cleanup completed")
        except Exception as e:
            print(f"⚠️ Error during canvas cleanup: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Export canvas state to dictionary"""
        try:
            # Export components
            components_data = []
            for component in self.components.values():
                comp_data = {
                    'id': component.id,
                    'type': getattr(component, 'component_type', 'unknown'),
                    'name': getattr(component, 'name', ''),
                    'position': {'x': component.pos().x(), 'y': component.pos().y()},
                    'rotation': component.rotation()
                }
                
                # Add custom properties if available
                if hasattr(component, 'to_dict'):
                    comp_data.update(component.to_dict())
                
                components_data.append(comp_data)
            
            # Export connections
            connections_data = []
            for connection in self.connections:
                connections_data.append({
                    'start_component': getattr(connection, 'start_component', {}).get('id', ''),
                    'start_port': getattr(connection, 'start_port', ''),
                    'end_component': getattr(connection, 'end_component', {}).get('id', ''),
                    'end_port': getattr(connection, 'end_port', '')
                })
            
            return {
                'components': components_data,
                'connections': connections_data,
                'grid_size': self.grid_size,
                'grid_visible': self.grid_visible,
                'snap_to_grid': self.snap_to_grid
            }
            
        except Exception as e:
            print(f"⚠️ Error saving canvas: {e}")
            return {}
    
    def load_from_dict(self, data: Dict[str, Any]) -> bool:
        """Load canvas state from dictionary"""
        try:
            # Clear current state
            self.clear_canvas()
            
            # Load settings
            self.grid_size = data.get('grid_size', 20)
            self.grid_visible = data.get('grid_visible', True)
            self.snap_to_grid = data.get('snap_to_grid', True)
            
            # Load components
            for comp_data in data.get('components', []):
                component_type = comp_data.get('type', 'unknown')
                component = self.add_component(
                    component_type,
                    comp_data.get('name'),
                    QPointF(comp_data.get('position', {}).get('x', 0),
                           comp_data.get('position', {}).get('y', 0))
                )
                
                if component:
                    component.setRotation(comp_data.get('rotation', 0))
                    if hasattr(component, 'from_dict'):
                        component.from_dict(comp_data)
            
            # Load connections (after components are loaded)
            for conn_data in data.get('connections', []):
                start_comp_id = conn_data.get('start_component')
                end_comp_id = conn_data.get('end_component')
                
                start_comp = self.components.get(start_comp_id)
                end_comp = self.components.get(end_comp_id)
                
                if start_comp and end_comp:
                    self.add_connection(
                        start_comp, conn_data.get('start_port', ''),
                        end_comp, conn_data.get('end_port', '')
                    )
            
            print("✓ Canvas loaded from data")
            return True
            
        except Exception as e:
            print(f"⚠️ Error loading canvas: {e}")
            return False

    # Grid control methods
    def set_grid_visible(self, visible: bool):
        """Set grid visibility"""
        self.grid_visible = visible
        self.viewport().update()
        print(f"🔧 Grid {'visible' if visible else 'hidden'}")
    
    def set_grid_size(self, size: int):
        """Set grid size"""
        self.grid_size = max(5, min(100, size))  # Clamp between 5-100
        self.viewport().update()
        print(f"🔧 Grid size set to: {self.grid_size}")
    
    def set_snap_to_grid(self, enabled: bool):
        """Set snap to grid"""
        self.snap_to_grid = enabled
        print(f"🔧 Snap to grid {'enabled' if enabled else 'disabled'}")

    # View control methods
    def zoom_to_fit(self):
        """Zoom to fit all components"""
        if self.components:
            self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            print("🔍 Zoomed to fit all components")
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.resetTransform()
        self.zoom_factor = 1.0
        print("🔍 Zoom reset to 100%")

    def load_chip_image_with_loader(self, component, loader):
        """Load chip image using enhanced loader"""
        try:
            if loader and hasattr(loader, 'load_component_image'):
                image_path = loader.load_component_image(component)
                if image_path:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        if hasattr(component, 'update_with_image'):
                            component.update_with_image(pixmap)
                        else:
                            component.pinout_pixmap = pixmap
                            if hasattr(component, 'setRect'):
                                component.setRect(0, 0, pixmap.width(), pixmap.height())
                        print(f"🖼️ Loaded image via loader: {image_path}")
                        return True
            return False
        except Exception as e:
            print(f"⚠️ Error loading image with loader: {e}")
            return False


# Create alias for backward compatibility
PCBCanvas = EnhancedPCBCanvas
