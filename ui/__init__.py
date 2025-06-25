#!/usr/bin/env python3
"""
X-Seti - June25 2025 - UI Package - Visual Retro Emulator
Clean UI package without conflicts or duplicate components
"""
#this belongs in ui/__init__.py

import sys
import os

# Main Window
MainWindow = None
try:
    from .main_window import MainWindow
    print("✓ MainWindow imported")
except ImportError as e:
    print(f"⚠️ Could not import MainWindow: {e}")

# Canvas
PCBCanvas = None
try:
    from .canvas import PCBCanvas
    print("✓ Canvas imported")
except ImportError as e:
    print(f"⚠️ Could not import Canvas: {e}")

# Clean Toolbar (no ComponentToolbar)
MainToolbar = None
try:
    from .toolbar import MainToolbar
    print("✓ MainToolbar imported")
except ImportError as e:
    print(f"⚠️ Could not import MainToolbar: {e}")

# Clean Menu Bar
CleanMenuBar = None
try:
    from .menu_bar import CleanMenuBar
    print("✓ CleanMenuBar imported")
except ImportError as e:
    print(f"⚠️ Could not import CleanMenuBar: {e}")

# Status Bar
StatusBarManager = None
try:
    from .status_bar import StatusBarManager
    print("✓ StatusBarManager imported")
except ImportError as e:
    print(f"⚠️ Could not import StatusBarManager: {e}")

# Component Palette
ComponentPalette = None
try:
    from .component_palette import ComponentPalette
    print("✓ ComponentPalette imported")
except ImportError as e:
    print(f"⚠️ Could not import ComponentPalette: {e}")

# CAD Tools Panel
CADToolsPanel = None
try:
    from .cad_tools_panel import CADToolsPanel
    print("✓ CADToolsPanel imported")
except ImportError as e:
    print(f"⚠️ Could not import CADToolsPanel: {e}")

# Properties Panel
PropertiesPanel = None
try:
    from .property_panel import PropertiesPanel
    print("✓ PropertiesPanel imported")
except ImportError as e:
    print(f"⚠️ Could not import PropertiesPanel: {e}")

# Layer Controls
LayerControls = None
try:
    from .layer_controls import LayerControls
    print("✓ LayerControls imported")
except ImportError as e:
    print(f"⚠️ Could not import LayerControls: {e}")

# Chip Renderer
ChipRenderer = None
ChipGraphicsItem = None
try:
    from .chip_renderer import ChipRenderer, ChipGraphicsItem
    print("✓ ChipRenderer imported")
except ImportError as e:
    print(f"⚠️ Could not import ChipRenderer: {e}")

# Dark Theme
apply_dark_theme = None
try:
    from .dark_theme import apply_dark_theme
    print("✓ Dark theme imported")
except ImportError as e:
    print(f"⚠️ Could not import Dark theme: {e}")

# Pin Numbers
add_pin_numbers_to_canvas = None
try:
    from .pin_numbers import add_pin_numbers_to_canvas
    print("✓ Pin numbers imported")
except ImportError as e:
    print(f"⚠️ Could not import Pin numbers: {e}")

# Export available components (only non-None ones)
__all__ = []

# Add available components to exports
available_components = [
    ('MainWindow', MainWindow),
    ('PCBCanvas', PCBCanvas),
    ('MainToolbar', MainToolbar),
    ('CleanMenuBar', CleanMenuBar),
    ('StatusBarManager', StatusBarManager),
    ('ComponentPalette', ComponentPalette),
    ('CADToolsPanel', CADToolsPanel),
    ('PropertiesPanel', PropertiesPanel),
    ('LayerControls', LayerControls),
    ('ChipRenderer', ChipRenderer),
    ('ChipGraphicsItem', ChipGraphicsItem),
    ('apply_dark_theme', apply_dark_theme),
    ('add_pin_numbers_to_canvas', add_pin_numbers_to_canvas),
]

for name, component in available_components:
    if component is not None:
        __all__.append(name)

print(f"✅ UI package initialized with components: {__all__}")

# Backward compatibility aliases
MenuBarManager = CleanMenuBar
RetroEmulatorMenuBar = CleanMenuBar