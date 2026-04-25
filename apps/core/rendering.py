# X-Seti - June23 2025 - Component Rendering System with Pin Numbers
# this belongs in core/rendering.py

import math
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygonF, QPainter, QFont


class ICPackage:
    """Defines standard IC package types with accurate dimensions and pin layouts"""
    
    # Package types with accurate dimensions for proper pin spacing (2.54mm = 8px scale)
    PACKAGES = {
        # DIP packages
        "DIP-8": {"width": 80, "height": 60, "pins": 8, "pin_spacing": 8, "row_spacing": 7.62},
        "DIP-14": {"width": 80, "height": 80, "pins": 14, "pin_spacing": 8, "row_spacing": 7.62},
        "DIP-16": {"width": 80, "height": 90, "pins": 16, "pin_spacing": 8, "row_spacing": 7.62},
        "DIP-18": {"width": 80, "height": 100, "pins": 18, "pin_spacing": 8, "row_spacing": 7.62},
        "DIP-20": {"width": 80, "height": 110, "pins": 20, "pin_spacing": 8, "row_spacing": 7.62},
        "DIP-24": {"width": 80, "height": 130, "pins": 24, "pin_spacing": 8, "row_spacing": 7.62},
        "DIP-28": {"width": 80, "height": 150, "pins": 28, "pin_spacing": 8, "row_spacing": 7.62},
        "DIP-40": {"width": 80, "height": 200, "pins": 40, "pin_spacing": 8, "row_spacing": 15.24},
        "DIP-64": {"width": 120, "height": 220, "pins": 64, "pin_spacing": 6, "row_spacing": 22.86},
        "DIP-48": {"width": 100, "height": 200, "pins": 48, "pin_spacing": 7, "row_spacing": 15.24},
        
        # Surface mount packages
        "SOIC-8": {"width": 60, "height": 40, "pins": 8, "pin_spacing": 6, "row_spacing": 5.3},
        "SOIC-14": {"width": 80, "height": 50, "pins": 14, "pin_spacing": 6, "row_spacing": 5.3},
        "SOIC-16": {"width": 90, "height": 55, "pins": 16, "pin_spacing": 6, "row_spacing": 5.3},
        "SOIC-28": {"width": 120, "height": 60, "pins": 28, "pin_spacing": 6, "row_spacing": 5.3},
        
        # Quad packages
        "PLCC-44": {"width": 120, "height": 120, "pins": 44, "pin_spacing": 6, "quad": True},
        "PLCC-68": {"width": 150, "height": 150, "pins": 68, "pin_spacing": 5, "quad": True},
        "QFP-44": {"width": 120, "height": 120, "pins": 44, "pin_spacing": 5, "quad": True},
        "QFP-64": {"width": 140, "height": 140, "pins": 64, "pin_spacing": 4, "quad": True},
        "QFP-80": {"width": 160, "height": 160, "pins": 80, "pin_spacing": 4, "quad": True},
        "QFP-100": {"width": 180, "height": 180, "pins": 100, "pin_spacing": 3.5, "quad": True},
        
        # Grid packages
        "PGA-68": {"width": 180, "height": 180, "pins": 68, "pin_spacing": 10, "grid": True},
        "BGA-256": {"width": 200, "height": 200, "pins": 256, "pin_spacing": 8, "grid": True}
    }
    
    @classmethod
    def get_package_info(cls, package_type):
        """Get package information"""
        return cls.PACKAGES.get(package_type, cls.PACKAGES["DIP-40"])
    
    @classmethod
    def calculate_pin_positions(cls, package_type):
        """Calculate pin positions for a package type"""
        pkg_info = cls.get_package_info(package_type)
        
        if "quad" in pkg_info:
            return cls._calculate_quad_pins(pkg_info)
        elif "grid" in pkg_info:
            return cls._calculate_grid_pins(pkg_info)
        else:
            return cls._calculate_dip_pins(pkg_info)
    
    @classmethod
    def _calculate_dip_pins(cls, pkg_info):
        """Calculate pin positions for DIP packages"""
        pins = []
        pin_count = pkg_info["pins"]
        pins_per_side = pin_count // 2
        height = pkg_info["height"]
        
        if pins_per_side <= 1:
            return pins
        
        pin_spacing = (height - 20) / (pins_per_side - 1)
        
        # Left side pins (1 to pins_per_side)
        for i in range(pins_per_side):
            pins.append({
                "number": i + 1,
                "x": 0,
                "y": 10 + i * pin_spacing,
                "side": "left"
            })
        
        # Right side pins (pin_count down to pins_per_side + 1)
        for i in range(pins_per_side):
            pins.append({
                "number": pin_count - i,
                "x": pkg_info["width"],
                "y": 10 + i * pin_spacing,
                "side": "right"
            })
        
        return pins
    
    @classmethod
    def _calculate_quad_pins(cls, pkg_info):
        """Calculate pin positions for quad packages (QFP, PLCC)"""
        pins = []
        pin_count = pkg_info["pins"]
        pins_per_side = pin_count // 4
        width = pkg_info["width"]
        height = pkg_info["height"]
        
        if pins_per_side <= 1:
            return pins
        
        pin_spacing = (width - 20) / (pins_per_side - 1)
        pin_num = 1
        
        # Top side (left to right)
        for i in range(pins_per_side):
            pins.append({
                "number": pin_num,
                "x": 10 + i * pin_spacing,
                "y": 0,
                "side": "top"
            })
            pin_num += 1
        
        # Right side (top to bottom)
        for i in range(pins_per_side):
            pins.append({
                "number": pin_num,
                "x": width,
                "y": 10 + i * pin_spacing,
                "side": "right"
            })
            pin_num += 1
        
        # Bottom side (right to left)
        for i in range(pins_per_side):
            pins.append({
                "number": pin_num,
                "x": width - 10 - i * pin_spacing,
                "y": height,
                "side": "bottom"
            })
            pin_num += 1
        
        # Left side (bottom to top)
        for i in range(pins_per_side):
            pins.append({
                "number": pin_num,
                "x": 0,
                "y": height - 10 - i * pin_spacing,
                "side": "left"
            })
            pin_num += 1
        
        return pins
    
    @classmethod
    def _calculate_grid_pins(cls, pkg_info):
        """Calculate pin positions for grid packages (PGA, BGA)"""
        pins = []
        pin_count = pkg_info["pins"]
        grid_size = int(math.sqrt(pin_count))
        width = pkg_info["width"]
        height = pkg_info["height"]
        
        spacing_x = width / (grid_size + 1)
        spacing_y = height / (grid_size + 1)
        
        pin_num = 1
        for row in range(grid_size):
            for col in range(grid_size):
                if pin_num <= pin_count:
                    pins.append({
                        "number": pin_num,
                        "x": spacing_x * (col + 1),
                        "y": spacing_y * (row + 1),
                        "side": "grid"
                    })
                    pin_num += 1
        
        return pins


class PinPoint(QGraphicsEllipseItem):
    """Pin point with accurate positioning and visual representation"""
    
    def __init__(self, parent, pin_info, pin_def, layer_mode="chip"):
        self.pin_info = pin_info  # Physical pin information
        self.pin_def = pin_def    # Logical pin definition
        self.layer_mode = layer_mode
        
        # Pin numbers visibility
        self.pin_numbers_visible = True
        self._pin_number_text = None
        
        # Size based on layer mode
        if layer_mode == "chip":
            radius = 3
        elif layer_mode == "pcb":
            radius = 4
        else:  # gerber
            radius = 2
        
        super().__init__(-radius, -radius, radius*2, radius*2, parent)
        self.setPos(pin_info["x"], pin_info["y"])
        
        # Set appearance based on pin type and layer
        self._set_appearance()
        
        # Enable selection and interaction
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        
        # Tooltip with pin information
        tooltip = f"Pin {pin_info['number']}: {pin_def['name']} ({pin_def['type']}, {pin_def['direction']})"
        self.setToolTip(tooltip)
        
        # Connection tracking
        self.connections = []
        
        # Create pin number text
        self._create_pin_number_text()
    
    def get_scene_pos(self):
        """Get the scene position of this pin"""
        return self.scenePos()
    
    def set_pin_numbers_visible(self, visible):
        """Set pin number visibility"""
        self.pin_numbers_visible = visible
        if self._pin_number_text:
            self._pin_number_text.setVisible(visible)
    
    def _create_pin_number_text(self):
        """Create pin number text item"""
        if hasattr(self, 'pin_info') and 'number' in self.pin_info:
            self._pin_number_text = QGraphicsTextItem(str(self.pin_info['number']), self)
            self._pin_number_text.setFont(QFont("Arial", 6, QFont.Weight.Bold))
            self._pin_number_text.setDefaultTextColor(QColor(255, 255, 0))  # Yellow
            
            # Position text based on pin side
            text_rect = self._pin_number_text.boundingRect()
            side = self.pin_info.get('side', 'left')
            
            if side == 'left':
                self._pin_number_text.setPos(-text_rect.width() - 15, -text_rect.height() / 2)
            elif side == 'right':
                self._pin_number_text.setPos(8, -text_rect.height() / 2)
            elif side == 'top':
                self._pin_number_text.setPos(-text_rect.width() / 2, -text_rect.height() - 8)
            elif side == 'bottom':
                self._pin_number_text.setPos(-text_rect.width() / 2, 8)
            else:  # grid or default
                self._pin_number_text.setPos(8, -text_rect.height() / 2)
            
            self._pin_number_text.setVisible(self.pin_numbers_visible)
    
    def _set_appearance(self):
        """Set pin appearance based on type and layer mode"""
        # Color coding by pin type
        type_colors = {
            "power": QColor(255, 0, 0),      # Red
            "ground": QColor(0, 0, 0),       # Black
            "address": QColor(255, 165, 0),   # Orange
            "data": QColor(0, 100, 255),     # Blue
            "control": QColor(128, 0, 128),   # Purple
            "clock": QColor(0, 255, 0),      # Green
            "analog": QColor(255, 192, 203),  # Pink
            "video": QColor(255, 255, 0),    # Yellow
            "audio": QColor(0, 255, 255),    # Cyan
            "unused": QColor(128, 128, 128), # Gray
            "interrupt": QColor(255, 128, 0), # Orange-red
            "reset": QColor(255, 0, 255),    # Magenta
            "default": QColor(100, 100, 100) # Dark gray
        }
        
        color = type_colors.get(self.pin_def.get("type", "default"), type_colors["default"])
        
        if self.layer_mode == "chip":
            self.setBrush(QBrush(color))
            self.setPen(QPen(Qt.GlobalColor.black, 1))
        elif self.layer_mode == "pcb":
            # PCB pads are typically copper colored
            self.setBrush(QBrush(QColor(184, 115, 51)))  # Copper color
            self.setPen(QPen(Qt.GlobalColor.darkRed, 2))
        else:  # gerber
            # Gerber view shows drill holes
            self.setBrush(QBrush(Qt.GlobalColor.white))
            self.setPen(QPen(Qt.GlobalColor.black, 1))


class HardwareComponent(QGraphicsRectItem):
    """Hardware component with accurate IC package rendering and pin numbers"""
    
    def __init__(self, component_def, package_type=None, layer_mode="chip"):
        self.component_def = component_def
        self.layer_mode = layer_mode
        
        # Pin numbers visibility
        self.pin_numbers_visible = True
        
        # Determine package type
        if package_type:
            self.package_type = package_type
        else:
            # Try to infer from component definition or use default
            self.package_type = getattr(component_def, 'package_type', 'DIP-40')
        
        # Get package dimensions
        self.package_info = ICPackage.get_package_info(self.package_type)
        width = self.package_info["width"]
        height = self.package_info["height"]
        
        super().__init__(0, 0, width, height)
        
        # Component properties
        self.component_id = component_def.component_id
        self.name = component_def.name
        self.category = component_def.category
        self.description = component_def.description
        self.properties = {}
        
        # Copy properties from definition
        self.properties = {}
        if hasattr(component_def, 'properties') and component_def.properties:
            try:
                # Handle list of property dictionaries
                if isinstance(component_def.properties, list):
                    for prop in component_def.properties:
                        if isinstance(prop, dict) and "name" in prop and "default" in prop:
                            self.properties[prop["name"]] = prop["default"]
                        else:
                            print(f"⚠️  Skipping invalid property: {prop}")
                
                # Handle direct dictionary of properties
                elif isinstance(component_def.properties, dict):
                    self.properties = component_def.properties.copy()
                
                else:
                    print(f"⚠️  Unknown properties structure: {type(component_def.properties)}")
                    
            except Exception as e:
                print(f"⚠️  Error copying properties for {component_def.name}: {e}")
                self.properties = {}
        
        # Set interaction flags
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Set appearance based on layer mode
        self._set_appearance()
        
        # Create pins
        self.pin_points = {}
        self._create_pins()
        
        # Add component identifier notch for DIP packages
        self._add_package_features()
    
    def set_pin_numbers_visible(self, visible):
        """Set pin numbers visibility for this component"""
        self.pin_numbers_visible = visible
        
        # Update all pin points
        for pin_point in self.pin_points.values():
            if hasattr(pin_point, 'set_pin_numbers_visible'):
                pin_point.set_pin_numbers_visible(visible)
        
        # Force component repaint
        self.update()
        
        print(f"🔢 Pin numbers {'visible' if visible else 'hidden'} on {self.name}")
    
    def get_pin_numbers_visible(self):
        """Get pin numbers visibility state"""
        return self.pin_numbers_visible
    
    def _set_appearance(self):
        """Set component appearance based on layer mode"""
        if self.layer_mode == "chip":
            # Chip view - realistic IC colors
            if "CPU" in self.category.upper():
                color = QColor(20, 20, 20)  # Dark ceramic
            elif "MEMORY" in self.category.upper():
                color = QColor(50, 50, 50)  # Dark gray
            elif "CUSTOM" in self.category.upper():
                color = QColor(40, 40, 80)  # Dark blue
            else:
                color = QColor(60, 60, 60)  # Default dark
            
            self.setBrush(QBrush(color))
            self.setPen(QPen(Qt.GlobalColor.lightGray, 2))
            
        elif self.layer_mode == "pcb":
            # PCB component outline
            self.setBrush(QBrush(Qt.GlobalColor.transparent))
            self.setPen(QPen(Qt.GlobalColor.white, 2, Qt.PenStyle.DashLine))
            
        else:  # gerber
            # Gerber layer - component outline
            self.setBrush(QBrush(Qt.GlobalColor.transparent))
            self.setPen(QPen(Qt.GlobalColor.yellow, 1))
    
    def _create_pins(self):
        """Create pins with accurate package positioning"""
        try:
            # Get physical pin positions from package
            physical_pins = ICPackage.calculate_pin_positions(self.package_type)
            
            # Map logical pins to physical pins
            logical_pins = {pin["name"]: pin for pin in self.component_def.pins}
            
            # Create pin objects
            for i, phys_pin in enumerate(physical_pins):
                # Try to find matching logical pin
                logical_pin = None
                
                # First try to match by pin number if available
                pin_name = f"Pin{phys_pin['number']}"
                if pin_name in logical_pins:
                    logical_pin = logical_pins[pin_name]
                else:
                    # Try to match by index
                    if i < len(self.component_def.pins):
                        logical_pin = self.component_def.pins[i]
                    else:
                        # Create a default pin
                        logical_pin = {
                            "name": f"Pin{phys_pin['number']}",
                            "type": "unused",
                            "direction": "input"
                        }
                
                # Create the pin point
                try:
                    pin_point = PinPoint(self, phys_pin, logical_pin, self.layer_mode)
                    pin_name = logical_pin["name"]
                    self.pin_points[pin_name] = pin_point
                except Exception as pin_error:
                    print(f"Error creating pin {phys_pin.get('number', 'unknown')}: {pin_error}")
                    # Continue with other pins
                    continue
            
            print(f"✅ Created {len(self.pin_points)} pins for {self.name} ({self.package_type})")
            
        except Exception as e:
            print(f"❌ Error creating pins for {self.name}: {e}")
            # Create a minimal fallback pin
            try:
                fallback_pin = {
                    "name": "Pin1",
                    "type": "unused", 
                    "direction": "input"
                }
                fallback_phys = {"number": 1, "x": 0, "y": 10, "side": "left"}
                pin_point = PinPoint(self, fallback_phys, fallback_pin, self.layer_mode)
                self.pin_points["Pin1"] = pin_point
                print(f"⚠️  Created fallback pin for {self.name}")
            except:
                print(f"❌ Could not create any pins for {self.name}")
                pass
    
    def _add_package_features(self):
        """Add package-specific visual features like notches, dots, etc."""
        if self.package_type.startswith("DIP"):
            # Add notch at pin 1 end for DIP packages (top center for vertical orientation)
            notch = QGraphicsEllipseItem(-5, -5, 10, 10, self)
            notch.setPos(self.package_info["width"] / 2, 5)  # Center horizontally, top vertically
            notch.setBrush(QBrush(Qt.GlobalColor.darkGray))
            notch.setPen(QPen(Qt.GlobalColor.black, 1))
        elif self.package_type.startswith("QFP") or self.package_type.startswith("PLCC"):
            # Add pin 1 indicator dot for surface mount packages
            dot = QGraphicsEllipseItem(-3, -3, 6, 6, self)
            dot.setPos(5, 5)  # Top-left corner
            dot.setBrush(QBrush(Qt.GlobalColor.white))
            dot.setPen(QPen(Qt.GlobalColor.black, 1))
    
    def paint(self, painter, option, widget):
        """Custom paint method with pin numbers support"""
        # Draw the basic package
        super().paint(painter, option, widget)
        
        if self.layer_mode == "chip":
            # Draw component label
            painter.setPen(QPen(Qt.GlobalColor.white))
            font = QFont("Arial", 8, QFont.Weight.Bold)
            painter.setFont(font)
            
            # Component name - adjust for DIP orientation
            if self.package_type.startswith("DIP"):
                # For vertical DIP packages, draw text normally (not rotated)
                text_rect = QRectF(5, 5, self.rect().width()-10, 20)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.name)
                
                # Package type at bottom
                text_rect = QRectF(5, self.rect().height()-20, self.rect().width()-10, 15)
                painter.setFont(QFont("Arial", 6))
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.package_type)
            else:
                # For other packages (QFP, etc.), use original layout
                text_rect = QRectF(5, 5, self.rect().width()-10, 15)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.name)
                
                # Package type
                text_rect = QRectF(5, self.rect().height()-15, self.rect().width()-10, 10)
                painter.setFont(QFont("Arial", 6))
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.package_type)
            
        elif self.layer_mode == "pcb":
            # Draw silkscreen text
            painter.setPen(QPen(Qt.GlobalColor.white))
            font = QFont("Arial", 7)
            painter.setFont(font)
            
            # Reference designator (e.g., U1, U2, etc.)
            ref_des = getattr(self, 'reference_designator', 'U?')
            painter.drawText(5, 12, ref_des)
    
    def set_layer_mode(self, mode):
        """Change the layer mode and update appearance"""
        self.layer_mode = mode
        self._set_appearance()
        
        # Update all pins
        for pin in self.pin_points.values():
            pin.layer_mode = mode
            pin._set_appearance()
        
        self.update()
    
    def itemChange(self, change, value):
        """Handle item changes"""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            # Update connections when component moves
            for pin in self.pin_points.values():
                for connection in pin.connections:
                    if hasattr(connection, 'update_position'):
                        connection.update_position()
        
        return super().itemChange(change, value)


class LayerManager:
    """Manages the three view layers: chip, pcb, and gerber"""
    
    def __init__(self):
        self.current_layer = "chip"
        self.components = []  # List of all components in the design
    
    def add_component(self, component):
        """Add a component to the layer manager"""
        if component not in self.components:
            self.components.append(component)
    
    def remove_component(self, component):
        """Remove a component from the layer manager"""
        if component in self.components:
            self.components.remove(component)
    
    def set_layer(self, layer_name):
        """Switch to a different layer view"""
        if layer_name in ["chip", "pcb", "gerber"]:
            self.current_layer = layer_name
            
            # Update all components to show the new layer
            for component in self.components:
                component.set_layer_mode(layer_name)
    
    def get_current_layer(self):
        """Get the current layer name"""
        return self.current_layer
    
    def get_layer_info(self):
        """Get information about all layers"""
        return {
            "chip": {
                "name": "Chip Placement",
                "description": "Component placement and logical connections",
                "color_scheme": "realistic"
            },
            "pcb": {
                "name": "PCB Layout", 
                "description": "Physical board layout with copper traces",
                "color_scheme": "pcb_green"
            },
            "gerber": {
                "name": "Gerber/Manufacturing",
                "description": "Manufacturing files and drill patterns",
                "color_scheme": "technical"
            }
        }


# Aliases for backwards compatibility
EnhancedHardwareComponent = HardwareComponent
EnhancedPinPoint = PinPoint

# Export
__all__ = ['ICPackage', 'PinPoint', 'HardwareComponent', 'LayerManager', 'EnhancedHardwareComponent', 'EnhancedPinPoint']
