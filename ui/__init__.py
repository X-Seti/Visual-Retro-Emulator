#!/usr/bin/env python3
"""
X-Seti - June23 2025 - UI Package - Visual Retro Emulator  
Clean UI package with single implementations only
"""
#this belongs in ui/__init__.py

import sys
import os

# Import main components - single clean import paths only
MainWindow = None
try:
    from .main_window import MainWindow
    print("✓ MainWindow imported")
except ImportError as e:
    print(f"❌ Could not import MainWindow: {e}")
    MainWindow = None

# Canvas components
PCBCanvas = None
try:
    from .canvas import PCBCanvas
    print("✓ Canvas imported")
except ImportError as e:
    print(f"⚠️ Could not import Canvas: {e}")
    PCBCanvas = None

# CAD Tools Panel 
CADToolsPanel = None
try:
    from .cad_tools_panel import CADToolsPanel
    print("✓ CAD Tools Panel imported")
except ImportError as e:
    print(f"⚠️ Could not import CAD Tools Panel: {e}")
    CADToolsPanel = None

# Chip Renderer
ChipRenderer = None
ChipGraphicsItem = None
try:
    from .chip_renderer import ChipRenderer, ChipGraphicsItem
    print("✓ Chip Renderer imported")
except ImportError as e:
    print(f"⚠️ Could not import Chip Renderer: {e}")
    ChipRenderer = None
    ChipGraphicsItem = None

# Component Palette
ComponentPalette = None
try:
    from .component_palette import ComponentPalette
    print("✓ Component Palette imported")
except ImportError as e:
    print(f"⚠️ Could not import Component Palette: {e}")
    ComponentPalette = None

# Status Bar
RetroEmulatorStatusBar = None
try:
    from .status_bar import RetroEmulatorStatusBar
    # Alias for compatibility
    StatusBarManager = RetroEmulatorStatusBar
    print("✓ Status Bar imported")
except ImportError as e:
    print(f"⚠️ Could not import Status Bar: {e}")
    RetroEmulatorStatusBar = None
    StatusBarManager = None

# Menu Bar
RetroEmulatorMenuBar = None
try:
    from .menu_bar import RetroEmulatorMenuBar
    # Alias for compatibility  
    MenuBarManager = RetroEmulatorMenuBar
    print("✓ Menu Bar imported")
except ImportError as e:
    print(f"⚠️ Could not import Menu Bar: {e}")
    RetroEmulatorMenuBar = None
    MenuBarManager = None

# Toolbar
MainToolbar = None
ComponentToolbar = None
try:
    from .toolbar import MainToolbar, ComponentToolbar
    print("✓ Toolbars imported")
except ImportError as e:
    print(f"⚠️ Could not import Toolbars: {e}")
    MainToolbar = None
    ComponentToolbar = None

# Properties Panel
PropertiesPanel = None
try:
    from .property_panel import PropertiesPanel
    print("✓ Properties Panel imported")
except ImportError as e:
    print(f"⚠️ Could not import Properties Panel: {e}")
    PropertiesPanel = None

# Layer Controls
LayerControls = None
try:
    from .layer_controls import LayerControls
    print("✓ Layer Controls imported")
except ImportError as e:
    print(f"⚠️ Could not import Layer Controls: {e}")
    LayerControls = None

# Export available components (only non-None ones)
__all__ = []

# Add components that successfully imported
for component_name, component_class in [
    ('MainWindow', MainWindow),
    ('PCBCanvas', PCBCanvas), 
    ('CADToolsPanel', CADToolsPanel),
    ('ChipRenderer', ChipRenderer),
    ('ChipGraphicsItem', ChipGraphicsItem),
    ('ComponentPalette', ComponentPalette),
    ('RetroEmulatorStatusBar', RetroEmulatorStatusBar),
    ('StatusBarManager', StatusBarManager),
    ('RetroEmulatorMenuBar', RetroEmulatorMenuBar),
    ('MenuBarManager', MenuBarManager),
    ('MainToolbar', MainToolbar),
    ('ComponentToolbar', ComponentToolbar),
    ('PropertiesPanel', PropertiesPanel),
    ('LayerControls', LayerControls)
]:
    if component_class is not None:
        __all__.append(component_name)

print(f"✓ UI package initialized with: {len(__all__)} components")
print(f"  Available: {__all__}")

# NO FALLBACKS - if a component doesn't import, it's not available
# This forces fixing the actual files instead of using inferior fallbacks