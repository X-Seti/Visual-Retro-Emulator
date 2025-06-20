"""
X-Seti June14 2025 - Canvas Grid System
Visual Retro System Emulator Builder - Advanced Grid Options
"""

#this belongs in ui/ canvas_grid.py

import math
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QLineF
from enum import Enum


class GridStyle(Enum):
    """Grid style options"""
    SOLID_LINE = "solid"
    DOTTED_LINE = "dotted"
    PAPER_CUT_LINE = "paper_cut"
    LEGO_BREADBOARD = "lego_breadboard"
    PCB_PERFBOARD = "pcb_perfboard"
    ENGINEERING_GRID = "engineering"
    NONE = "none"


class GridSpacing(Enum):
    """Standard grid spacings for different applications"""
    FINE = 2.54  # 0.1 inch (2.54mm) - Standard breadboard/PCB spacing
    STANDARD = 5.08  # 0.2 inch (5.08mm) - DIP IC spacing
    COARSE = 7.62  # 0.3 inch (7.62mm) - Wide component spacing
    CUSTOM = 0  # User-defined spacing


class CanvasGrid:
    """Grid system with multiple styles and accurate PCB/breadboard spacing"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.grid_visible = True
        self.grid_style = GridStyle.SOLID_LINE
        self.grid_spacing = GridSpacing.STANDARD
        self.custom_spacing = 20  # pixels
        self.grid_color = QColor(80, 80, 120, 180)
        self.grid_major_color = QColor(120, 120, 160, 200)
        self.snap_to_grid = True
        
        # Grid appearance settings
        self.major_grid_interval = 5  # Every 5th line is major
        self.pin_hole_radius = 1.5  # For breadboard style
        self.paper_cut_length = 8  # Length of cut marks
        
        # Colors for different grid styles
        self.grid_colors = {
            GridStyle.SOLID_LINE: QColor(80, 80, 120, 180),
            GridStyle.DOTTED_LINE: QColor(100, 100, 140, 160),
            GridStyle.PAPER_CUT_LINE: QColor(150, 150, 150, 200),
            GridStyle.LEGO_BREADBOARD: QColor(220, 180, 60, 200),  # Yellow-ish for breadboard
            GridStyle.PCB_PERFBOARD: QColor(45, 80, 22, 180),  # PCB green
            GridStyle.ENGINEERING_GRID: QColor(120, 120, 120, 160),
        }
    
    def get_grid_spacing_pixels(self):
        """Get current grid spacing in pixels"""
        if self.grid_spacing == GridSpacing.CUSTOM:
            return self.custom_spacing
        else:
            # Convert real-world spacing to screen pixels
            # Using 1mm = 3.78 pixels (typical screen DPI conversion)
            mm_to_pixels = 3.78
            return self.grid_spacing.value * mm_to_pixels
    
    def set_grid_style(self, style: GridStyle):
        """Set the grid display style"""
        self.grid_style = style
        if style in self.grid_colors:
            self.grid_color = self.grid_colors[style]
        self.canvas.viewport().update()
    
    def set_grid_spacing(self, spacing: GridSpacing, custom_value=None):
        """Set grid spacing"""
        self.grid_spacing = spacing
        if spacing == GridSpacing.CUSTOM and custom_value:
            self.custom_spacing = custom_value
        self.canvas.viewport().update()
    
    def set_grid_visible(self, visible: bool):
        """Toggle grid visibility"""
        self.grid_visible = visible
        self.canvas.viewport().update()
    
    def set_snap_to_grid(self, enabled: bool):
        """Enable/disable snap to grid"""
        self.snap_to_grid = enabled
    
    def snap_to_grid_point(self, point: QPointF) -> QPointF:
        """Snap a point to the nearest grid intersection"""
        if not self.snap_to_grid:
            return point
        
        spacing = self.get_grid_spacing_pixels()
        snapped_x = round(point.x() / spacing) * spacing
        snapped_y = round(point.y() / spacing) * spacing
        return QPointF(snapped_x, snapped_y)
    
    def draw_grid_background(self, painter: QPainter, rect: QRectF):
        """Main grid drawing method - called from canvas drawBackground"""
        if not self.grid_visible or self.grid_style == GridStyle.NONE:
            return
        
        # Delegate to specific drawing methods based on style
        if self.grid_style == GridStyle.SOLID_LINE:
            self._draw_solid_grid(painter, rect)
        elif self.grid_style == GridStyle.DOTTED_LINE:
            self._draw_dotted_grid(painter, rect)
        elif self.grid_style == GridStyle.PAPER_CUT_LINE:
            self._draw_paper_cut_grid(painter, rect)
        elif self.grid_style == GridStyle.LEGO_BREADBOARD:
            self._draw_lego_breadboard_grid(painter, rect)
        elif self.grid_style == GridStyle.PCB_PERFBOARD:
            self._draw_pcb_perfboard_grid(painter, rect)
        elif self.grid_style == GridStyle.ENGINEERING_GRID:
            self._draw_engineering_grid(painter, rect)
    
    def _draw_solid_grid(self, painter: QPainter, rect: QRectF):
        """Draw solid line grid"""
        spacing = self.get_grid_spacing_pixels()
        
        # Minor grid lines
        minor_pen = QPen(self.grid_color, 0.5, Qt.PenStyle.SolidLine)
        painter.setPen(minor_pen)
        
        # Major grid lines
        major_pen = QPen(self.grid_major_color, 1.0, Qt.PenStyle.SolidLine)
        
        self._draw_grid_lines(painter, rect, spacing, minor_pen, major_pen)
    
    def _draw_dotted_grid(self, painter: QPainter, rect: QRectF):
        """Draw dotted line grid"""
        spacing = self.get_grid_spacing_pixels()
        
        # Create dotted pen
        dotted_pen = QPen(self.grid_color, 1.0, Qt.PenStyle.DotLine)
        dotted_pen.setDashPattern([2, 3])  # 2 pixel dash, 3 pixel gap
        painter.setPen(dotted_pen)
        
        major_pen = QPen(self.grid_major_color, 1.5, Qt.PenStyle.DashLine)
        major_pen.setDashPattern([4, 2])
        
        self._draw_grid_lines(painter, rect, spacing, dotted_pen, major_pen)
    
    def _draw_paper_cut_grid(self, painter: QPainter, rect: QRectF):
        """Draw paper cutting mat style grid with cut marks"""
        spacing = self.get_grid_spacing_pixels()
        
        # Fine grid lines
        fine_pen = QPen(self.grid_color, 0.3, Qt.PenStyle.SolidLine)
        painter.setPen(fine_pen)
        
        # Draw basic grid
        self._draw_grid_lines(painter, rect, spacing, fine_pen, fine_pen)
        
        # Add cut marks at intersections
        cut_pen = QPen(QColor(180, 180, 180, 220), 1.5, Qt.PenStyle.SolidLine)
        painter.setPen(cut_pen)
        
        left = int(rect.left() // spacing) * spacing
        top = int(rect.top() // spacing) * spacing
        
        y = top
        while y <= rect.bottom():
            x = left
            while x <= rect.right():
                # Draw small cut marks at major intersections
                if int(x // spacing) % self.major_grid_interval == 0 and int(y // spacing) % self.major_grid_interval == 0:
                    self._draw_cut_mark(painter, QPointF(x, y))
                x += spacing
            y += spacing
    
    def _draw_lego_breadboard_grid(self, painter: QPainter, rect: QRectF):
        """Draw breadboard-style grid with pin holes"""
        spacing = self.get_grid_spacing_pixels()
        
        # Breadboard background color
        bg_color = QColor(245, 235, 200, 50)  # Light beige
        painter.fillRect(rect, bg_color)
        
        # Draw tie lines (breadboard strips)
        strip_pen = QPen(QColor(200, 200, 200, 150), 2.0, Qt.PenStyle.SolidLine)
        painter.setPen(strip_pen)
        
        # Horizontal tie strips
        y = int(rect.top() // spacing) * spacing
        while y <= rect.bottom():
            if int(y // spacing) % 2 == 0:  # Every other row
                painter.drawLine(QLineF(rect.left(), y, rect.right(), y))
            y += spacing
        
        # Draw pin holes
        hole_brush = QBrush(QColor(40, 40, 40, 200))  # Dark holes
        painter.setBrush(hole_brush)
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        
        left = int(rect.left() // spacing) * spacing
        top = int(rect.top() // spacing) * spacing
        
        y = top
        while y <= rect.bottom():
            x = left
            while x <= rect.right():
                painter.drawEllipse(QPointF(x, y), self.pin_hole_radius, self.pin_hole_radius)
                x += spacing
            y += spacing
    
    def _draw_pcb_perfboard_grid(self, painter: QPainter, rect: QRectF):
        """Draw PCB perfboard style with accurate hole spacing"""
        spacing = self.get_grid_spacing_pixels()
        
        # PCB background
        pcb_color = QColor(45, 80, 22, 30)  # Transparent PCB green
        painter.fillRect(rect, pcb_color)
        
        # Copper pad color
        copper_brush = QBrush(QColor(184, 115, 51, 180))  # Copper color
        painter.setBrush(copper_brush)
        
        # Drill hole color
        hole_brush = QBrush(QColor(20, 20, 20, 255))  # Black holes
        
        left = int(rect.left() // spacing) * spacing
        top = int(rect.top() // spacing) * spacing
        
        y = top
        while y <= rect.bottom():
            x = left
            while x <= rect.right():
                # Draw copper pad
                painter.setBrush(copper_brush)
                painter.setPen(QPen(QColor(160, 100, 40), 0.5))
                pad_radius = spacing * 0.3  # Pad is 30% of spacing
                painter.drawEllipse(QPointF(x, y), pad_radius, pad_radius)
                
                # Draw drill hole
                painter.setBrush(hole_brush)
                painter.setPen(QPen(Qt.PenStyle.NoPen))
                hole_radius = spacing * 0.12  # Hole is 12% of spacing (typical 0.8mm hole)
                painter.drawEllipse(QPointF(x, y), hole_radius, hole_radius)
                
                x += spacing
            y += spacing
    
    def _draw_engineering_grid(self, painter: QPainter, rect: QRectF):
        """Draw engineering/technical drawing style grid"""
        spacing = self.get_grid_spacing_pixels()
        
        # Fine grid
        fine_pen = QPen(QColor(140, 140, 140, 100), 0.25, Qt.PenStyle.SolidLine)
        
        # Medium grid (every 5 lines)
        medium_pen = QPen(QColor(120, 120, 120, 150), 0.5, Qt.PenStyle.SolidLine)
        
        # Major grid (every 10 lines)
        major_pen = QPen(QColor(100, 100, 100, 200), 1.0, Qt.PenStyle.SolidLine)
        
        # Draw fine grid
        painter.setPen(fine_pen)
        self._draw_grid_lines(painter, rect, spacing, fine_pen, fine_pen)
        
        # Draw medium grid
        painter.setPen(medium_pen)
        self._draw_grid_lines(painter, rect, spacing * 5, medium_pen, medium_pen)
        
        # Draw major grid
        painter.setPen(major_pen)
        self._draw_grid_lines(painter, rect, spacing * 10, major_pen, major_pen)
    
    def _draw_grid_lines(self, painter: QPainter, rect: QRectF, spacing: float, minor_pen: QPen, major_pen: QPen):
        """Helper method to draw grid lines"""
        left = int(rect.left() // spacing) * spacing
        top = int(rect.top() // spacing) * spacing
        
        # Draw vertical lines
        x = left
        line_count = 0
        while x <= rect.right():
            if line_count % self.major_grid_interval == 0:
                painter.setPen(major_pen)
            else:
                painter.setPen(minor_pen)
            
            painter.drawLine(QLineF(x, rect.top(), x, rect.bottom()))
            x += spacing
            line_count += 1
        
        # Draw horizontal lines
        y = top
        line_count = 0
        while y <= rect.bottom():
            if line_count % self.major_grid_interval == 0:
                painter.setPen(major_pen)
            else:
                painter.setPen(minor_pen)
            
            painter.drawLine(QLineF(rect.left(), y, rect.right(), y))
            y += spacing
            line_count += 1
    
    def _draw_cut_mark(self, painter: QPainter, center: QPointF):
        """Draw a cutting mat style mark at the specified point"""
        half_length = self.paper_cut_length / 2
        
        # Horizontal cut mark
        painter.drawLine(
            QLineF(center.x() - half_length, center.y(), center.x() + half_length, center.y())
        )
        
        # Vertical cut mark
        painter.drawLine(
            QLineF(center.x(), center.y() - half_length, center.x(), center.y() + half_length)
        )


class PCBCanvasWithGrid(QGraphicsView):
    """PCB Canvas with advanced grid system"""
    
    # Signals
    component_selected = pyqtSignal(object)
    component_moved = pyqtSignal(object, QPointF)
    
    def __init__(self):
        super().__init__()
        
        # Initialize scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Initialize grid system
        self.grid_system = CanvasGrid(self)
        
        # Component tracking
        self.components = {}
        self.connections = []
        self.selected_components = set()
        
        # Zoom tracking
        self.zoom_factor = 1.0
        
        # Legacy compatibility properties
        self.grid_visible = True
        self.grid_size = 20
        self.snap_to_grid = True
        self.grid_color = QColor(80, 80, 120, 180)
        
        # Setup canvas
        self._setup_canvas()
        self._setup_interactions()
    
    def _setup_canvas(self):
        """Setup canvas properties with enhanced grid"""
        # Set scene size for large designs
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)
        
        # Configure view with high quality rendering
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setRenderHint(QPainter.RenderHint.LosslessImageRendering)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Set dark background for contrast
        self.setBackgroundBrush(QBrush(QColor(25, 25, 35)))
    
    def _setup_interactions(self):
        """Setup mouse and keyboard interactions"""
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
    
    def drawBackground(self, painter: QPainter, rect: QRectF):
        """Draw background with enhanced grid system"""
        super().drawBackground(painter, rect)
        
        # Use the enhanced grid system
        self.grid_system.draw_grid_background(painter, rect)
    
    # Grid control methods
    def set_grid_style(self, style: GridStyle):
        """Set grid visual style"""
        self.grid_system.set_grid_style(style)
        print(f"🎨 Grid style changed to: {style.value}")
    
    def set_grid_spacing(self, spacing: GridSpacing, custom_value=None):
        """Set grid spacing"""
        self.grid_system.set_grid_spacing(spacing, custom_value)
        spacing_desc = f"{spacing.value}mm" if spacing != GridSpacing.CUSTOM else f"{custom_value}px"
        print(f"📏 Grid spacing changed to: {spacing_desc}")
    
    def set_grid_visible(self, visible: bool):
        """Toggle grid visibility"""
        self.grid_system.set_grid_visible(visible)
        print(f"👁️ Grid {'visible' if visible else 'hidden'}")
    
    def set_snap_to_grid(self, enabled: bool):
        """Enable/disable snap to grid"""
        self.grid_system.set_snap_to_grid(enabled)
        print(f"🧲 Snap to grid {'enabled' if enabled else 'disabled'}")
    
    def _snap_to_grid(self, point: QPointF) -> QPointF:
        """Snap point to grid (delegates to grid system)"""
        return self.grid_system.snap_to_grid_point(point)
    
    # Convenience methods for common grid configurations
    def set_breadboard_mode(self):
        """Configure for breadboard prototyping"""
        self.set_grid_style(GridStyle.LEGO_BREADBOARD)
        self.set_grid_spacing(GridSpacing.FINE)  # 2.54mm spacing
        self.set_snap_to_grid(True)
        print("🍞 Breadboard mode activated")
    
    def set_pcb_mode(self):
        """Configure for PCB design"""
        self.set_grid_style(GridStyle.PCB_PERFBOARD)
        self.set_grid_spacing(GridSpacing.FINE)  # 2.54mm spacing
        self.set_snap_to_grid(True)
        print("🔧 PCB design mode activated")
    
    def set_schematic_mode(self):
        """Configure for schematic drawing"""
        self.set_grid_style(GridStyle.ENGINEERING_GRID)
        self.set_grid_spacing(GridSpacing.STANDARD)  # 5.08mm spacing
        self.set_snap_to_grid(True)
        print("📋 Schematic mode activated")
    
    def set_freeform_mode(self):
        """Configure for freeform layout"""
        self.set_grid_style(GridStyle.DOTTED_LINE)
        self.set_snap_to_grid(False)
        print("🎨 Freeform mode activated")


# Create alias for backward compatibility
PCBCanvas = PCBCanvasWithGrid