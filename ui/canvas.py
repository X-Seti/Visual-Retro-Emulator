#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Canvas functionality
"""
#this belongs in ui/ canvas.py

import sys
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import json
import os

try:
    from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem, 
                               QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem,
                               QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsPathItem,
                               QApplication, QMenu, QMessageBox, QGraphicsProxyWidget,
                               QWidget, QVBoxLayout, QLabel, QPushButton)
    from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF, pyqtSignal, QTimer
    from PyQt6.QtGui import (QPen, QBrush, QColor, QPainter, QPolygonF, QFont, 
                           QCursor, QPainterPath, QPixmap, QDrag, QTransform)
    PYQT6_AVAILABLE = True
except ImportError as e:
    print(f"❌ PyQt6 import failed: {e}")
    PYQT6_AVAILABLE = False

# CAD Tool Enums
class CADTool(Enum):
    SELECT = "select"
    TRACE = "trace"
    PAD = "pad"
    VIA = "via"
    COPPER_FILL = "copper_fill"
    KEEPOUT = "keepout"
    SILKSCREEN = "silkscreen"
    DRILL = "drill"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    POLYGON = "polygon"
    TEXT = "text"
    DIMENSION = "dimension"
    RULER = "ruler"

class TraceStyle(Enum):
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"

class PadType(Enum):
    ROUND = "round"
    SQUARE = "square"
    OVAL = "oval"
    ROUNDED_RECT = "rounded_rect"
    OCTAGON = "octagon"

class ViaType(Enum):
    THROUGH = "through"
    BLIND = "blind"
    BURIED = "buried"
    MICRO = "micro"

if PYQT6_AVAILABLE:
    
    # === CAD GRAPHICS ITEMS ===
    
    class CADGraphicsItem(QGraphicsItem):
        """Base class for all CAD graphics items"""
        
        def __init__(self, layer_name: str = "pcb"):
            super().__init__()
            self.layer_name = layer_name
            self.cad_type = "unknown"
            self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | 
                         QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        
        def get_properties(self) -> dict:
            """Get item properties for saving"""
            return {
                'layer': self.layer_name,
                'position': [self.pos().x(), self.pos().y()],
                'type': self.cad_type
            }
    
    class PCBTrace(CADGraphicsItem):
        """PCB Trace graphics item"""
        
        def __init__(self, points: List[QPointF], width: float, layer_name: str = "pcb", style: TraceStyle = TraceStyle.SOLID):
            super().__init__(layer_name)
            self.cad_type = "trace"
            self.points = points
            self.width = width
            self.style = style
            
        def boundingRect(self) -> QRectF:
            if not self.points:
                return QRectF()
            
            min_x = min(p.x() for p in self.points)
            max_x = max(p.x() for p in self.points)
            min_y = min(p.y() for p in self.points)
            max_y = max(p.y() for p in self.points)
            
            margin = self.width * 1.5
            return QRectF(min_x - margin, min_y - margin, 
                         max_x - min_x + 2*margin, max_y - min_y + 2*margin)
        
        def paint(self, painter: QPainter, option, widget):
            if len(self.points) < 2:
                return
            
            # Set pen style based on trace style
            pen_style = Qt.PenStyle.SolidLine
            if self.style == TraceStyle.DASHED:
                pen_style = Qt.PenStyle.DashLine
            elif self.style == TraceStyle.DOTTED:
                pen_style = Qt.PenStyle.DotLine
            
            # Trace color based on layer
            if self.layer_name == "chip":
                color = QColor(100, 150, 255)  # Blue for chip
            elif self.layer_name == "gerber":
                color = QColor(255, 100, 100)  # Red for gerber
            else:
                color = QColor(184, 115, 51)   # Copper for PCB
            
            # Convert trace width from mm to pixels (3.78 pixels per mm)
            pen_width = max(1, self.width * 3.78)  # Minimum 1 pixel width
            pen = QPen(color, pen_width, pen_style)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            
            # Draw trace segments
            for i in range(len(self.points) - 1):
                painter.drawLine(self.points[i], self.points[i + 1])
            
            # Highlight if selected
            if self.isSelected():
                highlight_pen = QPen(QColor(255, 255, 0), max(2, pen_width + 2), Qt.PenStyle.DashLine)
                painter.setPen(highlight_pen)
                for i in range(len(self.points) - 1):
                    painter.drawLine(self.points[i], self.points[i + 1])
        
        def get_properties(self) -> dict:
            props = super().get_properties()
            props.update({
                'points': [[p.x(), p.y()] for p in self.points],
                'width': self.width,
                'style': self.style.value
            })
            return props
    
    class PCBPad(CADGraphicsItem):
        """PCB Pad graphics item"""
        
        def __init__(self, position: QPointF, width: float, height: float, 
                     pad_type: PadType = PadType.ROUND, layer_name: str = "pcb"):
            super().__init__(layer_name)
            self.cad_type = "pad"
            self.pad_width = width
            self.pad_height = height
            self.pad_type = pad_type
            self.setPos(position)
        
        def boundingRect(self) -> QRectF:
            pixel_w = self.pad_width * 3.78
            pixel_h = self.pad_height * 3.78
            return QRectF(-pixel_w/2, -pixel_h/2, pixel_w, pixel_h)
        
        def paint(self, painter: QPainter, option, widget):
            pixel_w = self.pad_width * 3.78
            pixel_h = self.pad_height * 3.78
            
            # Pad color based on layer
            if self.layer_name == "chip":
                color = QColor(150, 150, 150)  # Gray for chip
            else:
                color = QColor(184, 115, 51)   # Copper
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color.darker(), 1))
            
            rect = QRectF(-pixel_w/2, -pixel_h/2, pixel_w, pixel_h)
            
            if self.pad_type == PadType.ROUND:
                painter.drawEllipse(rect)
            elif self.pad_type == PadType.SQUARE:
                painter.drawRect(rect)
            elif self.pad_type == PadType.OVAL:
                painter.drawEllipse(rect)
            elif self.pad_type == PadType.ROUNDED_RECT:
                painter.drawRoundedRect(rect, pixel_w*0.1, pixel_h*0.1)
            elif self.pad_type == PadType.OCTAGON:
                # Create octagon
                polygon = QPolygonF()
                for i in range(8):
                    angle = i * 45 * 3.14159 / 180
                    x = (pixel_w/2) * 0.8 * (1 if i % 2 == 0 else 0.7) * (1 if abs(angle) < 1.6 or abs(angle) > 4.7 else -1)
                    y = (pixel_h/2) * 0.8 * (1 if i % 2 == 0 else 0.7) * (1 if 0.8 < angle < 2.4 or 3.9 < angle < 5.5 else -1)
                    polygon.append(QPointF(x, y))
                painter.drawPolygon(polygon)
            
            # Highlight if selected
            if self.isSelected():
                highlight_pen = QPen(QColor(255, 255, 0), 2, Qt.PenStyle.DashLine)
                painter.setPen(highlight_pen)
                painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
                painter.drawRect(rect.adjusted(-2, -2, 2, 2))
        
        def get_properties(self) -> dict:
            props = super().get_properties()
            props.update({
                'width': self.pad_width,
                'height': self.pad_height,
                'pad_type': self.pad_type.value
            })
            return props
    
    class PCBVia(CADGraphicsItem):
        """PCB Via graphics item"""
        
        def __init__(self, position: QPointF, outer_dia: float, drill_dia: float, 
                     via_type: ViaType = ViaType.THROUGH, layer_name: str = "pcb"):
            super().__init__(layer_name)
            self.cad_type = "via"
            self.outer_dia = outer_dia
            self.drill_dia = drill_dia
            self.via_type = via_type
            self.setPos(position)
        
        def boundingRect(self) -> QRectF:
            pixel_dia = self.outer_dia * 3.78
            return QRectF(-pixel_dia/2, -pixel_dia/2, pixel_dia, pixel_dia)
        
        def paint(self, painter: QPainter, option, widget):
            outer_pixels = self.outer_dia * 3.78
            drill_pixels = self.drill_dia * 3.78
            
            # Via pad (copper)
            painter.setBrush(QBrush(QColor(184, 115, 51)))
            painter.setPen(QPen(QColor(160, 100, 40), 1))
            outer_rect = QRectF(-outer_pixels/2, -outer_pixels/2, outer_pixels, outer_pixels)
            painter.drawEllipse(outer_rect)
            
            # Drill hole
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            drill_rect = QRectF(-drill_pixels/2, -drill_pixels/2, drill_pixels, drill_pixels)
            painter.drawEllipse(drill_rect)
            
            # Via type indicator
            if self.via_type != ViaType.THROUGH:
                painter.setPen(QPen(QColor(255, 255, 255), 1))
                painter.setFont(QFont("Arial", 6))
                if self.via_type == ViaType.BLIND:
                    painter.drawText(outer_rect, Qt.AlignmentFlag.AlignCenter, "B")
                elif self.via_type == ViaType.BURIED:
                    painter.drawText(outer_rect, Qt.AlignmentFlag.AlignCenter, "U")
                elif self.via_type == ViaType.MICRO:
                    painter.drawText(outer_rect, Qt.AlignmentFlag.AlignCenter, "μ")
            
            # Highlight if selected
            if self.isSelected():
                highlight_pen = QPen(QColor(255, 255, 0), 2, Qt.PenStyle.DashLine)
                painter.setPen(highlight_pen)
                painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
                painter.drawEllipse(outer_rect.adjusted(-2, -2, 2, 2))
        
        def get_properties(self) -> dict:
            props = super().get_properties()
            props.update({
                'outer_dia': self.outer_dia,
                'drill_dia': self.drill_dia,
                'via_type': self.via_type.value
            })
            return props
    
    class PCBText(CADGraphicsItem):
        """PCB Text graphics item"""
        
        def __init__(self, position: QPointF, text: str, font_size: float = 1.0, layer_name: str = "silkscreen"):
            super().__init__(layer_name)
            self.cad_type = "text"
            self.text = text
            self.font_size = font_size
            self.setPos(position)
        
        def boundingRect(self) -> QRectF:
            # Create a font metrics object properly
            font = QFont("Arial", int(self.font_size * 10))
            from PyQt6.QtGui import QFontMetrics
            metrics = QFontMetrics(font)
            rect = metrics.boundingRect(self.text)
            return QRectF(rect)
        
        def paint(self, painter: QPainter, option, widget):
            if self.layer_name == "silkscreen":
                color = QColor(255, 255, 255)  # White for silkscreen
            elif self.layer_name == "copper":
                color = QColor(184, 115, 51)   # Copper
            else:
                color = QColor(100, 100, 100)  # Gray default
            
            font = QFont("Arial", int(self.font_size * 10))
            painter.setFont(font)
            painter.setPen(QPen(color))
            painter.drawText(0, 0, self.text)
            
            # Highlight if selected
            if self.isSelected():
                highlight_pen = QPen(QColor(255, 255, 0), 1, Qt.PenStyle.DashLine)
                painter.setPen(highlight_pen)
                painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
                painter.drawRect(self.boundingRect())
        
        def get_properties(self) -> dict:
            props = super().get_properties()
            props.update({
                'text': self.text,
                'font_size': self.font_size
            })
            return props
    
    class PCBRectangle(CADGraphicsItem):
        """PCB Rectangle graphics item"""
        
        def __init__(self, start_pos: QPointF, end_pos: QPointF, layer_name: str = "pcb"):
            super().__init__(layer_name)
            self.cad_type = "rectangle"
            self.start_pos = start_pos
            self.end_pos = end_pos
            self.setPos(start_pos)
        
        def boundingRect(self) -> QRectF:
            rect = QRectF(self.start_pos, self.end_pos).normalized()
            return rect.adjusted(-2, -2, 2, 2)
        
        def paint(self, painter: QPainter, option, widget):
            # Color based on layer
            if self.layer_name == "keepout":
                color = QColor(255, 0, 0, 100)  # Transparent red
            elif self.layer_name == "copper":
                color = QColor(184, 115, 51, 150)  # Semi-transparent copper
            else:
                color = QColor(100, 100, 100, 100)  # Gray
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color.darker(), 2))
            
            rect = QRectF(self.start_pos, self.end_pos).normalized()
            painter.drawRect(rect)
            
            # Highlight if selected
            if self.isSelected():
                highlight_pen = QPen(QColor(255, 255, 0), 2, Qt.PenStyle.DashLine)
                painter.setPen(highlight_pen)
                painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
                painter.drawRect(rect.adjusted(-2, -2, 2, 2))
        
        def get_properties(self) -> dict:
            props = super().get_properties()
            props.update({
                'start_pos': [self.start_pos.x(), self.start_pos.y()],
                'end_pos': [self.end_pos.x(), self.end_pos.y()]
            })
            return props
    
    class PCBCircle(CADGraphicsItem):
        """PCB Circle graphics item"""
        
        def __init__(self, center: QPointF, radius: float, layer_name: str = "pcb"):
            super().__init__(layer_name)
            self.cad_type = "circle"
            self.radius = radius
            self.setPos(center)
        
        def boundingRect(self) -> QRectF:
            r = self.radius + 2
            return QRectF(-r, -r, 2*r, 2*r)
        
        def paint(self, painter: QPainter, option, widget):
            # Color based on layer
            if self.layer_name == "keepout":
                color = QColor(255, 0, 0, 100)  # Transparent red
            elif self.layer_name == "copper":
                color = QColor(184, 115, 51, 150)  # Semi-transparent copper
            else:
                color = QColor(100, 100, 100, 100)  # Gray
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color.darker(), 2))
            painter.drawEllipse(-self.radius, -self.radius, 2*self.radius, 2*self.radius)
            
            # Highlight if selected
            if self.isSelected():
                highlight_pen = QPen(QColor(255, 255, 0), 2, Qt.PenStyle.DashLine)
                painter.setPen(highlight_pen)
                painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
                painter.drawEllipse(-self.radius-2, -self.radius-2, 2*(self.radius+2), 2*(self.radius+2))
        
        def get_properties(self) -> dict:
            props = super().get_properties()
            props.update({
                'radius': self.radius
            })
            return props
    
    # === CANVAS CLASS ===
    
    class PCBCanvas(QGraphicsView):
        """PCB Canvas"""
        
        # Signals
        component_selected = pyqtSignal(object)
        component_added = pyqtSignal(object)
        cad_item_added = pyqtSignal(object)
        cad_item_selected = pyqtSignal(object)
        zoom_changed = pyqtSignal(float)
        
        def __init__(self, parent=None):
            super().__init__(parent)
            
            # Initialize scene
            self.scene = QGraphicsScene()
            self.setScene(self.scene)
            
            # Canvas properties
            self.zoom_factor = 1.0
            self.grid_visible = True
            self.grid_spacing = 20
            self.snap_to_grid = True
            
            # Component management
            self.components = {}
            self.connections = []
            
            # CAD tool properties
            self.current_cad_tool = CADTool.SELECT
            self.cad_items = []
            
            # CAD drawing state
            self.is_cad_drawing = False
            self.current_trace_points = []
            self.temp_cad_item = None
            self.drawing_start_pos = None
            
            # CAD settings
            self.trace_width = 0.2
            self.trace_style = TraceStyle.SOLID
            self.pad_width = 1.0
            self.pad_height = 1.0
            self.pad_type = PadType.ROUND
            self.via_outer = 0.6
            self.via_drill = 0.3
            self.via_type = ViaType.THROUGH
            self.active_layer = "pcb"
            
            # Text input for text tool
            self.text_input = ""
            
            self._setup_canvas()
            print("✅ PCB Canvas with CAD tools initialized")
        
        def _setup_canvas(self):
            """Setup canvas properties"""
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            self.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # === CAD TOOL METHODS ===
        
        def set_cad_tool(self, tool: CADTool):
            """Set the current CAD tool"""
            # Finish any ongoing operation before switching tools
            if self.is_cad_drawing:
                if self.current_cad_tool == CADTool.TRACE and len(self.current_trace_points) >= 2:
                    # Auto-finish the current trace
                    self._finish_trace()
                elif self.current_cad_tool == CADTool.POLYGON and len(self.current_trace_points) >= 3:
                    # Auto-finish the current polygon
                    self._finish_polygon()
                else:
                    # Cancel other incomplete operations
                    self._cancel_cad_operation()
            
            self.current_cad_tool = tool
            
            # Update cursor based on tool
            cursors = {
                CADTool.SELECT: Qt.CursorShape.ArrowCursor,
                CADTool.TRACE: Qt.CursorShape.CrossCursor,
                CADTool.PAD: Qt.CursorShape.PointingHandCursor,
                CADTool.VIA: Qt.CursorShape.PointingHandCursor,
                CADTool.COPPER_FILL: Qt.CursorShape.CrossCursor,
                CADTool.KEEPOUT: Qt.CursorShape.ForbiddenCursor,
                CADTool.SILKSCREEN: Qt.CursorShape.IBeamCursor,
                CADTool.DRILL: Qt.CursorShape.PointingHandCursor,
                CADTool.RECTANGLE: Qt.CursorShape.CrossCursor,
                CADTool.CIRCLE: Qt.CursorShape.CrossCursor,
                CADTool.POLYGON: Qt.CursorShape.CrossCursor,
                CADTool.TEXT: Qt.CursorShape.IBeamCursor,
                CADTool.DIMENSION: Qt.CursorShape.CrossCursor,
                CADTool.RULER: Qt.CursorShape.CrossCursor
            }
            
            self.setCursor(QCursor(cursors.get(tool, Qt.CursorShape.ArrowCursor)))
            print(f"🔧 CAD tool set: {tool.value}")
            
            # If we auto-finished a trace, show a message
            if tool != CADTool.TRACE and hasattr(self, '_just_finished_trace'):
                print("📝 Trace auto-completed when switching tools")
                delattr(self, '_just_finished_trace')
        
        def set_trace_width(self, width: float):
            """Set trace width"""
            self.trace_width = width
        
        def set_trace_style(self, style: TraceStyle):
            """Set trace style"""
            self.trace_style = style
        
        def set_pad_size(self, width: float, height: float):
            """Set pad size"""
            self.pad_width = width
            self.pad_height = height
        
        def set_pad_type(self, pad_type: PadType):
            """Set pad type"""
            self.pad_type = pad_type
        
        def set_via_size(self, outer: float, drill: float):
            """Set via size"""
            self.via_outer = outer
            self.via_drill = drill
        
        def set_via_type(self, via_type: ViaType):
            """Set via type"""
            self.via_type = via_type
        
        def set_active_layer(self, layer: str):
            """Set active layer"""
            self.active_layer = layer
        
        # === MOUSE EVENT HANDLERS ===
        
        def mousePressEvent(self, event):
            """Handle mouse press for CAD operations"""
            if event.button() == Qt.MouseButton.LeftButton:
                scene_pos = self.mapToScene(event.pos())
                
                # Snap to grid if enabled
                if self.snap_to_grid:
                    scene_pos = self._snap_to_grid(scene_pos)
                
                # Handle different CAD tools
                if self.current_cad_tool == CADTool.TRACE:
                    self._handle_trace_click(scene_pos)
                elif self.current_cad_tool == CADTool.PAD:
                    self._place_pad(scene_pos)
                elif self.current_cad_tool == CADTool.VIA:
                    self._place_via(scene_pos)
                elif self.current_cad_tool == CADTool.CIRCLE:
                    self._handle_circle_click(scene_pos)
                elif self.current_cad_tool == CADTool.RECTANGLE:
                    self._handle_rectangle_click(scene_pos)
                elif self.current_cad_tool == CADTool.COPPER_FILL:
                    self._place_copper_fill(scene_pos)
                elif self.current_cad_tool == CADTool.KEEPOUT:
                    self._place_keepout(scene_pos)
                elif self.current_cad_tool == CADTool.DRILL:
                    self._place_drill(scene_pos)
                elif self.current_cad_tool == CADTool.TEXT:
                    self._place_text(scene_pos)
                elif self.current_cad_tool == CADTool.SILKSCREEN:
                    self._place_silkscreen(scene_pos)
                elif self.current_cad_tool == CADTool.POLYGON:
                    self._handle_polygon_click(scene_pos)
                elif self.current_cad_tool == CADTool.DIMENSION:
                    self._handle_dimension_click(scene_pos)
                elif self.current_cad_tool == CADTool.RULER:
                    self._handle_ruler_click(scene_pos)
                else:
                    # Default selection behavior
                    super().mousePressEvent(event)
                    
            elif event.button() == Qt.MouseButton.RightButton:
                # Right click cancels current operation
                self._cancel_cad_operation()
            else:
                super().mousePressEvent(event)
        
        def mouseMoveEvent(self, event):
            """Handle mouse move for CAD operations"""
            scene_pos = self.mapToScene(event.pos())
            
            if self.snap_to_grid:
                scene_pos = self._snap_to_grid(scene_pos)
            
            # Handle drawing previews
            if self.is_cad_drawing:
                if self.current_cad_tool == CADTool.TRACE:
                    self._update_trace_preview(scene_pos)
                elif self.current_cad_tool == CADTool.CIRCLE:
                    self._update_circle_preview(scene_pos)
                elif self.current_cad_tool == CADTool.RECTANGLE:
                    self._update_rectangle_preview(scene_pos)
            
            super().mouseMoveEvent(event)
        
        def mouseDoubleClickEvent(self, event):
            """Handle double click to finish operations"""
            if self.current_cad_tool == CADTool.TRACE and self.is_cad_drawing:
                self._finish_trace()
            elif self.current_cad_tool == CADTool.POLYGON and self.is_cad_drawing:
                self._finish_polygon()
            else:
                super().mouseDoubleClickEvent(event)
        
        def keyPressEvent(self, event):
            """Handle keyboard shortcuts"""
            key = event.key()
            
            # CAD tool shortcuts
            tool_shortcuts = {
                Qt.Key.Key_S: CADTool.SELECT,
                Qt.Key.Key_T: CADTool.TRACE,
                Qt.Key.Key_P: CADTool.PAD,
                Qt.Key.Key_V: CADTool.VIA,
                Qt.Key.Key_R: CADTool.RECTANGLE,
                Qt.Key.Key_C: CADTool.CIRCLE,
                Qt.Key.Key_F: CADTool.COPPER_FILL,
                Qt.Key.Key_K: CADTool.KEEPOUT,
                Qt.Key.Key_G: CADTool.SILKSCREEN,
                Qt.Key.Key_D: CADTool.DRILL,
                Qt.Key.Key_L: CADTool.POLYGON,
                Qt.Key.Key_X: CADTool.TEXT,
                Qt.Key.Key_M: CADTool.DIMENSION,
                Qt.Key.Key_U: CADTool.RULER
            }
            
            if key in tool_shortcuts:
                self.set_cad_tool(tool_shortcuts[key])
                return
            
            if key == Qt.Key.Key_Escape:
                self._cancel_cad_operation()
                return
            
            super().keyPressEvent(event)
        
        # === CAD TOOL IMPLEMENTATIONS ===
        
        def _handle_trace_click(self, pos: QPointF):
            """Handle trace tool clicks"""
            if not self.is_cad_drawing:
                # Start new trace
                self.is_cad_drawing = True
                self.current_trace_points = [pos]
                print(f"🔧 Started trace at {pos.x():.1f}, {pos.y():.1f}")
            else:
                # Add point to current trace
                self.current_trace_points.append(pos)
                print(f"🔧 Added trace point at {pos.x():.1f}, {pos.y():.1f}")
        
        def _update_trace_preview(self, pos: QPointF):
            """Update trace preview while drawing"""
            if not self.current_trace_points:
                return
            
            # Remove old preview
            if self.temp_cad_item:
                self.scene.removeItem(self.temp_cad_item)
            
            # Create preview trace
            preview_points = self.current_trace_points + [pos]
            self.temp_cad_item = PCBTrace(preview_points, self.trace_width, self.active_layer, self.trace_style)
            self.temp_cad_item.setOpacity(0.7)  # Semi-transparent preview
            self.scene.addItem(self.temp_cad_item)
        
        def _finish_trace(self):
            """Finish drawing the current trace"""
            if self.is_cad_drawing and len(self.current_trace_points) >= 2:
                # Remove preview
                if self.temp_cad_item:
                    self.scene.removeItem(self.temp_cad_item)
                    self.temp_cad_item = None
                
                # Create final trace
                trace = PCBTrace(self.current_trace_points.copy(), self.trace_width, self.active_layer, self.trace_style)
                self.scene.addItem(trace)
                self.cad_items.append(trace)
                self.cad_item_added.emit(trace)
                
                print(f"✅ Created trace with {len(self.current_trace_points)} points, width: {self.trace_width}mm")
                
                # Mark that we just finished a trace (for tool switching message)
                self._just_finished_trace = True
                
                # Reset state
                self.is_cad_drawing = False
                self.current_trace_points = []
            elif self.is_cad_drawing and len(self.current_trace_points) == 1:
                # Only one point, cancel instead
                print("❌ Need at least 2 points for trace")
                self._cancel_cad_operation()
        
        def _place_pad(self, pos: QPointF):
            """Place a pad at position"""
            pad = PCBPad(pos, self.pad_width, self.pad_height, self.pad_type, self.active_layer)
            self.scene.addItem(pad)
            self.cad_items.append(pad)
            self.cad_item_added.emit(pad)
            print(f"✅ Placed {self.pad_type.value} pad at {pos.x():.1f}, {pos.y():.1f}")
        
        def _place_via(self, pos: QPointF):
            """Place a via at position"""
            via = PCBVia(pos, self.via_outer, self.via_drill, self.via_type, self.active_layer)
            self.scene.addItem(via)
            self.cad_items.append(via)
            self.cad_item_added.emit(via)
            print(f"✅ Placed {self.via_type.value} via at {pos.x():.1f}, {pos.y():.1f}")
        
        def _handle_circle_click(self, pos: QPointF):
            """Handle circle tool clicks"""
            if not self.is_cad_drawing:
                # Start circle drawing
                self.is_cad_drawing = True
                self.drawing_start_pos = pos
                print(f"🔧 Started circle at {pos.x():.1f}, {pos.y():.1f}")
            else:
                # Finish circle
                radius = ((pos.x() - self.drawing_start_pos.x())**2 + 
                         (pos.y() - self.drawing_start_pos.y())**2)**0.5
                
                # Remove preview
                if self.temp_cad_item:
                    self.scene.removeItem(self.temp_cad_item)
                    self.temp_cad_item = None
                
                # Create final circle
                circle = PCBCircle(self.drawing_start_pos, radius, self.active_layer)
                self.scene.addItem(circle)
                self.cad_items.append(circle)
                self.cad_item_added.emit(circle)
                
                print(f"✅ Created circle with radius {radius:.1f}")
                
                # Reset state
                self.is_cad_drawing = False
                self.drawing_start_pos = None
        
        def _update_circle_preview(self, pos: QPointF):
            """Update circle preview"""
            if not self.drawing_start_pos:
                return
            
            # Remove old preview
            if self.temp_cad_item:
                self.scene.removeItem(self.temp_cad_item)
            
            # Calculate radius
            radius = ((pos.x() - self.drawing_start_pos.x())**2 + 
                     (pos.y() - self.drawing_start_pos.y())**2)**0.5
            
            # Create preview circle
            self.temp_cad_item = PCBCircle(self.drawing_start_pos, radius, self.active_layer)
            self.temp_cad_item.setOpacity(0.7)
            self.scene.addItem(self.temp_cad_item)
        
        def _handle_rectangle_click(self, pos: QPointF):
            """Handle rectangle tool clicks"""
            if not self.is_cad_drawing:
                # Start rectangle drawing
                self.is_cad_drawing = True
                self.drawing_start_pos = pos
                print(f"🔧 Started rectangle at {pos.x():.1f}, {pos.y():.1f}")
            else:
                # Finish rectangle
                # Remove preview
                if self.temp_cad_item:
                    self.scene.removeItem(self.temp_cad_item)
                    self.temp_cad_item = None
                
                # Create final rectangle
                rect = PCBRectangle(self.drawing_start_pos, pos, self.active_layer)
                self.scene.addItem(rect)
                self.cad_items.append(rect)
                self.cad_item_added.emit(rect)
                
                print(f"✅ Created rectangle from {self.drawing_start_pos.x():.1f},{self.drawing_start_pos.y():.1f} to {pos.x():.1f},{pos.y():.1f}")
                
                # Reset state
                self.is_cad_drawing = False
                self.drawing_start_pos = None
        
        def _update_rectangle_preview(self, pos: QPointF):
            """Update rectangle preview"""
            if not self.drawing_start_pos:
                return
            
            # Remove old preview
            if self.temp_cad_item:
                self.scene.removeItem(self.temp_cad_item)
            
            # Create preview rectangle
            self.temp_cad_item = PCBRectangle(self.drawing_start_pos, pos, self.active_layer)
            self.temp_cad_item.setOpacity(0.7)
            self.scene.addItem(self.temp_cad_item)
        
        def _place_copper_fill(self, pos: QPointF):
            """Place copper fill (simplified as rectangle for now)"""
            # For now, create a 10x10mm copper fill rectangle
            size = 10.0 * 3.78  # Convert to pixels
            start_pos = QPointF(pos.x() - size/2, pos.y() - size/2)
            end_pos = QPointF(pos.x() + size/2, pos.y() + size/2)
            
            fill = PCBRectangle(start_pos, end_pos, "copper")
            self.scene.addItem(fill)
            self.cad_items.append(fill)
            self.cad_item_added.emit(fill)
            print(f"✅ Placed copper fill at {pos.x():.1f}, {pos.y():.1f}")
        
        def _place_keepout(self, pos: QPointF):
            """Place keepout area (as rectangle)"""
            # Create a 5x5mm keepout rectangle
            size = 5.0 * 3.78  # Convert to pixels
            start_pos = QPointF(pos.x() - size/2, pos.y() - size/2)
            end_pos = QPointF(pos.x() + size/2, pos.y() + size/2)
            
            keepout = PCBRectangle(start_pos, end_pos, "keepout")
            self.scene.addItem(keepout)
            self.cad_items.append(keepout)
            self.cad_item_added.emit(keepout)
            print(f"✅ Placed keepout area at {pos.x():.1f}, {pos.y():.1f}")
        
        def _place_drill(self, pos: QPointF):
            """Place drill hole (as small via)"""
            drill = PCBVia(pos, self.via_drill * 1.5, self.via_drill, ViaType.THROUGH, "drill")
            self.scene.addItem(drill)
            self.cad_items.append(drill)
            self.cad_item_added.emit(drill)
            print(f"✅ Placed drill hole at {pos.x():.1f}, {pos.y():.1f}")
        
        def _place_text(self, pos: QPointF):
            """Place text with input dialog"""
            from PyQt6.QtWidgets import QInputDialog
            
            # Get text from user
            text, ok = QInputDialog.getText(self, 'PCB Text', 'Enter text:')
            
            if ok and text:
                text_item = PCBText(pos, text, 1.0, self.active_layer)
                self.scene.addItem(text_item)
                self.cad_items.append(text_item)
                self.cad_item_added.emit(text_item)
                print(f"✅ Placed text '{text}' at {pos.x():.1f}, {pos.y():.1f}")
            else:
                print("❌ Text input cancelled")
        
        def _place_silkscreen(self, pos: QPointF):
            """Place silkscreen text with input dialog"""
            from PyQt6.QtWidgets import QInputDialog
            
            # Get text from user
            text, ok = QInputDialog.getText(self, 'Silkscreen Text', 'Enter text for silkscreen:')
            
            if ok and text:
                silk_item = PCBText(pos, text, 0.8, "silkscreen")
                self.scene.addItem(silk_item)
                self.cad_items.append(silk_item)
                self.cad_item_added.emit(silk_item)
                print(f"✅ Placed silkscreen text '{text}' at {pos.x():.1f}, {pos.y():.1f}")
            else:
                print("❌ Silkscreen text cancelled")
        
        def _handle_polygon_click(self, pos: QPointF):
            """Handle polygon tool clicks (similar to trace but closed)"""
            if not self.is_cad_drawing:
                # Start new polygon
                self.is_cad_drawing = True
                self.current_trace_points = [pos]
                print(f"🔧 Started polygon at {pos.x():.1f}, {pos.y():.1f}")
            else:
                # Add point to current polygon
                self.current_trace_points.append(pos)
                print(f"🔧 Added polygon point at {pos.x():.1f}, {pos.y():.1f}")
        
        def _finish_polygon(self):
            """Finish drawing the current polygon"""
            if self.is_cad_drawing and len(self.current_trace_points) >= 3:
                # Close the polygon by adding first point at end
                closed_points = self.current_trace_points + [self.current_trace_points[0]]
                
                # Remove preview
                if self.temp_cad_item:
                    self.scene.removeItem(self.temp_cad_item)
                    self.temp_cad_item = None
                
                # Create final polygon (as trace for now)
                polygon = PCBTrace(closed_points, self.trace_width, self.active_layer, self.trace_style)
                self.scene.addItem(polygon)
                self.cad_items.append(polygon)
                self.cad_item_added.emit(polygon)
                
                print(f"✅ Created polygon with {len(self.current_trace_points)} vertices")
                
                # Reset state
                self.is_cad_drawing = False
                self.current_trace_points = []
        
        def _handle_dimension_click(self, pos: QPointF):
            """Handle dimension tool clicks"""
            if not self.is_cad_drawing:
                # Start dimension line
                self.is_cad_drawing = True
                self.drawing_start_pos = pos
                print(f"🔧 Started dimension at {pos.x():.1f}, {pos.y():.1f}")
            else:
                # Finish dimension line
                # Calculate distance
                distance = ((pos.x() - self.drawing_start_pos.x())**2 + 
                           (pos.y() - self.drawing_start_pos.y())**2)**0.5 / 3.78  # Convert to mm
                
                # Remove preview
                if self.temp_cad_item:
                    self.scene.removeItem(self.temp_cad_item)
                    self.temp_cad_item = None
                
                # Create dimension line (as trace) and text
                dim_line = PCBTrace([self.drawing_start_pos, pos], 0.1, "dimension")
                self.scene.addItem(dim_line)
                self.cad_items.append(dim_line)
                
                # Add dimension text
                mid_point = QPointF((self.drawing_start_pos.x() + pos.x()) / 2,
                                   (self.drawing_start_pos.y() + pos.y()) / 2)
                dim_text = PCBText(mid_point, f"{distance:.1f}mm", 0.6, "dimension")
                self.scene.addItem(dim_text)
                self.cad_items.append(dim_text)
                
                self.cad_item_added.emit(dim_line)
                self.cad_item_added.emit(dim_text)
                
                print(f"✅ Created dimension: {distance:.1f}mm")
                
                # Reset state
                self.is_cad_drawing = False
                self.drawing_start_pos = None
        
        def _handle_ruler_click(self, pos: QPointF):
            """Handle ruler tool clicks (measurement only)"""
            if not self.is_cad_drawing:
                # Start measurement
                self.is_cad_drawing = True
                self.drawing_start_pos = pos
                print(f"🔧 Started measurement at {pos.x():.1f}, {pos.y():.1f}")
            else:
                # Finish measurement and show result
                distance = ((pos.x() - self.drawing_start_pos.x())**2 + 
                           (pos.y() - self.drawing_start_pos.y())**2)**0.5 / 3.78  # Convert to mm
                
                # Remove preview
                if self.temp_cad_item:
                    self.scene.removeItem(self.temp_cad_item)
                    self.temp_cad_item = None
                
                print(f"📏 Measured distance: {distance:.2f}mm")
                
                # Reset state
                self.is_cad_drawing = False
                self.drawing_start_pos = None
        
        def _cancel_cad_operation(self):
            """Cancel current CAD operation"""
            if self.temp_cad_item:
                self.scene.removeItem(self.temp_cad_item)
                self.temp_cad_item = None
            
            self.is_cad_drawing = False
            self.current_trace_points = []
            self.drawing_start_pos = None
            print("❌ CAD operation cancelled")
        
        def _snap_to_grid(self, pos: QPointF) -> QPointF:
            """Snap position to grid"""
            if not self.snap_to_grid:
                return pos
            
            grid_size = self.grid_spacing
            snapped_x = round(pos.x() / grid_size) * grid_size
            snapped_y = round(pos.y() / grid_size) * grid_size
            
            return QPointF(snapped_x, snapped_y)
        
        # === GRID AND VIEW METHODS ===
        
        def set_grid_visible(self, visible: bool):
            """Set grid visibility"""
            self.grid_visible = visible
            self.scene.update()
        
        def set_grid_spacing(self, spacing: int):
            """Set grid spacing"""
            self.grid_spacing = spacing
            self.scene.update()
        
        def set_snap_to_grid(self, snap: bool):
            """Set snap to grid"""
            self.snap_to_grid = snap
        
        def zoom_in(self):
            """Zoom in"""
            self.scale(1.25, 1.25)
            self.zoom_factor *= 1.25
            self.zoom_changed.emit(self.zoom_factor)
        
        def zoom_out(self):
            """Zoom out"""
            self.scale(0.8, 0.8)
            self.zoom_factor *= 0.8
            self.zoom_changed.emit(self.zoom_factor)
        
        def reset_zoom(self):
            """Reset zoom to 100%"""
            self.resetTransform()
            self.zoom_factor = 1.0
            self.zoom_changed.emit(self.zoom_factor)
        
        def fit_to_window(self):
            """Fit all items to window"""
            self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            # Calculate zoom factor from transform
            transform = self.transform()
            self.zoom_factor = transform.m11()  # Get scale factor
            self.zoom_changed.emit(self.zoom_factor)
        
        # === CAD DATA MANAGEMENT ===
        
        def clear_all_cad_items(self):
            """Clear all CAD items from canvas"""
            for item in self.cad_items:
                self.scene.removeItem(item)
            self.cad_items.clear()
            print("🧹 All CAD items cleared")
        
        def get_cad_items_data(self) -> List[dict]:
            """Get all CAD items as data for saving"""
            items_data = []
            for item in self.cad_items:
                if hasattr(item, 'get_properties'):
                    items_data.append(item.get_properties())
            return items_data
        
        def load_cad_items_data(self, items_data: List[dict]):
            """Load CAD items from data"""
            self.clear_all_cad_items()
            
            for item_data in items_data:
                try:
                    item_type = item_data.get('type', 'unknown')
                    
                    if item_type == 'trace':
                        points = [QPointF(*p) for p in item_data.get('points', [])]
                        if len(points) >= 2:
                            trace = PCBTrace(points, item_data.get('width', 0.2), 
                                           item_data.get('layer', 'pcb'),
                                           TraceStyle(item_data.get('style', 'solid')))
                            self.scene.addItem(trace)
                            self.cad_items.append(trace)
                    
                    elif item_type == 'pad':
                        pos = QPointF(*item_data.get('position', [0, 0]))
                        pad = PCBPad(pos, item_data.get('width', 1.0), item_data.get('height', 1.0),
                                    PadType(item_data.get('pad_type', 'round')), item_data.get('layer', 'pcb'))
                        self.scene.addItem(pad)
                        self.cad_items.append(pad)
                    
                    elif item_type == 'via':
                        pos = QPointF(*item_data.get('position', [0, 0]))
                        via = PCBVia(pos, item_data.get('outer_dia', 0.6), item_data.get('drill_dia', 0.3),
                                    ViaType(item_data.get('via_type', 'through')), item_data.get('layer', 'pcb'))
                        self.scene.addItem(via)
                        self.cad_items.append(via)
                    
                    elif item_type == 'rectangle':
                        start_pos = QPointF(*item_data.get('start_pos', [0, 0]))
                        end_pos = QPointF(*item_data.get('end_pos', [10, 10]))
                        rect = PCBRectangle(start_pos, end_pos, item_data.get('layer', 'pcb'))
                        self.scene.addItem(rect)
                        self.cad_items.append(rect)
                    
                    elif item_type == 'circle':
                        pos = QPointF(*item_data.get('position', [0, 0]))
                        circle = PCBCircle(pos, item_data.get('radius', 5.0), item_data.get('layer', 'pcb'))
                        self.scene.addItem(circle)
                        self.cad_items.append(circle)
                    
                    elif item_type == 'text':
                        pos = QPointF(*item_data.get('position', [0, 0]))
                        text = PCBText(pos, item_data.get('text', 'TEXT'), 
                                      item_data.get('font_size', 1.0), item_data.get('layer', 'silkscreen'))
                        self.scene.addItem(text)
                        self.cad_items.append(text)
                        
                except Exception as e:
                    print(f"⚠️ Error loading CAD item: {e}")
            
            print(f"✅ Loaded {len(self.cad_items)} CAD items")

else:

    class PCBCanvas:
        """PCB Canvas"""
        
        def __init__(self, parent=None):
            print("⚠️ PCB Canvas: PyQt6 not available")
        
        def set_cad_tool(self, tool):
            print(f"⚠️ Fallback canvas: CAD tool {tool}")

# Export
__all__ = [
    'PCBCanvas', 'CADTool', 'TraceStyle', 'PadType', 'ViaType',
    'PCBTrace', 'PCBPad', 'PCBVia', 'PCBText', 'PCBRectangle', 'PCBCircle',
    'CADGraphicsItem'
]

if __name__ == "__main__":
    # Test the canvas
    if PYQT6_AVAILABLE:
        app = QApplication(sys.argv)
        canvas = PCBCanvas()
        canvas.show()
        canvas.set_cad_tool(CADTool.TRACE)
        print("🧪 Canvas test - close window to continue")
        app.exec()
        print("✅ Canvas test completed")
    else:
        print("⚠️ Cannot test - PyQt6 not available")
