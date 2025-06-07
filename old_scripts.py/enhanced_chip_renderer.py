#!/usr/bin/env python3
"""
Enhanced Chip Renderer with Vertical Text
Updates the existing rendering.py to include vertical text like real ICs
"""

from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QFont, QTransform
from PyQt6.QtCore import Qt, QRectF


def create_realistic_chip_with_vertical_text(component_def, package_type, width, height):
    """Create chip image with realistic vertical text"""
    
    # Create pixmap
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Era-appropriate chip color (black plastic for 1980s/90s)
    year = getattr(component_def, 'year', '1985')
    if isinstance(year, str):
        try:
            year_int = int(year)
        except:
            year_int = 1985
    else:
        year_int = year
    
    if year_int < 1980:
        # Early era - brown ceramic
        chip_color = QColor(139, 118, 76)
        text_color = QColor(255, 248, 220)
    else:
        # Classic era - black plastic
        chip_color = QColor(45, 45, 45)
        text_color = QColor(255, 255, 255)
    
    # Draw chip body
    body_rect = QRectF(5, 5, width - 10, height - 10)
    painter.setBrush(QBrush(chip_color))
    painter.setPen(QPen(chip_color.lighter(120), 2))
    
    if package_type.startswith('QFP') or package_type.startswith('BGA'):
        painter.drawRect(body_rect)
    elif package_type.startswith('PLCC'):
        painter.drawRoundedRect(body_rect, 5, 5)
    else:
        # DIP packages with rounded corners
        painter.drawRoundedRect(body_rect, 8, 8)
    
    # Draw pin 1 indicator
    if package_type.startswith('DIP'):
        # Notch for DIP packages
        notch_width = min(40, width * 0.15)
        notch_rect = QRectF(width/2 - notch_width/2, 2, notch_width, 15)
        painter.setBrush(QBrush(chip_color.darker(150)))
        painter.drawEllipse(notch_rect)
    else:
        # Dot for other packages
        painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
        painter.drawEllipse(12, 12, 8, 8)
    
    # Add vertical text like real ICs
    painter.setPen(QPen(text_color))
    
    # Component name - large, bold, vertical
    name = getattr(component_def, 'name', 'Unknown')
    if len(name) > 16:
        name = name[:13] + "..."
    
    font_size = max(10, min(16, width // 35))
    font = QFont("Arial", font_size, QFont.Weight.Bold)
    painter.setFont(font)
    
    # Draw main component name vertically down the center-left
    painter.save()
    text_x = width * 0.25  # 25% from left edge
    text_y = height * 0.85  # Start near bottom
    painter.translate(text_x, text_y)
    painter.rotate(-90)  # Rotate for vertical text
    painter.drawText(0, 0, name)
    painter.restore()
    
    # Package type - smaller, vertical
    small_font = QFont("Arial", max(7, font_size - 3))
    painter.setFont(small_font)
    
    painter.save()
    text_x = width * 0.45  # 45% from left edge
    text_y = height * 0.75
    painter.translate(text_x, text_y)
    painter.rotate(-90)
    painter.drawText(0, 0, package_type)
    painter.restore()
    
    # Speed/frequency info if available
    speed = getattr(component_def, 'speed', None)
    if speed:
        painter.save()
        text_x = width * 0.65  # 65% from left edge  
        text_y = height * 0.7
        painter.translate(text_x, text_y)
        painter.rotate(-90)
        painter.drawText(0, 0, speed)
        painter.restore()
    
    # Manufacturer info if available and chip is wide enough
    if width > 400:
        manufacturer = getattr(component_def, 'manufacturer', None)
        if manufacturer:
            # Simplify manufacturer name
            if 'Motorola' in manufacturer:
                mfg_text = "MOTOROLA"
            elif 'Commodore' in manufacturer:
                mfg_text = "COMMODORE" 
            elif 'MOS' in manufacturer:
                mfg_text = "MOS"
            else:
                mfg_text = manufacturer[:8]
            
            tiny_font = QFont("Arial", max(6, font_size - 4))
            painter.setFont(tiny_font)
            
            painter.save()
            text_x = width * 0.8  # 80% from left edge
            text_y = height * 0.6
            painter.translate(text_x, text_y)
            painter.rotate(-90)
            painter.drawText(0, 0, mfg_text)
            painter.restore()
    
    painter.end()
    return pixmap


def patch_existing_renderer():
    """
    Instructions to patch your existing rendering.py file:
    
    1. Find the EnhancedHardwareComponent class
    2. Replace the text drawing section with vertical text code
    3. Update the paint() method to use create_realistic_chip_with_vertical_text()
    """
    
    patch_code = '''
# Add this to your EnhancedHardwareComponent class paint() method:

def paint(self, painter, option, widget):
    """Enhanced paint method with vertical text"""
    
    # Get component dimensions
    rect = self.boundingRect()
    width = rect.width()
    height = rect.height()
    
    # Create chip pixmap with vertical text
    pixmap = create_realistic_chip_with_vertical_text(
        self.component_def, 
        self.package_type, 
        int(width), 
        int(height)
    )
    
    # Draw the pixmap
    painter.drawPixmap(rect.toRect(), pixmap)
    
    # Draw pins with color coding
    self._draw_pins_with_colors(painter)
    
    # Draw selection highlight if selected
    if self.isSelected():
        painter.setPen(QPen(QColor(0, 120, 255), 3))
        painter.setBrush(QBrush())
        painter.drawRect(rect)

def _draw_pins_with_colors(self, painter):
    """Draw pins with proper color coding"""
    if not hasattr(self.component_def, 'pins'):
        return
        
    pin_size = 4
    
    for pin in self.component_def.pins:
        pin_type = pin.get('type', 'io')
        x = pin.get('x', 0)
        y = pin.get('y', 0)
        
        # Color code pins by type
        if pin_type == 'power':
            color = QColor(255, 100, 100)  # Red
        elif pin_type == 'ground':
            color = QColor(50, 50, 50)     # Black
        elif pin_type == 'clock':
            color = QColor(100, 255, 100)  # Green
        elif pin_type == 'address':
            color = QColor(255, 165, 0)    # Orange
        elif pin_type == 'data':
            color = QColor(100, 150, 255)  # Blue
        elif pin_type == 'control':
            color = QColor(200, 100, 255)  # Purple
        elif pin_type == 'video':
            color = QColor(255, 255, 100)  # Yellow
        elif pin_type == 'audio':
            color = QColor(175, 238, 238)  # Cyan
        else:
            color = QColor(180, 180, 180)  # Gray
        
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(color.darker(150), 1))
        painter.drawEllipse(x - pin_size/2, y - pin_size/2, pin_size, pin_size)
    '''
    
    return patch_code


def main():
    """Test the vertical text chip rendering"""
    from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
    
    app = QApplication([])
    
    # Create mock MC68000 component
    class MockComponent:
        def __init__(self):
            self.name = "MC68000P8"
            self.manufacturer = "Motorola"
            self.speed = "8MHz"
            self.year = "1985"
    
    component = MockComponent()
    
    # Create test images with different sizes
    test_chips = [
        ("MC68000 DIP-64", create_realistic_chip_with_vertical_text(component, "DIP-64", 750, 280)),
        ("Z80 DIP-40", create_realistic_chip_with_vertical_text(component, "DIP-40", 240, 260)),
        ("Agnus PLCC-84", create_realistic_chip_with_vertical_text(component, "PLCC-84", 360, 360))
    ]
    
    # Display all test chips
    window = QWidget()
    layout = QVBoxLayout()
    
    for name, pixmap in test_chips:
        label = QLabel(name)
        layout.addWidget(label)
        
        chip_label = QLabel()
        chip_label.setPixmap(pixmap)
        layout.addWidget(chip_label)
    
    window.setLayout(layout)
    window.setWindowTitle("Chips with Vertical Text")
    window.show()
    
    print("✅ Created test chips with vertical text")
    print("📏 MC68000: 750x280 pixels (much wider!)")
    print("🔄 Text: Vertical orientation like real ICs")
    print("🎨 Colors: Era-appropriate chip styling")
    
    app.exec()


if __name__ == "__main__":
    main()
