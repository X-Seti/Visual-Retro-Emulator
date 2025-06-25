#!/usr/bin/env python3
"""
X-Seti - June25 2025 - Visual Retro System Emulator Builder - Main Window Core
Minimal core window - uses existing UI files, no conflicts
"""
#this belongs in ui/main_window.py

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ui.menu_bar import create_menu_bar


class MainWindow(QMainWindow):
    """Main window - minimal core, delegates to existing UI files"""
    
    def __init__(self):
        super().__init__()
        
        # State
        self.current_tool = 'select'
        self.current_project_path = None
        self.is_modified = False
        self.menu_bar = create_menu_bar(self)
        # Core references - set by main_app.py
        self.canvas = None
        self.component_manager = None
        self.project_manager = None
        self.simulation_engine = None
        self.layer_manager = None
        
        # UI Components - created by setup functions
        self.cad_tools_panel = None
        self.component_palette = None
        self.properties_panel = None
        self.status_manager = None
        self.menu_manager = None
        self.pin_numbers_manager = None
        self.layer_controls = None
        
        # Setup
        self._setup_window()
        from .main_window_init import initialize_main_window
        initialize_main_window(self)
        
        print("✅ Main window initialized")
    
    def _setup_window(self):
        """Basic window setup"""
        self.setWindowTitle("Visual Retro System Emulator Builder")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
    
    # Manager setters - called by main_app.py
    def set_component_manager(self, manager):
        self.component_manager = manager
        print("✓ Component manager connected")

    def set_project_manager(self, manager):
        self.project_manager = manager
        print("✓ Project manager connected")

    def set_simulation_engine(self, engine):
        self.simulation_engine = engine
        print("✓ Simulation engine connected")

    def refresh_component_palette(self):
        """Refresh component palette"""
        if self.component_palette and hasattr(self.component_palette, 'refresh'):
            self.component_palette.refresh()
        print("✓ Component palette refreshed")

    # Event handlers - delegates to separate files
    def closeEvent(self, event):
        from .main_window_events import handle_close_event
        handle_close_event(self, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

# Export
__all__ = ['MainWindow']
