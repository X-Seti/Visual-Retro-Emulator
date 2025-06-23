#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Main Window Implementation
"""
#this belongs in ui/main_window.py

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
        self.layer_controls = None
        self.cad_tools_panel = None
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

        # Dock widgets - UPDATED NAMES TO MATCH IMPLEMENTATION
        self.component_palette_dock = None
        self.display_controls_dock = None  # ← Renamed from left_tools_dock
        self.properties_dock = None
        self.layer_controls_dock = None
        self.cad_tools_dock = None  # ← Added missing CAD tools dock

        # Control widget references for keyboard shortcuts
        self.pin_numbers_check = None
        self.component_labels_check = None
        self.grid_check = None
        self.snap_check = None
        self.grid_size_spin = None
        self.zoom_slider = None
        self.zoom_display = None

        # Apply theme - use global theme manager
        # self._apply_dark_theme()

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
        self._initialize_pin_numbers()

        # Update display
        self._update_window_title()
        self._update_status_counts()

        print("✅ Complete Main Window initialized with clean dock structure")

    def _initialize_managers(self):
        """Initialize all manager components"""
        print("Initializing managers...")

        try:
            # Initialize Layer Manager
            from managers.layer_manager import LayerManager
            self.layer_manager = LayerManager()
            print("✓ Layer Manager initialized")
        except ImportError as e:
            print(f"⚠️ Layer Manager not available: {e}")
            self.layer_manager = None

        try:
            # Initialize Component Manager
            from core.components import ComponentManager
            self.component_manager = ComponentManager()
            print("✓ Component Manager initialized")
        except ImportError as e:
            print(f"⚠️ Component Manager not available: {e}")
            self.component_manager = None

        try:
            # Initialize Project Manager
            from managers.project_manager import ProjectManager
            self.project_manager = ProjectManager()
            print("✓ Project Manager initialized")
        except ImportError as e:
            print(f"⚠️ Project Manager not available: {e}")
            self.project_manager = None

        try:
            # Initialize Simulation Engine
            from core.simulation import SimulationEngine
            self.simulation_engine = SimulationEngine()
            print("✓ Simulation Engine initialized")
        except ImportError as e:
            print(f"⚠️ Simulation Engine not available: {e}")
            self.simulation_engine = None

    def _initialize_pin_numbers(self):
        """Initialize pin numbers manager - call from __init__ or _post_init_setup"""
        try:
            from .pin_numbers import add_pin_numbers_to_canvas

            if self.canvas:
                self.pin_numbers_manager = add_pin_numbers_to_canvas(self.canvas)
                print("✓ Pin numbers manager initialized")
            else:
                print("⚠️ Canvas not available for pin numbers initialization")

        except ImportError as e:
            print(f"⚠️ Could not import pin numbers module: {e}")
            self.pin_numbers_manager = None

    def _add_pin_numbers_to_view_menu(self):
        """Add pin numbers options to View menu - call from _create_menu_bar"""
        if not hasattr(self, 'view_menu'):
            print("⚠️ No view_menu found")
            return

        # Add separator
        self.view_menu.addSeparator()

        # Pin Numbers submenu
        pin_menu = self.view_menu.addMenu("📍 Pin Numbers")

        # Show/Hide pin numbers
        self.pin_numbers_action = pin_menu.addAction("Show Pin Numbers")
        self.pin_numbers_action.setCheckable(True)
        self.pin_numbers_action.setChecked(True)
        self.pin_numbers_action.triggered.connect(self._toggle_pin_numbers)

        # Pin number styles
        pin_style_menu = pin_menu.addMenu("Pin Number Style")

        self.pin_style_group = []
        styles = ["Outside", "Inside", "On Pin", "Tooltips Only"]

        for style in styles:
            action = pin_style_menu.addAction(style)
            action.setCheckable(True)
            if style == "Outside":
                action.setChecked(True)
            action.triggered.connect(lambda checked, s=style: self._set_pin_number_style(s))
            self.pin_style_group.append(action)

        print("✓ Pin numbers menu added to View menu")

    def _add_pin_numbers_hotkeys(self):
        """Add pin numbers keyboard shortcuts - call from _setup_hotkeys"""
        try:
            from PyQt6.QtGui import QShortcut, QKeySequence

            # Toggle pin numbers
            pin_shortcut = QShortcut(QKeySequence('Ctrl+P'), self)
            pin_shortcut.activated.connect(self._toggle_pin_numbers)

            # Cycle pin styles
            style_shortcut = QShortcut(QKeySequence('Ctrl+Shift+P'), self)
            style_shortcut.activated.connect(self._cycle_pin_styles)

            print("✓ Pin numbers hotkeys added (Ctrl+P, Ctrl+Shift+P)")

        except ImportError as e:
            print(f"⚠️ Could not add pin numbers hotkeys: {e}")

    def _toggle_pin_numbers(self, enabled=None):
        """Toggle pin numbers visibility"""
        if enabled is None:
            enabled = self.pin_numbers_action.isChecked()

        if hasattr(self, 'pin_numbers_manager') and self.pin_numbers_manager:
            self.pin_numbers_manager.set_pin_numbers_visible(enabled)
            print(f"🔢 Pin numbers {'shown' if enabled else 'hidden'}")
        elif self.canvas and hasattr(self.canvas, 'set_pin_numbers_visible'):
            self.canvas.set_pin_numbers_visible(enabled)
            print(f"🔢 Pin numbers {'shown' if enabled else 'hidden'}")
        else:
            print("⚠️ Pin numbers not available")

    def _set_pin_number_style(self, style):
        """Set pin number display style"""
        # Uncheck all style actions
        for action in self.pin_style_group:
            action.setChecked(False)

        # Check the selected style
        for action in self.pin_style_group:
            if action.text() == style:
                action.setChecked(True)
                break

        # Apply the style
        if hasattr(self, 'pin_numbers_manager') and self.pin_numbers_manager:
            self.pin_numbers_manager.set_pin_number_style(style.lower().replace(" ", "_"))
            print(f"📌 Pin number style: {style}")
        else:
            print(f"⚠️ Pin numbers manager not available for style: {style}")

    def _cycle_pin_styles(self):
        """Cycle through pin number styles"""
        if not hasattr(self, 'pin_style_group'):
            return

        # Find currently checked style
        current_index = -1
        for i, action in enumerate(self.pin_style_group):
            if action.isChecked():
                current_index = i
                break

        # Move to next style
        next_index = (current_index + 1) % len(self.pin_style_group)
        next_style = self.pin_style_group[next_index].text()
        self._set_pin_number_style(next_style)


    def _create_canvas(self):
        """Create main canvas"""
        self.canvas = self._create_canvasarea()

    def _create_canvasarea(self):
        """Create enhanced canvas with realistic chip rendering"""
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
                
                # Display settings
                self.show_pin_numbers = True
                self.show_component_labels = True
                
                # Component tracking
                self.components = {}
                self.connections = []

                # Enable drag & drop
                self.setAcceptDrops(True)
                self.setBackgroundBrush(QBrush(QColor(40, 40, 50)))

                # Set viewport update mode for better grid rendering
                self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

                print("✓ Enhanced canvas created with realistic chip rendering")
                self.viewport().update()

            def drawBackground(self, painter, rect):
                super().drawBackground(painter, rect)
                if self.grid_visible:
                    self._draw_grid(painter, rect)

            def _draw_grid(self, painter, rect):
                """Draw grid lines"""
                painter.save()
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

            def dragEnterEvent(self, event):
                """Handle drag enter"""
                if event.mimeData().hasText():
                    text = event.mimeData().text()
                    if (text.startswith("component:") or ":" in text):
                        event.acceptProposedAction()
                        print(f"✅ Drag accepted: {text}")
                    else:
                        event.ignore()
                else:
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
                        # Parse component data
                        if component_data.startswith("component:"):
                            parts = component_data.split(":", 3)
                            if len(parts) >= 3:
                                category = parts[1]
                                name = parts[2]
                                package = parts[3] if len(parts) > 3 else "DIP-40"
                        elif ":" in component_data:
                            parts = component_data.split(":", 2)
                            category = parts[0] if len(parts) > 0 else "Unknown"
                            name = parts[1] if len(parts) > 1 else "Component"
                            package = parts[2] if len(parts) > 2 else "DIP-40"
                        else:
                            category = "Unknown"
                            name = component_data
                            package = "DIP-40"

                        # Get drop position
                        scene_pos = self.mapToScene(event.position().toPoint())

                        # Snap to grid
                        if self.snap_to_grid:
                            scene_pos.setX(round(scene_pos.x() / self.grid_size) * self.grid_size)
                            scene_pos.setY(round(scene_pos.y() / self.grid_size) * self.grid_size)

                        # Create realistic component
                        comp_id = self._create_realistic_component(name, category, package, scene_pos)
                        if comp_id:
                            print(f"🎯 Component created: {name} from {category}")

                        event.acceptProposedAction()

                    except Exception as e:
                        print(f"❌ Error handling drop: {e}")
                        import traceback
                        traceback.print_exc()
                        event.ignore()
                else:
                    event.ignore()

            def _create_realistic_component(self, name, category, package, position):
                """Create a highly realistic visual component"""
                try:
                    from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem
                    
                    # Create component group
                    component_group = QGraphicsItemGroup()
                    
                    # Get package info
                    package_info = self._get_package_info(package, name, category)
                    width = package_info['width']
                    height = package_info['height']
                    pin_count = package_info['pin_count']
                    
                    # Create main chip body
                    body_rect = QGraphicsRectItem(-width/2, -height/2, width, height)
                    
                    # Get realistic colors
                    body_color, outline_color, text_color = self._get_chip_colors(name, category)
                    
                    body_rect.setBrush(QBrush(body_color))
                    body_rect.setPen(QPen(outline_color, 1.8))
                    component_group.addToGroup(body_rect)
                    
                    # Add package-specific features
                    if package.startswith("DIP"):
                        self._add_dip_notch(component_group, width, height)
                        self._create_dip_pins(component_group, width, height, pin_count)
                    elif package.startswith("QFP"):
                        self._add_pin1_dot(component_group, width, height)
                        self._create_qfp_pins(component_group, width, height, pin_count)
                    
                    # Add enhanced labels
                    self._add_chip_labels(component_group, name, package, width, height, text_color, category)
                    
                    # Position and configure
                    component_group.setPos(position)
                    component_group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
                    component_group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)
                    
                    # Add to scene
                    self.scene().addItem(component_group)
                    
                    # Track component
                    comp_id = f"{name}_{len(self.components)}"
                    self.components[comp_id] = {
                        'group': component_group,
                        'name': name,
                        'category': category,
                        'package': package,
                        'position': position,
                        'width': width,
                        'height': height,
                        'pin_count': pin_count
                    }

                    print(f"✅ Realistic component created: {name} ({package}) - {pin_count} pins")
                    return comp_id

                except Exception as e:
                    print(f"❌ Error creating realistic component: {e}")
                    import traceback
                    traceback.print_exc()
                    return None

            def _get_package_info(self, package, name, category):
                """Get package dimensions and pin info"""
                info = {'width': 60, 'height': 120, 'pin_count': 40}
                
                if package.startswith("DIP"):
                    try:
                        pin_count = int(package.split("-")[1])
                    except:
                        pin_count = 40
                    
                    # Scale based on pin count
                    if pin_count <= 8:
                        info.update({'width': 32, 'height': 40, 'pin_count': pin_count})
                    elif pin_count <= 14:
                        info.update({'width': 32, 'height': 56, 'pin_count': pin_count})
                    elif pin_count <= 16:
                        info.update({'width': 32, 'height': 64, 'pin_count': pin_count})
                    elif pin_count <= 20:
                        info.update({'width': 32, 'height': 80, 'pin_count': pin_count})
                    elif pin_count <= 24:
                        info.update({'width': 32, 'height': 96, 'pin_count': pin_count})
                    elif pin_count <= 28:
                        info.update({'width': 32, 'height': 112, 'pin_count': pin_count})
                    elif pin_count <= 40:
                        info.update({'width': 32, 'height': 160, 'pin_count': pin_count})
                    elif pin_count <= 64:
                        info.update({'width': 38, 'height': 256, 'pin_count': pin_count})
                
                elif package.startswith("QFP"):
                    try:
                        pin_count = int(package.split("-")[1])
                    except:
                        pin_count = 44
                    
                    side_length = max(48, pin_count * 1.3)
                    info.update({'width': side_length, 'height': side_length, 'pin_count': pin_count})
                
                return info

            def _get_chip_colors(self, name, category):
                """Get authentic chip colors"""
                # Default colors
                body_color = QColor(50, 50, 60)
                outline_color = QColor(175, 175, 175)
                text_color = QColor(255, 255, 255)
                
                if category == "CPUs":
                    if "Z80" in name:
                        body_color = QColor(35, 35, 45)  # Dark Zilog ceramic
                    elif "6502" in name or "6510" in name:
                        body_color = QColor(45, 35, 35)  # MOS brownish
                    elif "68000" in name:
                        body_color = QColor(40, 40, 50)  # Motorola ceramic
                    elif "8080" in name or "8086" in name:
                        body_color = QColor(45, 45, 55)  # Intel ceramic
                        
                elif category == "Memory":
                    if "27" in name:  # EPROM
                        body_color = QColor(55, 45, 65)  # Purple-tinted
                    else:
                        body_color = QColor(55, 55, 65)
                        
                elif category == "Graphics":
                    if "VIC" in name or "6567" in name:
                        body_color = QColor(45, 35, 55)  # Commodore purple-brown
                    elif "TMS" in name:
                        body_color = QColor(40, 50, 40)  # TI greenish
                    elif name in ["Agnus", "Denise", "Paula"]:
                        body_color = QColor(35, 45, 35)  # Amiga green
                        
                elif category == "Audio":
                    if "SID" in name:
                        body_color = QColor(45, 35, 55)  # Commodore SID
                    elif "AY" in name or "YM" in name:
                        body_color = QColor(40, 50, 50)  # Yamaha teal
                        
                elif category == "Logic":
                    body_color = QColor(25, 25, 25)  # Black plastic
                    text_color = QColor(220, 220, 220)
                
                return body_color, outline_color, text_color

            def _add_dip_notch(self, group, width, height):
                """Add DIP notch"""
                notch_width = min(width * 0.4, 12)
                notch_height = 4
                notch = QGraphicsRectItem(-notch_width/2, -height/2 - 1, notch_width, notch_height)
                notch.setBrush(QBrush(QColor(15, 15, 15)))
                notch.setPen(QPen(QColor(80, 80, 80), 0.8))
                group.addToGroup(notch)

            def _add_pin1_dot(self, group, width, height):
                """Add pin 1 dot for surface mount packages"""
                dot = QGraphicsEllipseItem(-width/2 + 6, -height/2 + 6, 3, 3)
                dot.setBrush(QBrush(QColor(255, 255, 255)))
                dot.setPen(QPen(QColor(200, 200, 200), 0.5))
                group.addToGroup(dot)

            def _create_dip_pins(self, group, width, height, pin_count):
                """Create DIP pins with numbers on the outside"""
                pins_per_side = pin_count // 2
                pin_spacing = (height - 20) / (pins_per_side - 1) if pins_per_side > 1 else 0
                start_y = -height/2 + 10
                
                # Left side pins (1 to N/2)
                for i in range(pins_per_side):
                    y_pos = start_y + (i * pin_spacing)
                    
                    # Main pin body - extending outward from chip
                    pin = QGraphicsRectItem(-width/2 - 8, y_pos - 1, 8, 2)
                    pin.setBrush(QBrush(QColor(220, 220, 230)))
                    pin.setPen(QPen(QColor(180, 180, 190), 0.8))
                    group.addToGroup(pin)
                    
                    # Pin number - OUTSIDE the chip, to the left of the pin
                    if self.show_pin_numbers and (pin_count <= 28 or i % 2 == 0):
                        pin_num = QGraphicsTextItem(str(i + 1))
                        pin_num.setDefaultTextColor(QColor(200, 200, 200))
                        pin_num.setFont(QFont("Arial", 6, QFont.Weight.Bold))
                        pin_rect = pin_num.boundingRect()
                        # Position to the left of the pin, outside the chip
                        pin_num.setPos(-width/2 - 8 - pin_rect.width() - 2, y_pos - pin_rect.height()/2)
                        group.addToGroup(pin_num)
                
                # Right side pins (N/2+1 to N) - numbered counter-clockwise
                for i in range(pins_per_side):
                    y_pos = start_y + ((pins_per_side - 1 - i) * pin_spacing)
                    
                    # Main pin body
                    pin = QGraphicsRectItem(width/2, y_pos - 1, 8, 2)
                    pin.setBrush(QBrush(QColor(220, 220, 230)))
                    pin.setPen(QPen(QColor(180, 180, 190), 0.8))
                    group.addToGroup(pin)
                    
                    # Pin number - OUTSIDE the chip, to the right of the pin
                    if self.show_pin_numbers and (pin_count <= 28 or i % 2 == 0):
                        pin_num = QGraphicsTextItem(str(pins_per_side + i + 1))
                        pin_num.setDefaultTextColor(QColor(200, 200, 200))
                        pin_num.setFont(QFont("Arial", 6, QFont.Weight.Bold))
                        pin_rect = pin_num.boundingRect()
                        # Position to the right of the pin, outside the chip
                        pin_num.setPos(width/2 + 8 + 2, y_pos - pin_rect.height()/2)
                        group.addToGroup(pin_num)

            def _create_qfp_pins(self, group, width, height, pin_count):
                """Create QFP pins"""
                pins_per_side = pin_count // 4
                pin_size = 3
                
                # Top, Right, Bottom, Left sides
                for side in range(4):
                    for i in range(pins_per_side):
                        if side == 0:  # Top
                            x_pos = -width/2 + (width / (pins_per_side + 1)) * (i + 1)
                            y_pos = -height/2 - pin_size
                            pin_rect = QRectF(x_pos - pin_size/2, y_pos, pin_size, pin_size)
                        elif side == 1:  # Right
                            x_pos = width/2
                            y_pos = -height/2 + (height / (pins_per_side + 1)) * (i + 1)
                            pin_rect = QRectF(x_pos, y_pos - pin_size/2, pin_size, pin_size)
                        elif side == 2:  # Bottom
                            x_pos = width/2 - (width / (pins_per_side + 1)) * (i + 1)
                            y_pos = height/2
                            pin_rect = QRectF(x_pos - pin_size/2, y_pos, pin_size, pin_size)
                        else:  # Left
                            x_pos = -width/2 - pin_size
                            y_pos = height/2 - (height / (pins_per_side + 1)) * (i + 1)
                            pin_rect = QRectF(x_pos, y_pos - pin_size/2, pin_size, pin_size)
                        
                        pin = QGraphicsRectItem(pin_rect)
                        pin.setBrush(QBrush(QColor(210, 210, 220)))
                        pin.setPen(QPen(QColor(170, 170, 180), 0.6))
                        group.addToGroup(pin)

            def _add_chip_labels(self, group, name, package, width, height, text_color, category):
                """Add enhanced chip labels oriented along the chip's length"""
                # Check if labels should be shown
                if not self.show_component_labels:
                    return
                
                # Determine orientation based on chip dimensions
                is_tall = height > width * 1.5  # Chip is taller than it is wide
                
                # Main component name
                display_name = name
                if len(name) > 10 and category != "Logic":
                    if "-" in name:
                        parts = name.split("-", 1)
                        display_name = parts[0] + "\n" + parts[1]
                
                text_item = QGraphicsTextItem(display_name)
                text_item.setDefaultTextColor(text_color)
                
                # Font sizing based on chip dimensions
                if is_tall:
                    # For tall chips, use the width to determine font size
                    base_font_size = max(6, min(14, int(width / 4)))
                else:
                    # For wide chips, use the height to determine font size
                    base_font_size = max(6, min(14, int(height / 4)))
                
                if category == "Logic":
                    base_font_size = max(7, base_font_size)  # Logic chips need readable text
                
                font = QFont("Arial", base_font_size, QFont.Weight.Bold)
                text_item.setFont(font)
                
                # Rotate text for tall chips to align with length
                if is_tall:
                    # Rotate 90 degrees for vertical orientation
                    text_item.setRotation(90)
                
                # Center text after rotation
                text_rect = text_item.boundingRect()
                if is_tall:
                    # For rotated text, adjust positioning
                    text_item.setPos(-text_rect.height()/2, -text_rect.width()/2)
                else:
                    # Normal horizontal positioning
                    text_item.setPos(-text_rect.width()/2, -text_rect.height()/2)
                
                group.addToGroup(text_item)
                
                # Package label (smaller, positioned appropriately)
                if package not in ["DIP-40", "DIP-16", "DIP-14"]:
                    package_text = QGraphicsTextItem(package)
                    package_text.setDefaultTextColor(text_color.darker(130))
                    package_font = QFont("Arial", max(4, base_font_size - 3))
                    package_text.setFont(package_font)
                    
                    pkg_rect = package_text.boundingRect()
                    
                    if is_tall:
                        # For tall chips, rotate package label too and position at bottom
                        package_text.setRotation(90)
                        package_text.setPos(text_rect.height()/2 + 5, -pkg_rect.width()/2)
                    else:
                        # For wide chips, position at bottom
                        y_offset = height/2 - pkg_rect.height() - 2
                        if y_offset > text_rect.height()/2 + 2:
                            package_text.setPos(-pkg_rect.width()/2, y_offset)
                    
                    group.addToGroup(package_text)
                
                # Manufacturer labels for classic chips
                if category == "CPUs" and (width > 25 or height > 80):
                    mfg_text = ""
                    if "Z80" in name:
                        mfg_text = "ZILOG"
                    elif "6502" in name or "6510" in name:
                        mfg_text = "MOS"
                    elif "68000" in name:
                        mfg_text = "MOTOROLA"
                    elif "8080" in name or "8086" in name:
                        mfg_text = "INTEL"
                    
                    if mfg_text:
                        mfg_label = QGraphicsTextItem(mfg_text)
                        mfg_label.setDefaultTextColor(text_color.darker(160))
                        mfg_font = QFont("Arial", max(4, base_font_size - 4))
                        mfg_label.setFont(mfg_font)
                        
                        mfg_rect = mfg_label.boundingRect()
                        
                        if is_tall:
                            # For tall chips, rotate manufacturer label
                            mfg_label.setRotation(90)
                            mfg_label.setPos(-text_rect.height()/2 - mfg_rect.height() - 3, -mfg_rect.width()/2)
                        else:
                            # For wide chips, position below main text
                            mfg_label.setPos(-mfg_rect.width()/2, text_rect.height()/2 + 2)
                        
                        group.addToGroup(mfg_label)

            # Working toggle methods
            def toggle_pin_numbers(self, show=None):
                """Toggle pin number visibility - WORKING VERSION"""
                if show is None:
                    self.show_pin_numbers = not self.show_pin_numbers
                else:
                    self.show_pin_numbers = show

                print(f"📍 Pin numbers toggle: {self.show_pin_numbers}")

                # Recreate all components with new settings
                self._refresh_all_components()

            def toggle_component_labels(self, show=None):
                """Toggle component label visibility - WORKING VERSION"""
                if show is None:
                    self.show_component_labels = not self.show_component_labels
                else:
                    self.show_component_labels = show
                
                print(f"🏷️ Component labels toggle: {self.show_component_labels}")
                
                # Recreate all components with new settings
                self._refresh_all_components()

            def _refresh_all_components(self):
                """Refresh all components to apply new display settings"""
                # Store current component data
                components_to_recreate = []
                for comp_id, comp_data in self.components.items():
                    if 'group' in comp_data:
                        components_to_recreate.append({
                            'name': comp_data['name'],
                            'category': comp_data['category'],
                            'package': comp_data['package'],
                            'position': comp_data['group'].pos()
                        })
                        # Remove old component from scene
                        self.scene().removeItem(comp_data['group'])
                
                # Clear components dict
                self.components.clear()
                
                # Recreate all components with new settings
                for comp_data in components_to_recreate:
                    self._create_realistic_component(
                        comp_data['name'],
                        comp_data['category'],
                        comp_data['package'],
                        comp_data['position']
                    )
                
                print(f"🔄 Refreshed {len(components_to_recreate)} components")

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
                if self.components:
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
                print("🧹 Canvas cleared")

            def _create_realistic_component(self, name, category, package, position):
                """Create a highly realistic visual component"""
                try:
                    from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsLineItem
                    
                    # Create component group
                    component_group = QGraphicsItemGroup()
                    
                    # Get package info
                    package_info = self._get_package_info(package, name, category)
                    width = package_info['width']
                    height = package_info['height']
                    pin_count = package_info['pin_count']
                    
                    # Create main chip body
                    body_rect = QGraphicsRectItem(-width/2, -height/2, width, height)
                    
                    # Get realistic colors
                    body_color, outline_color, text_color = self._get_chip_colors(name, category)
                    
                    body_rect.setBrush(QBrush(body_color))
                    body_rect.setPen(QPen(outline_color, 1.8))
                    component_group.addToGroup(body_rect)
                    
                    # Add package-specific features
                    if package.startswith("DIP"):
                        self._add_dip_notch(component_group, width, height)
                        self._create_dip_pins(component_group, width, height, pin_count)
                    elif package.startswith("QFP"):
                        self._add_pin1_dot(component_group, width, height)
                        self._create_qfp_pins(component_group, width, height, pin_count)
                    
                    # Add enhanced labels
                    self._add_chip_labels(component_group, name, package, width, height, text_color, category)
                    
                    # Position and configure
                    component_group.setPos(position)
                    component_group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
                    component_group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)
                    
                    # Add to scene
                    self.scene().addItem(component_group)
                    
                    # Track component
                    comp_id = f"{name}_{len(self.components)}"
                    self.components[comp_id] = {
                        'group': component_group,
                        'name': name,
                        'category': category,
                        'package': package,
                        'position': position,
                        'width': width,
                        'height': height,
                        'pin_count': pin_count
                    }

                    print(f"✅ Realistic component created: {name} ({package}) - {pin_count} pins")
                    return comp_id

                except Exception as e:
                    print(f"❌ Error creating realistic component: {e}")
                    return None

            def _get_package_info(self, package, name, category):
                """Get package dimensions and pin info"""
                info = {'width': 60, 'height': 120, 'pin_count': 40}
                
                if package.startswith("DIP"):
                    try:
                        pin_count = int(package.split("-")[1])
                    except:
                        pin_count = 40
                    
                    # Scale based on pin count
                    if pin_count <= 8:
                        info.update({'width': 32, 'height': 40, 'pin_count': pin_count})
                    elif pin_count <= 14:
                        info.update({'width': 32, 'height': 56, 'pin_count': pin_count})
                    elif pin_count <= 16:
                        info.update({'width': 32, 'height': 64, 'pin_count': pin_count})
                    elif pin_count <= 20:
                        info.update({'width': 32, 'height': 80, 'pin_count': pin_count})
                    elif pin_count <= 24:
                        info.update({'width': 32, 'height': 96, 'pin_count': pin_count})
                    elif pin_count <= 28:
                        info.update({'width': 32, 'height': 112, 'pin_count': pin_count})
                    elif pin_count <= 40:
                        info.update({'width': 32, 'height': 160, 'pin_count': pin_count})
                    elif pin_count <= 64:
                        info.update({'width': 38, 'height': 256, 'pin_count': pin_count})
                
                elif package.startswith("QFP"):
                    try:
                        pin_count = int(package.split("-")[1])
                    except:
                        pin_count = 44
                    
                    side_length = max(48, pin_count * 1.3)
                    info.update({'width': side_length, 'height': side_length, 'pin_count': pin_count})
                
                return info

            def _get_chip_colors(self, name, category):
                """Get authentic chip colors"""
                # Default colors
                body_color = QColor(50, 50, 60)
                outline_color = QColor(175, 175, 175)
                text_color = QColor(255, 255, 255)
                
                if category == "CPUs":
                    if "Z80" in name:
                        body_color = QColor(35, 35, 45)  # Dark Zilog ceramic
                    elif "6502" in name or "6510" in name:
                        body_color = QColor(45, 35, 35)  # MOS brownish
                    elif "68000" in name:
                        body_color = QColor(40, 40, 50)  # Motorola ceramic
                    elif "8080" in name or "8086" in name:
                        body_color = QColor(45, 45, 55)  # Intel ceramic
                        
                elif category == "Memory":
                    if "27" in name:  # EPROM
                        body_color = QColor(55, 45, 65)  # Purple-tinted
                    else:
                        body_color = QColor(55, 55, 65)
                        
                elif category == "Graphics":
                    if "VIC" in name or "6567" in name:
                        body_color = QColor(45, 35, 55)  # Commodore purple-brown
                    elif "TMS" in name:
                        body_color = QColor(40, 50, 40)  # TI greenish
                    elif name in ["Agnus", "Denise", "Paula"]:
                        body_color = QColor(35, 45, 35)  # Amiga green
                        
                elif category == "Audio":
                    if "SID" in name:
                        body_color = QColor(45, 35, 55)  # Commodore SID
                    elif "AY" in name or "YM" in name:
                        body_color = QColor(40, 50, 50)  # Yamaha teal
                        
                elif category == "Logic":
                    body_color = QColor(25, 25, 25)  # Black plastic
                    text_color = QColor(220, 220, 220)
                
                return body_color, outline_color, text_color

            def _add_dip_notch(self, group, width, height):
                """Add DIP notch"""
                notch_width = min(width * 0.4, 12)
                notch_height = 4
                notch = QGraphicsRectItem(-notch_width/2, -height/2 - 1, notch_width, notch_height)
                notch.setBrush(QBrush(QColor(15, 15, 15)))
                notch.setPen(QPen(QColor(80, 80, 80), 0.8))
                group.addToGroup(notch)

            def _add_pin1_dot(self, group, width, height):
                """Add pin 1 dot for surface mount packages"""
                dot = QGraphicsEllipseItem(-width/2 + 6, -height/2 + 6, 3, 3)
                dot.setBrush(QBrush(QColor(255, 255, 255)))
                dot.setPen(QPen(QColor(200, 200, 200), 0.5))
                group.addToGroup(dot)

            def _create_dip_pins(self, group, width, height, pin_count):
                """Create DIP pins"""
                pins_per_side = pin_count // 2
                pin_spacing = (height - 20) / (pins_per_side - 1) if pins_per_side > 1 else 0
                start_y = -height/2 + 10
                
                # Left side pins
                for i in range(pins_per_side):
                    y_pos = start_y + (i * pin_spacing)
                    pin = QGraphicsRectItem(-width/2 - 8, y_pos - 1, 8, 2)
                    pin.setBrush(QBrush(QColor(220, 220, 230)))
                    pin.setPen(QPen(QColor(180, 180, 190), 0.8))
                    group.addToGroup(pin)
                    
                    # Pin number
                    if pin_count <= 28 or i % 2 == 0:
                        pin_num = QGraphicsTextItem(str(i + 1))
                        pin_num.setDefaultTextColor(QColor(255, 255, 255))
                        pin_num.setFont(QFont("Arial", 6, QFont.Weight.Bold))
                        pin_rect = pin_num.boundingRect()
                        pin_num.setPos(-width/2 + 2, y_pos - pin_rect.height()/2)
                        group.addToGroup(pin_num)
                
                # Right side pins
                for i in range(pins_per_side):
                    y_pos = start_y + ((pins_per_side - 1 - i) * pin_spacing)
                    pin = QGraphicsRectItem(width/2, y_pos - 1, 8, 2)
                    pin.setBrush(QBrush(QColor(220, 220, 230)))
                    pin.setPen(QPen(QColor(180, 180, 190), 0.8))
                    group.addToGroup(pin)
                    
                    # Pin number
                    if pin_count <= 28 or i % 2 == 0:
                        pin_num = QGraphicsTextItem(str(pins_per_side + i + 1))
                        pin_num.setDefaultTextColor(QColor(255, 255, 255))
                        pin_num.setFont(QFont("Arial", 6, QFont.Weight.Bold))
                        pin_rect = pin_num.boundingRect()
                        pin_num.setPos(width/2 - pin_rect.width() - 2, y_pos - pin_rect.height()/2)
                        group.addToGroup(pin_num)

            def _create_qfp_pins(self, group, width, height, pin_count):
                """Create QFP pins"""
                pins_per_side = pin_count // 4
                pin_size = 3
                
                # Top, Right, Bottom, Left sides
                for side in range(4):
                    for i in range(pins_per_side):
                        if side == 0:  # Top
                            x_pos = -width/2 + (width / (pins_per_side + 1)) * (i + 1)
                            y_pos = -height/2 - pin_size
                            pin_rect = QRectF(x_pos - pin_size/2, y_pos, pin_size, pin_size)
                        elif side == 1:  # Right
                            x_pos = width/2
                            y_pos = -height/2 + (height / (pins_per_side + 1)) * (i + 1)
                            pin_rect = QRectF(x_pos, y_pos - pin_size/2, pin_size, pin_size)
                        elif side == 2:  # Bottom
                            x_pos = width/2 - (width / (pins_per_side + 1)) * (i + 1)
                            y_pos = height/2
                            pin_rect = QRectF(x_pos - pin_size/2, y_pos, pin_size, pin_size)
                        else:  # Left
                            x_pos = -width/2 - pin_size
                            y_pos = height/2 - (height / (pins_per_side + 1)) * (i + 1)
                            pin_rect = QRectF(x_pos, y_pos - pin_size/2, pin_size, pin_size)
                        
                        pin = QGraphicsRectItem(pin_rect)
                        pin.setBrush(QBrush(QColor(210, 210, 220)))
                        pin.setPen(QPen(QColor(170, 170, 180), 0.6))
                        group.addToGroup(pin)

            def _add_chip_labels(self, group, name, package, width, height, text_color, category):
                """Add enhanced chip labels"""
                # Main component name
                display_name = name
                if len(name) > 10 and category != "Logic":
                    if "-" in name:
                        parts = name.split("-", 1)
                        display_name = parts[0] + "\n" + parts[1]
                
                text_item = QGraphicsTextItem(display_name)
                text_item.setDefaultTextColor(text_color)
                
                # Font sizing
                base_font_size = max(7, min(12, int(min(width, height) / 7)))
                if category == "Logic":
                    base_font_size = max(8, base_font_size)
                
                font = QFont("Arial", base_font_size, QFont.Weight.Bold)
                text_item.setFont(font)
                
                # Center text
                text_rect = text_item.boundingRect()
                text_item.setPos(-text_rect.width()/2, -text_rect.height()/2)
                group.addToGroup(text_item)
                
                # Package label
                if package not in ["DIP-40", "DIP-16", "DIP-14"]:
                    package_text = QGraphicsTextItem(package)
                    package_text.setDefaultTextColor(text_color.darker(130))
                    package_font = QFont("Arial", max(5, base_font_size - 3))
                    package_text.setFont(package_font)
                    
                    pkg_rect = package_text.boundingRect()
                    y_offset = height/2 - pkg_rect.height() - 2
                    if y_offset > text_rect.height()/2 + 2:
                        package_text.setPos(-pkg_rect.width()/2, y_offset)
                        group.addToGroup(package_text)
                
                # Manufacturer labels for classic chips
                if category == "CPUs" and height > 80:
                    mfg_text = ""
                    if "Z80" in name:
                        mfg_text = "ZILOG"
                    elif "6502" in name or "6510" in name:
                        mfg_text = "MOS"
                    elif "68000" in name:
                        mfg_text = "MOTOROLA"
                    
                    if mfg_text:
                        mfg_label = QGraphicsTextItem(mfg_text)
                        mfg_label.setDefaultTextColor(text_color.darker(160))
                        mfg_font = QFont("Arial", max(5, base_font_size - 4))
                        mfg_label.setFont(mfg_font)
                        
                        mfg_rect = mfg_label.boundingRect()
                        mfg_label.setPos(-mfg_rect.width()/2, text_rect.height()/2 + 2)
                        group.addToGroup(mfg_label)

            # Canvas control methods
            def set_grid_visible(self, visible):
                self.grid_visible = visible
                self.viewport().update()

            def set_grid_size(self, size):
                self.grid_size = size
                self.viewport().update()

            def set_snap_to_grid(self, enabled):
                self.snap_to_grid = enabled

            def zoom_fit(self):
                self.fitInView(self.scene().itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

            def zoom_in(self):
                self.scale(1.25, 1.25)

            def zoom_out(self):
                self.scale(0.8, 0.8)

            def clear(self):
                self.scene().clear()
                self.components.clear()

        return Canvas_DoodleArea()

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



    def _create_component_palette_dock(self):
        """Create enhanced component palette with comprehensive chip library"""
        from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QScrollArea
        from PyQt6.QtCore import QMimeData, QPoint
        from PyQt6.QtGui import QDrag, QPixmap, QPainter, QPen, QColor, QFont

        class ComponentTreeWidget(QTreeWidget):
            def __init__(self):
                super().__init__()
                self.setHeaderLabel("Components")
                self.setDragEnabled(True)
                self.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)

                # Enhanced component library
                categories = {
                    "CPUs": [
                        "Z80", "Z80A", "Z80B", "6502", "6502A", "6510", "65C02",
                        "8080", "8080A", "8085", "6800", "6809", "68000", "68008", 
                        "68010", "68020", "68030", "8086", "8088", "80286"
                    ],
                    "Memory": [
                        "2114", "4116", "4164", "41256", "6116", "6264", "62256",
                        "2708", "2716", "2732", "2764", "27128", "27256", "27512",
                        "2816", "2864", "28256", "X2816A", "DS1220Y"
                    ],
                    "Graphics": [
                        "VIC", "VIC-II", "6567", "6569", "8564", "VDC", "8563",
                        "TIA", "GTIA", "ANTIC", "POKEY", "TMS9918A", "TMS9928A",
                        "Agnus", "Denise", "Paula", "Gary", "Buster", "6845", "MC6845"
                    ],
                    "Audio": [
                        "SID", "6581", "8580", "AY-3-8910", "AY-3-8912", "YM2149",
                        "YM2203", "YM2612", "SN76489", "TIA", "Pokey", "Paula"
                    ],
                    "Logic": [
                        "74LS00", "74LS02", "74LS04", "74LS08", "74LS10", "74LS14",
                        "74LS20", "74LS32", "74LS74", "74LS76", "74LS83", "74LS85",
                        "74LS86", "74LS90", "74LS93", "74LS138", "74LS139", "74LS151",
                        "74LS153", "74LS157", "74LS161", "74LS240", "74LS244", "74LS245",
                        "74LS373", "74LS374", "74LS377"
                    ],
                    "I/O": [
                        "8255", "8255A", "Z80-PIO", "6522", "6821", "6840", "6850",
                        "8251", "Z80-SIO", "16550", "6526", "CIA", "8520"
                    ],
                    "Timers": [
                        "8253", "8254", "Z80-CTC", "6840", "NE555", "556", "MC6840"
                    ],
                    "Analog": [
                        "LM324", "LM358", "LM741", "TL072", "LM386", "LM393", "NE555"
                    ],
                    "Power": [
                        "7805", "7812", "7815", "LM317", "78L05", "79L05"
                    ],
                    "Connectors": [
                        "DB25", "DB9", "DIN-5", "RCA", "BNC", "Header-2x10", "IDC-40"
                    ]
                }

                for category, components in categories.items():
                    cat_item = QTreeWidgetItem(self, [f"📁 {category}"])
                    cat_item.setExpanded(True)

                    for comp in components:
                        comp_item = QTreeWidgetItem(cat_item, [f"🔲 {comp}"])
                        package = self._determine_package(comp, category)
                        comp_item.setData(0, Qt.ItemDataRole.UserRole, f"component:{category}:{comp}:{package}")

                print(f"✅ Enhanced component tree created with {sum(len(comps) for comps in categories.values())} components")

            def _determine_package(self, component, category):
                """Determine appropriate package for component"""
                if category == "CPUs":
                    if component in ["68000", "68020", "68030"]:
                        return "DIP-64"
                    else:
                        return "DIP-40"
                elif category == "Memory":
                    if component in ["2708", "2716", "2732"]:
                        return "DIP-24"
                    elif component in ["27128", "27256", "27512"]:
                        return "DIP-28"
                    else:
                        return "DIP-28"
                elif category == "Graphics":
                    if component in ["VIC-II", "6567", "TMS9918A"]:
                        return "DIP-40"
                    elif component in ["Agnus", "Denise", "Paula"]:
                        return "PLCC-84"
                    else:
                        return "DIP-40"
                elif category == "Audio":
                    if component in ["SID", "6581", "8580"]:
                        return "DIP-28"
                    elif component in ["AY-3-8910"]:
                        return "DIP-40"
                    else:
                        return "DIP-28"
                elif category == "Logic":
                    if component in ["74LS00", "74LS02", "74LS04", "74LS08", "74LS10", "74LS14", "74LS20", "74LS32"]:
                        return "DIP-14"
                    elif component in ["74LS240", "74LS244", "74LS245", "74LS373", "74LS374"]:
                        return "DIP-20"
                    else:
                        return "DIP-16"
                elif category == "I/O":
                    return "DIP-40"
                elif category == "Timers":
                    if component in ["NE555", "556"]:
                        return "DIP-8"
                    else:
                        return "DIP-24"
                elif category == "Analog":
                    if component in ["LM324"]:
                        return "DIP-14"
                    else:
                        return "DIP-8"
                elif category == "Power":
                    return "TO-220"
                else:
                    return "DIP-40"

            def startDrag(self, supportedActions):
                """Handle drag start"""
                current_item = self.currentItem()
                if current_item and current_item.parent():
                    drag_data = current_item.data(0, Qt.ItemDataRole.UserRole)

                    if drag_data:
                        drag = QDrag(self)
                        mime_data = QMimeData()
                        mime_data.setText(drag_data)
                        drag.setMimeData(mime_data)

                        pixmap = QPixmap(120, 30)
                        pixmap.fill(QColor(52, 152, 219, 180))

                        painter = QPainter(pixmap)
                        painter.setPen(QPen(QColor(255, 255, 255)))
                        painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))

                        comp_name = current_item.text(0).replace("🔲 ", "")
                        painter.drawText(5, 20, comp_name)
                        painter.end()

                        drag.setPixmap(pixmap)
                        drag.setHotSpot(QPoint(60, 15))

                        result = drag.exec(Qt.DropAction.CopyAction)
                        print(f"🎯 Drag executed: {drag_data}")
                        return

                super().startDrag(supportedActions)

        # Create main widget
        palette_widget = QWidget()
        layout = QVBoxLayout(palette_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create the tree
        tree = ComponentTreeWidget()
        tree.setMinimumHeight(400)
        layout.addWidget(tree)

        # Instructions
        instructions = QLabel("Drag components to canvas")
        instructions.setStyleSheet("color: #888; font-style: italic; font-size: 10px; padding: 5px;")
        layout.addWidget(instructions)

        # Create dock
        self.component_palette_dock = QDockWidget("Component Library", self)
        self.component_palette_dock.setWidget(palette_widget)
        self.component_palette_dock.setMinimumWidth(250)
        self.component_palette_dock.setMaximumWidth(350)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.component_palette_dock)

        print("✅ Enhanced component palette created")

    # Working event handlers with explicit state parameter
    def _on_tool_clicked(self, tool_id, button):
        """Handle tool button clicks - WORKING VERSION"""
        print(f"🔧 Tool button clicked: {tool_id}")
        
        # Uncheck all other buttons
        for tid, btn in self.tool_buttons.items():
            if tid != tool_id:
                btn.setChecked(False)
        
        # Ensure clicked button stays checked
        button.setChecked(True)
        
        # Set the tool
        self._set_tool_direct(tool_id)

    def _test_controls(self):
        """Test all controls to verify they work"""
        
        # Test pin numbers
        current_pin_state = self.pin_numbers_check.isChecked()
        print(f"📍 Pin numbers checkbox state: {current_pin_state}")
        
        # Test component labels
        current_label_state = self.component_labels_check.isChecked()
        print(f"🏷️ Component labels checkbox state: {current_label_state}")
        
        # Test grid
        current_grid_state = self.grid_check.isChecked()
        print(f"🔲 Grid checkbox state: {current_grid_state}")
        
        # Test canvas availability
        if self.canvas:
            print(f"✅ Canvas available: {type(self.canvas).__name__}")
            canvas_methods = [method for method in dir(self.canvas) if not method.startswith('_')]
            print(f"🔧 Canvas methods: {', '.join(canvas_methods[:10])}...")
        else:
            print("❌ Canvas not available")

    # Update keyboard shortcut methods to use working versions
    def _toggle_pin_numbers(self):
        """Toggle pin numbers via keyboard shortcut - WORKING"""
        if hasattr(self, 'pin_numbers_check') and self.pin_numbers_check:
            current_state = self.pin_numbers_check.isChecked()
            new_state = not current_state
            self.pin_numbers_check.setChecked(new_state)
            print(f"⌨️ Pin numbers toggled via Ctrl+P: {new_state}")
        else:
            print("⚠️ Pin numbers checkbox not found")

    def _toggle_component_labels(self):
        """Toggle component labels via keyboard shortcut - WORKING"""
        if hasattr(self, 'component_labels_check') and self.component_labels_check:
            current_state = self.component_labels_check.isChecked()
            new_state = not current_state
            self.component_labels_check.setChecked(new_state)
            print(f"⌨️ Component labels toggled via Ctrl+L: {new_state}")
        else:
            print("⚠️ Component labels checkbox not found")

    def _toggle_grid(self):
        """Toggle grid display - WORKING"""
        if hasattr(self, 'grid_check') and self.grid_check:
            current_state = self.grid_check.isChecked()
            new_state = not current_state
            self.grid_check.setChecked(new_state)
            print(f"⌨️ Grid toggled via Ctrl+G: {new_state}")
        else:
            print("⚠️ Grid checkbox not found")

    def _create_properties_dock(self):
        """Create properties dock"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        props_widget = QWidget()
        layout = QVBoxLayout(props_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # No selection message
        self.no_selection_label = QLabel("No component selected\n\nClick on a component to view its properties")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_selection_label.setStyleSheet("color: #888; font-style: italic; padding: 20px;")
        layout.addWidget(self.no_selection_label)

        layout.addStretch()
        scroll_area.setWidget(props_widget)

        self.properties_dock = QDockWidget("Properties", self)
        self.properties_dock.setWidget(scroll_area)
        self.properties_dock.setMinimumWidth(200)
        self.properties_dock.setMaximumWidth(300)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)

        print("✅ Properties dock created")

    def _create_docks(self):
        """Create dock widgets - SINGLE CLEAN IMPLEMENTATION"""
        print("Creating dock widgets...")

        # Component Palette Dock
        self._create_component_palette_dock()

        # Display Controls Dock (formerly left tools dock)
        self._create_display_controls_dock()

        # Layer Controls Dock
        self._create_layer_controls_dock()

        # Properties Dock
        self._create_properties_dock()

        # CAD Tools Dock
        self._create_cad_tools_dock()

        print("✓ All dock widgets created")

    def _create_display_controls_dock(self):
        """Create display controls dock - SINGLE IMPLEMENTATION"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        controls_widget = QWidget()
        layout = QVBoxLayout(controls_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # === DISPLAY SETTINGS GROUP ===
        display_group = QGroupBox("Display")
        display_layout = QVBoxLayout(display_group)

        # Pin numbers toggle
        self.pin_numbers_check = QCheckBox("Show Pin Numbers")
        self.pin_numbers_check.setChecked(True)
        self.pin_numbers_check.setObjectName("pin_numbers_check")
        self.pin_numbers_check.stateChanged.connect(self._pin_numbers_state_changed)
        display_layout.addWidget(self.pin_numbers_check)

        # Component labels toggle
        self.component_labels_check = QCheckBox("Show Component Labels")
        self.component_labels_check.setChecked(True)
        self.component_labels_check.setObjectName("component_labels_check")
        self.component_labels_check.stateChanged.connect(self._component_labels_state_changed)
        display_layout.addWidget(self.component_labels_check)

        layout.addWidget(display_group)

        # === GRID SETTINGS GROUP ===
        grid_group = QGroupBox("Grid Settings")
        grid_layout = QVBoxLayout(grid_group)

        # Grid visibility toggle
        self.grid_check = QCheckBox("Show Grid")
        self.grid_check.setChecked(True)
        self.grid_check.setObjectName("grid_check")
        self.grid_check.stateChanged.connect(self._grid_state_changed)
        grid_layout.addWidget(self.grid_check)

        # Snap to grid toggle
        self.snap_check = QCheckBox("Snap to Grid")
        self.snap_check.setChecked(True)
        self.snap_check.setObjectName("snap_check")
        self.snap_check.stateChanged.connect(self._snap_state_changed)
        grid_layout.addWidget(self.snap_check)

        # Grid size controls
        grid_size_layout = QHBoxLayout()
        grid_size_layout.addWidget(QLabel("Grid Size:"))
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(5)
        self.grid_size_spin.setMaximum(100)
        self.grid_size_spin.setValue(20)
        self.grid_size_spin.setSuffix(" px")
        self.grid_size_spin.valueChanged.connect(self._grid_size_changed)
        grid_size_layout.addWidget(self.grid_size_spin)
        grid_layout.addLayout(grid_size_layout)

        layout.addWidget(grid_group)

        # === VIEW CONTROLS GROUP ===
        view_group = QGroupBox("View Controls")
        view_layout = QVBoxLayout(view_group)

        # Zoom controls
        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(QLabel("Zoom:"))

        zoom_out_btn = QPushButton("-")
        zoom_out_btn.setMaximumWidth(30)
        zoom_out_btn.clicked.connect(self._zoom_out)
        zoom_layout.addWidget(zoom_out_btn)

        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(25)
        self.zoom_slider.setMaximum(400)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self._zoom_slider_changed)
        zoom_layout.addWidget(self.zoom_slider)

        zoom_in_btn = QPushButton("+")
        zoom_in_btn.setMaximumWidth(30)
        zoom_in_btn.clicked.connect(self._zoom_in)
        zoom_layout.addWidget(zoom_in_btn)

        view_layout.addLayout(zoom_layout)

        # Zoom level display
        self.zoom_display = QLabel("100%")
        self.zoom_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_display.setStyleSheet("font-weight: bold; color: #666;")
        view_layout.addWidget(self.zoom_display)

        # Fit buttons
        fit_layout = QHBoxLayout()
        fit_width_btn = QPushButton("Fit Width")
        fit_width_btn.clicked.connect(self._fit_width)
        fit_layout.addWidget(fit_width_btn)

        fit_all_btn = QPushButton("Fit All")
        fit_all_btn.clicked.connect(self._zoom_fit)
        fit_layout.addWidget(fit_all_btn)
        view_layout.addLayout(fit_layout)

        layout.addWidget(view_group)

        layout.addStretch()
        scroll_area.setWidget(controls_widget)

        # Create dock
        self.display_controls_dock = QDockWidget("Display Controls", self)
        self.display_controls_dock.setWidget(scroll_area)
        self.display_controls_dock.setMinimumWidth(200)
        self.display_controls_dock.setMaximumWidth(280)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.display_controls_dock)

        print("✓ Display controls dock created")

    def _create_layer_controls_dock(self):
        """Create clean working layer controls dock"""
        try:
            # Import backend layer manager
            from managers.layer_manager import LayerManager
            self.layer_manager = LayerManager()
            print("✓ Layer manager (backend) initialized")

        except ImportError as e:
            print(f"⚠️ Could not load LayerManager backend: {e}")
            self.layer_manager = None

        try:
            # Import UI layer controls
            from ui.layer_controls import LayerControls
            self.layer_controls = LayerControls()

            # Connect UI to backend
            if self.layer_manager:
                self.layer_controls.set_layer_manager(self.layer_manager)

            # Connect UI to canvas
            if hasattr(self, 'canvas') and self.canvas:
                self.layer_controls.set_canvas(self.canvas)

            # Connect layer signals to main window
            self.layer_controls.layerVisibilityChanged.connect(self._on_layer_visibility_changed)
            self.layer_controls.currentLayerChanged.connect(self._on_current_layer_changed)

            # Create dock
            self.layer_controls_dock = QDockWidget("Layers", self)
            self.layer_controls_dock.setWidget(self.layer_controls)
            self.layer_controls_dock.setMinimumWidth(220)
            self.layer_controls_dock.setMaximumWidth(300)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.layer_controls_dock)

            print("✓ Clean layer controls dock created with backend + frontend")

        except ImportError as e:
            print(f"❌ Could not load layer controls UI: {e}")
            print("❌ Layer controls required - check ui/layer_controls.py exists")

    def _on_layer_visibility_changed(self, layer_name, visible):
        """Handle layer visibility changes"""
        # Update canvas if available
        if hasattr(self.canvas, 'set_layer_visibility'):
            self.canvas.set_layer_visibility(layer_name, visible)

        # Update status bar if available
        if hasattr(self, 'status_manager') and self.status_manager:
            visible_count = sum(1 for layer in ["Components", "Connections", "PCB Traces", "Annotations", "Grid"]
                              if self.layer_controls.get_layer_visibility(layer))
            self.status_manager.show_temporary_message(f"Layer '{layer_name}' {'shown' if visible else 'hidden'} ({visible_count}/5 visible)")

        print(f"👁️ Layer '{layer_name}': {'visible' if visible else 'hidden'}")

    def _on_current_layer_changed(self, layer_name):
        """Handle current layer changes"""
        # Update canvas if available
        if hasattr(self.canvas, 'set_current_layer'):
            self.canvas.set_current_layer(layer_name)

        # Update status bar if available
        if hasattr(self, 'status_manager') and self.status_manager:
            self.status_manager.show_temporary_message(f"Active layer: {layer_name}")

        print(f"📄 Current layer: {layer_name}")

    def _update_layer_info(self):
        """Update layer controls with current canvas info"""
        if hasattr(self, 'layer_controls') and self.layer_controls:
            # Update component counts
            component_count = 0
            connection_count = 0

            if hasattr(self.canvas, 'get_component_count'):
                component_count = self.canvas.get_component_count()
            elif hasattr(self.canvas, 'components'):
                component_count = len(getattr(self.canvas, 'components', {}))

            if hasattr(self.canvas, 'get_connection_count'):
                connection_count = self.canvas.get_connection_count()
            elif hasattr(self.canvas, 'connections'):
                connection_count = len(getattr(self.canvas, 'connections', []))

            self.layer_controls.update_component_counts(component_count, connection_count)

    def _create_cad_tools_dock(self):
        """Create CAD tools dock - SINGLE IMPLEMENTATION"""
        try:
            from ui.cad_tools_panel import CADToolsPanel
            self.cad_tools_panel = CADToolsPanel()

            # Connect CAD tools to canvas if available
            if hasattr(self, 'canvas') and self.canvas:
                self.cad_tools_panel.set_canvas(self.canvas)

            # Create dock
            cad_dock = QDockWidget("CAD Tools", self)
            cad_dock.setWidget(self.cad_tools_panel)
            cad_dock.setMinimumWidth(200)
            cad_dock.setMaximumWidth(280)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, cad_dock)

            print("✓ Professional CAD tools dock created")

        except ImportError as e:
            print(f"❌ Could not load CAD tools: {e}")
            print("❌ CAD tools are required - check ui/cad_tools_panel.py")

    # === DISPLAY CONTROL EVENT HANDLERS ===
    def _pin_numbers_state_changed(self, state):
        """Handle pin numbers toggle"""
        enabled = state == Qt.CheckState.Checked.value
        if hasattr(self.canvas, 'set_pin_numbers_visible'):
            self.canvas.set_pin_numbers_visible(enabled)
        print(f"📍 Pin numbers: {'shown' if enabled else 'hidden'}")

    def _component_labels_state_changed(self, state):
        """Handle component labels toggle"""
        enabled = state == Qt.CheckState.Checked.value
        if hasattr(self.canvas, 'set_component_labels_visible'):
            self.canvas.set_component_labels_visible(enabled)
        print(f"🏷️ Component labels: {'shown' if enabled else 'hidden'}")

    def _grid_state_changed(self, state):
        """Handle grid toggle"""
        enabled = state == Qt.CheckState.Checked.value
        if hasattr(self.canvas, 'set_grid_visible'):
            self.canvas.set_grid_visible(enabled)
        print(f"📐 Grid: {'shown' if enabled else 'hidden'}")

    def _snap_state_changed(self, state):
        """Handle snap to grid toggle"""
        enabled = state == Qt.CheckState.Checked.value
        if hasattr(self.canvas, 'set_snap_to_grid'):
            self.canvas.set_snap_to_grid(enabled)
        print(f"🧲 Snap to grid: {'enabled' if enabled else 'disabled'}")

    def _grid_size_changed(self, size):
        """Handle grid size change"""
        if hasattr(self.canvas, 'set_grid_size'):
            self.canvas.set_grid_size(size)
        print(f"📏 Grid size: {size}px")

    def _zoom_slider_changed(self, value):
        """Handle zoom slider change"""
        zoom_factor = value / 100.0
        if hasattr(self.canvas, 'set_zoom'):
            self.canvas.set_zoom(zoom_factor)
        self.zoom_display.setText(f"{value}%")
        print(f"🔍 Zoom: {value}%")

    def _fit_width(self):
        """Fit canvas width to view"""
        if hasattr(self.canvas, 'fit_width'):
            self.canvas.fit_width()
        print("↔️ Fit width")


    def _create_menu_bar(self): #new
        """Create menu bar - SINGLE IMPLEMENTATION"""
        try:
            from ui.menu_bar import RetroEmulatorMenuBar
            self.menu_manager = RetroEmulatorMenuBar(self)
            self.setMenuBar(self.menu_manager)

            # Connect menu signals to main window methods
            self._connect_menu_signals()

            # Add custom pin numbers menu items
            self._add_pin_numbers_to_view_menu()

            print("✓ Professional menu bar created")

        except ImportError as e:
            print(f"❌ Could not load menu bar: {e}")
            print("❌ Menu bar is required - check ui/menu_bar.py")
            # Don't create fallback - require proper menu bar

    def _connect_menu_signals(self): #new
        """Connect menu bar signals to main window methods"""
        if not hasattr(self, 'menu_manager'):
            return

        signals = self.menu_manager.signals

        # File menu connections
        signals.newProject.connect(self._new_project)
        signals.openProject.connect(self._open_project_file)
        signals.saveProject.connect(self._save_project)
        signals.saveProjectAs.connect(self._save_project_as)
        signals.exitApplication.connect(self.close)

        # Edit menu connections
        signals.undo.connect(self._undo)
        signals.redo.connect(self._redo)
        signals.cut.connect(self._cut)
        signals.copy.connect(self._copy)
        signals.paste.connect(self._paste)
        signals.delete.connect(self._delete)
        signals.selectAll.connect(self._select_all)

        # View menu connections
        signals.zoomIn.connect(self._zoom_in)
        signals.zoomOut.connect(self._zoom_out)
        signals.zoomFit.connect(self._zoom_fit)
        signals.zoomActual.connect(self._zoom_actual)
        signals.toggleGrid.connect(self._toggle_grid)

        # Simulation menu connections
        signals.startSimulation.connect(self._start_simulation)
        signals.stopSimulation.connect(self._stop_simulation)
        signals.pauseSimulation.connect(self._pause_simulation)
        signals.resetSimulation.connect(self._reset_simulation)

        print("✓ Menu signals connected")

    def _open_project_file(self, file_path):
        """Open project from file path (called by menu)"""
        try:
            if self.project_manager:
                self.project_manager.open_project(file_path)
                self._update_window_title()
                print(f"✓ Opened project: {file_path}")
            else:
                print("⚠️ No project manager available")
        except Exception as e:
            print(f"❌ Failed to open project: {e}")

    def _save_project_as(self, file_path):
        """Save project as (called by menu)"""
        try:
            if self.project_manager:
                self.project_manager.save_project(file_path)
                self._update_window_title()
                print(f"✓ Saved project as: {file_path}")
            else:
                print("⚠️ No project manager available")
        except Exception as e:
            print(f"❌ Failed to save project: {e}")

    # ADD MISSING MENU ACTION METHODS
    def _cut(self):
        """Cut selected items"""
        if hasattr(self.canvas, 'cut_selected'):
            self.canvas.cut_selected()
        print("Cut action")

    def _copy(self):
        """Copy selected items"""
        if hasattr(self.canvas, 'copy_selected'):
            self.canvas.copy_selected()
        print("Copy action")

    def _paste(self):
        """Paste from clipboard"""
        if hasattr(self.canvas, 'paste'):
            self.canvas.paste()
        print("Paste action")

    def _delete(self):
        """Delete selected items"""
        if hasattr(self.canvas, 'delete_selected'):
            self.canvas.delete_selected()
        print("Delete action")

    def _select_all(self):
        """Select all items"""
        if hasattr(self.canvas, 'select_all'):
            self.canvas.select_all()
        print("Select all action")

    def _zoom_actual(self):
        """Zoom to actual size (100%)"""
        if hasattr(self.canvas, 'zoom_actual'):
            self.canvas.zoom_actual()
        else:
            print("Zoom actual (100%)")

    def _pause_simulation(self):
        """Pause simulation"""
        if self.simulation_engine:
            self.simulation_engine.pause()
        print("Simulation paused")

    def _reset_simulation(self):
        """Reset simulation"""
        if self.simulation_engine:
            self.simulation_engine.reset()
        print("Simulation reset")


    def _create_status_bar(self):
        """Create status bar"""
        try:
            from ui.status_bar import StatusBarManager
            self.status_manager = StatusBarManager(self)
            print("✓ Status bar created")
        except ImportError:
            print("⚠️ Status bar not available - using fallback")
            self._create_fallback_status_bar()

    def _create_status_bar(self):
        """Create status bar - SINGLE IMPLEMENTATION"""
        try:
            from ui.status_bar import create_status_bar
            self.status_manager = create_status_bar(self)

            # Connect status bar signals
            self._connect_status_bar_signals()

            print("✓ Professional status bar created")

        except ImportError as e:
            print(f"❌ Could not load status bar: {e}")
            print("❌ Status bar is required - check ui/status_bar.py")
            # Don't create fallback - require proper status bar

    def _connect_status_bar_signals(self):
        """Connect status bar signals to main window methods"""
        if not hasattr(self, 'status_manager'):
            return

        # Connect status bar signals
        self.status_manager.zoomChanged.connect(self._on_status_zoom_changed)
        self.status_manager.gridToggled.connect(self._on_status_grid_toggled)
        self.status_manager.snapToggled.connect(self._on_status_snap_toggled)
        self.status_manager.unitsChanged.connect(self._on_status_units_changed)
        self.status_manager.coordinatesClicked.connect(self._on_coordinates_clicked)

        print("✓ Status bar signals connected")

    def _on_status_zoom_changed(self, zoom_level):
        """Handle zoom change from status bar"""
        if hasattr(self.canvas, 'set_zoom'):
            if zoom_level == -1:  # Fit to window
                self.canvas.zoom_fit()
            else:
                self.canvas.set_zoom(zoom_level / 100.0)
        print(f"Zoom changed to: {zoom_level}%")

    def _on_status_grid_toggled(self, visible):
        """Handle grid toggle from status bar"""
        if hasattr(self.canvas, 'set_grid_visible'):
            self.canvas.set_grid_visible(visible)
        print(f"Grid toggled: {visible}")

    def _on_status_snap_toggled(self, enabled):
        """Handle snap toggle from status bar"""
        if hasattr(self.canvas, 'set_snap_to_grid'):
            self.canvas.set_snap_to_grid(enabled)
        print(f"Snap toggled: {enabled}")

    def _on_status_units_changed(self, units):
        """Handle units change from status bar"""
        # Update canvas units
        if hasattr(self.canvas, 'set_units'):
            self.canvas.set_units(units)
        print(f"Units changed to: {units}")

    def _on_coordinates_clicked(self):
        """Handle coordinates label clicked"""
        # Could toggle between different coordinate systems
        print("Coordinates clicked - could toggle coordinate system")

    # ADD STATUS BAR UPDATE METHODS
    def _update_status_counts(self):
        """Update component and connection counts in status bar"""
        if hasattr(self, 'status_manager'):
            # Count components on canvas
            component_count = 0
            connection_count = 0

            if hasattr(self.canvas, 'get_component_count'):
                component_count = self.canvas.get_component_count()
            elif hasattr(self.canvas, 'components'):
                component_count = len(self.canvas.components)

            if hasattr(self.canvas, 'get_connection_count'):
                connection_count = self.canvas.get_connection_count()
            elif hasattr(self.canvas, 'connections'):
                connection_count = len(self.canvas.connections)

            self.status_manager.set_component_count(component_count)
            self.status_manager.set_connection_count(connection_count)

    def _update_mouse_coordinates(self, x, y):
        """Update mouse coordinates in status bar"""
        if hasattr(self, 'status_manager'):
            self.status_manager.set_coordinates(x, y)

    def _update_zoom_display(self, zoom_level):
        """Update zoom display in status bar"""
        if hasattr(self, 'status_manager'):
            self.status_manager.set_zoom(zoom_level * 100)

    def _update_project_status(self, project_name=None, modified=False):
        """Update project status in status bar"""
        if hasattr(self, 'status_manager'):
            if project_name:
                self.status_manager.set_project_name(project_name)
            self.status_manager.set_project_modified(modified)

    def _update_simulation_status(self, running=False, info=""):
        """Update simulation status in status bar"""
        if hasattr(self, 'status_manager'):
            self.status_manager.set_simulation_status(running, info)


    def _setup_connections(self):
        """Setup signal connections"""
        print("Setting up connections...")
        print("✓ Connections setup complete")

    def _create_toolbars(self):
        """Create toolbars"""
        from ui.toolbar import create_toolbars
        self.main_toolbar, self.component_toolbar = create_toolbars(self)

        # Connect toolbar signals
        self.main_toolbar.new_project.connect(self._new_project)
        self.main_toolbar.open_project.connect(self._open_project)
        self.main_toolbar.save_project.connect(self._save_project)
        # ... connect other signals as needed

        print("✓ Toolbars created and connected")


    def _setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        print("Setting up hotkeys...")

        self._add_pin_numbers_hotkeys()
        # Standard shortcuts
        QShortcut(QKeySequence('Ctrl+F'), self, self._show_search_dialog)
        QShortcut(QKeySequence('F1'), self, self._show_shortcuts)
        QShortcut(QKeySequence('Escape'), self, self._cancel_current_operation)

        # Tool shortcuts
        QShortcut(QKeySequence('S'), self, lambda: self._set_tool('select'))
        QShortcut(QKeySequence('P'), self, lambda: self._set_tool('place'))
        QShortcut(QKeySequence('W'), self, lambda: self._set_tool('wire'))
        QShortcut(QKeySequence('T'), self, lambda: self._set_tool('trace'))
        QShortcut(QKeySequence('V'), self, lambda: self._set_tool('via'))

        # View shortcuts
        QShortcut(QKeySequence('Ctrl+G'), self, self._toggle_grid)

        print("✓ Hotkeys setup complete")

    def _post_init_setup(self):
        """Post-initialization setup"""
        print("Post-initialization setup...")

        if self.canvas:
            self.canvas.setFocus()

        self._update_ui_state()
        print("✓ Post-initialization complete")

    # System integration methods
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

    def _setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        print("Setting up hotkeys...")

        # Standard shortcuts
        QShortcut(QKeySequence('Ctrl+F'), self, self._show_search_dialog)
        QShortcut(QKeySequence('F1'), self, self._show_shortcuts)
        QShortcut(QKeySequence('Escape'), self, self._cancel_current_operation)

        # Tool shortcuts - with working references
        QShortcut(QKeySequence('S'), self, lambda: self._set_tool_direct('select'))
        QShortcut(QKeySequence('P'), self, lambda: self._set_tool_direct('place'))
        QShortcut(QKeySequence('W'), self, lambda: self._set_tool_direct('wire'))
        QShortcut(QKeySequence('T'), self, lambda: self._set_tool_direct('trace'))
        QShortcut(QKeySequence('V'), self, lambda: self._set_tool_direct('via'))
        QShortcut(QKeySequence('A'), self, lambda: self._set_tool_direct('pad'))
        QShortcut(QKeySequence('M'), self, lambda: self._set_tool_direct('measure'))
        QShortcut(QKeySequence('Delete'), self, lambda: self._set_tool_direct('delete'))

        # View shortcuts
        QShortcut(QKeySequence('Ctrl+G'), self, self._toggle_grid)
        
        # Display shortcuts - WORKING VERSIONS
        QShortcut(QKeySequence('Ctrl+P'), self, self._toggle_pin_numbers)
        QShortcut(QKeySequence('Ctrl+L'), self, self._toggle_component_labels)

        # Zoom shortcuts
        QShortcut(QKeySequence('Ctrl++'), self, self._zoom_in)
        QShortcut(QKeySequence('Ctrl+-'), self, self._zoom_out)
        QShortcut(QKeySequence('Ctrl+0'), self, self._zoom_fit)

        print("✓ Enhanced hotkeys setup complete with working references")

    # Project operations
    def _new_project(self):
        """Create new project"""
        if self.canvas and hasattr(self.canvas, 'clear'):
            self.canvas.clear()
        print("📁 New project created")

    def _open_project(self):
        """Open project"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Projects (*.xset);;All Files (*)")
        if file_path:
            print(f"📁 Opening project: {file_path}")

    def _save_project(self):
        """Save project"""
        print("💾 Saving project")

    def _undo(self):
        """Undo operation"""
        print("↶ Undo")

    def _redo(self):
        """Redo operation"""
        print("↷ Redo")

    # View operations
    def _zoom_in(self):
        """Zoom in"""
        if self.canvas and hasattr(self.canvas, 'zoom_in'):
            self.canvas.zoom_in()

    def _zoom_out(self):
        """Zoom out"""
        if self.canvas and hasattr(self.canvas, 'zoom_out'):
            self.canvas.zoom_out()

    def _zoom_fit(self):
        """Zoom to fit"""
        if self.canvas and hasattr(self.canvas, 'zoom_fit'):
            self.canvas.zoom_fit()

    def _toggle_grid(self):
        """Toggle grid display"""
        if self.canvas and hasattr(self.canvas, 'grid_visible'):
            enabled = not self.canvas.grid_visible
            self.canvas.set_grid_visible(enabled)

    # Simulation operations
    def _start_simulation(self):
        """Start simulation"""
        print("▶️ Simulation started")

    def _stop_simulation(self):
        """Stop simulation"""
        print("⏹️ Simulation stopped")

    # Dialog operations
    def _show_search_dialog(self):
        """Show search dialog"""
        from PyQt6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, 'Search', 'Search for:')
        if ok and text:
            print(f"🔍 Searching for: {text}")

    def _show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts_text = """
<b>Enhanced Keyboard Shortcuts</b><br><br>

<b>🔧 Tools:</b><br>
<b>S</b> - Select Tool<br>
<b>P</b> - Place Component<br>
<b>W</b> - Wire Tool<br>
<b>T</b> - Trace Tool<br>
<b>V</b> - Via Tool<br><br>

<b>👁️ Display Controls:</b><br>
<b>Ctrl+P</b> - Toggle Pin Numbers<br>
<b>Ctrl+L</b> - Toggle Component Labels<br>
<b>Ctrl+G</b> - Toggle Grid<br><br>

<b>🔍 View:</b><br>
<b>Ctrl++</b> - Zoom In<br>
<b>Ctrl+-</b> - Zoom Out<br>
<b>Ctrl+0</b> - Zoom Fit<br><br>

<b>📁 File:</b><br>
<b>Ctrl+N</b> - New Project<br>
<b>Ctrl+O</b> - Open Project<br>
<b>Ctrl+S</b> - Save Project<br><br>

<b>✏️ Edit:</b><br>
<b>Ctrl+Z</b> - Undo<br>
<b>Ctrl+Y</b> - Redo<br><br>

<b>🎮 Simulation:</b><br>
<b>F5</b> - Start Simulation<br><br>

<b>🔍 Other:</b><br>
<b>Ctrl+F</b> - Search Components<br>
<b>F1</b> - This Help<br>
<b>Esc</b> - Cancel Operation<br><br>

<b>💡 Tips:</b><br>
• Pin numbers appear outside the chip edges<br>
• Text rotates on tall chips for better readability<br>
• Use display controls to toggle visibility<br>
• All settings are remembered during session
        """
        QMessageBox.information(self, "Enhanced Keyboard Shortcuts", shortcuts_text)

    def _cancel_current_operation(self):
        """Cancel current operation"""
        self._set_tool('select')
        print("❌ Operation cancelled")

    # Update methods
    def _update_window_title(self):
        """Update window title"""
        title = "Visual Retro System Emulator Builder - Enhanced Edition"
        if self.current_project_path:
            title += f" - {os.path.basename(self.current_project_path)}"
        if self.is_modified:
            title += " *"
        self.setWindowTitle(title)

    def _update_status_counts(self):
        """Update status bar counts"""
        if hasattr(self, 'component_count_label') and self.component_count_label:
            component_count = 0
            if self.canvas and hasattr(self.canvas, 'components'):
                component_count = len(self.canvas.components)
            self.component_count_label.setText(f"Components: {component_count}")

    def _update_ui_state(self):
        """Update UI state"""
        self._update_status_counts()
        if hasattr(self, 'tool_label') and self.tool_label:
            self.tool_label.setText(f"Tool: {self.current_tool.title()}")

    def refresh_component_palette(self):
        """Refresh component palette"""
        print("✓ Component palette refreshed")

    # Event handlers
    def closeEvent(self, event):
        """Handle window close"""
        event.accept()
        print("👋 Application closed")

    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        """Handle key press events"""
        super().keyPressEvent(event)

# Export
__all__ = ['MainWindow']

# Test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print("🚀 Enhanced Main Window running with realistic chip rendering!")
    sys.exit(app.exec())
