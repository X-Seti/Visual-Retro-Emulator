"""
May26, 2025 X-Seti - Realistic Chip Package Image Generator
Creates realistic chip package images with transparent backgrounds for better integration
"""

import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont, QPen, QBrush, QLinearGradient
from PyQt6.QtCore import Qt, QRectF, QPointF
import math


class ChipPackageRenderer:
    """Generates realistic chip package images for different IC types"""
    
    def __init__(self):
        self.chip_colors = {
            "ceramic": QColor(139, 119, 101),  # Ceramic brown
            "plastic": QColor(20, 20, 20),     # Black plastic
            "gold": QColor(255, 215, 0),       # Gold leads
            "silver": QColor(192, 192, 192),   # Silver leads
            "copper": QColor(184, 115, 51),    # Copper color
            "pcb_green": QColor(45, 80, 22),   # PCB green
            "white_text": QColor(255, 255, 255),
            "yellow_text": QColor(255, 255, 0)
        }
    
    def create_chip_image(self, component_def, package_type, image_size=400):
        """Create a realistic chip package image with transparent background"""
        # Create pixmap with transparency support
        pixmap = QPixmap(image_size, image_size)
        pixmap.fill(Qt.GlobalColor.transparent)  # ✅ TRANSPARENT BACKGROUND
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Determine chip style based on package type
        if package_type.startswith('QFP') or package_type.startswith('QFN'):
            self._draw_qfp_chip(painter, component_def, package_type, image_size)
        elif package_type.startswith('BGA'):
            self._draw_bga_chip(painter, component_def, package_type, image_size)
        elif package_type.startswith('DIP'):
            self._draw_dip_chip(painter, component_def, package_type, image_size)
        elif package_type.startswith('PLCC'):
            self._draw_plcc_chip(painter, component_def, package_type, image_size)
        else:
            # Default to QFP style
            self._draw_qfp_chip(painter, component_def, package_type, image_size)
        
        painter.end()
        return pixmap
    
    def _get_part_number(self, component_def, package_type):
        """Generate a realistic part number based on component type"""
        base_name = component_def.name.lower()
        
        if 'z80' in base_name:
            if package_type.startswith('QFP'):
                return "Z80CPU-QFP44"
            else:
                return "Z80CPU-DIP40"
        elif '8086' in base_name:
            if package_type.startswith('QFP'):
                return "i8086-2-QFP40"
            else:
                return "i8086-2-DIP40"
        elif '6502' in base_name:
            if package_type.startswith('QFP'):
                return "WDC65C02S-QFP40"
            else:
                return "WDC65C02S14P"
        elif '68000' in base_name:
            if package_type.startswith('QFP'):
                return "MC68000CFC16"
            elif package_type.startswith('PLCC'):
                return "MC68000FN16"
            else:
                return "MC68000P12"
        elif 'paula' in base_name:
            return "Paula 8364"
        elif 'denise' in base_name:
            return "Denise 8362"
        elif 'agnus' in base_name:
            return "Agnus 8370"
        elif 'gary' in base_name:
            return "Gary 8364"
        elif 'alice' in base_name:
            return "Alice 8374"
        elif 'lisa' in base_name:
            return "Lisa 8375"
        elif 'ramsey' in base_name:
            return "Ramsey 8372"
        else:
            return f"{component_def.component_id.upper()}"
    
    def _draw_dip_chip(self, painter, component_def, package_type, image_size):
        """Draw DIP package chip"""
        center_x = image_size // 2
        center_y = image_size // 2
        
        # DIP dimensions
        chip_width = int(image_size * 0.25)
        chip_height = int(image_size * 0.7)
        
        chip_rect = QRectF(center_x - chip_width//2, center_y - chip_height//2, 
                          chip_width, chip_height)
        
        # Draw chip body (black plastic)
        painter.setBrush(QBrush(self.chip_colors["plastic"]))
        painter.setPen(QPen(QColor(10, 10, 10), 2))
        painter.drawRoundedRect(chip_rect, 4, 4)
        
        # Draw notch at pin 1 end
        notch_rect = QRectF(center_x - 8, chip_rect.top() - 2, 16, 6)
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawEllipse(notch_rect)
        
        # Draw pins
        self._draw_dip_pins(painter, chip_rect, component_def, package_type)
        
        # Draw text
        painter.setPen(QPen(self.chip_colors["white_text"]))
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        # Rotate text for better DIP appearance
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(90)
        
        text_rect = QRectF(-chip_height//2, -20, chip_height, 40)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, 
                        f"{component_def.name}\n{self._get_part_number(component_def, package_type)}")
        
        painter.restore()
    
    def _draw_dip_pins(self, painter, chip_rect, component_def, package_type):
        """Draw DIP-style pins"""
        try:
            pin_count = int(package_type.split('-')[1])
        except:
            pin_count = 40
        
        pins_per_side = pin_count // 2
        pin_spacing = chip_rect.height() / (pins_per_side + 1)
        
        # Pin dimensions
        pin_width = 4
        pin_length = 15
        
        # Get pin names
        comp_pins = getattr(component_def, 'pins', [])
        pin_names = {}
        for i, pin in enumerate(comp_pins[:pin_count]):
            pin_names[i+1] = pin.get('name', f'P{i+1}')
        
        # Left side pins
        for i in range(pins_per_side):
            pin_num = i + 1
            y = chip_rect.top() + (i + 1) * pin_spacing
            
            # Pin
            pin_rect = QRectF(chip_rect.left() - pin_length, y - pin_width//2, 
                             pin_length, pin_width)
            painter.setBrush(QBrush(self.chip_colors["silver"]))
            painter.setPen(QPen(QColor(150, 150, 150), 1))
            painter.drawRect(pin_rect)
            
            # Label - Convert float coordinates to integers
            pin_name = pin_names.get(pin_num, str(pin_num))
            painter.setPen(QPen(self.chip_colors["white_text"]))
            painter.setFont(QFont("Arial", 6))
            painter.drawText(int(chip_rect.left() - pin_length - 25), int(y - 5), 20, 10, 
                           Qt.AlignmentFlag.AlignRight, pin_name)
        
        # Right side pins (numbered from bottom to top)
        for i in range(pins_per_side):
            pin_num = pin_count - i
            y = chip_rect.bottom() - (i + 1) * pin_spacing
            
            # Pin
            pin_rect = QRectF(chip_rect.right(), y - pin_width//2, 
                             pin_length, pin_width)
            painter.setBrush(QBrush(self.chip_colors["silver"]))
            painter.setPen(QPen(QColor(150, 150, 150), 1))
            painter.drawRect(pin_rect)
            
            # Label - Convert float coordinates to integers
            pin_name = pin_names.get(pin_num, str(pin_num))
            painter.setPen(QPen(self.chip_colors["white_text"]))
            painter.setFont(QFont("Arial", 6))
            painter.drawText(int(chip_rect.right() + pin_length + 5), int(y - 5), 20, 10, 
                           Qt.AlignmentFlag.AlignLeft, pin_name)
    
    def _draw_qfp_chip(self, painter, component_def, package_type, image_size):
        """Draw QFP/QFN style chip like the Z80 example"""
        center = image_size // 2
        chip_size = int(image_size * 0.6)
        chip_rect = QRectF(center - chip_size//2, center - chip_size//2, chip_size, chip_size)
        
        # Create gradient for chip body
        gradient = QLinearGradient(chip_rect.topLeft(), chip_rect.bottomRight())
        gradient.setColorAt(0, QColor(60, 45, 35))  # Dark brown
        gradient.setColorAt(0.3, QColor(139, 119, 101))  # Ceramic brown
        gradient.setColorAt(0.7, QColor(120, 100, 82))   # Medium brown
        gradient.setColorAt(1, QColor(80, 65, 50))       # Dark brown
        
        # Draw chip body
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(40, 30, 20), 2))
        painter.drawRoundedRect(chip_rect, 8, 8)
        
        # Draw beveled edges
        painter.setPen(QPen(QColor(180, 160, 140), 1))
        inner_rect = chip_rect.adjusted(4, 4, -4, -4)
        painter.drawRoundedRect(inner_rect, 6, 6)
        
        # Draw pins
        self._draw_qfp_pins(painter, chip_rect, component_def, package_type)
        
        # Draw chip text
        self._draw_chip_text(painter, chip_rect, component_def, package_type)
        
        # Draw pin 1 indicator
        pin1_x = chip_rect.left() + 15
        pin1_y = chip_rect.top() + 15
        painter.setBrush(QBrush(self.chip_colors["white_text"]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(pin1_x, pin1_y), 4, 4)
    
    def _draw_qfp_pins(self, painter, chip_rect, component_def, package_type):
        """Draw QFP-style pins with labels"""
        # Extract pin count from package type (e.g., QFP-44 -> 44)
        try:
            pin_count = int(package_type.split('-')[1])
        except:
            pin_count = 44  # Default
        
        pins_per_side = pin_count // 4
        
        # Pin dimensions
        pin_width = 3
        pin_length = 12
        
        # Get component pins if available
        comp_pins = getattr(component_def, 'pins', [])
        pin_names = {}
        for i, pin in enumerate(comp_pins):
            if i < pin_count:
                pin_names[i+1] = pin.get('name', f'P{i+1}')
        
        # Draw pins on each side
        sides = ['top', 'right', 'bottom', 'left']
        
        for side_idx, side in enumerate(sides):
            for pin_idx in range(pins_per_side):
                pin_num = side_idx * pins_per_side + pin_idx + 1
                
                if side == 'top':
                    x = chip_rect.left() + (pin_idx + 1) * (chip_rect.width() / (pins_per_side + 1))
                    y = chip_rect.top()
                    pin_rect = QRectF(x - pin_width//2, y - pin_length, pin_width, pin_length)
                    text_x, text_y = x, y - pin_length - 5
                    text_angle = -90
                    
                elif side == 'right':
                    x = chip_rect.right()
                    y = chip_rect.top() + (pin_idx + 1) * (chip_rect.height() / (pins_per_side + 1))
                    pin_rect = QRectF(x, y - pin_width//2, pin_length, pin_width)
                    text_x, text_y = x + pin_length + 15, y
                    text_angle = 0
                    
                elif side == 'bottom':
                    x = chip_rect.right() - (pin_idx + 1) * (chip_rect.width() / (pins_per_side + 1))
                    y = chip_rect.bottom()
                    pin_rect = QRectF(x - pin_width//2, y, pin_width, pin_length)
                    text_x, text_y = x, y + pin_length + 15
                    text_angle = 90
                    
                else:  # left
                    x = chip_rect.left()
                    y = chip_rect.bottom() - (pin_idx + 1) * (chip_rect.height() / (pins_per_side + 1))
                    pin_rect = QRectF(x - pin_length, y - pin_width//2, pin_length, pin_width)
                    text_x, text_y = x - pin_length - 25, y
                    text_angle = 0
                
                # Draw pin
                painter.setBrush(QBrush(self.chip_colors["silver"]))
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                painter.drawRect(pin_rect)
                
                # Draw pin label
                pin_name = pin_names.get(pin_num, f'{pin_num}')
                painter.setPen(QPen(self.chip_colors["white_text"]))
                painter.setFont(QFont("Arial", 7, QFont.Weight.Bold))
                
                painter.save()
                painter.translate(text_x, text_y)
                painter.rotate(text_angle)
                painter.drawText(-20, 0, 40, 10, Qt.AlignmentFlag.AlignCenter, pin_name)
                painter.restore()
    
    def _draw_chip_text(self, painter, chip_rect, component_def, package_type):
        """Draw text on the chip like manufacturer, part number, etc."""
        painter.setPen(QPen(self.chip_colors["white_text"]))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        text_rect = chip_rect.adjusted(15, 15, -15, -15)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, 
                        f"{component_def.name}\n{self._get_part_number(component_def, package_type)}")
    
    def _draw_bga_chip(self, painter, component_def, package_type, image_size):
        """Draw BGA package chip"""
        center = image_size // 2
        chip_size = int(image_size * 0.5)
        chip_rect = QRectF(center - chip_size//2, center - chip_size//2, chip_size, chip_size)
        
        # Draw substrate (green PCB-like)
        painter.setBrush(QBrush(self.chip_colors["pcb_green"]))
        painter.setPen(QPen(QColor(30, 50, 15), 2))
        painter.drawRect(chip_rect)
        
        # Draw ball grid
        try:
            pin_count = int(package_type.split('-')[1])
        except:
            pin_count = 144
        
        grid_size = int(math.sqrt(pin_count))
        ball_spacing = chip_size * 0.8 / (grid_size + 1)
        ball_radius = 2
        
        painter.setBrush(QBrush(self.chip_colors["silver"]))
        painter.setPen(Qt.PenStyle.NoPen)
        
        for row in range(grid_size):
            for col in range(grid_size):
                if row * grid_size + col < pin_count:
                    x = chip_rect.left() + chip_size * 0.1 + col * ball_spacing
                    y = chip_rect.top() + chip_size * 0.1 + row * ball_spacing
                    painter.drawEllipse(QPointF(x, y), ball_radius, ball_radius)
        
        # Draw text
        painter.setPen(QPen(self.chip_colors["white_text"]))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        text_rect = chip_rect.adjusted(10, 10, -10, -10)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, 
                        f"{component_def.name}\n{package_type}")
    
    def _draw_plcc_chip(self, painter, component_def, package_type, image_size):
        """Draw PLCC package chip"""
        center = image_size // 2
        chip_size = int(image_size * 0.6)
        chip_rect = QRectF(center - chip_size//2, center - chip_size//2, chip_size, chip_size)
        
        # Draw chip body (ceramic)
        painter.setBrush(QBrush(self.chip_colors["ceramic"]))
        painter.setPen(QPen(QColor(100, 80, 60), 2))
        painter.drawRoundedRect(chip_rect, 4, 4)
        
        # Draw J-leads (PLCC characteristic)
        self._draw_plcc_leads(painter, chip_rect, component_def, package_type)
        
        # Draw text
        painter.setPen(QPen(self.chip_colors["white_text"]))
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        text_rect = chip_rect.adjusted(15, 15, -15, -15)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, 
                        f"{component_def.name}\n{self._get_part_number(component_def, package_type)}")
    
    def _draw_plcc_leads(self, painter, chip_rect, component_def, package_type):
        """Draw PLCC J-leads"""
        try:
            pin_count = int(package_type.split('-')[1])
        except:
            pin_count = 68
        
        pins_per_side = pin_count // 4
        
        # J-lead dimensions
        lead_width = 2
        lead_length = 8
        
        painter.setBrush(QBrush(self.chip_colors["silver"]))
        painter.setPen(QPen(QColor(150, 150, 150), 1))
        
        # Draw leads on each side
        for side in range(4):
            for pin in range(pins_per_side):
                if side == 0:  # Top
                    x = chip_rect.left() + (pin + 1) * (chip_rect.width() / (pins_per_side + 1))
                    y = chip_rect.top()
                    # J-shaped lead - Convert float coordinates to integers
                    painter.drawRect(int(x - lead_width//2), int(y - lead_length), lead_width, lead_length)
                    painter.drawRect(int(x - lead_width//2 - 2), int(y - lead_length), 4, 2)
                    
                elif side == 1:  # Right
                    x = chip_rect.right()
                    y = chip_rect.top() + (pin + 1) * (chip_rect.height() / (pins_per_side + 1))
                    painter.drawRect(int(x), int(y - lead_width//2), lead_length, lead_width)
                    painter.drawRect(int(x + lead_length - 2), int(y - lead_width//2 - 2), 2, 4)
                    
                elif side == 2:  # Bottom
                    x = chip_rect.right() - (pin + 1) * (chip_rect.width() / (pins_per_side + 1))
                    y = chip_rect.bottom()
                    painter.drawRect(int(x - lead_width//2), int(y), lead_width, lead_length)
                    painter.drawRect(int(x - lead_width//2 - 2), int(y + lead_length - 2), 4, 2)
                    
                else:  # Left
                    x = chip_rect.left()
                    y = chip_rect.bottom() - (pin + 1) * (chip_rect.height() / (pins_per_side + 1))
                    painter.drawRect(int(x - lead_length), int(y - lead_width//2), lead_length, lead_width)
                    painter.drawRect(int(x - lead_length), int(y - lead_width//2 - 2), 2, 4)
