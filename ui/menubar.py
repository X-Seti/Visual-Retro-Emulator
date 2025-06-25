#!/usr/bin/env python3
"""
X-Seti - June25 2025 - Visual Retro System Emulator Builder - Clean Menu Bar
Simple, clean menu bar without conflicts or complexity
"""
#this belongs in ui/menu_bar.py

from PyQt6.QtWidgets import QMenuBar, QMessageBox, QFileDialog, QInputDialog
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QAction, QKeySequence
import os

class MenuBarSignals(QObject):
    """Clean signals for menu actions"""
    # File menu
    new_project = pyqtSignal()
    open_project = pyqtSignal()
    save_project = pyqtSignal()
    save_as_project = pyqtSignal()
    exit_app = pyqtSignal()
    
    # Edit menu
    undo = pyqtSignal()
    redo = pyqtSignal()
    cut = pyqtSignal()
    copy = pyqtSignal()
    paste = pyqtSignal()
    delete = pyqtSignal()
    select_all = pyqtSignal()
    
    # View menu
    zoom_in = pyqtSignal()
    zoom_out = pyqtSignal()
    zoom_fit = pyqtSignal()
    zoom_actual = pyqtSignal()
    toggle_grid = pyqtSignal()
    toggle_pin_numbers = pyqtSignal()
    toggle_component_labels = pyqtSignal()
    
    # Component menu
    search_components = pyqtSignal()
    
    # Simulation menu
    start_simulation = pyqtSignal()
    stop_simulation = pyqtSignal()
    
    # Help menu
    show_shortcuts = pyqtSignal()
    show_about = pyqtSignal()

class CleanMenuBar(QMenuBar):
    """Clean, simple menu bar for Visual Retro Emulator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = MenuBarSignals()
        self.main_window = parent
        self._create_menus()
        print("✅ Clean menu bar created")
    
    def _create_menus(self):
        """Create all menu items"""
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_component_menu()
        self._create_simulation_menu()
        self._create_help_menu()
    
    def _create_file_menu(self):
        """Create File menu"""
        file_menu = self.addMenu('&File')
        
        # New Project
        new_action = QAction('&New Project', self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip('Create a new project')
        new_action.triggered.connect(self.signals.new_project.emit)
        file_menu.addAction(new_action)
        
        # Open Project
        open_action = QAction('&Open Project...', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip('Open an existing project')
        open_action.triggered.connect(self.signals.open_project.emit)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Save Project
        save_action = QAction('&Save Project', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip('Save the current project')
        save_action.triggered.connect(self.signals.save_project.emit)
        file_menu.addAction(save_action)
        
        # Save As
        save_as_action = QAction('Save &As...', self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip('Save the project with a new name')
        save_as_action.triggered.connect(self.signals.save_as_project.emit)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.signals.exit_app.emit)
        file_menu.addAction(exit_action)
    
    def _create_edit_menu(self):
        """Create Edit menu"""
        edit_menu = self.addMenu('&Edit')
        
        # Undo
        undo_action = QAction('&Undo', self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.signals.undo.emit)
        edit_menu.addAction(undo_action)
        
        # Redo
        redo_action = QAction('&Redo', self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.signals.redo.emit)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Cut
        cut_action = QAction('Cu&t', self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.signals.cut.emit)
        edit_menu.addAction(cut_action)
        
        # Copy
        copy_action = QAction('&Copy', self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.signals.copy.emit)
        edit_menu.addAction(copy_action)
        
        # Paste
        paste_action = QAction('&Paste', self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.signals.paste.emit)
        edit_menu.addAction(paste_action)
        
        # Delete
        delete_action = QAction('&Delete', self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.signals.delete.emit)
        edit_menu.addAction(delete_action)
        
        edit_menu.addSeparator()
        
        # Select All
        select_all_action = QAction('Select &All', self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.signals.select_all.emit)
        edit_menu.addAction(select_all_action)
    
    def _create_view_menu(self):
        """Create View menu"""
        view_menu = self.addMenu('&View')
        
        # Zoom In
        zoom_in_action = QAction('Zoom &In', self)
        zoom_in_action.setShortcut('Ctrl++')
        zoom_in_action.triggered.connect(self.signals.zoom_in.emit)
        view_menu.addAction(zoom_in_action)
        
        # Zoom Out
        zoom_out_action = QAction('Zoom &Out', self)
        zoom_out_action.setShortcut('Ctrl+-')
        zoom_out_action.triggered.connect(self.signals.zoom_out.emit)
        view_menu.addAction(zoom_out_action)
        
        # Zoom Fit
        zoom_fit_action = QAction('Zoom &Fit', self)
        zoom_fit_action.setShortcut('Ctrl+0')
        zoom_fit_action.triggered.connect(self.signals.zoom_fit.emit)
        view_menu.addAction(zoom_fit_action)
        
        # Zoom Actual
        zoom_actual_action = QAction('&Actual Size', self)
        zoom_actual_action.setShortcut('Ctrl+1')
        zoom_actual_action.triggered.connect(self.signals.zoom_actual.emit)
        view_menu.addAction(zoom_actual_action)
        
        view_menu.addSeparator()
        
        # Toggle Grid
        grid_action = QAction('Show &Grid', self)
        grid_action.setCheckable(True)
        grid_action.setChecked(True)
        grid_action.setShortcut('Ctrl+G')
        grid_action.triggered.connect(self.signals.toggle_grid.emit)
        view_menu.addAction(grid_action)
        
        # Toggle Pin Numbers
        pin_numbers_action = QAction('Show &Pin Numbers', self)
        pin_numbers_action.setCheckable(True)
        pin_numbers_action.setChecked(True)
        pin_numbers_action.setShortcut('Ctrl+P')
        pin_numbers_action.triggered.connect(self.signals.toggle_pin_numbers.emit)
        view_menu.addAction(pin_numbers_action)
        
        # Toggle Component Labels
        labels_action = QAction('Show Component &Labels', self)
        labels_action.setCheckable(True)
        labels_action.setChecked(True)
        labels_action.setShortcut('Ctrl+L')
        labels_action.triggered.connect(self.signals.toggle_component_labels.emit)
        view_menu.addAction(labels_action)
    
    def _create_component_menu(self):
        """Create Component menu"""
        component_menu = self.addMenu('&Component')
        
        # Search Components
        search_action = QAction('&Search Components...', self)
        search_action.setShortcut('Ctrl+F')
        search_action.triggered.connect(self.signals.search_components.emit)
        component_menu.addAction(search_action)
    
    def _create_simulation_menu(self):
        """Create Simulation menu"""
        simulation_menu = self.addMenu('&Simulation')
        
        # Start Simulation
        start_action = QAction('&Start Simulation', self)
        start_action.setShortcut('F5')
        start_action.triggered.connect(self.signals.start_simulation.emit)
        simulation_menu.addAction(start_action)
        
        # Stop Simulation
        stop_action = QAction('S&top Simulation', self)
        stop_action.setShortcut('Shift+F5')
        stop_action.triggered.connect(self.signals.stop_simulation.emit)
        simulation_menu.addAction(stop_action)
    
    def _create_help_menu(self):
        """Create Help menu"""
        help_menu = self.addMenu('&Help')
        
        # Keyboard Shortcuts
        shortcuts_action = QAction('&Keyboard Shortcuts', self)
        shortcuts_action.setShortcut('F1')
        shortcuts_action.triggered.connect(self.signals.show_shortcuts.emit)
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        # About
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.signals.show_about.emit)
        help_menu.addAction(about_action)

def create_menu_bar(main_window):
    """Create and connect menu bar to main window"""
    menu_bar = CleanMenuBar(main_window)
    main_window.setMenuBar(menu_bar)
    
    # Connect menu signals to main window methods if they exist
    signals = menu_bar.signals
    
    # File menu connections
    if hasattr(main_window, '_new_project'):
        signals.new_project.connect(main_window._new_project)
    if hasattr(main_window, '_open_project'):
        signals.open_project.connect(main_window._open_project)
    if hasattr(main_window, '_save_project'):
        signals.save_project.connect(main_window._save_project)
    if hasattr(main_window, '_save_as_project'):
        signals.save_as_project.connect(main_window._save_as_project)
    if hasattr(main_window, 'close'):
        signals.exit_app.connect(main_window.close)
    
    # Edit menu connections
    if hasattr(main_window, '_undo'):
        signals.undo.connect(main_window._undo)
    if hasattr(main_window, '_redo'):
        signals.redo.connect(main_window._redo)
    if hasattr(main_window, '_cut'):
        signals.cut.connect(main_window._cut)
    if hasattr(main_window, '_copy'):
        signals.copy.connect(main_window._copy)
    if hasattr(main_window, '_paste'):
        signals.paste.connect(main_window._paste)
    if hasattr(main_window, '_delete'):
        signals.delete.connect(main_window._delete)
    if hasattr(main_window, '_select_all'):
        signals.select_all.connect(main_window._select_all)
    
    # View menu connections
    if hasattr(main_window, '_zoom_in'):
        signals.zoom_in.connect(main_window._zoom_in)
    if hasattr(main_window, '_zoom_out'):
        signals.zoom_out.connect(main_window._zoom_out)
    if hasattr(main_window, '_zoom_fit'):
        signals.zoom_fit.connect(main_window._zoom_fit)
    if hasattr(main_window, '_zoom_actual'):
        signals.zoom_actual.connect(main_window._zoom_actual)
    if hasattr(main_window, '_toggle_grid'):
        signals.toggle_grid.connect(main_window._toggle_grid)
    if hasattr(main_window, '_toggle_pin_numbers'):
        signals.toggle_pin_numbers.connect(main_window._toggle_pin_numbers)
    if hasattr(main_window, '_toggle_component_labels'):
        signals.toggle_component_labels.connect(main_window._toggle_component_labels)
    
    # Component menu connections
    if hasattr(main_window, '_search_components'):
        signals.search_components.connect(main_window._search_components)
    
    # Simulation menu connections
    if hasattr(main_window, '_start_simulation'):
        signals.start_simulation.connect(main_window._start_simulation)
    if hasattr(main_window, '_stop_simulation'):
        signals.stop_simulation.connect(main_window._stop_simulation)
    
    # Help menu connections
    if hasattr(main_window, '_show_shortcuts'):
        signals.show_shortcuts.connect(main_window._show_shortcuts)
    if hasattr(main_window, '_show_about'):
        signals.show_about.connect(main_window._show_about)
    
    print("✅ Menu bar connected to main window")
    return menu_bar

# Backward compatibility
MenuBarManager = CleanMenuBar
RetroEmulatorMenuBar = CleanMenuBar

# Export
__all__ = ['CleanMenuBar', 'MenuBarManager', 'RetroEmulatorMenuBar', 'create_menu_bar']