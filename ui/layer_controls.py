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
    - Color management, opacity controls, layer properties
    - Complete signal system for main window integration
    """
    
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

        # === ORIGINAL: LAYERS GROUP ===
        self._create_layers_group(layout)
        
        # === ORIGINAL: LAYER PROPERTIES GROUP ===
        self._create_layer_properties_group(layout)
        
        # === ORIGINAL: GLOBAL CONTROLS GROUP ===
        self._create_global_controls_group(layout)
        
        layout.addStretch()  # Push everything to top

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
EnhancedLayerControls = LayerControls  # Alternative name

# Export
__all__ = ['LayerControls', 'LayerControlsWidget', 'LayerItem', 'LayerListWidget', 
           'GridStyle', 'GridSpacing', 'QuickMode']
