#!/usr/bin/env python3
"""
X-Seti - June16 2025 - Clean Main Window with Enhanced UI
Visual Retro System Emulator Builder - Streamlined interface with floating menus
"""

#this belongs in ui/main_window.py

import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                           QDockWidget, QSplitter, QMessageBox, QApplication,
                           QPushButton, QLabel, QStatusBar, QMenuBar, QMenu,
                           QToolBar, QFrame, QTabWidget)
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QShortcut, QKeySequence, QColor, QIcon, QAction

# Import our clean UI components
try:
    from .component_palette import CleanComponentPalette
    from .enhanced_canvas import EnhancedPCBCanvas
    print("✅ Imported clean UI components")
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    # Fallback to basic widgets
    CleanComponentPalette = None
    EnhancedPCBCanvas = None

class MinimalPropertiesPanel(QWidget):
    """Minimal properties panel that appears only when needed"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Title
        title = QLabel("🔧 Properties")
        title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 12px;
                color: #2c3e50;
                background-color: rgba(52, 152, 219, 0.1);
                padding: 8px;
                border-radius: 4px;
                border: 1px solid rgba(52, 152, 219, 0.3);
            }
        """)
        layout.addWidget(title)
        
        # Content placeholder
        content = QLabel("Select a component\nto view properties")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-style: italic;
                padding: 20px;
                border: 2px dashed #bdc3c7;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(content)
        
        layout.addStretch()
        
        # Initially hidden
        self.hide()

class StatusIndicator(QWidget):
    """Clean status indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Status elements
        self.tool_label = QLabel("🔍 Select")
        self.zoom_label = QLabel("🔍 100%")
        self.components_label = QLabel("📦 0 components")
        self.grid_label = QLabel("⌗ Grid: ON")
        
        # Style labels
        for label in [self.tool_label, self.zoom_label, self.components_label, self.grid_label]:
            label.setStyleSheet("""
                QLabel {
                    background-color: rgba(44, 62, 80, 0.1);
                    color: #2c3e50;
                    padding: 4px 8px;
                    border-radius: 4px;
                    margin: 2px;
                    font-size: 10px;
                }
            """)
        
        layout.addWidget(self.tool_label)
        layout.addWidget(self.zoom_label)
        layout.addWidget(self.components_label)
        layout.addWidget(self.grid_label)
        layout.addStretch()
    
    def update_tool(self, tool):
        """Update current tool display"""
        icons = {'select': '🔍', 'pan': '✋', 'zoom': '🔍'}
        icon = icons.get(tool, '🔧')
        self.tool_label.setText(f"{icon} {tool.title()}")
    
    def update_zoom(self, zoom_factor):
        """Update zoom display"""
        self.zoom_label.setText(f"🔍 {int(zoom_factor * 100)}%")
    
    def update_components(self, count):
        """Update component count"""
        self.components_label.setText(f"📦 {count} components")
    
    def update_grid(self, enabled):
        """Update grid status"""
        status = "ON" if enabled else "OFF"
        self.grid_label.setText(f"⌗ Grid: {status}")

class CleanMainWindow(QMainWindow):
    """Clean main window with minimal UI and floating menus"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("X-Seti Visual Retro System Emulator Builder - CLEAN")
        self.resize(1400, 900)
        
        print("🚀 Initializing Clean Main Window...")
        
        # Initialize state
        self.current_project = None
        self.selected_component = None
        
        # Setup UI
        self._create_clean_ui()
        self._setup_menu_bar()
        self._setup_connections()
        self._setup_shortcuts()
        
        # Apply clean styling
        self._apply_clean_theme()
        
        print("✅ Clean Main Window initialized")
    
    def _create_clean_ui(self):
        """Create clean, minimal UI"""
        # Central widget - just the canvas
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Component palette (collapsible)
        if CleanComponentPalette:
            self.component_palette = CleanComponentPalette()
            self.component_palette.setMaximumWidth(300)
            main_layout.addWidget(self.component_palette)
        else:
            print("⚠️ CleanComponentPalette not available, creating placeholder")
            self.component_palette = QLabel("Component\nPalette\nPlaceholder")
            self.component_palette.setMaximumWidth(200)
            main_layout.addWidget(self.component_palette)
        
        # Canvas area with toolbar
        canvas_widget = QWidget()
        canvas_layout = QVBoxLayout(canvas_widget)
        canvas_layout.setContentsMargins(4, 4, 4, 0)
        canvas_layout.setSpacing(4)
        
        # Top toolbar (moved from floating to fixed position)
        self.top_toolbar = self._create_top_toolbar()
        canvas_layout.addWidget(self.top_toolbar)
        
        # Canvas
        if EnhancedPCBCanvas:
            self.canvas = EnhancedPCBCanvas()
            # Disable the floating toolbar since we have a fixed one
            if hasattr(self.canvas, 'toolbar'):
                self.canvas.toolbar.hide()
                self.canvas.toolbar.setEnabled(False)
            # Disable toolbar auto-show methods
            if hasattr(self.canvas, 'show_toolbar'):
                self.canvas.show_toolbar = lambda: None
            if hasattr(self.canvas, 'show_toolbar_at_cursor'):
                self.canvas.show_toolbar_at_cursor = lambda: None
        else:
            print("⚠️ EnhancedPCBCanvas not available, creating placeholder")
            self.canvas = QLabel("Enhanced\nCanvas\nPlaceholder")
            self.canvas.setStyleSheet("background-color: #2c3e50; color: white;")
        
        canvas_layout.addWidget(self.canvas, 1)  # Canvas takes most space
        
        main_layout.addWidget(canvas_widget, 1)  # Canvas takes most space
        
        # Create proper status bar at bottom
        self._create_status_bar()
        
        # Properties panel (initially hidden)
        self.properties_panel = MinimalPropertiesPanel()
        
        # Create dock for properties (but keep it hidden initially)
        properties_dock = QDockWidget("Properties", self)
        properties_dock.setWidget(self.properties_panel)
        properties_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | 
                                  QDockWidget.DockWidgetFeature.DockWidgetMovable)
        properties_dock.hide()  # Hidden by default
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, properties_dock)
        
        self.properties_dock = properties_dock
    
    def _create_top_toolbar(self):
        """Create fixed top toolbar instead of floating"""
        toolbar = QWidget()
        toolbar.setFixedHeight(50)
        toolbar.setStyleSheet("""
            QWidget {
                background-color: rgba(44, 62, 80, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin: 2px;
            }
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        
        # Tool buttons with better styling
        self.tools = {}
        
        # Selection tool
        self.tools['select'] = self._create_toolbar_button("🔍", "Select Tool (S)", self.select_tool)
        layout.addWidget(self.tools['select'])
        
        # Pan tool
        self.tools['pan'] = self._create_toolbar_button("✋", "Pan Tool (H)", self.pan_tool)
        layout.addWidget(self.tools['pan'])
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("color: rgba(255,255,255,0.3); margin: 4px;")
        layout.addWidget(separator)
        
        # Zoom controls
        self.tools['zoom_in'] = self._create_toolbar_button("🔍+", "Zoom In (+)", self.zoom_in)
        layout.addWidget(self.tools['zoom_in'])
        
        self.tools['zoom_out'] = self._create_toolbar_button("🔍-", "Zoom Out (-)", self.zoom_out)
        layout.addWidget(self.tools['zoom_out'])
        
        self.tools['zoom_fit'] = self._create_toolbar_button("⬜", "Fit to Window (F)", self.fit_to_window)
        layout.addWidget(self.tools['zoom_fit'])
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.VLine) 
        separator2.setStyleSheet("color: rgba(255,255,255,0.3); margin: 4px;")
        layout.addWidget(separator2)
        
        # Grid and layer controls
        self.tools['grid'] = self._create_toolbar_button("⌗", "Grid Settings (G)", self.show_grid_settings)
        layout.addWidget(self.tools['grid'])
        
        self.tools['layers'] = self._create_toolbar_button("📄", "Layers", self.show_layers)
        layout.addWidget(self.tools['layers'])
        
        # Separator
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.VLine)
        separator3.setStyleSheet("color: rgba(255,255,255,0.3); margin: 4px;")
        layout.addWidget(separator3)
        
        # Quick actions
        self.tools['save'] = self._create_toolbar_button("💾", "Save Project (Ctrl+S)", self.save_project)
        layout.addWidget(self.tools['save'])
        
        self.tools['search'] = self._create_toolbar_button("🔍", "Find Components (Ctrl+F)", self.show_component_search)
        layout.addWidget(self.tools['search'])
        
        layout.addStretch()
        
        return toolbar
    
    def _create_toolbar_button(self, icon, tooltip, callback):
        """Create a toolbar button with consistent styling"""
        btn = QPushButton(icon)
        btn.setToolTip(tooltip)
        btn.setFixedSize(32, 32)
        btn.clicked.connect(callback)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(52, 152, 219, 0.7);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:pressed {
                background-color: rgba(41, 128, 185, 1.0);
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
        """)
        return btn
    
    def _create_status_bar(self):
        """Create comprehensive status bar"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Status bar styling
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #34495e;
                color: white;
                border-top: 1px solid #2c3e50;
                padding: 2px;
            }
            QStatusBar::item {
                border: none;
            }
        """)
        
        # Left side - Tool and mode info
        self.status_tool = QLabel("🔍 Select Tool")
        self.status_tool.setStyleSheet("color: #ecf0f1; padding: 2px 8px;")
        status_bar.addWidget(self.status_tool)
        
        status_bar.addWidget(self._create_status_separator())
        
        # Component count
        self.status_components = QLabel("📦 0 Components")
        self.status_components.setStyleSheet("color: #ecf0f1; padding: 2px 8px;")
        status_bar.addWidget(self.status_components)
        
        status_bar.addWidget(self._create_status_separator())
        
        # Grid status
        self.status_grid = QLabel("⌗ Grid: ON")
        self.status_grid.setStyleSheet("color: #ecf0f1; padding: 2px 8px;")
        status_bar.addWidget(self.status_grid)
        
        status_bar.addWidget(self._create_status_separator())
        
        # Zoom level
        self.status_zoom = QLabel("🔍 100%")
        self.status_zoom.setStyleSheet("color: #ecf0f1; padding: 2px 8px;")
        status_bar.addWidget(self.status_zoom)
        
        # Right side - System info
        status_bar.addPermanentWidget(self._create_status_separator())
        
        # Memory usage
        self.status_memory = QLabel("💾 Memory: -- MB")
        self.status_memory.setStyleSheet("color: #e74c3c; padding: 2px 8px;")
        status_bar.addPermanentWidget(self.status_memory)
        
        status_bar.addPermanentWidget(self._create_status_separator())
        
        # Performance indicator
        self.status_performance = QLabel("⚡ Performance: Good")
        self.status_performance.setStyleSheet("color: #27ae60; padding: 2px 8px;")
        status_bar.addPermanentWidget(self.status_performance)
        
        status_bar.addPermanentWidget(self._create_status_separator())
        
        # Project status
        self.status_project = QLabel("📋 Ready")
        self.status_project.setStyleSheet("color: #f39c12; padding: 2px 8px;")
        status_bar.addPermanentWidget(self.status_project)
        
        # Setup timer for updating memory usage
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_system_status)
        self.status_timer.start(2000)  # Update every 2 seconds
        
        return status_bar
    
    def _create_status_separator(self):
        """Create a status bar separator"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("color: rgba(255,255,255,0.3); margin: 2px 4px;")
        separator.setFixedHeight(16)
        return separator
    
    def _update_system_status(self):
        """Update system status information"""
        try:
            import psutil
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_mb = memory.used // (1024 * 1024)
            memory_percent = memory.percent
            
            self.status_memory.setText(f"💾 Memory: {memory_mb} MB ({memory_percent:.1f}%)")
            
            # Update memory color based on usage
            if memory_percent > 80:
                color = "#e74c3c"  # Red
            elif memory_percent > 60:
                color = "#f39c12"  # Orange  
            else:
                color = "#27ae60"  # Green
            
            self.status_memory.setStyleSheet(f"color: {color}; padding: 2px 8px;")
            
            # CPU usage for performance indicator
            cpu_percent = psutil.cpu_percent(interval=None)
            if cpu_percent > 80:
                performance = "⚡ Performance: Heavy"
                perf_color = "#e74c3c"
            elif cpu_percent > 50:
                performance = "⚡ Performance: Moderate"
                perf_color = "#f39c12"
            else:
                performance = "⚡ Performance: Good"
                perf_color = "#27ae60"
            
            self.status_performance.setText(performance)
            self.status_performance.setStyleSheet(f"color: {perf_color}; padding: 2px 8px;")
            
        except ImportError:
            # psutil not available, show static info
            self.status_memory.setText("💾 Memory: -- MB")
            self.status_performance.setText("⚡ Performance: --")
    
    def _setup_menu_bar(self):
        """Setup minimal menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 4px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #3498db;
            }
            QMenu {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
            }
            QMenu::item {
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #3498db;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        new_action = QAction("🆕 New Project", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("📂 Open Project", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("💾 Save Project", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("📤 Export Design", self)
        export_action.triggered.connect(self.export_design)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("❌ Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("✏️ Edit")
        
        undo_action = QAction("↶ Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("↷ Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("🔲 Select All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)
        
        delete_action = QAction("🗑️ Delete", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.delete_selected)
        edit_menu.addAction(delete_action)
        
        # View menu
        view_menu = menubar.addMenu("👁️ View")
        
        zoom_in_action = QAction("🔍+ Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("🔍- Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        fit_action = QAction("⬜ Fit to Window", self)
        fit_action.setShortcut(QKeySequence("F"))
        fit_action.triggered.connect(self.fit_to_window)
        view_menu.addAction(fit_action)
        
        view_menu.addSeparator()
        
        grid_action = QAction("⌗ Grid Settings", self)
        grid_action.setShortcut(QKeySequence("G"))
        grid_action.triggered.connect(self.show_grid_settings)
        view_menu.addAction(grid_action)
        
        properties_action = QAction("🔧 Properties Panel", self)
        properties_action.setShortcut(QKeySequence("P"))
        properties_action.setCheckable(True)
        properties_action.triggered.connect(self.toggle_properties_panel)
        view_menu.addAction(properties_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("🔧 Tools")
        
        select_tool_action = QAction("🔍 Select Tool", self)
        select_tool_action.setShortcut(QKeySequence("S"))
        select_tool_action.triggered.connect(self.select_tool)
        tools_menu.addAction(select_tool_action)
        
        pan_tool_action = QAction("✋ Pan Tool", self)
        pan_tool_action.setShortcut(QKeySequence("H"))
        pan_tool_action.triggered.connect(self.pan_tool)
        tools_menu.addAction(pan_tool_action)
        
        tools_menu.addSeparator()
        
        component_search_action = QAction("🔍 Find Components", self)
        component_search_action.setShortcut(QKeySequence.StandardKey.Find)
        component_search_action.triggered.connect(self.show_component_search)
        tools_menu.addAction(component_search_action)
        
        encyclopedia_action = QAction("📚 Component Encyclopedia", self)
        encyclopedia_action.setShortcut(QKeySequence("Ctrl+E"))
        encyclopedia_action.triggered.connect(self.show_encyclopedia)
        tools_menu.addAction(encyclopedia_action)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        
        shortcuts_action = QAction("⌨️ Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)
        
        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _setup_connections(self):
        """Setup signal connections"""
        if hasattr(self.canvas, 'zoom_changed'):
            self.canvas.zoom_changed.connect(self.update_zoom_status)
        
        if hasattr(self.canvas, 'component_added'):
            self.canvas.component_added.connect(self.on_canvas_component_added)
            
        if hasattr(self.canvas, 'component_selected'):
            self.canvas.component_selected.connect(self.on_canvas_component_selected)
        
        if hasattr(self.component_palette, 'component_selected'):
            self.component_palette.component_selected.connect(self.on_component_selected)
        
        if hasattr(self.component_palette, 'component_double_clicked'):
            self.component_palette.component_double_clicked.connect(self.on_component_add)
        
        print("✅ Signal connections established")
    
    def update_zoom_status(self, zoom_factor):
        """Update zoom status in status bar"""
        self.status_zoom.setText(f"🔍 {int(zoom_factor * 100)}%")
        
    def on_canvas_component_added(self, category, component, position):
        """Handle component added to canvas"""
        component_count = len(getattr(self.canvas, 'components', {}))
        self.status_components.setText(f"📦 {component_count} Components")
        self.status_project.setText("📋 Modified")
        print(f"📦 Canvas component added: {component}")
        
    def on_canvas_component_selected(self, component_item):
        """Handle component selected on canvas"""
        if component_item:
            self.selected_component = component_item
            print(f"🎯 Canvas component selected: {component_item.name}")
            
            # Show properties panel
            if not self.properties_dock.isVisible():
                self.properties_dock.show()
                self.properties_panel.show()
        else:
            self.selected_component = None
    
    def _setup_shortcuts(self):
        """Setup additional keyboard shortcuts"""
        shortcuts = [
            ('Space', self.show_toolbar),
            ('Ctrl+1', lambda: self.set_tool('select')),
            ('Ctrl+2', lambda: self.set_tool('pan')),
            ('Escape', self.cancel_current_action),
            ('Ctrl+Shift+P', self.show_command_palette)
        ]
        
        for key, callback in shortcuts:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(callback)
    
    def _apply_clean_theme(self):
        """Apply clean, modern theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                color: #2c3e50;
            }
            QDockWidget {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
            }
            QDockWidget::title {
                background-color: #e9ecef;
                padding: 6px;
                font-weight: bold;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10px;
            }
        """)
    
    # Signal handlers
    def on_component_selected(self, category, component):
        """Handle component selection"""
        self.selected_component = (category, component)
        print(f"📦 Component selected: {component} from {category}")
        
        # Show properties panel if hidden
        if not self.properties_dock.isVisible():
            self.properties_dock.show()
            self.properties_panel.show()
    
    def on_component_add(self, category, component):
        """Handle component addition to canvas"""
        print(f"➕ Adding {component} from {category} to canvas")
        # This would add the component to the canvas
        component_count = len(getattr(self.canvas, 'components', {}))
        self.status_components.setText(f"📦 {component_count} Components")
    
    # Menu actions
    def new_project(self):
        """Create new project"""
        print("🆕 New project")
        self.current_project = None
        self.setWindowTitle("X-Seti Visual Retro System Emulator Builder - CLEAN")
    
    def open_project(self):
        """Open existing project"""
        print("📂 Open project")
        # Implementation for project opening
    
    def save_project(self):
        """Save current project"""
        print("💾 Save project")
        # Implementation for project saving
    
    def export_design(self):
        """Export design"""
        print("📤 Export design")
        # Implementation for design export
    
    def undo(self):
        """Undo last action"""
        print("↶ Undo")
        if hasattr(self.canvas, 'undo'):
            self.canvas.undo()
    
    def redo(self):
        """Redo last action"""
        print("↷ Redo")
        if hasattr(self.canvas, 'redo'):
            self.canvas.redo()
    
    def select_all(self):
        """Select all components"""
        print("🔲 Select all")
        if hasattr(self.canvas, 'select_all'):
            self.canvas.select_all()
    
    def delete_selected(self):
        """Delete selected components"""
        print("🗑️ Delete selected")
        if hasattr(self.canvas, 'delete_selected'):
            self.canvas.delete_selected()
    
    def zoom_in(self):
        """Zoom in"""
        if hasattr(self.canvas, 'zoom_in'):
            self.canvas.zoom_in()
    
    def zoom_out(self):
        """Zoom out"""
        if hasattr(self.canvas, 'zoom_out'):
            self.canvas.zoom_out()
    
    def fit_to_window(self):
        """Fit canvas to window"""
        if hasattr(self.canvas, 'fit_to_window'):
            self.canvas.fit_to_window()
    
    def show_grid_settings(self):
        """Show grid settings dialog"""
        if hasattr(self.canvas, 'show_grid_settings'):
            self.canvas.show_grid_settings()
    
    def toggle_properties_panel(self):
        """Toggle properties panel visibility"""
        if self.properties_dock.isVisible():
            self.properties_dock.hide()
        else:
            self.properties_dock.show()
    
    def select_tool(self):
        """Activate select tool"""
        if hasattr(self.canvas, 'set_current_tool'):
            self.canvas.set_current_tool('select')
        self.status_tool.setText("🔍 Select Tool")
    
    def pan_tool(self):
        """Activate pan tool"""
        if hasattr(self.canvas, 'set_current_tool'):
            self.canvas.set_current_tool('pan')
        self.status_tool.setText("✋ Pan Tool")
    
    def show_layers(self):
        """Show layers panel"""
        print("📄 Layers panel")
        # Implementation for layers
    
    def set_tool(self, tool):
        """Set current tool"""
        if hasattr(self.canvas, 'set_current_tool'):
            self.canvas.set_current_tool(tool)
        self.status_tool.setText(f"🔧 {tool.title()} Tool")
    
    def show_component_search(self):
        """Show component search"""
        if hasattr(self.component_palette, 'set_search_focus'):
            self.component_palette.set_search_focus()
        print("🔍 Component search focused")
    
    def show_encyclopedia(self):
        """Show component encyclopedia"""
        if hasattr(self.component_palette, '_open_encyclopedia'):
            self.component_palette._open_encyclopedia()
        print("📚 Component encyclopedia opened")
    
    def show_toolbar(self):
        """Show floating toolbar - DISABLED since we have fixed toolbar"""
        print("🔧 Fixed toolbar already visible at top")
        # Do nothing - we have a fixed toolbar now
    
    def cancel_current_action(self):
        """Cancel current action"""
        print("❌ Action cancelled")
        self.select_tool()  # Return to select tool
    
    def show_command_palette(self):
        """Show command palette"""
        print("⌨️ Command palette (future feature)")
        # Future: Quick command search dialog
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        shortcuts_text = """
        Keyboard Shortcuts:
        
        Tools:
        S - Select Tool
        H - Pan Tool
        Space - Show Toolbar
        
        View:
        + - Zoom In
        - - Zoom Out
        F - Fit to Window
        G - Grid Settings
        P - Properties Panel
        
        Edit:
        Ctrl+Z - Undo
        Ctrl+Y - Redo
        Ctrl+A - Select All
        Delete - Delete Selected
        
        File:
        Ctrl+N - New Project
        Ctrl+O - Open Project
        Ctrl+S - Save Project
        
        Search:
        Ctrl+F - Find Components
        Ctrl+E - Component Encyclopedia
        """
        
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        X-Seti Visual Retro System Emulator Builder
        
        A modern, clean interface for building virtual retro computer systems.
        
        Features:
        • Clean, minimal UI with floating menus
        • Component bubbles with quick info
        • Comprehensive component encyclopedia
        • Advanced grid and canvas controls
        • Keyboard shortcuts for efficiency
        
        Version: Clean UI Edition
        Date: June 16, 2025
        """
        
        QMessageBox.about(self, "About X-Seti", about_text)

# For compatibility
FixedMainWindow = CleanMainWindow
MainWindow = CleanMainWindow
EnhancedMainWindow = CleanMainWindow

# Export
__all__ = ['CleanMainWindow', 'MainWindow', 'FixedMainWindow', 'EnhancedMainWindow',
           'MinimalPropertiesPanel', 'StatusIndicator']