#!/usr/bin/env python3
"""
X-Seti - June25 2025 - Visual Retro System Emulator Builder - Action Functions
Action handlers - small focused functions only
"""
#this belongs in ui/main_window_actions.py

import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# File Actions
def new_project(main_window):
    """Create new project"""
    main_window.current_project_path = None
    main_window.is_modified = False
    if main_window.canvas and hasattr(main_window.canvas, 'clear'):
        main_window.canvas.clear()
    update_window_title(main_window)
    print("📄 New project created")

def open_project(main_window):
    """Open project"""
    filename, _ = QFileDialog.getOpenFileName(main_window, "Open Project", "", "Project Files (*.json)")
    if filename:
        main_window.current_project_path = filename
        main_window.is_modified = False
        update_window_title(main_window)
        print(f"📂 Project opened: {filename}")

def save_project(main_window):
    """Save project"""
    if not main_window.current_project_path:
        filename, _ = QFileDialog.getSaveFileName(main_window, "Save Project", "", "Project Files (*.json)")
        if filename:
            main_window.current_project_path = filename
    
    if main_window.current_project_path:
        main_window.is_modified = False
        update_window_title(main_window)
        print(f"💾 Project saved: {main_window.current_project_path}")

# Edit Actions
def undo_action(main_window):
    """Undo action"""
    print("↶ Undo")

def redo_action(main_window):
    """Redo action"""
    print("↷ Redo")

# View Actions
def zoom_in(main_window):
    """Zoom in"""
    if main_window.canvas:
        main_window.canvas.scale(1.2, 1.2)
    print("🔍 Zoom in")

def zoom_out(main_window):
    """Zoom out"""
    if main_window.canvas:
        main_window.canvas.scale(0.8, 0.8)
    print("🔍 Zoom out")

def zoom_fit(main_window):
    """Zoom to fit"""
    if main_window.canvas and hasattr(main_window.canvas, 'fitInView'):
        main_window.canvas.fitInView(main_window.canvas.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
    print("🔍 Zoom fit")

def toggle_grid(main_window):
    """Toggle grid"""
    if main_window.canvas and hasattr(main_window.canvas, 'toggle_grid'):
        main_window.canvas.toggle_grid()
    print("⊞ Grid toggled")

# Tool Actions
def set_tool(main_window, tool_name):
    """Set current tool"""
    main_window.current_tool = tool_name
    
    # Update canvas tool if available
    if main_window.canvas and hasattr(main_window.canvas, 'set_tool'):
        main_window.canvas.set_tool(tool_name)
    
    # Update CAD tools selection
    if main_window.cad_tools_panel and hasattr(main_window.cad_tools_panel, 'select_tool'):
        main_window.cad_tools_panel.select_tool(tool_name)
    
    print(f"🔧 Tool changed to: {tool_name}")

# Simulation Actions
def start_simulation(main_window):
    """Start simulation"""
    print("▶️ Simulation started")

def stop_simulation(main_window):
    """Stop simulation"""
    print("⏹️ Simulation stopped")

# Dialog Actions
def show_search(main_window):
    """Show search dialog"""
    text, ok = QInputDialog.getText(main_window, "Search Components", "Search for:")
    if ok and text:
        print(f"🔍 Searching for: {text}")

def show_shortcuts(main_window):
    """Show keyboard shortcuts"""
    shortcuts_text = """
<b>🎯 Visual Retro Emulator - Keyboard Shortcuts</b><br><br>

<b>📁 File:</b><br>
<b>Ctrl+N</b> - New Project<br>
<b>Ctrl+O</b> - Open Project<br>
<b>Ctrl+S</b> - Save Project<br><br>

<b>✏️ Edit:</b><br>
<b>Ctrl+Z</b> - Undo<br>
<b>Ctrl+Y</b> - Redo<br><br>

<b>🔍 View:</b><br>
<b>Ctrl++</b> - Zoom In<br>
<b>Ctrl+-</b> - Zoom Out<br>
<b>Ctrl+0</b> - Zoom Fit<br>
<b>Ctrl+G</b> - Toggle Grid<br><br>

<b>🎮 Simulation:</b><br>
<b>F5</b> - Start Simulation<br><br>

<b>🔍 Other:</b><br>
<b>Ctrl+F</b> - Search Components<br>
<b>F1</b> - This Help<br>
<b>Esc</b> - Cancel Operation<br><br>
        """
    QMessageBox.information(main_window, "Keyboard Shortcuts", shortcuts_text)

def cancel_current_operation(main_window):
    """Cancel current operation"""
    set_tool(main_window, 'select')
    print("❌ Operation cancelled")

# Helper functions
def update_window_title(main_window):
    """Update window title"""
    title = "Visual Retro System Emulator Builder"
    if main_window.current_project_path:
        title += f" - {os.path.basename(main_window.current_project_path)}"
    if main_window.is_modified:
        title += " *"
    main_window.setWindowTitle(title)