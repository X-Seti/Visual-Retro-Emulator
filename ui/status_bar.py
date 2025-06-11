"""
X-Seti - June11 2025 - Application Status Bar
Provides status information and quick controls for the retro emulator
"""

from PyQt6.QtWidgets import (
    QStatusBar, QLabel, QProgressBar, QPushButton, QFrame,
    QHBoxLayout, QWidget, QSizePolicy, QToolButton, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QFont
from typing import Optional, Dict, Any
import time

class StatusBarWidget(QWidget):
    """Custom widget for status bar sections"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(4)
        
    def addWidget(self, widget):
        """Add widget to the status section"""
        self.layout.addWidget(widget)
        
    def addStretch(self):
        """Add stretch to the status section"""
        self.layout.addStretch()

class RetroEmulatorStatusBar(QStatusBar):
    """Main application status bar"""
    
    # Signals
    zoomChanged = pyqtSignal(float)  # zoom_level
    gridToggled = pyqtSignal(bool)   # grid_visible
    snapToggled = pyqtSignal(bool)   # snap_enabled
    unitsChanged = pyqtSignal(str)   # units (mm/inch)
    
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
        
        # Progress tracking
        self.current_operation = ""
        self.progress_value = 0
        
        # Setup UI elements
        self.setup_status_bar()
        
        # Timer for updating dynamic info
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dynamic_info)
        self.update_timer.start(1000)  # Update every second
        
    def setup_status_bar(self):
        """Setup status bar widgets"""
        
        # Main status message (default Qt status)
        self.status_label = QLabel("Ready")
        self.addWidget(self.status_label)
        
        # Project info section
        self.project_section = self.create_project_section()
        self.addWidget(self.project_section)
        
        # View controls section
        self.view_section = self.create_view_section()
        self.addWidget(self.view_section)
        
        # Component info section
        self.component_section = self.create_component_section()
        self.addWidget(self.component_section)
        
        # Simulation status section
        self.simulation_section = self.create_simulation_section()
        self.addWidget(self.simulation_section)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.addPermanentWidget(self.progress_bar)
        
        # System info section (permanent)
        self.system_section = self.create_system_section()
        self.addPermanentWidget(self.system_section)
        
    def create_project_section(self) -> QWidget:
        """Create project information section"""
        section = StatusBarWidget()
        
        # Project status
        self.project_label = QLabel("No Project")
        self.project_label.setStyleSheet("font-weight: bold;")
        section.addWidget(self.project_label)
        
        # Modified indicator
        self.modified_label = QLabel("")
        self.modified_label.setStyleSheet("color: red; font-weight: bold;")
        section.addWidget(self.modified_label)
        
        return section
        
    def create_view_section(self) -> QWidget:
        """Create view controls section"""
        section = StatusBarWidget()
        
        # Zoom controls
        zoom_label = QLabel("Zoom:")
        section.addWidget(zoom_label)
        
        self.zoom_button = QToolButton()
        self.zoom_button.setText(f"{self.current_zoom:.0f}%")
        self.zoom_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        # Zoom menu
        zoom_menu = QMenu()
        zoom_levels = [25, 50, 75, 100, 125, 150, 200, 400, 800]
        for level in zoom_levels:
            action = zoom_menu.addAction(f"{level}%")
            action.triggered.connect(lambda checked, z=level: self.set_zoom(z))
        zoom_menu.addAction("Fit to Window").triggered.connect(lambda: self.set_zoom(-1))
        zoom_menu.addAction("Actual Size").triggered.connect(lambda: self.set_zoom(100))
        
        self.zoom_button.setMenu(zoom_menu)
        section.addWidget(self.zoom_button)
        
        # Grid toggle
        self.grid_button = QPushButton("Grid")
        self.grid_button.setCheckable(True)
        self.grid_button.setChecked(self.grid_visible)
        self.grid_button.clicked.connect(self.toggle_grid)
        self.grid_button.setMaximumWidth(50)
        section.addWidget(self.grid_button)
        
        # Snap toggle
        self.snap_button = QPushButton("Snap")
        self.snap_button.setCheckable(True)
        self.snap_button.setChecked(self.snap_enabled)
        self.snap_button.clicked.connect(self.toggle_snap)
        self.snap_button.setMaximumWidth(50)
        section.addWidget(self.snap_button)
        
        # Units selector
        self.units_button = QToolButton()
        self.units_button.setText(self.current_units)
        self.units_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        units_menu = QMenu()
        for unit in ["mm", "inch", "mil", "pixel"]:
            action = units_menu.addAction(unit)
            action.triggered.connect(lambda checked, u=unit: self.set_units(u))
        self.units_button.setMenu(units_menu)
        section.addWidget(self.units_button)
        
        return section
        
    def create_component_section(self) -> QWidget:
        """Create component information section"""
        section = StatusBarWidget()
        
        # Component count
        self.component_count_label = QLabel("Components: 0")
        section.addWidget(self.component_count_label)
        
        # Connection count
        self.connection_count_label = QLabel("Connections: 0")
        section.addWidget(self.connection_count_label)
        
        # Selection info
        self.selection_label = QLabel("")
        section.addWidget(self.selection_label)
        
        return section
        
    def create_simulation_section(self) -> QWidget:
        """Create simulation status section"""
        section = StatusBarWidget()
        
        # Simulation status indicator
        self.sim_status_label = QLabel("●")
        self.sim_status_label.setStyleSheet("color: gray; font-size: 14px;")
        self.sim_status_label.setToolTip("Simulation Status")
        section.addWidget(self.sim_status_label)
        
        # Simulation info
        self.sim_info_label = QLabel("Stopped")
        section.addWidget(self.sim_info_label)
        
        # Clock speed (when running)
        self.clock_speed_label = QLabel("")
        section.addWidget(self.clock_speed_label)
        
        return section
        
    def create_system_section(self) -> QWidget:
        """Create system information section"""
        section = StatusBarWidget()
        
        # Memory usage
        self.memory_label = QLabel("Memory: 0 MB")
        self.memory_label.setMinimumWidth(80)
        section.addWidget(self.memory_label)
        
        # Current time
        self.time_label = QLabel("")
        self.time_label.setMinimumWidth(60)
        section.addWidget(self.time_label)
        
        return section
        
    def create_status_bar(self):
        """Compatibility method for main window"""
        return self
        
    # Public methods for updating status
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
            self.modified_label.setToolTip("Project has unsaved changes")
        else:
            self.modified_label.setText("")
            self.modified_label.setToolTip("")
            
    def set_zoom(self, zoom_level: float):
        """Set zoom level"""
        if zoom_level == -1:  # Fit to window
            self.zoom_button.setText("Fit")
            self.current_zoom = -1
        else:
            self.current_zoom = zoom_level
            self.zoom_button.setText(f"{zoom_level:.0f}%")
        self.zoomChanged.emit(zoom_level)
        
    def toggle_grid(self, checked: bool = None):
        """Toggle grid visibility"""
        if checked is None:
            self.grid_visible = not self.grid_visible
        else:
            self.grid_visible = checked
        self.grid_button.setChecked(self.grid_visible)
        self.gridToggled.emit(self.grid_visible)
        
    def toggle_snap(self, checked: bool = None):
        """Toggle snap to grid"""
        if checked is None:
            self.snap_enabled = not self.snap_enabled
        else:
            self.snap_enabled = checked
        self.snap_button.setChecked(self.snap_enabled)
        self.snapToggled.emit(self.snap_enabled)
        
    def set_units(self, units: str):
        """Set measurement units"""
        self.current_units = units
        self.units_button.setText(units)
        self.unitsChanged.emit(units)
        
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
            self.sim_info_label.setText("Running")
        else:
            self.sim_status_label.setStyleSheet("color: gray; font-size: 14px;")
            self.sim_info_label.setText("Stopped")
            
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
        
    def update_dynamic_info(self):
        """Update dynamic information"""
        # Update time
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(current_time)
        
        # Update memory usage (basic implementation)
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.memory_label.setText(f"Memory: {memory_mb:.0f} MB")
        except ImportError:
            # Fallback if psutil not available
            import sys
            import gc
            gc.collect()
            # Very rough estimate
            objects = len(gc.get_objects())
            self.memory_label.setText(f"Objects: {objects}")

# Aliases for backward compatibility
EnhancedStatusBar = RetroEmulatorStatusBar
StatusBar = RetroEmulatorStatusBar
StatusBarManager = RetroEmulatorStatusBar
