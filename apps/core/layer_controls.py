#!/usr/bin/env python3
"""
X-Seti - June23 2025 - Simple Working Layer Controls
Visual Retro System Emulator Builder - Basic layer management that actually works
"""
#this belongs in ui/layer_controls.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                           QPushButton, QCheckBox, QLabel, QFrame, QComboBox,
                           QSlider, QSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

class LayerControls(QWidget):
    """Simple, working layer controls for retro computer PCB design"""
    
    # Simple signals that actually work
    layerVisibilityChanged = pyqtSignal(str, bool)  # layer_name, visible
    currentLayerChanged = pyqtSignal(str)           # layer_name
    layerSelected = pyqtSignal(str)                 # layer_name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = None
        self.current_layer = "Components"
        
        self._create_ui()
        
        print("✓ Simple Layer Controls initialized")
    
    def _create_ui(self):
        """Create simple, working UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)
        
        # === ACTIVE LAYER SELECTION ===
        active_group = QGroupBox("Active Layer")
        active_layout = QVBoxLayout(active_group)
        
        self.layer_combo = QComboBox()
        self.layer_combo.addItems(["Components", "Connections", "PCB Traces", "Annotations"])
        self.layer_combo.setCurrentText("Components")
        self.layer_combo.currentTextChanged.connect(self._on_layer_changed)
        active_layout.addWidget(self.layer_combo)
        
        layout.addWidget(active_group)
        
        # === LAYER VISIBILITY ===
        visibility_group = QGroupBox("Layer Visibility")
        visibility_layout = QVBoxLayout(visibility_group)
        
        # Components layer
        self.components_check = QCheckBox("Components")
        self.components_check.setChecked(True)
        self.components_check.toggled.connect(
            lambda checked: self._on_visibility_changed("Components", checked)
        )
        visibility_layout.addWidget(self.components_check)
        
        # Connections layer
        self.connections_check = QCheckBox("Connections")
        self.connections_check.setChecked(True)
        self.connections_check.toggled.connect(
            lambda checked: self._on_visibility_changed("Connections", checked)
        )
        visibility_layout.addWidget(self.connections_check)
        
        # PCB Traces layer
        self.traces_check = QCheckBox("PCB Traces")
        self.traces_check.setChecked(False)
        self.traces_check.toggled.connect(
            lambda checked: self._on_visibility_changed("PCB Traces", checked)
        )
        visibility_layout.addWidget(self.traces_check)
        
        # Annotations layer
        self.annotations_check = QCheckBox("Annotations")
        self.annotations_check.setChecked(True)
        self.annotations_check.toggled.connect(
            lambda checked: self._on_visibility_changed("Annotations", checked)
        )
        visibility_layout.addWidget(self.annotations_check)
        
        # Grid layer
        self.grid_check = QCheckBox("Grid")
        self.grid_check.setChecked(True)
        self.grid_check.toggled.connect(
            lambda checked: self._on_visibility_changed("Grid", checked)
        )
        visibility_layout.addWidget(self.grid_check)
        
        layout.addWidget(visibility_group)
        
        # === LAYER CONTROLS ===
        controls_group = QGroupBox("Layer Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        # Show/Hide All buttons
        buttons_layout = QHBoxLayout()
        
        show_all_btn = QPushButton("Show All")
        show_all_btn.clicked.connect(self._show_all_layers)
        buttons_layout.addWidget(show_all_btn)
        
        hide_all_btn = QPushButton("Hide All")
        hide_all_btn.clicked.connect(self._hide_all_layers)
        buttons_layout.addWidget(hide_all_btn)
        
        controls_layout.addLayout(buttons_layout)
        
        # Layer opacity
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Opacity:"))
        
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(10)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self._on_opacity_changed)
        opacity_layout.addWidget(self.opacity_slider)
        
        self.opacity_label = QLabel("100%")
        self.opacity_label.setMinimumWidth(40)
        opacity_layout.addWidget(self.opacity_label)
        
        controls_layout.addLayout(opacity_layout)
        
        layout.addWidget(controls_group)
        
        # === COMPONENT INFO ===
        info_group = QGroupBox("Component Info")
        info_layout = QVBoxLayout(info_group)
        
        self.component_count_label = QLabel("Components: 0")
        info_layout.addWidget(self.component_count_label)
        
        self.connections_count_label = QLabel("Connections: 0")
        info_layout.addWidget(self.connections_count_label)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
    
    def _on_layer_changed(self, layer_name):
        """Handle active layer change"""
        self.current_layer = layer_name
        self.currentLayerChanged.emit(layer_name)
        self.layerSelected.emit(layer_name)
        print(f"📄 Active layer: {layer_name}")
    
    def _on_visibility_changed(self, layer_name, visible):
        """Handle layer visibility change"""
        self.layerVisibilityChanged.emit(layer_name, visible)
        
        # Update canvas if connected
        if self.canvas and hasattr(self.canvas, 'set_layer_visibility'):
            self.canvas.set_layer_visibility(layer_name, visible)
        
        print(f"👁️ Layer '{layer_name}': {'visible' if visible else 'hidden'}")
    
    def _on_opacity_changed(self, value):
        """Handle opacity change"""
        self.opacity_label.setText(f"{value}%")
        
        # Update canvas if connected
        if self.canvas and hasattr(self.canvas, 'set_layer_opacity'):
            self.canvas.set_layer_opacity(self.current_layer, value / 100.0)
        
        print(f"🌗 Layer opacity: {value}%")
    
    def _show_all_layers(self):
        """Show all layers"""
        self.components_check.setChecked(True)
        self.connections_check.setChecked(True)
        self.traces_check.setChecked(True)
        self.annotations_check.setChecked(True)
        self.grid_check.setChecked(True)
        print("👁️ All layers shown")
    
    def _hide_all_layers(self):
        """Hide all layers except components"""
        self.components_check.setChecked(True)  # Always keep components visible
        self.connections_check.setChecked(False)
        self.traces_check.setChecked(False)
        self.annotations_check.setChecked(False)
        self.grid_check.setChecked(False)
        print("👁️ All layers hidden (except components)")
    
    # === PUBLIC API ===
    def set_canvas(self, canvas):
        """Set canvas reference for integration"""
        self.canvas = canvas
        print("✓ Canvas connected to layer controls")
    
    def get_layer_visibility(self, layer_name):
        """Get layer visibility status"""
        layer_checks = {
            "Components": self.components_check,
            "Connections": self.connections_check,
            "PCB Traces": self.traces_check,
            "Annotations": self.annotations_check,
            "Grid": self.grid_check
        }
        
        check = layer_checks.get(layer_name)
        return check.isChecked() if check else True
    
    def set_layer_visibility(self, layer_name, visible):
        """Set layer visibility"""
        layer_checks = {
            "Components": self.components_check,
            "Connections": self.connections_check,
            "PCB Traces": self.traces_check,
            "Annotations": self.annotations_check,
            "Grid": self.grid_check
        }
        
        check = layer_checks.get(layer_name)
        if check:
            check.setChecked(visible)
    
    def update_component_counts(self, components=0, connections=0):
        """Update component and connection counts"""
        self.component_count_label.setText(f"Components: {components}")
        self.connections_count_label.setText(f"Connections: {connections}")
    
    def get_current_layer(self):
        """Get current active layer"""
        return self.current_layer
    
    def set_current_layer(self, layer_name):
        """Set current active layer"""
        self.layer_combo.setCurrentText(layer_name)


# Export
__all__ = ['LayerControls']


# Test function
def test_layer_controls():
    """Test the layer controls"""
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    controls = LayerControls()
    controls.show()
    controls.resize(250, 400)
    
    # Test signals
    controls.layerVisibilityChanged.connect(
        lambda layer, visible: print(f"Signal: {layer} -> {visible}")
    )
    controls.currentLayerChanged.connect(
        lambda layer: print(f"Signal: Current layer -> {layer}")
    )
    
    print("Layer controls test - close window to continue")
    sys.exit(app.exec())


if __name__ == "__main__":
    test_layer_controls()