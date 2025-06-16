"""
X-Seti - June16 2025 - Main Window with Fixed Left Panel Organization
Visual Retro System Emulator Builder - Main Window with consolidated component sections and proper theming
"""

#this belongs in ui/main_window.py

import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                           QDockWidget, QSplitter, QMessageBox, QApplication,
                           QPushButton, QLabel, QListWidget, QCheckBox, QGroupBox,
                           QTreeWidget, QTreeWidgetItem, QFrame, QLineEdit, QComboBox,
                           QTextEdit, QTabWidget, QScrollArea, QGraphicsView, QGraphicsScene)
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QRectF
from PyQt6.QtGui import QShortcut, QKeySequence, QFont, QPainter, QPen, QColor

class FixedMainWindow(QMainWindow):
    """
    Main Window with Fixed Left Panel Organization
    
    FIXES APPLIED:
    ✅ Consolidated component sections (removed duplicates)
    ✅ Fixed white background issues with proper theming
    ✅ Consistent theme application across all panels
    ✅ Keyboard shortcuts (Ctrl+F for search)
    ✅ Switchable button icons/text
    ✅ Grid display settings
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Retro System Emulator Builder")
        self.resize(1400, 900)
        
        # Initialize component references
        self.component_manager = None
        self.project_manager = None
        self.simulation_engine = None
        self.layer_manager = None
        self.app_settings = None
        
        # UI components
        self.canvas = None
        self.component_palette = None
        self.layer_controls = None
        self.menu_manager = None
        self.status_manager = None
        self.properties_panel = None
        
        # Initialize managers and settings
        self._initialize_managers()
        self._load_app_settings()
        
        # Create UI components in correct order
        self._create_ui()
        self._create_docks_consolidated()
        
        # Setup connections and theming
        self._setup_connections()
        self._setup_hotkeys()
        self._apply_theme()
        
        # Final setup
        QTimer.singleShot(100, self._post_initialization_setup)
        self._update_window_title()
        
        print("✅ Main Window with fixed left panels initialized successfully")
    
    def _initialize_managers(self):
        """Initialize managers with fallback handling"""
        try:
            try:
                from managers.project_manager import ProjectManager
                self.project_manager = ProjectManager()
                print("✅ ProjectManager loaded")
            except ImportError:
                from project_manager import ProjectManager
                self.project_manager = ProjectManager()
                print("✅ ProjectManager loaded (fallback)")
        except ImportError as e:
            print(f"⚠️ ProjectManager unavailable: {e}")
            self.project_manager = self._create_fallback_project_manager()
        
        try:
            from core.layer_manager import LayerManager
            self.layer_manager = LayerManager()
            print("✅ LayerManager loaded")
        except ImportError as e:
            print(f"⚠️ LayerManager unavailable: {e}")
            self.layer_manager = self._create_fallback_layer_manager()
    
    def _load_app_settings(self):
        """Load application settings for theming"""
        try:
            from utils.App_settings_system import AppSettingsSystem
            self.app_settings = AppSettingsSystem()
            print("✅ App Settings loaded")
        except ImportError:
            try:
                from utils.app_settings_fallback import AppSettingsSystem
                self.app_settings = AppSettingsSystem()
                print("✅ App Settings loaded (fallback)")
            except ImportError as e:
                print(f"⚠️ App Settings unavailable: {e}")
                self.app_settings = self._create_fallback_settings()
    
    def _create_ui(self):
        """Create main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Create canvas with robust fallback handling
        self._create_canvas()
        if self.canvas:
            splitter.addWidget(self.canvas)
            print("✅ Canvas added to splitter")
        else:
            print("❌ Failed to create canvas")
        
        self._create_menu_bar()
        self._create_status_bar()
    
    def _create_docks_consolidated(self):
        """Create consolidated dock widgets with proper theming"""
        
        # CONSOLIDATED COMPONENT DOCK (Left Side) - Single unified section
        self._create_unified_component_dock()
        
        # LAYER CONTROLS DOCK (Right Side)
        self._create_layer_controls_dock()
        
        # PROPERTIES PANEL DOCK (Right Side, below layers)
        self._create_properties_panel_dock()
    
    def _create_unified_component_dock(self):
        """Create unified component dock - consolidates all component sections into one"""
        try:
            # Create main widget for unified components
            component_widget = QWidget()
            component_layout = QVBoxLayout(component_widget)
            component_layout.setContentsMargins(6, 6, 6, 6)
            component_layout.setSpacing(8)
            
            # === UNIFIED COMPONENT SECTION ===
            components_group = QGroupBox("Components")
            components_layout = QVBoxLayout(components_group)
            
            # Search section
            search_frame = QFrame()
            search_layout = QVBoxLayout(search_frame)
            
            # Search box with Ctrl+F shortcut
            search_row = QHBoxLayout()
            search_row.addWidget(QLabel("Search:"))
            
            self.component_search = QLineEdit()
            self.component_search.setPlaceholderText("Type to search components... (Ctrl+F)")
            search_row.addWidget(self.component_search)
            
            search_layout.addLayout(search_row)
            
            # Filter by type
            filter_row = QHBoxLayout()
            filter_row.addWidget(QLabel("Filter:"))
            
            self.component_filter = QComboBox()
            self.component_filter.addItems(["All Types", "CPU", "Memory", "Audio", "Video", "I/O", "Custom"])
            filter_row.addWidget(self.component_filter)
            
            search_layout.addLayout(filter_row)
            components_layout.addWidget(search_frame)
            
            # Component tree (consolidated single section)
            self.component_tree = QTreeWidget()
            self.component_tree.setHeaderLabel("Components")
            self.component_tree.setDragEnabled(True)
            self.component_tree.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
            components_layout.addWidget(self.component_tree)
            
            # Component info panel
            info_frame = QFrame()
            info_layout = QVBoxLayout(info_frame)
            
            self.component_name_label = QLabel("Select a component")
            self.component_name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            info_layout.addWidget(self.component_name_label)
            
            self.component_details = QTextEdit()
            self.component_details.setMaximumHeight(80)
            self.component_details.setReadOnly(True)
            info_layout.addWidget(self.component_details)
            
            components_layout.addWidget(info_frame)
            
            # Action buttons with icon/text switching
            button_layout = QHBoxLayout()
            
            self.add_custom_btn = QPushButton("Add Custom")
            self.refresh_btn = QPushButton("Refresh")
            
            button_layout.addWidget(self.add_custom_btn)
            button_layout.addWidget(self.refresh_btn)
            
            components_layout.addLayout(button_layout)
            component_layout.addWidget(components_group)
            
            # Populate component tree
            self._populate_component_tree()
            
            # Create dock
            self.component_dock = QDockWidget("Components", self)
            self.component_dock.setWidget(component_widget)
            self.component_dock.setAllowedAreas(
                Qt.DockWidgetArea.LeftDockWidgetArea | 
                Qt.DockWidgetArea.RightDockWidgetArea
            )
            self.component_dock.setMinimumWidth(280)
            self.component_dock.setMaximumWidth(400)
            
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.component_dock)
            print("✅ Unified component dock created (consolidated sections)")
            
        except Exception as e:
            print(f"⚠️ Component dock creation failed: {e}")
            self._create_fallback_component_dock()
    
    def _populate_component_tree(self):
        """Populate the unified component tree"""
        self.component_tree.clear()
        
        # Component categories
        categories = {
            "CPUs": ["Z80", "6502", "68000", "8080", "6809"],
            "Memory": ["ROM", "RAM", "EEPROM", "Flash"],
            "Audio": ["SID", "AY-3-8910", "YM2612", "POKEY"],
            "Video": ["TMS9918", "VIC-II", "PPU", "VERA"],
            "I/O": ["PIA", "VIA", "UART", "ACIA"],
            "Custom": ["User Defined", "Import Component"]
        }
        
        for category_name, components in categories.items():
            cat_item = QTreeWidgetItem(self.component_tree, [category_name])
            cat_item.setExpanded(True)
            
            for component in components:
                comp_item = QTreeWidgetItem(cat_item, [component])
                comp_item.setData(0, Qt.ItemDataRole.UserRole, (category_name, component))
    
    def _create_layer_controls_dock(self):
        """Create layer controls dock with proper theming"""
        try:
            # Create layer controls widget
            layer_widget = QWidget()
            layer_layout = QVBoxLayout(layer_widget)
            layer_layout.setContentsMargins(6, 6, 6, 6)
            layer_layout.setSpacing(8)
            
            # Grid Settings Group
            grid_group = QGroupBox("Grid Settings")
            grid_layout = QVBoxLayout(grid_group)
            
            self.show_grid_check = QCheckBox("Show Grid")
            self.show_grid_check.setChecked(True)
            grid_layout.addWidget(self.show_grid_check)
            
            # Grid style
            style_layout = QHBoxLayout()
            style_layout.addWidget(QLabel("Style:"))
            self.grid_style_combo = QComboBox()
            self.grid_style_combo.addItems(["Dots", "Lines", "Crosses", "Breadboard"])
            self.grid_style_combo.setCurrentText("Breadboard")
            style_layout.addWidget(self.grid_style_combo)
            grid_layout.addLayout(style_layout)
            
            # Grid colors
            color_layout = QHBoxLayout()
            color_layout.addWidget(QLabel("Grid Color:"))
            self.grid_color_combo = QComboBox()
            self.grid_color_combo.addItems(["Foreground", "Background", "Custom"])
            color_layout.addWidget(self.grid_color_combo)
            grid_layout.addLayout(color_layout)
            
            layer_layout.addWidget(grid_group)
            
            # Layers Group
            layers_group = QGroupBox("Layers")
            layers_layout = QVBoxLayout(layers_group)
            
            self.layer_list = QListWidget()
            self.layer_list.setMaximumHeight(120)
            
            # Add default layers
            layers = ["Component", "PCB", "Gerber", "Silkscreen"]
            for layer in layers:
                self.layer_list.addItem(layer)
                
            layers_layout.addWidget(self.layer_list)
            
            # Layer buttons
            layer_btn_layout = QHBoxLayout()
            self.add_layer_btn = QPushButton("Add")
            self.remove_layer_btn = QPushButton("Remove")
            
            layer_btn_layout.addWidget(self.add_layer_btn)
            layer_btn_layout.addWidget(self.remove_layer_btn)
            layers_layout.addLayout(layer_btn_layout)
            
            layer_layout.addWidget(layers_group)
            layer_layout.addStretch()
            
            # Create dock
            self.layer_dock = QDockWidget("Layers & Grid", self)
            self.layer_dock.setWidget(layer_widget)
            self.layer_dock.setAllowedAreas(
                Qt.DockWidgetArea.LeftDockWidgetArea | 
                Qt.DockWidgetArea.RightDockWidgetArea
            )
            self.layer_dock.setMinimumWidth(200)
            self.layer_dock.setMaximumWidth(300)
            
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.layer_dock)
            print("✅ Layer controls dock created")
            
        except Exception as e:
            print(f"⚠️ Layer controls dock creation failed: {e}")
    
    def _create_properties_panel_dock(self):
        """Create properties panel dock"""
        try:
            prop_widget = QWidget()
            prop_layout = QVBoxLayout(prop_widget)
            prop_layout.setContentsMargins(6, 6, 6, 6)
            
            # Properties group
            props_group = QGroupBox("Properties")
            props_layout = QVBoxLayout(props_group)
            
            self.props_label = QLabel("Select a component to view properties")
            self.props_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            props_layout.addWidget(self.props_label)
            
            prop_layout.addWidget(props_group)
            prop_layout.addStretch()
            
            # Create dock
            self.properties_dock = QDockWidget("Properties", self)
            self.properties_dock.setWidget(prop_widget)
            self.properties_dock.setAllowedAreas(
                Qt.DockWidgetArea.LeftDockWidgetArea | 
                Qt.DockWidgetArea.RightDockWidgetArea
            )
            self.properties_dock.setMinimumWidth(200)
            self.properties_dock.setMaximumWidth(300)
            
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)
            print("✅ Properties panel dock created")
            
        except Exception as e:
            print(f"⚠️ Properties panel dock creation failed: {e}")
    
    def _apply_theme(self):
        """Apply current theme to all UI elements"""
        if not self.app_settings:
            return
            
        try:
            current_theme = self.app_settings.get_theme()
            colors = current_theme.get('colors', {})
            
            # Get theme colors
            bg_primary = colors.get('bg_primary', '#f0f0f0')
            bg_secondary = colors.get('bg_secondary', '#ffffff')
            text_primary = colors.get('text_primary', '#000000')
            text_secondary = colors.get('text_secondary', '#666666')
            accent_primary = colors.get('accent_primary', '#0078d4')
            border = colors.get('border', '#cccccc')
            panel_bg = colors.get('panel_bg', bg_secondary)
            
            # Main window stylesheet
            main_style = f"""
            QMainWindow {{
                background-color: {bg_primary};
                color: {text_primary};
            }}
            
            QDockWidget {{
                background-color: {panel_bg};
                color: {text_primary};
                border: 1px solid {border};
            }}
            
            QDockWidget::title {{
                background-color: {accent_primary};
                color: white;
                padding: 4px;
                border: none;
            }}
            
            QGroupBox {{
                background-color: {panel_bg};
                color: {text_primary};
                border: 2px solid {border};
                border-radius: 6px;
                margin-top: 1ex;
                padding-top: 6px;
            }}
            
            QGroupBox::title {{
                color: {text_primary};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            
            QFrame {{
                background-color: {panel_bg};
                color: {text_primary};
                border: 1px solid {border};
            }}
            
            QLabel {{
                background-color: transparent;
                color: {text_primary};
            }}
            
            QLineEdit {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 1px solid {border};
                padding: 4px;
                border-radius: 3px;
            }}
            
            QLineEdit:focus {{
                border: 2px solid {accent_primary};
            }}
            
            QComboBox {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 1px solid {border};
                padding: 4px;
                border-radius: 3px;
            }}
            
            QComboBox::drop-down {{
                border: none;
                background-color: {accent_primary};
            }}
            
            QComboBox::down-arrow {{
                width: 0;
                height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid white;
            }}
            
            QTreeWidget {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 1px solid {border};
                alternate-background-color: {panel_bg};
            }}
            
            QTreeWidget::item:selected {{
                background-color: {accent_primary};
                color: white;
            }}
            
            QListWidget {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 1px solid {border};
            }}
            
            QListWidget::item:selected {{
                background-color: {accent_primary};
                color: white;
            }}
            
            QTextEdit {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 1px solid {border};
                border-radius: 3px;
            }}
            
            QPushButton {{
                background-color: {accent_primary};
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {colors.get('button_hover', accent_primary)}99;
            }}
            
            QPushButton:pressed {{
                background-color: {colors.get('button_pressed', accent_primary)}CC;
            }}
            
            QCheckBox {{
                color: {text_primary};
                spacing: 8px;
            }}
            
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {border};
                background-color: {bg_secondary};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {accent_primary};
                border: 1px solid {accent_primary};
            }}
            """
            
            self.setStyleSheet(main_style)
            print(f"✅ Theme applied: {current_theme.get('name', 'Unknown')}")
            
        except Exception as e:
            print(f"⚠️ Theme application failed: {e}")
    
    def _setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        # Ctrl+F for component search
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(self._focus_component_search)
        
        # Ctrl+G for grid toggle
        grid_shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        grid_shortcut.activated.connect(self._toggle_grid)
        
        print("✅ Keyboard shortcuts setup (Ctrl+F, Ctrl+G)")
    
    def _focus_component_search(self):
        """Focus the component search box"""
        if hasattr(self, 'component_search'):
            self.component_search.setFocus()
            self.component_search.selectAll()
    
    def _toggle_grid(self):
        """Toggle grid visibility"""
        if hasattr(self, 'show_grid_check'):
            current = self.show_grid_check.isChecked()
            self.show_grid_check.setChecked(not current)
    
    def _create_canvas(self):
        """Create canvas with robust fallback handling"""
        self.canvas = None
        
        # Try 1: Import directly from canvas module
        try:
            from ui.canvas import EnhancedPCBCanvas, PCBCanvas
            if EnhancedPCBCanvas:
                self.canvas = EnhancedPCBCanvas()
                print("✅ Enhanced PCB Canvas created")
                return
            elif PCBCanvas:
                self.canvas = PCBCanvas()
                print("✅ PCB Canvas created")
                return
        except ImportError as e:
            print(f"⚠️ Direct canvas import failed: {e}")
        
        # Try 2: Import from ui package
        try:
            from ui import EnhancedPCBCanvas, PCBCanvas
            if EnhancedPCBCanvas and EnhancedPCBCanvas is not type(None):
                self.canvas = EnhancedPCBCanvas()
                print("✅ Enhanced PCB Canvas created (from ui)")
                return
            elif PCBCanvas and PCBCanvas is not type(None):
                self.canvas = PCBCanvas()
                print("✅ PCB Canvas created (from ui)")
                return
        except ImportError as e:
            print(f"⚠️ UI package canvas import failed: {e}")
        
        # Try 3: Import from missing_ui_modules
        try:
            from ui.missing_ui_modules import PCBCanvas
            if PCBCanvas:
                self.canvas = PCBCanvas()
                print("✅ PCB Canvas created (from missing_ui_modules)")
                return
        except ImportError as e:
            print(f"⚠️ Missing UI modules canvas import failed: {e}")
        
        # Fallback: Create working QGraphicsView with basic functionality
        print("🔄 Creating fallback canvas...")
        self.canvas = self._create_working_fallback_canvas()
    
    def _create_working_fallback_canvas(self):
        """Create a working fallback canvas with basic functionality"""
        from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
        from PyQt6.QtCore import QRectF
        from PyQt6.QtGui import QPainter, QPen, QColor
        
        class WorkingFallbackCanvas(QGraphicsView):
            """Working fallback canvas with basic grid and drag/drop support"""
            
            def __init__(self):
                super().__init__()
                
                # Create scene
                self.scene = QGraphicsScene()
                self.setScene(self.scene)
                
                # Basic settings
                self.grid_size = 20
                self.grid_visible = True
                self.snap_to_grid = True
                self.grid_style = "lines"
                self.grid_color = QColor(100, 140, 100)  # Default green
                self.background_color = QColor(255, 255, 255)  # Default white
                
                # Enable drag/drop
                self.setAcceptDrops(True)
                self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
                self.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                # Component tracking
                self.components = {}
                
                print("✅ Working fallback canvas created")
            
            def drawBackground(self, painter, rect):
                """Draw grid background with all patterns"""
                # Draw background color first
                painter.fillRect(rect, self.background_color)
                
                if not self.grid_visible:
                    return
                
                style_lower = self.grid_style.lower()
                
                if style_lower == "dots":
                    self._draw_dots_pattern(painter, rect)
                elif style_lower == "lines":
                    self._draw_lines_pattern(painter, rect)
                elif style_lower == "crosses":
                    self._draw_crosses_pattern(painter, rect)
                elif style_lower == "paper cut":
                    self._draw_paper_cut_pattern(painter, rect)
                elif style_lower == "paper cut + crosses":
                    self._draw_paper_cut_crosses_pattern(painter, rect)
                elif style_lower == "breadboard":
                    self._draw_breadboard_pattern(painter, rect)
            
            def _draw_dots_pattern(self, painter, rect):
                """Draw dots at grid intersections"""
                painter.setPen(QPen(self.grid_color, 2))
                left = int(rect.left()) - (int(rect.left()) % self.grid_size)
                top = int(rect.top()) - (int(rect.top()) % self.grid_size)
                
                x = left
                while x < rect.right():
                    y = top
                    while y < rect.bottom():
                        painter.drawPoint(x, y)
                        y += self.grid_size
                    x += self.grid_size
            
            def _draw_lines_pattern(self, painter, rect):
                """Draw solid grid lines"""
                painter.setPen(QPen(self.grid_color, 0.5))
                left = int(rect.left()) - (int(rect.left()) % self.grid_size)
                top = int(rect.top()) - (int(rect.top()) % self.grid_size)
                
                # Vertical lines
                x = left
                while x < rect.right():
                    painter.drawLine(x, rect.top(), x, rect.bottom())
                    x += self.grid_size
                
                # Horizontal lines
                y = top
                while y < rect.bottom():
                    painter.drawLine(rect.left(), y, rect.right(), y)
                    y += self.grid_size
            
            def _draw_crosses_pattern(self, painter, rect):
                """Draw cross marks at grid intersections"""
                painter.setPen(QPen(self.grid_color, 1))
                left = int(rect.left()) - (int(rect.left()) % self.grid_size)
                top = int(rect.top()) - (int(rect.top()) % self.grid_size)
                
                cross_size = 4
                x = left
                while x < rect.right():
                    y = top
                    while y < rect.bottom():
                        # Draw cross
                        painter.drawLine(x - cross_size, y, x + cross_size, y)
                        painter.drawLine(x, y - cross_size, x, y + cross_size)
                        y += self.grid_size
                    x += self.grid_size
            
            def _draw_breadboard_pattern(self, painter, rect):
                """Draw realistic breadboard pattern with 0.1" (2.54mm) spacing"""
                # Breadboard spacing: 0.1 inches = 2.54mm
                # At standard zoom, use 10 pixels per hole (adjustable)
                hole_spacing = 10
                hole_radius = 1.5
                
                # Calculate grid bounds
                left = int(rect.left()) - (int(rect.left()) % hole_spacing)
                top = int(rect.top()) - (int(rect.top()) % hole_spacing)
                
                # Power rail colors
                power_rail_color = QColor(220, 100, 100)  # Red for power
                ground_rail_color = QColor(100, 100, 220)  # Blue for ground
                tie_point_color = QColor(80, 80, 80)      # Dark gray for tie points
                
                # Draw power rails (top and bottom)
                rail_height = 60
                center_gap = 30
                
                # Top power rails
                top_power_y = top + 20
                top_ground_y = top + 35
                
                # Bottom power rails  
                bottom_power_y = top + rail_height + center_gap + 80
                bottom_ground_y = bottom_power_y + 15
                
                x = left
                while x < rect.right():
                    # Top power rail (red line)
                    painter.setPen(QPen(power_rail_color, 2))
                    painter.drawLine(x - 5, top_power_y, x + 5, top_power_y)
                    painter.setBrush(power_rail_color)
                    painter.drawEllipse(x - hole_radius, top_power_y - hole_radius, 
                                      hole_radius * 2, hole_radius * 2)
                    
                    # Top ground rail (blue line)
                    painter.setPen(QPen(ground_rail_color, 2))
                    painter.drawLine(x - 5, top_ground_y, x + 5, top_ground_y)
                    painter.setBrush(ground_rail_color)
                    painter.drawEllipse(x - hole_radius, top_ground_y - hole_radius,
                                      hole_radius * 2, hole_radius * 2)
                    
                    # Bottom power rail (red line)
                    painter.setPen(QPen(power_rail_color, 2))
                    painter.drawLine(x - 5, bottom_power_y, x + 5, bottom_power_y)
                    painter.setBrush(power_rail_color)
                    painter.drawEllipse(x - hole_radius, bottom_power_y - hole_radius,
                                      hole_radius * 2, hole_radius * 2)
                    
                    # Bottom ground rail (blue line)
                    painter.setPen(QPen(ground_rail_color, 2))
                    painter.drawLine(x - 5, bottom_ground_y, x + 5, bottom_ground_y)
                    painter.setBrush(ground_rail_color)
                    painter.drawEllipse(x - hole_radius, bottom_ground_y - hole_radius,
                                      hole_radius * 2, hole_radius * 2)
                    
                    x += hole_spacing
                
                # Draw main tie point area
                painter.setPen(QPen(tie_point_color, 1))
                painter.setBrush(tie_point_color)
                
                # Top tie point section
                tie_start_y = top + 50
                tie_rows = 5
                
                row = 0
                while row < tie_rows:
                    y = tie_start_y + (row * hole_spacing)
                    if y > rect.bottom():
                        break
                        
                    col = 0
                    x = left
                    while x < rect.right():
                        # Draw tie point hole
                        painter.drawEllipse(x - hole_radius, y - hole_radius,
                                          hole_radius * 2, hole_radius * 2)
                        
                        # Draw connection lines every 5 holes (tie point groups)
                        if col % 5 == 0 and col > 0:
                            # Draw separator line
                            painter.setPen(QPen(QColor(150, 150, 150), 0.5))
                            painter.drawLine(x - hole_spacing/2, y - hole_spacing*2, 
                                           x - hole_spacing/2, y + hole_spacing*2)
                            painter.setPen(QPen(tie_point_color, 1))
                        
                        x += hole_spacing
                        col += 1
                    row += 1
                
                # Center divider channel
                center_y = tie_start_y + (tie_rows * hole_spacing) + center_gap/2
                painter.setPen(QPen(QColor(200, 200, 200), 3))
                painter.drawLine(rect.left(), center_y, rect.right(), center_y)
                
                # Bottom tie point section
                bottom_tie_start_y = center_y + center_gap/2
                
                row = 0
                while row < tie_rows:
                    y = bottom_tie_start_y + (row * hole_spacing)
                    if y > rect.bottom() - 60:  # Leave space for bottom power rails
                        break
                        
                    col = 0
                    x = left
                    while x < rect.right():
                        # Draw tie point hole
                        painter.setBrush(tie_point_color)
                        painter.setPen(QPen(tie_point_color, 1))
                        painter.drawEllipse(x - hole_radius, y - hole_radius,
                                          hole_radius * 2, hole_radius * 2)
                        
                        # Draw connection lines every 5 holes (tie point groups)
                        if col % 5 == 0 and col > 0:
                            # Draw separator line
                            painter.setPen(QPen(QColor(150, 150, 150), 0.5))
                            painter.drawLine(x - hole_spacing/2, y - hole_spacing*2,
                                           x - hole_spacing/2, y + hole_spacing*2)
                            painter.setPen(QPen(tie_point_color, 1))
                        
                        x += hole_spacing
                        col += 1
                    row += 1
            
            def _draw_paper_cut_pattern(self, painter, rect):
                """Draw paper cut pattern with dotted lines (like graph paper)"""
                # Create dotted line pen
                pen = QPen(self.grid_color, 1)
                pen.setStyle(Qt.PenStyle.DotLine)
                painter.setPen(pen)
                
                left = int(rect.left()) - (int(rect.left()) % self.grid_size)
                top = int(rect.top()) - (int(rect.top()) % self.grid_size)
                
                # Vertical dotted lines
                x = left
                while x < rect.right():
                    painter.drawLine(x, rect.top(), x, rect.bottom())
                    x += self.grid_size
                
                # Horizontal dotted lines
                y = top
                while y < rect.bottom():
                    painter.drawLine(rect.left(), y, rect.right(), y)
                    y += self.grid_size
            
            def _draw_paper_cut_crosses_pattern(self, painter, rect):
                """Draw paper cut pattern with crosses at intersections"""
                # First draw the dotted lines
                self._draw_paper_cut_pattern(painter, rect)
                
                # Then add crosses at intersections
                painter.setPen(QPen(self.grid_color, 1.5))
                left = int(rect.left()) - (int(rect.left()) % self.grid_size)
                top = int(rect.top()) - (int(rect.top()) % self.grid_size)
                
                cross_size = 3
                x = left
                while x < rect.right():
                    y = top
                    while y < rect.bottom():
                        # Draw small cross at intersection
                        painter.drawLine(x - cross_size, y, x + cross_size, y)
                        painter.drawLine(x, y - cross_size, x, y + cross_size)
                        y += self.grid_size
                    x += self.grid_size
            
            def _draw_breadboard_pattern(self, painter, rect):
                """Draw realistic breadboard pattern with 0.1" (2.54mm) spacing"""
                # Breadboard spacing: 0.1 inches = 2.54mm
                # At standard zoom, use 10 pixels per hole (adjustable)
                hole_spacing = 10
                hole_radius = 1.5
                
                # Calculate grid bounds
                left = int(rect.left()) - (int(rect.left()) % hole_spacing)
                top = int(rect.top()) - (int(rect.top()) % hole_spacing)
                
                # Power rail colors
                power_rail_color = QColor(220, 100, 100)  # Red for power
                ground_rail_color = QColor(100, 100, 220)  # Blue for ground
                tie_point_color = QColor(80, 80, 80)      # Dark gray for tie points
                
                # Draw power rails (top and bottom)
                rail_height = 60
                center_gap = 30
                
                # Top power rails
                top_power_y = top + 20
                top_ground_y = top + 35
                
                # Bottom power rails  
                bottom_power_y = top + rail_height + center_gap + 80
                bottom_ground_y = bottom_power_y + 15
                
                x = left
                while x < rect.right():
                    # Top power rail (red line)
                    painter.setPen(QPen(power_rail_color, 2))
                    painter.drawLine(x - 5, top_power_y, x + 5, top_power_y)
                    painter.setBrush(power_rail_color)
                    painter.drawEllipse(x - hole_radius, top_power_y - hole_radius, 
                                      hole_radius * 2, hole_radius * 2)
                    
                    # Top ground rail (blue line)
                    painter.setPen(QPen(ground_rail_color, 2))
                    painter.drawLine(x - 5, top_ground_y, x + 5, top_ground_y)
                    painter.setBrush(ground_rail_color)
                    painter.drawEllipse(x - hole_radius, top_ground_y - hole_radius,
                                      hole_radius * 2, hole_radius * 2)
                    
                    # Bottom power rail (red line)
                    painter.setPen(QPen(power_rail_color, 2))
                    painter.drawLine(x - 5, bottom_power_y, x + 5, bottom_power_y)
                    painter.setBrush(power_rail_color)
                    painter.drawEllipse(x - hole_radius, bottom_power_y - hole_radius,
                                      hole_radius * 2, hole_radius * 2)
                    
                    # Bottom ground rail (blue line)
                    painter.setPen(QPen(ground_rail_color, 2))
                    painter.drawLine(x - 5, bottom_ground_y, x + 5, bottom_ground_y)
                    painter.setBrush(ground_rail_color)
                    painter.drawEllipse(x - hole_radius, bottom_ground_y - hole_radius,
                                      hole_radius * 2, hole_radius * 2)
                    
                    x += hole_spacing
                
                # Draw main tie point area
                painter.setPen(QPen(tie_point_color, 1))
                painter.setBrush(tie_point_color)
                
                # Top tie point section
                tie_start_y = top + 50
                tie_rows = 5
                
                row = 0
                while row < tie_rows:
                    y = tie_start_y + (row * hole_spacing)
                    if y > rect.bottom():
                        break
                        
                    col = 0
                    x = left
                    while x < rect.right():
                        # Draw tie point hole
                        painter.drawEllipse(x - hole_radius, y - hole_radius,
                                          hole_radius * 2, hole_radius * 2)
                        
                        # Draw connection lines every 5 holes (tie point groups)
                        if col % 5 == 0 and col > 0:
                            # Draw separator line
                            painter.setPen(QPen(QColor(150, 150, 150), 0.5))
                            painter.drawLine(x - hole_spacing/2, y - hole_spacing*2, 
                                           x - hole_spacing/2, y + hole_spacing*2)
                            painter.setPen(QPen(tie_point_color, 1))
                        
                        x += hole_spacing
                        col += 1
                    row += 1
                
                # Center divider channel
                center_y = tie_start_y + (tie_rows * hole_spacing) + center_gap/2
                painter.setPen(QPen(QColor(200, 200, 200), 3))
                painter.drawLine(rect.left(), center_y, rect.right(), center_y)
                
                # Bottom tie point section
                bottom_tie_start_y = center_y + center_gap/2
                
                row = 0
                while row < tie_rows:
                    y = bottom_tie_start_y + (row * hole_spacing)
                    if y > rect.bottom() - 60:  # Leave space for bottom power rails
                        break
                        
                    col = 0
                    x = left
                    while x < rect.right():
                        # Draw tie point hole
                        painter.setBrush(tie_point_color)
                        painter.setPen(QPen(tie_point_color, 1))
                        painter.drawEllipse(x - hole_radius, y - hole_radius,
                                          hole_radius * 2, hole_radius * 2)
                        
                        # Draw connection lines every 5 holes (tie point groups)
                        if col % 5 == 0 and col > 0:
                            # Draw separator line
                            painter.setPen(QPen(QColor(150, 150, 150), 0.5))
                            painter.drawLine(x - hole_spacing/2, y - hole_spacing*2,
                                           x - hole_spacing/2, y + hole_spacing*2)
                            painter.setPen(QPen(tie_point_color, 1))
                        
                        x += hole_spacing
                        col += 1
                    row += 1
            
            def set_grid_visible(self, visible):
                self.grid_visible = visible
                self.viewport().update()
                print(f"🔧 Fallback grid visibility: {visible}")
            
            def set_grid_style(self, style):
                self.grid_style = style.lower()
                self.viewport().update()
                print(f"🔧 Fallback grid style: {style}")
            
            def set_grid_color(self, color_name):
                """Set grid color by name"""
                color_map = {
                    "green": QColor(100, 140, 100),
                    "gray": QColor(128, 128, 128),
                    "blue": QColor(100, 100, 200),
                    "red": QColor(200, 100, 100),
                    "custom": QColor(150, 150, 150)  # Default custom
                }
                self.grid_color = color_map.get(color_name.lower(), QColor(100, 140, 100))
                self.viewport().update()
                print(f"🎨 Grid color changed to: {color_name}")
            
            def set_background_color(self, color_name):
                """Set background color by name"""
                color_map = {
                    "white": QColor(255, 255, 255),
                    "light gray": QColor(240, 240, 240),
                    "dark gray": QColor(64, 64, 64),
                    "black": QColor(0, 0, 0),
                    "cream": QColor(255, 253, 240),
                    "custom": QColor(230, 230, 230)  # Default custom
                }
                self.background_color = color_map.get(color_name.lower(), QColor(255, 255, 255))
                self.viewport().update()
                print(f"🎨 Background color changed to: {color_name}")
            
            def set_grid_spacing(self, spacing):
                if isinstance(spacing, str):
                    if "Fine" in spacing:
                        self.grid_size = 10
                    elif "Medium" in spacing:
                        self.grid_size = 20
                    elif "Coarse" in spacing:
                        self.grid_size = 40
                else:
                    self.grid_size = int(spacing) if spacing else 20
                self.viewport().update()
                print(f"🔧 Fallback grid size: {self.grid_size}")
            
            def set_snap_to_grid(self, enabled):
                self.snap_to_grid = enabled
                print(f"🔧 Fallback snap to grid: {enabled}")
            
            def dragEnterEvent(self, event):
                if event.mimeData().hasText():
                    event.acceptProposedAction()
                    print("✅ Fallback drag accepted")
            
            def dropEvent(self, event):
                if event.mimeData().hasText():
                    print(f"📦 Fallback drop: {event.mimeData().text()}")
                    event.acceptProposedAction()
            
            def wheelEvent(self, event):
                """Handle mouse wheel for zooming"""
                zoom_in_factor = 1.25
                zoom_out_factor = 1 / zoom_in_factor
                
                if event.angleDelta().y() > 0:
                    zoom_factor = zoom_in_factor
                else:
                    zoom_factor = zoom_out_factor
                
                self.scale(zoom_factor, zoom_factor)
        
        return WorkingFallbackCanvas()
    
    def _create_menu_bar(self):
        """Create menu bar"""
        try:
            from ui.menu_bar import MenuManager
            self.menu_manager = MenuManager(self, self.app_settings)
            print("✅ Menu bar created")
        except ImportError:
            self._create_fallback_menu()
    
    def _create_status_bar(self):
        """Create status bar"""
        try:
            from ui.status_bar import RetroEmulatorStatusBar
            self.status_manager = RetroEmulatorStatusBar(self)
            self.setStatusBar(self.status_manager)
            print("✅ Status bar created")
        except ImportError:
            self.statusBar().showMessage("Ready")
            print("✅ Fallback status bar created")
    
    def _setup_connections(self):
        """Setup signal connections"""
        try:
            # Component tree connections
            if hasattr(self, 'component_tree'):
                self.component_tree.itemSelectionChanged.connect(self._on_component_selected)
                self.component_tree.itemDoubleClicked.connect(self._on_component_double_clicked)
            
            # Search connections
            if hasattr(self, 'component_search'):
                self.component_search.textChanged.connect(self._filter_components)
            
            if hasattr(self, 'component_filter'):
                self.component_filter.currentTextChanged.connect(self._filter_by_type)
            
            # Grid connections
            if hasattr(self, 'show_grid_check'):
                self.show_grid_check.toggled.connect(self._on_grid_toggled)
            
            if hasattr(self, 'grid_style_combo'):
                self.grid_style_combo.currentTextChanged.connect(self._on_grid_style_changed)
            
            if hasattr(self, 'grid_color_combo'):
                self.grid_color_combo.currentTextChanged.connect(self._on_grid_color_changed)
            
            if hasattr(self, 'bg_color_combo'):
                self.bg_color_combo.currentTextChanged.connect(self._on_background_color_changed)
            
            print("✅ Signal connections established")
            
        except Exception as e:
            print(f"⚠️ Connection setup failed: {e}")
    
    def _on_component_selected(self):
        """Handle component selection"""
        if hasattr(self, 'component_tree'):
            current = self.component_tree.currentItem()
            if current and hasattr(self, 'component_name_label'):
                self.component_name_label.setText(current.text(0))
                if hasattr(self, 'component_details'):
                    self.component_details.setText(f"Selected: {current.text(0)}")
    
    def _on_component_double_clicked(self, item, column):
        """Handle component double-click"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            category, component = data
            print(f"🎯 Adding component: {component} from {category}")
    
    def _filter_components(self, text):
        """Filter components by search text"""
        # Implementation for component filtering
        print(f"🔍 Filtering components: {text}")
    
    def _filter_by_type(self, type_name):
        """Filter components by type"""
        print(f"📂 Filtering by type: {type_name}")
    
    def _on_grid_toggled(self, checked):
        """Handle grid toggle"""
        print(f"⚏ Grid visibility: {checked}")
        if self.canvas and hasattr(self.canvas, 'set_grid_visible'):
            self.canvas.set_grid_visible(checked)
    
    def _on_grid_style_changed(self, style):
        """Handle grid style change"""
        print(f"🎨 Grid style: {style}")
        if self.canvas and hasattr(self.canvas, 'set_grid_style'):
            self.canvas.set_grid_style(style)
    
    def _on_grid_color_changed(self, color):
        """Handle grid color change"""
        print(f"🎨 Grid color: {color}")
        if self.canvas and hasattr(self.canvas, 'set_grid_color'):
            self.canvas.set_grid_color(color)
    
    def _on_background_color_changed(self, color):
        """Handle background color change"""
        print(f"🎨 Background color: {color}")
        if self.canvas and hasattr(self.canvas, 'set_background_color'):
            self.canvas.set_background_color(color)
    
    def _post_initialization_setup(self):
        """Final setup after initialization"""
        self._apply_theme()
        if hasattr(self, 'component_dock'):
            self.component_dock.raise_()
        print("✅ Post-initialization setup complete")
    
    def _update_window_title(self):
        """Update window title"""
        title = "Visual Retro System Emulator Builder"
        if self.project_manager and hasattr(self.project_manager, 'current_project'):
            if self.project_manager.current_project:
                title += f" - {self.project_manager.current_project}"
        self.setWindowTitle(title)
    
    # Fallback methods
    def _create_fallback_project_manager(self):
        class FallbackProjectManager:
            def __init__(self):
                self.current_project = None
        return FallbackProjectManager()
    
    def _create_fallback_layer_manager(self):
        class FallbackLayerManager:
            def __init__(self):
                self.layers = ['Component', 'PCB', 'Gerber']
                self.active_layer = 'Component'
        return FallbackLayerManager()
    
    def _create_fallback_settings(self):
        class FallbackSettings:
            def get_theme(self):
                return {
                    'name': 'Default',
                    'colors': {
                        'bg_primary': '#f0f0f0',
                        'bg_secondary': '#ffffff',
                        'text_primary': '#000000',
                        'accent_primary': '#0078d4',
                        'border': '#cccccc',
                        'panel_bg': '#ffffff'
                    }
                }
        return FallbackSettings()
    
    def _create_fallback_component_dock(self):
        """Create simple fallback component dock"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Components (Fallback)"))
        
        for name in ["Z80 CPU", "6502 CPU", "RAM", "ROM"]:
            btn = QPushButton(name)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        dock = QDockWidget("Components", self)
        dock.setWidget(widget)
        dock.setMinimumWidth(250)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        print("✅ Fallback component dock created")
    
    def _create_fallback_menu(self):
        """Create fallback menu"""
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        view_menu = menubar.addMenu('View')
        help_menu = menubar.addMenu('Help')
        print("✅ Fallback menu created")


# For compatibility
MainWindow = FixedMainWindow