#!/usr/bin/env python3
"""
X-Seti - June23 2025 - Enhanced Canvas with ALL Features Merged
Visual Retro System Emulator Builder - Complete canvas with enhanced functionality
"""
#this belongs in ui/canvas.py

import os
import sys
from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox,
                           QCheckBox, QSlider, QButtonGroup, QFrame, QColorDialog,
                           QToolButton, QMenu, QWidgetAction, QDialog, QGridLayout,
                           QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem,
                           QGraphicsPixmapItem, QApplication, QFileDialog,
                           QMessageBox, QFormLayout)
from PyQt6.QtCore import (Qt, QPointF, QRectF, QTimer, pyqtSignal, QPropertyAnimation,
                        QEasingCurve, QParallelAnimationGroup, QPoint)
from PyQt6.QtGui import (QPainter, QPen, QBrush, QColor, QPixmap, QFont, QIcon,
                       QPainterPath, QMouseEvent, QWheelEvent, QKeyEvent, QCursor,
                       QShortcut, QKeySequence, QAction, QPolygonF)

# Try PyQt6 imports
PYQT6_AVAILABLE = True
try:
    from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
    from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal
    from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
    print("✓ PyQt6 imports successful for Enhanced Canvas")
except ImportError as e:
    print(f"❌ PyQt6 import failed in Enhanced Canvas: {e}")
    PYQT6_AVAILABLE = False


class ComponentItem(QGraphicsItem):
    """Enhanced visual component item for the canvas"""
    
    def __init__(self, name, category, package_type="DIP-40", parent=None):
        super().__init__(parent)
        
        self.name = name
        self.category = category
        self.package_type = package_type
        self.selected = False
        
        # Make item selectable and movable
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Component dimensions based on package type
        self.width, self.height = self._get_package_dimensions(package_type)
        
        # Pin configuration
        self.pins = self._get_pin_configuration(package_type)
        
        # Visual settings
        self.show_pins = True
        self.show_labels = True
        
        print(f"🔧 Component created: {name} ({package_type})")
    
    def _get_package_dimensions(self, package_type):
        """Get component dimensions based on package type"""
        dimensions = {
            'DIP-8': (20, 60),
            'DIP-14': (20, 80),
            'DIP-16': (20, 90),
            'DIP-18': (20, 100),
            'DIP-20': (20, 110),
            'DIP-24': (25, 130),
            'DIP-28': (25, 150),
            'DIP-40': (30, 200),
            'DIP-64': (35, 320),
            'QFP-44': (80, 80),
            'QFP-68': (100, 100),
            'PLCC-44': (75, 75),
            'PGA-68': (90, 90)
        }
        return dimensions.get(package_type, (30, 200))  # Default DIP-40
    
    def _get_pin_configuration(self, package_type):
        """Get pin configuration for package type"""
        pin_count = int(package_type.split('-')[-1]) if '-' in package_type else 40
        
        if 'DIP' in package_type:
            # DIP packages - pins on two sides
            pins_per_side = pin_count // 2
            pins = []
            
            # Left side pins (1 to pins_per_side)
            for i in range(pins_per_side):
                y_pos = (i + 0.5) * (self.height / pins_per_side)
                pins.append({'number': i + 1, 'x': 0, 'y': y_pos, 'side': 'left'})
            
            # Right side pins (pins_per_side+1 to pin_count)
            for i in range(pins_per_side):
                y_pos = (pins_per_side - i - 0.5) * (self.height / pins_per_side)
                pins.append({'number': pins_per_side + i + 1, 'x': self.width, 'y': y_pos, 'side': 'right'})
            
            return pins
        
        elif 'QFP' in package_type or 'PLCC' in package_type:
            # Quad packages - pins on all four sides
            pins_per_side = pin_count // 4
            pins = []
            
            # Top side
            for i in range(pins_per_side):
                x_pos = (i + 0.5) * (self.width / pins_per_side)
                pins.append({'number': i + 1, 'x': x_pos, 'y': 0, 'side': 'top'})
            
            # Right side
            for i in range(pins_per_side):
                y_pos = (i + 0.5) * (self.height / pins_per_side)
                pins.append({'number': pins_per_side + i + 1, 'x': self.width, 'y': y_pos, 'side': 'right'})
            
            # Bottom side
            for i in range(pins_per_side):
                x_pos = (pins_per_side - i - 0.5) * (self.width / pins_per_side)
                pins.append({'number': 2 * pins_per_side + i + 1, 'x': x_pos, 'y': self.height, 'side': 'bottom'})
            
            # Left side
            for i in range(pins_per_side):
                y_pos = (pins_per_side - i - 0.5) * (self.height / pins_per_side)
                pins.append({'number': 3 * pins_per_side + i + 1, 'x': 0, 'y': y_pos, 'side': 'left'})
            
            return pins
        
        return []  # Default no pins
    
    def boundingRect(self):
        """Return the bounding rectangle of the component"""
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget):
        """Paint the component"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Component body
        body_color = QColor(40, 40, 40) if not self.isSelected() else QColor(60, 120, 200)
        painter.fillRect(self.boundingRect(), body_color)
        
        # Component outline
        outline_pen = QPen(QColor(200, 200, 200), 2)
        painter.setPen(outline_pen)
        painter.drawRect(self.boundingRect())
        
        # Component name
        if self.show_labels:
            painter.setPen(QColor(255, 255, 255))
            font = QFont("Arial", 8)
            painter.setFont(font)
            
            # Draw name in center
            text_rect = self.boundingRect()
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.name)
        
        # Draw pins
        if self.show_pins:
            self._draw_pins(painter)
    
    def _draw_pins(self, painter):
        """Draw component pins"""
        pin_size = 4
        pin_color = QColor(255, 215, 0)  # Gold color for pins
        
        painter.setBrush(QBrush(pin_color))
        painter.setPen(QPen(QColor(200, 160, 0), 1))
        
        for pin in self.pins:
            # Draw pin circle
            pin_rect = QRectF(pin['x'] - pin_size/2, pin['y'] - pin_size/2, pin_size, pin_size)
            painter.drawEllipse(pin_rect)
            
            # Draw pin number (for debugging/development)
            if len(self.pins) <= 40:  # Only show numbers for smaller packages
                painter.setPen(QColor(255, 255, 255))
                font = QFont("Arial", 6)
                painter.setFont(font)
                number_rect = QRectF(pin['x'] - 8, pin['y'] - 8, 16, 16)
                painter.drawText(number_rect, Qt.AlignmentFlag.AlignCenter, str(pin['number']))
                painter.setPen(QPen(QColor(200, 160, 0), 1))


class GridSettingsDialog(QDialog):
    """Advanced grid settings dialog"""
    
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.setWindowTitle("Grid Settings")
        self.setModal(True)
        self.resize(400, 500)
        
        # Current settings
        self.grid_settings = current_settings or {}
        
        # Colors
        self.grid_color = self.grid_settings.get('grid_color', QColor(100, 100, 100, 100))
        self.bg_color = self.grid_settings.get('bg_color', QColor(40, 44, 52))
        
        self._setup_ui()
        self._load_current_settings()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Grid visibility group
        grid_group = QGroupBox("Grid Display")
        grid_layout = QFormLayout(grid_group)
        
        self.show_grid = QCheckBox()
        self.snap_to_grid = QCheckBox()
        
        grid_layout.addRow("Show Grid:", self.show_grid)
        grid_layout.addRow("Snap to Grid:", self.snap_to_grid)
        
        layout.addWidget(grid_group)
        
        # Grid style group
        style_group = QGroupBox("Grid Style")
        style_layout = QFormLayout(style_group)
        
        self.grid_style = QComboBox()
        self.grid_style.addItems(["Dotted", "Solid Lines", "Grid Points", "Cross Hatch"])
        
        self.grid_spacing = QSpinBox()
        self.grid_spacing.setRange(5, 100)
        self.grid_spacing.setSuffix(" px")
        
        style_layout.addRow("Grid Style:", self.grid_style)
        style_layout.addRow("Grid Spacing:", self.grid_spacing)
        
        layout.addWidget(style_group)
        
        # Color group
        color_group = QGroupBox("Colors")
        color_layout = QFormLayout(color_group)
        
        self.grid_color_btn = QPushButton()
        self.grid_color_btn.setFixedHeight(30)
        self.grid_color_btn.clicked.connect(self._choose_grid_color)
        
        self.bg_color_btn = QPushButton()
        self.bg_color_btn.setFixedHeight(30)
        self.bg_color_btn.clicked.connect(self._choose_bg_color)
        
        color_layout.addRow("Grid Color:", self.grid_color_btn)
        color_layout.addRow("Background Color:", self.bg_color_btn)
        
        layout.addWidget(color_group)
        
        # Background pattern group
        bg_group = QGroupBox("Background")
        bg_layout = QFormLayout(bg_group)
        
        self.bg_type = QComboBox()
        self.bg_type.addItems(["Solid Color", "Paper", "Grid Paper", "Dots", "Stripes"])
        
        bg_layout.addRow("Background Type:", self.bg_type)
        
        layout.addWidget(bg_group)
        
        # Additional options
        options_group = QGroupBox("Additional Options")
        options_layout = QFormLayout(options_group)
        
        self.show_margins = QCheckBox()
        self.show_rulers = QCheckBox()
        
        options_layout.addRow("Show Margins:", self.show_margins)
        options_layout.addRow("Show Rulers:", self.show_rulers)
        
        layout.addWidget(options_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self._reset_to_defaults)
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Update color buttons
        self.update_color_button()
        self.update_bg_color_button()
    
    def _connect_signals(self):
        """Connect signals"""
        # Enable/disable grid spacing when grid is toggled
        self.show_grid.toggled.connect(lambda checked: self.grid_spacing.setEnabled(checked))
        self.show_grid.toggled.connect(lambda checked: self.grid_style.setEnabled(checked))
    
    def _choose_grid_color(self):
        """Choose grid color"""
        color = QColorDialog.getColor(self.grid_color, self, "Choose Grid Color")
        if color.isValid():
            self.grid_color = color
            self.update_color_button()
    
    def _choose_bg_color(self):
        """Choose background color"""
        color = QColorDialog.getColor(self.bg_color, self, "Choose Background Color")
        if color.isValid():
            self.bg_color = color
            self.update_bg_color_button()
    
    def update_color_button(self):
        """Update grid color button appearance"""
        self.grid_color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.grid_color.name()};
                border: 2px solid #555;
            }}
        """)
        self.grid_color_btn.setText(f"Grid: {self.grid_color.name()}")
    
    def update_bg_color_button(self):
        """Update background color button appearance"""
        self.bg_color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.bg_color.name()};
                border: 2px solid #555;
                color: white;
            }}
        """)
        self.bg_color_btn.setText(f"Background: {self.bg_color.name()}")
    
    def _reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.show_grid.setChecked(True)
        self.snap_to_grid.setChecked(True)
        self.grid_style.setCurrentText("Dotted")
        self.grid_spacing.setValue(25)
        self.bg_type.setCurrentText("Solid Color")
        self.show_margins.setChecked(False)
        self.show_rulers.setChecked(False)
        
        # Reset colors
        self.grid_color = QColor(100, 100, 100, 100)
        self.bg_color = QColor(40, 44, 52)
        self.update_color_button()
        self.update_bg_color_button()
    
    def get_settings(self):
        """Get current settings"""
        return {
            'show_grid': self.show_grid.isChecked(),
            'snap_to_grid': self.snap_to_grid.isChecked(),
            'grid_style': self.grid_style.currentText(),
            'grid_spacing': self.grid_spacing.value(),
            'grid_color': self.grid_color,
            'bg_type': self.bg_type.currentText(),
            'bg_color': self.bg_color,
            'show_margins': self.show_margins.isChecked(),
            'show_rulers': self.show_rulers.isChecked()
        }
    
    def _load_current_settings(self):
        """Load current settings into dialog"""
        try:
            # Disable signals temporarily
            self.show_grid.blockSignals(True)
            self.snap_to_grid.blockSignals(True)
            self.grid_style.blockSignals(True)
            self.grid_spacing.blockSignals(True)
            self.bg_type.blockSignals(True)
            self.show_margins.blockSignals(True)
            self.show_rulers.blockSignals(True)
            
            # Load settings
            self.show_grid.setChecked(self.grid_settings.get('show_grid', True))
            self.snap_to_grid.setChecked(self.grid_settings.get('snap_to_grid', True))
            self.grid_style.setCurrentText(str(self.grid_settings.get('grid_style', 'Dotted')))
            self.grid_spacing.setValue(self.grid_settings.get('grid_spacing', 25))
            self.bg_type.setCurrentText(self.grid_settings.get('bg_type', 'Solid Color'))
            self.show_margins.setChecked(self.grid_settings.get('show_margins', False))
            self.show_rulers.setChecked(self.grid_settings.get('show_rulers', False))
            
            # Load colors
            if 'grid_color' in self.grid_settings:
                self.grid_color = self.grid_settings['grid_color']
                self.update_color_button()
            
            if 'bg_color' in self.grid_settings:
                self.bg_color = self.grid_settings['bg_color']
                self.update_bg_color_button()
            
            # Re-enable signals
            self.show_grid.blockSignals(False)
            self.snap_to_grid.blockSignals(False)
            self.grid_style.blockSignals(False)
            self.grid_spacing.blockSignals(False)
            self.bg_type.blockSignals(False)
            self.show_margins.blockSignals(False)
            self.show_rulers.blockSignals(False)
            
            print("✅ Grid dialog loaded with current settings")
            
        except Exception as e:
            print(f"⚠️ Error loading settings into dialog: {e}")


if PYQT6_AVAILABLE:

    class PCBCanvas(QGraphicsView):
        """Enhanced PCB Canvas with complete functionality"""
        
        # Signals
        component_added = pyqtSignal(str, str, QPointF)  # category, component, position
        component_selected = pyqtSignal(object)
        zoom_changed = pyqtSignal(float)
        
        def __init__(self, parent=None):
            super().__init__(parent)
            
            # Initialize scene
            self.scene = QGraphicsScene()
            self.setScene(self.scene)
            
            # Enhanced grid settings
            self.grid_settings = {
                'show_grid': True,
                'snap_to_grid': True,
                'grid_style': 'Dotted',
                'grid_spacing': 25,
                'grid_color': QColor(100, 100, 100, 100),
                'bg_type': 'Solid Color',
                'bg_color': QColor(40, 44, 52),
                'show_margins': False,
                'show_rulers': False
            }
            
            # Canvas state
            self.current_tool = 'select'
            self.zoom_factor = 1.0
            self.components = {}
            self.connections = []
            
            # Enhanced undo/redo functionality
            self.undo_stack = []
            self.redo_stack = []
            self.max_undo_levels = 50
            
            # Visual settings
            self.show_pin_numbers = True
            self.show_component_labels = True
            
            # Load saved grid settings
            self.load_grid_settings()
            
            # Setup canvas
            self.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            self.setMouseTracking(True)
            self.setAcceptDrops(True)
            
            # Setup scene
            self.scene.setSceneRect(-2000, -2000, 4000, 4000)
            
            # Apply background
            self.update_background()
            
            print("✅ Enhanced PCB Canvas initialized")
        
        def load_grid_settings(self):
            """Load grid settings from file"""
            settings_file = "canvas_grid_settings.json"
            try:
                if os.path.exists(settings_file):
                    import json
                    with open(settings_file, 'r') as f:
                        saved_settings = json.load(f)
                    
                    # Convert color data back to QColor objects
                    if 'grid_color' in saved_settings:
                        color_data = saved_settings['grid_color']
                        if isinstance(color_data, list) and len(color_data) >= 3:
                            self.grid_settings['grid_color'] = QColor(*color_data[:4])
                    
                    if 'bg_color' in saved_settings:
                        color_data = saved_settings['bg_color']
                        if isinstance(color_data, list) and len(color_data) >= 3:
                            self.grid_settings['bg_color'] = QColor(*color_data[:4])
                    
                    # Update other settings
                    for key in ['show_grid', 'snap_to_grid', 'grid_style', 'grid_spacing', 'bg_type', 'show_margins', 'show_rulers']:
                        if key in saved_settings:
                            self.grid_settings[key] = saved_settings[key]
                    
                    print("✅ Grid settings loaded from file")
            
            except Exception as e:
                print(f"⚠️ Could not load grid settings: {e}")
        
        def save_grid_settings(self):
            """Save grid settings to file"""
            settings_file = "canvas_grid_settings.json"
            try:
                import json
                
                # Convert QColor objects to serializable format
                save_data = self.grid_settings.copy()
                save_data['grid_color'] = [
                    self.grid_settings['grid_color'].red(),
                    self.grid_settings['grid_color'].green(),
                    self.grid_settings['grid_color'].blue(),
                    self.grid_settings['grid_color'].alpha()
                ]
                save_data['bg_color'] = [
                    self.grid_settings['bg_color'].red(),
                    self.grid_settings['bg_color'].green(),
                    self.grid_settings['bg_color'].blue(),
                    self.grid_settings['bg_color'].alpha()
                ]
                
                with open(settings_file, 'w') as f:
                    json.dump(save_data, f, indent=2)
                
                print("✅ Grid settings saved to file")
            
            except Exception as e:
                print(f"⚠️ Could not save grid settings: {e}")
        
        def update_background(self):
            """Update canvas background and grid"""
            # Set background color
            self.setBackgroundBrush(QBrush(self.grid_settings['bg_color']))
            
            # Force scene update
            self.scene.update()
            self.viewport().update()
        
        def drawBackground(self, painter, rect):
            """Draw custom background with grid"""
            super().drawBackground(painter, rect)
            
            if not self.grid_settings['show_grid']:
                return
            
            # Grid settings
            grid_spacing = self.grid_settings['grid_spacing']
            grid_color = self.grid_settings['grid_color']
            grid_style = self.grid_settings['grid_style']
            
            # Set up painter
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
            
            # Draw grid based on style
            if grid_style == "Dotted":
                self._draw_dotted_grid(painter, rect, grid_spacing, grid_color)
            elif grid_style == "Solid Lines":
                self._draw_line_grid(painter, rect, grid_spacing, grid_color)
            elif grid_style == "Grid Points":
                self._draw_point_grid(painter, rect, grid_spacing, grid_color)
            elif grid_style == "Cross Hatch":
                self._draw_crosshatch_grid(painter, rect, grid_spacing, grid_color)
        
        def _draw_dotted_grid(self, painter, rect, spacing, color):
            """Draw dotted grid"""
            pen = QPen(color, 1, Qt.PenStyle.DotLine)
            painter.setPen(pen)
            
            # Vertical lines
            start_x = int(rect.left() / spacing) * spacing
            for x in range(int(start_x), int(rect.right()) + spacing, spacing):
                painter.drawLine(x, rect.top(), x, rect.bottom())
            
            # Horizontal lines
            start_y = int(rect.top() / spacing) * spacing
            for y in range(int(start_y), int(rect.bottom()) + spacing, spacing):
                painter.drawLine(rect.left(), y, rect.right(), y)
        
        def _draw_line_grid(self, painter, rect, spacing, color):
            """Draw solid line grid"""
            pen = QPen(color, 1, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            
            # Vertical lines
            start_x = int(rect.left() / spacing) * spacing
            for x in range(int(start_x), int(rect.right()) + spacing, spacing):
                painter.drawLine(x, rect.top(), x, rect.bottom())
            
            # Horizontal lines
            start_y = int(rect.top() / spacing) * spacing
            for y in range(int(start_y), int(rect.bottom()) + spacing, spacing):
                painter.drawLine(rect.left(), y, rect.right(), y)
        
        def _draw_point_grid(self, painter, rect, spacing, color):
            """Draw point grid"""
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            point_size = 2
            
            start_x = int(rect.left() / spacing) * spacing
            start_y = int(rect.top() / spacing) * spacing
            
            for x in range(int(start_x), int(rect.right()) + spacing, spacing):
                for y in range(int(start_y), int(rect.bottom()) + spacing, spacing):
                    painter.drawEllipse(x - point_size/2, y - point_size/2, point_size, point_size)
        
        def _draw_crosshatch_grid(self, painter, rect, spacing, color):
            """Draw crosshatch grid"""
            pen = QPen(color, 1, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            
            # Primary grid
            self._draw_line_grid(painter, rect, spacing, color)
            
            # Secondary grid (lighter)
            lighter_color = QColor(color)
            lighter_color.setAlpha(color.alpha() // 2)
            pen.setColor(lighter_color)
            painter.setPen(pen)
            
            half_spacing = spacing // 2
            start_x = int(rect.left() / half_spacing) * half_spacing
            start_y = int(rect.top() / half_spacing) * half_spacing
            
            for x in range(int(start_x), int(rect.right()) + half_spacing, half_spacing):
                if x % spacing != 0:  # Skip main grid lines
                    painter.drawLine(x, rect.top(), x, rect.bottom())
            
            for y in range(int(start_y), int(rect.bottom()) + half_spacing, half_spacing):
                if y % spacing != 0:  # Skip main grid lines
                    painter.drawLine(rect.left(), y, rect.right(), y)
        
        # Grid control methods
        def set_grid_visible(self, visible):
            """Set grid visibility"""
            self.grid_settings['show_grid'] = visible
            self.update_background()
            print(f"🔲 Grid visibility: {visible}")
        
        def set_snap_to_grid(self, enabled):
            """Set snap to grid"""
            self.grid_settings['snap_to_grid'] = enabled
            print(f"🧲 Snap to grid: {enabled}")
        
        def set_grid_size(self, size):
            """Set grid size"""
            self.grid_settings['grid_spacing'] = size
            self.update_background()
            print(f"📏 Grid size: {size}")
        
        def show_grid_settings(self):
            """Show grid settings dialog"""
            dialog = GridSettingsDialog(self, self.grid_settings)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Apply new settings
                new_settings = dialog.get_settings()
                self.grid_settings.update(new_settings)
                self.update_background()
                self.save_grid_settings()
                print("✅ Grid settings updated")
        
        def _snap_to_grid(self, pos):
            """Snap position to grid if enabled"""
            if not self.grid_settings['snap_to_grid']:
                return pos
            
            spacing = self.grid_settings['grid_spacing']
            snapped_x = round(pos.x() / spacing) * spacing
            snapped_y = round(pos.y() / spacing) * spacing
            return QPointF(snapped_x, snapped_y)
        
        # Enhanced component management
        def add_component(self, category, component_name, position, package_type="DIP-40"):
            """Add a component to the canvas with undo support"""
            try:
                # Save state for undo
                self.save_state_for_undo()
                
                # Snap position to grid if enabled
                snapped_position = self._snap_to_grid(position)
                
                # Create component item
                component_item = ComponentItem(component_name, category, package_type)
                component_item.setPos(snapped_position)
                
                # Apply visual settings
                component_item.show_pins = self.show_pin_numbers
                component_item.show_labels = self.show_component_labels
                
                # Add to scene
                self.scene.addItem(component_item)
                
                # Track component
                component_id = f"{component_name}_{len(self.components)}"
                self.components[component_id] = component_item
                
                # Emit signal
                self.component_added.emit(category, component_name, snapped_position)
                
                print(f"✅ Component added: {component_name} at {snapped_position}")
                return component_item
                
            except Exception as e:
                print(f"❌ Error adding component: {e}")
                return None
        
        def remove_component(self, component_item):
            """Remove a component from the canvas with undo support"""
            try:
                # Save state for undo
                self.save_state_for_undo()
                
                # Remove from scene
                self.scene.removeItem(component_item)
                
                # Remove from tracking
                for comp_id, comp in list(self.components.items()):
                    if comp == component_item:
                        del self.components[comp_id]
                        break
                
                self.component_selected.emit(None)
                print(f"🗑️ Component removed")
                
            except Exception as e:
                print(f"❌ Error removing component: {e}")
        
        def clear_canvas(self):
            """Clear all components from canvas"""
            self.save_state_for_undo()
            self.scene.clear()
            self.components.clear()
            self.connections.clear()
            print("🧹 Canvas cleared")
        
        # Component selection methods
        def delete_selected_components(self):
            """Delete all selected components"""
            selected_items = [item for item in self.scene.selectedItems() if isinstance(item, ComponentItem)]
            
            if selected_items:
                self.save_state_for_undo()
                for item in selected_items:
                    self.remove_component(item)
                print(f"🗑️ Deleted {len(selected_items)} components")
            else:
                print("🗑️ No components selected to delete")
        
        def select_all_components(self):
            """Select all components on canvas"""
            component_items = [item for item in self.scene.items() if isinstance(item, ComponentItem)]
            
            for item in component_items:
                item.setSelected(True)
            
            print(f"🔲 Selected {len(component_items)} components")
        
        def get_selected_components(self):
            """Get list of selected components"""
            return [item for item in self.scene.selectedItems() if isinstance(item, ComponentItem)]
        
        # Enhanced undo/redo functionality
        def save_state_for_undo(self):
            """Save current state for undo functionality"""
            state = self.save_canvas_state()
            
            # Add to undo stack
            self.undo_stack.append(state)
            
            # Limit undo stack size
            if len(self.undo_stack) > self.max_undo_levels:
                self.undo_stack.pop(0)
            
            # Clear redo stack since new action was performed
            self.redo_stack.clear()
        
        def undo(self):
            """Undo last action"""
            if self.undo_stack:
                # Save current state to redo stack
                current_state = self.save_canvas_state()
                self.redo_stack.append(current_state)
                
                # Restore previous state
                previous_state = self.undo_stack.pop()
                self.load_canvas_state(previous_state)
                
                print("↶ Undo performed")
            else:
                print("↶ Nothing to undo")
        
        def redo(self):
            """Redo last undone action"""
            if self.redo_stack:
                # Save current state to undo stack
                current_state = self.save_canvas_state()
                self.undo_stack.append(current_state)
                
                # Restore next state
                next_state = self.redo_stack.pop()
                self.load_canvas_state(next_state)
                
                print("↷ Redo performed")
            else:
                print("↷ Nothing to redo")
        
        # Canvas state management
        def save_canvas_state(self):
            """Save current canvas state"""
            canvas_data = {
                'components': [],
                'connections': self.connections,
                'grid_settings': self.grid_settings.copy(),
                'zoom_factor': self.zoom_factor,
                'visual_settings': {
                    'show_pin_numbers': self.show_pin_numbers,
                    'show_component_labels': self.show_component_labels
                }
            }
            
            # Save component data
            for comp_id, component in self.components.items():
                comp_data = {
                    'id': comp_id,
                    'name': component.name,
                    'category': component.category,
                    'package_type': component.package_type,
                    'position': {'x': component.pos().x(), 'y': component.pos().y()},
                    'rotation': component.rotation()
                }
                canvas_data['components'].append(comp_data)
            
            return canvas_data
        
        def load_canvas_state(self, canvas_data):
            """Load canvas state from data"""
            try:
                # Clear existing canvas
                self.scene.clear()
                self.components.clear()
                
                # Load components
                if 'components' in canvas_data:
                    for comp_data in canvas_data['components']:
                        position = QPointF(comp_data['position']['x'], comp_data['position']['y'])
                        component = self.add_component(
                            comp_data['category'],
                            comp_data['name'],
                            position,
                            comp_data.get('package_type', 'DIP-40')
                        )
                        
                        if component and 'rotation' in comp_data:
                            component.setRotation(comp_data['rotation'])
                
                # Load connections
                if 'connections' in canvas_data:
                    self.connections = canvas_data['connections']
                
                # Load grid settings
                if 'grid_settings' in canvas_data:
                    self.grid_settings.update(canvas_data['grid_settings'])
                    self.update_background()
                
                # Load visual settings
                if 'visual_settings' in canvas_data:
                    vs = canvas_data['visual_settings']
                    self.show_pin_numbers = vs.get('show_pin_numbers', True)
                    self.show_component_labels = vs.get('show_component_labels', True)
                    self.toggle_pin_numbers(self.show_pin_numbers)
                    self.toggle_component_labels(self.show_component_labels)
                
                # Load zoom
                if 'zoom_factor' in canvas_data:
                    target_zoom = canvas_data['zoom_factor']
                    current_zoom = self.zoom_factor
                    scale_factor = target_zoom / current_zoom
                    self.scale(scale_factor, scale_factor)
                    self.zoom_factor = target_zoom
                    self.zoom_changed.emit(self.zoom_factor)
                
                print(f"✅ Canvas state loaded: {len(self.components)} components")
                
            except Exception as e:
                print(f"❌ Error loading canvas state: {e}")
        
        # Visual control methods
        def toggle_pin_numbers(self, show):
            """Toggle pin number display"""
            self.show_pin_numbers = show
            for component in self.components.values():
                if isinstance(component, ComponentItem):
                    component.show_pins = show
                    component.update()
            print(f"📍 Pin numbers: {'shown' if show else 'hidden'}")
        
        def toggle_component_labels(self, show):
            """Toggle component label display"""
            self.show_component_labels = show
            for component in self.components.values():
                if isinstance(component, ComponentItem):
                    component.show_labels = show
                    component.update()
            print(f"🏷️ Component labels: {'shown' if show else 'hidden'}")
        
        # Enhanced zoom functionality
        def zoom_in(self):
            """Zoom in"""
            if self.zoom_factor < 5.0:
                self.scale(1.2, 1.2)
                self.zoom_factor *= 1.2
                self.zoom_changed.emit(self.zoom_factor)
                print(f"🔍 Zoom in: {self.zoom_factor:.1f}x")
        
        def zoom_out(self):
            """Zoom out"""
            if self.zoom_factor > 0.1:
                self.scale(0.8, 0.8)
                self.zoom_factor *= 0.8
                self.zoom_changed.emit(self.zoom_factor)
                print(f"🔍 Zoom out: {self.zoom_factor:.1f}x")
        
        def zoom_fit(self):
            """Zoom to fit all components"""
            if self.components:
                # Get bounding rect of all components
                items_rect = self.scene.itemsBoundingRect()
                
                # Add some padding
                padding = 50
                items_rect.adjust(-padding, -padding, padding, padding)
                
                # Fit view to rect
                self.fitInView(items_rect, Qt.AspectRatioMode.KeepAspectRatio)
                
                # Update zoom factor
                transform = self.transform()
                self.zoom_factor = transform.m11()  # Get scale factor
                self.zoom_changed.emit(self.zoom_factor)
                
                print(f"🎯 Zoom fit: {self.zoom_factor:.1f}x")
            else:
                print("🎯 No components to fit view to")
        
        def reset_zoom(self):
            """Reset zoom to 100%"""
            self.resetTransform()
            self.zoom_factor = 1.0
            self.zoom_changed.emit(self.zoom_factor)
            print("🎯 Zoom reset to 100%")
        
        # Enhanced mouse handling
        def mousePressEvent(self, event):
            """Handle mouse press events"""
            if event.button() == Qt.MouseButton.RightButton:
                # Right click - show context menu
                self.show_context_menu(event.pos())
            else:
                # Handle selection
                item = self.itemAt(event.pos())
                if isinstance(item, ComponentItem):
                    self.component_selected.emit(item)
                    print(f"🎯 Component selected: {item.name}")
                else:
                    self.component_selected.emit(None)
                
                super().mousePressEvent(event)
        
        def mouseMoveEvent(self, event):
            """Handle mouse move events - prevent trails"""
            super().mouseMoveEvent(event)
            # Force scene update during movement to prevent trails
            self.scene.update()
        
        def mouseReleaseEvent(self, event):
            """Handle mouse release events"""
            super().mouseReleaseEvent(event)
            # Final scene update after movement
            self.scene.update()
        
        def wheelEvent(self, event):
            """Handle wheel events for zooming"""
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                # Zoom with Ctrl + wheel
                if event.angleDelta().y() > 0:
                    self.zoom_in()
                else:
                    self.zoom_out()
            else:
                super().wheelEvent(event)
        
        def keyPressEvent(self, event):
            """Handle key press events"""
            if event.key() == Qt.Key.Key_Delete:
                # Delete selected components
                self.delete_selected_components()
            elif event.key() == Qt.Key.Key_Escape:
                # Deselect all
                self.scene.clearSelection()
                self.component_selected.emit(None)
            elif event.key() == Qt.Key.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                # Select all components
                self.select_all_components()
            elif event.key() == Qt.Key.Key_Z and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                # Undo
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    self.redo()
                else:
                    self.undo()
            else:
                super().keyPressEvent(event)
        
        # Context menu functionality
        def show_context_menu(self, position):
            """Show context menu at position"""
            menu = QMenu(self)
            
            # Get item at position
            item = self.itemAt(position)
            
            if isinstance(item, ComponentItem):
                # Component context menu
                menu.addAction("🔧 Properties", lambda: self.show_component_properties(item))
                menu.addAction("📋 Copy", lambda: self.copy_component(item))
                menu.addAction("🔄 Rotate", lambda: self.rotate_component(item))
                menu.addSeparator()
                menu.addAction("🗑️ Delete", lambda: self.remove_component(item))
            else:
                # Canvas context menu
                scene_pos = self.mapToScene(position)
                menu.addAction("📦 Add Component", lambda: self.show_add_component_dialog(scene_pos))
                menu.addAction("📋 Paste", lambda: self.paste_component(scene_pos))
                menu.addSeparator()
                menu.addAction("⌗ Grid Settings", self.show_grid_settings)
                menu.addAction("🧹 Clear Canvas", self.clear_canvas)
            
            # Show menu
            global_pos = self.mapToGlobal(position)
            menu.exec(global_pos)
        
        def show_component_properties(self, component):
            """Show component properties dialog"""
            print(f"🔧 Properties for {component.name}")
            # TODO: Implement properties dialog
        
        def copy_component(self, component):
            """Copy component to clipboard"""
            print(f"📋 Copied {component.name}")
            # TODO: Implement copy functionality
        
        def rotate_component(self, component):
            """Rotate component"""
            self.save_state_for_undo()
            current_rotation = component.rotation()
            component.setRotation(current_rotation + 90)
            print(f"🔄 Rotated {component.name}")
        
        def show_add_component_dialog(self, position):
            """Show add component dialog"""
            print(f"📦 Add component at {position}")
            # TODO: Implement add component dialog
        
        def paste_component(self, position):
            """Paste component at position"""
            print(f"📋 Paste at {position}")
            # TODO: Implement paste functionality
        
        # Enhanced drag and drop functionality
        def dragEnterEvent(self, event):
            """Handle drag enter for component placement"""
            if event.mimeData().hasText():
                mime_text = event.mimeData().text()
                if mime_text.startswith("component:"):
                    event.acceptProposedAction()
                    print(f"🎯 Drag enter accepted: {mime_text}")
                else:
                    event.ignore()
            else:
                event.ignore()
        
        def dragMoveEvent(self, event):
            """Handle drag move"""
            if event.mimeData().hasText():
                event.acceptProposedAction()
            else:
                event.ignore()
        
        def dropEvent(self, event):
            """Handle drop event for component placement"""
            if event.mimeData().hasText():
                mime_text = event.mimeData().text()
                if mime_text.startswith("component:"):
                    try:
                        # Parse component data: "component:category:name:package"
                        parts = mime_text.split(":")
                        if len(parts) >= 3:
                            category = parts[1]
                            component_name = parts[2]
                            package_type = parts[3] if len(parts) > 3 else "DIP-40"
                            
                            # Get drop position
                            drop_pos = self.mapToScene(event.position().toPoint())
                            
                            # Add component
                            self.add_component(category, component_name, drop_pos, package_type)
                            
                            event.acceptProposedAction()
                            print(f"🎯 Component dropped: {component_name}")
                        else:
                            print(f"❌ Invalid component data: {mime_text}")
                            event.ignore()
                    except Exception as e:
                        print(f"❌ Error handling drop: {e}")
                        event.ignore()
                else:
                    event.ignore()
            else:
                event.ignore()
        
        # Utility methods
        def export_canvas_image(self, filename=None):
            """Export canvas as image"""
            try:
                if not filename:
                    filename, _ = QFileDialog.getSaveFileName(
                        self, "Export Canvas", "", "PNG Images (*.png);;JPG Images (*.jpg);;All Files (*)"
                    )
                
                if filename:
                    # Get scene bounding rect
                    scene_rect = self.scene.itemsBoundingRect()
                    if scene_rect.isEmpty():
                        scene_rect = QRectF(-500, -500, 1000, 1000)
                    
                    # Add padding
                    padding = 50
                    scene_rect.adjust(-padding, -padding, padding, padding)
                    
                    # Create pixmap
                    pixmap = QPixmap(int(scene_rect.width()), int(scene_rect.height()))
                    pixmap.fill(self.grid_settings['bg_color'])
                    
                    # Render scene to pixmap
                    painter = QPainter(pixmap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    self.scene.render(painter, QRectF(), scene_rect)
                    painter.end()
                    
                    # Save pixmap
                    pixmap.save(filename)
                    print(f"💾 Canvas exported to {filename}")
                    return filename
                
            except Exception as e:
                print(f"❌ Error exporting canvas: {e}")
                return None
        
        def get_canvas_statistics(self):
            """Get canvas statistics"""
            stats = {
                'total_components': len(self.components),
                'component_types': {},
                'total_connections': len(self.connections),
                'canvas_bounds': self.scene.itemsBoundingRect(),
                'zoom_level': self.zoom_factor,
                'grid_settings': self.grid_settings.copy()
            }
            
            # Count component types
            for component in self.components.values():
                category = component.category
                stats['component_types'][category] = stats['component_types'].get(category, 0) + 1
            
            return stats
        
        # Tool management
        def set_tool(self, tool_name):
            """Set current tool"""
            self.current_tool = tool_name
            
            # Update cursor based on tool
            cursors = {
                'select': Qt.CursorShape.ArrowCursor,
                'place': Qt.CursorShape.CrossCursor,
                'wire': Qt.CursorShape.PointingHandCursor,
                'trace': Qt.CursorShape.CrossCursor,
                'via': Qt.CursorShape.PointingHandCursor,
                'pad': Qt.CursorShape.PointingHandCursor,
                'measure': Qt.CursorShape.SizeAllCursor
            }
            
            cursor = cursors.get(tool_name, Qt.CursorShape.ArrowCursor)
            self.setCursor(cursor)
            
            print(f"🔧 Canvas tool set to: {tool_name}")
        
        # Compatibility methods for existing code
        def delete_selected(self):
            """Delete selected components (compatibility)"""
            self.delete_selected_components()
        
        def select_all(self):
            """Select all components (compatibility)"""
            self.select_all_components()
        
        def save_canvas(self):
            """Save canvas to file (compatibility)"""
            print("💾 Canvas save functionality - use save_canvas_state()")
        
        def open_canvas(self):
            """Open canvas from file (compatibility)"""
            print("📁 Canvas open functionality - use load_canvas_state()")
        
        def clear(self):
            """Clear canvas (compatibility)"""
            self.clear_canvas()

else:
    # Fallback class when PyQt6 is not available
    class PCBCanvas:
        """Fallback PCB Canvas when PyQt6 is not available"""
        
        def __init__(self, parent=None):
            self.components = {}
            self.connections = []
            self.current_tool = "select"
            print("⚠️ PCB Canvas: PyQt6 not available, using fallback")
        
        def set_tool(self, tool):
            self.current_tool = tool
            print(f"⚠️ Fallback canvas: tool set to {tool}")
        
        def add_component(self, category, name, position, package="DIP-40"):
            print(f"⚠️ Fallback canvas: would add {name}")
        
        def set_grid_visible(self, visible):
            print(f"⚠️ Fallback canvas: grid visibility {visible}")
        
        def set_snap_to_grid(self, enabled):
            print(f"⚠️ Fallback canvas: snap to grid {enabled}")
        
        def set_grid_size(self, size):
            print(f"⚠️ Fallback canvas: grid size {size}")


# Export classes
__all__ = ['PCBCanvas', 'ComponentItem', 'GridSettingsDialog']

# Test function
if __name__ == "__main__":
    if PYQT6_AVAILABLE:
        app = QApplication(sys.argv)
        
        # Create and show enhanced canvas
        canvas = PCBCanvas()
        canvas.show()
        canvas.resize(800, 600)
        
        # Add some test components
        canvas.add_component("CPU", "Z80", QPointF(100, 100), "DIP-40")
        canvas.add_component("Memory", "RAM", QPointF(200, 200), "DIP-28")
        
        print("🧪 Enhanced Canvas test - close window to continue")
        app.exec()
        print("✅ Enhanced Canvas test completed")
    else:
        print("⚠️ Cannot test - PyQt6 not available")