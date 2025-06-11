"""
X-Seti - June11 2025 - Layer Controls Widget
Manages different layers in the PCB/canvas view (components, connections, etc.)
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QSlider, QSpinBox,
    QGroupBox, QColorDialog, QComboBox, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPixmap, QPainter, QBrush, QIcon
from typing import Dict, List, Optional, Any

class LayerItem:
    """Represents a single layer"""
    
    def __init__(self, name: str, visible: bool = True, color: QColor = None, opacity: float = 1.0):
        self.name = name
        self.visible = visible
        self.color = color or QColor(0, 0, 0)
        self.opacity = opacity
        self.locked = False
        self.layer_type = "general"  # general, component, connection, annotation
        
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
            QColor(data.get('color', '#000000')),
            data.get('opacity', 1.0)
        )
        layer.locked = data.get('locked', False)
        layer.layer_type = data.get('layer_type', 'general')
        return layer

class LayerListWidget(QListWidget):
    """Custom list widget for layers"""
    
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
        painter.drawRect(2, 2, 12, 12)
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

class LayerControlsWidget(QWidget):
    """Main layer controls widget"""
    
    # All the signals that main_window.py might need
    layerAdded = pyqtSignal(str)  # layer_name
    layerRemoved = pyqtSignal(str)  # layer_name
    layerVisibilityChanged = pyqtSignal(str, bool)  # layer_name, visible
    layerPropertiesChanged = pyqtSignal(str, dict)  # layer_name, properties
    layerChanged = pyqtSignal(str)  # layer_name - THIS IS THE MISSING SIGNAL
    currentLayerChanged = pyqtSignal(str)  # layer_name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_layer: Optional[str] = None
        self.property_editors = {}
        self.setupUI()
        self.create_default_layers()
        
    def setupUI(self):
        """Setup the layer controls UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Layer list
        layers_group = QGroupBox("Layers")
        layers_layout = QVBoxLayout(layers_group)
        
        self.layer_list = LayerListWidget()
        self.layer_list.layerVisibilityChanged.connect(self.on_layer_visibility_changed)
        self.layer_list.layerSelected.connect(self.on_layer_selected)
        layers_layout.addWidget(self.layer_list)
        
        # Layer buttons
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
        
        layout.addWidget(layers_group)
        
        # Layer properties
        props_group = QGroupBox("Layer Properties")
        props_layout = QVBoxLayout(props_group)
        
        # Layer name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.layer_name_edit = QLineEdit()
        self.layer_name_edit.textChanged.connect(self.on_layer_name_changed)
        name_layout.addWidget(self.layer_name_edit)
        props_layout.addLayout(name_layout)
        
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
        
        layout.addWidget(props_group)
        
        # Global controls
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
        
        layout.addWidget(global_group)
        
        # Initially disable properties (no layer selected)
        self.enable_properties(False)
        
    def create_default_layers(self):
        """Create default layers"""
        default_layers = [
            LayerItem("Background", True, QColor(240, 240, 240), 1.0),
            LayerItem("Components", True, QColor(100, 100, 100), 1.0),
            LayerItem("Connections", True, QColor(0, 0, 255), 1.0),
            LayerItem("Labels", True, QColor(0, 0, 0), 1.0),
            LayerItem("Annotations", True, QColor(255, 0, 0), 0.8)
        ]
        
        for layer in default_layers:
            layer.layer_type = layer.name.lower()
            self.layer_list.add_layer(layer)
            
        # Set components as current layer and emit signal
        self.current_layer = "Components"
        self.layerChanged.emit("Components")
        self.currentLayerChanged.emit("Components")
            
    def add_new_layer(self):
        """Add a new layer"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, 'Add Layer', 'Layer name:')
        if ok and name:
            if name in self.layer_list.layers:
                QMessageBox.warning(self, "Warning", "Layer with this name already exists")
                return
                
            layer = LayerItem(name, True, QColor(100, 100, 100), 1.0)
            self.layer_list.add_layer(layer)
            self.layerAdded.emit(name)
            
    def remove_selected_layer(self):
        """Remove the selected layer"""
        current_item = self.layer_list.currentItem()
        if current_item:
            layer_name = current_item.data(Qt.ItemDataRole.UserRole)
            
            # Don't allow removing essential layers
            if layer_name in ["Background", "Components", "Connections"]:
                QMessageBox.warning(self, "Warning", "Cannot remove essential layers")
                return
                
            reply = QMessageBox.question(self, "Confirm", f"Remove layer '{layer_name}'?")
            if reply == QMessageBox.StandardButton.Yes:
                self.layer_list.remove_layer(layer_name)
                self.layerRemoved.emit(layer_name)
                self.enable_properties(False)
                
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
                
    def on_layer_visibility_changed(self, layer_name: str, visible: bool):
        """Handle layer visibility change"""
        self.layerVisibilityChanged.emit(layer_name, visible)
        
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
                    
    def on_opacity_changed(self, value: int):
        """Handle opacity change"""
        if self.current_layer:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer:
                layer.opacity = value / 100.0
                self.layer_list.refresh_display()
                self.emit_layer_properties_changed()
                
    def on_layer_type_changed(self, type_text: str):
        """Handle layer type change"""
        if self.current_layer:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer:
                layer.layer_type = type_text.lower()
                self.emit_layer_properties_changed()
                
    def on_layer_lock_changed(self, locked: bool):
        """Handle layer lock change"""
        if self.current_layer:
            layer = self.layer_list.get_layer(self.current_layer)
            if layer:
                layer.locked = locked
                self.layer_list.refresh_display()
                self.emit_layer_properties_changed()
                
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
            
    def hide_all_layers(self):
        """Hide all layers"""
        for layer_name in self.layer_list.layers:
            self.layer_list.set_layer_visibility(layer_name, False)
            
    def reset_layers(self):
        """Reset to default layers"""
        reply = QMessageBox.question(self, "Confirm", "Reset all layers to default?")
        if reply == QMessageBox.StandardButton.Yes:
            self.layer_list.layers.clear()
            self.create_default_layers()
            self.enable_properties(False)
            self.current_layer = None
            
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

# Aliases for backward compatibility
EnhancedLayerControls = LayerControlsWidget
LayerControlWidget = LayerControlsWidget  # Singular alias
