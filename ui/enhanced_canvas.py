"""
X-Seti - June16 2025 - Layer Controls without duplicate Components section
Visual Retro System Emulator Builder - Layer & Grid Controls only
"""

#this belongs in ui/layer_controls.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                           QCheckBox, QComboBox, QLabel, QPushButton, 
                           QListWidget, QListWidgetItem, QLineEdit, 
                           QSpinBox, QDoubleSpinBox, QSlider, QButtonGroup,
                           QRadioButton, QFrame, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QFont

# Import theme system
try:
    from utils.App_settings_system import AppSettings
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False
    print("⚠️ Theme system not available for layer controls")

class LayerListWidget(QListWidget):
    """Custom list widget for layers"""
    
    layerVisibilityChanged = pyqtSignal(str, bool)
    layerSelected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumHeight(100)
        self.itemChanged.connect(self._on_item_changed)
        self.itemSelectionChanged.connect(self._on_selection_changed)
    
    def _on_item_changed(self, item):
        """Handle item state change"""
        layer_name = item.text()
        is_visible = item.checkState() == Qt.CheckState.Checked
        self.layerVisibilityChanged.emit(layer_name, is_visible)
    
    def _on_selection_changed(self):
        """Handle selection change"""
        current_item = self.currentItem()
        if current_item:
            self.layerSelected.emit(current_item.text())

class LayerControls(QWidget):
    """
    Layer Controls Widget - Grid and Layer management only
    
    FIXED:
    ✅ Removed duplicate Components section
    ✅ Focus on Layers and Grid functionality only
    ✅ Proper theming integration
    ✅ Clean, organized layout
    """
    
    # Grid signals
    gridVisibilityChanged = pyqtSignal(bool)
    gridStyleChanged = pyqtSignal(str)
    gridSpacingChanged = pyqtSignal(float)
    snapToGridChanged = pyqtSignal(bool)
    
    # Layer signals
    layerAdded = pyqtSignal(str)
    layerRemoved = pyqtSignal(str)
    layerVisibilityChanged = pyqtSignal(str, bool)
    layerSelected = pyqtSignal(str)
    layerRenamed = pyqtSignal(str, str)
    
    # Mode signals
    modeChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize theme system
        self.app_settings = None
        if THEME_AVAILABLE:
            try:
                self.app_settings = AppSettings()
            except Exception as e:
                print(f"⚠️ Layer controls theme initialization failed: {e}")
        
        # State variables
        self.grid_visible = True
        self.snap_to_grid = True
        self.grid_style = "Breadboard"
        self.grid_spacing = 2.54
        self.current_mode = "Breadboard"
        
        # Layer data
        self.layers = {}
        self.current_layer = None
        
        # UI components
        self.layer_list = None
        self.layer_name_edit = None
        self.position_label = None
        self.size_label = None
        
        # Setup UI
        self._setup_ui()
        self._apply_theme()
        self._create_default_layers()
        
        print("✓ Layer Controls initialized (Components section removed)")
    
    def _get_theme_color(self, color_name, fallback="#ffffff"):
        """Get theme color with fallback"""
        if self.app_settings:
            try:
                return self.app_settings.get_color(color_name)
            except:
                pass
        return fallback
    
    def _setup_ui(self):
        """Setup the UI layout - Grid and Layers only"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)
        
        # === GRID SETTINGS GROUP ===
        self._create_grid_settings_group(layout)
        
        # === QUICK MODES GROUP ===
        self._create_quick_modes_group(layout)
        
        # === LAYERS GROUP ===
        self._create_layers_group(layout)
        
        # === LAYER PROPERTIES GROUP ===
        self._create_layer_properties_group(layout)
        
        layout.addStretch()  # Push everything to top
    
    def _create_grid_settings_group(self, parent_layout):
        """Create Grid Settings group"""
        grid_group = QGroupBox("Grid Settings")
        grid_layout = QVBoxLayout(grid_group)
        
        # Show Grid checkbox
        self.show_grid_check = QCheckBox("✓ Show Grid")
        self.show_grid_check.setChecked(self.grid_visible)
        self.show_grid_check.toggled.connect(self._on_grid_visibility_changed)
        grid_layout.addWidget(self.show_grid_check)
        
        # Grid Style
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Grid Style:"))
        self.grid_style_combo = QComboBox()
        self.grid_style_combo.addItems(["Dots", "Lines", "Crosses", "Breadboard"])
        self.grid_style_combo.setCurrentText("Breadboard")
        self.grid_style_combo.currentTextChanged.connect(self._on_grid_style_changed)
        style_layout.addWidget(self.grid_style_combo)
        grid_layout.addLayout(style_layout)
        
        # Grid Spacing
        spacing_layout = QHBoxLayout()
        spacing_layout.addWidget(QLabel("Spacing:"))
        self.grid_spacing_combo = QComboBox()
        self.grid_spacing_combo.addItems([
            "Fine (2.54mm)", "Medium (5.08mm)", "Coarse (10.16mm)", "Custom"
        ])
        self.grid_spacing_combo.setCurrentText("Fine (2.54mm)")
        self.grid_spacing_combo.currentTextChanged.connect(self._on_grid_spacing_changed)
        spacing_layout.addWidget(self.grid_spacing_combo)
        grid_layout.addLayout(spacing_layout)
        
        # Snap to Grid
        self.snap_grid_check = QCheckBox("✓ Snap to Grid")
        self.snap_grid_check.setChecked(self.snap_to_grid)
        self.snap_grid_check.toggled.connect(self._on_snap_changed)
        grid_layout.addWidget(self.snap_grid_check)
        
        parent_layout.addWidget(grid_group)
    
    def _create_quick_modes_group(self, parent_layout):
        """Create Quick Modes group"""
        modes_group = QGroupBox("Quick Modes")
        modes_layout = QVBoxLayout(modes_group)
        
        # Mode buttons
        self.mode_button_group = QButtonGroup(self)
        self.mode_button_group.buttonClicked.connect(self._on_mode_changed)
        
        modes = [
            ("🔧 Breadboard", "Breadboard"),
            ("🔌 PCB Design", "PCB"),
            ("📐 Schematic", "Schematic"),
            ("🎨 Freeform", "Freeform")
        ]
        
        for i, (text, mode) in enumerate(modes):
            btn = QRadioButton(text)
            if mode == "Breadboard":
                btn.setChecked(True)
            btn.mode = mode
            btn.toggled.connect(lambda checked, m=mode: self._on_quick_mode_changed(m))
            self.mode_button_group.addButton(btn, i)
            modes_layout.addWidget(btn)
        
        parent_layout.addWidget(modes_group)
    
    def _create_layers_group(self, parent_layout):
        """Create Layers group"""
        layers_group = QGroupBox("Layers")
        layers_layout = QVBoxLayout(layers_group)
        
        # Layer list
        self.layer_list = LayerListWidget()
        self.layer_list.setMaximumHeight(120)
        self.layer_list.layerVisibilityChanged.connect(self.on_layer_visibility_changed)
        self.layer_list.layerSelected.connect(self.on_layer_selected)
        layers_layout.addWidget(self.layer_list)
        
        # Layer control buttons
        buttons_layout = QHBoxLayout()
        self.add_layer_btn = QPushButton("Add")
        self.remove_layer_btn = QPushButton("Remove")
        self.duplicate_layer_btn = QPushButton("Duplicate")
        
        self.add_layer_btn.clicked.connect(self.add_new_layer)
        self.remove_layer_btn.clicked.connect(self.remove_selected_layer)
        self.duplicate_layer_btn.clicked.connect(self.duplicate_selected_layer)
        
        buttons_layout.addWidget(self.add_layer_btn)
        buttons_layout.addWidget(self.remove_layer_btn)
        buttons_layout.addWidget(self.duplicate_layer_btn)
        layers_layout.addLayout(buttons_layout)
        
        parent_layout.addWidget(layers_group)
    
    def _create_layer_properties_group(self, parent_layout):
        """Create Layer Properties group"""
        props_group = QGroupBox("Layer Properties")
        props_layout = QVBoxLayout(props_group)
        
        # Layer name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.layer_name_edit = QLineEdit()
        self.layer_name_edit.textChanged.connect(self.on_layer_name_changed)
        name_layout.addWidget(self.layer_name_edit)
        props_layout.addLayout(name_layout)
        
        # Position info (read-only display)
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("Position:"))
        self.position_label = QLabel("PyQt6.QtCore.QPointF(-60.0, -140.0)")
        self.position_label.setStyleSheet("font-family: monospace; font-size: 8px;")
        position_layout.addWidget(self.position_label)
        props_layout.addLayout(position_layout)
        
        # Size info (read-only display)
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.size_label = QLabel("PyQt6.QtCore.QSizeF(8.40, 0.53x6f(8.40)")
        self.size_label.setStyleSheet("font-family: monospace; font-size: 8px;")
        size_layout.addWidget(self.size_label)
        props_layout.addLayout(size_layout)
        
        parent_layout.addWidget(props_group)
    
    def _apply_theme(self):
        """Apply theme colors to layer controls"""
        if not self.app_settings:
            self._apply_fallback_theme()
            return
        
        try:
            # Get theme colors
            bg_primary = self._get_theme_color("bg_primary", "#2c3e50")
            bg_secondary = self._get_theme_color("bg_secondary", "#34495e")
            text_primary = self._get_theme_color("text_primary", "#ffffff")
            text_secondary = self._get_theme_color("text_secondary", "#bdc3c7")
            panel_bg = self._get_theme_color("panel_bg", "#2c3e50")
            border = self._get_theme_color("border", "#7f8c8d")
            accent_primary = self._get_theme_color("accent_primary", "#3498db")
            
            # Apply theme stylesheet
            theme_style = f"""
            QWidget {{
                background-color: {bg_primary};
                color: {text_primary};
                font-family: "Segoe UI", Arial, sans-serif;
            }}
            
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {border};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 8px;
                background-color: {panel_bg};
                color: {text_primary};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: {text_primary};
                background-color: {bg_primary};
            }}
            
            QCheckBox {{
                color: {text_primary};
                spacing: 8px;
                font-weight: bold;
            }}
            
            QRadioButton {{
                color: {text_primary};
                spacing: 8px;
                font-weight: bold;
            }}
            
            QLabel {{
                color: {text_primary};
                background-color: transparent;
            }}
            
            QComboBox {{
                background-color: {bg_secondary};
                border: 1px solid {border};
                color: {text_primary};
                padding: 4px;
                border-radius: 4px;
                min-width: 100px;
            }}
            
            QComboBox::drop-down {{
                border: none;
                background-color: {accent_primary};
                border-radius: 2px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {bg_secondary};
                color: {text_primary};
                selection-background-color: {accent_primary};
            }}
            
            QLineEdit {{
                background-color: {bg_secondary};
                border: 1px solid {border};
                color: {text_primary};
                padding: 4px;
                border-radius: 4px;
            }}
            
            QListWidget {{
                background-color: {bg_secondary};
                border: 1px solid {border};
                color: {text_primary};
                selection-background-color: {accent_primary};
            }}
            
            QPushButton {{
                background-color: {accent_primary};
                border: 1px solid {border};
                color: {text_primary};
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 60px;
            }}
            
            QPushButton:hover {{
                background-color: {self._get_theme_color("button_hover", "#2980b9")};
            }}
            
            QPushButton:pressed {{
                background-color: {self._get_theme_color("button_pressed", "#1f618d")};
            }}
            """
            
            self.setStyleSheet(theme_style)
            print("✓ Layer controls theme applied")
            
        except Exception as e:
            print(f"⚠️ Layer controls theme application failed: {e}")
            self._apply_fallback_theme()
    
    def _apply_fallback_theme(self):
        """Apply fallback theme for layer controls"""
        fallback_style = """
        QWidget {
            background-color: #2c3e50;
            color: #ffffff;
            font-family: "Segoe UI", Arial, sans-serif;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #7f8c8d;
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 8px;
            background-color: #34495e;
            color: #ffffff;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: #ffffff;
            background-color: #2c3e50;
        }
        
        QCheckBox {
            color: #ffffff;
            spacing: 8px;
            font-weight: bold;
        }
        
        QRadioButton {
            color: #ffffff;
            spacing: 8px;
            font-weight: bold;
        }
        
        QLabel {
            color: #ffffff;
            background-color: transparent;
        }
        
        QComboBox {
            background-color: #34495e;
            border: 1px solid #7f8c8d;
            color: #ffffff;
            padding: 4px;
            border-radius: 4px;
            min-width: 100px;
        }
        
        QComboBox::drop-down {
            border: none;
            background-color: #3498db;
            border-radius: 2px;
        }
        
        QLineEdit {
            background-color: #34495e;
            border: 1px solid #7f8c8d;
            color: #ffffff;
            padding: 4px;
            border-radius: 4px;
        }
        
        QListWidget {
            background-color: #34495e;
            border: 1px solid #7f8c8d;
            color: #ffffff;
            selection-background-color: #3498db;
        }
        
        QPushButton {
            background-color: #3498db;
            border: 1px solid #7f8c8d;
            color: #ffffff;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 60px;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #1f618d;
        }
        """
        
        self.setStyleSheet(fallback_style)
        print("✓ Layer controls fallback theme applied")
    
    def _create_default_layers(self):
        """Create default layers"""
        default_layers = [
            {"name": "Background", "visible": True},
            {"name": "Connections", "visible": True},
            {"name": "Advanced", "visible": False}
        ]
        
        for layer_data in default_layers:
            self._add_layer_to_list(layer_data["name"], layer_data["visible"])
        
        # Set first layer as current
        if self.layer_list.count() > 0:
            self.layer_list.setCurrentRow(0)
            self.current_layer = "Background"
            self.layer_name_edit.setText("Background")
    
    def _add_layer_to_list(self, name, visible=True):
        """Add layer to the layer list"""
        item = QListWidgetItem(name)
        item.setCheckState(Qt.CheckState.Checked if visible else Qt.CheckState.Unchecked)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        self.layer_list.addItem(item)
        
        self.layers[name] = {
            "visible": visible,
            "locked": False,
            "opacity": 1.0
        }
    
    # Grid event handlers
    def _on_grid_visibility_changed(self, visible):
        """Handle grid visibility change"""
        self.grid_visible = visible
        self.gridVisibilityChanged.emit(visible)
        print(f"🔧 Grid visibility: {visible}")
    
    def _on_grid_style_changed(self, style):
        """Handle grid style change"""
        self.grid_style = style
        self.gridStyleChanged.emit(style)
        print(f"🔧 Grid style: {style}")
    
    def _on_grid_spacing_changed(self, spacing_text):
        """Handle grid spacing change"""
        if "Fine" in spacing_text:
            spacing = 2.54
        elif "Medium" in spacing_text:
            spacing = 5.08
        elif "Coarse" in spacing_text:
            spacing = 10.16
        else:
            spacing = 2.54
        
        self.grid_spacing = spacing
        self.gridSpacingChanged.emit(spacing)
        print(f"🔧 Grid spacing: {spacing}mm")
    
    def _on_snap_changed(self, snap):
        """Handle snap to grid change"""
        self.snap_to_grid = snap
        self.snapToGridChanged.emit(snap)
        print(f"🔧 Snap to grid: {snap}")
    
    def _on_mode_changed(self, button):
        """Handle mode button change"""
        mode = getattr(button, 'mode', 'Breadboard')
        self._on_quick_mode_changed(mode)
    
    def _on_quick_mode_changed(self, mode):
        """Handle quick mode change"""
        if hasattr(self, '_mode_changing'):
            return
        
        self._mode_changing = True
        self.current_mode = mode
        self.modeChanged.emit(mode)
        print(f"🔧 Mode changed: {mode}")
        
        # Update grid style based on mode
        if mode == "Breadboard":
            self.grid_style_combo.setCurrentText("Breadboard")
        elif mode == "PCB":
            self.grid_style_combo.setCurrentText("Dots")
        elif mode == "Schematic":
            self.grid_style_combo.setCurrentText("Lines")
        elif mode == "Freeform":
            self.show_grid_check.setChecked(False)
        
        delattr(self, '_mode_changing')
    
    # Layer event handlers
    def add_new_layer(self):
        """Add new layer"""
        layer_name = f"Layer {self.layer_list.count() + 1}"
        self._add_layer_to_list(layer_name)
        self.layerAdded.emit(layer_name)
        print(f"✓ Layer added: {layer_name}")
    
    def remove_selected_layer(self):
        """Remove selected layer"""
        current_row = self.layer_list.currentRow()
        if current_row >= 0:
            item = self.layer_list.item(current_row)
            layer_name = item.text()
            self.layer_list.takeItem(current_row)
            
            if layer_name in self.layers:
                del self.layers[layer_name]
            
            self.layerRemoved.emit(layer_name)
            print(f"✓ Layer removed: {layer_name}")
    
    def duplicate_selected_layer(self):
        """Duplicate selected layer"""
        current_row = self.layer_list.currentRow()
        if current_row >= 0:
            item = self.layer_list.item(current_row)
            original_name = item.text()
            new_name = f"{original_name} Copy"
            
            is_visible = item.checkState() == Qt.CheckState.Checked
            self._add_layer_to_list(new_name, is_visible)
            self.layerAdded.emit(new_name)
            print(f"✓ Layer duplicated: {new_name}")
    
    def on_layer_visibility_changed(self, layer_name, visible):
        """Handle layer visibility change"""
        if layer_name in self.layers:
            self.layers[layer_name]["visible"] = visible
        self.layerVisibilityChanged.emit(layer_name, visible)
        print(f"🔧 Layer '{layer_name}' visibility: {visible}")
    
    def on_layer_selected(self, layer_name):
        """Handle layer selection"""
        self.current_layer = layer_name
        self.layer_name_edit.setText(layer_name)
        self.layerSelected.emit(layer_name)
        print(f"🔧 Layer selected: {layer_name}")
    
    def on_layer_name_changed(self, new_name):
        """Handle layer name change"""
        if self.current_layer and new_name != self.current_layer:
            # Update the list item
            current_item = self.layer_list.currentItem()
            if current_item:
                old_name = current_item.text()
                current_item.setText(new_name)
                
                # Update internal data
                if old_name in self.layers:
                    self.layers[new_name] = self.layers.pop(old_name)
                
                self.layerRenamed.emit(old_name, new_name)
                self.current_layer = new_name
                print(f"🔧 Layer renamed: {old_name} → {new_name}")

# Backward compatibility
LayerControlsWidget = LayerControls

# Export
__all__ = ['LayerControls', 'LayerControlsWidget', 'LayerListWidget']
