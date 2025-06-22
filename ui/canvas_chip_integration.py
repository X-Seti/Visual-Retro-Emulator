#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Canvas Chip Integration
Integrates realistic chip graphics with the canvas system
"""

#this belongs in ui/canvas_chip_integration.py

import os
from pathlib import Path
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QBrush
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal

class ChipCanvasItem(QGraphicsPixmapItem):
    """
    Realistic chip item for canvas - shows proper chip images instead of rectangles
    """
    
    # Signals
    propertyChanged = pyqtSignal(str, object)
    selectionChanged = pyqtSignal(bool)
    
    def __init__(self, component_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        
        # Store component data
        self.component_data = component_data
        self.component_id = component_data.get('id', component_data.get('chip_id', 'unknown'))
        self.component_name = component_data.get('name', 'Unknown Chip')
        self.component_type = component_data.get('category', 'Unknown')
        self.package_type = component_data.get('package_type', 'DIP-40')
        self.pin_count = component_data.get('pin_count', 40)
        
        # Visual properties
        self.selected_color = QColor(0, 120, 215)
        self.hover_color = QColor(0, 120, 215, 100)
        
        # Load the chip image
        self._load_chip_image()
        
        # Make it interactive
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        
        print(f"✅ Created canvas chip item: {self.component_name}")
    
    def _load_chip_image(self):
        """Load the chip image from component data or generate fallback"""
        # Try to use the image from component data
        if self.component_data.get('has_image') and self.component_data.get('image'):
            pixmap = self.component_data['image']
            if pixmap and not pixmap.isNull():
                self.setPixmap(pixmap)
                return
        
        # Try to load from image files
        image_path = self._find_chip_image()
        if image_path and image_path.exists():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                # Scale to reasonable size
                scaled_pixmap = pixmap.scaled(120, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.setPixmap(scaled_pixmap)
                return
        
        # Generate fallback chip image
        self._generate_fallback_chip()
    
    def _find_chip_image(self) -> Optional[Path]:
        """Find chip image file"""
        image_dirs = [
            Path("images/components"),
            Path("images"),
            Path("../images/components"),
            Path("../images")
        ]
        
        # Create search patterns
        chip_name = self.component_name.lower().replace(' ', '_').replace('-', '_')
        package = self.package_type.lower().replace('-', '_')
        
        patterns = [
            f"{chip_name}_{package}.png",
            f"cpu_{chip_name}_dip_40.png" if "cpu" in self.component_type.lower() else None,
            f"c64_{chip_name}_dip_28.png" if "sid" in chip_name else None,
            f"c64_{chip_name}_dip_40.png" if "vic" in chip_name else None,
            f"amiga_{chip_name}_plcc_84.png" if "agnus" in chip_name else None,
            f"amiga_{chip_name}_dip_48.png" if "paula" in chip_name else None,
            f"{chip_name}.png"
        ]
        
        for image_dir in image_dirs:
            if not image_dir.exists():
                continue
            for pattern in patterns:
                if pattern:
                    image_path = image_dir / pattern
                    if image_path.exists():
                        return image_path
        
        return None
    
    def _generate_fallback_chip(self):
        """Generate a fallback chip image when no real image is found"""
        width, height = 120, 80
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Chip body rectangle
        body_rect = QRectF(10, 10, width-20, height-20)
        
        # Draw shadow
        shadow_rect = body_rect.translated(2, 2)
        painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(shadow_rect, 3, 3)
        
        # Choose body color based on package type
        if self.package_type.startswith("DIP"):
            body_color = QColor(240, 235, 220)  # Ceramic beige
        elif self.package_type.startswith("QFP"):
            body_color = QColor(45, 45, 45)     # Black plastic
        elif self.package_type.startswith("PLCC"):
            body_color = QColor(60, 60, 60)     # Dark plastic
        else:
            body_color = QColor(80, 60, 45)     # Brown plastic
        
        # Draw chip body
        painter.setBrush(QBrush(body_color))
        painter.setPen(QPen(body_color.darker(115), 1))
        painter.drawRoundedRect(body_rect, 3, 3)
        
        # Draw pin 1 notch for DIP packages
        if self.package_type.startswith("DIP"):
            notch_rect = QRectF(body_rect.left() + 5, body_rect.top() - 1, 10, 3)
            painter.setBrush(QBrush(body_color.darker(130)))
            painter.drawRoundedRect(notch_rect, 2, 2)
        
        # Draw pins
        self._draw_fallback_pins(painter, body_rect)
        
        # Draw text
        text_color = Qt.GlobalColor.white if body_color.lightness() < 128 else Qt.GlobalColor.black
        painter.setPen(QPen(text_color))
        
        # Component name
        font = QFont("Arial", 8, QFont.Weight.Bold)
        painter.setFont(font)
        name_rect = QRectF(body_rect.left() + 5, body_rect.top() + 8, body_rect.width() - 10, 16)
        
        # Truncate long names
        display_name = self.component_name
        if len(display_name) > 12:
            display_name = display_name[:10] + "..."
        
        painter.drawText(name_rect, Qt.AlignmentFlag.AlignCenter, display_name)
        
        # Package info
        font.setPointSize(6)
        painter.setFont(font)
        package_rect = QRectF(body_rect.left() + 5, body_rect.bottom() - 16, body_rect.width() - 10, 12)
        painter.drawText(package_rect, Qt.AlignmentFlag.AlignCenter, self.package_type)
        
        painter.end()
        self.setPixmap(pixmap)
        print(f"🎨 Generated fallback chip image for {self.component_name}")
    
    def _draw_fallback_pins(self, painter: QPainter, body_rect: QRectF):
        """Draw pins for fallback chip"""
        pin_color = QColor(192, 192, 192)  # Silver
        painter.setBrush(QBrush(pin_color))
        painter.setPen(QPen(pin_color.darker(130), 1))
        
        if self.package_type.startswith("DIP"):
            # DIP pins on left and right
            pins_per_side = self.pin_count // 2
            if pins_per_side > 1:
                pin_spacing = (body_rect.height() - 10) / (pins_per_side - 1)
                
                for i in range(pins_per_side):
                    y = body_rect.top() + 5 + i * pin_spacing
                    # Left side pins
                    painter.drawRect(int(body_rect.left() - 8), int(y - 1), 8, 2)
                    # Right side pins
                    painter.drawRect(int(body_rect.right()), int(y - 1), 8, 2)
        
        elif self.package_type.startswith("QFP"):
            # QFP pins on all sides
            pins_per_side = self.pin_count // 4
            if pins_per_side > 1:
                pin_spacing = (min(body_rect.width(), body_rect.height()) - 10) / (pins_per_side - 1)
                
                for i in range(pins_per_side):
                    offset = 5 + i * pin_spacing
                    # Top pins
                    painter.drawRect(int(body_rect.left() + offset - 1), int(body_rect.top() - 4), 2, 4)
                    # Bottom pins
                    painter.drawRect(int(body_rect.left() + offset - 1), int(body_rect.bottom()), 2, 4)
                    # Left pins
                    painter.drawRect(int(body_rect.left() - 4), int(body_rect.top() + offset - 1), 4, 2)
                    # Right pins
                    painter.drawRect(int(body_rect.right()), int(body_rect.top() + offset - 1), 4, 2)
    
    # === PROPERTY METHODS ===
    
    def set_package_type(self, package_type: str):
        """Change package type and regenerate"""
        if package_type != self.package_type:
            old_package = self.package_type
            self.package_type = package_type
            self.component_data['package_type'] = package_type
            
            # Update pin count if component data has package-specific info
            if 'package_types' in self.component_data:
                # Extract pin count from package type
                try:
                    self.pin_count = int(package_type.split('-')[1]) if '-' in package_type else self.pin_count
                    self.component_data['pin_count'] = self.pin_count
                except:
                    pass
            
            # Regenerate image
            self._load_chip_image()
            
            self.propertyChanged.emit("package", package_type)
            print(f"📦 Changed {self.component_name} package: {old_package} → {package_type}")
    
    def get_properties(self) -> Dict[str, Any]:
        """Get component properties for properties panel"""
        return {
            'name': {
                'value': self.component_name,
                'type': 'string',
                'label': 'Component Name'
            },
            'package': {
                'value': self.package_type,
                'type': 'choice',
                'choices': self.component_data.get('package_types', [self.package_type]),
                'label': 'Package Type'
            },
            'pins': {
                'value': self.pin_count,
                'type': 'int',
                'label': 'Pin Count'
            },
            'category': {
                'value': self.component_type,
                'type': 'string',
                'label': 'Category'
            },
            'x': {
                'value': self.pos().x(),
                'type': 'float',
                'label': 'X Position'
            },
            'y': {
                'value': self.pos().y(),
                'type': 'float',
                'label': 'Y Position'
            }
        }
    
    def set_property(self, prop_name: str, value: Any):
        """Set a property"""
        if prop_name == 'package':
            self.set_package_type(value)
        elif prop_name == 'name':
            self.component_name = value
            self.component_data['name'] = value
            self._load_chip_image()  # Regenerate with new name
        elif prop_name == 'x':
            pos = self.pos()
            self.setPos(value, pos.y())
        elif prop_name == 'y':
            pos = self.pos()
            self.setPos(pos.x(), value)
        
        self.propertyChanged.emit(prop_name, value)
    
    # === VISUAL METHODS ===
    
    def paint(self, painter, option, widget):
        """Custom paint method for selection effects"""
        # Draw the chip pixmap
        super().paint(painter, option, widget)
        
        # Draw selection outline
        if self.isSelected():
            painter.setPen(QPen(self.selected_color, 2))
            painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
            painter.drawRect(self.boundingRect().adjusted(1, 1, -1, -1))
    
    def itemChange(self, change, value):
        """Handle item changes"""
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            self.selectionChanged.emit(value)
        
        return super().itemChange(change, value)
    
    def hoverEnterEvent(self, event):
        """Handle hover enter"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        """Handle hover leave"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverLeaveEvent(event)


def create_chip_canvas_item(component_data: Dict[str, Any]) -> ChipCanvasItem:
    """Factory function to create chip canvas items"""
    return ChipCanvasItem(component_data)


# Canvas integration helpers
class CanvasChipIntegration:
    """Helper class for integrating chips with canvas"""
    
    @staticmethod
    def add_component_to_canvas(canvas, component_data: Dict[str, Any], position: QPointF = None):
        """Add a component to the canvas as a realistic chip"""
        # Create chip item
        chip_item = create_chip_canvas_item(component_data)
        
        # Set position
        if position:
            chip_item.setPos(position)
        else:
            # Default to center of canvas
            scene_rect = canvas.scene().sceneRect()
            chip_item.setPos(scene_rect.center())
        
        # Add to scene
        canvas.scene().addItem(chip_item)
        
        print(f"🎯 Added {component_data['name']} to canvas at {chip_item.pos()}")
        return chip_item
    
    @staticmethod
    def replace_rectangles_with_chips(canvas):
        """Replace any existing rectangular components with chip items"""
        scene = canvas.scene()
        items_to_replace = []
        
        # Find rectangular items that should be chips
        for item in scene.items():
            if (hasattr(item, 'component_data') and 
                not isinstance(item, ChipCanvasItem)):
                items_to_replace.append(item)
        
        # Replace them
        for item in items_to_replace:
            position = item.pos()
            component_data = getattr(item, 'component_data', {})
            
            # Remove old item
            scene.removeItem(item)
            
            # Add new chip item
            if component_data:
                CanvasChipIntegration.add_component_to_canvas(canvas, component_data, position)
        
        print(f"🔄 Replaced {len(items_to_replace)} rectangular components with chips")


# Export
__all__ = ['ChipCanvasItem', 'create_chip_canvas_item', 'CanvasChipIntegration']
