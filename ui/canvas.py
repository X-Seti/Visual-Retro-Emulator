"""
X-Seti - June11 2025 - Enhanced PCB Canvas
Visual Retro Emulator - Canvas Module
"""

import os
import sys
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# Import fallback components first
try:
    from core.components import BaseComponent, ProcessorComponent, HardwareComponent
    CORE_COMPONENTS_AVAILABLE = True
    print("✓ Core components imported successfully")
except ImportError as e:
    print(f"⚠️ Core components not available: {e}")
    CORE_COMPONENTS_AVAILABLE = False
    
    # Create fallback base component that's always visible
    class VisibleBaseComponent(QGraphicsRectItem):
        """Guaranteed visible fallback component"""
        
        def __init__(self, component_type: str = "unknown", name: str = None):
            super().__init__()
            
            # Generate unique ID
            import uuid
            self.id = str(uuid.uuid4())
            
            # Basic properties
            self.component_type = component_type
            self.name = name or f"{component_type}_{self.id[:8]}"
            
            # Visual properties
            self.width = 120
            self.height = 80
            self.pinout_pixmap = None
            
            # Set rectangle bounds
            self.setRect(0, 0, self.width, self.height)
            
            # Force visibility
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.setVisible(True)
            self.setOpacity(1.0)
            
            # Default colors
            self.setBrush(QBrush(QColor(80, 80, 120)))  # Dark blue-gray
            self.setPen(QPen(QColor(200, 200, 200), 2))  # Light border
            
            print(f"🔧 Created VisibleBaseComponent: {self.name}")
        
        def paint(self, painter: QPainter, option, widget=None):
            """Custom paint method for realistic chip appearance"""
            # If we have a pinout image, draw it
            if hasattr(self, 'pinout_pixmap') and self.pinout_pixmap:
                print(f"🖼️ Drawing pinout image for: {self.name}")
                painter.drawPixmap(self.boundingRect().toRect(), self.pinout_pixmap)
            else:
                # Realistic chip appearance fallback
                rect = self.boundingRect()
                
                # Draw chip body (dark gray/black like real chips)
                painter.fillRect(rect, QColor(40, 40, 40))  # Dark chip body
                
                # Draw chip border (metallic look)
                painter.setPen(QPen(QColor(160, 160, 160), 2))  # Light gray border
                painter.drawRect(rect)
                
                # Draw pin indicators (small rectangles on sides)
                pin_width = 3
                pin_height = 8
                pin_spacing = 8
                
                # Left side pins
                y_start = 10
                for i in range(int((rect.height() - 20) / pin_spacing)):
                    y_pos = y_start + i * pin_spacing
                    if y_pos + pin_height < rect.height() - 10:
                        painter.fillRect(0, y_pos, pin_width, pin_height, QColor(200, 200, 200))
                
                # Right side pins
                for i in range(int((rect.height() - 20) / pin_spacing)):
                    y_pos = y_start + i * pin_spacing
                    if y_pos + pin_height < rect.height() - 10:
                        painter.fillRect(rect.width() - pin_width, y_pos, pin_width, pin_height, QColor(200, 200, 200))
                
                # Draw chip label (white text on dark background)
                painter.setPen(QPen(QColor(255, 255, 255)))
                font = QFont("Arial", 8, QFont.Weight.Bold)
                painter.setFont(font)
                
                # Draw text with background
                text_rect = rect.adjusted(5, 5, -5, -5)
                painter.fillRect(text_rect, QColor(0, 0, 0, 100))  # Semi-transparent background
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)
                
                # Draw notch (chip orientation indicator)
                notch_size = 8
                notch_rect = QRectF(rect.center().x() - notch_size/2, rect.top(), notch_size, notch_size/2)
                painter.fillRect(notch_rect, QColor(20, 20, 20))
            
            # Selection highlight
            if self.isSelected():
                painter.setPen(QPen(QColor(0, 150, 255), 3))  # Blue selection
                painter.setBrush(QBrush())
                painter.drawRect(self.boundingRect().adjusted(-2, -2, 2, 2))
        
        def shape(self):
            """Return the shape for selection"""
            path = QPainterPath()
            path.addRect(self.boundingRect())
            return path

    # Use our guaranteed visible component at module level
    BaseComponent = VisibleBaseComponent

# Try to import hardware components
try:
    from hardware.components import EnhancedHardwareComponent
    HARDWARE_COMPONENTS_AVAILABLE = True
    print("✓ Hardware components imported")
except ImportError as e:
    print(f"⚠️ Hardware components not available: {e}")
    HARDWARE_COMPONENTS_AVAILABLE = False
    EnhancedHardwareComponent = VisibleBaseComponent

# Try to import connections
try:
    from connections.connection_system import Connection, EnhancedConnection
    CONNECTION_SYSTEM_AVAILABLE = True
    print("✓ Connection system imported")
except ImportError as e:
    print(f"⚠️ Connection system not available: {e}")
    CONNECTION_SYSTEM_AVAILABLE = False
    
    # Create fallback connection
    class Connection(QGraphicsLineItem):
        def __init__(self, start_point: QPointF, end_point: QPointF):
            super().__init__(QLineF(start_point, end_point))
            self.setPen(QPen(QColor(255, 255, 0), 2))  # Yellow connection
    
    EnhancedConnection = Connection

# Layer Manager
class LayerManager:
    """Manage canvas layers"""
    
    def __init__(self):
        self.layers = {
            "chip": {"visible": True, "opacity": 1.0},
            "pcb": {"visible": False, "opacity": 0.5},
            "gerber": {"visible": False, "opacity": 0.3}
        }
        self.current_layer = "chip"
    
    def set_layer_visibility(self, name: str, visible: bool):
        """Set layer visibility"""
        if name in self.layers:
            self.layers[name]["visible"] = visible
    
    def get_layer_visibility(self, name: str) -> bool:
        """Get layer visibility"""
        return self.layers.get(name, {}).get("visible", False)
    
    def set_current_layer(self, name: str):
        """Set current active layer"""
        if name in self.layers:
            self.current_layer = name
    
    def get_current_layer(self) -> str:
        """Get current active layer"""
        return self.current_layer

# Try to import database
try:
    from database.retro_database import retro_database
    DATABASE_AVAILABLE = True
    print("✓ Retro database imported")
except ImportError as e:
    print(f"⚠️ Retro database not available: {e}")
    DATABASE_AVAILABLE = False
    
    # Create placeholder database
    class PlaceholderDatabase:
        def __init__(self):
            self.components = []
        
        def get_component(self, name: str):
            return None
        
        def get_all_components(self):
            return []
        
        def search_components(self, query: str):
            return []
    
    retro_database = PlaceholderDatabase()

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
    
    def _setup_canvas(self):
        """Setup canvas properties"""
        # Set scene size
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        
        # Configure view
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Set background
        self.setBackgroundBrush(QBrush(QColor(20, 20, 30)))  # Dark background
        
        # Grid drawing will be handled in drawBackground
    
    def _setup_interactions(self):
        """Setup mouse and keyboard interactions"""
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
    
    def drawBackground(self, painter: QPainter, rect: QRectF):
        """Draw grid background"""
        super().drawBackground(painter, rect)
        
        if not self.grid_visible:
            return
        
        # Set grid pen
        painter.setPen(QPen(QColor(60, 60, 80), 1, Qt.PenStyle.DotLine))
        
        # Draw grid lines
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
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
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle zoom with mouse wheel"""
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        
        # Get mouse position in scene coordinates
        old_pos = self.mapToScene(event.position().toPoint())
        
        # Zoom
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        
        self.scale(zoom_factor, zoom_factor)
        
        # Get new mouse position
        new_pos = self.mapToScene(event.position().toPoint())
        
        # Move scene to keep mouse position constant
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
        
        self.zoom_factor *= zoom_factor
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.MiddleButton:
            # Pan mode
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.drag_start_pos = event.position()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events"""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
        super().mouseReleaseEvent(event)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter for component drops"""
        if event.mimeData().hasFormat("application/x-component"):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event: QDragMoveEvent):
        """Handle drag move events"""
        if event.mimeData().hasFormat("application/x-component"):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event: QDropEvent):
        """Handle component drops onto canvas"""
        try:
            if not event.mimeData().hasFormat("application/x-component"):
                event.ignore()
                return
            
            # Get component data
            component_data_bytes = event.mimeData().data("application/x-component")
            component_data_str = component_data_bytes.data().decode('utf-8')
            
            try:
                import json
                component_data = json.loads(component_data_str)
            except json.JSONDecodeError:
                # Fallback to simple parsing
                component_data = {"name": component_data_str, "type": "unknown"}
            
            # Convert drop position to scene coordinates
            drop_pos = self.mapToScene(event.position().toPoint())
            
            # Create component
            component = self.add_component(
                component_data.get('type', 'unknown'),
                component_data.get('name'),
                drop_pos
            )
            
            if component:
                event.acceptProposedAction()
                print(f"✅ Component dropped successfully: {component_data.get('name')} at {drop_pos}")
                print(f"📊 Total components on canvas: {len(self.components)}")
            else:
                print("❌ Failed to create component")
                event.ignore()
                
        except Exception as e:
            print(f"💥 Error handling drop: {e}")
            import traceback
            traceback.print_exc()
            event.ignore()
    
    def add_component(self, component_type: str, name: str = None, 
                     position: QPointF = None) -> Optional[VisibleBaseComponent]:
        """Add a component to the canvas"""
        try:
            # FORCE use of our VisibleBaseComponent - guaranteed to work
            component = VisibleBaseComponent(component_type, name)
            print(f"🔧 FORCED VisibleBaseComponent creation: {component.name}")
            
            print(f"🔧 Created component: {component.name}, bounding rect: {component.boundingRect()}")
            
            # Set position
            if position:
                if self.snap_to_grid:
                    position = self._snap_to_grid(position)
                component.setPos(position)
                print(f"📍 Set position: {position}")
            else:
                # Default position at center
                center = self.mapToScene(self.viewport().rect().center())
                if self.snap_to_grid:
                    center = self._snap_to_grid(center)
                component.setPos(center)
            
            # Add to scene and tracking
            self.scene.addItem(component)
            self.components[component.id] = component
            print(f"📦 Added to scene, total items: {len(self.scene.items())}")
            
            # Make selectable and movable
            component.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            component.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            
            # Force component to front and make fully visible
            component.setZValue(100)  # Bring to front
            component.setOpacity(1.0)  # Full opacity
            component.setVisible(True)  # Explicitly visible
            
            # Debug component state
            print(f"🔍 Component visibility: {component.isVisible()}")
            print(f"🔍 Component opacity: {component.opacity()}")
            print(f"🔍 Component z-value: {component.zValue()}")
            print(f"🔍 Component flags: {component.flags()}")
            
            # Load actual chip image from your images directory
            self._load_chip_image(component, name)
            
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
        """Load actual chip image from your images/components directory"""
        if not name:
            return
        
        # Clean name for filename matching
        clean_name = name.lower().replace(" ", "_").replace("-", "_")
        
        # Map component names to your actual image files
        image_mappings = {
            # CPUs
            "6502 cpu": "images/components/cpu-6502_dip_40.png",
            "68000 cpu": "images/components/cpu-68000_dip_40.png", 
            "68020 cpu": "images/components/cpu-68000_dip_40.png",  # Use 68000 for 68020
            "8502 cpu": "images/components/cpu-6502_dip_40.png",    # Use 6502 for 8502
            "z80 cpu": "images/components/cpu-z80_dip_40.png",
            "6507 cpu": "images/components/cpu-6502_dip_40.png",    # Use 6502 for 6507
            
            # Commodore chips
            "6567 vic-ii": "images/components/c64_vic2_dip_40.png",
            "6581 sid": "images/components/c64_sid_dip_28.png",
            "8563 vdc": "images/components/c64_vic2_dip_40.png",    # Use VIC-II for VDC
            
            # Amiga chips  
            "agnus": "images/components/amiga_agnus_dip_84.png",
            "denise": "images/components/amiga_denise_dip_48.png", 
            "paula": "images/components/amiga_paula_dip_48.png",
            
            # Atari chips
            "antic": "images/components/atari_antic_dip_40.png",
            "gtia": "images/components/atari_gtia_dip_40.png",
            "pokey": "images/components/atari_pokey_dip_40.png",
        }
        
        # Try exact match first
        image_path = image_mappings.get(clean_name)
        
        # If no exact match, try pattern matching
        if not image_path:
            for key, path in image_mappings.items():
                if key in clean_name or clean_name in key:
                    image_path = path
                    break
        
        # Try loading the image - FIXED: Complete try-except block
        if image_path and os.path.exists(image_path):
            try:
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    # Scale to component size while keeping aspect ratio
                    scaled = pixmap.scaled(component.width, component.height, 
                                         Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
                    
                    # Store pixmap for painting
                    component.pinout_pixmap = scaled
                    
                    # Adjust component size to match image
                    component.width = scaled.width()
                    component.height = scaled.height()
                    
                    print(f"🖼️ Loaded chip image: {image_path} for {name}")
                    return
            except Exception as e:
                print(f"⚠️ Error loading image {image_path}: {e}")
        
        print(f"📷 No chip image found for {name}, using realistic chip drawing")
    
    def _try_load_component_image(self, component, name: str):
        """Try to load component image from your images directory"""
        if not name:
            return
        
        # Clean name for filename matching
        clean_name = name.lower().replace(" ", "_").replace("-", "_")
        
        # Try various image path combinations based on your file list
        image_patterns = [
            f"images/components/c64_vic2_dip_40.png",  # VIC-II
            f"images/components/cpu-6502_dip_40.png",  # 6502
            f"images/components/cpu-68000_dip_40.png", # 68000
            f"images/components/c64_sid_dip_28.png",   # SID
            f"images/components/{clean_name}_dip_40.png",
            f"images/cpu_{clean_name}_dip_40.png",
            f"images/{clean_name}.png"
        ]
        
        for pattern in image_patterns:
            if os.path.exists(pattern):
                try:
                    pixmap = QPixmap(pattern)
                    if not pixmap.isNull():
                        # Scale to reasonable size
                        scaled = pixmap.scaled(120, 80, 
                                             Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
                        
                        # Store pixmap for painting
                        component.pinout_pixmap = scaled
                        component.setRect(0, 0, scaled.width(), scaled.height())
                        print(f"🖼️ Loaded image: {pattern} for {name}")
                        return
                except Exception as e:
                    print(f"⚠️ Error loading image {pattern}: {e}")
        
        print(f"📷 No image found for {name}, using colored rectangle")
    
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
    
    def add_connection(self, start_component, start_port: str, 
                      end_component, end_port: str) -> Optional[Connection]:
        """Add a connection between components"""
        try:
            if CONNECTION_SYSTEM_AVAILABLE:
                connection = EnhancedConnection(start_component.pos(), end_component.pos())
            else:
                connection = Connection(start_component.pos(), end_component.pos())
            
            # Set connection properties
            connection.start_component = start_component
            connection.start_port = start_port
            connection.end_component = end_component
            connection.end_port = end_port
            
            # Add to scene and tracking
            self.scene.addItem(connection)
            self.connections.append(connection)
            
            # Connect components
            if hasattr(start_component, 'connect_to_component'):
                start_component.connect_to_component(end_component, start_port, end_port)
            
            # Emit signal
            self.connection_created.emit(start_component, end_component, start_port, end_port)
            
            print(f"✓ Connected {start_component.name}:{start_port} -> {end_component.name}:{end_port}")
            return connection
            
        except Exception as e:
            print(f"⚠️ Error creating connection: {e}")
            return None
    
    def remove_connection(self, connection) -> bool:
        """Remove a connection"""
        try:
            if connection in self.connections:
                # Disconnect components
                if (hasattr(connection, 'start_component') and 
                    hasattr(connection, 'end_component') and
                    hasattr(connection.start_component, 'disconnect_from_component')):
                    connection.start_component.disconnect_from_component(
                        connection.end_component, 
                        connection.start_port, 
                        connection.end_port
                    )
                
                # Remove from scene and tracking
                self.scene.removeItem(connection)
                self.connections.remove(connection)
                
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
            if isinstance(item, (BaseComponent, EnhancedHardwareComponent)):
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

# Create alias for backward compatibility
PCBCanvas = EnhancedPCBCanvas
