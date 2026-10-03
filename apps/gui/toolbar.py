#!/usr/bin/env python3
"""
X-Seti - June25 2025 - Visual Retro System Emulator Builder - Clean Toolbar
Standard application toolbar ONLY - no horizontal component toolbar
"""
#this belongs in ui/toolbar.py

from PyQt6.QtWidgets import QToolBar
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction, QKeySequence

class MainToolbar(QToolBar):
    """Main application toolbar - file, edit, view, simulation actions only"""
    
    # Signals for toolbar actions
    new_project = pyqtSignal()
    open_project = pyqtSignal()
    save_project = pyqtSignal()
    undo_action = pyqtSignal()
    redo_action = pyqtSignal()
    zoom_in = pyqtSignal()
    zoom_out = pyqtSignal()
    zoom_fit = pyqtSignal()
    toggle_grid = pyqtSignal()
    start_simulation = pyqtSignal()
    stop_simulation = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MainToolbar")
        self.setWindowTitle("Main Toolbar")
        self.setMovable(True)
        self._create_actions()
        print("✅ Main toolbar created")
    
    def _create_actions(self):
        """Create toolbar actions"""
        # File actions
        self.new_action = QAction("New", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.setToolTip("New Project (Ctrl+N)")
        self.new_action.triggered.connect(self.new_project.emit)
        self.addAction(self.new_action)
        
        self.open_action = QAction("Open", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.setToolTip("Open Project (Ctrl+O)")
        self.open_action.triggered.connect(self.open_project.emit)
        self.addAction(self.open_action)
        
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.setToolTip("Save Project (Ctrl+S)")
        self.save_action.triggered.connect(self.save_project.emit)
        self.addAction(self.save_action)
        
        self.addSeparator()
        
        # Edit actions
        self.undo_act = QAction("Undo", self)
        self.undo_act.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_act.setToolTip("Undo (Ctrl+Z)")
        self.undo_act.triggered.connect(self.undo_action.emit)
        self.addAction(self.undo_act)
        
        self.redo_act = QAction("Redo", self)
        self.redo_act.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_act.setToolTip("Redo (Ctrl+Y)")
        self.redo_act.triggered.connect(self.redo_action.emit)
        self.addAction(self.redo_act)
        
        self.addSeparator()
        
        # View actions
        self.zoom_in_act = QAction("Zoom In", self)
        self.zoom_in_act.setShortcut("Ctrl++")
        self.zoom_in_act.setToolTip("Zoom In (Ctrl++)")
        self.zoom_in_act.triggered.connect(self.zoom_in.emit)
        self.addAction(self.zoom_in_act)
        
        self.zoom_out_act = QAction("Zoom Out", self)
        self.zoom_out_act.setShortcut("Ctrl+-")
        self.zoom_out_act.setToolTip("Zoom Out (Ctrl+-)")
        self.zoom_out_act.triggered.connect(self.zoom_out.emit)
        self.addAction(self.zoom_out_act)
        
        self.zoom_fit_act = QAction("Zoom Fit", self)
        self.zoom_fit_act.setShortcut("Ctrl+0")
        self.zoom_fit_act.setToolTip("Zoom to Fit (Ctrl+0)")
        self.zoom_fit_act.triggered.connect(self.zoom_fit.emit)
        self.addAction(self.zoom_fit_act)
        
        self.grid_act = QAction("Grid", self)
        self.grid_act.setShortcut("Ctrl+G")
        self.grid_act.setToolTip("Toggle Grid (Ctrl+G)")
        self.grid_act.setCheckable(True)
        self.grid_act.triggered.connect(self.toggle_grid.emit)
        self.addAction(self.grid_act)
        
        self.addSeparator()
        
        # Simulation actions
        self.start_sim_act = QAction("Start", self)
        self.start_sim_act.setShortcut("F5")
        self.start_sim_act.setToolTip("Start Simulation (F5)")
        self.start_sim_act.triggered.connect(self.start_simulation.emit)
        self.addAction(self.start_sim_act)
        
        self.stop_sim_act = QAction("Stop", self)
        self.stop_sim_act.setToolTip("Stop Simulation")
        self.stop_sim_act.triggered.connect(self.stop_simulation.emit)
        self.addAction(self.stop_sim_act)

def create_main_toolbar(main_window):
    """Create and connect main toolbar to main window"""
    toolbar = MainToolbar(main_window)
    
    # Connect toolbar signals to main window methods if they exist
    if hasattr(main_window, '_new_project'):
        toolbar.new_project.connect(main_window._new_project)
    if hasattr(main_window, '_open_project'):
        toolbar.open_project.connect(main_window._open_project)
    if hasattr(main_window, '_save_project'):
        toolbar.save_project.connect(main_window._save_project)
    if hasattr(main_window, '_undo'):
        toolbar.undo_action.connect(main_window._undo)
    if hasattr(main_window, '_redo'):
        toolbar.redo_action.connect(main_window._redo)
    if hasattr(main_window, '_zoom_in'):
        toolbar.zoom_in.connect(main_window._zoom_in)
    if hasattr(main_window, '_zoom_out'):
        toolbar.zoom_out.connect(main_window._zoom_out)
    if hasattr(main_window, '_zoom_fit'):
        toolbar.zoom_fit.connect(main_window._zoom_fit)
    if hasattr(main_window, '_toggle_grid'):
        toolbar.toggle_grid.connect(main_window._toggle_grid)
    if hasattr(main_window, '_start_simulation'):
        toolbar.start_simulation.connect(main_window._start_simulation)
    if hasattr(main_window, '_stop_simulation'):
        toolbar.stop_simulation.connect(main_window._stop_simulation)
    
    # Add toolbar to main window
    main_window.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
    
    print("✅ Main toolbar connected to main window")
    return toolbar

# Export only clean components - NO ComponentToolbar references
__all__ = ['MainToolbar', 'create_main_toolbar']

# NO OTHER FUNCTIONS - this prevents any old code from being called