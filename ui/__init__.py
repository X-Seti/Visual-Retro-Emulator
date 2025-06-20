#!/usr/bin/env python3
"""
X-Seti - June17 2025 - UI Package - Visual Retro Emulator
Contains all user interface components including CAD tools with robust error handling
"""

#this belongs in ui/__init__.py
import sys
import os

# Try to import main components with fallbacks
MainWindow = None
try:
    from .main_window import MainWindow, EnhancedMainWindow, FixedMainWindow
    #from .fallback_window import MainWindow, EnhancedMainWindow, FixedMainWindow
    print("✓ MainWindow imported from ui.main_window")
except ImportError as e:
    print(f"⚠️ Could not import MainWindow from ui.main_window: {e}")
    try:
        # Try importing from the current directory
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        from main_window import MainWindow
        print("✓ MainWindow imported from main_window")
    except ImportError as e2:
        print(f"⚠️ Could not import MainWindow from main_window: {e2}")
        MainWindow = None

# Canvas components
EnhancedPCBCanvas = None
PCBCanvas = None
try:
    from .canvas import EnhancedPCBCanvas, PCBCanvas
    print("✓ Canvas components imported")
except ImportError as e:
    print(f"⚠️ Could not import Canvas components: {e}")
    EnhancedPCBCanvas = None
    PCBCanvas = None

# CAD Tools Panel - NEW!
CADToolsPanel = None
try:
    from .cad_tools_panel import CADToolsPanel
    print("✓ CAD Tools Panel imported")
except ImportError as e:
    print(f"⚠️ Could not import CAD Tools Panel: {e}")
    print(f"   Make sure ui/cad_tools_panel.py exists")
    CADToolsPanel = None

# Enhanced Chip Renderer - NEW!
ChipRenderer = None
EnhancedChipGraphicsItem = None
try:
    from .enhanced_chip_renderer import ChipRenderer, EnhancedChipGraphicsItem
    print("✓ Enhanced Chip Renderer imported")
except ImportError as e:
    print(f"⚠️ Could not import Enhanced Chip Renderer: {e}")
    ChipRenderer = None
    EnhancedChipGraphicsItem = None

# Component Palette
EnhancedComponentPalette = None
try:
    from .component_palette import EnhancedComponentPalette
    print("✓ ComponentPalette imported")
except ImportError as e:
    print(f"⚠️ Could not import ComponentPalette: {e}")
    EnhancedComponentPalette = None

# Status Bar Manager
StatusBarManager = None
try:
    from .status_bar import StatusBarManager
    print("✓ StatusBar imported")
except ImportError as e:
    print(f"⚠️ Could not import StatusBar: {e}")
    StatusBarManager = None

# Menu Bar Manager
MenuBarManager = None
try:
    from .menu_bar import MenuBarManager
    print("✓ MenuBar imported")
except ImportError as e:
    print(f"⚠️ Could not import MenuBar: {e}")
    MenuBarManager = None

# Properties Panel
PropertiesPanel = None
try:
    from .properties_panel import PropertiesPanel
    print("✓ PropertiesPanel imported")
except ImportError as e:
    print(f"⚠️ Could not import PropertiesPanel: {e}")
    PropertiesPanel = None

# Layer Controls
LayerControls = None
try:
    from .layer_controls import LayerControls
    print("✓ LayerControls imported")
except ImportError as e:
    print(f"⚠️ Could not import LayerControls: {e}")
    LayerControls = None

# Export available components (only non-None ones)
__all__ = []

if MainWindow is not None:
    __all__.extend(['MainWindow', 'EnhancedMainWindow', 'FixedMainWindow'])

if EnhancedPCBCanvas is not None:
    __all__.extend(['EnhancedPCBCanvas', 'PCBCanvas'])

if CADToolsPanel is not None:
    __all__.append('CADToolsPanel')

if ChipRenderer is not None:
    __all__.extend(['ChipRenderer', 'EnhancedChipGraphicsItem'])

if EnhancedComponentPalette is not None:
    __all__.append('EnhancedComponentPalette')

if StatusBarManager is not None:
    __all__.append('StatusBarManager')

if MenuBarManager is not None:
    __all__.append('MenuBarManager')

if PropertiesPanel is not None:
    __all__.append('PropertiesPanel')

if LayerControls is not None:
    __all__.append('LayerControls')

print(f"✓ UI package initialized with components: {__all__}")

# Create fallback for CAD Tools Panel if needed
if CADToolsPanel is None:
    print("⚠️ Creating fallback CAD Tools Panel placeholder")
    
    class CADToolsPanelFallback:
        """Fallback CAD Tools Panel when real one isn't available"""
        
        def __init__(self, parent=None):
            from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
            
            self.widget = QWidget(parent)
            layout = QVBoxLayout(self.widget)
            layout.addWidget(QLabel("🔧 CAD Tools"))
            layout.addWidget(QLabel("CAD Tools Panel not available"))
            layout.addWidget(QLabel("Check ui/cad_tools_panel.py"))
            print("⚠️ Using fallback CAD Tools Panel")
        
        def set_canvas(self, canvas):
            print("⚠️ Fallback CAD Tools Panel - canvas set")
        
        def select_tool(self, tool):
            print(f"⚠️ Fallback CAD Tools Panel - tool selected: {tool}")
    
    CADToolsPanel = CADToolsPanelFallback
    __all__.append('CADToolsPanel')

# Ensure backwards compatibility
if 'EnhancedMainWindow' not in globals() and MainWindow is not None:
    EnhancedMainWindow = MainWindow

if 'FixedMainWindow' not in globals() and MainWindow is not None:
    FixedMainWindow = MainWindow

print("🎯 UI package ready with CAD tools support!")

# Debug function
def check_cad_tools_availability():
    """Check if CAD tools are properly available"""
    print("\n🔧 CAD Tools Availability Check:")
    print(f"   CADToolsPanel: {'✓ Available' if CADToolsPanel and not hasattr(CADToolsPanel, 'widget') else '❌ Fallback'}")
    print(f"   ChipRenderer: {'✓ Available' if ChipRenderer else '❌ Not available'}")
    print(f"   Enhanced Canvas: {'✓ Available' if EnhancedPCBCanvas else '❌ Not available'}")
    
    if CADToolsPanel and not hasattr(CADToolsPanel, 'widget'):
        print("   🎉 Full CAD functionality is available!")
    else:
        print("   ⚠️ Using fallback mode - create ui/cad_tools_panel.py for full functionality")

# Auto-check on import
if os.getenv('XSETI_DEBUG') == '1':
    check_cad_tools_availability()
