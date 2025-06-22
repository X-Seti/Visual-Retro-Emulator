#!/usr/bin/env python3
"""
X-Seti - June22 2025 - CAD Tools Integration Guide
How to add Electronic CAD tools to X-Seti main window
"""

def integrate_cad_tools_to_main_window():
    """
    Add this code to ui/main_window.py in the _create_layout method
    """
    
    # In ui/main_window.py, add this import at the top:
    from .cad_tools_panel import CADToolsPanel
    
    # In the _create_layout method, add CAD tools panel:
    def _create_layout_with_cad_tools(self):
        """Create main window layout with CAD tools"""
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # === LEFT SIDE: Component Palette (existing) ===
        try:
            from .component_palette import EnhancedComponentPalette
            self.component_palette = EnhancedComponentPalette()
            component_dock = QDockWidget("Components", self)
            component_dock.setWidget(self.component_palette)
            component_dock.setFixedWidth(300)
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, component_dock)
        except ImportError:
            print("⚠️ Component palette not available")
        
        # === CENTER: Canvas (existing) ===
        try:
            from .canvas import EnhancedPCBCanvas
            self.canvas = EnhancedPCBCanvas()
            main_layout.addWidget(self.canvas)
        except ImportError:
            print("❌ Canvas not available")
            return
        
        # === RIGHT SIDE: Add CAD Tools Panel ===
        # NEW: CAD Tools Panel
        self.cad_tools_panel = CADToolsPanel()
        self.cad_tools_panel.set_canvas(self.canvas)  # Connect to canvas
        
        cad_tools_dock = QDockWidget("CAD Tools", self)
        cad_tools_dock.setWidget(self.cad_tools_panel)
        cad_tools_dock.setFixedWidth(320)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, cad_tools_dock)
        
        # === BOTTOM: Properties Panel (existing) ===
        try:
            from .properties_panel import PropertiesPanel
            self.properties_panel = PropertiesPanel()
            props_dock = QDockWidget("Properties", self)
            props_dock.setWidget(self.properties_panel)
            props_dock.setMaximumHeight(200)
            self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, props_dock)
        except ImportError:
            print("⚠️ Properties panel not available")
        
        print("✅ CAD Tools integrated into main window")

# === METHOD 2: Quick Test Integration ===

def quick_cad_tools_test():
    """
    Quick standalone test of CAD tools
    Save as: test_cad_tools.py and run: python test_cad_tools.py
    """
    
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
    from ui.canvas import EnhancedPCBCanvas
    from ui.cad_tools_panel import CADToolsPanel
    
    class CADTestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("X-Seti CAD Tools Test")
            self.setGeometry(100, 100, 1200, 800)
            
            #
