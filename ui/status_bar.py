#!/usr/bin/env python3
"""
X-Seti - June23 2025 - Application Status Bar - Single Implementation
Visual Retro System Emulator Builder - Complete status bar system
"""
#this belongs in ui/status_bar.py

from PyQt6.QtWidgets import (
    QStatusBar, QLabel, QProgressBar, QPushButton, QFrame,
    QHBoxLayout, QWidget, QSizePolicy, QToolButton, QMenu, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QFont
from typing import Optional, Dict, Any
import time

class StatusBarSection(QWidget):
    """Custom widget for status bar sections"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(4, 2, 4, 2)
        self.layout.setSpacing(6)
        
        # Add separator frame on left
        separator = QFrame()
        separator.setFrameStyle(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)
        
    def addWidget(self, widget):
        """Add widget to the status section"""
        self.layout.addWidget(widget)
        
    def addStretch(self):
        """Add stretch to the status section"""
        self.layout.addStretch()


class RetroEmulatorStatusBar(QStatusBar):
    """Professional status bar for Visual Retro System Emulator Builder"""
    
    # Signals
    zoomChanged = pyqtSignal(float)      # zoom_level
    gridToggled = pyqtSignal(bool)       # grid_visible
    snapToggled = pyqtSignal(bool)       # snap_enabled
    unitsChanged = pyqtSignal(str)       # units (mm/inch)
    coordinatesClicked = pyqtSignal()    # coordinates clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Status tracking
        self.current_zoom = 100.0
        self.grid_visible = True
        self.snap_enabled = True
        self.current_units = "mm"
        self.component_count = 0
        self.connection_count = 0
        self.simulation_running = False
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Progress tracking
        self.current_operation = ""
        self.progress_value = 0
        
        # Create status bar sections
        self._create_status_sections()
        
        # Timer for updating dynamic info
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_dynamic_info)
        self.update_timer.start(1000)  # Update every second
        
        print("✓ Professional status bar created")
        
    def _create_status_sections(self):
        """Create all status bar sections"""
        # Main status message (uses Qt's built-in status area)
        self.showMessage("Ready")
        
        # Project section
        self._create_project_section()
        
        # Coordinates section
        self._create_coordinates_section()
        
        # View controls section
        self._create_view_section()
        
        # Component info section
        self._create_component_section()
        
        # Simulation section
        self._create_simulation_section()
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setMinimumWidth(150)
        self.addPermanentWidget(self.progress_bar)
        
        # System info section (permanent, rightmost)
        self._create_system_section()
        
    def _create_project_section(self):
        """Create project information section"""
        section = StatusBarSection()
        
        # Project name
        self.project_label = QLabel("No Project")
        self.project_label.setStyleSheet("font-weight: bold; color: #333;")
        section.addWidget(self.project_label)
        
        # Modified indicator
        self.modified_label = QLabel("")
        self.modified_label.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")
        self.modified_label.setToolTip("Project has unsaved changes")
        section.addWidget(self.modified_label)
        
        self.addWidget(section)
        
    def _create_coordinates_section(self):
        """Create coordinates section"""
        section = StatusBarSection()
        
        # Mouse coordinates (clickable)
        self.coordinates_label = QLabel("X: 0, Y: 0")
        self.coordinates_label.setMinimumWidth(80)
        self.coordinates_label.setStyleSheet("color: #666; font-family: monospace;")
        self.coordinates_label.setToolTip("Click to toggle coordinate system")
        self.coordinates_label.mousePressEvent = lambda e: self.coordinatesClicked.emit()
        section.addWidget(self.coordinates_label)
        
        self.addWidget(section)
        
    def _create_view_section(self):
        """Create view controls section"""
        section = StatusBarSection()
        
        # Zoom controls
        zoom_label = QLabel("Zoom:")
        section.addWidget(zoom_label)
        
        self.zoom_button = QToolButton()
        self.zoom_button.setText(f"{self.current_zoom:.0f}%")
        self.zoom_button.setToolTip("Click for zoom options")
        self.zoom_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        # Zoom menu
        zoom_menu = QMenu()
        zoom_levels = [25, 50, 75, 100, 125, 150, 200, 400, 800]
        for level in zoom_levels:
            action = zoom_menu.addAction(f"{level}%")
            action.triggered.connect(lambda checked, z=level: self.zoomChanged.emit(z))
        
        zoom_menu.addSeparator()
        fit_action = zoom_menu.addAction("Fit to Window")
        fit_action.triggered.connect(lambda: self.zoomChanged.emit(-1))
        
        self.zoom_button.setMenu(zoom_menu)
        section.addWidget(self.zoom_button)
        
        # Grid toggle
        self.grid_checkbox = QCheckBox("Grid")
        self.grid_checkbox.setChecked(self.grid_visible)
        self.grid_checkbox.toggled.connect(self.gridToggled.emit)
        section.addWidget(self.grid_checkbox)
        
        # Snap toggle
        self.snap_checkbox = QCheckBox("Snap")
        self.snap_checkbox.setChecked(self.snap_enabled)
        self.snap_checkbox.toggled.connect(self.snapToggled.emit)
        section.addWidget(self.snap_checkbox)
        
        # Units toggle
        self.units_button = QPushButton(self.current_units)
        self.units_button.setMaximumWidth(40)
        self.units_button.setToolTip("Toggle measurement units")
        self.units_button.clicked.connect(self._toggle_units)
        section.addWidget(self.units_button)
        
        self.addWidget(section)
        
    def _create_component_section(self):
        """Create component information section"""
        section = StatusBarSection()
        
        # Component count
        self.component_count_label = QLabel("Components: 0")
        self.component_count_label.setMinimumWidth(90)
        section.addWidget(self.component_count_label)
        
        # Connection count
        self.connection_count_label = QLabel("Connections: 0")
        self.connection_count_label.setMinimumWidth(90)
        section.addWidget(self.connection_count_label)
        
        # Selection info
        self.selection_label = QLabel("")
        section.addWidget(self.selection_label)
        
        self.addWidget(section)
        
    def _create_simulation_section(self):
        """Create simulation status section"""
        section = StatusBarSection()
        
        # Simulation status indicator
        self.sim_status_label = QLabel("●")
        self.sim_status_label.setStyleSheet("color: gray; font-size: 14px;")
        self.sim_status_label.setToolTip("Simulation Status: Stopped")
        section.addWidget(self.sim_status_label)
        
        # Simulation info
        self.sim_info_label = QLabel("Stopped")
        self.sim_info_label.setMinimumWidth(60)
        section.addWidget(self.sim_info_label)
        
        # Clock speed (when running)
        self.clock_speed_label = QLabel("")
        section.addWidget(self.clock_speed_label)
        
        self.addWidget(section)
        
    def _create_system_section(self):
        """Create system information section (permanent)"""
        section = StatusBarSection()
        
        # Memory usage
        self.memory_label = QLabel("Memory: 0 MB")
        self.memory_label.setMinimumWidth(90)
        self.memory_label.setStyleSheet("color: #666; font-size: 11px;")
        section.addWidget(self.memory_label)
        
        # Current time
        self.time_label = QLabel("")
        self.time_label.setMinimumWidth(70)
        self.time_label.setStyleSheet("color: #666; font-size: 11px;")
        section.addWidget(self.time_label)
        
        self.addPermanentWidget(section)
        
    def _toggle_units(self):
        """Toggle measurement units"""
        if self.current_units == "mm":
            self.current_units = "inch"
        else:
            self.current_units = "mm"
        
        self.units_button.setText(self.current_units)
        self.unitsChanged.emit(self.current_units)
        
    def _update_dynamic_info(self):
        """Update time and memory usage"""
        # Update time
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(current_time)
        
        # Update memory usage
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.memory_label.setText(f"Memory: {memory_mb:.0f} MB")
        except ImportError:
            # Fallback if psutil not available
            import gc
            gc.collect()
            objects = len(gc.get_objects())
            self.memory_label.setText(f"Objects: {objects}")
    
    # PUBLIC API METHODS
    def set_project_name(self, name: str):
        """Set current project name"""
        if name:
            self.project_label.setText(f"Project: {name}")
        else:
            self.project_label.setText("No Project")
            
    def set_project_modified(self, modified: bool):
        """Set project modified status"""
        if modified:
            self.modified_label.setText("●")
        else:
            self.modified_label.setText("")
            
    def set_zoom(self, zoom_level: float):
        """Set zoom level display"""
        if zoom_level == -1:  # Fit to window
            self.zoom_button.setText("Fit")
            self.current_zoom = 100.0
        else:
            self.current_zoom = zoom_level
            self.zoom_button.setText(f"{zoom_level:.0f}%")
            
    def set_coordinates(self, x: float, y: float):
        """Set mouse coordinates"""
        self.mouse_x = x
        self.mouse_y = y
        if self.current_units == "mm":
            self.coordinates_label.setText(f"X: {x:.1f}, Y: {y:.1f}")
        else:
            # Convert to inches
            x_inch = x / 25.4
            y_inch = y / 25.4
            self.coordinates_label.setText(f"X: {x_inch:.3f}\", Y: {y_inch:.3f}\"")
            
    def set_grid_visible(self, visible: bool):
        """Set grid visibility"""
        self.grid_visible = visible
        self.grid_checkbox.setChecked(visible)
        
    def set_snap_enabled(self, enabled: bool):
        """Set snap to grid enabled"""
        self.snap_enabled = enabled
        self.snap_checkbox.setChecked(enabled)
        
    def set_component_count(self, count: int):
        """Set component count"""
        self.component_count = count
        self.component_count_label.setText(f"Components: {count}")
        
    def set_connection_count(self, count: int):
        """Set connection count"""
        self.connection_count = count
        self.connection_count_label.setText(f"Connections: {count}")
        
    def set_selection_info(self, info: str):
        """Set selection information"""
        self.selection_label.setText(info)
        
    def set_simulation_status(self, running: bool, info: str = ""):
        """Set simulation status"""
        self.simulation_running = running
        if running:
            self.sim_status_label.setStyleSheet("color: green; font-size: 14px;")
            self.sim_status_label.setToolTip("Simulation Status: Running")
            self.sim_info_label.setText("Running")
        else:
            self.sim_status_label.setStyleSheet("color: gray; font-size: 14px;")
            self.sim_status_label.setToolTip("Simulation Status: Stopped")
            self.sim_info_label.setText("Stopped")
            self.clock_speed_label.setText("")
            
        if info:
            self.sim_info_label.setText(info)
            
    def set_clock_speed(self, speed: str):
        """Set simulation clock speed"""
        self.clock_speed_label.setText(speed)
        
    def show_progress(self, operation: str, maximum: int = 100):
        """Show progress bar for operation"""
        self.current_operation = operation
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.showMessage(f"{operation}...")
        
    def update_progress(self, value: int, message: str = ""):
        """Update progress bar value"""
        self.progress_value = value
        self.progress_bar.setValue(value)
        
        if message:
            self.showMessage(f"{self.current_operation}: {message}")
        else:
            percentage = int((value / self.progress_bar.maximum()) * 100) if self.progress_bar.maximum() > 0 else 0
            self.showMessage(f"{self.current_operation}: {percentage}%")
            
    def hide_progress(self):
        """Hide progress bar"""
        self.progress_bar.setVisible(False)
        self.current_operation = ""
        self.showMessage("Ready")
        
    def show_temporary_message(self, message: str, timeout: int = 3000):
        """Show temporary message"""
        self.showMessage(message, timeout)


# Convenience function for main window integration
def create_status_bar(main_window):
    """Create and setup status bar for main window"""
    status_bar = RetroEmulatorStatusBar(main_window)
    main_window.setStatusBar(status_bar)
    return status_bar


# Backward compatibility aliases
StatusBarManager = RetroEmulatorStatusBar
StatusBar = RetroEmulatorStatusBar
EnhancedStatusBar = RetroEmulatorStatusBar

# Export
__all__ = [
    'RetroEmulatorStatusBar', 
    'StatusBarManager', 
    'StatusBar', 
    'EnhancedStatusBar',
    'create_status_bar'
]


# Test function
def test_status_bar():
    """Test the status bar system"""
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
    import sys
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Status Bar Test")
    window.resize(800, 600)
    
    # Create status bar
    status_bar = create_status_bar(window)
    
    # Create test widget
    central = QWidget()
    layout = QVBoxLayout(central)
    
    # Test buttons
    project_btn = QPushButton("Set Project: Test Project")
    project_btn.clicked.connect(lambda: status_bar.set_project_name("Test Project"))
    layout.addWidget(project_btn)
    
    modified_btn = QPushButton("Toggle Modified")
    modified_btn.clicked.connect(lambda: status_bar.set_project_modified(True))
    layout.addWidget(modified_btn)
    
    zoom_btn = QPushButton("Set Zoom 150%")
    zoom_btn.clicked.connect(lambda: status_bar.set_zoom(150))
    layout.addWidget(zoom_btn)
    
    components_btn = QPushButton("Set 5 Components")
    components_btn.clicked.connect(lambda: status_bar.set_component_count(5))
    layout.addWidget(components_btn)
    
    sim_btn = QPushButton("Start Simulation")
    sim_btn.clicked.connect(lambda: status_bar.set_simulation_status(True, "Running at 1MHz"))
    layout.addWidget(sim_btn)
    
    progress_btn = QPushButton("Show Progress")
    def show_progress():
        status_bar.show_progress("Testing", 10)
        import threading
        def update():
            for i in range(11):
                status_bar.update_progress(i)
                time.sleep(0.2)
            status_bar.hide_progress()
        threading.Thread(target=update).start()
    
    progress_btn.clicked.connect(show_progress)
    layout.addWidget(progress_btn)
    
    window.setCentralWidget(central)
    window.show()
    
    print("Status bar test window - close to continue")
    print("Try the test buttons to see status bar features")
    sys.exit(app.exec())


if __name__ == "__main__":
    test_status_bar()