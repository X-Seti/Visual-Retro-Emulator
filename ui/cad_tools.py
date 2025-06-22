#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Electronic CAD Canvas Tools
Electronic CAD drawing functions for the first canvas layer (chip layer)
Adds PCB design tools: traces, pads, vias, copper fills, silkscreen, etc.
"""
#this belongs in ui/ cad_tools.py

from enum import Enum
from typing import List, Dict, Optional, Tuple, Any
from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem, 
                           QGraphicsPathItem, QGraphicsEllipseItem, QGraphicsRectItem,
                           QGraphicsLineItem, QGraphicsPolygonItem, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QButtonGroup, QComboBox, QSpinBox,
                           QDoubleSpinBox, QLabel, QColorDialog, QGroupBox, QSlider,
                           QCheckBox, QToolButton, QMenu, QAction)
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF, QTimer
from PyQt6.QtGui import (QPainter, QPen, QBrush, QColor, QPainterPath, QPolygonF,
                        QFont, QIcon, QPixmap, QCursor)

# === CAD TOOL MODES ===
class CADTool(Enum):
    """Electronic CAD drawing tools"""
    SELECT = "select"
    TRACE = "trace"               # PCB traces/tracks
    PAD = "pad"                   # SMD/THT pads
    VIA = "via"                   # Vias for layer connections
    COPPER_FILL = "copper_fill"   # Copper fill areas
    KEEPOUT = "keepout"           # Keepout areas
    SILKSCREEN = "silkscreen"     # Silkscreen text/graphics
    DRILL = "drill"               # Drill holes
    RECTANGLE = "rectangle"       # Rectangle drawing
    CIRCLE = "circle"             # Circle drawing
    POLYGON = "polygon"           # Polygon drawing
    TEXT = "text"                 # Text placement
    DIMENSION = "dimension"       # Dimension lines
    RULER = "ruler"              # Measurement tool

class TraceStyle(Enum):
    """PCB trace styles"""
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"

class PadType(Enum):
    """PCB pad types"""
    ROUND = "round"
    SQUARE = "square"
    OVAL = "oval"
    ROUNDED_RECT = "rounded_rect"
    OCTAGON = "octagon"

class ViaType(Enum):
    """Via types"""
    THROUGH = "through"           # Through-hole via
    BLIND = "blind"               # Blind via
    BURIED = "buried"             # Buried via
    MICRO = "micro"               # Microvia

# === CAD GRAPHICS ITEMS ===
class CADGraphicsItem(QGraphicsItem):
    """Base class for CAD graphics items"""
    
    def __init__(self, layer_name: str = "chip"):
        super().__init__()
        self.layer_name = layer_name
        self.cad_type = "generic"
        self.properties = {}
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

class PCBTrace(CADGraphicsItem):
    """PCB trace/track item"""
    
    def __init__(self, points: List[QPointF], width: float = 0.2, layer_name: str = "chip"):
        super().__init__(layer_name)
        self.cad_type = "trace"
        self.points = points
        self.width = width  # in mm
        self.style = TraceStyle.SOLID
        self.net_name = ""
        self.properties = {
            'width': width,
            'style': TraceStyle.SOLID.value,
            'net_name': '',
            'layer': layer_name
        }
        self._setup_path()
    
    def _setup_path(self):
        """Create the trace path"""
        self.path = QPainterPath()
        if len(self.points) >= 2:
            self.path.moveTo(self.points[0])
            for point in self.points[1:]:
                self.path.lineTo(point)
    
    def boundingRect(self) -> QRectF:
        """Return bounding rectangle"""
        if hasattr(self, 'path'):
            return self.path.boundingRect().adjusted(-self.width/2, -self.width/2, 
                                                   self.width/2, self.width/2)
        return QRectF()
    
    def paint(self, painter: QPainter, option, widget):
        """Paint the trace"""
        if not hasattr(self, 'path'):
            return
            
        # Convert mm to pixels (assuming 96 DPI, 1mm = 3.78 pixels)
        pixel_width = self.width * 3.78
        
        # Trace color based on layer
        if self.layer_name == "chip":
            color = QColor(184, 115, 51)  # Copper color
        else:
            color = QColor(100, 200, 100)  # Green for other layers
        
        # Draw trace
        pen = QPen(color, pixel_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        if self.style == TraceStyle.DASHED:
            pen.setStyle(Qt.PenStyle.DashLine)
        elif self.style == TraceStyle.DOTTED:
            pen.setStyle(Qt.PenStyle.DotLine)
        
        painter.setPen(pen)
        painter.drawPath(self.path)
        
        # Highlight if selected
        if self.isSelected():
            highlight_pen = QPen(QColor(255, 255, 0), 2, Qt.PenStyle.DashLine)
            painter.setPen(highlight_pen)
            painter.drawPath(self.path)

class PCBPad(CADGraphicsItem):
    """PCB pad item"""
    
    def __init__(self, center: QPointF, width: float, height: float, 
                 pad_type: PadType = PadType.ROUND, layer_name: str = "chip"):
        super().__init__(layer_name)
        self.cad_type = "pad"
        self.center = center
        self.width = width  # in mm
        self.height = height  # in mm
        self.pad_type = pad_type
        self.drill_size = 0.0  # 0 = SMD, >0 = THT
        self.net_name = ""
        self.properties = {
            'width': width,
            'height': height,
            'pad_type': pad_type.value,
            'drill_size': self.drill_size,
            'net_name': '',
            'layer': layer_name
        }
        self.setPos(center)
    
    def boundingRect(self) -> QRectF:
        """Return bounding rectangle"""
        pixel_width = self.width * 3.78
        pixel_height = self.height * 3.78
        return QRectF(-pixel_width/2, -pixel_height/2, pixel_width, pixel_height)
    
    def paint(self, painter: QPainter, option, widget):
        """Paint the pad"""
        # Convert mm to pixels
        pixel_width = self.width * 3.78
        pixel_height = self.height * 3.78
        
        # Pad color
        if self.layer_name == "chip":
            color = QColor(184, 115, 51)  # Copper color
            painter.setBrush(QBrush(color))
        else:
            color = QColor(100, 200, 100)
            painter.setBrush(QBrush(color))
        
        painter.setPen(QPen(color.darker(120), 1))
        
        rect = QRectF(-pixel_width/2, -pixel_height/2, pixel_width, pixel_height)
        
        # Draw based on pad type
        if self.pad_type == PadType.ROUND:
            painter.drawEllipse(rect)
        elif self.pad_type == PadType.SQUARE:
            painter.drawRect(rect)
        elif self.pad_type == PadType.OVAL:
            painter.drawRoundedRect(rect, pixel_width/4, pixel_height/4)
        elif self.pad_type == PadType.ROUNDED_RECT:
            painter.drawRoundedRect(rect, 2, 2)
        elif self.pad_type == PadType.OCTAGON:
            # Draw octagon
            octagon = QPolygonF()
            w, h = pixel_width/2, pixel_height/2
            cut = min(w, h) * 0.3  # 30% corner cut
            octagon << QPointF(-w+cut, -h) << QPointF(w-cut, -h) << QPointF(w, -h+cut)
            octagon << QPointF(w, h-cut) << QPointF(w-cut, h) << QPointF(-w+cut, h)
            octagon << QPointF(-w, h-cut) << QPointF(-w, -h+cut)
            painter.drawPolygon(octagon)
        
        # Draw drill hole if THT
        if self.drill_size > 0:
            drill_pixels = self.drill_size * 3.78
            painter.setBrush(QBrush(QColor(0, 0, 0)))  # Black hole
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            drill_rect = QRectF(-drill_pixels/2, -drill_pixels/2, drill_pixels, drill_pixels)
            painter.drawEllipse(drill_rect)
        
        # Highlight if selected
        if self.isSelected():
            highlight_pen = QPen(QColor(255, 255, 0), 2, Qt.PenStyle.DashLine)
            painter.setPen(highlight_pen)
            painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
            painter.drawRect(rect.adjusted(-2, -2, 2, 2))

class PCBVia(CADGraphicsItem):
    """PCB via item"""
    
    def __init__(self, center: QPointF, outer_dia: float = 0.6, drill_dia: float = 0.3,
                 via_type: ViaType = ViaType.THROUGH, layer_name: str = "chip"):
        super().__init__(layer_name)
        self.cad_type = "via"
        self.center = center
        self.outer_dia = outer_dia  # in mm
        self.drill_dia = drill_dia  # in mm
        self.via_type = via_type
        self.net_name = ""
        self.properties = {
            'outer_dia': outer_dia,
            'drill_dia': drill_dia,
            'via_type': via_type.value,
            'net_name': '',
            'layer': layer_name
        }
        self.setPos(center)
    
    def boundingRect(self) -> QRectF:
        """Return bounding rectangle"""
        pixel_dia = self.outer_dia * 3.78
        return QRectF(-pixel_dia/2, -pixel_dia/2, pixel_dia, pixel_dia)
    
    def paint(self, painter: QPainter, option, widget):
        """Paint the via"""
        outer_pixels = self.outer_dia * 3.78
        drill_pixels = self.drill_dia * 3.78
        
        # Via pad (copper)
        painter.setBrush(QBrush(QColor(184, 115, 51)))  # Copper color
        painter.setPen(QPen(QColor(160, 100, 40), 1))
        outer_rect = QRectF(-outer_pixels/2, -outer_pixels/2, outer_pixels, outer_pixels)
        painter.drawEllipse(outer_rect)
        
        # Drill hole
        painter.setBrush(QBrush(QColor(0, 0, 0)))  # Black hole
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

# === CAD TOOLS WIDGET ===
class CADToolsWidget(QWidget):
    """Electronic CAD tools panel"""
    
    tool_changed = pyqtSignal(CADTool)
    trace_width_changed = pyqtSignal(float)
    pad_size_changed = pyqtSignal(float, float)
    via_size_changed = pyqtSignal(float, float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_tool = CADTool.SELECT
        self.trace_width = 0.2  # mm
        self.pad_width = 1.0   # mm
        self.pad_height = 1.0  # mm
        self.via_outer = 0.6   # mm
        self.via_drill = 0.3   # mm
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        
        # Drawing Tools Group
        tools_group = QGroupBox("CAD Tools")
        tools_layout = QVBoxLayout(tools_group)
        
        # Tool buttons
        self.tool_buttons = QButtonGroup(self)
        
        # Row 1: Basic tools
        row1 = QHBoxLayout()
        self.select_btn = self._create_tool_button("Select", CADTool.SELECT, "🔍")
        self.trace_btn = self._create_tool_button("Trace", CADTool.TRACE, "⚡")
        self.pad_btn = self._create_tool_button("Pad", CADTool.PAD, "⬜")
        self.via_btn = self._create_tool_button("Via", CADTool.VIA, "⚫")
        
        row1.addWidget(self.select_btn)
        row1.addWidget(self.trace_btn)
        row1.addWidget(self.pad_btn)
        row1.addWidget(self.via_btn)
        
        # Row 2: Advanced tools
        row2 = QHBoxLayout()
        self.copper_btn = self._create_tool_button("Copper Fill", CADTool.COPPER_FILL, "🔶")
        self.keepout_btn = self._create_tool_button("Keepout", CADTool.KEEPOUT, "🚫")
        self.silk_btn = self._create_tool_button("Silkscreen", CADTool.SILKSCREEN, "📝")
        self.drill_btn = self._create_tool_button("Drill", CADTool.DRILL, "🕳️")
        
        row2.addWidget(self.copper_btn)
        row2.addWidget(self.keepout_btn)
        row2.addWidget(self.silk_btn)
        row2.addWidget(self.drill_btn)
        
        # Row 3: Shape tools
        row3 = QHBoxLayout()
        self.rect_btn = self._create_tool_button("Rectangle", CADTool.RECTANGLE, "▭")
        self.circle_btn = self._create_tool_button("Circle", CADTool.CIRCLE, "⭕")
        self.poly_btn = self._create_tool_button("Polygon", CADTool.POLYGON, "🔷")
        self.text_btn = self._create_tool_button("Text", CADTool.TEXT, "📄")
        
        row3.addWidget(self.rect_btn)
        row3.addWidget(self.circle_btn)
        row3.addWidget(self.poly_btn)
        row3.addWidget(self.text_btn)
        
        # Row 4: Measurement tools
        row4 = QHBoxLayout()
        self.dim_btn = self._create_tool_button("Dimension", CADTool.DIMENSION, "📏")
        self.ruler_btn = self._create_tool_button("Ruler", CADTool.RULER, "📐")
        row4.addWidget(self.dim_btn)
        row4.addWidget(self.ruler_btn)
        row4.addStretch()
        
        tools_layout.addLayout(row1)
        tools_layout.addLayout(row2)
        tools_layout.addLayout(row3)
        tools_layout.addLayout(row4)
        
        # Tool Properties Group
        props_group = QGroupBox("Tool Properties")
        props_layout = QVBoxLayout(props_group)
        
        # Trace properties
        trace_layout = QHBoxLayout()
        trace_layout.addWidget(QLabel("Trace Width:"))
        self.trace_width_spin = QDoubleSpinBox()
        self.trace_width_spin.setRange(0.1, 10.0)
        self.trace_width_spin.setValue(self.trace_width)
        self.trace_width_spin.setSuffix(" mm")
        self.trace_width_spin.setDecimals(2)
        self.trace_width_spin.valueChanged.connect(self._on_trace_width_changed)
        trace_layout.addWidget(self.trace_width_spin)
        props_layout.addLayout(trace_layout)
        
        # Pad properties
        pad_layout = QHBoxLayout()
        pad_layout.addWidget(QLabel("Pad:"))
        self.pad_width_spin = QDoubleSpinBox()
        self.pad_width_spin.setRange(0.1, 20.0)
        self.pad_width_spin.setValue(self.pad_width)
        self.pad_width_spin.setSuffix(" mm")
        self.pad_width_spin.setDecimals(2)
        self.pad_width_spin.valueChanged.connect(self._on_pad_size_changed)
        
        pad_layout.addWidget(self.pad_width_spin)
        pad_layout.addWidget(QLabel("×"))
        
        self.pad_height_spin = QDoubleSpinBox()
        self.pad_height_spin.setRange(0.1, 20.0)
        self.pad_height_spin.setValue(self.pad_height)
        self.pad_height_spin.setSuffix(" mm")
        self.pad_height_spin.setDecimals(2)
        self.pad_height_spin.valueChanged.connect(self._on_pad_size_changed)
        pad_layout.addWidget(self.pad_height_spin)
        props_layout.addLayout(pad_layout)
        
        # Via properties
        via_layout = QHBoxLayout()
        via_layout.addWidget(QLabel("Via:"))
        self.via_outer_spin = QDoubleSpinBox()
        self.via_outer_spin.setRange(0.1, 5.0)
        self.via_outer_spin.setValue(self.via_outer)
        self.via_outer_spin.setSuffix(" mm")
        self.via_outer_spin.setDecimals(2)
        self.via_outer_spin.valueChanged.connect(self._on_via_size_changed)
        
        via_layout.addWidget(self.via_outer_spin)
        via_layout.addWidget(QLabel("/"))
        
        self.via_drill_spin = QDoubleSpinBox()
        self.via_drill_spin.setRange(0.05, 3.0)
        self.via_drill_spin.setValue(self.via_drill)
        self.via_drill_spin.setSuffix(" mm")
        self.via_drill_spin.setDecimals(2)
        self.via_drill_spin.valueChanged.connect(self._on_via_size_changed)
        via_layout.addWidget(self.via_drill_spin)
        props_layout.addLayout(via_layout)
        
        # Quick Presets
        presets_group = QGroupBox("Quick Presets")
        presets_layout = QVBoxLayout(presets_group)
        
        preset_btn_layout = QHBoxLayout()
        
        fine_btn = QPushButton("Fine (0.1mm)")
        fine_btn.clicked.connect(lambda: self._apply_preset(0.1, 0.8, 0.8, 0.4, 0.2))
        preset_btn_layout.addWidget(fine_btn)
        
        std_btn = QPushButton("Standard (0.2mm)")
        std_btn.clicked.connect(lambda: self._apply_preset(0.2, 1.0, 1.0, 0.6, 0.3))
        preset_btn_layout.addWidget(std_btn)
        
        thick_btn = QPushButton("Thick (0.5mm)")
        thick_btn.clicked.connect(lambda: self._apply_preset(0.5, 2.0, 2.0, 1.0, 0.5))
        preset_btn_layout.addWidget(thick_btn)
        
        presets_layout.addLayout(preset_btn_layout)
        
        # Keyboard shortcuts label
        shortcuts_label = QLabel("""
<b>Keyboard Shortcuts:</b><br>
S - Select tool<br>
T - Trace tool<br>
P - Pad tool<br>
V - Via tool<br>
R - Rectangle tool<br>
C - Circle tool<br>
ESC - Cancel current operation
        """)
        shortcuts_label.setStyleSheet("font-size: 9px; color: #888;")
        
        # Add to main layout
        layout.addWidget(tools_group)
        layout.addWidget(props_group)
        layout.addWidget(presets_group)
        layout.addWidget(shortcuts_label)
        layout.addStretch()
        
        # Set default tool
        self.select_btn.setChecked(True)
    
    def _create_tool_button(self, text: str, tool: CADTool, icon: str) -> QPushButton:
        """Create a tool button"""
        btn = QPushButton(f"{icon}\n{text}")
        btn.setCheckable(True)
        btn.setFixedSize(80, 60)
        btn.clicked.connect(lambda: self._on_tool_selected(tool))
        self.tool_buttons.addButton(btn)
        return btn
    
    def _on_tool_selected(self, tool: CADTool):
        """Handle tool selection"""
        self.current_tool = tool
        self.tool_changed.emit(tool)
        print(f"🔧 CAD Tool selected: {tool.value}")
    
    def _on_trace_width_changed(self, value: float):
        """Handle trace width change"""
        self.trace_width = value
        self.trace_width_changed.emit(value)
    
    def _on_pad_size_changed(self):
        """Handle pad size change"""
        self.pad_width = self.pad_width_spin.value()
        self.pad_height = self.pad_height_spin.value()
        self.pad_size_changed.emit(self.pad_width, self.pad_height)
    
    def _on_via_size_changed(self):
        """Handle via size change"""
        self.via_outer = self.via_outer_spin.value()
        self.via_drill = self.via_drill_spin.value()
        self.via_size_changed.emit(self.via_outer, self.via_drill)
    
    def _apply_preset(self, trace_w: float, pad_w: float, pad_h: float, 
                     via_outer: float, via_drill: float):
        """Apply preset values"""
        self.trace_width_spin.setValue(trace_w)
        self.pad_width_spin.setValue(pad_w)
        self.pad_height_spin.setValue(pad_h)
        self.via_outer_spin.setValue(via_outer)
        self.via_drill_spin.setValue(via_drill)
        print(f"🎯 Applied preset: Trace={trace_w}mm, Pad={pad_w}×{pad_h}mm, Via={via_outer}/{via_drill}mm")

# === ENHANCED CANVAS WITH CAD TOOLS ===
class ElectronicCADCanvas(QGraphicsView):
    """Enhanced canvas with Electronic CAD functionality"""
    
    cad_item_added = pyqtSignal(CADGraphicsItem)
    cad_item_selected = pyqtSignal(CADGraphicsItem)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # CAD state
        self.current_cad_tool = CADTool.SELECT
        self.is_drawing = False
        self.current_trace_points = []
        self.temp_item = None
        
        # CAD properties
        self.trace_width = 0.2  # mm
        self.pad_width = 1.0    # mm
        self.pad_height = 1.0   # mm
        self.via_outer = 0.6    # mm
        self.via_drill = 0.3    # mm
        
        # CAD items storage
        self.cad_items = []
        
        self._setup_canvas()
        print("✅ Electronic CAD Canvas initialized")
    
    def _setup_canvas(self):
        """Setup canvas properties"""
        self.scene.setSceneRect(-3000, -3000, 6000, 6000)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    
    def set_cad_tool(self, tool: CADTool):
        """Set current CAD tool"""
        self.current_cad_tool = tool
        
        # Update cursor based on tool
        if tool == CADTool.SELECT:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        elif tool in [CADTool.TRACE, CADTool.DIMENSION]:
            self.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        elif tool in [CADTool.PAD, CADTool.VIA, CADTool.CIRCLE]:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        
        print(f"🔧 CAD Canvas tool: {tool.value}")
    
    def set_trace_width(self, width: float):
        """Set trace width"""
        self.trace_width = width
    
    def set_pad_size(self, width: float, height: float):
        """Set pad size"""
        self.pad_width = width
        self.pad_height = height
    
    def set_via_size(self, outer: float, drill: float):
        """Set via size"""
        self.via_outer = outer
        self.via_drill = drill
    
    def mousePressEvent(self, event):
        """Handle mouse press for CAD operations"""
        if event.button() == Qt.MouseButton.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            
            if self.current_cad_tool == CADTool.TRACE:
                self._start_trace(scene_pos)
            elif self.current_cad_tool == CADTool.PAD:
                self._place_pad(scene_pos)
            elif self.current_cad_tool == CADTool.VIA:
                self._place_via(scene_pos)
            elif self.current_cad_tool == CADTool.CIRCLE:
                self._start_circle(scene_pos)
            elif self.current_cad_tool == CADTool.RECTANGLE:
                self._start_rectangle(scene_pos)
            else:
                super().mousePressEvent(event)
        elif event.button() == Qt.MouseButton.RightButton:
            # Right click cancels current operation
            self._cancel_current_operation()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for CAD operations"""
        scene_pos = self.mapToScene(event.pos())
        
        if self.is_drawing and self.current_cad_tool == CADTool.TRACE:
            self._update_trace_preview(scene_pos)
        elif self.is_drawing and self.current_cad_tool == CADTool.CIRCLE:
            self._update_circle_preview(scene_pos)
        elif self.is_drawing and self.current_cad_tool == CADTool.RECTANGLE:
            self._update_rectangle_preview(scene_pos)
        
        super().mouseMoveEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """Handle double click to finish operations"""
        if self.current_cad_tool == CADTool.TRACE and self.is_drawing:
            self._finish_trace()
        else:
            super().mouseDoubleClickEvent(event)
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        key = event.key()
        
        # Tool shortcuts
        if key == Qt.Key.Key_S:
            self.set_cad_tool(CADTool.SELECT)
        elif key == Qt.Key.Key_T:
            self.set_cad_tool(CADTool.TRACE)
        elif key == Qt.Key.Key_P:
            self.set_cad_tool(CADTool.PAD)
        elif key == Qt.Key.Key_V:
            self.set_cad_tool(CADTool.VIA)
        elif key == Qt.Key.Key_R:
            self.set_cad_tool(CADTool.RECTANGLE)
        elif key == Qt.Key.Key_C:
            self.set_cad_tool(CADTool.CIRCLE)
        elif key == Qt.Key.Key_Escape:
            self._cancel_current_operation()
        else:
            super().keyPressEvent(event)
    
    # === CAD OPERATION METHODS ===
    
    def _start_trace(self, pos: QPointF):
        """Start drawing a trace"""
        if not self.is_drawing:
            # Start new trace
            self.is_drawing = True
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
        if self.temp_item:
            self.scene.removeItem(self.temp_item)
        
        # Create preview trace
        preview_points = self.current_trace_points + [pos]
        self.temp_item = PCBTrace(preview_points, self.trace_width)
        self.temp_item.setOpacity(0.7)  # Semi-transparent preview
        self.scene.addItem(self.temp_item)
    
    def _finish_trace(self):
        """Finish drawing the current trace"""
        if self.is_drawing and len(self.current_trace_points) >= 2:
            # Remove preview
            if self.temp_item:
                self.scene.removeItem(self.temp_item)
                self.temp_item = None
            
            # Create final trace
            trace = PCBTrace(self.current_trace_points, self.trace_width)
            self.scene.addItem(trace)
            self.cad_items.append(trace)
            self.cad_item_added.emit(trace)
            
            print(f"✅ Finished trace with {len(self.current_trace_points)} points")
        
        # Reset state
        self.is_drawing = False
        self.current_trace_points = []
    
    def _place_pad(self, pos: QPointF):
        """Place a pad at position"""
        pad = PCBPad(pos, self.pad_width, self.pad_height, PadType.ROUND)
        self.scene.addItem(pad)
        self.cad_items.append(pad)
        self.cad_item_added.emit(pad)
        print(f"✅ Placed pad at {pos.x():.1f}, {pos.y():.1f}")
    
    def _place_via(self, pos: QPointF):
        """Place a via at position"""
        via = PCBVia(pos, self.via_outer, self.via_drill, ViaType.THROUGH)
        self.scene.addItem(via)
        self.cad_items.append(via)
        self.cad_item_added.emit(via)
        print(f"✅ Placed via at {pos.x():.1f}, {pos.y():.1f}")
    
    def _start_circle(self, pos: QPointF):
        """Start drawing a circle"""
        self.is_drawing = True
        self.circle_center = pos
        print(f"🔧 Started circle at {pos.x():.1f}, {pos.y():.1f}")
    
    def _update_circle_preview(self, pos: QPointF):
        """Update circle preview"""
        if not hasattr(self, 'circle_center'):
            return
        
        # Remove old preview
        if self.temp_item:
            self.scene.removeItem(self.temp_item)
        
        # Calculate radius
        radius = ((pos.x() - self.circle_center.x())**2 + 
                 (pos.y() - self.circle_center.y())**2)**0.5
        
        # Create preview circle
        self.temp_item = QGraphicsEllipseItem(
            self.circle_center.x() - radius, self.circle_center.y() - radius,
            radius * 2, radius * 2
        )
        self.temp_item.setPen(QPen(QColor(255, 255, 0), 2, Qt.PenStyle.DashLine))
        self.temp_item.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        self.scene.addItem(self.temp_item)
    
    def _start_rectangle(self, pos: QPointF):
        """Start drawing a rectangle"""
        self.is_drawing = True
        self.rect_start = pos
        print(f"🔧 Started rectangle at {pos.x():.1f}, {pos.y():.1f}")
    
    def _update_rectangle_preview(self, pos: QPointF):
        """Update rectangle preview"""
        if not hasattr(self, 'rect_start'):
            return
        
        # Remove old preview
        if self.temp_item:
            self.scene.removeItem(self.temp_item)
        
        # Create preview rectangle
        rect = QRectF(self.rect_start, pos).normalized()
        self.temp_item = QGraphicsRectItem(rect)
        self.temp_item.setPen(QPen(QColor(255, 255, 0), 2, Qt.PenStyle.DashLine))
        self.temp_item.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        self.scene.addItem(self.temp_item)
    
    def _cancel_current_operation(self):
        """Cancel current drawing operation"""
        if self.is_drawing:
            # Remove preview
            if self.temp_item:
                self.scene.removeItem(self.temp_item)
                self.temp_item = None
            
            # Reset state
            self.is_drawing = False
            self.current_trace_points = []
            
            if hasattr(self, 'circle_center'):
                delattr(self, 'circle_center')
            if hasattr(self, 'rect_start'):
                delattr(self, 'rect_start')
            
            print("❌ Cancelled current CAD operation")
    
    def clear_all_cad_items(self):
        """Clear all CAD items from canvas"""
        for item in self.cad_items:
            self.scene.removeItem(item)
        self.cad_items.clear()
        print("🗑️ Cleared all CAD items")
    
    def get_cad_items_data(self) -> List[Dict[str, Any]]:
        """Get CAD items data for saving"""
        data = []
        for item in self.cad_items:
            item_data = {
                'type': item.cad_type,
                'layer': item.layer_name,
                'properties': item.properties.copy()
            }
            
            if isinstance(item, PCBTrace):
                item_data['points'] = [(p.x(), p.y()) for p in item.points]
            elif isinstance(item, (PCBPad, PCBVia)):
                item_data['position'] = (item.center.x(), item.center.y())
            
            data.append(item_data)
        
        return data
    
    def load_cad_items_data(self, data: List[Dict[str, Any]]):
        """Load CAD items from data"""
        self.clear_all_cad_items()
        
        for item_data in data:
            try:
                if item_data['type'] == 'trace':
                    points = [QPointF(x, y) for x, y in item_data['points']]
                    width = item_data['properties'].get('width', 0.2)
                    trace = PCBTrace(points, width, item_data['layer'])
                    self.scene.addItem(trace)
                    self.cad_items.append(trace)
                
                elif item_data['type'] == 'pad':
                    pos = QPointF(*item_data['position'])
                    props = item_data['properties']
                    pad = PCBPad(pos, props.get('width', 1.0), props.get('height', 1.0),
                               PadType(props.get('pad_type', 'round')), item_data['layer'])
                    pad.drill_size = props.get('drill_size', 0.0)
                    self.scene.addItem(pad)
                    self.cad_items.append(pad)
                
                elif item_data['type'] == 'via':
                    pos = QPointF(*item_data['position'])
                    props = item_data['properties']
                    via = PCBVia(pos, props.get('outer_dia', 0.6), props.get('drill_dia', 0.3),
                               ViaType(props.get('via_type', 'through')), item_data['layer'])
                    self.scene.addItem(via)
                    self.cad_items.append(via)
                    
            except Exception as e:
                print(f"⚠️ Error loading CAD item: {e}")
        
        print(f"✅ Loaded {len(self.cad_items)} CAD items")

# === MAIN CAD INTERFACE ===
class ElectronicCADInterface(QWidget):
    """Complete Electronic CAD interface combining tools and canvas"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        print("✅ Electronic CAD Interface initialized")
    
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QHBoxLayout(self)
        
        # CAD Tools Panel (left side)
        self.tools_widget = CADToolsWidget()
        self.tools_widget.setFixedWidth(300)
        layout.addWidget(self.tools_widget)
        
        # CAD Canvas (main area)
        self.canvas = ElectronicCADCanvas()
        layout.addWidget(self.canvas)
        
        # Set proportions
        layout.setStretch(0, 0)  # Tools panel fixed width
        layout.setStretch(1, 1)  # Canvas takes remaining space
    
    def _connect_signals(self):
        """Connect signals between tools and canvas"""
        # Tool changes
        self.tools_widget.tool_changed.connect(self.canvas.set_cad_tool)
        self.tools_widget.trace_width_changed.connect(self.canvas.set_trace_width)
        self.tools_widget.pad_size_changed.connect(self.canvas.set_pad_size)
        self.tools_widget.via_size_changed.connect(self.canvas.set_via_size)
        
        # Canvas events
        self.canvas.cad_item_added.connect(self._on_cad_item_added)
        self.canvas.cad_item_selected.connect(self._on_cad_item_selected)
    
    def _on_cad_item_added(self, item: CADGraphicsItem):
        """Handle CAD item added"""
        print(f"📎 CAD item added: {item.cad_type} on layer {item.layer_name}")
    
    def _on_cad_item_selected(self, item: CADGraphicsItem):
        """Handle CAD item selected"""
        print(f"🎯 CAD item selected: {item.cad_type}")
    
    def get_canvas(self) -> ElectronicCADCanvas:
        """Get the CAD canvas"""
        return self.canvas
    
    def get_tools_widget(self) -> CADToolsWidget:
        """Get the tools widget"""
        return self.tools_widget

# === INTEGRATION FUNCTIONS ===
def integrate_cad_with_existing_canvas(existing_canvas):
    """Integrate CAD tools with existing canvas"""
    print("🔧 Integrating Electronic CAD tools with existing canvas...")
    
    # Add CAD functionality to existing canvas
    if hasattr(existing_canvas, 'scene'):
        # Copy CAD methods to existing canvas
        existing_canvas.cad_items = []
        existing_canvas.current_cad_tool = CADTool.SELECT
        existing_canvas.is_drawing = False
        existing_canvas.current_trace_points = []
        existing_canvas.temp_item = None
        
        # Copy CAD properties
        existing_canvas.trace_width = 0.2
        existing_canvas.pad_width = 1.0
        existing_canvas.pad_height = 1.0
        existing_canvas.via_outer = 0.6
        existing_canvas.via_drill = 0.3
        
        # Add CAD methods
        existing_canvas.set_cad_tool = ElectronicCADCanvas.set_cad_tool.__get__(existing_canvas)
        existing_canvas.set_trace_width = ElectronicCADCanvas.set_trace_width.__get__(existing_canvas)
        existing_canvas.set_pad_size = ElectronicCADCanvas.set_pad_size.__get__(existing_canvas)
        existing_canvas.set_via_size = ElectronicCADCanvas.set_via_size.__get__(existing_canvas)
        existing_canvas._start_trace = ElectronicCADCanvas._start_trace.__get__(existing_canvas)
        existing_canvas._place_pad = ElectronicCADCanvas._place_pad.__get__(existing_canvas)
        existing_canvas._place_via = ElectronicCADCanvas._place_via.__get__(existing_canvas)
        existing_canvas._cancel_current_operation = ElectronicCADCanvas._cancel_current_operation.__get__(existing_canvas)
        existing_canvas.clear_all_cad_items = ElectronicCADCanvas.clear_all_cad_items.__get__(existing_canvas)
        existing_canvas.get_cad_items_data = ElectronicCADCanvas.get_cad_items_data.__get__(existing_canvas)
        existing_canvas.load_cad_items_data = ElectronicCADCanvas.load_cad_items_data.__get__(existing_canvas)
        
        print("✅ Successfully integrated CAD tools with existing canvas")
        return True
    else:
        print("❌ Cannot integrate - existing canvas missing scene")
        return False

# Export main classes
__all__ = [
    'CADTool', 'TraceStyle', 'PadType', 'ViaType',
    'PCBTrace', 'PCBPad', 'PCBVia', 'CADGraphicsItem',
    'CADToolsWidget', 'ElectronicCADCanvas', 'ElectronicCADInterface',
    'integrate_cad_with_existing_canvas'
]
