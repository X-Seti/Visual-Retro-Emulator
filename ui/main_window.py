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
        """Create the main user interface with error handling"""
        # Create central canvas
        try:
            # Try to import the canvas
            try:
                from .canvas import EnhancedPCBCanvas
                self.canvas = EnhancedPCBCanvas()
                print("✓ Canvas loaded from ui package")
            except ImportError:
                # Try alternative canvas names
                try:
                    from .enhanced_canvas import EnhancedPCBCanvas
                    self.canvas = EnhancedPCBCanvas()
                    print("✓ Enhanced canvas loaded")
                except ImportError:
                    # Try other possible names
                    try:
                        from .canvas import PCBCanvas
                        self.canvas = PCBCanvas()
                        print("✓ PCB Canvas loaded")
                    except ImportError:
                        # Use fallback canvas
                        raise ImportError("No canvas implementation found")
        except ImportError as e:
            print(f"⚠️ Canvas import failed: {e}")
            self.canvas = self._create_fallback_canvas()
        
        # Set canvas as central widget
        if self.canvas:
            self.setCentralWidget(self.canvas)
            # Connect layer manager if canvas has one
            if hasattr(self.canvas, 'layer_manager'):
                self.layer_manager = self.canvas.layer_manager
        
        # Create menu bar
        try:
            from .menu_bar import MenuBarManager, RetroEmulatorMenuBar
            # Try both possible class names
            try:
                self.menu_manager = MenuBarManager(self)
                # The menu bar IS the menu bar - don't call create_menu_bar()
                self.setMenuBar(self.menu_manager)
                print("✓ Menu bar created with MenuBarManager")
            except:
                # Try RetroEmulatorMenuBar directly
                self.menu_manager = RetroEmulatorMenuBar(self)
                self.setMenuBar(self.menu_manager)
                print("✓ Menu bar created with RetroEmulatorMenuBar")
        except ImportError as e:
            print(f"⚠️ Menu bar import failed: {e}")
            self._create_fallback_menu_bar()
        
        # Create status bar
        try:
            from .status_bar import StatusBarManager
            self.status_manager = StatusBarManager(self)
            self.setStatusBar(self.status_manager)
            print("✓ Status bar created")
        except ImportError as e:
            print(f"⚠️ Status bar import failed: {e}")
            self._create_fallback_status_bar()
    
    def _create_docks(self):
        """Create dock widgets with error handling"""
        # Component Palette Dock
        try:
            from .component_palette import EnhancedComponentPalette
            self.component_palette = EnhancedComponentPalette()
            
            palette_dock = QDockWidget("Component Palette", self)
            palette_dock.setWidget(self.component_palette)
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, palette_dock)
            print("✓ Component palette dock created")
        except ImportError as e:
            print(f"⚠️ Component palette import failed: {e}")
            self._create_fallback_component_palette()
        
        # Layer Controls Dock
        try:
            from .layer_controls import LayerControlWidget
            self.layer_controls = LayerControlWidget()
            
            layer_dock = QDockWidget("Layer Controls", self)
            layer_dock.setWidget(self.layer_controls)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layer_dock)
            print("✓ Layer controls dock created")
        except ImportError as e:
            print(f"⚠️ Layer controls import failed: {e}")
            self._create_fallback_layer_controls()
        
        # Property Editor Dock
        try:
            from .property_editor import PropertyEditorWidget
            self.property_editor = PropertyEditorWidget()
            
            props_dock = QDockWidget("Properties", self)
            props_dock.setWidget(self.property_editor)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, props_dock)
            print("✓ Property editor dock created")
        except ImportError as e:
            print(f"⚠️ Property editor import failed: {e}")
            self._create_fallback_property_editor()
    
    def _setup_connections(self):
        """Setup signal connections"""
        # Connect canvas signals if available
        if self.canvas and hasattr(self.canvas, 'component_selected'):
            try:
                if self.property_editor and hasattr(self.property_editor, 'set_component'):
                    self.canvas.component_selected.connect(self.property_editor.set_component)
            except AttributeError:
                pass
        
        # Connect menu signals to project manager
        if self.menu_manager and hasattr(self.menu_manager, 'signals'):
            try:
                # File menu connections
                self.menu_manager.signals.newProject.connect(self._new_project)
                self.menu_manager.signals.openProject.connect(self._open_project)
                self.menu_manager.signals.saveProject.connect(self._save_project)
                self.menu_manager.signals.saveProjectAs.connect(self._save_project_as)
                
                # Edit menu connections
                self.menu_manager.signals.undo.connect(self._undo)
                self.menu_manager.signals.redo.connect(self._redo)
                
                # View menu connections
                self.menu_manager.signals.zoomIn.connect(self._zoom_in)
                self.menu_manager.signals.zoomOut.connect(self._zoom_out)
                self.menu_manager.signals.zoomFit.connect(self._fit_to_window)
                self.menu_manager.signals.toggleGrid.connect(self._toggle_grid)
                
                # Component menu connections
                self.menu_manager.signals.addComponent.connect(self._add_component_dialog)
                
                print("✓ Menu signals connected")
            except Exception as e:
                print(f"⚠️ Error connecting menu signals: {e}")
        
        # Connect component palette signals
        if self.component_palette:
            try:
                if hasattr(self.component_palette, 'componentDoubleClicked'):
                    self.component_palette.componentDoubleClicked.connect(self._add_component_from_palette)
                print("✓ Component palette signals connected")
            except Exception as e:
                print(f"⚠️ Error connecting component palette signals: {e}")
    
    # ========== MENU ACTIONS ==========
    
    def _new_project(self):
        """Create new project"""
        if self.project_manager and hasattr(self.project_manager, 'new_project'):
            self.project_manager.new_project("New Project")
        
        # Clear canvas
        if self.canvas and hasattr(self.canvas, 'clear_canvas'):
            self.canvas.clear_canvas()
        
        self._update_window_title()
        print("✓ New project created")
    
    def _open_project(self, filename=None):
        """Open project"""
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Open Project", "", "Project Files (*.json);;All Files (*)")
        
        if filename and self.project_manager:
            if hasattr(self.project_manager, 'open_project'):
                if self.project_manager.open_project(filename):
                    # Load project data into canvas
                    self._load_project_to_canvas()
                    self._update_window_title()
                    print(f"✓ Project opened: {filename}")
    
    def _save_project(self):
        """Save project"""
        if self.project_manager:
            # Save canvas state to project
            if self.canvas and hasattr(self.canvas, 'save_to_dict'):
                canvas_data = self.canvas.save_to_dict()
                if hasattr(self.project_manager, 'update_canvas_state'):
                    self.project_manager.update_canvas_state(canvas_data)
            
            # Save project
            if hasattr(self.project_manager, 'save_project'):
                if self.project_manager.save_project():
                    self._update_window_title()
                    print("✓ Project saved")
    
    def _save_project_as(self, filename=None):
        """Save project as"""
        if not filename:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Project As", "", "Project Files (*.json);;All Files (*)")
        
        if filename and self.project_manager:
            # Ensure .json extension
            if not filename.endswith('.json'):
                filename += '.json'
            
            # Save canvas state
            if self.canvas and hasattr(self.canvas, 'save_to_dict'):
                canvas_data = self.canvas.save_to_dict()
                if hasattr(self.project_manager, 'update_canvas_state'):
                    self.project_manager.update_canvas_state(canvas_data)
            
            # Save project
            if hasattr(self.project_manager, 'save_project'):
                if self.project_manager.save_project(filename):
                    self._update_window_title()
                    print(f"✓ Project saved as: {filename}")
    
    def _load_project_to_canvas(self):
        """Load project data to canvas"""
        if not self.project_manager or not self.canvas:
            return
        
        try:
            if hasattr(self.project_manager, 'get_canvas_state'):
                canvas_data = self.project_manager.get_canvas_state()
                if canvas_data and hasattr(self.canvas, 'load_from_dict'):
                    self.canvas.load_from_dict(canvas_data)
                    print("✓ Project data loaded to canvas")
        except Exception as e:
            print(f"⚠️ Error loading project to canvas: {e}")
    
    def _add_component_from_palette(self, component_data):
        """Add component from palette double-click"""
        if self.canvas and hasattr(self.canvas, 'add_component'):
            # Add component at center of view
            center = self.canvas.mapToScene(self.canvas.viewport().rect().center())
            component = self.canvas.add_component(
                component_data.get('type', 'unknown'),
                component_data.get('name', 'Component'),
                position=center
            )
            
            if component:
                # Set additional component properties
                if hasattr(component, 'component_data'):
                    component.component_data = component_data
                print(f"✓ Added component: {component_data.get('name')}")
    
    def _add_component_dialog(self, component_type=None):
        """Show add component dialog"""
        # This would open a component selection dialog
        print(f"Add component dialog for type: {component_type}")
    
    def _undo(self):
        """Undo last action"""
        print("Undo action")
        # Implement undo functionality
    
    def _redo(self):
        """Redo last action"""
        print("Redo action")
        # Implement redo functionality
    
    def _toggle_grid(self, visible):
        """Toggle grid visibility"""
        if self.canvas and hasattr(self.canvas, 'set_grid_visible'):
            self.canvas.set_grid_visible(visible)
            print(f"Grid {'visible' if visible else 'hidden'}")
    
    def _setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        try:
            # Basic shortcuts
            QShortcut(QKeySequence("Ctrl+N"), self, self._new_project)
            QShortcut(QKeySequence("Ctrl+O"), self, self._open_project)
            QShortcut(QKeySequence("Ctrl+S"), self, self._save_project)
            QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
            
            # View shortcuts
            QShortcut(QKeySequence("Ctrl+0"), self, self._fit_to_window)
            QShortcut(QKeySequence("Ctrl++"), self, self._zoom_in)
            QShortcut(QKeySequence("Ctrl+-"), self, self._zoom_out)
            
            print("✓ Hotkeys setup")
        except Exception as e:
            print(f"⚠️ Hotkey setup failed: {e}")
    
    # ========== FALLBACK CREATORS ==========
    
    def _create_fallback_project_manager(self):
        """Create fallback project manager"""
        class FallbackProjectManager:
            def __init__(self):
                self.current_file = None
                self.modified = False
            
            def get_current_file(self):
                return self.current_file
            
            def is_modified(self):
                return self.modified
        
        return FallbackProjectManager()
    
    def _create_fallback_layer_manager(self):
        """Create fallback layer manager"""
        class FallbackLayerManager:
            def __init__(self):
                self.current_layer = "chip"
            
            def get_current_layer(self):
                return self.current_layer
        
        return FallbackLayerManager()
    
    def _create_fallback_canvas(self):
        """Create fallback canvas"""
        from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
        
        class FallbackCanvas(QGraphicsView):
            def __init__(self):
                super().__init__()
                self.scene = QGraphicsScene()
                self.setScene(self.scene)
                self.selected_components = []
                self.layer_manager = None
                print("⚠️ Using fallback canvas")
            
            def fitInView(self, rect, mode):
                super().fitInView(rect, mode)
        
        return FallbackCanvas()
    
    def _create_fallback_menu_bar(self):
        """Create fallback menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New", self._new_project)
        file_menu.addAction("Open", self._open_project)
        file_menu.addAction("Save", self._save_project)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Fit to Window", self._fit_to_window)
        view_menu.addAction("Zoom In", self._zoom_in)
        view_menu.addAction("Zoom Out", self._zoom_out)
        
        print("⚠️ Using fallback menu bar")
    
    def _create_fallback_status_bar(self):
        """Create fallback status bar"""
        self.status_manager = self.statusBar()
        self.status_manager.showMessage("Ready")
        print("⚠️ Using fallback status bar")
    
    def _create_fallback_component_palette(self):
        """Create fallback component palette"""
        from PyQt6.QtWidgets import QTreeWidget
        
        self.component_palette = QTreeWidget()
        self.component_palette.setHeaderLabel("Components")
        
        # Add some basic items
        cpu_item = QTreeWidgetItem(["CPU"])
        cpu_item.addChild(QTreeWidgetItem(["6502"]))
        cpu_item.addChild(QTreeWidgetItem(["68000"]))
        self.component_palette.addTopLevelItem(cpu_item)
        
        palette_dock = QDockWidget("Components", self)
        palette_dock.setWidget(self.component_palette)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, palette_dock)
        
        print("⚠️ Using fallback component palette")
    
    def _create_fallback_layer_controls(self):
        """Create fallback layer controls"""
        from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QPushButton("Chip Layer"))
        layout.addWidget(QPushButton("PCB Layer"))
        layout.addWidget(QPushButton("Gerber Layer"))
        
        self.layer_controls = widget
        
        layer_dock = QDockWidget("Layers", self)
        layer_dock.setWidget(widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layer_dock)
        
        print("⚠️ Using fallback layer controls")
    
    def _create_fallback_property_editor(self):
        """Create fallback property editor"""
        from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Properties"))
        layout.addWidget(QLabel("Select a component to edit properties"))
        
        self.property_editor = widget
        
        props_dock = QDockWidget("Properties", self)
        props_dock.setWidget(widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, props_dock)
        
        print("⚠️ Using fallback property editor")
    
    # ========== MENU ACTIONS ==========
    
    def _new_project(self):
        """Create new project"""
        if self.project_manager and hasattr(self.project_manager, 'new_project'):
            self.project_manager.new_project()
        self._update_window_title()
        print("New project created")
    
    def _open_project(self):
        """Open project"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Project Files (*.json);;All Files (*)")
        
        if filename:
            if self.project_manager and hasattr(self.project_manager, 'open_project'):
                self.project_manager.open_project(filename)
            self._update_window_title()
            print(f"Project opened: {filename}")
    
    def _save_project(self):
        """Save project"""
        if self.project_manager and hasattr(self.project_manager, 'save_project'):
            self.project_manager.save_project()
        self._update_window_title()
        print("Project saved")
    
    def _fit_to_window(self):
        """Fit view to window"""
        if self.canvas and hasattr(self.canvas, 'fitInView'):
            try:
                self.canvas.fitInView(self.canvas.scene.itemsBoundingRect(), 
                                     Qt.AspectRatioMode.KeepAspectRatio)
                print("Fit to window")
            except:
                print("⚠️ Fit to window failed")
    
    def _zoom_in(self):
        """Zoom in"""
        if self.canvas:
            self.canvas.scale(1.2, 1.2)
            print("Zoomed in")
    
    def _zoom_out(self):
        """Zoom out"""
        if self.canvas:
            self.canvas.scale(0.8, 0.8)
            print("Zoomed out")
    
    # ========== UTILITY METHODS ==========
    
    def _update_status_counts(self):
        """Update status bar counts"""
        if not self.status_manager:
            return
        
        try:
            # Try to get component counts from canvas
            component_count = 0
            connection_count = 0
            selected_count = 0
            
            if self.canvas and hasattr(self.canvas, 'scene'):
                items = self.canvas.scene.items()
                # Count different types of items
                for item in items:
                    item_type = type(item).__name__
                    if 'Component' in item_type:
                        component_count += 1
                    elif 'Connection' in item_type:
                        connection_count += 1
                
                if hasattr(self.canvas, 'selected_components'):
                    selected_count = len(self.canvas.selected_components)
            
            # Update status if methods exist
            if hasattr(self.status_manager, 'update_counts'):
                self.status_manager.update_counts(component_count, connection_count, selected_count)
            elif hasattr(self.status_manager, 'showMessage'):
                self.status_manager.showMessage(
                    f"Components: {component_count} | Connections: {connection_count} | Selected: {selected_count}")
        
        except Exception as e:
            print(f"⚠️ Status update failed: {e}")
    
    def _update_window_title(self):
        """Update window title"""
        title = "Visual Retro System Emulator Builder"
        
        if self.project_manager:
            try:
                current_file = self.project_manager.get_current_file()
                if current_file:
                    filename = os.path.basename(current_file)
                    title += f" - {filename}"
                else:
                    title += " - Untitled"
                
                if self.project_manager.is_modified():
                    title += " *"
            except:
                pass
        
        self.setWindowTitle(title)
    
    # ========== PUBLIC INTERFACE ==========
    
    def set_component_manager(self, manager):
        """Set component manager"""
        self.component_manager = manager
        print("✓ Component manager set")
    
    def set_project_manager(self, manager):
        """Set project manager"""
        self.project_manager = manager
        print("✓ Project manager set")
    
    def set_simulation_engine(self, engine):
        """Set simulation engine"""
        self.simulation_engine = engine
        print("✓ Simulation engine set")
    
    def refresh_component_palette(self):
        """Refresh component palette"""
        if self.component_palette and hasattr(self.component_palette, '_populate_tree'):
            try:
                self.component_palette._populate_tree()
                print("✓ Component palette refreshed")
            except Exception as e:
                print(f"⚠️ Component palette refresh failed: {e}")
    
    def get_canvas(self):
        """Get canvas widget"""
        return self.canvas
    
    def get_selected_components(self):
        """Get selected components"""
        if self.canvas and hasattr(self.canvas, 'selected_components'):
            return self.canvas.selected_components
        return []
    
    # ========== EVENT HANDLERS ==========
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Check if project needs saving
        if self.project_manager and hasattr(self.project_manager, 'is_modified'):
            try:
                # Handle both callable and property forms
                if callable(self.project_manager.is_modified):
                    is_modified = self.project_manager.is_modified()
                else:
                    is_modified = self.project_manager.is_modified
                    
                if is_modified:
                    reply = QMessageBox.question(
                        self, 'Save Project?',
                        'The project has unsaved changes. Do you want to save before closing?',
                        QMessageBox.StandardButton.Save | 
                        QMessageBox.StandardButton.Discard | 
                        QMessageBox.StandardButton.Cancel,
                        QMessageBox.StandardButton.Save
                    )
                    
                    if reply == QMessageBox.StandardButton.Save:
                        self._save_project()
                    elif reply == QMessageBox.StandardButton.Cancel:
                        event.ignore()
                        return
            except Exception as e:
                print(f"⚠️ Error checking project modification status: {e}")
        
        # Clean up resources
        try:
            if self.simulation_engine and hasattr(self.simulation_engine, 'stop_simulation'):
                self.simulation_engine.stop_simulation()
        except:
            pass
        
        event.accept()
        print("✓ Main window closed")
    
    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        # Update status counts when window resizes
        QTimer.singleShot(100, self._update_status_counts)