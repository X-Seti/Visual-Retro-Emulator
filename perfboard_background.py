#!/usr/bin/env python3
"""
Perfboard Background Generator for Chip Editor
Creates authentic PCB perfboard pattern with proper pin alignment
"""

from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter
from PyQt6.QtWidgets import QGraphicsScene

class PerfboardBackground:
    """Generates realistic perfboard background pattern"""
    
    def __init__(self):
        self.hole_spacing = 10  # 2.54mm scaled to pixels
        self.hole_radius = 1.5
        self.board_color = QColor(34, 139, 34)  # PCB green
        self.hole_color = QColor(20, 20, 20)   # Dark holes
        self.pad_color = QColor(184, 115, 51)  # Copper pads
        
    def draw_perfboard(self, painter, rect):
        """Draw perfboard pattern on given rectangle"""
        # Fill background with PCB green
        painter.fillRect(rect, self.board_color)
        
        # Calculate grid bounds
        start_x = int(rect.left() // self.hole_spacing) * self.hole_spacing
        start_y = int(rect.top() // self.hole_spacing) * self.hole_spacing
        end_x = rect.right() + self.hole_spacing
        end_y = rect.bottom() + self.hole_spacing
        
        # Draw copper pads and holes
        for x in range(int(start_x), int(end_x), self.hole_spacing):
            for y in range(int(start_y), int(end_y), self.hole_spacing):
                # Copper pad (slightly larger than hole)
                painter.setBrush(QBrush(self.pad_color))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    x - self.hole_radius - 1, 
                    y - self.hole_radius - 1,
                    (self.hole_radius + 1) * 2, 
                    (self.hole_radius + 1) * 2
                )
                
                # Drill hole
                painter.setBrush(QBrush(self.hole_color))
                painter.drawEllipse(
                    x - self.hole_radius, 
                    y - self.hole_radius,
                    self.hole_radius * 2, 
                    self.hole_radius * 2
                )

class PerfboardScene(QGraphicsScene):
    """Scene with perfboard background and fixed pin alignment"""
    
    # Copy the same signals from InteractiveChipScene
    chipResized = pyqtSignal(float, float)
    pinMoved = pyqtSignal(dict)
    actionCompleted = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)  # Only pass parent to QGraphicsScene
        self.perfboard = PerfboardBackground()
        self.show_perfboard = True
        self.pin_grid = 10  # Align to perfboard holes
        
        # Store undo_manager separately
        self.undo_manager = None
        
        # Copy all the properties from InteractiveChipScene
        self.grid_size = 5
        self.chip_body = None
        self.pin_items = []
        self.pin_numbers = []
        self.chip_data = {}
        
        self.setSceneRect(0, 0, 600, 400)
    
    def set_undo_manager(self, undo_manager):
        """Set the undo manager after scene creation"""
        self.undo_manager = undo_manager
        
    def drawBackground(self, painter, rect):
        """Draw perfboard background"""
        super().drawBackground(painter, rect)
        
        if self.show_perfboard:
            self.perfboard.draw_perfboard(painter, rect)
        else:
            # Draw original grid if perfboard is off
            self._draw_original_grid(painter, rect)
    
    def _draw_original_grid(self, painter, rect):
        """Draw original grid background"""
        painter.setPen(QPen(QColor(60, 60, 60), 1))

        x = rect.left()
        while x <= rect.right():
            if int(x) % self.grid_size == 0:
                painter.drawLine(x, rect.top(), x, rect.bottom())
            x += 1

        y = rect.top()
        while y <= rect.bottom():
            if int(y) % self.grid_size == 0:
                painter.drawLine(rect.left(), y, rect.right(), y)
            y += 1

        # Major grid lines
        painter.setPen(QPen(QColor(80, 80, 80), 1))

        x = rect.left()
        while x <= rect.right():
            if int(x) % 25 == 0:
                painter.drawLine(x, rect.top(), x, rect.bottom())
            x += 5

        y = rect.top()
        while y <= rect.bottom():
            if int(y) % 25 == 0:
                painter.drawLine(rect.left(), y, rect.right(), y)
            y += 5
    
    def snap_to_grid(self, pos):
        """Snap position to perfboard grid"""
        if self.show_perfboard:
            x = round(pos.x() / self.pin_grid) * self.pin_grid
            y = round(pos.y() / self.pin_grid) * self.pin_grid
        else:
            x = round(pos.x() / self.grid_size) * self.grid_size
            y = round(pos.y() / self.grid_size) * self.grid_size
        return QPointF(x, y)
    
    def get_chip_data(self):
        """Get current chip data for undo/redo"""
        import copy
        return copy.deepcopy(self.chip_data)

    def create_chip(self, width, height, pins):
        """Create interactive chip with draggable pins - copied from InteractiveChipScene"""
        # Import here to avoid circular imports
        from chip_editor import ResizableChipBody, DraggablePin
        
        self.clear()
        self.pin_items.clear()
        self.pin_numbers.clear()

        self.chip_data = {
            'width': width,
            'height': height,
            'pins': copy.deepcopy(pins)
        }

        chip_x = 150
        chip_y = 50

        self.chip_body = ResizableChipBody(width, height, self.undo_manager)
        self.chip_body.setPos(chip_x, chip_y)
        self.addItem(self.chip_body)

        # Add pin 1 notch
        from PyQt6.QtWidgets import QGraphicsEllipseItem
        notch = QGraphicsEllipseItem(width/2 - 6, -3, 12, 6)
        notch.setBrush(QBrush(QColor(80, 80, 80)))
        notch.setParentItem(self.chip_body)

        # Create draggable pins
        for pin in pins:
            pin_item = DraggablePin(pin, self.grid_size, self.undo_manager)
            pin_item.setParentItem(self.chip_body)
            self.pin_items.append(pin_item)

            # Pin number label
            from PyQt6.QtGui import QFont
            label = self.addText(str(pin['number']), QFont("Arial", 8, QFont.Weight.Bold))
            label.setDefaultTextColor(QColor(255, 255, 150))
            label.setParentItem(self.chip_body)

            label_offset = self._get_label_offset(pin)
            label.setPos(pin['x'] + label_offset[0], pin['y'] + label_offset[1])
            self.pin_numbers.append(label)

        # Chip name
        name_text = self.addText("Test Chip", QFont("Arial", 10, QFont.Weight.Bold))
        name_text.setDefaultTextColor(QColor(255, 255, 255))
        name_text.setParentItem(self.chip_body)
        name_text.setPos(width/2 - 30, height/2 - 8)

    def _get_label_offset(self, pin):
        """Get label offset based on pin side"""
        side = pin.get('side', 'left')

        if side == 'left':
            return (-20, -6)
        elif side == 'right':
            return (8, -6)
        elif side == 'top':
            return (-6, -18)
        elif side == 'bottom':
            return (-6, 8)
        else:
            return (8, -6)

    def toggle_grid(self, show):
        """Toggle grid visibility"""
        self.show_grid = show
        self.update()
