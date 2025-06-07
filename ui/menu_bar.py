"""
Application Menu Bar
Provides the main menu system for the retro emulator
"""

from PyQt6.QtWidgets import QMenuBar, QMenu, QMessageBox, QFileDialog, QInputDialog
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QAction, QKeySequence
import os
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
    """Main application menu bar"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = MenuBarSignals()
        self.recent_projects = []
        self.max_recent_projects = 10
        
        # Theme support - try to load your App_Settings_System
        self.app_settings = None
        self.current_theme = "default"
        self.load_app_settings()
        
        self.create_menus()
        
    def load_app_settings(self):
        """Load the App_Settings_System for theme support"""
        try:
            import sys
            import os
            # Add utils directory to path if not already there
            utils_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils')
            if utils_path not in sys.path:
                sys.path.append(utils_path)
                
            from App_settings_system import AppSettingsSystem
            self.app_settings = AppSettingsSystem()
            print("✅ App_Settings_System loaded successfully - themes will work!")
        except ImportError as e:
            print(f"⚠️  App_Settings_System not found ({e}) - using basic themes")
            self.app_settings = None
            
    def create_menus(self):
        """Create all menu items"""
        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_component_menu()
        self.create_simulation_menu()
        self.create_tools_menu()
        self.create_help_menu()
        
    def create_file_menu(self):
        """Create File menu"""
        file_menu = self.addMenu("&File")
        
        # New Project
        new_action = QAction("&New Project", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip("Create a new project")
        new_action.triggered.connect(self.signals.newProject)
        file_menu.addAction(new_action)
        
        # Open Project
        open_action = QAction("&Open Project...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Open an existing project")
        open_action.triggered.connect(self.open_project_dialog)
        file_menu.addAction(open_action)
        
        # Recent Projects submenu
        self.recent_menu = file_menu.addMenu("Recent Projects")
        self.update_recent_projects_menu()
        
        file_menu.addSeparator()
        
        # Save Project
        save_action = QAction("&Save Project", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip("Save the current project")
        save_action.triggered.connect(self.signals.saveProject)
        file_menu.addAction(save_action)
        
        # Save As
        save_as_action = QAction("Save Project &As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip("Save the project with a new name")
        save_as_action.triggered.connect(self.save_project_as_dialog)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Import/Export
        import_action = QAction("&Import Project...", self)
        import_action.setStatusTip("Import a project from archive")
        import_action.triggered.connect(self.import_project_dialog)
        file_menu.addAction(import_action)
        
        export_action = QAction("&Export Project...", self)
        export_action.setStatusTip("Export project to archive")
        export_action.triggered.connect(self.export_project_dialog)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.signals.exitApplication)
        file_menu.addAction(exit_action)
        
    def create_edit_menu(self):
        """Create Edit menu"""
        edit_menu = self.addMenu("&Edit")
        
        # Undo/Redo
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.signals.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.signals.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Cut/Copy/Paste
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.signals.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.signals.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.signals.paste)
        edit_menu.addAction(paste_action)
        
        delete_action = QAction("&Delete", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.signals.delete)
        edit_menu.addAction(delete_action)
        
        edit_menu.addSeparator()
        
        # Select All
        select_all_action = QAction("Select &All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.signals.selectAll)
        edit_menu.addAction(select_all_action)
        
        edit_menu.addSeparator()
        
        # Preferences
        prefs_action = QAction("&Preferences...", self)
        prefs_action.setShortcut(QKeySequence.StandardKey.Preferences)
        prefs_action.triggered.connect(self.signals.preferences)
        edit_menu.addAction(prefs_action)
        
    def create_view_menu(self):
        """Create View menu"""
        view_menu = self.addMenu("&View")
        
        # Zoom
        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.signals.zoomIn)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.signals.zoomOut)
        view_menu.addAction(zoom_out_action)
        
        zoom_fit_action = QAction("Zoom to &Fit", self)
        zoom_fit_action.setShortcut("Ctrl+0")
        zoom_fit_action.triggered.connect(self.signals.zoomFit)
        view_menu.addAction(zoom_fit_action)
        
        zoom_actual_action = QAction("&Actual Size", self)
        zoom_actual_action.setShortcut("Ctrl+1")
        zoom_actual_action.triggered.connect(self.signals.zoomActual)
        view_menu.addAction(zoom_actual_action)
        
        view_menu.addSeparator()
        
        # Toggle panels
        self.grid_action = QAction("Show &Grid", self)
        self.grid_action.setCheckable(True)
        self.grid_action.setChecked(True)
        self.grid_action.triggered.connect(self.signals.toggleGrid)
        view_menu.addAction(self.grid_action)
        
        self.rulers_action = QAction("Show &Rulers", self)
        self.rulers_action.setCheckable(True)
        self.rulers_action.setChecked(True)
        self.rulers_action.triggered.connect(self.signals.toggleRulers)
        view_menu.addAction(self.rulers_action)
        
        view_menu.addSeparator()
        
        # Dock panels
        self.palette_action = QAction("Component &Palette", self)
        self.palette_action.setCheckable(True)
        self.palette_action.setChecked(True)
        self.palette_action.triggered.connect(self.signals.togglePalette)
        view_menu.addAction(self.palette_action)
        
        self.properties_action = QAction("&Properties Panel", self)
        self.properties_action.setCheckable(True)
        self.properties_action.setChecked(True)
        self.properties_action.triggered.connect(self.signals.toggleProperties)
        view_menu.addAction(self.properties_action)
        
        self.layers_action = QAction("&Layers Panel", self)
        self.layers_action.setCheckable(True)
        self.layers_action.setChecked(True)
        self.layers_action.triggered.connect(self.signals.toggleLayers)
        view_menu.addAction(self.layers_action)
        
        view_menu.addSeparator()
        
        # Themes submenu
        self.create_themes_submenu(view_menu)
        
    def create_themes_submenu(self, parent_menu):
        """Create themes submenu with App_Settings_System integration"""
        themes_menu = parent_menu.addMenu("&Themes")
        
        if self.app_settings:
            # Use your App_Settings_System themes
            try:
                available_themes = self.app_settings.get_available_themes()
                current_theme = self.app_settings.get_current_theme()
                
                for theme_name in available_themes:
                    theme_action = QAction(theme_name.title(), self)
                    theme_action.setCheckable(True)
                    theme_action.setChecked(theme_name == current_theme)
                    theme_action.triggered.connect(lambda checked, name=theme_name: self.change_theme(name))
                    themes_menu.addAction(theme_action)
                    
                print(f"✅ Loaded {len(available_themes)} themes from App_Settings_System")
                
            except Exception as e:
                print(f"⚠️  Error loading themes from App_Settings_System: {e}")
                self.create_basic_themes(themes_menu)
        else:
            # Fallback basic themes
            self.create_basic_themes(themes_menu)
            
    def create_basic_themes(self, themes_menu):
        """Create basic theme options as fallback"""
        basic_themes = ["Default", "Dark", "Light", "Retro", "High Contrast"]
        
        for theme_name in basic_themes:
            theme_action = QAction(theme_name, self)
            theme_action.setCheckable(True)
            theme_action.setChecked(theme_name.lower() == self.current_theme)
            theme_action.triggered.connect(lambda checked, name=theme_name.lower(): self.change_theme(name))
            themes_menu.addAction(theme_action)
            
    def change_theme(self, theme_name: str):
        """Change application theme"""
        if self.app_settings:
            try:
                # Use your App_Settings_System to change theme
                self.app_settings.set_theme(theme_name)
                self.current_theme = theme_name
                self.signals.themeChanged.emit(theme_name)
                print(f"✅ Theme changed to: {theme_name}")
            except Exception as e:
                print(f"⚠️  Error changing theme: {e}")
        else:
            # Basic theme change
            self.current_theme = theme_name
            self.signals.themeChanged.emit(theme_name)
            print(f"📝 Basic theme change to: {theme_name}")
            
    def create_component_menu(self):
        """Create Component menu"""
        component_menu = self.addMenu("&Component")
        
        # Add components submenu
        add_menu = component_menu.addMenu("&Add Component")
        component_types = ["Processor", "Memory", "Graphics", "Audio", "I/O", "Custom"]
        
        for comp_type in component_types:
            action = QAction(comp_type, self)
            action.triggered.connect(lambda checked, ct=comp_type: self.signals.addComponent.emit(ct))
            add_menu.addAction(action)
            
        component_menu.addSeparator()
        
        # Component operations
        edit_action = QAction("&Edit Component", self)
        edit_action.triggered.connect(self.signals.editComponent)
        component_menu.addAction(edit_action)
        
        delete_action = QAction("&Delete Component", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.signals.deleteComponent)
        component_menu.addAction(delete_action)
        
        duplicate_action = QAction("D&uplicate Component", self)
        duplicate_action.setShortcut("Ctrl+D")
        duplicate_action.triggered.connect(self.signals.duplicateComponent)
        component_menu.addAction(duplicate_action)
        
        component_menu.addSeparator()
        
        # Transform
        rotate_menu = component_menu.addMenu("&Rotate")
        rotations = [("90° CW", 90), ("90° CCW", -90), ("180°", 180)]
        for label, angle in rotations:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, a=angle: self.signals.rotateComponent.emit(a))
            rotate_menu.addAction(action)
            
        flip_h_action = QAction("Flip &Horizontal", self)
        flip_h_action.triggered.connect(self.signals.flipHorizontal)
        component_menu.addAction(flip_h_action)
        
        flip_v_action = QAction("Flip &Vertical", self)
        flip_v_action.triggered.connect(self.signals.flipVertical)
        component_menu.addAction(flip_v_action)
        
    def create_simulation_menu(self):
        """Create Simulation menu"""
        sim_menu = self.addMenu("&Simulation")
        
        start_action = QAction("&Start Simulation", self)
        start_action.setShortcut("F5")
        start_action.triggered.connect(self.signals.startSimulation)
        sim_menu.addAction(start_action)
        
        stop_action = QAction("S&top Simulation", self)
        stop_action.setShortcut("Shift+F5")
        stop_action.triggered.connect(self.signals.stopSimulation)
        sim_menu.addAction(stop_action)
        
        pause_action = QAction("&Pause Simulation", self)
        pause_action.setShortcut("F6")
        pause_action.triggered.connect(self.signals.pauseSimulation)
        sim_menu.addAction(pause_action)
        
        step_action = QAction("Step &Forward", self)
        step_action.setShortcut("F10")
        step_action.triggered.connect(self.signals.stepSimulation)
        sim_menu.addAction(step_action)
        
        reset_action = QAction("&Reset Simulation", self)
        reset_action.setShortcut("Ctrl+F5")
        reset_action.triggered.connect(self.signals.resetSimulation)
        sim_menu.addAction(reset_action)
        
        sim_menu.addSeparator()
        
        settings_action = QAction("Simulation &Settings...", self)
        settings_action.triggered.connect(self.signals.simulationSettings)
        sim_menu.addAction(settings_action)
        
    def create_tools_menu(self):
        """Create Tools menu"""
        tools_menu = self.addMenu("&Tools")
        
        connection_action = QAction("&Connection Tool", self)
        connection_action.setShortcut("C")
        connection_action.triggered.connect(self.signals.connectionTool)
        tools_menu.addAction(connection_action)
        
        measure_action = QAction("&Measure Tool", self)
        measure_action.setShortcut("M")
        measure_action.triggered.connect(self.signals.measureTool)
        tools_menu.addAction(measure_action)
        
        tools_menu.addSeparator()
        
        pin_align_action = QAction("&Pin Alignment Tool", self)
        pin_align_action.triggered.connect(self.signals.pinAlignment)
        tools_menu.addAction(pin_align_action)
        
        chip_gen_action = QAction("Component &Generator", self)
        chip_gen_action.triggered.connect(self.signals.componentGenerator)
        tools_menu.addAction(chip_gen_action)
        
        tools_menu.addSeparator()
        
        export_mfg_action = QAction("Export for &Manufacturing", self)
        export_mfg_action.triggered.connect(self.signals.exportManufacturing)
        tools_menu.addAction(export_mfg_action)
        
    def create_help_menu(self):
        """Create Help menu"""
        help_menu = self.addMenu("&Help")
        
        help_action = QAction("&Help Contents", self)
        help_action.setShortcut(QKeySequence.StandardKey.HelpContents)
        help_action.triggered.connect(self.signals.showHelp)
        help_menu.addAction(help_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.signals.showAbout)
        help_menu.addAction(about_action)
        
        updates_action = QAction("Check for &Updates", self)
        updates_action.triggered.connect(self.signals.checkUpdates)
        help_menu.addAction(updates_action)
        
    # Dialog methods
    def open_project_dialog(self):
        """Open project file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Retro Emulator Projects (*.vrse);;All Files (*)"
        )
        if file_path:
            self.signals.openProject.emit(file_path)
            self.add_recent_project(file_path)
            
    def save_project_as_dialog(self):
        """Save project as dialog"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project As", "", "Retro Emulator Projects (*.vrse);;All Files (*)"
        )
        if file_path:
            if not file_path.endswith('.vrse'):
                file_path += '.vrse'
            self.signals.saveProjectAs.emit(file_path)
            self.add_recent_project(file_path)
            
    def import_project_dialog(self):
        """Import project dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Project", "", "Archive Files (*.zip *.tar.gz);;All Files (*)"
        )
        if file_path:
            self.signals.importProject.emit(file_path)
            
    def export_project_dialog(self):
        """Export project dialog"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Project", "", "Archive Files (*.zip);;All Files (*)"
        )
        if file_path:
            if not file_path.endswith('.zip'):
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

# Aliases for backward compatibility
EnhancedMenuBar = RetroEmulatorMenuBar
MenuBar = RetroEmulatorMenuBar
MenuBarManager = RetroEmulatorMenuBar  # Manager alias