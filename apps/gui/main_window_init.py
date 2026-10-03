#!/usr/bin/env python3
"""
X-Seti - June25 2025 - Visual Retro System Emulator Builder - Main Window Initialization
Uses existing UI files, no duplicated functions
"""
#this belongs in ui/main_window_init.py

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

def initialize_main_window(main_window):
    """Main initialization function - uses existing UI files"""
    initialize_managers(main_window)
    create_central_widget(main_window)
    create_docks(main_window)
    create_menu_bar(main_window)
    create_status_bar(main_window)
    setup_shortcuts(main_window)
    apply_theme(main_window)
    post_init_setup(main_window)

def initialize_managers(main_window):
    """Initialize managers - only missing ones"""
    print("Initializing managers...")
    
    # Layer Manager
    from managers.layer_manager import LayerManager
    main_window.layer_manager = LayerManager()
    print("✓ Layer Manager initialized")

def create_central_widget(main_window):
    """Create canvas as central widget"""
    from ui.canvas import PCBCanvas
    main_window.canvas = PCBCanvas()
    main_window.setCentralWidget(main_window.canvas)
    print("✅ Canvas created")

def create_docks(main_window):
    """Create dock widgets - uses existing UI files"""
    create_component_palette_dock(main_window)
    create_cad_tools_dock(main_window)
    create_properties_dock(main_window)
    create_layer_controls_dock(main_window)

def create_component_palette_dock(main_window):
    """Create component palette dock - uses existing ui/component_palette.py"""
    from ui.component_palette import ComponentPalette
    main_window.component_palette = ComponentPalette()
    
    palette_dock = QDockWidget("Components", main_window)
    palette_dock.setWidget(main_window.component_palette)
    palette_dock.setMinimumWidth(250)
    
    main_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, palette_dock)
    main_window.component_palette_dock = palette_dock
    print("✅ Component palette dock created")

def create_cad_tools_dock(main_window):
    """Create CAD tools dock - uses existing ui/cad_tools_panel.py"""
    from ui.cad_tools_panel import CADToolsPanel
    main_window.cad_tools_panel = CADToolsPanel()
    
    # Connect to canvas
    if main_window.canvas:
        main_window.cad_tools_panel.set_canvas(main_window.canvas)
    
    cad_dock = QDockWidget("CAD Tools", main_window)
    cad_dock.setWidget(main_window.cad_tools_panel)
    cad_dock.setMinimumWidth(200)
    cad_dock.setMaximumWidth(280)
    
    main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, cad_dock)
    main_window.cad_tools_dock = cad_dock
    print("✅ CAD Tools dock created")

def create_properties_dock(main_window):
    """Create properties dock - uses existing ui/property_panel.py"""
    from ui.property_panel import PropertiesPanel
    main_window.properties_panel = PropertiesPanel()
    
    prop_dock = QDockWidget("Properties", main_window)
    prop_dock.setWidget(main_window.properties_panel)
    prop_dock.setMinimumWidth(250)
    
    main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, prop_dock)
    main_window.properties_dock = prop_dock
    print("✅ Properties dock created")

def create_layer_controls_dock(main_window):
    """Create layer controls dock - uses existing ui/layer_controls.py"""
    from ui.layer_controls import LayerControls
    main_window.layer_controls = LayerControls()
    
    layer_dock = QDockWidget("Layers", main_window)
    layer_dock.setWidget(main_window.layer_controls)
    layer_dock.setMinimumWidth(180)
    layer_dock.setMaximumWidth(250)
    
    main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layer_dock)
    main_window.layer_controls_dock = layer_dock
    print("✅ Layer controls dock created")

def create_menu_bar(main_window):
    """Create menu bar - uses existing ui/menu_bar.py"""
    from ui.menu_bar import RetroEmulatorMenuBar
    main_window.menu_manager = RetroEmulatorMenuBar(main_window)
    main_window.setMenuBar(main_window.menu_manager)
    print("✅ Menu bar created")

def create_status_bar(main_window):
    """Create status bar - uses existing ui/status_bar.py"""
    from ui.status_bar import StatusBarManager
    main_window.status_manager = StatusBarManager(main_window)
    print("✅ Status bar created")

def setup_shortcuts(main_window):
    """Setup keyboard shortcuts"""
    from .main_window_shortcuts import setup_all_shortcuts
    setup_all_shortcuts(main_window)

def apply_theme(main_window):
    """Apply theme - uses existing ui/dark_theme.py"""
    from ui.dark_theme import apply_dark_theme
    apply_dark_theme(main_window)
    print("✅ Dark theme applied")

def post_init_setup(main_window):
    """Post-initialization setup"""
    initialize_pin_numbers(main_window)
    update_window_title(main_window)
    update_status_counts(main_window)

def initialize_pin_numbers(main_window):
    """Initialize pin numbers - uses existing ui/pin_numbers.py"""
    from ui.pin_numbers import add_pin_numbers_to_canvas
    if main_window.canvas:
        main_window.pin_numbers_manager = add_pin_numbers_to_canvas(main_window.canvas)
        print("✓ Pin numbers manager initialized")

def update_window_title(main_window):
    """Update window title"""
    title = "Visual Retro System Emulator Builder"
    if main_window.current_project_path:
        import os
        title += f" - {os.path.basename(main_window.current_project_path)}"
    if main_window.is_modified:
        title += " *"
    main_window.setWindowTitle(title)

def update_status_counts(main_window):
    """Update status bar counts"""
    if main_window.status_manager:
        component_count = 0
        if main_window.canvas and hasattr(main_window.canvas, 'components'):
            component_count = len(main_window.canvas.components)
        main_window.status_manager.update_component_count(component_count)