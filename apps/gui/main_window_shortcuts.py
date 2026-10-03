#!/usr/bin/env python3
"""
X-Seti - June25 2025 - Visual Retro System Emulator Builder - Keyboard Shortcuts
Only keyboard shortcuts - actions handled by existing files
"""
#this belongs in ui/main_window_shortcuts.py

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

def setup_all_shortcuts(main_window):
    """Setup all keyboard shortcuts"""
    setup_file_shortcuts(main_window)
    setup_edit_shortcuts(main_window)
    setup_view_shortcuts(main_window)
    setup_tool_shortcuts(main_window)
    print("✅ Keyboard shortcuts setup")

def setup_file_shortcuts(main_window):
    """Setup file shortcuts"""
    from .main_window_actions import new_project, open_project, save_project
    
    QShortcut(QKeySequence.StandardKey.New, main_window, lambda: new_project(main_window))
    QShortcut(QKeySequence.StandardKey.Open, main_window, lambda: open_project(main_window)) 
    QShortcut(QKeySequence.StandardKey.Save, main_window, lambda: save_project(main_window))

def setup_edit_shortcuts(main_window):
    """Setup edit shortcuts"""
    from .main_window_actions import undo_action, redo_action
    
    QShortcut(QKeySequence.StandardKey.Undo, main_window, lambda: undo_action(main_window))
    QShortcut(QKeySequence.StandardKey.Redo, main_window, lambda: redo_action(main_window))

def setup_view_shortcuts(main_window):
    """Setup view shortcuts"""
    from .main_window_actions import zoom_in, zoom_out, zoom_fit, toggle_grid
    
    QShortcut(QKeySequence("Ctrl++"), main_window, lambda: zoom_in(main_window))
    QShortcut(QKeySequence("Ctrl+-"), main_window, lambda: zoom_out(main_window))
    QShortcut(QKeySequence("Ctrl+0"), main_window, lambda: zoom_fit(main_window))
    QShortcut(QKeySequence("Ctrl+G"), main_window, lambda: toggle_grid(main_window))

def setup_tool_shortcuts(main_window):
    """Setup tool shortcuts"""
    from .main_window_actions import start_simulation, show_search, show_shortcuts, cancel_current_operation
    
    QShortcut(QKeySequence("F5"), main_window, lambda: start_simulation(main_window))
    QShortcut(QKeySequence("Ctrl+F"), main_window, lambda: show_search(main_window))
    QShortcut(QKeySequence("F1"), main_window, lambda: show_shortcuts(main_window))
    QShortcut(QKeySequence("Escape"), main_window, lambda: cancel_current_operation(main_window))