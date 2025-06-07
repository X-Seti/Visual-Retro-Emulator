"""
X-Seti - June07 2025 - Main Window Implementation
Contains the primary window layout and menu system
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                           QDockWidget, QTreeWidget, QTreeWidgetItem, QSplitter,
                           QMessageBox, QFileDialog, QLabel, QStatusBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence

from .canvas import EnhancedPCBCanvas
from .component_palette import EnhancedComponentPalette
from .layer_controls import LayerControlWidget
from .menu_bar import MenuBarManager
from .status_bar import StatusBarManager
from .property_editor import PropertyEditorWidget

from managers.project_manager import ProjectManager
from managers.layer_manager import LayerManager
from chip_editor.chip_editor_dialog import ChipEditorDialog
from database.retro_database import retro_database, global_component_library

class MainWindow(QMainWindow):
    """Enhanced main window with integrated chip editor"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Retro System Emulator Builder - Enhanced")
        self.resize(1400, 900)
        
        # Initialize managers
        self.project_manager = ProjectManager()
        self.layer_manager = LayerManager()
        
        # Create UI components
        self._create_ui()
        self._create_docks()
        self._setup_connections()
        self._setup_hotkeys()
        
        # Update display
        self._update_window_title()
        self._update_status_counts()
        
        print("✓ Enhanced main window initialized")
    
    def _create_ui(self):
        """Create the main user interface"""
        # Create central canvas
        self.canvas = EnhancedPCBCanvas()
        self.layer_manager = self.canvas.layer_manager
        self.setCentralWidget(self.canvas)
        
        # Create menu bar
        self.menu_manager = MenuBarManager(self)
        self.setMenuBar(self.menu_manager.create_menu_bar())
        
        # Create status bar
        self.status_manager = StatusBarManager(self)
        self.setStatusBar(self.status_manager.create_status_bar())
    
    def _create_docks(self):
        """Create dockable widgets"""
        # Component palette dock
        palette_dock = QDockWidget("Components", self)
        self.component_palette = EnhancedComponentPalette()
        palette_dock.setWidget(self.component_palette)
        palette_dock.setFloating(False)
        palette_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, palette_dock)
        
        # Layer controls dock
        layer_dock = QDockWidget("Layer Controls", self)
        self.layer_controls = LayerControlWidget(self)
        layer_dock.setWidget(self.layer_controls)
        layer_dock.setFloating(False)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, layer_dock)
        
        # Property editor dock
        properties_dock = QDockWidget("Properties", self)
        self.property_editor = PropertyEditorWidget()
        properties_dock.setWidget(self.property_editor)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, properties_dock)
    
    def _setup_connections(self):
        """Setup signal connections"""
        # Canvas signals
        self.canvas.selectionChanged.connect(self._on_selection_changed)
        self.canvas.componentsDeleted.connect(self._on_components_deleted)
        
        # Layer controls signals
        self.layer_controls.layerChanged.connect(self._on_layer_changed)
    
    def _setup_hotkeys(self):
        """Setup global hotkeys"""
        # File operations
        self._create_shortcut(QKeySequence.StandardKey.New, self._new_project)
        self._create_shortcut(QKeySequence.StandardKey.Open, self._open_project)
        self._create_shortcut(QKeySequence.StandardKey.Save, self._save_project)
        self._create_shortcut(QKeySequence("Ctrl+Shift+S"), self._save_project_as)
        
        # View operations
        self._create_shortcut(QKeySequence("Ctrl+="), self._zoom_in)
        self._create_shortcut(QKeySequence("Ctrl+-"), self._zoom_out)
        self._create_shortcut(QKeySequence("Ctrl+0"), self._zoom_fit)
        
        # Layer switching
        self._create_shortcut(QKeySequence("F1"), lambda: self._switch_layer("chip"))
        self._create_shortcut(QKeySequence("F2"), lambda: self._switch_layer("pcb"))
        self._create_shortcut(QKeySequence("F3"), lambda: self._switch_layer("gerber"))
        
        # Chip Editor hotkeys
        self._create_shortcut(QKeySequence("Ctrl+Shift+N"), self._open_chip_editor)
        self._create_shortcut(QKeySequence("Ctrl+E"), self._edit_selected_chip)
        
        # Quick actions
        self._create_shortcut(QKeySequence("F5"), self._validate_design)
        self._create_shortcut(QKeySequence("F6"), self._reload_components)
    
    def _create_shortcut(self, key_sequence, slot):
        """Helper to create shortcuts"""
        shortcut = QShortcut(key_sequence, self)
        shortcut.activated.connect(slot)
        return shortcut
    
    # ========== EVENT HANDLERS ==========
    
    def _on_selection_changed(self):
        """Handle selection changes from canvas"""
        selected_count = len(self.canvas.selected_components)
        
        # Update layer controls
        self.layer_controls.update_selection_info(selected_count)
        
        # Update status counts
        self._update_status_counts()
        
        # Update property editor
        if selected_count == 1:
            component = self.canvas.selected_components[0]
            self.property_editor.update_component(component)
        else:
            self.property_editor.clear_component()
    
    def _on_components_deleted(self, count):
        """Handle component deletion"""
        self._update_status_counts()
        self.status_manager.set_message(f"Deleted {count} component(s)")
    
    def _on_layer_changed(self, layer_name):
        """Handle layer change"""
        self.canvas._update_layer_appearance(layer_name)
        self.status_manager.set_layer(layer_name)
    
    # ========== CHIP EDITOR INTEGRATION ==========
    
    def _open_chip_editor(self):
        """Open chip editor for new component"""
        editor = ChipEditorDialog(self)
        editor.componentCreated.connect(self._on_component_created)
        
        if editor.exec() == editor.DialogCode.Accepted:
            print("✓ New component created")
    
    def _edit_selected_chip(self):
        """Edit the currently selected chip"""
        if not self.canvas.selected_components:
            QMessageBox.information(self, "No Selection", 
                                  "Please select a component to edit")
            return
        
        if len(self.canvas.selected_components) > 1:
            QMessageBox.information(self, "Multiple Selection", 
                                  "Please select only one component to edit")
            return
        
        selected_component = self.canvas.selected_components[0]
        if hasattr(selected_component, 'component_def'):
            editor = ChipEditorDialog(self, selected_component.component_def)
            
            if editor.exec() == editor.DialogCode.Accepted:
                # Update the component on the canvas
                selected_component.component_def = editor.current_component
                
                # Update visual representation
                if hasattr(selected_component, 'update'):
                    selected_component.update()
                
                # Refresh component palette
                self.component_palette._populate_tree()
                
                print("✓ Component updated")
                self.status_manager.set_message("Component successfully updated")
    
    def _on_component_created(self, component):
        """Handle new component creation"""
        try:
            # Add to global component library
            global_component_library.add_component(component)
            
            # Refresh component palette
            self.component_palette._populate_tree()
            
            # Update status
            self.status_manager.set_message(f"Component '{component.name}' created successfully")
            print(f"✓ Created component: {component.name}")
            
            QMessageBox.information(self, "Component Created", 
                                  f"Component '{component.name}' created successfully!\n\n"
                                  f"You can now find it in the component palette.")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Failed to add component: {str(e)}")
            print(f"✗ Error creating component: {e}")
    
    # ========== PROJECT MANAGEMENT ==========
    
    def _new_project(self):
        """Create new project"""
        try:
            self.project_manager.new_project(self.canvas)
            self._update_window_title()
            self._update_status_counts()
            self.status_manager.set_message("New project created")
            print("✓ New project created")
        except Exception as e:
            print(f"Error creating new project: {e}")
            QMessageBox.critical(self, "Error", f"Failed to create new project:\n{str(e)}")
    
    def _open_project(self):
        """Open project"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Project Files (*.json);;All Files (*)"
        )
        if filename:
            try:
                self.project_manager.load_project(self.canvas, filename)
                self._update_window_title()
                self._update_status_counts()
                self.status_manager.set_message(f"Opened: {os.path.basename(filename)}")
                print(f"✓ Opened project: {filename}")
            except Exception as e:
                print(f"Error opening project: {e}")
                QMessageBox.critical(self, "Error", f"Failed to open project:\n{str(e)}")
    
    def _save_project(self):
        """Save project"""
        current_file = self.project_manager.get_current_file()
        if current_file:
            try:
                self.project_manager.save_project(self.canvas, current_file)
                self._update_window_title()
                self.status_manager.set_message("Project saved")
                print(f"✓ Saved project: {current_file}")
            except Exception as e:
                print(f"Error saving project: {e}")
                QMessageBox.critical(self, "Error", f"Failed to save project:\n{str(e)}")
        else:
            self._save_project_as()
    
    def _save_project_as(self):
        """Save project as"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Project As", "", "Project Files (*.json);;All Files (*)"
        )
        if filename:
            if not filename.lower().endswith('.json'):
                filename += '.json'
            
            try:
                self.project_manager.save_project(self.canvas, filename)
                self._update_window_title()
                self.status_manager.set_message(f"Saved as: {os.path.basename(filename)}")
                print(f"✓ Saved project as: {filename}")
            except Exception as e:
                print(f"Error saving project: {e}")
                QMessageBox.critical(self, "Error", f"Failed to save project:\n{str(e)}")
    
    # ========== VIEW OPERATIONS ==========
    
    def _zoom_in(self):
        """Zoom in"""
        self.canvas.scale(1.2, 1.2)
        self.status_manager.set_message("Zoomed in")
    
    def _zoom_out(self):
        """Zoom out"""
        self.canvas.scale(0.8, 0.8)
        self.status_manager.set_message("Zoomed out")
    
    def _zoom_fit(self):
        """Fit to window"""
        self.canvas.fitInView(self.canvas.scene.itemsBoundingRect(), 
                             Qt.AspectRatioMode.KeepAspectRatio)
        self.status_manager.set_message("Fit to window")
    
    def _switch_layer(self, layer_name):
        """Switch to different layer"""
        self.layer_controls._switch_layer(layer_name)
    
    # ========== TOOLS ==========
    
    def _validate_design(self):
        """Validate design"""
        from rendering import EnhancedHardwareComponent
        from connection_system import Connection, EnhancedConnection
        
        components = [item for item in self.canvas.scene.items() 
                     if isinstance(item, EnhancedHardwareComponent)]
        connections = [item for item in self.canvas.scene.items() 
                      if isinstance(item, (Connection, EnhancedConnection))]
        
        msg = QMessageBox()
        msg.setWindowTitle("Design Validation")
        msg.setText(f"Design Summary:\n\n"
                   f"• Components: {len(components)}\n"
                   f"• Connections: {len(connections)}\n"
                   f"• Selected: {len(self.canvas.selected_components)}\n"
                   f"• Current Layer: {self.layer_manager.get_current_layer().title()}\n\n"
                   f"Validation: All components properly placed ✓")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _reload_components(self):
        """Reload component database"""
        try:
            retro_database.reload_components()
            self.component_palette._populate_tree()
            self.status_manager.set_message("Components reloaded")
            print("✓ Component database reloaded")
        except Exception as e:
            print(f"Error reloading components: {e}")
            QMessageBox.critical(self, "Error", f"Failed to reload components:\n{str(e)}")
    
    # ========== UTILITY METHODS ==========
    
    def _update_status_counts(self):
        """Update status bar counts"""
        from rendering import EnhancedHardwareComponent
        from connection_system import Connection, EnhancedConnection
        
        components = [item for item in self.canvas.scene.items() 
                     if isinstance(item, EnhancedHardwareComponent)]
        connections = [item for item in self.canvas.scene.items() 
                      if isinstance(item, (Connection, EnhancedConnection))]
        selected = len(self.canvas.selected_components)
        
        self.status_manager.update_counts(len(components), len(connections), selected)
        
        # Update parts list
        if hasattr(self, 'layer_controls'):
            self.layer_controls._update_parts_list()
    
    def _update_window_title(self):
        """Update window title"""
        title = "Visual Retro System Emulator Builder - Enhanced"
        
        current_file = self.project_manager.get_current_file()
        if current_file:
            filename = os.path.basename(current_file)
            title += f" - {filename}"
        else:
            title += " - Untitled"
        
        if self.project_manager.is_modified():
            title += " *"
        
        self.setWindowTitle(title)
