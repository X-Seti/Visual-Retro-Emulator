#!/usr/bin/env python3
"""
X-Seti - June23 2025 - UI Package - Visual Retro Emulator
Contains all user interface components - cleaned up imports
"""
#this belongs in ui/__init__.py

import sys
import os

# Import main components - single clean import path
MainWindow = None
try:
    from .main_window import MainWindow
    print("✓ MainWindow imported from ui.main_window")
except ImportError as e:
    print(f"❌ Could not import MainWindow: {e}")
    MainWindow = None

# Canvas components
PCBCanvas = None
try:
    from .canvas import PCBCanvas
    print("✓ Canvas components imported")
except ImportError as e:
    print(f"⚠️ Could not import Canvas components: {e}")
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
    print("✓ ComponentPalette imported")
except ImportError as e:
    print(f"⚠️ Could not import ComponentPalette: {e}")
    ComponentPalette = None

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
    from .property_panel import PropertiesPanel
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
    __all__.append('MainWindow')

if PCBCanvas is not None:
    __all__.append('PCBCanvas')

if CADToolsPanel is not None:
    __all__.append('CADToolsPanel')

if ChipRenderer is not None:
    __all__.extend(['ChipRenderer', 'ChipGraphicsItem'])

if ComponentPalette is not None:
    __all__.append('ComponentPalette')

if StatusBarManager is not None:
    __all__.append('StatusBarManager')

if MenuBarManager is not None:
    __all__.append('MenuBarManager')

if PropertiesPanel is not None:
    __all__.append('PropertiesPanel')

if LayerControls is not None:
    __all__.append('LayerControls')

print(f"✓ UI package initialized with components: {__all__}")
