"""
X-Seti - June12 2025 - UI Package - Visual Retro Emulator
Contains all user interface components with robust error handling
"""

#this belongs in ui/__init__.py
import sys
import os

# Try to import main components with fallbacks
MainWindow = None
try:
    from .main_window import MainWindow
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

EnhancedPCBCanvas = None
PCBCanvas = None
try:
    from .canvas import EnhancedPCBCanvas, PCBCanvas
    print("✓ Canvas components imported")
except ImportError as e:
    print(f"⚠️ Could not import Canvas components: {e}")
    EnhancedPCBCanvas = None
    PCBCanvas = None

EnhancedComponentPalette = None
try:
    from .component_palette import EnhancedComponentPalette
    print("✓ ComponentPalette imported")
except ImportError as e:
    print(f"⚠️ Could not import ComponentPalette: {e}")
    EnhancedComponentPalette = None

StatusBarManager = None
try:
    from .status_bar import StatusBarManager
    print("✓ StatusBar imported")
except ImportError as e:
    print(f"⚠️ Could not import StatusBar: {e}")
    StatusBarManager = None

MenuBarManager = None
try:
    from .menu_bar import MenuBarManager
    print("✓ MenuBar imported")
except ImportError as e:
    print(f"⚠️ Could not import MenuBar: {e}")
    MenuBarManager = None

PropertiesPanel = None
try:
    from .properties_panel import PropertiesPanel
    print("✓ PropertiesPanel imported")
except ImportError as e:
    print(f"⚠️ Could not import PropertiesPanel: {e}")
    PropertiesPanel = None

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
    __all__.append('MainWindow')

if EnhancedPCBCanvas is not None:
    __all__.extend(['EnhancedPCBCanvas', 'PCBCanvas'])

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