"""
Simple Chip Renderer - Fallback for when the realistic renderer fails
Creates basic chip representations without complex drawing
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont, QPen, QBrush
from PyQt6.QtCore import Qt, QRectF


class SimpleChipRenderer:
    """Simple chip renderer for fallback use"""
    
    def __init__(self):
        self.chip_colors = {
            "plastic": QColor(20, 20, 20),      # Black plastic
            "ceramic": QColor(139, 119, 101),   # Ceramic brown
            "gold": QColor(255, 215, 0),        # Gold leads
            "silver": QColor(192, 192, 192),    # Silver leads
            "white_text": QColor(255, 255, 255)
        }
    
    def create_chip_image(self, component_def, package_type, image_size=400):
        """Create a simple chip package image"""
        try:
            pixmap = QPixmap(image_size, image_size)
            pixmap.fill(QColor(30, 30, 30))  # Dark background
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Determine chip style and draw
            if package_type.startswith('DIP'):
                self._draw_simple_dip(painter, component_def, image_size)
            elif package_type.startswith('QFP'):
                self._draw_simple_qfp(painter, component_def, image_size)
            elif package_type.startswith('PLCC'):
                self._draw_simple_plcc(painter, component_def, image_size)
            else:
                self._draw_simple_generic(painter, component_def, image_size)
            
            painter.end()
            return pixmap
            
        except Exception as e:
            print(f"⚠️ Error in simple chip renderer: {e}")
            # Return a basic colored rectangle as ultimate fallback
            return self._create_fallback_pixmap(component_def, image_size)
    
    def _draw_simple_dip(self, painter, component_def, image_size):
        """Draw simple DIP package"""
        center = image_size // 2
        chip_width = int(image_size * 0.3)
        chip_height = int(image_size * 0.8)
        
        chip_rect = QRectF(center - chip_width//2, center - chip_height//2, 
                          chip_width, chip_height)
        
        # Draw chip body
        painter.setBrush(QBrush(self.chip_colors["plastic"]))
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawRoundedRect(chip_rect, 4, 4)
        
        # Draw notch
        notch_size = 8
        notch_rect = QRectF(center - notch_size//2, chip_rect.top() - 2, notch_size, 4)
        painter.setBrush(QBrush(QColor(60, 60, 60)))
        painter.drawEllipse(notch_rect)
        
        # Draw text
        painter.setPen(QPen(self.chip_colors["white_text"]))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        text = component_def.name if hasattr(component_def, 'name') else "CHIP"
        painter.drawText(chip_rect, Qt.AlignmentFlag.AlignCenter, text)
        
        # Draw simple pins
        self._draw_simple_dip_pins(painter, chip_rect)
    
    def _draw_simple_qfp(self, painter, component_def, image_size):
        """Draw simple QFP package"""
        center = image_size // 2
        chip_size = int(image_size * 0.6)
        chip_rect = QRectF(center - chip_size//2, center - chip_size//2, chip_size, chip_size)
        
        # Draw chip body
        painter.setBrush(QBrush(self.chip_colors["ceramic"]))
        painter.setPen(QPen(QColor(100, 80, 60), 2))
        painter.drawRoundedRect(chip_rect, 8, 8)
        
        # Draw text
        painter.setPen(QPen(self.chip_colors["white_text"]))
        painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        text = component_def.name if hasattr(component_def, 'name') else "CHIP"
        painter.drawText(chip_rect, Qt.AlignmentFlag.AlignCenter, text)
        
        # Draw simple pins on all sides
        self._draw_simple_qfp_pins(painter, chip_rect)
    
    def _draw_simple_plcc(self, painter, component_def, image_size):
        """Draw simple PLCC package"""