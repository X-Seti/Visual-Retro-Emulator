#!/usr/bin/env python3
"""
X-Seti - June23 2025 - Main Toolbar System - Single Implementation
Visual Retro System Emulator Builder - Main toolbar for file, edit, view, simulation actions
"""
#this belongs in ui/toolbar.py

from PyQt6.QtWidgets import (QToolBar, QWidget, QHBoxLayout, QVBoxLayout, 
                           QPushButton, QButtonGroup, QLabel, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QKeySequence

class MainToolbar(QToolBar):
    """Main application toolbar with file, edit, view, and simulation actions"""
    
    # Signals
    new_project = pyqtSignal()
    open_project = pyqtSignal()
    save_project = pyqtSignal()
    undo = pyqtSignal()
    redo = pyqtSignal()
    zoom_in = pyqtSignal()
    zoom_out = pyqtSignal()
    zoom_fit = pyqtSignal()
    start_simulation = pyqtSignal()
    stop_simulation = pyqtSignal()
    toggle_grid = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("Main Toolbar", parent)
        self.setObjectName("MainToolbar")
        self.setMovable(False)
        
        self._create_actions()
        self._setup_toolbar()
        
        print("✓ Main toolbar created")
    
    def _create_actions(self):
        """Create toolbar actions"""
        # File actions
        self.new_action = QAction("New", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.setToolTip("New Project (Ctrl+N)")
        self.new_action.triggered.connect(self.new_project.emit)
        
        self.open_action = QAction("Open", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.setToolTip("Open Project (Ctrl+O)")
        self.open_action.triggered.connect(self.open_project.emit)
        
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.setToolTip("Save Project (Ctrl+S)")
        self.save_action.triggered.connect(self.save_project.emit)
        
        # Edit actions
        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.setToolTip("Undo (Ctrl+Z)")
        self.undo_action.triggered.connect(self.undo.emit)
        
        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.setToolTip("Redo (Ctrl+Y)")
        self.redo_action.triggered.connect(self.redo.emit)
        
        # View actions
        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_in_action.setShortcut(QKeySequence("Ctrl+="))
        self.zoom_in_action.setToolTip("Zoom In (Ctrl++)")
        self.zoom_in_action.triggered.connect(self.zoom_in.emit)
        
        self.zoom_out_action = QAction("Zoom Out", self)
        self.zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        self.zoom_out_action.setToolTip("Zoom Out (Ctrl+-)")
        self.zoom_out_action.triggered.connect(self.zoom_out.emit)
        
        self.zoom_fit_action = QAction("Zoom Fit", self)
        self.zoom_fit_action.setShortcut(QKeySequence("Ctrl+0"))
        self.zoom_fit_action.setToolTip("Zoom to Fit (Ctrl+0)")
        self.zoom_fit_action.triggered.connect(self.zoom_fit.emit)
        
        self.grid_action = QAction("Grid", self)
        self.grid_action.setShortcut(QKeySequence("Ctrl+G"))
        self.grid_action.setToolTip("Toggle Grid (Ctrl+G)")
        self.grid_action.triggered.connect(self.toggle_grid.emit)
        
        # Simulation actions
        self.start_action = QAction("Start", self)
        self.start_action.setShortcut(QKeySequence("F5"))
        self.start_action.setToolTip("Start Simulation (F5)")
        self.start_action.triggered.connect(self.start_simulation.emit)
        
        self.stop_action = QAction("Stop", self)
        self.stop_action.setShortcut(QKeySequence("Shift+F5"))
        self.stop_action.setToolTip("Stop Simulation (Shift+F5)")
        self.stop_action.triggered.connect(self.stop_simulation.emit)
    
    def _setup_toolbar(self):
        """Setup toolbar layout"""
        # File section
        self.addAction(self.new_action)
        self.addAction(self.open_action)
        self.addAction(self.save_action)
        self.addSeparator()
        
        # Edit section
        self.addAction(self.undo_action)
        self.addAction(self.redo_action)
        self.addSeparator()
        
        # View section
        self.addAction(self.zoom_in_action)
        self.addAction(self.zoom_out_action)
        self.addAction(self.zoom_fit_action)
        self.addAction(self.grid_action)
        self.addSeparator()
        
        # Simulation section
        self.addAction(self.start_action)
        self.addAction(self.stop_action)
    
    def set_undo_enabled(self, enabled):
        """Enable/disable undo action"""
        self.undo_action.setEnabled(enabled)
    
    def set_redo_enabled(self, enabled):
        """Enable/disable redo action"""
        self.redo_action.setEnabled(enabled)
    
    def set_simulation_running(self, running):
        """Update simulation button states"""
        self.start_action.setEnabled(not running)
        self.stop_action.setEnabled(running)


class ComponentToolbar(QToolBar):
    """Horizontal component selection toolbar"""
    
    # Signals
    component_selected = pyqtSignal(str, str)  # category, component_name
    
    def __init__(self, parent=None):
        super().__init__("Components", parent)
        self.setObjectName("ComponentToolbar")
        self.setMovable(False)
        
        self.current_category = "CPU"
        self.component_buttons = {}
        
        self._create_component_toolbar()
        
        print("✓ Component toolbar created")
    
    def _create_component_toolbar(self):
        """Create horizontal component toolbar"""
        # Category selector
        self.category_combo = QComboBox()
        self.category_combo.addItems(["CPU", "Memory", "Graphics", "Audio", "IO", "Custom"])
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        self.addWidget(QLabel("Category:"))
        self.addWidget(self.category_combo)
        self.addSeparator()
        
        # Component buttons container
        self.component_widget = QWidget()
        self.component_layout = QHBoxLayout(self.component_widget)
        self.component_layout.setContentsMargins(5, 2, 5, 2)
        self.component_layout.setSpacing(3)
        
        self.addWidget(self.component_widget)
        
        # Load initial components
        self._load_components_for_category("CPU")
    
    def _on_category_changed(self, category):
        """Handle category change"""
        self.current_category = category
        self._load_components_for_category(category)
    
    def _load_components_for_category(self, category):
        """Load components for selected category"""
        # Clear existing buttons
        for button in self.component_buttons.values():
            button.deleteLater()
        self.component_buttons.clear()
        
        # Component definitions by category
        components = {
            "CPU": ["Z80", "6502", "68000", "8080", "6809"],
            "Memory": ["2114", "4116", "2716", "2732", "6264"],
            "Graphics": ["TMS9918", "6845", "6560", "ULA"],
            "Audio": ["AY-3-8910", "SN76489", "SID"],
            "IO": ["6520", "6522", "8255", "Z80-PIO"],
            "Custom": ["Custom1", "Custom2", "Custom3"]
        }
        
        category_components = components.get(category, [])
        
        # Create buttons for components
        for component in category_components:
            button = QPushButton(component)
            button.setFixedSize(60, 30)
            button.setToolTip(f"Add {component} to canvas")
            button.clicked.connect(lambda checked, comp=component: 
                                 self.component_selected.emit(category, comp))
            
            self.component_layout.addWidget(button)
            self.component_buttons[component] = button
        
        # Add stretch to push buttons to left
        self.component_layout.addStretch()


def create_toolbars(main_window):
    """Create and setup all toolbars for main window"""
    # Main toolbar
    main_toolbar = MainToolbar(main_window)
    main_window.addToolBar(Qt.ToolBarArea.TopToolBarArea, main_toolbar)
    
    # Component toolbar  
    component_toolbar = ComponentToolbar(main_window)
    main_window.addToolBarBreak(Qt.ToolBarArea.TopToolBarArea)
    main_window.addToolBar(Qt.ToolBarArea.TopToolBarArea, component_toolbar)
    
    return main_toolbar, component_toolbar


# Export
__all__ = ['MainToolbar', 'ComponentToolbar', 'create_toolbars']


# Test function
def test_toolbars():
    """Test the toolbar system"""
    from PyQt6.QtWidgets import QApplication, QMainWindow
    import sys
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Toolbar Test")
    window.resize(800, 600)
    
    # Create toolbars
    main_toolbar, component_toolbar = create_toolbars(window)
    
    # Connect some test signals
    main_toolbar.new_project.connect(lambda: print("New project clicked"))
    component_toolbar.component_selected.connect(
        lambda cat, comp: print(f"Component selected: {comp} from {cat}")
    )
    
    window.show()
    print("Toolbar test window - close to continue")
    sys.exit(app.exec())


if __name__ == "__main__":
    test_toolbars()