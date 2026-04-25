#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Chip Renderer
Professional chip rendering with notches, proper text, and realistic appearance
"""
#this belongs in ui/ chip_renderer.py

from typing import Tuple, Optional, Dict, Any
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPixmap, QPolygonF
from PyQt6.QtCore import QRectF, QPointF, Qt
from PyQt6.QtWidgets import QGraphicsPixmapItem

class ChipRenderer:
    """Professional chip renderer with realistic appearance"""
    
    def __init__(self):
        self.chip_colors = {
            # Chip body colors
            "ceramic_beige": QColor(240, 235, 220),    # Classic ceramic DIP
            "ceramic_white": QColor(250, 248, 245),    # White ceramic
            "plastic_black": QColor(45, 45, 45),       # Black plastic
            "plastic_brown": QColor(80, 60, 45),       # Brown plastic (vintage)
            "pcb_green": QColor(45, 80, 22),           # PCB substrate
            
            # Metal colors
            "gold_pins": QColor(255, 215, 0),          # Gold plated pins
            "tin_pins": QColor(192, 192, 192),         # Tin/silver pins
            "copper_traces": QColor(184, 115, 51),     # Copper color
            
            # Text colors
            "white_text": QColor(255, 255, 255),       # White text
            "black_text": QColor(0, 0, 0),             # Black text
            "laser_etch": QColor(200, 200, 200),       # Laser etched text
            
            # Details
            "notch_highlight": QColor(220, 220, 220),   # Pin 1 notch
            "pin1_dot": QColor(255, 0, 0),              # Red pin 1 dot
            "shadow": QColor(0, 0, 0, 50),              # Subtle shadow
        }
        
        # Package definitions
        self.package_specs = {
            "DIP": {"pins_per_side": True, "pin_spacing": 2.54, "body_width": 15.24},
            "SOIC": {"pins_per_side": True, "pin_spacing": 1.27, "body_width": 7.5},
            "QFP": {"pins_per_side": False, "pin_spacing": 0.8, "body_width": 14},
            "PLCC": {"pins_per_side": False, "pin_spacing": 1.27, "body_width": 20},
            "BGA": {"pins_per_side": False, "pin_spacing": 1.0, "body_width": 15},
        }
    
    def render_chip(self, 
                   chip_name: str, 
                   package_type: str = "DIP", 
                   pin_count: int = 40,
                   size: Tuple[int, int] = (100, 60),
                   vintage_style: bool = True) -> QPixmap:
        """
        Render a professional chip with notch and proper text
        
        Args:
            chip_name: Name to display on chip (e.g., "Z80", "6502")
            package_type: Package type (DIP, SOIC, QFP, PLCC, BGA)
            pin_count: Number of pins
            size: Chip size in pixels (width, height)
            vintage_style: Use vintage colors and styling
        
        Returns:
            QPixmap with rendered chip
        """
        
        pixmap = QPixmap(size[0], size[1])
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # Calculate chip body rectangle (leave space for pins)
        pin_overhang = 8 if package_type == "DIP" else 4
        body_rect = QRectF(
            pin_overhang, 
            pin_overhang, 
            size[0] - 2 * pin_overhang, 
            size[1] - 2 * pin_overhang
        )
        
        # Draw shadow first
        self._draw_shadow(painter, body_rect)
        
        # Draw chip body
        self._draw_chip_body(painter, body_rect, package_type, vintage_style)
        
        # Draw notch (pin 1 indicator)
        self._draw_notch(painter, body_rect, package_type)
        
        # Draw pins
        self._draw_pins(painter, body_rect, package_type, pin_count, vintage_style)
        
        # Draw text
        self._draw_chip_text(painter, body_rect, chip_name, package_type, pin_count, vintage_style)
        
        # Draw additional details
        self._draw_details(painter, body_rect, package_type, vintage_style)
        
        painter.end()
        return pixmap
    
    def _draw_shadow(self, painter: QPainter, body_rect: QRectF):
        """Draw subtle shadow for depth"""
        shadow_offset = 2
        shadow_rect = body_rect.translated(shadow_offset, shadow_offset)
        
        painter.setBrush(QBrush(self.chip_colors["shadow"]))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.drawRoundedRect(shadow_rect, 3, 3)
    
    def _draw_chip_body(self, painter: QPainter, body_rect: QRectF, package_type: str, vintage_style: bool):
        """Draw the main chip body"""
        
        # Select body color based on package and style
        if package_type in ["DIP", "PDIP"]:
            body_color = self.chip_colors["ceramic_brown"] if vintage_style else self.chip_colors["ceramic_beige"]
            edge_color = body_color.darker(115)
        elif package_type in ["SOIC", "SSOP"]:
            body_color = self.chip_colors["plastic_black"]
            edge_color = QColor(60, 60, 60)
        elif package_type in ["QFP", "TQFP", "LQFP"]:
            body_color = self.chip_colors["plastic_black"]
            edge_color = QColor(60, 60, 60)
        elif package_type == "PLCC":
            body_color = self.chip_colors["ceramic_white"]
            edge_color = body_color.darker(110)
        else:
            body_color = self.chip_colors["pcb_green"]
            edge_color = body_color.darker(120)
        
        # Draw main body
        painter.setBrush(QBrush(body_color))
        painter.setPen(QPen(edge_color, 1.5))
        
        if package_type == "PLCC":
            # Square with cut corners for PLCC
            self._draw_plcc_body(painter, body_rect)
        else:
            # Standard rounded rectangle
            corner_radius = 4 if package_type == "DIP" else 2
            painter.drawRoundedRect(body_rect, corner_radius, corner_radius)
        
        # Add subtle gradient for 3D effect
        self._add_body_gradient(painter, body_rect, body_color)
    
    def _draw_plcc_body(self, painter: QPainter, body_rect: QRectF):
        """Draw PLCC package body with cut corners"""
        cut_size = min(8, body_rect.width() * 0.1)
        
        # Create polygon with cut corners
        polygon = QPolygonF()
        
        # Top edge with cuts
        polygon << QPointF(body_rect.left() + cut_size, body_rect.top())
        polygon << QPointF(body_rect.right() - cut_size, body_rect.top())
        
        # Right edge with cuts
        polygon << QPointF(body_rect.right(), body_rect.top() + cut_size)
        polygon << QPointF(body_rect.right(), body_rect.bottom() - cut_size)
        
        # Bottom edge with cuts
        polygon << QPointF(body_rect.right() - cut_size, body_rect.bottom())
        polygon << QPointF(body_rect.left() + cut_size, body_rect.bottom())
        
        # Left edge with cuts
        polygon << QPointF(body_rect.left(), body_rect.bottom() - cut_size)
        polygon << QPointF(body_rect.left(), body_rect.top() + cut_size)
        
        painter.drawPolygon(polygon)
    
    def _add_body_gradient(self, painter: QPainter, body_rect: QRectF, base_color: QColor):
        """Add subtle gradient for 3D effect"""
        # Top highlight
        highlight_color = base_color.lighter(120)
        highlight_color.setAlpha(100)
        
        painter.setBrush(QBrush(highlight_color))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        
        highlight_rect = QRectF(
            body_rect.left() + 2,
            body_rect.top() + 2,
            body_rect.width() - 4,
            body_rect.height() * 0.3
        )
        painter.drawRoundedRect(highlight_rect, 2, 2)
    
    def _draw_notch(self, painter: QPainter, body_rect: QRectF, package_type: str):
        """Draw pin 1 indicator notch"""
        
        if package_type in ["DIP", "PDIP", "SOIC", "SSOP"]:
            # Semicircular notch on top edge
            notch_width = min(12, body_rect.width() * 0.25)
            notch_center_x = body_rect.left() + body_rect.width() * 0.2
            
            # Draw notch cutout
            painter.setBrush(QBrush(self.chip_colors["notch_highlight"]))
            painter.setPen(QPen(QColor(180, 180, 180), 1))
            
            notch_rect = QRectF(
                notch_center_x - notch_width/2,
                body_rect.top() - 2,
                notch_width,
                6
            )
            painter.drawEllipse(notch_rect)
            
        elif package_type in ["QFP", "TQFP", "LQFP", "PLCC"]:
            # Pin 1 dot for surface mount packages
            dot_size = 3
            dot_center_x = body_rect.left() + 8
            dot_center_y = body_rect.top() + 8
            
            painter.setBrush(QBrush(self.chip_colors["pin1_dot"]))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            
            dot_rect = QRectF(
                dot_center_x - dot_size/2,
                dot_center_y - dot_size/2,
                dot_size, dot_size
            )
            painter.drawEllipse(dot_rect)
        
        elif package_type == "BGA":
            # Corner mark for BGA
            mark_size = 6
            painter.setBrush(QBrush(self.chip_colors["pin1_dot"]))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            
            # Small triangle in corner
            triangle = QPolygonF()
            triangle << QPointF(body_rect.left() + 3, body_rect.top() + 3)
            triangle << QPointF(body_rect.left() + 3 + mark_size, body_rect.top() + 3)
            triangle << QPointF(body_rect.left() + 3, body_rect.top() + 3 + mark_size)
            painter.drawPolygon(triangle)
    
    def _draw_pins(self, painter: QPainter, body_rect: QRectF, package_type: str, pin_count: int, vintage_style: bool):
        """Draw chip pins based on package type"""
        
        if package_type in ["DIP", "PDIP"]:
            self._draw_dip_pins(painter, body_rect, pin_count, vintage_style)
        elif package_type in ["SOIC", "SSOP"]:
            self._draw_soic_pins(painter, body_rect, pin_count, vintage_style)
        elif package_type in ["QFP", "TQFP", "LQFP"]:
            self._draw_qfp_pins(painter, body_rect, pin_count, vintage_style)
        elif package_type == "PLCC":
            self._draw_plcc_pins(painter, body_rect, pin_count, vintage_style)
        elif package_type == "BGA":
            self._draw_bga_pins(painter, body_rect, pin_count, vintage_style)
    
    def _draw_dip_pins(self, painter: QPainter, body_rect: QRectF, pin_count: int, vintage_style: bool):
        """Draw DIP package pins"""
        pins_per_side = pin_count // 2
        pin_width = 2
        pin_length = 8
        
        # Pin color
        pin_color = self.chip_colors["tin_pins"] if vintage_style else self.chip_colors["gold_pins"]
        painter.setBrush(QBrush(pin_color))
        painter.setPen(QPen(pin_color.darker(120), 0.5))
        
        if pins_per_side > 0:
            pin_spacing = (body_rect.height() - 12) / (pins_per_side - 1) if pins_per_side > 1 else 0
            start_y = body_rect.top() + 6
            
            # Left side pins
            for i in range(pins_per_side):
                pin_y = start_y + i * pin_spacing
                pin_rect = QRectF(
                    body_rect.left() - pin_length,
                    pin_y - pin_width/2,
                    pin_length + 2,  # Overlap with body slightly
                    pin_width
                )
                painter.drawRect(pin_rect)
            
            # Right side pins (numbered from bottom to top)
            for i in range(pins_per_side):
                pin_y = body_rect.bottom() - 6 - i * pin_spacing
                pin_rect = QRectF(
                    body_rect.right() - 2,  # Overlap with body slightly
                    pin_y - pin_width/2,
                    pin_length + 2,
                    pin_width
                )
                painter.drawRect(pin_rect)
    
    def _draw_soic_pins(self, painter: QPainter, body_rect: QRectF, pin_count: int, vintage_style: bool):
        """Draw SOIC package pins (gull-wing)"""
        pins_per_side = pin_count // 2
        pin_width = 1.5
        pin_length = 6
        
        pin_color = self.chip_colors["tin_pins"]
        painter.setBrush(QBrush(pin_color))
        painter.setPen(QPen(pin_color.darker(120), 0.5))
        
        if pins_per_side > 0:
            pin_spacing = (body_rect.height() - 8) / (pins_per_side - 1) if pins_per_side > 1 else 0
            start_y = body_rect.top() + 4
            
            # Left side pins
            for i in range(pins_per_side):
                pin_y = start_y + i * pin_spacing
                # Draw gull-wing shape
                self._draw_gull_wing_pin(painter, 
                    QPointF(body_rect.left() - pin_length, pin_y),
                    QPointF(body_rect.left(), pin_y),
                    pin_width, "left")
            
            # Right side pins
            for i in range(pins_per_side):
                pin_y = body_rect.bottom() - 4 - i * pin_spacing
                self._draw_gull_wing_pin(painter,
                    QPointF(body_rect.right(), pin_y),
                    QPointF(body_rect.right() + pin_length, pin_y),
                    pin_width, "right")
    
    def _draw_qfp_pins(self, painter: QPainter, body_rect: QRectF, pin_count: int, vintage_style: bool):
        """Draw QFP package pins (four sides)"""
        pins_per_side = pin_count // 4
        pin_width = 1.0
        pin_length = 4
        
        pin_color = self.chip_colors["tin_pins"]
        painter.setBrush(QBrush(pin_color))
        painter.setPen(QPen(pin_color.darker(120), 0.5))
        
        if pins_per_side > 0:
            # Top side
            pin_spacing = (body_rect.width() - 8) / (pins_per_side - 1) if pins_per_side > 1 else 0
            start_x = body_rect.left() + 4
            
            for i in range(pins_per_side):
                pin_x = start_x + i * pin_spacing
                self._draw_gull_wing_pin(painter,
                    QPointF(pin_x, body_rect.top() - pin_length),
                    QPointF(pin_x, body_rect.top()),
                    pin_width, "up")
            
            # Repeat for other sides...
            # (Similar logic for right, bottom, left sides)
    
    def _draw_plcc_pins(self, painter: QPainter, body_rect: QRectF, pin_count: int, vintage_style: bool):
        """Draw PLCC package J-lead pins"""
        # J-leads are drawn as small rectangles around the perimeter
        pin_color = self.chip_colors["tin_pins"]
        painter.setBrush(QBrush(pin_color))
        painter.setPen(QPen(pin_color.darker(120), 0.5))
        
        # Simplified J-lead representation
        pins_per_side = pin_count // 4
        pin_size = 1.5
        
        # Draw pins around perimeter (simplified)
        for side in range(4):
            for i in range(pins_per_side):
                # Calculate pin position based on side
                # (Implementation details for each side)
                pass
    
    def _draw_bga_pins(self, painter: QPainter, body_rect: QRectF, pin_count: int, vintage_style: bool):
        """Draw BGA package (ball grid array)"""
        # BGA packages have balls on the bottom - show as grid pattern
        ball_color = self.chip_colors["tin_pins"]
        painter.setBrush(QBrush(ball_color))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        
        # Estimate grid size
        grid_size = int((pin_count ** 0.5) + 0.5)
        ball_spacing = min(body_rect.width(), body_rect.height()) / (grid_size + 1)
        ball_radius = ball_spacing * 0.3
        
        start_x = body_rect.left() + ball_spacing
        start_y = body_rect.top() + ball_spacing
        
        # Draw ball grid (visible ones on edges)
        for row in range(grid_size):
            for col in range(grid_size):
                # Only draw edge balls for visibility
                if row == 0 or row == grid_size-1 or col == 0 or col == grid_size-1:
                    ball_x = start_x + col * ball_spacing
                    ball_y = start_y + row * ball_spacing
                    
                    ball_rect = QRectF(
                        ball_x - ball_radius,
                        ball_y - ball_radius,
                        ball_radius * 2,
                        ball_radius * 2
                    )
                    painter.drawEllipse(ball_rect)
    
    def _draw_gull_wing_pin(self, painter: QPainter, start: QPointF, end: QPointF, width: float, direction: str):
        """Draw gull-wing style pin"""
        # Simplified gull-wing as rectangle for now
        if direction in ["left", "right"]:
            pin_rect = QRectF(
                min(start.x(), end.x()),
                start.y() - width/2,
                abs(end.x() - start.x()),
                width
            )
        else:  # up, down
            pin_rect = QRectF(
                start.x() - width/2,
                min(start.y(), end.y()),
                width,
                abs(end.y() - start.y())
            )
        
        painter.drawRect(pin_rect)
    
    def _draw_chip_text(self, painter: QPainter, body_rect: QRectF, chip_name: str, 
                       package_type: str, pin_count: int, vintage_style: bool):
        """Draw chip text with proper formatting"""
        
        # Determine text color
        if package_type in ["DIP", "PDIP", "PLCC"]:
            text_color = self.chip_colors["black_text"]
        else:
            text_color = self.chip_colors["white_text"]
        
        painter.setPen(QPen(text_color))
        
        # Calculate font sizes
        base_font_size = max(6, min(14, int(body_rect.width() / 7)))
        
        # Main chip name (centered, larger)
        main_font = QFont("Arial", base_font_size, QFont.Weight.Bold)
        painter.setFont(main_font)
        
        # Clean chip name
        display_name = self._format_chip_name(chip_name)
        
        # Main text area (upper portion)
        name_rect = QRectF(
            body_rect.left() + 4,
            body_rect.top() + 4,
            body_rect.width() - 8,
            body_rect.height() * 0.5
        )
        painter.drawText(name_rect, Qt.AlignmentFlag.AlignCenter, display_name)
        
        # Package info (lower portion, smaller)
        small_font = QFont("Arial", max(4, base_font_size - 3))
        painter.setFont(small_font)
        
        # Format package string
        package_info = f"{package_type}-{pin_count}"
        
        info_rect = QRectF(
            body_rect.left() + 4,
            body_rect.top() + body_rect.height() * 0.6,
            body_rect.width() - 8,
            body_rect.height() * 0.25
        )
        painter.drawText(info_rect, Qt.AlignmentFlag.AlignCenter, package_info)
        
        # Add manufacturer code or date code if space allows
        if body_rect.height() > 40:
            tiny_font = QFont("Arial", max(3, base_font_size - 4))
            painter.setFont(tiny_font)
            
            # Simple date code (vintage style)
            date_code = "8142" if vintage_style else "2547"
            
            date_rect = QRectF(
                body_rect.left() + 4,
                body_rect.bottom() - 12,
                body_rect.width() - 8,
                8
            )
            painter.drawText(date_rect, Qt.AlignmentFlag.AlignCenter, date_code)
    
    def _format_chip_name(self, chip_name: str) -> str:
        """Format chip name for display"""
        # Clean and format the chip name
        name = chip_name.upper().strip()
        
        # Handle common prefixes
        if name.startswith("CPU_"):
            name = name[4:]
        elif name.startswith("PROC_"):
            name = name[5:]
        
        # Limit length
        if len(name) > 12:
            name = name[:12]
        
        # Add common formatting
        if name in ["Z80", "Z80A", "Z80B"]:
            return name
        elif name.startswith("6502"):
            return "MOS\n" + name
        elif name.startswith("68"):
            return "MC" + name
        elif name.startswith("8"):
            return "INTEL\n" + name
        
        return name
    
    def _draw_details(self, painter: QPainter, body_rect: QRectF, package_type: str, vintage_style: bool):
        """Draw additional realistic details"""
        
        # Add subtle line details for realism
        detail_color = QColor(200, 200, 200, 100)
        painter.setPen(QPen(detail_color, 0.5))
        
        if package_type in ["DIP", "PDIP"]:
            # Draw center seam line
            center_y = body_rect.center().y()
            painter.drawLine(
                QPointF(body_rect.left() + 4, center_y),
                QPointF(body_rect.right() - 4, center_y)
            )
        
        # Add corner highlights for 3D effect
        highlight_color = QColor(255, 255, 255, 80)
        painter.setPen(QPen(highlight_color, 1))
        
        # Top-left highlight
        painter.drawLine(
            QPointF(body_rect.left() + 2, body_rect.top() + 1),
            QPointF(body_rect.left() + 8, body_rect.top() + 1)
        )
        painter.drawLine(
            QPointF(body_rect.left() + 1, body_rect.top() + 2),
            QPointF(body_rect.left() + 1, body_rect.top() + 8)
        )

# === INTEGRATION WITH CANVAS ===

class ChipGraphicsItem(QGraphicsPixmapItem):
    """chip graphics item for canvas integration"""
    
    def __init__(self, chip_name: str, package_type: str = "DIP", pin_count: int = 40):
        super().__init__()
        
        self.chip_name = chip_name
        self.package_type = package_type
        self.pin_count = pin_count
        self.component_type = "processor"  # Default type
        self.component_id = id(self)
        
        # Create renderer and generate pixmap
        self.renderer = ChipRenderer()
        self._update_pixmap()
        
        # Make interactive
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
    
    def _update_pixmap(self, size: Tuple[int, int] = (100, 60)):
        """Update the chip pixmap"""
        pixmap = self.renderer.render_chip(
            self.chip_name,
            self.package_type,
            self.pin_count,
            size,
            vintage_style=True
        )
        self.setPixmap(pixmap)
    
    def set_chip_info(self, chip_name: str, package_type: str = None, pin_count: int = None):
        """Update chip information and re-render"""
        self.chip_name = chip_name
        if package_type:
            self.package_type = package_type
        if pin_count:
            self.pin_count = pin_count
        
        self._update_pixmap()
    
    def get_chip_info(self) -> Dict[str, Any]:
        """Get chip information"""
        return {
            "name": self.chip_name,
            "package": self.package_type,
            "pins": self.pin_count,
            "type": self.component_type
        }

# === FACTORY FUNCTIONS ===

def create_chip_component(chip_name: str, package_type: str = "DIP", pin_count: int = 40) -> ChipGraphicsItem:
    """Factory function to create chip components"""
    return ChipGraphicsItem(chip_name, package_type, pin_count)

def render_chip_preview(chip_name: str, package_type: str = "DIP", pin_count: int = 40, 
                       size: Tuple[int, int] = (80, 50)) -> QPixmap:
    """Generate chip preview pixmap"""
    renderer = ChipRenderer()
    return renderer.render_chip(chip_name, package_type, pin_count, size)

# === COMMON CHIP DEFINITIONS ===

COMMON_CHIPS = {
    "Z80": {"package": "DIP", "pins": 40, "type": "processor"},
    "Z80A": {"package": "DIP", "pins": 40, "type": "processor"},
    "6502": {"package": "DIP", "pins": 40, "type": "processor"},
    "6510": {"package": "DIP", "pins": 40, "type": "processor"},
    "68000": {"package": "DIP", "pins": 64, "type": "processor"},
    "8080": {"package": "DIP", "pins": 40, "type": "processor"},
    "8086": {"package": "DIP", "pins": 40, "type": "processor"},
    "SID": {"package": "DIP", "pins": 28, "type": "sound"},
    "VIC-II": {"package": "DIP", "pins": 40, "type": "graphics"},
    "PLA": {"package": "DIP", "pins": 28, "type": "logic"},
    "CIA": {"package": "DIP", "pins": 40, "type": "io"},
}

def create_common_chip(chip_name: str) -> Optional[ChipGraphicsItem]:
    """Create a common chip with predefined specifications"""
    if chip_name.upper() in COMMON_CHIPS:
        spec = COMMON_CHIPS[chip_name.upper()]
        chip = ChipGraphicsItem(
            chip_name.upper(),
            spec["package"],
            spec["pins"]
        )
        chip.component_type = spec["type"]
        return chip
    return None

# Export
__all__ = [
    'ChipRenderer', 
    'ChipGraphicsItem',
    'create_chip_component', 
    'render_chip_preview',
    'create_common_chip',
    'COMMON_CHIPS'
]
