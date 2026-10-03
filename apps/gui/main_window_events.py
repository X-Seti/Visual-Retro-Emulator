#!/usr/bin/env python3
"""
X-Seti - June25 2025 - Visual Retro System Emulator Builder - Event Handlers
Event handling functions
"""
#this belongs in ui/main_window_events.py

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

def handle_close_event(main_window, event):
    """Handle window close event"""
    if main_window.is_modified:
        reply = QMessageBox.question(main_window, "Unsaved Changes", 
                                   "Save changes before closing?",
                                   QMessageBox.StandardButton.Save | 
                                   QMessageBox.StandardButton.Discard | 
                                   QMessageBox.StandardButton.Cancel)
        
        if reply == QMessageBox.StandardButton.Save:
            from .main_window_actions import save_project
            save_project(main_window)
        elif reply == QMessageBox.StandardButton.Cancel:
            event.ignore()
            return
    
    event.accept()
    print("👋 Application closed")