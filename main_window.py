"""
X-Seti - June07 2025 - Main Window Implementation
Contains the primary window layout and menu system with robust import handling
"""

import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                           QDockWidget, QTreeWidget, QTreeWidgetItem, QSplitter,
                           QMessageBox, QFileDialog, QLabel, QStatusBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence

class MainWindow(QMainWindow):
    """Enhanced main window with robust import handling"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Retro System Emulator Builder")
        self.resize(1400, 900)
        
        # Initialize component references
        self.component_manager = None
        self.project_manager = None
        self.simulation_engine = None
        self.layer_manager = None
        
        # UI components
        self.canvas = None
        self.component_palette = None
        self.layer_controls = None
        self.menu_manager = None
        self.status_manager = None
        self.property_editor = None
        
        # Initialize managers with fallbacks
        self._initialize_managers()
        
        # Create UI components
        self._create_ui()
        self._create_docks()
        self._setup_connections()
        self._setup_hotkeys()
        
        # Update display
        self._update_window_title()
        self._update_status_counts()
        
        print("✓ Main window initialized")
    
    def _initialize_managers(self):
        """Initialize managers with fallback handling"""
        # Project Manager
        try:
            # Try managers package first
            try:
                from managers.project_manager import ProjectManager
                self.project_manager = ProjectManager()
                print("✓ ProjectManager loaded from managers")
            except ImportError:
                # Try root import
                from project_manager import ProjectManager
                self.project_manager = ProjectManager()
                print("✓ ProjectManager loaded from root")
        except ImportError as e:
            print(f"⚠️ ProjectManager import failed: {e}")
            self.project_manager = self._create_fallback_project_manager()
        
        # Layer Manager
        try:
            from managers.layer_manager import LayerManager
            self.layer_manager = LayerManager()
            print("✓ LayerManager loaded")
        except ImportError as e:
            print(f"⚠️ LayerManager import failed: {e}")
            self.layer_manager = self._create_fallback_layer_manager()
    
    def _create_ui(self):
        """Create main UI layout"""
        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Create canvas (center)
        self._create_canvas()
        if self.canvas:
            splitter.addWidget(self.canvas)
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_canvas(self):
        """Create the main PCB canvas"""
        try:
            # Try to import from ui package
            from ui import PCBCanvas, EnhancedPCBCanvas
            if EnhancedPCBCanvas:
                self.canvas = EnhancedPCBCanvas()
                print("✓ EnhancedPCBCanvas created")
            elif PCBCanvas:
                self.canvas = PCBCanvas()
                print("✓ PCBCanvas created")
            else:
                raise ImportError("No canvas classes available")
        except ImportError as e:
            print(f"⚠️ Canvas import failed: {e}")
            # Create minimal fallback canvas
            from PyQt6.QtWidgets import QGraphicsView
            self.canvas = QGraphicsView()
            print("✓ Fallback canvas created")
    
    def _create_docks(self):
        """Create dock widgets"""
        # Component palette dock
        self._create_component_palette_dock()
        
        # Layer controls dock
        self._create_layer_controls_dock()
        
        # Property editor dock
        self._create_property_editor_dock()
    
    def _create_component_palette_dock(self):
        """Create component palette dock"""
        try:
            from ui import EnhancedComponentPalette
            if EnhancedComponentPalette:
                self.component_palette = EnhancedComponentPalette()
                
                dock = QDockWidget("Components", self)
                dock.setWidget(self.component_palette)
                dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                                   Qt.DockWidgetArea.RightDockWidgetArea)
                
                self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
                print("✓ Component palette dock created")
            else:
                raise ImportError("EnhancedComponentPalette not available")
        except ImportError as e:
            print(f"⚠️ Component palette dock creation failed: {e}")
            # Create simple fallback
            self._create_fallback_component_dock()
    
    def _create_layer_controls_dock(self):
        """Create layer controls dock"""
        try:
            from ui import LayerControls
            if LayerControls:
                self.layer_controls = LayerControls()
                
                dock = QDockWidget("Layers", self)
                dock.setWidget(self.layer_controls)
                dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                                   Qt.DockWidgetArea.RightDockWidgetArea)
                
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
                print("✓ Layer controls dock created")
            else:
                raise ImportError("LayerControls not available")
        except ImportError as e:
            print(f"⚠️ Layer controls dock creation failed: {e}")
            self._create_fallback_layer_dock()
    
    def _create_property_editor_dock(self):
        """Create property editor dock"""
        try:
            from ui import PropertyEditor
            if PropertyEditor:
                self.property_editor = PropertyEditor()
                
                dock = QDockWidget("Properties", self)
                dock.setWidget(self.property_editor)
                dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                                   Qt.DockWidgetArea.RightDockWidgetArea)
                
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
                print("✓ Property editor dock created")
            else:
                raise ImportError("PropertyEditor not available")
        except ImportError as e:
            print(f"⚠️ Property editor dock creation failed: {e}")
            self._create_fallback_property_dock()
    
    def _create_menu_bar(self):
        """Create menu bar"""
        try:
            from ui import MenuBarManager
            if MenuBarManager:
                self.menu_manager = MenuBarManager(self.menuBar(), self)
                print("✓ Menu bar created")
            else:
                raise ImportError("MenuBarManager not available")
        except ImportError as e:
            print(f"⚠️ Menu bar creation failed: {e}")
            self._create_fallback_menu_bar()
    
    def _create_status_bar(self):
        """Create status bar"""
        try:
            from ui import StatusBarManager
            if StatusBarManager:
                self.status_manager = StatusBarManager(self.statusBar())
                print("✓ Status bar created")
            else:
                raise ImportError("StatusBarManager not available")
        except ImportError as e:
            print(f"⚠️ Status bar creation failed: {e}")
            self._create_fallback_status_bar()
    
    def _setup_connections(self):
        """Setup signal connections"""
        # Connect component palette to canvas
        if self.component_palette and hasattr(self.component_palette, 'component_selected'):
            if self.canvas and hasattr(self.canvas, 'add_component'):
                self.component_palette.component_selected.connect(self._on_component_selected)
        
        # Connect canvas to property editor
        if self.canvas and hasattr(self.canvas, 'component_selected'):
            self.canvas.component_selected.connect(self._on_canvas_component_selected)
    
    def _setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        # File operations
        QShortcut(QKeySequence.StandardKey.New, self, self._on_new_project)
        QShortcut(QKeySequence.StandardKey.Open, self, self._on_open_project)
        QShortcut(QKeySequence.StandardKey.Save, self, self._on_save_project)
        
        # Edit operations
        QShortcut(QKeySequence.StandardKey.Undo, self, self._on_undo)
        QShortcut(QKeySequence.StandardKey.Redo, self, self._on_redo)
        QShortcut(QKeySequence.StandardKey.Copy, self, self._on_copy)
        QShortcut(QKeySequence.StandardKey.Paste, self, self._on_paste)
        
        # View operations
        QShortcut(QKeySequence("Ctrl++"), self, self._on_zoom_in)
        QShortcut(QKeySequence("Ctrl+-"), self, self._on_zoom_out)
        QShortcut(QKeySequence("Ctrl+0"), self, self._on_fit_window)
    
    def _on_component_selected(self, component_type: str, component_name: str):
        """Handle component selection from palette"""
        print(f"Component selected: {component_type} - {component_name}")
        # TODO: Set canvas to component placement mode
    
    def _on_canvas_component_selected(self, component):
        """Handle component selection on canvas"""
        print(f"Canvas component selected: {component}")
        # TODO: Update property editor with component properties
    
    def _update_window_title(self):
        """Update window title with project info"""
        title = "Visual Retro System Emulator Builder"
        if self.project_manager and hasattr(self.project_manager, 'current_project'):
            if self.project_manager.current_project:
                project_name = getattr(self.project_manager.current_project, 'name', 'Untitled')
                title += f" - {project_name}"
        self.setWindowTitle(title)
    
    def _update_status_counts(self):
        """Update status bar with component/connection counts"""
        if self.status_manager:
            # Get counts from project manager or canvas
            component_count = 0
            connection_count = 0
            
            if self.project_manager and hasattr(self.project_manager, 'current_project'):
                if self.project_manager.current_project:
                    project = self.project_manager.current_project
                    if hasattr(project, 'components_data'):
                        component_count = len(project.components_data)
                    if hasattr(project, 'connections_data'):
                        connection_count = len(project.connections_data)
            
            self.status_manager.update_component_count(component_count)
            self.status_manager.update_connection_count(connection_count)
    
    # Fallback creation methods
    def _create_fallback_project_manager(self):
        """Create fallback project manager"""
        class FallbackProjectManager:
            def __init__(self):
                self.current_project = None
            def new_project(self):
                print("New project (fallback)")
            def open_project_dialog(self):
                print("Open project (fallback)")
            def save_current_project(self):
                print("Save project (fallback)")
        
        return FallbackProjectManager()
    
    def _create_fallback_layer_manager(self):
        """Create fallback layer manager"""
        class FallbackLayerManager:
            def __init__(self):
                self.layers = ['Component', 'PCB', 'Gerber']
                self.active_layer = 'Component'
        
        return FallbackLayerManager()
    
    def _create_fallback_component_dock(self):
        """Create fallback component dock"""
        from PyQt6.QtWidgets import QListWidget
        
        widget = QListWidget()
        widget.addItems(['6502 CPU', 'Z80 CPU', '68000 CPU', 'RAM', 'ROM'])
        
        dock = QDockWidget("Components", self)
        dock.setWidget(widget)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                           Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
    
    def _create_fallback_layer_dock(self):
        """Create fallback layer dock"""
        from PyQt6.QtWidgets import QVBoxLayout, QPushButton
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        for layer in ['Component', 'PCB', 'Gerber']:
            btn = QPushButton(layer)
            btn.setCheckable(True)
            if layer == 'Component':
                btn.setChecked(True)
            layout.addWidget(btn)
        
        dock = QDockWidget("Layers", self)
        dock.setWidget(widget)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
    
    def _create_fallback_property_dock(self):
        """Create fallback property dock"""
        widget = QLabel("Select a component\nto view properties")
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget.setStyleSheet("color: gray; font-style: italic;")
        
        dock = QDockWidget("Properties", self)
        dock.setWidget(widget)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
    
    def _create_fallback_menu_bar(self):
        """Create fallback menu bar"""
        # File menu
        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction('&New Project', self._on_new_project)
        file_menu.addAction('&Open Project...', self._on_open_project)
        file_menu.addAction('&Save Project', self._on_save_project)
        file_menu.addSeparator()
        file_menu.addAction('E&xit', self.close)
        
        # Help menu
        help_menu = self.menuBar().addMenu('&Help')
        help_menu.addAction('&About', self._on_about)
    
    def _create_fallback_status_bar(self):
        """Create fallback status bar"""
        self.statusBar().showMessage("Ready")
    
    # Menu action handlers
    def _on_new_project(self):
        """New project handler"""
        if self.project_manager:
            self.project_manager.new_project()
        self._update_window_title()
        
    def _on_open_project(self):
        """Open project handler"""
        if self.project_manager:
            self.project_manager.open_project_dialog()
        self._update_window_title()
        
    def _on_save_project(self):
        """Save project handler"""
        if self.project_manager:
            self.project_manager.save_current_project()
            
    def _on_undo(self):
        """Undo handler"""
        print("Undo requested")
        
    def _on_redo(self):
        """Redo handler"""
        print("Redo requested")
        
    def _on_copy(self):
        """Copy handler"""
        print("Copy requested")
        
    def _on_paste(self):
        """Paste handler"""
        print("Paste requested")
        
    def _on_zoom_in(self):
        """Zoom in handler"""
        if self.canvas and hasattr(self.canvas, 'zoom_in'):
            self.canvas.zoom_in()
            
    def _on_zoom_out(self):
        """Zoom out handler"""
        if self.canvas and hasattr(self.canvas, 'zoom_out'):
            self.canvas.zoom_out()
            
    def _on_fit_window(self):
        """Fit to window handler"""
        if self.canvas and hasattr(self.canvas, 'fit_in_view'):
            self.canvas.fit_in_view()
            
    def _on_about(self):
        """About dialog handler"""
        QMessageBox.about(self, "About", 
                         "Visual Retro System Emulator Builder\nVersion 1.0.0\n\nX-Seti - June 2025")
    
    # Public methods for external access
    def set_component_manager(self, manager):
        """Set component manager reference"""
        self.component_manager = manager
        
    def set_project_manager(self, manager):
        """Set project manager reference"""
        self.project_manager = manager
        self._update_window_title()
        
    def set_simulation_engine(self, engine):
        """Set simulation engine reference"""
        self.simulation_engine = engine