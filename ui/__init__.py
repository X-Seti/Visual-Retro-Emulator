"""
X-Seti - June11 2025 - UI Package - Visual Retro Emulator
Contains all user interface components
"""

# Try to import main components with fallbacks
try:
    from .main_window import MainWindow
except ImportError as e:
    print(f"⚠️ Could not import MainWindow: {e}")
    MainWindow = None

try:
    from .canvas import EnhancedPCBCanvas, PCBCanvas
except ImportError as e:
    print(f"⚠️ Could not import Canvas: {e}")
    EnhancedPCBCanvas = None
    PCBCanvas = None

try:
    from .component_palette import EnhancedComponentPalette
except ImportError as e:
    print(f"⚠️ Could not import ComponentPalette: {e}")
    EnhancedComponentPalette = None

try:
    from .status_bar import StatusBarManager
except ImportError as e:
    print(f"⚠️ Could not import StatusBar: {e}")
    StatusBarManager = None

try:
    from .menu_bar import MenuBarManager
except ImportError as e:
    print(f"⚠️ Could not import MenuBar: {e}")
    MenuBarManager = None

# Export available components
__all__ = [
    'MainWindow',
    'EnhancedPCBCanvas', 
    'PCBCanvas',
    'EnhancedComponentPalette',
    'StatusBarManager', 
    'MenuBarManager'
]
