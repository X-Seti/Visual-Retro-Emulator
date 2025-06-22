
#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Main Window Implementation
"""
#this belongs in ui/ main_window.py

import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                           QDockWidget, QTreeWidget, QTreeWidgetItem, QSplitter,
                           QMessageBox, QFileDialog, QLabel, QStatusBar, QPushButton,
                           QMenu, QMenuBar, QApplication, QFrame, QCheckBox, QComboBox,
                           QGraphicsView, QGraphicsScene, QToolBar, QSlider, QSpinBox,
                           QGroupBox, QGridLayout, QFormLayout, QTextEdit, QTabWidget,
                           QProgressBar, QToolButton, QButtonGroup, QRadioButton,
                           QLineEdit, QDoubleSpinBox, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize, QRect, QRectF
from PyQt6.QtGui import QShortcut, QKeySequence, QAction, QIcon, QFont, QPixmap, QPainter, QColor, QBrush, QPen
from .canvas_chip_integration import ChipCanvasItem, CanvasChipIntegration

"""
from .canvas_chip_integration import ChipCanvasItem, CanvasChipIntegration
"""

# ADD THESE METHODS TO YOUR MAINWINDOW CLASS:

class MainWindow(QMainWindow):
    """Complete main window with ALL functionality - RESTORED TO ORIGINAL SIZE"""

    # Signals
    component_selected = pyqtSignal(object)
    project_modified = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Retro System Emulator Builder")
        self.resize(1600, 1000)

        # Initialize component references
        self.component_manager = None
        self.project_manager = None
        self.simulation_engine = None
        self.layer_manager = None

        # UI components
        self.canvas = None
        self.component_palette = None
        self.cad_tools_panel = None
        self.layer_controls = None
        self.menu_manager = None
        self.status_manager = None
        self.property_editor = None

        # Project state
        self.current_project_path = None
        self.is_modified = False

        # Tool states
        self.current_tool = "select"
        self.tool_settings = {}

        # Status bar components
        self.status_bar = None
        self.coordinate_label = None
        self.zoom_label = None
        self.tool_label = None
        self.component_count_label = None
        self.connection_count_label = None
        self.cad_item_count_label = None

        # Dock widgets
        self.component_palette_dock = None
        self.cad_tools_dock = None
        self.properties_dock = None
        self.layer_controls_dock = None

        # Apply theme - use global theme manager.
        #self._apply_dark_theme()

        # Initialize everything
        self._initialize_managers()
        self._create_ui()
        self._create_docks()
        self._create_menu_bar()
        self._create_status_bar()
        self._create_toolbars()
        self._setup_connections()
        self._setup_hotkeys()
        self._post_init_setup()

        # Update display
        self._update_window_title()
        self._update_status_counts()

        print("✅ Complete Main Window initialized - FULL SIZE RESTORED")

    #Keep
    def _initialize_managers(self):
        """Initialize all manager components"""
        print("Initializing managers...")

        # Initialize Layer Manager
        from managers.layer_manager import LayerManager
        self.layer_manager = LayerManager()
        print("✓ Layer Manager initialized")

        # Initialize Component Manager
        from core.components import ComponentManager
        self.component_manager = ComponentManager()
        print("✓ Component Manager initialized")

        # Initialize Project Manager
        from managers.project_manager import ProjectManager
        self.project_manager = ProjectManager()
        print("✓ Project Manager initialized")

        # Initialize Simulation Engine
        from core.simulation import SimulationEngine
        self.simulation_engine = SimulationEngine()
        print("✓ Simulation Engine initialized")

    def _create_canvas(self):
        """Create main canvas"""
        self.canvas = self._create_canvasarea()

    def _create_canvasarea(self): #Weird SEGV (Address boundary error) _create_canvas
        from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
        from PyQt6.QtCore import QRectF
        from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont

        class Canvas_DoodleArea(QGraphicsView):
            def __init__(self):
                super().__init__()
                self.setScene(QGraphicsScene())
                self.scene().setSceneRect(-2000, -2000, 4000, 4000)

                # Grid settings
                self.grid_visible = True
                self.grid_size = 20
                self.grid_style = "dots"
                self.grid_color = QColor(100, 140, 100, 120)
                self.snap_to_grid = True
                self.components = {} #needs looking at.
                self.connections = [] #unused

                # Enable drag & drop - these need to be checked.
                self.setAcceptDrops(True)
                self.setBackgroundBrush(QBrush(QColor(40, 40, 50)))  # Dark blue-gray background

                # Set viewport update mode for better grid rendering
                self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

                # Add welcome message
                #self._add_welcome_message()

                print("✓ Canvas created with drag/drop support")
                print(f"✓ Grid visible: {self.grid_visible}, Grid size: {self.grid_size}")

                # Force initial grid draw
                self.viewport().update()

            def drawBackground(self, painter, rect):
                super().drawBackground(painter, rect)
                if self.grid_visible:
                    self._draw_grid(painter, rect)

            def _draw_grid(self, painter, rect):
                """Draw grid lines - FIXED for PyQt6"""
                painter.save()

                # Use brighter grid color for visibility
                grid_pen = QPen(QColor(100, 140, 100, 150), 1)
                painter.setPen(grid_pen)

                left = int(rect.left()) - (int(rect.left()) % self.grid_size)
                top = int(rect.top()) - (int(rect.top()) % self.grid_size)

                x = left
                while x < rect.right():
                    painter.drawLine(int(x), int(rect.top()), int(x), int(rect.bottom()))
                    x += self.grid_size

                y = top
                while y < rect.bottom():
                    painter.drawLine(int(rect.left()), int(y), int(rect.right()), int(y))
                    y += self.grid_size

                painter.restore()
                print(f"🔲 Grid drawn at size {self.grid_size}")

            def dragEnterEvent(self, event):
                """Handle drag enter"""
                if event.mimeData().hasText():
                    text = event.mimeData().text()
                    print(f"🔍 Checking drag data: '{text}'")
                    # Accept multiple formats
                    if (text.startswith("component:") or
                        text.startswith("Memory:") or
                        text.startswith("CPUs:") or
                        ":" in text):
                        event.acceptProposedAction()
                        print(f"✅ Drag accepted: {text}")
                    else:
                        print(f"❌ Drag rejected: {text}")
                        event.ignore()
                else:
                    print("❌ No text in drag data")
                    event.ignore()

            def dragMoveEvent(self, event):
                """Handle drag move"""
                if event.mimeData().hasText():
                    event.acceptProposedAction()

            def dropEvent(self, event):
                """Handle component drop"""
                if event.mimeData().hasText():
                    component_data = event.mimeData().text()
                    print(f"📦 Drop data received: '{component_data}'")

                    try:
                        # Handle multiple drag formats
                        if component_data.startswith("component:"):
                            # Format: "component:category:name:package"
                            parts = component_data.split(":", 3)
                            if len(parts) >= 3:
                                category = parts[1]
                                name = parts[2]
                                package = parts[3] if len(parts) > 3 else "DIP-40"
                        elif ":" in component_data:
                            # Format: "category:name" or other formats
                            parts = component_data.split(":", 2)
                            category = parts[0] if len(parts) > 0 else "Unknown"
                            name = parts[1] if len(parts) > 1 else "Component"
                            package = parts[2] if len(parts) > 2 else "DIP-40"
                        else:
                            # Single name
                            category = "Unknown"
                            name = component_data
                            package = "DIP-40"

                        # Get drop position
                        scene_pos = self.mapToScene(event.position().toPoint())

                        # Snap to grid
                        if self.snap_to_grid:
                            scene_pos.setX(round(scene_pos.x() / self.grid_size) * self.grid_size)
                            scene_pos.setY(round(scene_pos.y() / self.grid_size) * self.grid_size)

                        # Create visual component
                        self._create_component(name, category, package, scene_pos)

                        event.acceptProposedAction()
                        print(f"🎯 Component dropped: {name} from {category}")

                    except Exception as e:
                        print(f"❌ Error handling drop: {e}")
                        event.ignore()
                else:
                    event.ignore()

            def _create_component(self, name, category, package, position):
                """Create a visual component on the canvas"""
                try:
                    # Create component rectangle
                    if package.startswith("DIP"):
                        width = 60
                        height = 120
                    elif package.startswith("QFP"):
                        width = 80
                        height = 80
                    else:
                        width = 70
                        height = 100

                    # Create component visual
                    rect_item = QGraphicsRectItem(-width/2, -height/2, width, height)
                    rect_item.setBrush(QBrush(QColor(60, 60, 80)))
                    rect_item.setPen(QPen(QColor(150, 150, 150), 2))
                    rect_item.setPos(position)

                    # Add component label
                    text_item = QGraphicsTextItem(f"{name}\n{package}")
                    text_item.setDefaultTextColor(QColor(255, 255, 255))
                    text_item.setFont(QFont("Arial", 8))
                    text_item.setPos(position.x() - width/2 + 5, position.y() - height/2 + 5)

                    # Add to scene
                    self.scene().addItem(rect_item)
                    self.scene().addItem(text_item)

                    # Track component
                    comp_id = f"{name}_{len(self.components)}"
                    self.components[comp_id] = {
                        'rect': rect_item,
                        'text': text_item,
                        'name': name,
                        'category': category,
                        'package': package,
                        'position': position
                    }

                    print(f"✅ Component created: {name} ({package})")
                    return comp_id

                except Exception as e:
                    print(f"❌ Error creating component: {e}")
                    return None

            # Canvas control methods
            def set_grid_visible(self, visible):
                self.grid_visible = visible
                self.viewport().update()
                print(f"🔧 Grid visible: {visible}")

            def set_grid_size(self, size):
                self.grid_size = size
                self.viewport().update()
                print(f"🔧 Grid size: {size}")

            def set_snap_to_grid(self, enabled):
                self.snap_to_grid = enabled
                print(f"🔧 Snap to grid: {enabled}")

            def zoom_fit(self):
                self.fitInView(self.scene().itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
                print("🔍 Zoom fit")

            def zoom_in(self):
                self.scale(1.25, 1.25)
                print("🔍+ Zoom in")

            def zoom_out(self):
                self.scale(0.8, 0.8)
                print("🔍- Zoom out")

            def clear(self):
                self.scene().clear()
                self.components.clear()
                #self._add_welcome_message()
                print("🧹 Canvas cleared")

        return Canvas_DoodleArea()
        """Create layer manager"""
        class LayerManager:
            def __init__(self):
                self.layers = ["Top Layer", "Bottom Layer", "Silkscreen", "Solder Mask"]
                self.active_layer = "Top Layer"
                self.layer_visibility = {layer: True for layer in self.layers}

            def get_layers(self):
                return self.layers

            def set_active_layer(self, layer):
                self.active_layer = layer

            def get_active_layer(self):
                return self.active_layer

            def toggle_layer_visibility(self, layer):
                if layer in self.layer_visibility:
                    self.layer_visibility[layer] = not self.layer_visibility[layer]

        return LayerManager()



    def _create_ui(self):
        """Create main user interface"""
        print("Creating main UI...")

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panels
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)

        self._create_canvas()
        main_splitter.addWidget(self.canvas)

        # Set splitter sizes
        main_splitter.setSizes([1200, 400])

        print("✓ Main UI created")


    def _create_docks(self):
        """Create dock widgets"""
        print("Creating dock widgets...")

        # Component Palette Dock (single working one)
        self._create_component_palette_dock()

        # CAD Tools Dock
        self._create_cad_tools_dock()

        # Properties Dock
        self._create_properties_dock()

        # Layer Controls Dock
        self._create_layer_controls_dock()

        print("✓ Dock widgets created")


    def _create_component_palette_dock_with_chips(self):
        """Create component palette dock with realistic chip integration"""
        from .component_palette import ComponentPalette

        # Create the component palette
        self.component_palette = ComponentPalette()

        # Connect signals for chip integration
        self.component_palette.component_selected.connect(self._on_component_selected)
        self.component_palette.component_double_clicked.connect(self._on_component_add_to_canvas)

        # Create dock widget
        palette_dock = QDockWidget("Component Library", self)
        palette_dock.setWidget(self.component_palette)
        palette_dock.setMinimumWidth(300)
        palette_dock.setMaximumWidth(400)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, palette_dock)

        print("✅ Component palette with realistic chips loaded")
        print(f"📦 Total components available: {self.component_palette.get_total_components()}")

    def _on_component_selected(self, component_id: str, component_data: dict):
        """Handle component selection from palette"""
        print(f"🔍 Selected component: {component_data.get('name', 'Unknown')}")

        # Update properties panel if available
        if hasattr(self, 'properties_panel') and self.properties_panel:
            # Create a mock object with the component data for properties panel
            mock_component = type('Component', (), component_data)()
            mock_component.component_name = component_data.get('name', 'Unknown')
            mock_component.component_type = component_data.get('category', 'Unknown')
            mock_component.package_type = component_data.get('package_type', 'DIP-40')

            # Add position methods
            from PyQt6.QtCore import QPointF
            mock_component.pos = lambda: QPointF(0, 0)
            mock_component.setPos = lambda x, y: None

            self.properties_panel.setObject(mock_component)

    def _on_component_add_to_canvas(self, component_id: str, component_data: dict):
        """Add component to canvas with realistic chip image"""
        if not self.canvas or not hasattr(self.canvas, 'scene'):
            print("❌ Canvas not available")
            return

        try:
            # Use the canvas integration to add the chip
            chip_item = CanvasChipIntegration.add_component_to_canvas(
                self.canvas,
                component_data
            )

            # Connect chip signals to main window
            chip_item.selectionChanged.connect(self._on_chip_selection_changed)
            chip_item.propertyChanged.connect(self._on_chip_property_changed)

            # Update status
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage(f"Added {component_data['name']} to canvas", 3000)

            # Mark project as modified
            self.is_modified = True
            self._update_window_title()
            self._update_status_counts()

            print(f"✅ Successfully added {component_data['name']} to canvas")

        except Exception as e:
            print(f"❌ Error adding component to canvas: {e}")
            import traceback
            traceback.print_exc()

    def _on_chip_selection_changed(self, selected: bool):
        """Handle chip selection change on canvas"""
        if selected:
            # Get the selected chip item
            selected_items = self.canvas.scene().selectedItems()
            if selected_items and isinstance(selected_items[0], ChipCanvasItem):
                chip_item = selected_items[0]

                # Update properties panel
                if hasattr(self, 'properties_panel') and self.properties_panel:
                    self.properties_panel.setObject(chip_item)

                print(f"🎯 Selected chip on canvas: {chip_item.component_name}")

    def _on_chip_property_changed(self, property_name: str, value):
        """Handle chip property change"""
        print(f"🔧 Chip property changed: {property_name} = {value}")

        # Mark project as modified
        self.is_modified = True
        self._update_window_title()

    def replace_rectangular_components_with_chips(self):
        """Replace any existing rectangular components with realistic chips"""
        if self.canvas and hasattr(self.canvas, 'scene'):
            CanvasChipIntegration.replace_rectangles_with_chips(self.canvas)

    # CANVAS DROP EVENT INTEGRATION:
    def setup_canvas_drop_handling(self):
        """Setup canvas to handle component drops with realistic chips"""
        if not self.canvas:
            return

        # Enable drops on canvas
        self.canvas.setAcceptDrops(True)

        # Override the canvas dragEnterEvent if needed
        original_drag_enter = getattr(self.canvas, 'dragEnterEvent', None)

        def enhanced_drag_enter_event(event):
            """Enhanced drag enter event for canvas"""
            if event.mimeData().hasText():
                # Check if it's a component drag
                text = event.mimeData().text()
                if text.startswith('component:'):
                    event.acceptProposedAction()
                    return

            # Call original handler if it exists
            if original_drag_enter:
                original_drag_enter(event)

        def enhanced_drop_event(event):
            """Enhanced drop event for canvas"""
            if event.mimeData().hasText():
                text = event.mimeData().text()
                if text.startswith('component:'):
                    try:
                        # Parse component info from drag data
                        parts = text.split(':')
                        if len(parts) >= 3:
                            category = parts[1]
                            component_name = parts[2]

                            # Find component in palette
                            if hasattr(self, 'component_palette'):
                                component = self.component_palette.get_component_by_id(component_name)
                                if component:
                                    # Get drop position
                                    drop_pos = self.canvas.mapToScene(event.position().toPoint())

                                    # Add component at drop position
                                    chip_item = CanvasChipIntegration.add_component_to_canvas(
                                        self.canvas,
                                        component,
                                        drop_pos
                                    )

                                    # Connect signals
                                    chip_item.selectionChanged.connect(self._on_chip_selection_changed)
                                    chip_item.propertyChanged.connect(self._on_chip_property_changed)

                                    event.acceptProposedAction()
                                    print(f"📍 Dropped {component_name} at {drop_pos}")
                                    return

                    except Exception as e:
                        print(f"❌ Error handling drop: {e}")

            event.ignore()

        # Set the enhanced event handlers
        self.canvas.dragEnterEvent = enhanced_drag_enter_event
        self.canvas.dropEvent = enhanced_drop_event

        print("✅ Canvas drop handling setup for realistic chips")

    # INTEGRATION INITIALIZATION:
    def initialize_chip_integration(self):
        """Initialize the complete chip integration system"""
        print("🔗 Initializing chip integration...")

        # Setup component palette with chips
        self._create_component_palette_dock_with_chips()

        # Setup canvas drop handling
        self.setup_canvas_drop_handling()

        # Replace any existing rectangular components
        self.replace_rectangular_components_with_chips()

        print("✅ Chip integration initialized!")
        print("🎉 Your Visual Retro Emulator now has realistic chip graphics!")


    def _create_cad_tools_dock(self):
        """Create the single working CAD tools with scroll support"""
        # Create scrollable content widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        tools_widget = QWidget()
        layout = QVBoxLayout(tools_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # Title removed, we don't need Cad shown twice

        # Tool buttons group
        tools_group = QGroupBox("Tools")
        tools_layout = QVBoxLayout(tools_group)
        tool_group = QButtonGroup()

        tools = [
            ("Select", "S", "select"),
            ("Place Component", "P", "place"),
            ("Draw Wire", "W", "wire"),
            ("Draw Trace", "T", "trace"),
            ("Add Via", "V", "via"),
            ("Add Pad", "A", "pad"),
            ("Measure", "M", "measure"),
            ("Delete", "Del", "delete")
        ]

        for tool_name, shortcut, tool_id in tools:
            btn = QPushButton(f"{tool_name} ({shortcut})")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, t=tool_id: self._set_tool(t))
            tool_group.addButton(btn)
            tools_layout.addWidget(btn)

            if tool_id == "select":
                btn.setChecked(True)

        layout.addWidget(tools_group)

        # Grid settings group - keep this section
        grid_group = QGroupBox("Grid Settings")
        grid_layout = QFormLayout(grid_group)

        grid_check = QCheckBox("Show Grid")
        grid_check.setChecked(True)
        grid_check.toggled.connect(self._on_grid_visibility_changed)
        grid_layout.addRow(grid_check)

        snap_check = QCheckBox("Snap to Grid")
        snap_check.setChecked(True)
        snap_check.toggled.connect(self._on_snap_to_grid_changed)
        grid_layout.addRow(snap_check)

        grid_size_spin = QSpinBox()
        grid_size_spin.setRange(5, 100)
        grid_size_spin.setValue(20)
        grid_size_spin.setSuffix(" px")
        grid_size_spin.valueChanged.connect(self._on_grid_size_changed)
        grid_layout.addRow("Size:", grid_size_spin)

        layout.addWidget(grid_group)

        # Presets group
        presets_group = QGroupBox("Grid Presets")
        presets_layout = QVBoxLayout(presets_group)

        preset_buttons = [
            ("Fine (5px)", "fine"),
            ("Standard (10px)", "standard"),
            ("Prototype (20px)", "prototype"),
            ("Breadboard (25px)", "breadboard")
        ]

        for preset_name, preset_id in preset_buttons:
            btn = QPushButton(preset_name)
            btn.clicked.connect(lambda checked, p=preset_id: self._apply_grid_preset(p))
            presets_layout.addWidget(btn)

        layout.addWidget(presets_group)

        layout.addStretch()

        # Set scrollable content
        scroll_area.setWidget(tools_widget)

        self.cad_tools_dock = QDockWidget("CAD Tools", self)
        self.cad_tools_dock.setWidget(scroll_area)
        self.cad_tools_dock.setMinimumWidth(200)
        self.cad_tools_dock.setMaximumWidth(280)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.cad_tools_dock)

        print("✅ Working CAD tools created with scroll support")


    def _create_properties_dock(self):
        """Create the single working properties panel with scroll support"""
        # Create scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        props_widget = QWidget()
        layout = QVBoxLayout(props_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # Title removed - we don't need the name twice.

        # No selection message
        self.no_selection_label = QLabel("No component selected\n\nClick on a component to view its properties")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_selection_label.setStyleSheet("color: #888; font-style: italic; padding: 20px;")
        layout.addWidget(self.no_selection_label)

        # Component properties (will be shown when component is selected)
        self.properties_form = QWidget()
        self.properties_form.setVisible(False)

        # Component info group
        component_group = QGroupBox("Component")
        comp_layout = QFormLayout(component_group)

        self.name_edit = QLineEdit()
        comp_layout.addRow("Name:", self.name_edit)

        self.type_edit = QLineEdit()
        self.type_edit.setReadOnly(True)
        comp_layout.addRow("Type:", self.type_edit)

        self.package_edit = QLineEdit()
        comp_layout.addRow("Package:", self.package_edit)

        layout.addWidget(component_group)

        # Position group
        position_group = QGroupBox("Position")
        pos_layout = QFormLayout(position_group)

        self.x_spin = QSpinBox()
        self.x_spin.setRange(-10000, 10000)
        self.x_spin.setSuffix(" px")
        pos_layout.addRow("X:", self.x_spin)

        self.y_spin = QSpinBox()
        self.y_spin.setRange(-10000, 10000)
        self.y_spin.setSuffix(" px")
        pos_layout.addRow("Y:", self.y_spin)

        self.rotation_spin = QSpinBox()
        self.rotation_spin.setRange(0, 360)
        self.rotation_spin.setSuffix("°")
        pos_layout.addRow("Rotation:", self.rotation_spin)

        layout.addWidget(position_group)

        # Electrical group
        electrical_group = QGroupBox("Electrical")
        elec_layout = QFormLayout(electrical_group)

        self.voltage_edit = QLineEdit()
        self.voltage_edit.setPlaceholderText("e.g., 5V")
        elec_layout.addRow("Voltage:", self.voltage_edit)

        self.frequency_edit = QLineEdit()
        self.frequency_edit.setPlaceholderText("e.g., 1MHz")
        elec_layout.addRow("Frequency:", self.frequency_edit)

        layout.addWidget(electrical_group)

        layout.addWidget(self.properties_form)
        layout.addStretch()

        # Set scrollable content
        scroll_area.setWidget(props_widget)

        self.properties_dock = QDockWidget("Properties", self)
        self.properties_dock.setWidget(scroll_area)
        self.properties_dock.setMinimumWidth(200)
        self.properties_dock.setMaximumWidth(300)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)

        print("✅ Working properties panel created with scroll support")


    def _create_layer_controls_dock(self): #ui_layer_controls.py
        """Create layer controls dock"""
        from ui.layer_controls import LayerControls
        self.layer_controls = LayerControls()
        layer_dock = QDockWidget("Layers", self)
        layer_dock.setWidget(self.layer_controls)
        layer_dock.setMinimumWidth(180)
        layer_dock.setMaximumWidth(250)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layer_dock)
        print("✓ Layer controls dock created")

    def _create_menu_bar(self): #ui_menu_bar.py
        from ui.menu_bar import RetroEmulatorMenuBar
        self.menu_manager = RetroEmulatorMenuBar(self)
        self.setMenuBar(self.menu_manager)
        print("✓ Menu bar created")

    def _create_status_bar(self): #ui_status_bar.py
        """Create status bar"""
        from ui.status_bar import StatusBarManager
        self.status_manager = StatusBarManager(self)
        print("✓ Status bar created")

    def _create_toolbars(self):
        """Create toolbars"""
        print("Creating toolbars...")

        # Main toolbar
        main_toolbar = self.addToolBar("Main")
        main_toolbar.setObjectName("MainToolbar")
        main_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # File actions
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_project)
        main_toolbar.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_project)
        main_toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_project)
        main_toolbar.addAction(save_action)

        main_toolbar.addSeparator()

        # Edit actions
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._undo)
        main_toolbar.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._redo)
        main_toolbar.addAction(redo_action)

        main_toolbar.addSeparator()

        # View actions
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut('Ctrl++')
        zoom_in_action.triggered.connect(self._zoom_in)
        main_toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut('Ctrl+-')
        zoom_out_action.triggered.connect(self._zoom_out)
        main_toolbar.addAction(zoom_out_action)

        zoom_fit_action = QAction("Zoom Fit", self)
        zoom_fit_action.setShortcut('Ctrl+0')
        zoom_fit_action.triggered.connect(self._zoom_fit)
        main_toolbar.addAction(zoom_fit_action)

        main_toolbar.addSeparator()

        # Simulation actions
        start_sim_action = QAction("Start", self)
        start_sim_action.setShortcut('F5')
        start_sim_action.triggered.connect(self._start_simulation)
        main_toolbar.addAction(start_sim_action)

        stop_sim_action = QAction("Stop", self)
        stop_sim_action.setShortcut('Shift+F5')
        stop_sim_action.triggered.connect(self._stop_simulation)
        main_toolbar.addAction(stop_sim_action)

        # Tools toolbar
        tools_toolbar = self.addToolBar("Tools")
        tools_toolbar.setObjectName("ToolsToolbar")
        tools_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        # Tool buttons
        tool_group = QButtonGroup()

        select_tool_btn = QToolButton()
        select_tool_btn.setText("Select")
        select_tool_btn.setCheckable(True)
        select_tool_btn.setChecked(True)
        select_tool_btn.clicked.connect(lambda: self._set_tool('select'))
        tool_group.addButton(select_tool_btn)
        tools_toolbar.addWidget(select_tool_btn)

        place_tool_btn = QToolButton()
        place_tool_btn.setText("Place")
        place_tool_btn.setCheckable(True)
        place_tool_btn.clicked.connect(lambda: self._set_tool('place'))
        tool_group.addButton(place_tool_btn)
        tools_toolbar.addWidget(place_tool_btn)

        wire_tool_btn = QToolButton()
        wire_tool_btn.setText("Wire")
        wire_tool_btn.setCheckable(True)
        wire_tool_btn.clicked.connect(lambda: self._set_tool('wire'))
        tool_group.addButton(wire_tool_btn)
        tools_toolbar.addWidget(wire_tool_btn)

        trace_tool_btn = QToolButton()
        trace_tool_btn.setText("Trace")
        trace_tool_btn.setCheckable(True)
        trace_tool_btn.clicked.connect(lambda: self._set_tool('trace'))
        tool_group.addButton(trace_tool_btn)
        tools_toolbar.addWidget(trace_tool_btn)

        via_tool_btn = QToolButton()
        via_tool_btn.setText("Via")
        via_tool_btn.setCheckable(True)
        via_tool_btn.clicked.connect(lambda: self._set_tool('via'))
        tool_group.addButton(via_tool_btn)
        tools_toolbar.addWidget(via_tool_btn)

        pad_tool_btn = QToolButton()
        pad_tool_btn.setText("Pad")
        pad_tool_btn.setCheckable(True)
        pad_tool_btn.clicked.connect(lambda: self._set_tool('pad'))
        tool_group.addButton(pad_tool_btn)
        tools_toolbar.addWidget(pad_tool_btn)

        measure_tool_btn = QToolButton()
        measure_tool_btn.setText("Measure")
        measure_tool_btn.setCheckable(True)
        measure_tool_btn.clicked.connect(lambda: self._set_tool('measure'))
        tool_group.addButton(measure_tool_btn)
        tools_toolbar.addWidget(measure_tool_btn)

        print("✓ Toolbars created")

    def _setup_connections(self):
        """Setup signal connections"""
        print("Setting up connections...")

        # Connect canvas signals if available
        if self.canvas and hasattr(self.canvas, 'component_selected'):
            self.canvas.component_selected.connect(self.component_selected)

        # Connect component palette signals if available
        if self.component_palette and hasattr(self.component_palette, 'component_requested'):
            self.component_palette.component_requested.connect(self._add_component)

        # Connect CAD tools signals if available
        if self.cad_tools_panel and hasattr(self.cad_tools_panel, 'tool_changed'):
            self.cad_tools_panel.tool_changed.connect(self._on_tool_changed)

        print("✓ Connections setup complete")

    def _setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        print("Setting up hotkeys...")

        # Standard shortcuts
        QShortcut(QKeySequence('Ctrl+F'), self, self._show_search_dialog)
        QShortcut(QKeySequence('Ctrl+Shift+P'), self, self._show_command_palette)
        QShortcut(QKeySequence('F1'), self, self._show_shortcuts)
        QShortcut(QKeySequence('Escape'), self, self._cancel_current_operation)

        # Tool shortcuts
        QShortcut(QKeySequence('S'), self, lambda: self._set_tool('select'))
        QShortcut(QKeySequence('P'), self, lambda: self._set_tool('place'))
        QShortcut(QKeySequence('W'), self, lambda: self._set_tool('wire'))
        QShortcut(QKeySequence('T'), self, lambda: self._set_tool('trace'))
        QShortcut(QKeySequence('V'), self, lambda: self._set_tool('via'))
        QShortcut(QKeySequence('A'), self, lambda: self._set_tool('pad'))
        QShortcut(QKeySequence('M'), self, lambda: self._set_tool('measure'))

        # View shortcuts
        QShortcut(QKeySequence('Ctrl+G'), self, self._toggle_grid)
        QShortcut(QKeySequence('Ctrl+D'), self, self._toggle_cad_tools)

        print("✓ Hotkeys setup complete")

    def _post_init_setup(self):
        """Post-initialization setup"""
        print("Post-initialization setup...")

        # Set initial focus
        if self.canvas:
            self.canvas.setFocus()

        # Load last project if available
        self._load_last_project()

        # Update initial UI state
        self._update_ui_state()

        print("✓ Post-initialization complete")


    def set_component_manager(self, manager):
        """Set component manager"""
        self.component_manager = manager
        print("✓ Component manager connected")

    def set_project_manager(self, manager):
        """Set project manager"""
        self.project_manager = manager
        print("✓ Project manager connected")

    def set_simulation_engine(self, engine):
        """Set simulation engine"""
        self.simulation_engine = engine
        print("✓ Simulation engine connected")

    # Grid system
    def _on_grid_visibility_changed(self, enabled):
        """Handle grid visibility change from CAD tools panel"""
        if self.canvas and hasattr(self.canvas, 'set_grid_visible'):
            self.canvas.set_grid_visible(enabled)
            print(f"🔍 Grid visibility changed: {enabled}")
        else:
            print(f"⚠️ Canvas doesn't support set_grid_visible")

    def _on_snap_to_grid_changed(self, enabled):
        """Handle snap to grid change from CAD tools panel"""
        if self.canvas and hasattr(self.canvas, 'set_snap_to_grid'):
            self.canvas.set_snap_to_grid(enabled)
            print(f"🧲 Snap to grid changed: {enabled}")
        else:
            print(f"⚠️ Canvas doesn't support set_snap_to_grid")

    def _on_grid_size_changed(self, size):
        """Handle grid size change from CAD tools panel"""
        if self.canvas and hasattr(self.canvas, 'set_grid_size'):
            self.canvas.set_grid_size(size)
            print(f"📏 Grid size changed: {size}")
        else:
            print(f"⚠️ Canvas doesn't support set_grid_size")

    def _apply_grid_preset(self, preset_name):
        """Apply grid preset from CAD tools panel"""
        presets = {
            'fine': 5,
            'standard': 10,
            'prototype': 20,
            'breadboard': 25,
            'large': 50
        }

        if preset_name in presets:
            size = presets[preset_name]
            if self.canvas and hasattr(self.canvas, 'set_grid_size'):
                self.canvas.set_grid_size(size)
                print(f"🎯 Applied grid preset '{preset_name}': {size}px")
            else:
                print(f"⚠️ Canvas doesn't support set_grid_size for preset")


    def _set_tool(self, tool_name):
        """Set current tool"""
        self.current_tool = tool_name

        # Update canvas tool if available
        if self.canvas and hasattr(self.canvas, 'set_tool'):
            self.canvas.set_tool(tool_name)

        # Update tool label
        if hasattr(self, 'tool_label') and self.tool_label is not None:
            self.tool_label.setText(f"Tool: {tool_name.title()}")

        # Update status
        if hasattr(self, 'status_bar') and self.status_bar is not None:
            self.status_bar.showMessage(f"Tool changed to: {tool_name.title()}", 2000)

        print(f"🔧 Tool set to: {tool_name}")

    def _on_tool_changed(self, tool_name):
        """Handle tool change from CAD panel"""
        self._set_tool(tool_name)


    def _new_project(self):
        """Create new project"""
        if self._check_unsaved_changes():
            # Clear current project
            if self.canvas and hasattr(self.canvas, 'clear'):
                self.canvas.clear()

            if self.project_manager:
                self.project_manager.new_project()

            self.current_project_path = None
            self.is_modified = False
            self._update_window_title()
            self._update_status_counts()

            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage("New project created", 2000)

            print("📁 New project created")

    def _open_project(self):
        """Open existing project"""
        if self._check_unsaved_changes():
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Project",
                "",
                "Projects (*.xset);;All Files (*)"
            )

            if file_path:
                self._load_project(file_path)

    def _save_project(self):
        """Save current project"""
        if not self.current_project_path:
            self._save_project_as()
            return

        try:
            if self.project_manager and hasattr(self.project_manager, 'save_project'):
                self.project_manager.save_project(self.current_project_path)

            self.is_modified = False
            self._update_window_title()

            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage("Project saved", 2000)

            print(f"💾 Project saved: {self.current_project_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save project:\n{e}")

    def _save_project_as(self):
        """Save project with new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "",
            "Projects (*.xset);;All Files (*)"
        )

        if file_path:
            if not file_path.endswith('.xset'):
                file_path += '.xset'
            self.current_project_path = file_path
            self._save_project()

    def _load_project(self, file_path):
        """Load project from file"""
        try:
            if self.project_manager and hasattr(self.project_manager, 'load_project'):
                self.project_manager.load_project(file_path)

            self.current_project_path = file_path
            self.is_modified = False
            self._update_window_title()
            self._update_status_counts()

            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage(f"Project loaded: {os.path.basename(file_path)}", 2000)

            print(f"📁 Project loaded: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load project:\n{e}")

    def _load_last_project(self):
        """Load last opened project"""
        # TODO: Implement loading last project from settings
        pass

    def _import_project(self):
        """Import project from other formats"""
        print("📥 Import project requested")
        # TODO: Implement project import

    def _export_project(self):
        """Export project to other formats"""
        print("📤 Export project requested")
        # TODO: Implement project export

    def _check_unsaved_changes(self):
        """Check for unsaved changes"""
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "Save current project before continuing?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Save:
                self._save_project()
                return not self.is_modified
            elif reply == QMessageBox.StandardButton.Cancel:
                return False

        return True

    # EDIT OPERATIONS

    def _undo(self):
        """Undo last operation"""
        print("↶ Undo")
        # TODO: Implement undo

    def _redo(self):
        """Redo last undone operation"""
        print("↷ Redo")
        # TODO: Implement redo

    def _cut(self):
        """Cut selected items"""
        print("✂️ Cut")
        # TODO: Implement cut

    def _copy(self):
        """Copy selected items"""
        print("📋 Copy")
        # TODO: Implement copy

    def _paste(self):
        """Paste items from clipboard"""
        print("📋 Paste")
        # TODO: Implement paste

    def _delete(self):
        """Delete selected items"""
        print("🗑️ Delete")
        if self.canvas and hasattr(self.canvas, 'delete_selected'):
            self.canvas.delete_selected()

    def _select_all(self):
        """Select all items"""
        print("🔲 Select All")
        if self.canvas and hasattr(self.canvas, 'select_all'):
            self.canvas.select_all()


    # VIEW OPERATIONS

    def _zoom_in(self):
        """Zoom in"""
        if self.canvas and hasattr(self.canvas, 'zoom_in'):
            self.canvas.zoom_in()
        print("🔍+ Zoom In")

    def _zoom_out(self):
        """Zoom out"""
        if self.canvas and hasattr(self.canvas, 'zoom_out'):
            self.canvas.zoom_out()
        print("🔍- Zoom Out")

    def _zoom_fit(self):
        """Zoom to fit all components"""
        if self.canvas and hasattr(self.canvas, 'zoom_fit'):
            self.canvas.zoom_fit()
        print("🔍 Zoom Fit")

    def _zoom_actual(self):
        """Zoom to actual size (100%)"""
        if self.canvas and hasattr(self.canvas, 'zoom_actual'):
            self.canvas.zoom_actual()
        print("🔍 Zoom Actual Size")

    def _toggle_grid(self, enabled=None):
        """Toggle grid display"""
        if enabled is None:
            # Toggle current state
            if self.canvas and hasattr(self.canvas, 'grid_visible'):
                enabled = not self.canvas.grid_visible
            else:
                enabled = True

        if self.canvas and hasattr(self.canvas, 'set_grid_visible'):
            self.canvas.set_grid_visible(enabled)

        print(f"🔲 Grid {'enabled' if enabled else 'disabled'}")

    def _toggle_rulers(self, enabled):
        """Toggle rulers display"""
        print(f"📏 Rulers {'enabled' if enabled else 'disabled'}")
        # TODO: Implement rulers

    def _toggle_snap(self, enabled):
        """Toggle snap to grid"""
        if self.canvas and hasattr(self.canvas, 'set_snap_to_grid'):
            self.canvas.set_snap_to_grid(enabled)
        print(f"🧲 Snap {'enabled' if enabled else 'disabled'}")

    def _set_grid_size(self, size):
        """Set grid size"""
        if self.canvas and hasattr(self.canvas, 'set_grid_size'):
            self.canvas.set_grid_size(size)
        print(f"🔲 Grid size: {size}")


    # PANEL TOGGLES

    def _toggle_component_palette(self, visible):
        """Toggle component palette visibility"""
        if hasattr(self, 'component_palette_dock'):
            self.component_palette_dock.setVisible(visible)

    def _toggle_cad_tools(self, visible=None):
        """Toggle CAD tools panel visibility"""
        if hasattr(self, 'cad_tools_dock'):
            if visible is None:
                visible = not self.cad_tools_dock.isVisible()
            self.cad_tools_dock.setVisible(visible)

    def _toggle_properties(self, visible):
        """Toggle properties panel visibility"""
        if hasattr(self, 'properties_dock'):
            self.properties_dock.setVisible(visible)

    def _toggle_layers(self, visible):
        """Toggle layers panel visibility"""
        if hasattr(self, 'layer_controls_dock'):
            self.layer_controls_dock.setVisible(visible)


    # COMPONENT OPERATIONS

    def _add_component(self, component_type):
        """Add component to canvas"""
        if self.canvas and hasattr(self.canvas, 'add_component'):
            self.canvas.add_component(component_type)

        self.is_modified = True
        self._update_window_title()
        self._update_status_counts()

        print(f"🔧 Adding component: {component_type}")


    # PRESET OPERATIONS

    def _apply_preset(self, preset_name):
        """Apply CAD preset"""
        presets = {
            'fine': {
                'grid_size': 5,
                'trace_width': 0.1,
                'via_size': 0.2,
                'pad_size': 0.8
            },
            'standard': {
                'grid_size': 10,
                'trace_width': 0.2,
                'via_size': 0.3,
                'pad_size': 1.0
            },
            'prototype': {
                'grid_size': 20,
                'trace_width': 0.3,
                'via_size': 0.4,
                'pad_size': 1.2
            },
            'breadboard': {
                'grid_size': 25,
                'trace_width': 0.5,
                'via_size': 0.6,
                'pad_size': 1.5
            }
        }

        if preset_name in presets:
            preset = presets[preset_name]

            # Apply grid size
            if self.canvas and hasattr(self.canvas, 'set_grid_size'):
                self.canvas.set_grid_size(preset['grid_size'])

            # Apply other settings to CAD tools panel
            if self.cad_tools_panel and hasattr(self.cad_tools_panel, 'apply_preset'):
                self.cad_tools_panel.apply_preset(preset)

            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage(f"Applied preset: {preset_name}", 2000)

            print(f"🎯 Applied preset: {preset_name}")


    # SIMULATION OPERATIONS

    def _start_simulation(self):
        """Start simulation"""
        if self.simulation_engine:
            self.simulation_engine.start()
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage("Simulation started", 2000)
        print("▶️ Simulation started")

    def _stop_simulation(self):
        """Stop simulation"""
        if self.simulation_engine:
            self.simulation_engine.stop()
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage("Simulation stopped", 2000)
        print("⏹️ Simulation stopped")

    def _pause_simulation(self):
        """Pause simulation"""
        print("⏸️ Simulation paused")
        # TODO: Implement pause

    def _step_simulation(self):
        """Step simulation forward"""
        if self.simulation_engine and hasattr(self.simulation_engine, 'step'):
            self.simulation_engine.step()
        print("⏭️ Simulation step")

    def _reset_simulation(self):
        """Reset simulation"""
        print("🔄 Simulation reset")
        # TODO: Implement reset

    def _show_simulation_settings(self):
        """Show simulation settings dialog"""
        print("⚙️ Simulation settings")
        # TODO: Implement simulation settings dialog


    # DIALOG FUNCTIONS

    def _show_search_dialog(self):
        """Show search dialog (Ctrl+F)"""
        from PyQt6.QtWidgets import QInputDialog

        text, ok = QInputDialog.getText(self, 'Search', 'Search for:')
        if ok and text:
            print(f"🔍 Searching for: {text}")
            # TODO: Implement search functionality

    def _show_command_palette(self):
        """Show command palette (Ctrl+Shift+P)"""
        from PyQt6.QtWidgets import QInputDialog

        commands = [
            "New Project",
            "Open Project",
            "Save Project",
            "Toggle Grid",
            "Zoom Fit",
            "Add Resistor",
            "Add Capacitor",
            "Start Simulation",
            "Stop Simulation",
            "Apply Fine Preset",
            "Apply Standard Preset"
        ]

        command, ok = QInputDialog.getItem(self, 'Command Palette',
                                         'Select command:', commands, 0, False)
        if ok:
            print(f"⚡ Executing command: {command}")
            # TODO: Implement command execution

    def _show_preferences(self):
        """Show preferences dialog"""
        print("⚙️ Preferences")
        # TODO: Implement preferences dialog

    def _show_shortcuts(self):
        """Show keyboard shortcuts help"""
        shortcuts_text = """
<b>🎹 Shortcuts</b><br><br>

<b>📁 File Operations:</b><br>
<b>Ctrl+N</b> - New Project<br>
<b>Ctrl+O</b> - Open Project<br>
<b>Ctrl+S</b> - Save Project<br>
<b>Ctrl+Shift+S</b> - Save As<br>
<b>Ctrl+Q</b> - Exit<br><br>

<b>✏️ Edit Operations:</b><br>
<b>Ctrl+Z</b> - Undo<br>
<b>Ctrl+Y</b> - Redo<br>
<b>Ctrl+X</b> - Cut<br>
<b>Ctrl+C</b> - Copy<br>
<b>Ctrl+V</b> - Paste<br>
<b>Delete</b> - Delete Selected<br>
<b>Ctrl+A</b> - Select All<br><br>

<b>🔧 CAD Tools:</b><br>
<b>S</b> - Select Tool<br>
<b>P</b> - Place Component Tool<br>
<b>W</b> - Wire Tool<br>
<b>T</b> - Trace Tool<br>
<b>V</b> - Via Tool<br>
<b>A</b> - Pad Tool<br>
<b>M</b> - Measure Tool<br>
<b>Escape</b> - Cancel Current Operation<br><br>

<b>👁️ View Controls:</b><br>
<b>Ctrl+=</b> - Zoom In<br>
<b>Ctrl+-</b> - Zoom Out<br>
<b>Ctrl+0</b> - Zoom Fit<br>
<b>Ctrl+1</b> - Actual Size<br>
<b>Ctrl+G</b> - Toggle Grid<br>
<b>Ctrl+R</b> - Toggle Rulers<br>
<b>Ctrl+D</b> - Toggle CAD Tools Panel<br><br>

<b>🎮 Simulation:</b><br>
<b>F5</b> - Start Simulation<br>
<b>Shift+F5</b> - Stop Simulation<br>
<b>F6</b> - Pause Simulation<br>
<b>F10</b> - Step Forward<br>
<b>Ctrl+F5</b> - Reset Simulation<br><br>

<b>🔍 Search & Help:</b><br>
<b>Ctrl+F</b> - Search<br>
<b>Ctrl+Shift+P</b> - Command Palette<br>
<b>F1</b> - Show This Help<br>
        """

        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text)

    def _show_about(self):
        """Show about dialog"""
        about_text = """
<b>Visual Retro System Emulator Builder</b><br>
<i>CAD Edition</i><br><br>

<b>Version:</b> 1.0.0 CAD Functions<br>
<b>Date:</b> June 17, 2025<br><br>

<b>🔧 Features:</b><br>
• Professional Electronic CAD Tools<br>
• Multi-layer PCB Design Support<br>
• Component Library with Retro Chips<br>
• Real-time Grid and Snap System<br>
• Complete Project Management<br>
• Professional Keyboard Shortcuts<br>
• Comprehensive Simulation Engine<br>
• Dark Theme Interface<br>
• Export to Manufacturing Formats<br><br>

<b>🎯 Target Systems:</b><br>
• Z80-based Computers<br>
• 6502-based Systems<br>
• 68000-based Machines<br>
• Custom Retro Designs<br><br>

<b>📧 Support:</b> support@xseti.com<br>
<b>🌐 Website:</b> www.xseti.com<br>
        """

        QMessageBox.about(self, "About X-Seti", about_text)

    def _cancel_current_operation(self):
        """Cancel current operation (Escape)"""
        if self.canvas and hasattr(self.canvas, 'cancel_operation'):
            self.canvas.cancel_operation()

        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage("Operation cancelled", 1000)

        print("❌ Operation cancelled")


    # UPDATE FUNCTIONS

    def _update_window_title(self):
        """Update window title"""
        title = "Visual Retro System Emulator Builder - CAD Functons"

        if self.current_project_path:
            project_name = os.path.basename(self.current_project_path)
            title += f" - {project_name}"
        else:
            title += " - Untitled Project"

        if self.is_modified:
            title += " *"

        self.setWindowTitle(title)

    def _update_status_counts(self):
        """Update status bar counts"""
        if hasattr(self, 'component_count_label') and self.component_count_label is not None:
            # Component count
            component_count = 0
            if self.canvas and hasattr(self.canvas, 'components'):
                component_count = len(self.canvas.components)
            elif self.component_manager and hasattr(self.component_manager, 'components'):
                component_count = len(self.component_manager.components)

            self.component_count_label.setText(f"Components: {component_count}")

        if hasattr(self, 'connection_count_label') and self.connection_count_label is not None:
            # Connection count
            connection_count = 0
            if self.canvas and hasattr(self.canvas, 'connections'):
                connection_count = len(self.canvas.connections)

            self.connection_count_label.setText(f"Connections: {connection_count}")

        if hasattr(self, 'cad_item_count_label') and self.cad_item_count_label is not None:
            # CAD item count
            cad_count = 0
            if self.canvas and hasattr(self.canvas, 'cad_items'):
                cad_count = len(self.canvas.cad_items)

            self.cad_item_count_label.setText(f"CAD Items: {cad_count}")

    def _update_ui_state(self):
        """Update UI state based on current conditions"""
        # Update counts
        self._update_status_counts()

        # Update tool display
        if hasattr(self, 'tool_label') and self.tool_label is not None:
            self.tool_label.setText(f"Tool: {self.current_tool.title()}")

        # Update zoom display if available
        if hasattr(self, 'zoom_label') and self.zoom_label is not None and self.canvas:
            if hasattr(self.canvas, 'zoom_factor'):
                zoom_percent = int(self.canvas.zoom_factor * 100)
                self.zoom_label.setText(f"Zoom: {zoom_percent}%")


    # EVENT HANDLERS

    def mouseMoveEvent(self, event):
        """Handle mouse move events for coordinate display"""
        super().mouseMoveEvent(event)

        if (hasattr(self, 'coordinate_label') and self.coordinate_label is not None and
            self.canvas and hasattr(self.canvas, 'mapToScene')):
            try:
                # Get mouse position relative to canvas
                canvas_pos = self.canvas.mapFromGlobal(event.globalPosition().toPoint())
                scene_pos = self.canvas.mapToScene(canvas_pos)
                self.coordinate_label.setText(f"X: {int(scene_pos.x())}, Y: {int(scene_pos.y())}")
            except (AttributeError, TypeError):
                # Silently handle any coordinate conversion errors
                pass

    def closeEvent(self, event):
        """Handle window close event"""
        if self._check_unsaved_changes():
            event.accept()
            print("👋 Application closed")
        else:
            event.ignore()

    def resizeEvent(self, event):
        """Handle window resize event"""
        super().resizeEvent(event)
        # Update canvas if needed
        if self.canvas and hasattr(self.canvas, 'update_viewport'):
            self.canvas.update_viewport()

    def keyPressEvent(self, event):
        """Handle key press events"""
        super().keyPressEvent(event)

        # Handle tool-specific key events
        if self.canvas and hasattr(self.canvas, 'keyPressEvent'):
            self.canvas.keyPressEvent(event)


    # UTILITY METHODS

    def get_current_tool(self):
        """Get current tool name"""
        return self.current_tool

    def get_canvas(self):
        """Get canvas widget"""
        return self.canvas

    def get_component_manager(self):
        """Get component manager"""
        return self.component_manager

    def get_project_manager(self):
        """Get project manager"""
        return self.project_manager

    def get_simulation_engine(self):
        """Get simulation engine"""
        return self.simulation_engine

    def show_message(self, message, timeout=2000):
        """Show message in status bar"""
        if hasattr(self, 'status_bar') and self.status_bar is not None:
            self.status_bar.showMessage(message, timeout)

    def set_modified(self, modified=True):
        """Set project modified state"""
        self.is_modified = modified
        self._update_window_title()

    def refresh_ui(self):
        """Refresh entire UI"""
        self._update_window_title()
        self._update_status_counts()
        self._update_ui_state()

        # Refresh panels
        if self.component_palette and hasattr(self.component_palette, 'refresh'):
            self.component_palette.refresh()

        if self.property_editor and hasattr(self.property_editor, 'refresh'):
            self.property_editor.refresh()

        if self.layer_controls and hasattr(self.layer_controls, 'refresh'):
            self.layer_controls.refresh()


# Export all variants
__all__ = ['MainWindow']

# MODULE TEST

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show main window
    window = MainWindow()
    window.show()
    self.initialize_chip_integration()

    print("🚀 Main Window running!")
    print("=" * 60)
    print("✅ ALL FEATURES AVAILABLE:")
    print("  • Multiple Toolbars")
    print("  • Dockable Panels")
    print("  • Keyboard Shortcuts")
    print("  • Project Management")
    print("  • Component Library")
    print("  • Grid & Snap Controls")
    print("  • Zoom & Pan Controls")
    print("=" * 60)

    sys.exit(app.exec())
