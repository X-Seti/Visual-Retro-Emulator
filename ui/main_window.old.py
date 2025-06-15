"""
X-Seti - June07 2025 - Main Window Implementation
Contains the primary window layout and menu system with robust import handling
"""
#this goes in ui/
import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                           QDockWidget, QTreeWidget, QTreeWidgetItem, QSplitter,
                           QMessageBox, QFileDialog, QLabel, QStatusBar,
                           QPushButton, QToolBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence, QAction

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
    
    def _create_fallback_project_manager(self):
        """Create fallback project manager"""
        class FallbackProjectManager:
            def __init__(self):
                self.current_project = None
                self.project_name = "Untitled Project"
            
            def new_project(self):
                pass
            
            def save_project(self):
                pass
                
            def load_project(self):
                pass
        
        return FallbackProjectManager()
    
    def _create_fallback_layer_manager(self):
        """Create fallback layer manager"""
        class FallbackLayerManager:
            def __init__(self):
                self.current_layer = "default"
                self.layers = ["default"]
            
            def get_current_layer(self):
                return self.current_layer
            
            def set_current_layer(self, layer):
                self.current_layer = layer
        
        return FallbackLayerManager()
    
    def _create_ui(self):
        """Create the main UI components"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for main content
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Left panel (component palette)
        self._create_component_palette()
        if self.component_palette:
            main_splitter.addWidget(self.component_palette)
        
        # Center panel (canvas)
        self._create_canvas()
        if self.canvas:
            main_splitter.addWidget(self.canvas)
        
        # Set splitter proportions
        main_splitter.setSizes([300, 1100])  # Left panel smaller
        
        # Create menus and toolbars
        self._create_menus()
        self._create_toolbars()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_component_palette(self):
        """Create component palette with fallback"""
        try:
            from ui.component_palette import EnhancedComponentPalette
            self.component_palette = EnhancedComponentPalette()
            print("✓ Enhanced component palette loaded")
        except ImportError as e:
            print(f"⚠️ Using fallback component palette: {e}")
            # Create simple fallback
            self.component_palette = QWidget()
            layout = QVBoxLayout(self.component_palette)
            
            # Add some basic components
            components = [
                ("68000 CPU", "cpu"),
                ("6502 CPU", "cpu"),
                ("Z80 CPU", "cpu"),
                ("Paula", "audio"),
                ("Denise", "video"),
                ("Agnus", "video")
            ]
            
            for name, comp_type in components:
                btn = QPushButton(name)
                btn.clicked.connect(lambda checked, n=name, t=comp_type: self._add_component(t, n))
                layout.addWidget(btn)
            
            layout.addStretch()
    
    def _create_canvas(self):
        """Create canvas with fallback"""
        try:
            from ui.canvas import EnhancedPCBCanvas
            self.canvas = EnhancedPCBCanvas()
            print("✓ Enhanced PCB canvas loaded")
        except ImportError as e:
            print(f"⚠️ Using fallback canvas: {e}")
            # Create simple fallback
            self.canvas = QWidget()
            self.canvas.setMinimumSize(800, 600)
            self.canvas.setStyleSheet("background-color: #2a2a3a; border: 1px solid #555;")
            
            layout = QVBoxLayout(self.canvas)
            label = QLabel("Canvas Area\n(Canvas module not available)")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: white; font-size: 14px;")
            layout.addWidget(label)
    
    def _create_docks(self):
        """Create dock widgets"""
        # Properties dock
        try:
            from ui.properties_panel import PropertiesPanel
            self.property_editor = PropertiesPanel()
            properties_dock = QDockWidget("Properties", self)
            properties_dock.setWidget(self.property_editor)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, properties_dock)
            print("✓ Properties panel loaded")
        except ImportError as e:
            print(f"⚠️ Properties panel not available, creating fallback: {e}")
            # Create fallback properties panel
            self.property_editor = QWidget()
            prop_layout = QVBoxLayout(self.property_editor)
            
            from PyQt6.QtWidgets import QTextEdit, QLabel
            prop_layout.addWidget(QLabel("Properties"))
            
            self.property_text = QTextEdit()
            self.property_text.setMaximumHeight(200)
            self.property_text.setPlainText("Select a component to view properties")
            prop_layout.addWidget(self.property_text)
            
            prop_layout.addStretch()
            
            properties_dock = QDockWidget("Properties", self)
            properties_dock.setWidget(self.property_editor)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, properties_dock)
            print("✓ Fallback properties panel created")
        
        # Layer controls dock
        try:
            from ui.layer_controls import LayerControls
            self.layer_controls = LayerControls()
            layer_dock = QDockWidget("Layers", self)
            layer_dock.setWidget(self.layer_controls)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layer_dock)
            print("✓ Layer controls loaded")
        except ImportError as e:
            print(f"⚠️ Layer controls not available, creating fallback: {e}")
            # Create fallback layer controls
            self.layer_controls = QWidget()
            layer_layout = QVBoxLayout(self.layer_controls)
            
            from PyQt6.QtWidgets import QListWidget, QListWidgetItem
            layer_layout.addWidget(QLabel("Layers"))
            
            self.layer_list = QListWidget()
            self.layer_list.addItem(QListWidgetItem("Components"))
            self.layer_list.addItem(QListWidgetItem("Connections"))
            self.layer_list.addItem(QListWidgetItem("Background"))
            layer_layout.addWidget(self.layer_list)
            
            layer_dock = QDockWidget("Layers", self)
            layer_dock.setWidget(self.layer_controls)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layer_dock)
            print("✓ Fallback layer controls created")
        
        # Component info dock
        self.component_info = QWidget()
        info_layout = QVBoxLayout(self.component_info)
        
        info_layout.addWidget(QLabel("Component Info"))
        
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(150)
        self.info_text.setPlainText("No component selected")
        info_layout.addWidget(self.info_text)
        
        info_dock = QDockWidget("Component Info", self)
        info_dock.setWidget(self.component_info)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, info_dock)
        print("✓ Component info panel created")
    
    def _create_menus(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Project", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Project", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Project", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        grid_action = QAction("Toggle Grid", self)
        grid_action.setCheckable(True)
        grid_action.setChecked(True)
        grid_action.triggered.connect(self._toggle_grid)
        view_menu.addAction(grid_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        chip_gen_action = QAction("Generate Chip Images", self)
        chip_gen_action.triggered.connect(self._generate_chip_images)
        tools_menu.addAction(chip_gen_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbars(self):
        """Create toolbars"""
        # Main toolbar
        main_toolbar = QToolBar("Main", self)
        self.addToolBar(main_toolbar)
        
        # Add common actions
        new_action = QAction("New", self)
        new_action.triggered.connect(self._new_project)
        main_toolbar.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(self._open_project)
        main_toolbar.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self._save_project)
        main_toolbar.addAction(save_action)
        
        main_toolbar.addSeparator()
        
        # Simulation controls
        sim_toolbar = QToolBar("Simulation", self)
        self.addToolBar(sim_toolbar)
        
        play_action = QAction("Play", self)
        play_action.triggered.connect(self._start_simulation)
        sim_toolbar.addAction(play_action)
        
        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self._pause_simulation)
        sim_toolbar.addAction(pause_action)
        
        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self._stop_simulation)
        sim_toolbar.addAction(stop_action)
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add status labels
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        # Add permanent widgets
        self.component_count_label = QLabel("Components: 0")
        self.status_bar.addPermanentWidget(self.component_count_label)
        
        self.connection_count_label = QLabel("Connections: 0")
        self.status_bar.addPermanentWidget(self.connection_count_label)
    
    def _setup_connections(self):
        """Setup signal connections"""
        # Connect canvas signals if available
        if self.canvas and hasattr(self.canvas, 'component_added'):
            self.canvas.component_added.connect(self._on_component_added)
        
        if self.canvas and hasattr(self.canvas, 'component_removed'):
            self.canvas.component_removed.connect(self._on_component_removed)
        
        if self.canvas and hasattr(self.canvas, 'component_selected'):
            self.canvas.component_selected.connect(self._on_component_selected)
    
    def _setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        # Delete key for removing components
        delete_shortcut = QShortcut(QKeySequence.StandardKey.Delete, self)
        delete_shortcut.activated.connect(self._delete_selected)
        
        # Ctrl+A for select all
        select_all_shortcut = QShortcut(QKeySequence.StandardKey.SelectAll, self)
        select_all_shortcut.activated.connect(self._select_all)
        
        # Ctrl+Z for undo
        undo_shortcut = QShortcut(QKeySequence.StandardKey.Undo, self)
        undo_shortcut.activated.connect(self._undo)
        
        # Ctrl+Y for redo
        redo_shortcut = QShortcut(QKeySequence.StandardKey.Redo, self)
        redo_shortcut.activated.connect(self._redo)
    
    def _update_window_title(self):
        """Update window title"""
        project_name = "Untitled Project"
        if self.project_manager and hasattr(self.project_manager, 'project_name'):
            project_name = self.project_manager.project_name
        
        self.setWindowTitle(f"Visual Retro System Emulator Builder - {project_name}")
    
    def _update_status_counts(self):
        """Update status bar counts"""
        component_count = 0
        connection_count = 0
        
        if self.canvas and hasattr(self.canvas, 'components'):
            component_count = len(self.canvas.components)
        
        if self.canvas and hasattr(self.canvas, 'connections'):
            connection_count = len(self.canvas.connections)
        
        self.component_count_label.setText(f"Components: {component_count}")
        self.connection_count_label.setText(f"Connections: {connection_count}")
    
    # Menu action handlers
    def _new_project(self):
        """Create new project"""
        print("Creating new project...")
        if self.project_manager:
            self.project_manager.new_project()
        self._update_window_title()
        self.status_label.setText("New project created")
    
    def _open_project(self):
        """Open project"""
        print("Opening project...")
        filename, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Project Files (*.json)")
        if filename:
            if self.project_manager:
                self.project_manager.load_project(filename)
            self._update_window_title()
            self.status_label.setText(f"Opened project: {filename}")
    
    def _save_project(self):
        """Save project"""
        print("Saving project...")
        if self.project_manager:
            self.project_manager.save_project()
        self.status_label.setText("Project saved")
    
    def _toggle_grid(self):
        """Toggle grid visibility"""
        if self.canvas and hasattr(self.canvas, 'set_grid_visible'):
            current = getattr(self.canvas, 'grid_visible', True)
            self.canvas.set_grid_visible(not current)
            self.status_label.setText(f"Grid {'shown' if not current else 'hidden'}")
    
    def _generate_chip_images(self):
        """Generate chip images"""
        try:
            from retro_chip_generator import RetroChipGenerator
            generator = RetroChipGenerator()
            generator.generate_images()
            QMessageBox.information(self, "Success", "Chip images generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate chip images:\n{str(e)}")
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About", 
            "Visual Retro System Emulator Builder\n\n"
            "A tool for designing and emulating retro computer systems.\n"
            "Built with PyQt6 and love for retro computing.\n\n"
            "© 2025 X-Seti")
    
    def _start_simulation(self):
        """Start simulation"""
        print("Starting simulation...")
        if self.simulation_engine:
            self.simulation_engine.start()
        self.status_label.setText("Simulation started")
    
    def _pause_simulation(self):
        """Pause simulation"""
        print("Pausing simulation...")
        if self.simulation_engine:
            self.simulation_engine.pause()
        self.status_label.setText("Simulation paused")
    
    def _stop_simulation(self):
        """Stop simulation"""
        print("Stopping simulation...")
        if self.simulation_engine:
            self.simulation_engine.stop()
        self.status_label.setText("Simulation stopped")
    
    # Canvas event handlers
    def _on_component_added(self, component):
        """Handle component added"""
        print(f"Component added: {getattr(component, 'name', 'Unknown')}")
        self._update_status_counts()
    
    def _on_component_removed(self, component):
        """Handle component removed"""
        print(f"Component removed: {getattr(component, 'name', 'Unknown')}")
        self._update_status_counts()
    
    def _on_component_selected(self, component):
        """Handle component selected"""
        print(f"Component selected: {getattr(component, 'name', 'Unknown')}")
        
        # Update property editor
        if self.property_editor and hasattr(self.property_editor, 'set_component'):
            self.property_editor.set_component(component)
        elif hasattr(self, 'property_text'):
            # Update fallback property text
            info = f"Component: {getattr(component, 'name', 'Unknown')}\n"
            info += f"Type: {getattr(component, 'component_type', 'unknown')}\n"
            info += f"ID: {getattr(component, 'id', 'none')}\n"
            info += f"Position: {component.pos()}\n"
            info += f"Size: {component.boundingRect().size()}"
            self.property_text.setPlainText(info)
        
        # Update component info panel
        if hasattr(self, 'info_text'):
            comp_info = f"Selected: {getattr(component, 'name', 'Unknown')}\n"
            comp_info += f"Visible: {component.isVisible()}\n"
            comp_info += f"Selected: {component.isSelected()}\n"
            comp_info += f"Z-Value: {component.zValue()}"
            self.info_text.setPlainText(comp_info)
    
    # Keyboard shortcut handlers
    def _delete_selected(self):
        """Delete selected components"""
        if self.canvas and hasattr(self.canvas, 'selected_components'):
            for component in self.canvas.selected_components.copy():
                self.canvas.remove_component(component)
        self.status_label.setText("Selected components deleted")
    
    def _select_all(self):
        """Select all components"""
        if self.canvas and hasattr(self.canvas, 'components'):
            for component in self.canvas.components.values():
                component.setSelected(True)
        self.status_label.setText("All components selected")
    
    def _undo(self):
        """Undo last action"""
        print("Undo requested")
        self.status_label.setText("Undo")
    
    def _redo(self):
        """Redo last action"""
        print("Redo requested")
        self.status_label.setText("Redo")
    
    def _add_component(self, component_type, name):
        """Add component to canvas"""
        if self.canvas and hasattr(self.canvas, 'add_component'):
            self.canvas.add_component(component_type, name)
        else:
            print(f"Would add component: {name} ({component_type})")
    
    # Setter methods for dependency injection
    def set_component_manager(self, manager):
        """Set component manager"""
        self.component_manager = manager
        print("✓ Component manager set")
    
    def set_project_manager(self, manager):
        """Set project manager"""
        self.project_manager = manager
        self._update_window_title()
        print("✓ Project manager set")
    
    def set_simulation_engine(self, engine):
        """Set simulation engine"""
        self.simulation_engine = engine
        print("✓ Simulation engine set")
    
    def closeEvent(self, event):
        """Handle window close event"""
        print("Main window closing...")
        # Cleanup if needed
        event.accept()
