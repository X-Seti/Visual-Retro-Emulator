"""
X-Seti - June14 2025 - COMPLETE Layer Controls with ALL Original + New Features
Full implementation including LayerItem, LayerListWidget, Grid Settings, Quick Modes
COMPLETE: All original layer management + Grid Settings + Quick Modes + Color management
"""

#this belongs in ui/ layer_controls.py

import os
from enum import Enum
from typing import Dict, List, Optional, Any
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                           QPushButton, QCheckBox, QComboBox, QSlider, QSpinBox,
                           QLabel, QListWidget, QListWidgetItem, QColorDialog,
                           QLineEdit, QMessageBox, QButtonGroup, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QPixmap, QPainter, QBrush, QIcon

# === ENUMS FOR GRID SETTINGS ===
class GridStyle(Enum):
    """Grid style options"""
    DOTS = "dots"
    LINES = "lines"
    CROSSES = "crosses"
    BREADBOARD = "breadboard"

class GridSpacing(Enum):
    """Grid spacing presets"""
    FINE = "Fine (2.54mm)"
    MEDIUM = "Medium (5.08mm)" 
    COARSE = "Coarse (10.16mm)"
    CUSTOM = "Custom"

class QuickMode(Enum):
    """Quick mode presets"""
    BREADBOARD = "breadboard"
    PCB_DESIGN = "pcb_design"
    SCHEMATIC = "schematic"
    FREEFORM = "freeform"

# === LAYER DATA STRUCTURES ===
class LayerItem:
    """Represents a single layer with complete properties"""
    
    def __init__(self, name: str, visible: bool = True, color: QColor = None, opacity: float = 1.0):
        self.name = name
        self.visible = visible
        self.color = color or QColor(255, 107, 53)  # Default orange
        self.opacity = opacity
        self.locked = False
        self.layer_type = "general"  # general, component, connection, annotation, background
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'name': self.name,
            'visible': self.visible,
            'color': self.color.name(),
            'opacity': self.opacity,
            'locked': self.locked,
            'layer_type': self.layer_type
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LayerItem':
        """Create from dictionary"""
        layer = cls(
            data['name'],
            data.get('visible', True),
            QColor(data.get('color', '#FF6B35')),
            data.get('opacity', 1.0)
        )
        layer.locked = data.get('locked', False)
        layer.layer_type = data.get('layer_type', 'general')
        return layer

class LayerListWidget(QListWidget):
    """Custom list widget for comprehensive layer management"""
    
    layerVisibilityChanged = pyqtSignal(str, bool)  # layer_name, visible
    layerSelected = pyqtSignal(str)  # layer_name
    layerRenamed = pyqtSignal(str, str)  # old_name, new_name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layers: Dict[str, LayerItem] = {}
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.itemChanged.connect(self.on_item_changed)
        self.itemClicked.connect(self.on_item_clicked)
        
    def add_layer(self, layer: LayerItem):
        """Add a layer to the list"""
        self.layers[layer.name] = layer
        self.refresh_display()
        
    def remove_layer(self, name: str):
        """Remove a layer"""
        if name in self.layers:
            del self.layers[name]
            self.refresh_display()
            
    def get_layer(self, name: str) -> Optional[LayerItem]:
        """Get layer by name"""
        return self.layers.get(name)
        
    def set_layer_visibility(self, name: str, visible: bool):
        """Set layer visibility"""
        if name in self.layers:
            self.layers[name].visible = visible
            self.refresh_display()
            self.layerVisibilityChanged.emit(name, visible)
            
    def refresh_display(self):
        """Refresh the layer list display"""
        self.clear()
        
        for layer in self.layers.values():
            item = QListWidgetItem()
            item.setText(layer.name)
            item.setData(Qt.ItemDataRole.UserRole, layer.name)
            
            # Set checkbox for visibility
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if layer.visible else Qt.CheckState.Unchecked)
            
            # Create color icon
            color_icon = self.create_color_icon(layer.color, layer.opacity)
            item.setIcon(color_icon)
            
            # Gray out if locked
            if layer.locked:
                item.setBackground(QColor(220, 220, 220))
                
            self.addItem(item)
            
    def create_color_icon(self, color: QColor, opacity: float = 1.0) -> QIcon:
        """Create a color icon for the layer"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setOpacity(opacity)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(2, 2, 12, 12)
        painter.end()
        
        return QIcon(pixmap)
        
    def on_item_changed(self, item: QListWidgetItem):
        """Handle item changes"""
        layer_name = item.data(Qt.ItemDataRole.UserRole)
        if layer_name in self.layers:
            # Check if visibility changed
            is_checked = item.checkState() == Qt.CheckState.Checked
            if self.layers[layer_name].visible != is_checked:
                self.set_layer_visibility(layer_name, is_checked)
                
    def on_item_clicked(self, item: QListWidgetItem):
        """Handle item clicks"""
        layer_name = item.data(Qt.ItemDataRole.UserRole)
        self.layerSelected.emit(layer_name)

class LayerControls(QWidget):
    """
    COMPLETE Layer Controls Widget with ALL Features
    
    Includes:
    - Original comprehensive layer management (LayerItem, LayerListWidget)
    - NEW: Grid Settings with style, spacing, visibility, snap-to-grid
    - NEW: Quick Modes (Breadboard, PCB Design, Schematic, Freeform)
    - Color management, opacity controls, layer properties
    - Complete signal system for main window integration
    """
    
    # === ALL SIGNALS FOR COMPLETE INTEGRATION ===
    # Grid signals (NEW)
    gridStyleChanged = pyqtSignal(GridStyle)  # style
    gridSpacingChanged = pyqtSignal(GridSpacing, float)  # spacing_type, custom_value
    gridVisibilityChanged = pyqtSignal(bool)  # visible
    snapToGridChanged = pyqtSignal(bool)  # enabled
    quickModeChanged = pyqtSignal(QuickMode)  # mode
    
    # Layer signals (ORIGINAL)
    layerAdded = pyqtSignal(str)  # layer_name
    layerRemoved = pyqtSignal(str)  # layer_name
    layerVisibilityChanged = pyqtSignal(str, bool)  # layer_name, visible
    layerPropertiesChanged = pyqtSignal(str, dict)  # layer_name, properties
    layerChanged = pyqtSignal(str)  # layer_name
    currentLayerChanged = pyqtSignal(str)  # layer_name
    layerSelected = pyqtSignal(str)  # layer_name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = None  # Will be set by main window
        
        # Grid state (NEW)
        self.current_grid_style = GridStyle.BREADBOARD
        self.current_grid_spacing = GridSpacing.FINE
        self.current_custom_spacing = 2.54
        self.grid_visible = True
        self.snap_to_grid = True
        self.current_quick_mode = QuickMode.BREADBOARD
        
        # Layer state (ORIGINAL)
        self.current_layer: Optional[str] = None
        self.property_editors = {}
        
        self._setup_ui()
        self._create_default_layers()
        self._connect_signals()
        
        print("✓ COMPLETE Layer Controls initialized with ALL features")
    
    def _setup_ui(self):
        """Setup the complete UI layout with all sections"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)
        
        # === NEW: GRID SETTINGS GROUP (Top Section) ===
        self._create_grid_settings_group(layout)
        
        # === NEW: QUICK MODES GROUP ===
        self._create_quick_modes_group(layout)
        
        # === ORIGINAL: LAYERS GROUP ===
        self._create_layers_group(layout)
        
        # === ORIGINAL: LAYER PROPERTIES GROUP ===
        self._create_layer_properties_group(layout)
        
        # === ORIGINAL: GLOBAL CONTROLS GROUP ===
        self._create_global_controls_group(layout)
        
        layout.addStretch()  # Push everything to top
    
    def _create_grid_settings_group(self, parent_layout):
        """Create Grid Settings group (NEW)"""
        grid_group = QGroupBox("Grid Settings")
        grid_layout = QVBoxLayout(grid_group)
        
        # Show Grid checkbox
        self.show_grid_check = QCheckBox("Show Grid")
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
        
        # Custom spacing input (initially hidden)
        self.custom_spacing_layout = QHBoxLayout()
        self.custom_spacing_layout.addWidget(QLabel("Custom (mm):"))
        self.custom_spacing_spin = QSpinBox()
        self.custom_spacing_spin.setRange(1, 50)
        self.custom_spacing_spin.setValue(int(self.current_custom_spacing))
        self.custom_spacing_spin.setSuffix(" mm")
        self.custom_spacing_spin.valueChanged.connect(self._on_custom_spacing_changed)
        self.custom_spacing_layout.addWidget(self.custom_spacing_spin)
        grid_layout.addLayout(self.custom_spacing_layout)
        self._hide_custom_spacing()
        
        # Snap to Grid checkbox
        self.snap_to_grid_check = QCheckBox("Snap to Grid")
        self.snap_to_grid_check.setChecked(self.snap_to_grid)
        self.snap_to_grid_check.toggled.connect(self._on_snap_to_grid_changed)
        grid_layout.addWidget(self.snap_to_grid_check)
        
        parent_layout.addWidget(grid_group)
    
    def _create_quick_modes_group(self, parent_layout):
        """Create Quick Modes group (NEW)"""
        modes_group = QGroupBox("Quick Modes")
        modes_layout = QVBoxLayout(modes_group)
        
        # Create button group for exclusive selection
        self.mode_button_group = QButtonGroup()
        
        # Mode buttons with icons/colors
        mode_configs = [
            ("🍞 Breadboard", QuickMode.BREADBOARD, "#8B4513"),
            ("🔧 PCB Design", QuickMode.PCB_DESIGN, "#228B22"),
            ("📋 Schematic", QuickMode.SCHEMATIC, "#4682B4"),
            ("🎨 Freeform", QuickMode.FREEFORM, "#9370DB")
        ]
        
        for i, (text, mode, color) in enumerate(mode_configs):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding: 8px 12px;
                    border: 2px solid #555;
                    border-radius: 4px;
                    background-color: #3C3C3C;
                }}
                QPushButton:checked {{
                    background-color: {color};
                    color: white;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    border-color: {color};
                }}
            """)
            
            # Set default selection
            if mode == self.current_quick_mode:
                btn.setChecked(True)
            
            btn.clicked.connect(lambda checked, m=mode: self._on_quick_mode_changed(m))
            self.mode_button_group.addButton(btn, i)
            modes_layout.addWidget(btn)
        
        parent_layout.addWidget(modes_group)
    
    def _create_layers_group(self, parent_layout):
        """Create Layers group (ORIGINAL)"""
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
        """Create Layer Properties group (ORIGINAL)"""
        props_group = QGroupBox("Layer Properties")
        props_layout = QVBoxLayout(props_group)
        
        # Layer name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.layer_name_edit = QLineEdit()
        self.layer_name_edit.textChanged.connect(self.on_layer_name_changed)
        name_layout.addWidget(self.layer_name_edit)
        props_layout.addLayout(name_layout)
        
        # Position info (read-only display) - FROM SCREENSHOT
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("Position:"))
        self.position_label = QLabel("PyQt6.QtCore.QPointF(-60.0, -140.0)")
        self.position_label.setStyleSheet("color: #888; font-family: monospace;")
        position_layout.addWidget(self.position_label)
        props_layout.addLayout(position_layout)
        
        # Size info (read-only display) - FROM SCREENSHOT
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.size_label = QLabel("PyQt6.QtCore.QSizeF(82.0, 42.0)")
        self.size_label.setStyleSheet("color: #888; font-family: monospace;")
        size_layout.addWidget(self.size_label)
        props_layout.addLayout(size_layout)
        
        # Layer color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_button = QPushButton()
        self.color_button.setFixedSize(50, 25)
        self.color_button.clicked.connect(self.choose_layer_color)
        color_layout.addWidget(self.color_button)
        color_layout.addStretch()
        props_layout.addLayout(color_layout)
        
        # Layer opacity
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Opacity:"))
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        self.opacity_spinbox = QSpinBox()
        self.opacity_spinbox.setRange(0, 100)
        self.opacity_spinbox.setValue(100)
        self.opacity_spinbox.setSuffix("%")
        self.opacity_spinbox.valueChanged.connect(self.opacity_slider.setValue)
        self.opacity_slider.valueChanged.connect(self.opacity_spinbox.setValue)
        
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_spinbox)
        props_layout.addLayout(opacity_layout)
        
        # Layer type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.layer_type_combo = QComboBox()
        self.layer_type_combo.addItems(["General", "Components", "Connections", "Annotations", "Background"])
        self.layer_type_combo.currentTextChanged.connect(self.on_layer_type_changed)
        type_layout.addWidget(self.layer_type_combo)
        props_layout.addLayout(type_layout)
        
        # Lock layer
        self.lock_layer_check = QCheckBox("Lock Layer")
        self.lock_layer_check.toggled.connect(self.on_layer_lock_changed)
        props_layout.addWidget(self.lock_layer_check)
        
        parent_layout.addWidget(props_group)
    
    def _create_global_controls_group(self, parent_layout):
        """Create Global Controls group (ORIGINAL)"""
        global_group = QGroupBox("Global Controls")
        global_layout = QVBoxLayout(global_group)
        
        global_buttons_layout = QHBoxLayout()
        self.show_all_btn = QPushButton("Show All")
        self.hide_all_btn = QPushButton("Hide All")
        self.reset_layers_btn = QPushButton("Reset")
        
        self.show_all_btn.clicked.connect(self.show_all_layers)
        self.hide_all_btn.clicked.connect(self.hide_all_layers)
        self.reset_layers_btn.clicked.connect(self.reset_layers)
        
        global_buttons_layout.addWidget(self.show_all_btn)
        global_buttons_layout.addWidget(self.hide_all_btn)
        global_buttons_layout.addWidget(self.reset_layers_btn)
        global_layout.addLayout(global_buttons_layout)
        
        parent_layout.addWidget(global_group)
    
    def _create_default_layers(self):
        """Create default layers (ORIGINAL)"""
        default_layers = [
            LayerItem("Background", True, QColor(45, 45, 48), 1.0),
            LayerItem("Components", True, QColor(255, 107, 53), 1.0),
            LayerItem("Connections", True, QColor(78, 205, 196), 1.0)
        ]
        
        for layer in default_layers:
            self.layer_list.add_layer(layer)
        
        # Set first layer as current
        if default_layers:
            self.current_layer = default_layers[1].name  # Components
            self.layer_list.setCurrentRow(1)
            self.on_layer_selected(self.current_layer)
    
    def _connect_signals(self):
        """Connect internal signals (ORIGINAL)"""
        # Auto-update timer for properties display
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_layer_properties_display)
        self.update_timer.start(1000)  # Update every second
    
    # ========== NEW: GRID SIGNAL HANDLERS ==========
    def _on_grid_visibility_changed(self, visible: bool):
        """Handle grid visibility change"""
        self.grid_visible = visible
        print(f"🔍 Grid visibility changed: {visible}")
        self.gridVisibilityChanged.emit(visible)
    
    def _on_grid_style_changed(self, style_text: str):
        """Handle grid style change"""
        style_map = {
            "Dots": GridStyle.DOTS,
            "Lines": GridStyle.LINES, 
            "Crosses": GridStyle.CROSSES,
            "Breadboard": GridStyle.BREADBOARD
        }
        
        if style_text in style_map:
            self.current_grid_style = style_map[style_text]
            print(f"🎨 Grid style changed: {self.current_grid_style.value}")
            self.gridStyleChanged.emit(self.current_grid_style)
    
    def _on_grid_spacing_changed(self, spacing_text: str):
        """Handle grid spacing change"""
        spacing_map = {
            "Fine (2.54mm)": GridSpacing.FINE,
            "Medium (5.08mm)": GridSpacing.MEDIUM,
            "Coarse (10.16mm)": GridSpacing.COARSE,
            "Custom": GridSpacing.CUSTOM
        }
        
        if spacing_text in spacing_map:
            self.current_grid_spacing = spacing_map[spacing_text]
            
            # Show/hide custom spacing input
            if self.current_grid_spacing == GridSpacing.CUSTOM:
                self._show_custom_spacing()
            else:
                self._hide_custom_spacing()
            
            print(f"📏 Grid spacing changed: {self.current_grid_spacing.value}")
            self.gridSpacingChanged.emit(self.current_grid_spacing, self.current_custom_spacing)
    
    def _on_custom_spacing_changed(self, value: int):
        """Handle custom spacing value change"""
        self.current_custom_spacing = float(value)
        if self.current_grid_spacing == GridSpacing.CUSTOM:
            print(f"📏 Custom grid spacing: {self.current_custom_spacing}mm")
            self.gridSpacingChanged.emit(self.current_grid_spacing, self.current_custom_spacing)
    
    def _on_snap_to_grid_changed(self, enabled: bool):
        """Handle snap to grid change"""
        self.snap_to_grid = enabled
        print(f"🧲 Snap to grid: {enabled}")
        self.snapToGridChanged.emit(enabled)
    
    def _on_quick_mode_changed(self, mode: QuickMode):
        """Handle quick mode change"""
        self.current_quick_mode = mode
        print(f"⚡ Quick mode changed: {mode.value}")
        
        # Apply mode-specific settings
        self._apply_quick_mode_settings(mode)
        self.quickModeChanged.emit(mode)
    
    # ========== ORIGINAL: LAYER SIGNAL HANDLERS ==========
    def add_new_layer(self):
        """Add a new layer"""
        layer_name = f"Layer {len(self.layer_list.layers) + 1}"
        counter = 1
        while layer_name in self.layer_list.layers:
            layer_name = f"Layer {len(self.layer_list.layers) + counter}"
            counter += 1
        
        new_layer = LayerItem(layer_name, True, QColor(255, 107, 53), 1.0)
        self.layer_list.add_layer(new_layer)
        self.layerAdded.emit(layer_name)
        print(f"➕ Added layer: {layer_name}")
    
    def remove_selected_layer(self):
        """Remove the selected layer"""
        current_item = self.layer_list.currentItem()
        if current_item and len(self.layer_list.layers) > 1:
            layer_name = current_item.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(self, "Confirm", f"Remove layer '{layer_name}'?")
            if reply == QMessageBox.StandardButton.Yes:
                self.layer_list.remove_layer(layer_name)
                self.layerRemoved.emit(layer_name)
                self.enable_properties(False)
                print(f"➖ Removed layer: {layer_name}")
                
    def duplicate_selected_layer(self):
        """Duplicate the selected layer"""
        current_item = self.layer_list.currentItem()
        if current_item:
            layer_name = current_item.data(Qt.ItemDataRole.UserRole)
            original_layer = self.layer_list.get_layer(layer_name)
            
            if original_layer:
                new_name = f"{layer_name}_copy"
                counter = 1
                while new_name in self.layer_list.layers:
                    new_name = f"{layer_name}_copy_{counter}"
                    counter += 1
                    
                new_layer = LayerItem(
                    new_name,
                    original_layer.visible,
                    QColor(original_layer.color),
                    original_layer.opacity
                )
                new_layer.layer_type = original_layer.layer_type
                self.layer_list.add_layer(new_layer)
                self.layerAdded.emit(new_name)
                print(f"📋 Duplicated layer: {layer_name} -> {new_name}")
                
    def on_layer_visibility_changed(self, layer_name: str, visible: bool):
        """Handle layer visibility change"""
        self.layerVisibilityChanged.emit(layer_name, visible)
        print(f"👁️ Layer '{layer_name}' visibility: {visible}")
        
    def on_layer_selected(self, layer_name: str):
        """Handle layer selection"""
        self.current_layer = layer_name
        layer = self.layer_list.get_layer(layer_name)
        
        if layer:
            self.enable_properties(True)
            self.update_properties_display(layer)
        else:
            self.enable_properties(False)
            
        # Emit BOTH signals that main_window.py might be looking for
        self.layerChanged.emit(layer_name)
        self.currentLayerChanged.emit(layer_name)
        self.layerSelected.emit(layer_name)
        print(f"🎯 Layer selected: {layer_name}")
            
    def update_properties_display(self, layer: LayerItem):
        """Update properties display for selected layer"""
        self.layer_name_edit.setText(layer.name)
        self.update_color_button(layer.color)
        self.opacity_slider.setValue(int(layer.opacity * 100))
        
        # Set layer type
        type_text = layer.layer_type.title()
        index = self.layer_type_combo.findText(type_text)
        if index >= 0:
            self.layer_type_combo.setCurrentIndex(index)
            
        self.lock_layer_check.setChecked(layer.locked)
        
    def update_color_button(self, color: QColor):
        """Update color button appearance"""
        self.color_button.setStyleSheet(f"background-color: {color.name()};")
        
    def enable_properties(self, enabled: bool):
        """Enable/disable property controls"""
        self.layer_name_edit.setEnabled(enabled)
        self.color_button.setEnabled(enabled)
        self.opacity_slider.setEnabled(enabled)
        self.opacity_spinbox.setEnabled(enabled)
        self.layer_type_combo.setEnabled(enabled)
        self.lock_layer_check.setEnabled(enabled)
        
    def on_layer_name_changed(self, new_name: str):
        """Handle layer name change"""
        if self.current_layer and new_name:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer and layer.name != new_name:
                # Check if name already exists
                if new_name in self.layer_list.layers:
                    QMessageBox.warning(self, "Warning", "Layer with this name already exists")
                    self.layer_name_edit.setText(layer.name)  # Revert
                    return
                    
                old_name = layer.name
                layer.name = new_name
                
                # Update layer list
                self.layer_list.layers[new_name] = self.layer_list.layers.pop(old_name)
                self.layer_list.refresh_display()
                self.current_layer = new_name
                
                self.layer_list.layerRenamed.emit(old_name, new_name)
                self.layerChanged.emit(new_name)
                print(f"📝 Layer renamed: {old_name} -> {new_name}")
                
    def choose_layer_color(self):
        """Choose layer color"""
        if self.current_layer:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer:
                color = QColorDialog.getColor(layer.color, self)
                if color.isValid():
                    layer.color = color
                    self.update_color_button(color)
                    self.layer_list.refresh_display()
                    self.emit_layer_properties_changed()
                    print(f"🎨 Layer color changed: {color.name()}")
                    
    def on_opacity_changed(self, value: int):
        """Handle opacity change"""
        if self.current_layer:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer:
                layer.opacity = value / 100.0
                self.layer_list.refresh_display()
                self.emit_layer_properties_changed()
                print(f"💫 Layer opacity changed: {value}%")
                
    def on_layer_type_changed(self, type_text: str):
        """Handle layer type change"""
        if self.current_layer:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer:
                layer.layer_type = type_text.lower()
                self.emit_layer_properties_changed()
                print(f"🏷️ Layer type changed: {type_text}")
                
    def on_layer_lock_changed(self, locked: bool):
        """Handle layer lock change"""
        if self.current_layer:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer:
                layer.locked = locked
                self.layer_list.refresh_display()
                self.emit_layer_properties_changed()
                print(f"🔒 Layer lock changed: {locked}")
                
    def emit_layer_properties_changed(self):
        """Emit layer properties changed signal"""
        if self.current_layer:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer:
                self.layerPropertiesChanged.emit(self.current_layer, layer.to_dict())
                
    def show_all_layers(self):
        """Show all layers"""
        for layer_name in self.layer_list.layers:
            self.layer_list.set_layer_visibility(layer_name, True)
        print("👁️ All layers shown")
            
    def hide_all_layers(self):
        """Hide all layers"""
        for layer_name in self.layer_list.layers:
            self.layer_list.set_layer_visibility(layer_name, False)
        print("🙈 All layers hidden")
            
    def reset_layers(self):
        """Reset to default layers"""
        reply = QMessageBox.question(self, "Confirm", "Reset all layers to default?")
        if reply == QMessageBox.StandardButton.Yes:
            self.layer_list.layers.clear()
            self._create_default_layers()
            self.enable_properties(False)
            self.current_layer = None
            print("🔄 Layers reset to default")
    
    # ========== NEW: GRID UTILITY METHODS ==========
    def _show_custom_spacing(self):
        """Show custom spacing controls"""
        for i in range(self.custom_spacing_layout.count()):
            widget = self.custom_spacing_layout.itemAt(i).widget()
            if widget:
                widget.show()
    
    def _hide_custom_spacing(self):
        """Hide custom spacing controls"""
        for i in range(self.custom_spacing_layout.count()):
            widget = self.custom_spacing_layout.itemAt(i).widget()
            if widget:
                widget.hide()
    
    def _apply_quick_mode_settings(self, mode: QuickMode):
        """Apply settings for the selected quick mode"""
        mode_settings = {
            QuickMode.BREADBOARD: {
                "grid_style": "Breadboard",
                "grid_spacing": "Fine (2.54mm)",
                "grid_visible": True,
                "snap_to_grid": True
            },
            QuickMode.PCB_DESIGN: {
                "grid_style": "Lines", 
                "grid_spacing": "Fine (2.54mm)",
                "grid_visible": True,
                "snap_to_grid": True
            },
            QuickMode.SCHEMATIC: {
                "grid_style": "Dots",
                "grid_spacing": "Medium (5.08mm)",
                "grid_visible": True, 
                "snap_to_grid": True
            },
            QuickMode.FREEFORM: {
                "grid_style": "Dots",
                "grid_spacing": "Coarse (10.16mm)",
                "grid_visible": False,
                "snap_to_grid": False
            }
        }
        
        if mode in mode_settings:
            settings = mode_settings[mode]
            
            # Update controls without triggering signals
            self.grid_style_combo.blockSignals(True)
            self.grid_spacing_combo.blockSignals(True)
            self.show_grid_check.blockSignals(True)
            self.snap_to_grid_check.blockSignals(True)
            
            self.grid_style_combo.setCurrentText(settings["grid_style"])
            self.grid_spacing_combo.setCurrentText(settings["grid_spacing"])
            self.show_grid_check.setChecked(settings["grid_visible"])
            self.snap_to_grid_check.setChecked(settings["snap_to_grid"])
            
            self.grid_style_combo.blockSignals(False)
            self.grid_spacing_combo.blockSignals(False)
            self.show_grid_check.blockSignals(False)
            self.snap_to_grid_check.blockSignals(False)
            
            # Emit the signals manually to update canvas
            self._on_grid_style_changed(settings["grid_style"])
            self._on_grid_spacing_changed(settings["grid_spacing"])
            self._on_grid_visibility_changed(settings["grid_visible"])
            self._on_snap_to_grid_changed(settings["snap_to_grid"])
    
    def _update_layer_properties_display(self):
        """Update the layer properties display with current canvas state"""
        # This would typically get data from the canvas
        # For now, show placeholder data
        pass
    
    # ========== PUBLIC API METHODS FOR MAIN WINDOW ==========
    def set_canvas(self, canvas):
        """Set the canvas reference for integration"""
        self.canvas = canvas
        print("✓ Canvas reference set in layer controls")
    
    def get_grid_settings(self) -> Dict[str, Any]:
        """Get current grid settings"""
        return {
            "style": self.current_grid_style,
            "spacing": self.current_grid_spacing,
            "custom_spacing": self.current_custom_spacing,
            "visible": self.grid_visible,
            "snap_to_grid": self.snap_to_grid
        }
    
    def get_layer_settings(self) -> Dict[str, Any]:
        """Get current layer settings"""
        return {
            "layers": {name: layer.to_dict() for name, layer in self.layer_list.layers.items()},
            "current_layer": self.current_layer
        }
    
    def update_component_info(self, position: str, size: str):
        """Update component info display (called from main window)"""
        self.position_label.setText(position)
        self.size_label.setText(size)
    
    def get_layer_visibility(self, layer_name: str) -> bool:
        """Get layer visibility"""
        layer = self.layer_list.get_layer(layer_name)
        return layer.visible if layer else True
        
    def set_layer_visibility(self, layer_name: str, visible: bool):
        """Set layer visibility"""
        self.layer_list.set_layer_visibility(layer_name, visible)
        
    def get_all_layers(self) -> Dict[str, LayerItem]:
        """Get all layers"""
        return self.layer_list.layers.copy()

# Backward compatibility aliases
LayerControlsWidget = LayerControls  # Original name

# Export
__all__ = ['LayerControls', 'LayerControlsWidget', 'LayerItem', 'LayerListWidget', 'GridStyle', 'GridSpacing', 'QuickMode']
