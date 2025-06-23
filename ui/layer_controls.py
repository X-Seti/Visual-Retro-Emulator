#!/usr/bin/env python3
"""
X-Seti - June23 2025 - Layer Controls UI - Clean Working Implementation
Simple UI that connects to managers/layer_manager.py backend
"""
#this belongs in ui/layer_controls.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                           QPushButton, QCheckBox, QLabel, QComboBox, QSlider,
                           QSpinBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

class LayerControls(QWidget):
    """Clean, working layer controls UI - delegates to LayerManager backend"""
    
    # UI signals only
    layerVisibilityChanged = pyqtSignal(str, bool)  # layer_name, visible
    currentLayerChanged = pyqtSignal(str)           # layer_name
    layerSelected = pyqtSignal(str)                 # layer_name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layer_manager = None  # Will be set by main window
        self.canvas = None         # Will be set by main window
        self.current_layer = "Components"
        
        self._create_ui()
        print("✓ Layer Controls UI created")
    
    def _create_ui(self):
        """Create simple, working UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)
        
        # === ACTIVE LAYER SELECTION ===
        active_group = QGroupBox("Active Layer")
        active_layout = QVBoxLayout(active_group)
        
        self.layer_combo = QComboBox()
        self.layer_combo.addItems(["Components", "Connections", "PCB Traces", "Annotations"])
        self.layer_combo.setCurrentText("Components")
        self.layer_combo.currentTextChanged.connect(self._on_active_layer_changed)
        active_layout.addWidget(self.layer_combo)
        
        layout.addWidget(active_group)
        
        # === LAYER VISIBILITY ===
        visibility_group = QGroupBox("Layer Visibility")
        visibility_layout = QVBoxLayout(visibility_group)
        
        # Create checkboxes for each layer
        self.layer_checkboxes = {}
        layer_configs = [
            ("Components", True, "🔧"),
            ("Connections", True, "🔗"),
            ("PCB Traces", False, "📋"),
            ("Annotations", True, "📝"),
            ("Grid", True, "⚏")
        ]
        
        for layer_name, default_checked, icon in layer_configs:
            checkbox = QCheckBox(f"{icon} {layer_name}")
            checkbox.setChecked(default_checked)
            checkbox.toggled.connect(
                lambda checked, name=layer_name: self._on_layer_visibility_changed(name, checked)
            )
            self.layer_checkboxes[layer_name] = checkbox
            visibility_layout.addWidget(checkbox)
        
        layout.addWidget(visibility_group)
        
        # === LAYER OPACITY ===
        opacity_group = QGroupBox("Layer Opacity")
        opacity_layout = QVBoxLayout(opacity_group)
        
        # Current layer opacity
        current_opacity_layout = QHBoxLayout()
        current_opacity_layout.addWidget(QLabel("Current Layer:"))
        
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(10)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self._on_opacity_changed)
        current_opacity_layout.addWidget(self.opacity_slider)
        
        self.opacity_label = QLabel("100%")
        self.opacity_label.setMinimumWidth(40)
        current_opacity_layout.addWidget(self.opacity_label)
        
        opacity_layout.addLayout(current_opacity_layout)
        layout.addWidget(opacity_group)
        
        # === QUICK CONTROLS ===
        controls_group = QGroupBox("Quick Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        # Show/Hide buttons
        buttons_layout = QHBoxLayout()
        
        show_all_btn = QPushButton("Show All")
        show_all_btn.clicked.connect(self._show_all_layers)
        buttons_layout.addWidget(show_all_btn)
        
        hide_all_btn = QPushButton("Hide All")
        hide_all_btn.clicked.connect(self._hide_all_layers)
        buttons_layout.addWidget(hide_all_btn)
        
        controls_layout.addLayout(buttons_layout)
        
        # Reset button
        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self._reset_layers)
        controls_layout.addWidget(reset_btn)
        
        layout.addWidget(controls_group)
        
        # === LAYER INFO ===
        info_group = QGroupBox("Layer Info")
        info_layout = QVBoxLayout(info_group)
        
        self.current_layer_label = QLabel("Current: Components")
        self.current_layer_label.setStyleSheet("font-weight: bold; color: #333;")
        info_layout.addWidget(self.current_layer_label)
        
        self.visible_layers_label = QLabel("Visible: 4/5")
        info_layout.addWidget(self.visible_layers_label)
        
        # Component counts
        separator = QFrame()
        separator.setFrameStyle(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        info_layout.addWidget(separator)
        
        self.component_count_label = QLabel("Components: 0")
        info_layout.addWidget(self.component_count_label)
        
        self.connection_count_label = QLabel("Connections: 0")
        info_layout.addWidget(self.connection_count_label)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        # Initialize display
        self._update_info_display()
    
    def _on_active_layer_changed(self, layer_name):
        """Handle active layer change"""
        self.current_layer = layer_name
        
        # Update backend if available
        if self.layer_manager and hasattr(self.layer_manager, 'set_current_layer'):
            self.layer_manager.set_current_layer(layer_name)
        
        # Update canvas if available
        if self.canvas and hasattr(self.canvas, 'set_current_layer'):
            self.canvas.set_current_layer(layer_name)
        
        # Emit signals
        self.currentLayerChanged.emit(layer_name)
        self.layerSelected.emit(layer_name)
        
        # Update display
        self._update_info_display()
        
        print(f"📄 Active layer: {layer_name}")
    
    def _on_layer_visibility_changed(self, layer_name, visible):
        """Handle layer visibility change"""
        # Update backend if available
        if self.layer_manager and hasattr(self.layer_manager, 'set_layer_visibility'):
            self.layer_manager.set_layer_visibility(layer_name, visible)
        
        # Update canvas if available
        if self.canvas and hasattr(self.canvas, 'set_layer_visibility'):
            self.canvas.set_layer_visibility(layer_name, visible)
        
        # Emit signal
        self.layerVisibilityChanged.emit(layer_name, visible)
        
        # Update display
        self._update_info_display()
        
        print(f"👁️ Layer '{layer_name}': {'visible' if visible else 'hidden'}")
    
    def _on_opacity_changed(self, value):
        """Handle opacity change"""
        self.opacity_label.setText(f"{value}%")
        
        # Update backend if available
        if self.layer_manager and hasattr(self.layer_manager, 'set_layer_opacity'):
            self.layer_manager.set_layer_opacity(self.current_layer, value / 100.0)
        
        # Update canvas if available
        if self.canvas and hasattr(self.canvas, 'set_layer_opacity'):
            self.canvas.set_layer_opacity(self.current_layer, value / 100.0)
        
        print(f"🌗 Layer '{self.current_layer}' opacity: {value}%")
    
    def _show_all_layers(self):
        """Show all layers"""
        for checkbox in self.layer_checkboxes.values():
            checkbox.setChecked(True)
        print("👁️ All layers shown")
    
    def _hide_all_layers(self):
        """Hide all layers except components"""
        for name, checkbox in self.layer_checkboxes.items():
            # Always keep components visible for usability
            checkbox.setChecked(name == "Components")
        print("👁️ All layers hidden (except Components)")
    
    def _reset_layers(self):
        """Reset layers to default state"""
        # Default visibility settings
        defaults = {
            "Components": True,
            "Connections": True,
            "PCB Traces": False,
            "Annotations": True,
            "Grid": True
        }
        
        for name, default_visible in defaults.items():
            if name in self.layer_checkboxes:
                self.layer_checkboxes[name].setChecked(default_visible)
        
        # Reset to components layer
        self.layer_combo.setCurrentText("Components")
        
        # Reset opacity
        self.opacity_slider.setValue(100)
        
        print("🔄 Layers reset to defaults")
    
    def _update_info_display(self):
        """Update the information display"""
        # Update current layer
        self.current_layer_label.setText(f"Current: {self.current_layer}")
        
        # Count visible layers
        visible_count = sum(1 for cb in self.layer_checkboxes.values() if cb.isChecked())
        total_count = len(self.layer_checkboxes)
        self.visible_layers_label.setText(f"Visible: {visible_count}/{total_count}")
    
    # === PUBLIC API FOR INTEGRATION ===
    def set_layer_manager(self, layer_manager):
        """Set the backend layer manager"""
        self.layer_manager = layer_manager
        print("✓ Layer manager connected to UI")
    
    def set_canvas(self, canvas):
        """Set canvas reference for integration"""
        self.canvas = canvas
        print("✓ Canvas connected to layer controls")
    
    def get_layer_visibility(self, layer_name):
        """Get layer visibility status"""
        checkbox = self.layer_checkboxes.get(layer_name)
        return checkbox.isChecked() if checkbox else True
    
    def set_layer_visibility(self, layer_name, visible):
        """Set layer visibility programmatically"""
        checkbox = self.layer_checkboxes.get(layer_name)
        if checkbox:
            checkbox.setChecked(visible)
    
    def get_current_layer(self):
        """Get current active layer"""
        return self.current_layer
    
    def set_current_layer(self, layer_name):
        """Set current active layer programmatically"""
        if layer_name in [self.layer_combo.itemText(i) for i in range(self.layer_combo.count())]:
            self.layer_combo.setCurrentText(layer_name)
    
    def update_component_counts(self, components=0, connections=0):
        """Update component and connection counts"""
        self.component_count_label.setText(f"Components: {components}")
        self.connection_count_label.setText(f"Connections: {connections}")
    
    def refresh_from_backend(self):
        """Refresh UI from backend state"""
        if not self.layer_manager:
            return
        
        # Update checkboxes from backend
        if hasattr(self.layer_manager, 'get_layer_visibility'):
            for layer_name, checkbox in self.layer_checkboxes.items():
                try:
                    visible = self.layer_manager.get_layer_visibility(layer_name)
                    checkbox.setChecked(visible)
                except:
                    pass  # Backend might not have this layer
        
        # Update active layer from backend
        if hasattr(self.layer_manager, 'current_layer') and self.layer_manager.current_layer:
            self.set_current_layer(self.layer_manager.current_layer)
        
        # Update display
        self._update_info_display()
        print("🔄 Layer controls refreshed from backend")


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
    controls.resize(280, 500)
    controls.setWindowTitle("Layer Controls Test")
    
    # Test signals
    controls.layerVisibilityChanged.connect(
        lambda layer, visible: print(f"✓ Signal: {layer} visibility -> {visible}")
    )
    controls.currentLayerChanged.connect(
        lambda layer: print(f"✓ Signal: Current layer -> {layer}")
    )
    
    # Test component count updates
    controls.update_component_counts(5, 3)
    
    print("✓ Layer controls test running - close window to continue")
    sys.exit(app.exec())


if __name__ == "__main__":
    test_layer_controls()