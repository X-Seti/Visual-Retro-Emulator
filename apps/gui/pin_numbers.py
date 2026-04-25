# X-Seti - June23 2025 - Pin Numbers Visibility System
# this belongs in ui/pin_numbers.py

from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QFont, QColor

class PinNumbersManager:
    """Manages pin number visibility across all components"""
    
    def __init__(self, canvas=None):
        self.canvas = canvas
        self.pin_numbers_visible = True
        self.pin_number_style = "outside"  # outside, inside, on_pin, tooltips
        self.pin_number_font = QFont("Arial", 6)
        self.pin_number_color = QColor(255, 255, 255)
        
        print("✓ Pin Numbers Manager initialized")
    
    def set_canvas(self, canvas):
        """Set the canvas reference"""
        self.canvas = canvas
        print("✓ Canvas set in Pin Numbers Manager")
    
    def set_pin_numbers_visible(self, visible):
        """Set pin numbers visibility on all components"""
        self.pin_numbers_visible = visible
        
        if not self.canvas:
            print("⚠️ No canvas set in Pin Numbers Manager")
            return
        
        # Handle different component storage patterns
        components = self._get_all_components()
        
        for component in components:
            self._update_component_pin_visibility(component, visible)
        
        # Update scene
        if hasattr(self.canvas, 'scene'):
            self.canvas.scene().update()
        
        if hasattr(self.canvas, 'update'):
            self.canvas.update()
        
        print(f"🔢 Pin numbers {'visible' if visible else 'hidden'}")
    
    def get_pin_numbers_visible(self):
        """Get current pin numbers visibility state"""
        return self.pin_numbers_visible
    
    def set_pin_number_style(self, style):
        """Set pin number display style"""
        valid_styles = ["outside", "inside", "on_pin", "tooltips"]
        if style in valid_styles:
            self.pin_number_style = style
            # Re-apply visibility to update style
            self.set_pin_numbers_visible(self.pin_numbers_visible)
            print(f"📌 Pin number style: {style}")
        else:
            print(f"⚠️ Invalid pin style: {style}")
    
    def set_pin_number_font(self, font):
        """Set pin number font"""
        self.pin_number_font = font
        self.set_pin_numbers_visible(self.pin_numbers_visible)  # Refresh
    
    def set_pin_number_color(self, color):
        """Set pin number color"""
        self.pin_number_color = color
        self.set_pin_numbers_visible(self.pin_numbers_visible)  # Refresh
    
    def _get_all_components(self):
        """Get all components from canvas regardless of storage method"""
        components = []
        
        if not self.canvas:
            return components
        
        # Try different storage patterns
        if hasattr(self.canvas, 'components'):
            canvas_components = self.canvas.components
            
            # List storage
            if isinstance(canvas_components, list):
                components.extend(canvas_components)
            
            # Dictionary storage
            elif isinstance(canvas_components, dict):
                components.extend(canvas_components.values())
        
        # Also check scene items directly
        if hasattr(self.canvas, 'scene'):
            scene_items = self.canvas.scene().items()
            for item in scene_items:
                if self._is_component(item) and item not in components:
                    components.append(item)
        
        return components
    
    def _is_component(self, item):
        """Check if an item is a component"""
        # Check for common component attributes
        return (hasattr(item, 'name') and 
                (hasattr(item, 'pins') or 
                 hasattr(item, 'pin_points') or
                 hasattr(item, 'package_type')))
    
    def _update_component_pin_visibility(self, component, visible):
        """Update pin number visibility for a single component"""
        try:
            # Method 1: Component has built-in pin number support
            if hasattr(component, 'set_pin_numbers_visible'):
                component.set_pin_numbers_visible(visible)
                return
            
            # Method 2: Component has pin_numbers_visible attribute
            if hasattr(component, 'pin_numbers_visible'):
                component.pin_numbers_visible = visible
                if hasattr(component, 'update'):
                    component.update()
                return
            
            # Method 3: Component has pin_points collection
            if hasattr(component, 'pin_points'):
                self._update_pin_points_visibility(component.pin_points, visible)
                return
            
            # Method 4: Add pin numbers if component supports it
            if self._can_add_pin_numbers(component):
                self._add_or_update_pin_numbers(component, visible)
        
        except Exception as e:
            print(f"⚠️ Error updating pin visibility for {getattr(component, 'name', 'unknown')}: {e}")
    
    def _update_pin_points_visibility(self, pin_points, visible):
        """Update visibility for pin point collections"""
        if isinstance(pin_points, list):
            for pin in pin_points:
                if hasattr(pin, 'set_pin_numbers_visible'):
                    pin.set_pin_numbers_visible(visible)
                elif hasattr(pin, 'pin_numbers_visible'):
                    pin.pin_numbers_visible = visible
                    if hasattr(pin, 'update'):
                        pin.update()
        
        elif isinstance(pin_points, dict):
            for pin in pin_points.values():
                if hasattr(pin, 'set_pin_numbers_visible'):
                    pin.set_pin_numbers_visible(visible)
                elif hasattr(pin, 'pin_numbers_visible'):
                    pin.pin_numbers_visible = visible
                    if hasattr(pin, 'update'):
                        pin.update()
    
    def _can_add_pin_numbers(self, component):
        """Check if we can add pin numbers to a component"""
        return (hasattr(component, 'pins') or 
                hasattr(component, 'package_type') or
                hasattr(component, 'boundingRect'))
    
    def _add_or_update_pin_numbers(self, component, visible):
        """Add or update pin numbers for components that don't have built-in support"""
        # This is a fallback method for components without built-in pin number support
        
        # Remove existing pin number text items
        if hasattr(component, '_pin_number_texts'):
            for text_item in component._pin_number_texts:
                if hasattr(text_item, 'scene') and text_item.scene():
                    text_item.scene().removeItem(text_item)
            component._pin_number_texts = []
        
        if not visible:
            return
        
        # Try to add pin numbers based on component type
        if hasattr(component, 'package_type'):
            self._add_pin_numbers_by_package(component)
        elif hasattr(component, 'pins'):
            self._add_pin_numbers_by_pins(component)
    
    def _add_pin_numbers_by_package(self, component):
        """Add pin numbers based on package type"""
        package_type = getattr(component, 'package_type', 'DIP-40')
        
        if not hasattr(component, '_pin_number_texts'):
            component._pin_number_texts = []
        
        # Simple pin numbering for DIP packages
        if package_type.startswith('DIP-'):
            try:
                pin_count = int(package_type.split('-')[1])
                self._add_dip_pin_numbers(component, pin_count)
            except (ValueError, IndexError):
                print(f"⚠️ Invalid package type: {package_type}")
        
        # QFP packages
        elif package_type.startswith('QFP-'):
            try:
                pin_count = int(package_type.split('-')[1])
                self._add_qfp_pin_numbers(component, pin_count)
            except (ValueError, IndexError):
                print(f"⚠️ Invalid package type: {package_type}")
    
    def _add_dip_pin_numbers(self, component, pin_count):
        """Add pin numbers for DIP packages"""
        if not hasattr(component, 'boundingRect'):
            return
        
        rect = component.boundingRect()
        pins_per_side = pin_count // 2
        
        if pins_per_side <= 1:
            return
        
        pin_spacing = (rect.height() - 20) / (pins_per_side - 1)
        
        # Left side pins (1 to pins_per_side)
        for i in range(pins_per_side):
            pin_num = i + 1
            y = 10 + i * pin_spacing
            self._add_pin_number_text(component, pin_num, QPointF(-25, y))
        
        # Right side pins (pins_per_side+1 to pin_count)
        for i in range(pins_per_side):
            pin_num = pins_per_side + i + 1
            y = 10 + i * pin_spacing
            self._add_pin_number_text(component, pin_num, QPointF(rect.width() + 15, y))
    
    def _add_qfp_pin_numbers(self, component, pin_count):
        """Add pin numbers for QFP packages"""
        if not hasattr(component, 'boundingRect'):
            return
        
        rect = component.boundingRect()
        pins_per_side = pin_count // 4
        
        if pins_per_side <= 1:
            return
        
        pin_spacing = (rect.width() - 20) / (pins_per_side - 1)
        
        # Top pins
        for i in range(pins_per_side):
            pin_num = i + 1
            x = 10 + i * pin_spacing
            self._add_pin_number_text(component, pin_num, QPointF(x, -15))
        
        # Right pins
        for i in range(pins_per_side):
            pin_num = pins_per_side + i + 1
            y = 10 + i * pin_spacing
            self._add_pin_number_text(component, pin_num, QPointF(rect.width() + 15, y))
        
        # Bottom pins
        for i in range(pins_per_side):
            pin_num = 2 * pins_per_side + i + 1
            x = 10 + (pins_per_side - 1 - i) * pin_spacing
            self._add_pin_number_text(component, pin_num, QPointF(x, rect.height() + 15))
        
        # Left pins
        for i in range(pins_per_side):
            pin_num = 3 * pins_per_side + i + 1
            y = 10 + (pins_per_side - 1 - i) * pin_spacing
            self._add_pin_number_text(component, pin_num, QPointF(-25, y))
    
    def _add_pin_numbers_by_pins(self, component):
        """Add pin numbers based on pins attribute"""
        if not hasattr(component, 'pins'):
            return
        
        pins = component.pins
        
        if isinstance(pins, list):
            for i, pin in enumerate(pins):
                pin_num = i + 1
                # Try to get pin position
                if hasattr(pin, 'x') and hasattr(pin, 'y'):
                    pos = QPointF(pin.x, pin.y - 10)
                else:
                    # Fallback position
                    pos = QPointF(10 + i * 20, -15)
                
                self._add_pin_number_text(component, pin_num, pos)
    
    def _add_pin_number_text(self, component, pin_number, position):
        """Add a pin number text item"""
        if not hasattr(component, 'scene') or not component.scene():
            return
        
        text_item = QGraphicsTextItem(str(pin_number), component)
        text_item.setFont(self.pin_number_font)
        text_item.setDefaultTextColor(self.pin_number_color)
        text_item.setPos(position)
        
        # Store reference for cleanup
        if not hasattr(component, '_pin_number_texts'):
            component._pin_number_texts = []
        component._pin_number_texts.append(text_item)
    
    def get_settings(self):
        """Get current pin number settings"""
        return {
            'visible': self.pin_numbers_visible,
            'style': self.pin_number_style,
            'font': self.pin_number_font.toString(),
            'color': self.pin_number_color.name()
        }
    
    def apply_settings(self, settings):
        """Apply pin number settings"""
        if 'visible' in settings:
            self.set_pin_numbers_visible(settings['visible'])
        
        if 'style' in settings:
            self.set_pin_number_style(settings['style'])
        
        if 'font' in settings:
            font = QFont()
            font.fromString(settings['font'])
            self.set_pin_number_font(font)
        
        if 'color' in settings:
            color = QColor(settings['color'])
            self.set_pin_number_color(color)


# Convenience functions for easy integration
def add_pin_numbers_to_canvas(canvas):
    """Add pin numbers manager to an existing canvas"""
    if not hasattr(canvas, 'pin_numbers_manager'):
        canvas.pin_numbers_manager = PinNumbersManager(canvas)
        
        # Add convenience method to canvas
        canvas.set_pin_numbers_visible = canvas.pin_numbers_manager.set_pin_numbers_visible
        canvas.get_pin_numbers_visible = canvas.pin_numbers_manager.get_pin_numbers_visible
        
        print("✓ Pin numbers support added to canvas")
    
    return canvas.pin_numbers_manager

def create_pin_numbers_manager(canvas=None):
    """Create a new pin numbers manager"""
    return PinNumbersManager(canvas)


# Export
__all__ = ['PinNumbersManager', 'add_pin_numbers_to_canvas', 'create_pin_numbers_manager']
