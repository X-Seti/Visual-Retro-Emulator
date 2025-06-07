"""
UI Package
Visual Retro System Emulator Builder - User Interface Components
"""

from .main_window import MainWindow
from .canvas import EnhancedCanvas, EnhancedHardwareComponent, EnhancedPCBCanvas, Canvas, PCBCanvas
from .component_palette import ComponentPaletteWidget, DraggableComponentItem, EnhancedComponentPalette
from .properties_panel import PropertiesPanelWidget, PropertyEditor
from .layer_controls import LayerControlsWidget, EnhancedLayerControls, LayerControlWidget
from .menu_bar import RetroEmulatorMenuBar, EnhancedMenuBar, MenuBar, MenuBarManager
from .status_bar import RetroEmulatorStatusBar, EnhancedStatusBar, StatusBar, StatusBarManager
from .property_editor import (PropertyEditorDialog, BasePropertyEditor, PropertyEditorFactory,
                             EnhancedPropertyEditor, PropertyEditor, PropertyEditorWidget, PropertyManager)

__all__ = [
    'MainWindow',
    'EnhancedCanvas', 
    'EnhancedPCBCanvas',
    'Canvas',
    'PCBCanvas',
    'EnhancedHardwareComponent',
    'ComponentPaletteWidget',
    'EnhancedComponentPalette',  # Added alias
    'DraggableComponentItem', 
    'PropertiesPanelWidget',
    'PropertyEditor',
    'LayerControlsWidget',
    'EnhancedLayerControls',
    'LayerControlWidget',  # Singular alias
    'RetroEmulatorMenuBar',
    'EnhancedMenuBar',
    'MenuBar',
    'MenuBarManager',  # Manager alias
    'RetroEmulatorStatusBar',
    'EnhancedStatusBar',
    'StatusBar',
    'StatusBarManager',
    'PropertyEditorDialog',
    'BasePropertyEditor',
    'PropertyEditorFactory',
    'EnhancedPropertyEditor',
    'PropertyEditorWidget',
    'PropertyManager'
]

__version__ = '1.0.0'
__author__ = 'Visual Retro System Emulator Builder Team'