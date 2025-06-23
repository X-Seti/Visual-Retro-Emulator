# X-Seti - June23 2025 - Simple Working CAD Tools Panel
# this belongs in ui/cad_tools_working.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                           QPushButton, QButtonGroup, QComboBox, QDoubleSpinBox, 
                           QLabel, QGridLayout, QSpinBox, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from enum import Enum

# Simple CAD Tool definitions
class CADTool(Enum):
    SELECT = "select"
    TRACE = "trace"
    PAD = "pad"
    VIA = "via"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    TEXT = "text"
    MEASURE = "measure"

class SimpleCADToolsPanel(QWidget):
    """Simple working CAD tools panel without emoji dependencies"""
    
    # Signals
    tool_changed = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_tool = CADTool.SELECT
        self.canvas = None
        
        self._setup_ui()
        self._connect_signals()
        
        print("✅ Simple CAD Tools Panel initialized")
    
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Tool selection group
        tools_group = self._create_tools_group()
        layout.addWidget(tools_group)
        
        # Settings group
        settings_group = self._create_settings_group()
        layout.addWidget(settings_group)
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; font-size: 10px; padding: 4px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def _create_tools_group(self):
        """Create tools selection group"""
        group = QGroupBox("CAD Tools")
        layout = QGridLayout(group)
        
        # Create button group for exclusive selection
        self.tool_buttons = QButtonGroup(self)
        
        # Define tools with simple text labels (no emoji)
        tools = [
            (CADTool.SELECT, "Select", "SEL", 0, 0),
            (CADTool.TRACE, "Trace", "TRC", 0, 1),
            (CADTool.PAD, "Pad", "PAD", 1, 0),
            (CADTool.VIA, "Via", "VIA", 1, 1),
            (CADTool.RECTANGLE, "Rectangle", "RCT", 2, 0),
            (CADTool.CIRCLE, "Circle", "CRC", 2, 1),
            (CADTool.TEXT, "Text", "TXT", 3, 0),
            (CADTool.MEASURE, "Measure", "MSR", 3, 1)
        ]
        
        # Create buttons
        self.tool_button_map = {}
        
        for tool, name, short, row, col in tools:
            btn = QPushButton(f"{short}\n{name}")
            btn.setCheckable(True)
            btn.setMinimumSize(60, 50)
            btn.setMaximumSize(60, 50)
            btn.clicked.connect(lambda checked, t=tool: self._on_tool_selected(t))
            
            # Store button reference
            self.tool_button_map[tool] = btn
            self.tool_buttons.addButton(btn)
            layout.addWidget(btn, row, col)
        
        # Select default tool
        self.tool_button_map[CADTool.SELECT].setChecked(True)
        
        return group
    
    def _create_settings_group(self):
        """Create settings group"""
        group = QGroupBox("Settings")
        layout = QVBoxLayout(group)
        
        # Trace width
        trace_layout = QHBoxLayout()
        trace_layout.addWidget(QLabel("Trace Width:"))
        self.trace_width_spin = QDoubleSpinBox()
        self.trace_width_spin.setRange(0.05, 10.0)
        self.trace_width_spin.setValue(0.2)
        self.trace_width_spin.setSuffix(" mm")
        self.trace_width_spin.setDecimals(2)
        trace_layout.addWidget(self.trace_width_spin)
        layout.addLayout(trace_layout)
        
        # Grid settings
        grid_layout = QHBoxLayout()
        self.grid_check = QCheckBox("Show Grid")
        self.grid_check.setChecked(True)
        grid_layout.addWidget(self.grid_check)
        
        self.snap_check = QCheckBox("Snap to Grid")
        self.snap_check.setChecked(True)
        grid_layout.addWidget(self.snap_check)
        layout.addLayout(grid_layout)
        
        # Layer selection
        layer_layout = QHBoxLayout()
        layer_layout.addWidget(QLabel("Layer:"))
        self.layer_combo = QComboBox()
        self.layer_combo.addItems(["Top Copper", "Bottom Copper", "Silkscreen"])
        self.layer_combo.setCurrentText("Top Copper")
        layer_layout.addWidget(self.layer_combo)
        layout.addLayout(layer_layout)
        
        return group
    
    def _connect_signals(self):
        """Connect signals"""
        self.trace_width_spin.valueChanged.connect(self._on_trace_width_changed)
        self.grid_check.toggled.connect(self._on_grid_toggled)
        self.snap_check.toggled.connect(self._on_snap_toggled)
        self.layer_combo.currentTextChanged.connect(self._on_layer_changed)
    
    def _on_tool_selected(self, tool):
        """Handle tool selection"""
        self.current_tool = tool
        self.status_label.setText(f"Tool: {tool.value.title()}")
        self.tool_changed.emit(tool)
        
        # Update canvas tool if canvas is connected
        if self.canvas and hasattr(self.canvas, 'set_tool'):
            self.canvas.set_tool(tool.value)
        
        print(f"🔧 CAD Tool selected: {tool.value}")
    
    def _on_trace_width_changed(self, value):
        """Handle trace width change"""
        if self.canvas and hasattr(self.canvas, 'set_trace_width'):
            self.canvas.set_trace_width(value)
        print(f"📏 Trace width: {value}mm")
    
    def _on_grid_toggled(self, enabled):
        """Handle grid toggle"""
        if self.canvas and hasattr(self.canvas, 'set_grid_visible'):
            self.canvas.set_grid_visible(enabled)
        print(f"🔲 Grid: {'ON' if enabled else 'OFF'}")
    
    def _on_snap_toggled(self, enabled):
        """Handle snap toggle"""
        if self.canvas and hasattr(self.canvas, 'set_snap_to_grid'):
            self.canvas.set_snap_to_grid(enabled)
        print(f"🧲 Snap: {'ON' if enabled else 'OFF'}")
    
    def _on_layer_changed(self, layer):
        """Handle layer change"""
        if self.canvas and hasattr(self.canvas, 'set_layer'):
            self.canvas.set_layer(layer)
        print(f"📋 Layer: {layer}")
    
    def set_canvas(self, canvas):
        """Connect canvas to CAD tools"""
        self.canvas = canvas
        print("✅ Canvas connected to CAD tools")
        
        # Set initial tool
        if hasattr(canvas, 'set_tool'):
            canvas.set_tool(self.current_tool.value)
    
    def get_current_tool(self):
        """Get currently selected tool"""
        return self.current_tool
    
    def select_tool(self, tool):
        """Programmatically select a tool"""
        if tool in self.tool_button_map:
            self.tool_button_map[tool].setChecked(True)
            self._on_tool_selected(tool)


# Integration helper
def replace_cad_tools_in_main_window(main_window):
    """Replace existing CAD tools with simple working version"""
    try:
        # Remove existing CAD tools dock if it exists
        if hasattr(main_window, 'cad_tools_dock'):
            main_window.removeDockWidget(main_window.cad_tools_dock)
            print("🗑️ Removed old CAD tools dock")
        
        # Create new simple CAD tools
        simple_cad_tools = SimpleCADToolsPanel()
        
        # Connect to canvas if available
        if hasattr(main_window, 'canvas') and main_window.canvas:
            simple_cad_tools.set_canvas(main_window.canvas)
        
        # Create new dock widget
        from PyQt6.QtWidgets import QDockWidget
        from PyQt6.QtCore import Qt
        
        cad_dock = QDockWidget("CAD Tools", main_window)
        cad_dock.setWidget(simple_cad_tools)
        cad_dock.setMinimumWidth(200)
        cad_dock.setMaximumWidth(280)
        
        # Add to main window
        main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, cad_dock)
        
        # Store references
        main_window.cad_tools_dock = cad_dock
        main_window.cad_tools_panel = simple_cad_tools
        
        print("✅ Simple CAD tools successfully integrated")
        return True
        
    except Exception as e:
        print(f"❌ Failed to integrate simple CAD tools: {e}")
        return False


# Export
__all__ = ['SimpleCADToolsPanel', 'CADTool', 'replace_cad_tools_in_main_window']
