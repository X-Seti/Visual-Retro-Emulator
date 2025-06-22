#!/usr/bin/env python3
"""
X-Seti - June22 2025 - CAD Tools Panel - Complete Merged Version
Full CAD tools panel with all features from both versions merged
"""
#this belongs in ui/ cad_tools_panel.py

import sys
from enum import Enum

# Check PyQt6 availability
try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                               QPushButton, QButtonGroup, QComboBox, QDoubleSpinBox, 
                               QLabel, QGridLayout, QSpinBox, QCheckBox)
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QIcon
    PYQT6_AVAILABLE = True
    print("✓ PyQt6 imports successful for CAD Tools Panel")
except ImportError as e:
    print(f"❌ PyQt6 import failed in CAD Tools Panel: {e}")
    PYQT6_AVAILABLE = False

# Fallback enums if canvas import fails
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

# Try to import from canvas, use fallbacks if needed
try:
    from .canvas import CADTool as CanvasCADTool, TraceStyle as CanvasTraceStyle
    CADTool = CanvasCADTool
    TraceStyle = CanvasTraceStyle
    print("✓ CAD enums imported from canvas")
except ImportError:
    print("⚠️ Using fallback CAD enums - canvas not available")

if PYQT6_AVAILABLE:
    class CADToolsPanel(QWidget):
        """Complete CAD tools panel with all features merged"""
        
        # Signals
        tool_changed = pyqtSignal(object)
        trace_width_changed = pyqtSignal(float)
        trace_style_changed = pyqtSignal(object)
        pad_size_changed = pyqtSignal(float, float)
        pad_type_changed = pyqtSignal(object)
        via_size_changed = pyqtSignal(float, float)
        via_type_changed = pyqtSignal(object)
        layer_changed = pyqtSignal(str)
        
        def __init__(self, parent=None):
            super().__init__(parent)
            
            # Current settings
            self.current_tool = CADTool.SELECT
            self.trace_width = 0.2
            self.trace_style = TraceStyle.SOLID
            self.pad_width = 1.0
            self.pad_height = 1.0
            self.pad_type = PadType.ROUND
            self.via_outer = 0.6
            self.via_drill = 0.3
            self.via_type = ViaType.THROUGH
            self.canvas = None
            
            self._setup_ui()
            self._connect_signals()
            
            print("✅ Complete CAD Tools Panel initialized")
        
        def _setup_ui(self):
            """Setup the complete user interface"""
            layout = QVBoxLayout(self)
            layout.setSpacing(8)
            layout.setContentsMargins(8, 8, 8, 8)
            
            # === CAD TOOLS GROUP ===
            tools_group = self._create_tools_group()
            
            # === LAYER SELECTION ===
            layer_group = self._create_layer_group()
            
            # === TRACE PROPERTIES ===
            trace_group = self._create_trace_group()
            
            # === PAD PROPERTIES ===
            pad_group = self._create_pad_group()
            
            # === VIA PROPERTIES ===
            via_group = self._create_via_group()
            
            # === PRESETS ===
            presets_group = self._create_presets_group()
            
            # === SHORTCUTS INFO ===
            shortcuts_label = QLabel("""
<b>🎹 Shortcuts:</b><br>
<b>S</b>-Select <b>T</b>-Trace <b>P</b>-Pad <b>V</b>-Via<br>
<b>R</b>-Rect <b>C</b>-Circle <b>ESC</b>-Cancel<br>
<b>F</b>-Fill <b>K</b>-Keepout <b>Double-Click</b>-Finish<br>
<b>Trace Widths:</b> 0.05mm - 50mm supported
            """.strip())
            shortcuts_label.setStyleSheet("color: #666; font-size: 9px; padding: 4px;")
            
            # Add all groups to layout
            layout.addWidget(tools_group)
            layout.addWidget(layer_group)
            layout.addWidget(trace_group)
            layout.addWidget(pad_group)
            layout.addWidget(via_group)
            layout.addWidget(presets_group)
            layout.addWidget(shortcuts_label)
            layout.addStretch()
        
        def _create_tools_group(self):
            """Create tools selection group with all 14 tools"""
            group = QGroupBox("🔧 CAD Tools")
            layout = QGridLayout(group)
            
            # Create button group for exclusive selection
            self.tool_buttons = QButtonGroup(self)
            
            # Define all 14 tools with their icons/labels
            tools = [
                (CADTool.SELECT, "Select", "🔍", 0, 0),
                (CADTool.TRACE, "Trace", "📏", 0, 1),
                (CADTool.PAD, "Pad", "🔘", 0, 2),
                (CADTool.VIA, "Via", "⚫", 1, 0),
                (CADTool.COPPER_FILL, "Fill", "🟢", 1, 1),
                (CADTool.KEEPOUT, "Keep", "⛔", 1, 2),
                (CADTool.SILKSCREEN, "Silk", "🖨️", 2, 0),
                (CADTool.DRILL, "Drill", "🔩", 2, 1),
                (CADTool.RECTANGLE, "Rect", "▭", 2, 2),
                (CADTool.CIRCLE, "Circle", "●", 3, 0),
                (CADTool.POLYGON, "Poly", "🔶", 3, 1),
                (CADTool.TEXT, "Text", "🆃", 3, 2),
                (CADTool.DIMENSION, "Dim", "📐", 4, 0),
                (CADTool.RULER, "Rule", "📏", 4, 1)
            ]
            
            # Create buttons and store references
            self.tool_button_map = {}
            
            for tool, name, icon, row, col in tools:
                btn = QPushButton(f"{icon}\n{name}")
                btn.setCheckable(True)
                btn.setMinimumSize(60, 50)
                btn.setMaximumSize(60, 50)
                
                # Store button reference with conventional naming
                attr_name = f"{tool.value}_btn"
                setattr(self, attr_name, btn)
                self.tool_button_map[tool] = btn
                
                self.tool_buttons.addButton(btn)
                layout.addWidget(btn, row, col)
            
            # Select default tool
            self.select_btn.setChecked(True)
            
            return group
        
        def _create_layer_group(self):
            """Create layer selection group"""
            group = QGroupBox("📋 Layer")
            layout = QHBoxLayout(group)
            
            self.layer_combo = QComboBox()
            self.layer_combo.addItems(["Chip", "PCB", "Gerber"])
            self.layer_combo.setCurrentText("PCB")
            layout.addWidget(self.layer_combo)
            
            return group
        
        def _create_trace_group(self):
            """Create trace properties group"""
            group = QGroupBox("📏 Trace Properties")
            layout = QGridLayout(group)
            
            # Trace width
            layout.addWidget(QLabel("Width:"), 0, 0)
            self.trace_width_spin = QDoubleSpinBox()
            self.trace_width_spin.setRange(0.05, 50.0)  # Extended range: 0.05mm to 50mm
            self.trace_width_spin.setValue(self.trace_width)
            self.trace_width_spin.setSuffix(" mm")
            self.trace_width_spin.setDecimals(2)
            self.trace_width_spin.setSingleStep(0.1)  # 0.1mm increments
            layout.addWidget(self.trace_width_spin, 0, 1)
            
            # Trace style
            layout.addWidget(QLabel("Style:"), 1, 0)
            self.trace_style_combo = QComboBox()
            self.trace_style_combo.addItems([style.value.title() for style in TraceStyle])
            layout.addWidget(self.trace_style_combo, 1, 1)
            
            return group
        
        def _create_pad_group(self):
            """Create pad properties group"""
            group = QGroupBox("🔘 Pad Properties")
            layout = QGridLayout(group)
            
            # Pad width
            layout.addWidget(QLabel("Width:"), 0, 0)
            self.pad_width_spin = QDoubleSpinBox()
            self.pad_width_spin.setRange(0.1, 20.0)
            self.pad_width_spin.setValue(self.pad_width)
            self.pad_width_spin.setSuffix(" mm")
            layout.addWidget(self.pad_width_spin, 0, 1)
            
            # Pad height
            layout.addWidget(QLabel("Height:"), 1, 0)
            self.pad_height_spin = QDoubleSpinBox()
            self.pad_height_spin.setRange(0.1, 20.0)
            self.pad_height_spin.setValue(self.pad_height)
            self.pad_height_spin.setSuffix(" mm")
            layout.addWidget(self.pad_height_spin, 1, 1)
            
            # Pad type
            layout.addWidget(QLabel("Type:"), 2, 0)
            self.pad_type_combo = QComboBox()
            self.pad_type_combo.addItems([ptype.value.replace('_', ' ').title() for ptype in PadType])
            layout.addWidget(self.pad_type_combo, 2, 1)
            
            return group
        
        def _create_via_group(self):
            """Create via properties group"""
            group = QGroupBox("⚫ Via Properties")
            layout = QGridLayout(group)
            
            # Via outer diameter
            layout.addWidget(QLabel("Outer:"), 0, 0)
            self.via_outer_spin = QDoubleSpinBox()
            self.via_outer_spin.setRange(0.1, 5.0)
            self.via_outer_spin.setValue(self.via_outer)
            self.via_outer_spin.setSuffix(" mm")
            layout.addWidget(self.via_outer_spin, 0, 1)
            
            # Via drill diameter
            layout.addWidget(QLabel("Drill:"), 1, 0)
            self.via_drill_spin = QDoubleSpinBox()
            self.via_drill_spin.setRange(0.05, 3.0)
            self.via_drill_spin.setValue(self.via_drill)
            self.via_drill_spin.setSuffix(" mm")
            layout.addWidget(self.via_drill_spin, 1, 1)
            
            # Via type
            layout.addWidget(QLabel("Type:"), 2, 0)
            self.via_type_combo = QComboBox()
            self.via_type_combo.addItems([vtype.value.title() for vtype in ViaType])
            layout.addWidget(self.via_type_combo, 2, 1)
            
            return group
        
        def _create_presets_group(self):
            """Create presets group"""
            group = QGroupBox("⚡ Quick Presets")
            layout = QGridLayout(group)
            
            presets = [
                ("Fine", 0.1, 0.8, 0.8, 0.4, 0.2),
                ("Normal", 0.2, 1.0, 1.0, 0.6, 0.3),
                ("Thick", 0.5, 1.5, 1.5, 1.0, 0.5),
                ("Power", 2.0, 2.5, 2.5, 1.5, 0.8),
                ("Heavy", 5.0, 3.0, 3.0, 2.0, 1.0),
                ("Bus", 10.0, 4.0, 4.0, 2.5, 1.2)
            ]
            
            for i, (name, trace_w, pad_w, pad_h, via_outer, via_drill) in enumerate(presets):
                btn = QPushButton(name)
                btn.setToolTip(f"Trace: {trace_w}mm, Pad: {pad_w}×{pad_h}mm")
                btn.clicked.connect(lambda checked, tw=trace_w, pw=pad_w, ph=pad_h, vo=via_outer, vd=via_drill: 
                                  self._apply_preset(tw, pw, ph, vo, vd))
                layout.addWidget(btn, i // 2, i % 2)
            
            return group
        
        def _connect_signals(self):
            """Connect all UI signals"""
            self.tool_buttons.buttonClicked.connect(self._on_tool_clicked)
            self.layer_combo.currentTextChanged.connect(self._on_layer_changed)
            self.trace_width_spin.valueChanged.connect(self._on_trace_width_changed)
            self.trace_style_combo.currentTextChanged.connect(self._on_trace_style_changed)
            self.pad_width_spin.valueChanged.connect(self._on_pad_size_changed)
            self.pad_height_spin.valueChanged.connect(self._on_pad_size_changed)
            self.pad_type_combo.currentTextChanged.connect(self._on_pad_type_changed)
            self.via_outer_spin.valueChanged.connect(self._on_via_size_changed)
            self.via_drill_spin.valueChanged.connect(self._on_via_size_changed)
            self.via_type_combo.currentTextChanged.connect(self._on_via_type_changed)
        
        def _on_tool_clicked(self, button):
            """Handle tool button click"""
            # Find which tool this button represents
            for tool, btn in self.tool_button_map.items():
                if btn == button:
                    self.current_tool = tool
                    self.tool_changed.emit(self.current_tool)
                    print(f"🔧 CAD Tool: {self.current_tool.value}")
                    break
        
        def _on_layer_changed(self, layer_name):
            """Handle layer change"""
            self.layer_changed.emit(layer_name.lower())
            print(f"📋 Layer: {layer_name}")
        
        def _on_trace_width_changed(self, value):
            """Handle trace width change"""
            self.trace_width = value
            self.trace_width_changed.emit(value)
        
        def _on_trace_style_changed(self, style_name):
            """Handle trace style change"""
            try:
                self.trace_style = TraceStyle(style_name.lower())
                self.trace_style_changed.emit(self.trace_style)
            except ValueError:
                pass
        
        def _on_pad_size_changed(self):
            """Handle pad size change"""
            self.pad_width = self.pad_width_spin.value()
            self.pad_height = self.pad_height_spin.value()
            self.pad_size_changed.emit(self.pad_width, self.pad_height)
        
        def _on_pad_type_changed(self, type_name):
            """Handle pad type change"""
            try:
                type_value = type_name.lower().replace(' ', '_')
                self.pad_type = PadType(type_value)
                self.pad_type_changed.emit(self.pad_type)
            except ValueError:
                pass
        
        def _on_via_size_changed(self):
            """Handle via size change"""
            self.via_outer = self.via_outer_spin.value()
            self.via_drill = self.via_drill_spin.value()
            self.via_size_changed.emit(self.via_outer, self.via_drill)
        
        def _on_via_type_changed(self, type_name):
            """Handle via type change"""
            try:
                self.via_type = ViaType(type_name.lower())
                self.via_type_changed.emit(self.via_type)
            except ValueError:
                pass
        
        def _apply_preset(self, trace_w, pad_w, pad_h, via_outer, via_drill):
            """Apply preset values"""
            self.trace_width_spin.setValue(trace_w)
            self.pad_width_spin.setValue(pad_w)
            self.pad_height_spin.setValue(pad_h)
            self.via_outer_spin.setValue(via_outer)
            self.via_drill_spin.setValue(via_drill)
            print(f"🎯 Preset applied: {trace_w}mm trace")
        
        def set_canvas(self, canvas):
            """Connect to canvas"""
            self.canvas = canvas
            if canvas and hasattr(canvas, 'set_cad_tool'):
                # Connect signals to canvas
                self.tool_changed.connect(canvas.set_cad_tool)
                self.trace_width_changed.connect(canvas.set_trace_width)
                self.trace_style_changed.connect(getattr(canvas, 'set_trace_style', lambda x: None))
                self.pad_size_changed.connect(canvas.set_pad_size)
                self.pad_type_changed.connect(getattr(canvas, 'set_pad_type', lambda x: None))
                self.via_size_changed.connect(canvas.set_via_size)
                self.via_type_changed.connect(getattr(canvas, 'set_via_type', lambda x: None))
                self.layer_changed.connect(getattr(canvas, 'set_active_layer', lambda x: None))
                print("✅ CAD Tools connected to canvas")
            else:
                print("⚠️ Canvas connection: fallback mode")
        
        def select_tool(self, tool):
            """Programmatically select a tool"""
            if tool in self.tool_button_map:
                self.tool_button_map[tool].setChecked(True)
                self.current_tool = tool
                self.tool_changed.emit(tool)
        
        def get_current_settings(self) -> dict:
            """Get current CAD tool settings"""
            return {
                'tool': self.current_tool,
                'trace_width': self.trace_width,
                'trace_style': self.trace_style,
                'pad_width': self.pad_width,
                'pad_height': self.pad_height,
                'pad_type': self.pad_type,
                'via_outer': self.via_outer,
                'via_drill': self.via_drill,
                'via_type': self.via_type,
                'active_layer': self.layer_combo.currentText().lower()
            }
        
        def load_settings(self, settings: dict):
            """Load CAD tool settings"""
            try:
                if 'tool' in settings:
                    self.select_tool(settings['tool'])
                if 'trace_width' in settings:
                    self.trace_width_spin.setValue(settings['trace_width'])
                if 'trace_style' in settings:
                    style_name = settings['trace_style'].value if hasattr(settings['trace_style'], 'value') else str(settings['trace_style'])
                    index = self.trace_style_combo.findText(style_name.title())
                    if index >= 0:
                        self.trace_style_combo.setCurrentIndex(index)
                if 'pad_width' in settings:
                    self.pad_width_spin.setValue(settings['pad_width'])
                if 'pad_height' in settings:
                    self.pad_height_spin.setValue(settings['pad_height'])
                if 'pad_type' in settings:
                    type_name = settings['pad_type'].value if hasattr(settings['pad_type'], 'value') else str(settings['pad_type'])
                    display_name = type_name.replace('_', ' ').title()
                    index = self.pad_type_combo.findText(display_name)
                    if index >= 0:
                        self.pad_type_combo.setCurrentIndex(index)
                if 'via_outer' in settings:
                    self.via_outer_spin.setValue(settings['via_outer'])
                if 'via_drill' in settings:
                    self.via_drill_spin.setValue(settings['via_drill'])
                if 'via_type' in settings:
                    type_name = settings['via_type'].value if hasattr(settings['via_type'], 'value') else str(settings['via_type'])
                    index = self.via_type_combo.findText(type_name.title())
                    if index >= 0:
                        self.via_type_combo.setCurrentIndex(index)
                if 'active_layer' in settings:
                    layer_name = settings['active_layer'].title()
                    if layer_name in ['Chip', 'Pcb', 'Gerber']:
                        self.layer_combo.setCurrentText(layer_name)
                
                print("✅ CAD settings loaded")
            except Exception as e:
                print(f"⚠️ Error loading CAD settings: {e}")

else:
    # Fallback class when PyQt6 is not available
    class CADToolsPanel:
        """Fallback CAD Tools Panel when PyQt6 is not available"""
        
        def __init__(self, parent=None):
            self.current_tool = CADTool.SELECT
            self.canvas = None
            print("⚠️ CAD Tools Panel: PyQt6 not available, using minimal fallback")
        
        def set_canvas(self, canvas):
            self.canvas = canvas
            print("⚠️ Fallback CAD Tools Panel: canvas set")
        
        def select_tool(self, tool):
            self.current_tool = tool
            print(f"⚠️ Fallback CAD Tools Panel: tool {tool}")
        
        def get_current_settings(self):
            return {'tool': self.current_tool}
        
        def load_settings(self, settings):
            pass

# Export
__all__ = ['CADToolsPanel', 'CADTool', 'TraceStyle', 'PadType', 'ViaType']

# Test function for standalone testing
def test_cad_tools_panel():
    """Test the CAD tools panel"""
    if PYQT6_AVAILABLE:
        from PyQt6.QtWidgets import QApplication
        import sys
        
        app = QApplication(sys.argv)
        panel = CADToolsPanel()
        panel.show()
        
        print("🧪 CAD Tools Panel test - close window to continue")
        app.exec()
        print("✅ CAD Tools Panel test completed")
    else:
        print("⚠️ Cannot test - PyQt6 not available")

# Test import on module load
try:
    if PYQT6_AVAILABLE:
        print("✅ Complete CAD Tools Panel module loaded successfully")
    else:
        print("⚠️ CAD Tools Panel module loaded with fallbacks")
except Exception as e:
    print(f"❌ CAD Tools Panel module error: {e}")

if __name__ == "__main__":
    test_cad_tools_panel()
