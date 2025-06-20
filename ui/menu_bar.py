"""
X-Seti - June16 2025 - Application Menu Bar
Provides the main menu system for the retro emulator
"""

#this belongs in ui/ menu_bar.py
from PyQt6.QtWidgets import QMenuBar, QMenu, QMessageBox, QFileDialog, QInputDialog
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtGui import QAction, QKeySequence
import os
import sys
from typing import Optional

class MenuBarSignals(QObject):
    """Signals for menu actions"""
    # File menu
    newProject = pyqtSignal()
    openProject = pyqtSignal(str)  # file_path
    saveProject = pyqtSignal()
    saveProjectAs = pyqtSignal(str)  # file_path
    importProject = pyqtSignal(str)  # file_path
    exportProject = pyqtSignal(str)  # file_path
    recentProjectSelected = pyqtSignal(str)  # file_path
    exitApplication = pyqtSignal()
    
    # Edit menu
    undo = pyqtSignal()
    redo = pyqtSignal()
    cut = pyqtSignal()
    copy = pyqtSignal()
    paste = pyqtSignal()
    delete = pyqtSignal()
    selectAll = pyqtSignal()
    preferences = pyqtSignal()
    
    # View menu
    zoomIn = pyqtSignal()
    zoomOut = pyqtSignal()
    zoomFit = pyqtSignal()
    zoomActual = pyqtSignal()
    toggleGrid = pyqtSignal(bool)
    toggleRulers = pyqtSignal(bool)
    togglePalette = pyqtSignal(bool)
    toggleProperties = pyqtSignal(bool)
    toggleLayers = pyqtSignal(bool)
    themeChanged = pyqtSignal(str)  # theme_name
    
    # Component menu
    addComponent = pyqtSignal(str)  # component_type
    editComponent = pyqtSignal()
    deleteComponent = pyqtSignal()
    duplicateComponent = pyqtSignal()
    rotateComponent = pyqtSignal(float)  # degrees
    flipHorizontal = pyqtSignal()
    flipVertical = pyqtSignal()
    
    # Simulation menu
    startSimulation = pyqtSignal()
    stopSimulation = pyqtSignal()
    pauseSimulation = pyqtSignal()
    stepSimulation = pyqtSignal()
    resetSimulation = pyqtSignal()
    simulationSettings = pyqtSignal()
    
    # Tools menu
    connectionTool = pyqtSignal()
    measureTool = pyqtSignal()
    pinAlignment = pyqtSignal()
    componentGenerator = pyqtSignal()
    exportManufacturing = pyqtSignal()
    
    # Help menu
    showHelp = pyqtSignal()
    showAbout = pyqtSignal()
    checkUpdates = pyqtSignal()

class RetroEmulatorMenuBar(QMenuBar):
    """COMPLETE: Main application menu bar with all required methods"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = MenuBarSignals()
        self.recent_projects = []
        self.max_recent_projects = 10
        
        # FIXED: Initialize all required references to prevent AttributeError
        self.canvas = None
        self.project_manager = None
        self.component_manager = None
        self.simulation_engine = None
        self.app_settings = None
        
        # Try to load app settings system
        try:
            from App_settings_system import AppSettingsSystem
            self.app_settings = AppSettingsSystem()
            print("✅ App settings system loaded")
        except ImportError:
            print("⚠️ App settings system not available")
        
        # Create all menus
        self._create_menus()
        print("✅ Menu bar initialized with all required methods")
    
    # FIXED: All required setter methods
    def set_canvas(self, canvas):
        """FIXED: Set canvas reference for menu actions"""
        self.canvas = canvas
        print("✅ Canvas set in menu bar")
        
        # Connect canvas-specific menu actions if signals exist
        if hasattr(self, 'signals') and canvas:
            try:
                self.signals.zoomIn.connect(self._canvas_zoom_in)
                self.signals.zoomOut.connect(self._canvas_zoom_out)
                self.signals.zoomFit.connect(self._canvas_zoom_fit)
                self.signals.zoomActual.connect(self._canvas_zoom_actual)
                self.signals.toggleGrid.connect(self._canvas_toggle_grid)
                self.signals.toggleRulers.connect(self._canvas_toggle_rulers)
                print("✅ Canvas menu actions connected")
            except AttributeError as e:
                print(f"⚠️ Some menu signals not available: {e}")

    def set_project_manager(self, project_manager):
        """FIXED: Set project manager reference"""
        self.project_manager = project_manager
        print("✅ Project manager set in menu bar")
        
        # Connect project manager signals if available
        if hasattr(self, 'signals') and project_manager:
            try:
                self.signals.newProject.connect(project_manager.new_project)
                self.signals.saveProject.connect(project_manager.save_current_project)
                print("✅ Project manager signals connected")
            except AttributeError as e:
                print(f"⚠️ Some project manager signals not available: {e}")

    def set_component_manager(self, component_manager):
        """FIXED: Set component manager reference"""
        self.component_manager = component_manager
        print("✅ Component manager set in menu bar")

    def set_simulation_engine(self, simulation_engine):
        """FIXED: Set simulation engine reference"""
        self.simulation_engine = simulation_engine
        print("✅ Simulation engine set in menu bar")
        
        # Connect simulation signals if available
        if hasattr(self, 'signals') and simulation_engine:
            try:
                self.signals.startSimulation.connect(simulation_engine.start)
                self.signals.stopSimulation.connect(simulation_engine.stop)
                self.signals.pauseSimulation.connect(simulation_engine.pause)
                self.signals.resetSimulation.connect(simulation_engine.reset)
                print("✅ Simulation engine signals connected")
            except AttributeError as e:
                print(f"⚠️ Some simulation signals not available: {e}")

    # Canvas interaction methods for menu bar
    def _canvas_zoom_in(self):
        """Zoom in on canvas"""
        if self.canvas:
            if hasattr(self.canvas, 'zoom_in'):
                self.canvas.zoom_in()
            elif hasattr(self.canvas, 'scale'):
                self.canvas.scale(1.25, 1.25)
            print("🔍 Canvas zoom in")

    def _canvas_zoom_out(self):
        """Zoom out on canvas"""
        if self.canvas:
            if hasattr(self.canvas, 'zoom_out'):
                self.canvas.zoom_out()
            elif hasattr(self.canvas, 'scale'):
                self.canvas.scale(0.8, 0.8)
            print("🔍 Canvas zoom out")

    def _canvas_zoom_fit(self):
        """Fit canvas to window"""
        if self.canvas:
            if hasattr(self.canvas, 'fit_in_view'):
                self.canvas.fit_in_view()
            elif hasattr(self.canvas, 'fitInView') and hasattr(self.canvas, 'sceneRect'):
                self.canvas.fitInView(self.canvas.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            print("🔍 Canvas fit to window")

    def _canvas_zoom_actual(self):
        """Reset canvas zoom to 100%"""
        if self.canvas:
            if hasattr(self.canvas, 'reset_zoom'):
                self.canvas.reset_zoom()
            elif hasattr(self.canvas, 'resetTransform'):
                self.canvas.resetTransform()
            print("🔍 Canvas zoom reset")

    def _canvas_toggle_grid(self, checked):
        """Toggle grid visibility"""
        if self.canvas:
            if hasattr(self.canvas, 'set_grid_visible'):
                self.canvas.set_grid_visible(checked)
            elif hasattr(self.canvas, 'grid_visible'):
                self.canvas.grid_visible = checked
                if hasattr(self.canvas, 'viewport'):
                    self.canvas.viewport().update()
            print(f"🔧 Canvas grid: {checked}")

    def _canvas_toggle_rulers(self, checked):
        """Toggle ruler visibility"""
        if self.canvas:
            if hasattr(self.canvas, 'set_rulers_visible'):
                self.canvas.set_rulers_visible(checked)
            elif hasattr(self.canvas, 'show_ruler'):
                self.canvas.show_ruler = checked
                if hasattr(self.canvas, 'viewport'):
                    self.canvas.viewport().update()
            print(f"🔧 Canvas rulers: {checked}")

    def _create_menus(self):
        """Create all application menus"""
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_component_menu()
        self._create_simulation_menu()
        self._create_tools_menu()
        self._create_help_menu()
        
    def _create_file_menu(self):
        """Create File menu"""
        file_menu = self.addMenu('&File')
        
        # New project
        new_action = QAction('&New Project', self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip('Create a new project')
        new_action.triggered.connect(self.signals.newProject.emit)
        file_menu.addAction(new_action)
        
        # Open project
        open_action = QAction('&Open Project...', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip('Open an existing project')
        open_action.triggered.connect(self._open_project_dialog)
        file_menu.addAction(open_action)
        
        # Recent projects submenu
        self.recent_menu = file_menu.addMenu('Recent Projects')
        self.update_recent_projects_menu()
        
        file_menu.addSeparator()
        
        # Save project
        save_action = QAction('&Save Project', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip('Save the current project')
        save_action.triggered.connect(self.signals.saveProject.emit)
        file_menu.addAction(save_action)
        
        # Save project as
        save_as_action = QAction('Save Project &As...', self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip('Save the project with a new name')
        save_as_action.triggered.connect(self._save_project_as_dialog)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Import/Export
        import_action = QAction('&Import Project...', self)
        import_action.setStatusTip('Import project from file')
        import_action.triggered.connect(self._import_project_dialog)
        file_menu.addAction(import_action)
        
        export_action = QAction('&Export Project...', self)
        export_action.setStatusTip('Export project to file')
        export_action.triggered.connect(self._export_project_dialog)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence('Ctrl+Q'))
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.signals.exitApplication.emit)
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
        
        # Cut, Copy, Paste
        cut_action = QAction('Cu&t', self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.signals.cut.emit)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction('&Copy', self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.signals.copy.emit)
        edit_menu.addAction(copy_action)
        
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
        select_all_action.triggered.connect(self.signals.selectAll.emit)
        edit_menu.addAction(select_all_action)
        
        edit_menu.addSeparator()
        
        # Preferences
        prefs_action = QAction('&Preferences...', self)
        prefs_action.setShortcut(QKeySequence('Ctrl+,'))
        prefs_action.triggered.connect(self.signals.preferences.emit)
        edit_menu.addAction(prefs_action)
        
    def _create_view_menu(self):
        """Create View menu"""
        view_menu = self.addMenu('&View')
        
        # Zoom controls
        zoom_in_action = QAction('Zoom &In', self)
        zoom_in_action.setShortcut(QKeySequence('Ctrl++'))
        zoom_in_action.triggered.connect(self.signals.zoomIn.emit)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction('Zoom &Out', self)
        zoom_out_action.setShortcut(QKeySequence('Ctrl+-'))
        zoom_out_action.triggered.connect(self.signals.zoomOut.emit)
        view_menu.addAction(zoom_out_action)
        
        zoom_fit_action = QAction('&Fit to Window', self)
        zoom_fit_action.setShortcut(QKeySequence('Ctrl+0'))
        zoom_fit_action.triggered.connect(self.signals.zoomFit.emit)
        view_menu.addAction(zoom_fit_action)
        
        zoom_actual_action = QAction('&Actual Size', self)
        zoom_actual_action.setShortcut(QKeySequence('Ctrl+1'))
        zoom_actual_action.triggered.connect(self.signals.zoomActual.emit)
        view_menu.addAction(zoom_actual_action)
        
        view_menu.addSeparator()
        
        # Grid toggle
        grid_action = QAction('Show &Grid', self)
        grid_action.setCheckable(True)
        grid_action.setChecked(True)
        grid_action.setShortcut(QKeySequence('Ctrl+G'))
        grid_action.toggled.connect(self.signals.toggleGrid.emit)
        view_menu.addAction(grid_action)
        
        # Rulers toggle
        rulers_action = QAction('Show &Rulers', self)
        rulers_action.setCheckable(True)
        rulers_action.setChecked(False)
        rulers_action.setShortcut(QKeySequence('Ctrl+R'))
        rulers_action.toggled.connect(self.signals.toggleRulers.emit)
        view_menu.addAction(rulers_action)
        
        view_menu.addSeparator()
        
        # Panel toggles
        palette_action = QAction('Show Component &Palette', self)
        palette_action.setCheckable(True)
        palette_action.setChecked(True)
        palette_action.toggled.connect(self.signals.togglePalette.emit)
        view_menu.addAction(palette_action)
        
        properties_action = QAction('Show &Properties Panel', self)
        properties_action.setCheckable(True)
        properties_action.setChecked(True)
        properties_action.toggled.connect(self.signals.toggleProperties.emit)
        view_menu.addAction(properties_action)
        
        layers_action = QAction('Show &Layer Controls', self)
        layers_action.setCheckable(True)
        layers_action.setChecked(True)
        layers_action.toggled.connect(self.signals.toggleLayers.emit)
        view_menu.addAction(layers_action)
        
        # Theme submenu
        if self.app_settings:
            view_menu.addSeparator()
            theme_menu = view_menu.addMenu('&Theme')
            self._create_theme_menu(theme_menu)
        
    def _create_component_menu(self):
        """Create Component menu"""
        component_menu = self.addMenu('&Component')
        
        # Add component submenu
        add_menu = component_menu.addMenu('&Add Component')
        
        # Common components
        cpu_action = QAction('&CPU', self)
        cpu_action.triggered.connect(lambda: self.signals.addComponent.emit('cpu'))
        add_menu.addAction(cpu_action)
        
        memory_action = QAction('&Memory', self)
        memory_action.triggered.connect(lambda: self.signals.addComponent.emit('memory'))
        add_menu.addAction(memory_action)
        
        component_menu.addSeparator()
        
        # Edit operations
        edit_action = QAction('&Edit Component...', self)
        edit_action.triggered.connect(self.signals.editComponent.emit)
        component_menu.addAction(edit_action)
        
        delete_action = QAction('&Delete Component', self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.signals.deleteComponent.emit)
        component_menu.addAction(delete_action)
        
        duplicate_action = QAction('D&uplicate Component', self)
        duplicate_action.setShortcut(QKeySequence('Ctrl+D'))
        duplicate_action.triggered.connect(self.signals.duplicateComponent.emit)
        component_menu.addAction(duplicate_action)
        
        component_menu.addSeparator()
        
        # Transform operations
        rotate_menu = component_menu.addMenu('&Rotate')
        
        rotate_90_action = QAction('Rotate 90°', self)
        rotate_90_action.triggered.connect(lambda: self.signals.rotateComponent.emit(90))
        rotate_menu.addAction(rotate_90_action)
        
        rotate_180_action = QAction('Rotate 180°', self)
        rotate_180_action.triggered.connect(lambda: self.signals.rotateComponent.emit(180))
        rotate_menu.addAction(rotate_180_action)
        
        rotate_270_action = QAction('Rotate 270°', self)
        rotate_270_action.triggered.connect(lambda: self.signals.rotateComponent.emit(270))
        rotate_menu.addAction(rotate_270_action)
        
        flip_h_action = QAction('Flip &Horizontal', self)
        flip_h_action.triggered.connect(self.signals.flipHorizontal.emit)
        component_menu.addAction(flip_h_action)
        
        flip_v_action = QAction('Flip &Vertical', self)
        flip_v_action.triggered.connect(self.signals.flipVertical.emit)
        component_menu.addAction(flip_v_action)
        
    def _create_simulation_menu(self):
        """Create Simulation menu"""
        sim_menu = self.addMenu('&Simulation')
        
        # Simulation controls
        start_action = QAction('&Start Simulation', self)
        start_action.setShortcut(QKeySequence('F5'))
        start_action.triggered.connect(self.signals.startSimulation.emit)
        sim_menu.addAction(start_action)
        
        stop_action = QAction('S&top Simulation', self)
        stop_action.setShortcut(QKeySequence('Shift+F5'))
        stop_action.triggered.connect(self.signals.stopSimulation.emit)
        sim_menu.addAction(stop_action)
        
        pause_action = QAction('&Pause Simulation', self)
        pause_action.setShortcut(QKeySequence('F6'))
        pause_action.triggered.connect(self.signals.pauseSimulation.emit)
        sim_menu.addAction(pause_action)
        
        step_action = QAction('&Step Simulation', self)
        step_action.setShortcut(QKeySequence('F10'))
        step_action.triggered.connect(self.signals.stepSimulation.emit)
        sim_menu.addAction(step_action)
        
        reset_action = QAction('&Reset Simulation', self)
        reset_action.setShortcut(QKeySequence('Ctrl+F5'))
        reset_action.triggered.connect(self.signals.resetSimulation.emit)
        sim_menu.addAction(reset_action)
        
        sim_menu.addSeparator()
        
        # Simulation settings
        settings_action = QAction('Simulation &Settings...', self)
        settings_action.triggered.connect(self.signals.simulationSettings.emit)
        sim_menu.addAction(settings_action)
        
    def _create_tools_menu(self):
        """Create Tools menu"""
        tools_menu = self.addMenu('&Tools')
        
        # Connection tool
        connection_action = QAction('&Connection Tool', self)
        connection_action.setShortcut(QKeySequence('C'))
        connection_action.triggered.connect(self.signals.connectionTool.emit)
        tools_menu.addAction(connection_action)
        
        # Measure tool
        measure_action = QAction('&Measure Tool', self)
        measure_action.setShortcut(QKeySequence('M'))
        measure_action.triggered.connect(self.signals.measureTool.emit)
        tools_menu.addAction(measure_action)
        
        tools_menu.addSeparator()
        
        # Alignment tools
        align_action = QAction('Pin &Alignment Tool', self)
        align_action.triggered.connect(self.signals.pinAlignment.emit)
        tools_menu.addAction(align_action)
        
        # Component generator
        generator_action = QAction('Component &Generator', self)
        generator_action.triggered.connect(self.signals.componentGenerator.emit)
        tools_menu.addAction(generator_action)
        
        tools_menu.addSeparator()
        
        # Manufacturing export
        export_mfg_action = QAction('Export for &Manufacturing...', self)
        export_mfg_action.triggered.connect(self.signals.exportManufacturing.emit)
        tools_menu.addAction(export_mfg_action)
        
    def _create_help_menu(self):
        """Create Help menu"""
        help_menu = self.addMenu('&Help')
        
        # Help
        help_action = QAction('&Help', self)
        help_action.setShortcut(QKeySequence.StandardKey.HelpContents)
        help_action.triggered.connect(self.signals.showHelp.emit)
        help_menu.addAction(help_action)
        
        help_menu.addSeparator()
        
        # Check for updates
        updates_action = QAction('Check for &Updates...', self)
        updates_action.triggered.connect(self.signals.checkUpdates.emit)
        help_menu.addAction(updates_action)
        
        # About
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.signals.showAbout.emit)
        help_menu.addAction(about_action)
        
    def _create_theme_menu(self, theme_menu):
        """Create theme selection menu"""
        if not self.app_settings:
            return
            
        try:
            themes = self.app_settings.themes
            for theme_name, theme_data in themes.items():
                theme_action = QAction(theme_data.get('name', theme_name), self)
                theme_action.triggered.connect(lambda checked, name=theme_name: self.signals.themeChanged.emit(name))
                theme_menu.addAction(theme_action)
        except Exception as e:
            print(f"⚠️ Error creating theme menu: {e}")
    
    # Dialog methods
    def _open_project_dialog(self):
        """Show open project dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", 
            "Project Files (*.json *.xml *.proj);;All Files (*)"
        )
        if file_path:
            self.signals.openProject.emit(file_path)
            self.add_recent_project(file_path)
            
    def _save_project_as_dialog(self):
        """Show save project as dialog"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project As", "", 
            "Project Files (*.json *.xml *.proj);;All Files (*)"
        )
        if file_path:
            self.signals.saveProjectAs.emit(file_path)
            self.add_recent_project(file_path)
            
    def _import_project_dialog(self):
        """Show import project dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Project", "", 
            "All Supported (*.json *.xml *.zip *.tar.gz);;JSON Files (*.json);;XML Files (*.xml);;Archives (*.zip *.tar.gz);;All Files (*)"
        )
        if file_path:
            self.signals.importProject.emit(file_path)
            
    def _export_project_dialog(self):
        """Show export project dialog"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Project", "", 
            "ZIP Archive (*.zip);;TAR Archive (*.tar.gz);;JSON File (*.json);;All Files (*)"
        )
        if file_path:
            # Ensure proper extension
            if not any(file_path.endswith(ext) for ext in ['.zip', '.tar.gz', '.json']):
                file_path += '.zip'
            self.signals.exportProject.emit(file_path)
            
    # Recent projects management
    def add_recent_project(self, file_path: str):
        """Add project to recent projects list"""
        if file_path in self.recent_projects:
            self.recent_projects.remove(file_path)
        self.recent_projects.insert(0, file_path)
        self.recent_projects = self.recent_projects[:self.max_recent_projects]
        self.update_recent_projects_menu()
        
    def update_recent_projects_menu(self):
        """Update recent projects menu"""
        self.recent_menu.clear()
        
        if not self.recent_projects:
            no_recent_action = QAction("No recent projects", self)
            no_recent_action.setEnabled(False)
            self.recent_menu.addAction(no_recent_action)
        else:
            for i, file_path in enumerate(self.recent_projects):
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    action = QAction(f"&{i+1} {filename}", self)
                    action.setStatusTip(file_path)
                    action.triggered.connect(lambda checked, fp=file_path: self.signals.recentProjectSelected.emit(fp))
                    self.recent_menu.addAction(action)
                    
            if self.recent_projects:
                self.recent_menu.addSeparator()
                clear_action = QAction("&Clear Recent Projects", self)
                clear_action.triggered.connect(self.clear_recent_projects)
                self.recent_menu.addAction(clear_action)
                
    def clear_recent_projects(self):
        """Clear recent projects list"""
        self.recent_projects.clear()
        self.update_recent_projects_menu()
        
    def set_recent_projects(self, projects: list):
        """Set recent projects from external source"""
        self.recent_projects = projects[:self.max_recent_projects]
        self.update_recent_projects_menu()

# Backward compatibility aliases
MenuBarManager = RetroEmulatorMenuBar
MenuManager = RetroEmulatorMenuBar

# Export
__all__ = ['RetroEmulatorMenuBar', 'MenuBarManager', 'MenuManager', 'MenuBarSignals']