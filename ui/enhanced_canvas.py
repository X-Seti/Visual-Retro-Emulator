#!/usr/bin/env python3
"""
X-Seti - June16 2025 - Enhanced Canvas with Icon Menus and Grid Controls
Visual Retro System Emulator Builder - Clean canvas interface with working functionality
"""

#this belongs in ui/enhanced_canvas.py

import os
import sys
from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox,
                           QCheckBox, QSlider, QButtonGroup, QFrame, QColorDialog,
                           QToolButton, QMenu, QWidgetAction, QDialog, QGridLayout,
                           QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem,
                           QGraphicsPixmapItem, QApplication, QTreeWidget)
from PyQt6.QtCore import (Qt, QPointF, QRectF, QTimer, pyqtSignal, QPropertyAnimation,
                        QEasingCurve, QParallelAnimationGroup, QPoint)
from PyQt6.QtGui import (QPainter, QPen, QBrush, QColor, QPixmap, QFont, QIcon,
                       QPainterPath, QMouseEvent, QWheelEvent, QKeyEvent, QCursor,
                       QShortcut, QKeySequence, QAction, QPolygonF)

class ComponentItem(QGraphicsItem):
    """Visual component item for the canvas"""
    
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
        return dimensions.get(package_type, (30, 200))  # Default to DIP-40
    
    def _get_pin_configuration(self, package_type):
        """Get pin configuration for the package"""
        if package_type.startswith('DIP-'):
            pin_count = int(package_type.split('-')[1])
            pins_per_side = pin_count // 2
            return {'type': 'dip', 'total': pin_count, 'per_side': pins_per_side}
        elif package_type.startswith('QFP-'):
            pin_count = int(package_type.split('-')[1])
            pins_per_side = pin_count // 4
            return {'type': 'qfp', 'total': pin_count, 'per_side': pins_per_side}
        else:
            return {'type': 'generic', 'total': 40, 'per_side': 20}
    
    def boundingRect(self):
        """Return the bounding rectangle"""
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget):
        """Paint the component"""
        # Component body
        if self.isSelected():
            painter.setPen(QPen(QColor(255, 165, 0), 3))  # Orange selection
            painter.setBrush(QBrush(QColor(70, 70, 70)))
        else:
            painter.setPen(QPen(QColor(50, 50, 50), 2))
            painter.setBrush(QBrush(QColor(40, 40, 40)))
        
        # Draw component body
        rect = QRectF(0, 0, self.width, self.height)
        painter.drawRoundedRect(rect, 4, 4)
        
        # Draw pins
        self._draw_pins(painter)
        
        # Draw component name
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
        
        # Calculate text position
        text_rect = QRectF(2, 2, self.width - 4, self.height - 4)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.name)
        
        # Draw package type
        painter.setFont(QFont("Arial", 6))
        package_rect = QRectF(2, self.height - 15, self.width - 4, 12)
        painter.drawText(package_rect, Qt.AlignmentFlag.AlignCenter, self.package_type)
    
    def _draw_pins(self, painter):
        """Draw component pins"""
        pin_config = self.pins
        
        if pin_config['type'] == 'dip':
            self._draw_dip_pins(painter, pin_config)
        elif pin_config['type'] == 'qfp':
            self._draw_qfp_pins(painter, pin_config)
    
    def _draw_dip_pins(self, painter, config):
        """Draw DIP package pins"""
        pins_per_side = config['per_side']
        pin_spacing = (self.height - 20) / (pins_per_side - 1) if pins_per_side > 1 else 0
        
        # Pin colors
        colors = [
            QColor(255, 165, 0),    # Orange
            QColor(255, 255, 0),    # Yellow  
            QColor(0, 255, 0),      # Green
            QColor(0, 191, 255),    # Blue
            QColor(255, 0, 255),    # Magenta
            QColor(255, 0, 0),      # Red
        ]
        
        # Left side pins
        for i in range(pins_per_side):
            y = int(10 + i * pin_spacing)  # Convert to int
            color = colors[i % len(colors)]
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(-3, y - 2, 6, 4)
        
        # Right side pins  
        for i in range(pins_per_side):
            y = int(10 + i * pin_spacing)  # Convert to int
            color = colors[(pins_per_side + i) % len(colors)]
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(self.width - 3, y - 2, 6, 4)
    
    def _draw_qfp_pins(self, painter, config):
        """Draw QFP package pins"""
        pins_per_side = config['per_side']
        
        # Colors for pins
        colors = [
            QColor(255, 165, 0),    # Orange
            QColor(255, 255, 0),    # Yellow
            QColor(0, 255, 0),      # Green
            QColor(0, 191, 255),    # Blue
            QColor(255, 0, 255),    # Magenta
            QColor(255, 0, 0),      # Red
        ]
        
        pin_spacing = (self.width - 20) / (pins_per_side - 1) if pins_per_side > 1 else 0
        
        # Top pins
        for i in range(pins_per_side):
            x = int(10 + i * pin_spacing)  # Convert to int
            color = colors[i % len(colors)]
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(x - 2, -3, 4, 6)
        
        # Right pins
        for i in range(pins_per_side):
            y = int(10 + i * pin_spacing)  # Convert to int
            color = colors[(pins_per_side + i) % len(colors)]
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(self.width - 3, y - 2, 6, 4)
        
        # Bottom pins
        for i in range(pins_per_side):
            x = int(10 + (pins_per_side - 1 - i) * pin_spacing)  # Convert to int
            color = colors[(2 * pins_per_side + i) % len(colors)]
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(x - 2, self.height - 3, 4, 6)
        
        # Left pins
        for i in range(pins_per_side):
            y = int(10 + (pins_per_side - 1 - i) * pin_spacing)  # Convert to int
            color = colors[(3 * pins_per_side + i) % len(colors)]
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(-3, y - 2, 6, 4)

class GridSettingsDialog(QDialog):
    """Grid settings dialog"""
    
    # Define signals at class level  
    grid_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Grid Settings")
        self.setFixedSize(350, 400)
        
        layout = QVBoxLayout(self)
        
        # Grid visibility
        visibility_group = QFrame()
        visibility_group.setFrameStyle(QFrame.Shape.Box)
        visibility_layout = QVBoxLayout(visibility_group)
        
        visibility_layout.addWidget(QLabel("Grid Visibility"))
        
        self.show_grid = QCheckBox("Show Grid")
        self.show_grid.setChecked(True)
        visibility_layout.addWidget(self.show_grid)
        
        self.snap_to_grid = QCheckBox("Snap to Grid")
        self.snap_to_grid.setChecked(True)
        visibility_layout.addWidget(self.snap_to_grid)
        
        layout.addWidget(visibility_group)
        
        # Grid style
        style_group = QFrame()
        style_group.setFrameStyle(QFrame.Shape.Box)
        style_layout = QGridLayout(style_group)
        
        style_layout.addWidget(QLabel("Grid Style"), 0, 0, 1, 2)
        
        self.grid_style = QComboBox()
        self.grid_style.addItems(["Dotted", "Solid Lines", "Dashed Lines", "Cross Pattern"])
        self.grid_style.setCurrentText("Dotted")
        style_layout.addWidget(QLabel("Style:"), 1, 0)
        style_layout.addWidget(self.grid_style, 1, 1)
        
        # Grid spacing
        self.grid_spacing = QSpinBox()
        self.grid_spacing.setRange(5, 100)
        self.grid_spacing.setValue(25)
        self.grid_spacing.setSuffix(" px")
        style_layout.addWidget(QLabel("Spacing:"), 2, 0)
        style_layout.addWidget(self.grid_spacing, 2, 1)
        
        # Grid colors
        self.grid_color_btn = QPushButton("Grid Color")
        self.grid_color_btn.clicked.connect(self.choose_grid_color)
        self.grid_color = QColor(100, 100, 100, 100)
        self.update_color_button()
        style_layout.addWidget(QLabel("Color:"), 3, 0)
        style_layout.addWidget(self.grid_color_btn, 3, 1)
        
        layout.addWidget(style_group)
        
        # Background settings
        bg_group = QFrame()
        bg_group.setFrameStyle(QFrame.Shape.Box)
        bg_layout = QGridLayout(bg_group)
        
        bg_layout.addWidget(QLabel("Background"), 0, 0, 1, 2)
        
        self.bg_type = QComboBox()
        self.bg_type.addItems(["Solid Color", "PCB Pattern", "Breadboard", "Perfboard", "White Canvas", "Light Gray Canvas"])
        bg_layout.addWidget(QLabel("Type:"), 1, 0)
        bg_layout.addWidget(self.bg_type, 1, 1)
        
        self.bg_color_btn = QPushButton("Background Color")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        self.bg_color = QColor(40, 44, 52)
        self.update_bg_color_button()
        bg_layout.addWidget(QLabel("Color:"), 2, 0)
        bg_layout.addWidget(self.bg_color_btn, 2, 1)
        
        layout.addWidget(bg_group)
        
        # Paper cut guides
        guides_group = QFrame()
        guides_group.setFrameStyle(QFrame.Shape.Box)
        guides_layout = QVBoxLayout(guides_group)
        
        guides_layout.addWidget(QLabel("Paper Cut Guides"))
        
        self.show_margins = QCheckBox("Show Page Margins")
        guides_layout.addWidget(self.show_margins)
        
        self.show_rulers = QCheckBox("Show Rulers")
        guides_layout.addWidget(self.show_rulers)
        
        layout.addWidget(guides_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_settings)
        button_layout.addWidget(apply_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.show_grid.toggled.connect(self.emit_changes)
        self.snap_to_grid.toggled.connect(self.emit_changes)
        self.grid_style.currentTextChanged.connect(self.emit_changes)
        self.grid_spacing.valueChanged.connect(self.emit_changes)
        self.bg_type.currentTextChanged.connect(self.emit_changes)
    
    def choose_grid_color(self):
        """Choose grid color"""
        color = QColorDialog.getColor(self.grid_color, self, "Choose Grid Color")
        if color.isValid():
            self.grid_color = color
            self.update_color_button()
            self.emit_changes()
    
    def choose_bg_color(self):
        """Choose background color"""
        color = QColorDialog.getColor(self.bg_color, self, "Choose Background Color")
        if color.isValid():
            self.bg_color = color
            self.update_bg_color_button()
            self.emit_changes()
    
    def update_color_button(self):
        """Update grid color button appearance"""
        self.grid_color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.grid_color.name()};
                color: white;
                border: 2px solid #bdc3c7;
                padding: 6px 12px;
                border-radius: 4px;
            }}
        """)
    
    def update_bg_color_button(self):
        """Update background color button appearance"""
        self.bg_color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.bg_color.name()};
                color: white;
                border: 2px solid #bdc3c7;
                padding: 6px 12px;
                border-radius: 4px;
            }}
        """)
    
    def emit_changes(self):
        """Emit grid settings changes"""
        settings = {
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
        self.grid_changed.emit(settings)
    
    def apply_settings(self):
        """Apply settings"""
        self.emit_changes()
        print("✅ Grid settings applied")
    
    def reset_settings(self):
        """Reset to default settings"""
        self.show_grid.setChecked(True)
        self.snap_to_grid.setChecked(True)
        self.grid_style.setCurrentText("Dotted")
        self.grid_spacing.setValue(25)
        self.grid_color = QColor(100, 100, 100, 100)
        self.bg_type.setCurrentText("Solid Color")
        self.bg_color = QColor(40, 44, 52)
        self.show_margins.setChecked(False)
        self.show_rulers.setChecked(False)
        self.update_color_button()
        self.update_bg_color_button()
        self.emit_changes()
        print("🔄 Grid settings reset")
    
    def load_current_settings(self, settings):
        """Load current settings into the dialog"""
        try:
            # Block signals to prevent triggering changes while loading
            self.show_grid.blockSignals(True)
            self.snap_to_grid.blockSignals(True)
            self.grid_style.blockSignals(True)
            self.grid_spacing.blockSignals(True)
            self.bg_type.blockSignals(True)
            self.show_margins.blockSignals(True)
            self.show_rulers.blockSignals(True)
            
            # Load settings
            self.show_grid.setChecked(settings.get('show_grid', True))
            self.snap_to_grid.setChecked(settings.get('snap_to_grid', True))
            self.grid_style.setCurrentText(settings.get('grid_style', 'Dotted'))
            self.grid_spacing.setValue(settings.get('grid_spacing', 25))
            self.bg_type.setCurrentText(settings.get('bg_type', 'Solid Color'))
            self.show_margins.setChecked(settings.get('show_margins', False))
            self.show_rulers.setChecked(settings.get('show_rulers', False))
            
            # Load colors
            if 'grid_color' in settings:
                self.grid_color = settings['grid_color']
                self.update_color_button()
            
            if 'bg_color' in settings:
                self.bg_color = settings['bg_color']
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

class EnhancedPCBCanvas(QGraphicsView):
    """Enhanced PCB Canvas with working functionality"""
    
    component_added = pyqtSignal(str, str, QPointF)  # category, component, position
    component_selected = pyqtSignal(object)
    zoom_changed = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Canvas settings
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
        
        # Load saved settings
        self.load_grid_settings()
        
        # Canvas state
        self.current_tool = 'select'
        self.zoom_factor = 1.0
        self.components = {}
        self.connections = []
        
        # Undo/Redo functionality
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo_levels = 50
        
        # Setup canvas
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        
        # Create grid settings dialog
        self.grid_dialog = GridSettingsDialog(self)
        self.grid_dialog.grid_changed.connect(self.update_grid_settings)
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
        
        # Initial setup
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        self.update_background()
        
        print("✅ Enhanced PCB Canvas initialized")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        shortcuts = [
            ('S', self.select_tool),
            ('P', self.pan_tool),
            ('+', self.zoom_in),
            ('-', self.zoom_out),
            ('F', self.fit_to_window),
            ('G', self.show_grid_settings),
            ('Ctrl+Z', self.undo),
            ('Ctrl+Y', self.redo),
            ('Delete', self.delete_selected),
            ('Ctrl+A', self.select_all)
        ]
        
        for key, callback in shortcuts:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(callback)
    
    def set_current_tool(self, tool):
        """Set current tool"""
        self.current_tool = tool
        
        if tool == 'select':
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif tool == 'pan':
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        
        print(f"🔧 Tool changed to: {tool}")
    
    def select_tool(self):
        self.set_current_tool('select')
    
    def pan_tool(self):
        self.set_current_tool('pan')
    
    def zoom_in(self):
        """Zoom in"""
        self.scale(1.2, 1.2)
        self.zoom_factor *= 1.2
        self.zoom_changed.emit(self.zoom_factor)
        print(f"🔍+ Zoom: {self.zoom_factor:.2f}")
    
    def zoom_out(self):
        """Zoom out"""
        self.scale(0.8, 0.8)
        self.zoom_factor *= 0.8
        self.zoom_changed.emit(self.zoom_factor)
        print(f"🔍- Zoom: {self.zoom_factor:.2f}")
    
    def fit_to_window(self):
        """Fit canvas to window"""
        if self.components:
            # Calculate bounding rect of all components
            items = [item for item in self.scene.items() if isinstance(item, ComponentItem)]
            if items:
                bounding_rect = items[0].boundingRect().translated(items[0].pos())
                for item in items[1:]:
                    item_rect = item.boundingRect().translated(item.pos())
                    bounding_rect = bounding_rect.united(item_rect)
                
                self.fitInView(bounding_rect, Qt.AspectRatioMode.KeepAspectRatio)
            else:
                self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        
        # Update zoom factor
        transform = self.transform()
        self.zoom_factor = transform.m11()
        self.zoom_changed.emit(self.zoom_factor)
        print(f"⬜ Fit to window - Zoom: {self.zoom_factor:.2f}")
    
    def show_grid_settings(self):
        """Show grid settings dialog with current settings"""
        # Update dialog with current settings before showing
        self.grid_dialog.load_current_settings(self.grid_settings)
        self.grid_dialog.show()
        self.grid_dialog.raise_()
    
    def update_grid_settings(self, settings):
        """Update grid settings and save them"""
        self.grid_settings.update(settings)
        self.save_grid_settings()  # Auto-save when settings change
        self.update_background()
        self.scene.update()
        print(f"⌗ Grid settings updated and saved")
    
    def save_grid_settings(self):
        """Save grid settings to file"""
        try:
            import json
            settings_to_save = self.grid_settings.copy()
            
            # Convert QColor objects to hex strings for JSON serialization
            for key, value in settings_to_save.items():
                if isinstance(value, QColor):
                    settings_to_save[key] = value.name()  # Convert to hex string
            
            # Save to settings file
            with open('canvas_settings.json', 'w') as f:
                json.dump(settings_to_save, f, indent=2)
            
            print("💾 Canvas settings saved")
            
        except Exception as e:
            print(f"⚠️ Error saving canvas settings: {e}")
    
    def load_grid_settings(self):
        """Load grid settings from file"""
        try:
            import json
            import os
            
            if os.path.exists('canvas_settings.json'):
                with open('canvas_settings.json', 'r') as f:
                    saved_settings = json.load(f)
                
                # Convert hex color strings back to QColor objects
                for key, value in saved_settings.items():
                    if key in ['grid_color', 'bg_color'] and isinstance(value, str):
                        saved_settings[key] = QColor(value)
                
                # Update settings with saved values
                self.grid_settings.update(saved_settings)
                print("📂 Canvas settings loaded")
            else:
                print("📂 No saved canvas settings found, using defaults")
                
        except Exception as e:
            print(f"⚠️ Error loading canvas settings: {e}")
            print("📂 Using default canvas settings")
    
    def update_background(self):
        """Update canvas background"""
        bg_type = self.grid_settings['bg_type']
        
        if bg_type == "White Canvas":
            bg_color = QColor(255, 255, 255)  # White
        elif bg_type == "Light Gray Canvas":
            bg_color = QColor(240, 240, 240)  # Light gray
        else:
            bg_color = self.grid_settings['bg_color']
        
        self.setBackgroundBrush(QBrush(bg_color))
        self.scene.update()
    
    def drawBackground(self, painter, rect):
        """Draw custom background with grid and alternating row shading"""
        super().drawBackground(painter, rect)
        
        if not self.grid_settings['show_grid']:
            return
        
        # Grid settings
        spacing = self.grid_settings['grid_spacing']
        color = self.grid_settings['grid_color']
        style = self.grid_settings['grid_style']
        bg_type = self.grid_settings['bg_type']
        
        # Calculate grid bounds
        left = int(rect.left()) - (int(rect.left()) % spacing)
        top = int(rect.top()) - (int(rect.top()) % spacing)
        
        # Draw alternating row shading first (behind grid)
        self._draw_alternating_shading(painter, rect, spacing, left, top, bg_type)
        
        # Adjust grid color for light backgrounds
        if bg_type in ["White Canvas", "Light Gray Canvas"]:
            # Use darker colors for light backgrounds
            if color.lightness() > 150:  # If grid color is too light
                color = QColor(80, 80, 80)  # Dark gray
        
        # Setup pen for grid
        pen = QPen(color)
        
        if style == "Dotted":
            pen.setStyle(Qt.PenStyle.DotLine)
            pen.setWidth(1)
        elif style == "Solid Lines":
            pen.setStyle(Qt.PenStyle.SolidLine)
            pen.setWidth(1)
        elif style == "Dashed Lines":
            pen.setStyle(Qt.PenStyle.DashLine)
            pen.setWidth(1)
        
        painter.setPen(pen)
        
        # Draw grid
        if style == "Cross Pattern":
            # Draw cross pattern
            for x in range(left, int(rect.right()), spacing):
                for y in range(top, int(rect.bottom()), spacing):
                    painter.drawLine(x-3, y, x+3, y)
                    painter.drawLine(x, y-3, x, y+3)
        elif style == "Dotted":
            # Draw dots - make them more visible on light backgrounds
            dot_size = 2 if bg_type in ["White Canvas", "Light Gray Canvas"] else 1
            for x in range(left, int(rect.right()), spacing):
                for y in range(top, int(rect.bottom()), spacing):
                    if dot_size > 1:
                        painter.drawEllipse(x-1, y-1, dot_size, dot_size)
                    else:
                        painter.drawPoint(x, y)
        else:
            # Draw lines - fix the type conversion issue
            for x in range(left, int(rect.right()), spacing):
                painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))
            
            for y in range(top, int(rect.bottom()), spacing):
                painter.drawLine(int(rect.left()), y, int(rect.right()), y)
    
    def _draw_alternating_shading(self, painter, rect, spacing, left, top, bg_type):
        """Draw alternating row/column shading for better component alignment visibility"""
        # Choose shading colors based on background
        if bg_type in ["White Canvas", "Light Gray Canvas"]:
            # Light backgrounds - use subtle dark shading
            shade_color = QColor(220, 220, 220, 30)  # Very light gray with transparency
        else:
            # Dark backgrounds - use subtle light shading  
            shade_color = QColor(255, 255, 255, 15)  # Very light white with transparency
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(shade_color))
        
        # Draw alternating vertical stripes (for component columns)
        stripe_count = 0
        for x in range(left, int(rect.right()), spacing * 2):  # Every other column
            stripe_width = min(spacing, int(rect.right()) - x)
            if stripe_width > 0:
                stripe_rect = QRectF(x, rect.top(), stripe_width, rect.height())
                painter.drawRect(stripe_rect)
                stripe_count += 1
        
        # Optional: Add subtle horizontal stripes too (uncomment if desired)
        # Comment out this section if you only want vertical stripes
        if bg_type in ["White Canvas", "Light Gray Canvas"]:
            horizontal_shade = QColor(210, 210, 255, 20)  # Slightly blue tint
        else:
            horizontal_shade = QColor(255, 255, 200, 10)  # Slightly yellow tint
            
        painter.setBrush(QBrush(horizontal_shade))
        
        # Draw alternating horizontal stripes (every 4th row for subtlety)
        for y in range(top, int(rect.bottom()), spacing * 4):
            stripe_height = min(spacing, int(rect.bottom()) - y)
            if stripe_height > 0:
                stripe_rect = QRectF(rect.left(), y, rect.width(), stripe_height)
                painter.drawRect(stripe_rect)
    
    # Component management
    def add_component(self, category, component_name, position, package_type="DIP-40"):
        """Add a component to the canvas"""
        try:
            # Save state for undo
            self.save_state_for_undo()
            
            # Create component item
            component_item = ComponentItem(component_name, category, package_type)
            component_item.setPos(position)
            
            # Add to scene
            self.scene.addItem(component_item)
            
            # Track component
            component_id = f"{component_name}_{len(self.components)}"
            self.components[component_id] = component_item
            
            # Emit signal
            self.component_added.emit(category, component_name, position)
            
            print(f"✅ Component added: {component_name} at {position}")
            return component_item
            
        except Exception as e:
            print(f"❌ Error adding component: {e}")
            return None
    
    def remove_component(self, component_item):
        """Remove a component from the canvas"""
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
    
    # Drag and drop functionality
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
    
    def dropEvent(self, event):
        """Handle component drop"""
        if event.mimeData().hasText():
            mime_text = event.mimeData().text()
            if mime_text.startswith("component:"):
                try:
                    # Parse component data: "component:category:name:package"
                    parts = mime_text.split(":", 3)
                    if len(parts) >= 3:
                        category = parts[1]
                        component_name = parts[2]
                        package = parts[3] if len(parts) > 3 else "DIP-40"
                        
                        # Get drop position in scene coordinates
                        scene_pos = self.mapToScene(event.position().toPoint())
                        
                        # Snap to grid if enabled
                        if self.grid_settings['snap_to_grid']:
                            spacing = self.grid_settings['grid_spacing']
                            scene_pos.setX(round(scene_pos.x() / spacing) * spacing)
                            scene_pos.setY(round(scene_pos.y() / spacing) * spacing)
                        
                        # Add component
                        self.add_component(category, component_name, scene_pos, package)
                        
                        event.acceptProposedAction()
                        print(f"📦 Component dropped: {component_name} from {category}")
                    
                except Exception as e:
                    print(f"❌ Error handling drop: {e}")
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()
    
    # Mouse and keyboard events
    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.RightButton:
            # Right click - show context menu
            self.show_context_menu(event.position().toPoint())
        elif event.button() == Qt.MouseButton.MiddleButton:
            # Middle click for pan
            self.set_current_tool('pan')
            super().mousePressEvent(event)
        else:
            # Check for component selection
            item = self.itemAt(event.position().toPoint())
            if isinstance(item, ComponentItem):
                self.component_selected.emit(item)
                print(f"🎯 Component selected: {item.name}")
                # Save state for undo when starting to move
                self.save_state_for_undo()
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
        else:
            super().keyPressEvent(event)
    
    # Context menu
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
    
    def copy_component(self, component):
        """Copy component to clipboard"""
        print(f"📋 Copied {component.name}")
    
    def rotate_component(self, component):
        """Rotate component"""
        current_rotation = component.rotation()
        component.setRotation(current_rotation + 90)
        print(f"🔄 Rotated {component.name}")
    
    def show_add_component_dialog(self, position):
        """Show add component dialog"""
        print(f"📦 Add component at {position}")
    
    def paste_component(self, position):
        """Paste component at position"""
        print(f"📋 Paste at {position}")
    
    # Component selection methods
    def delete_selected_components(self):
        """Delete all selected components"""
        selected_items = [item for item in self.scene.selectedItems() if isinstance(item, ComponentItem)]
        
        if selected_items:
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
    
    # Undo/Redo functionality
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
            'grid_settings': self.grid_settings,
            'zoom_factor': self.zoom_factor
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
            self.clear_canvas()
            
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
    
    # Utility methods
    def export_canvas_image(self, filename):
        """Export canvas as image"""
        try:
            # Get scene bounding rect
            scene_rect = self.scene.itemsBoundingRect()
            if scene_rect.isEmpty():
                scene_rect = QRectF(-500, -500, 1000, 1000)
            
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
            
        except Exception as e:
            print(f"❌ Error exporting canvas: {e}")
    
    def get_canvas_statistics(self):
        """Get canvas statistics"""
        stats = {
            'total_components': len(self.components),
            'component_types': {},
            'total_connections': len(self.connections),
            'canvas_bounds': self.scene.itemsBoundingRect(),
            'zoom_level': self.zoom_factor
        }
        
        # Count component types
        for component in self.components.values():
            category = component.category
            stats['component_types'][category] = stats['component_types'].get(category, 0) + 1
        
        return stats
    
    # Compatibility methods
    def delete_selected(self):
        """Delete selected components"""
        self.delete_selected_components()
    
    def select_all(self):
        """Select all components"""
        self.select_all_components()
    
    def save_canvas(self):
        """Save canvas to file"""
        print("💾 Canvas save functionality - use save_canvas_state()")
    
    def open_canvas(self):
        """Open canvas from file"""
        print("📁 Canvas open functionality - use load_canvas_state()")

# For compatibility
PCBCanvas = EnhancedPCBCanvas

# Export
__all__ = ['EnhancedPCBCanvas', 'PCBCanvas', 'GridSettingsDialog', 'ComponentItem']