"""
X-Seti - June22 2025 - Layer Manager - Manages canvas layers
Provides layer management functionality for the canvas system
"""
#this goes in managers/

import os
import json
import time
import shutil
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor

class Layer:
    """Represents a single canvas layer"""
    
    def __init__(self, name: str, visible: bool = True, color: QColor = None, opacity: float = 1.0):
        self.name = name
        self.visible = visible
        self.color = color or QColor(0, 0, 0)
        self.opacity = opacity
        self.locked = False
        self.layer_type = "general"
        self.z_order = 0
        self.items = []  # Graphics items on this layer
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert layer to dictionary"""
        return {
            'name': self.name,
            'visible': self.visible,
            'color': self.color.name(),
            'opacity': self.opacity,
            'locked': self.locked,
            'layer_type': self.layer_type,
            'z_order': self.z_order
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Layer':
        """Create layer from dictionary"""
        layer = cls(
            data['name'],
            data.get('visible', True),
            QColor(data.get('color', '#000000')),
            data.get('opacity', 1.0)
        )
        layer.locked = data.get('locked', False)
        layer.layer_type = data.get('layer_type', 'general')
        layer.z_order = data.get('z_order', 0)
        return layer

class LayerManager(QObject):
    """Manages canvas layers"""
    
    # Signals
    layerAdded = pyqtSignal(str)           # layer_name
    layerRemoved = pyqtSignal(str)         # layer_name
    layerVisibilityChanged = pyqtSignal(str, bool)  # layer_name, visible
    layerOrderChanged = pyqtSignal()       # layer order changed
    currentLayerChanged = pyqtSignal(str)  # new_current_layer
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layers: Dict[str, Layer] = {}
        self.layer_order: List[str] = []  # Bottom to top
        self.current_layer: Optional[str] = None
        self.create_default_layers()
        
    def create_default_layers(self):
        """Create default layers for the canvas"""
        default_layers = [
            Layer("Background", True, QColor(240, 240, 240), 1.0),
            Layer("Grid", True, QColor(200, 200, 200), 0.5),
            Layer("Components", True, QColor(100, 100, 100), 1.0),
            Layer("Connections", True, QColor(0, 0, 255), 1.0),
            Layer("Labels", True, QColor(0, 0, 0), 1.0),
            Layer("Selection", True, QColor(255, 215, 0), 0.8),
            Layer("Annotations", True, QColor(255, 0, 0), 0.8)
        ]
        
        for i, layer in enumerate(default_layers):
            layer.layer_type = layer.name.lower()
            layer.z_order = i
            self.layers[layer.name] = layer
            self.layer_order.append(layer.name)
            
        # Set components as current layer
        self.current_layer = "Components"
        
    def add_layer(self, name: str, visible: bool = True, color: QColor = None, 
                  layer_type: str = "general") -> bool:
        """Add a new layer"""
        if name in self.layers:
            return False
            
        layer = Layer(name, visible, color or QColor(128, 128, 128))
        layer.layer_type = layer_type
        layer.z_order = len(self.layer_order)
        
        self.layers[name] = layer
        self.layer_order.append(name)
        
        self.layerAdded.emit(name)
        return True
        
    def remove_layer(self, name: str) -> bool:
        """Remove a layer"""
        if name not in self.layers:
            return False
            
        # Don't allow removing essential layers
        essential_layers = ["Background", "Components", "Connections"]
        if name in essential_layers:
            return False
            
        # Remove from layer order
        if name in self.layer_order:
            self.layer_order.remove(name)
            
        # Remove from layers dict
        del self.layers[name]
        
        # Change current layer if it was removed
        if self.current_layer == name:
            self.current_layer = self.layer_order[-1] if self.layer_order else None
            if self.current_layer:
                self.currentLayerChanged.emit(self.current_layer)
                
        self.layerRemoved.emit(name)
        return True
        
    def get_layer(self, name: str) -> Optional[Layer]:
        """Get layer by name"""
        return self.layers.get(name)
        
    def set_layer_visibility(self, name: str, visible: bool):
        """Set layer visibility"""
        if name in self.layers:
            self.layers[name].visible = visible
            self.layerVisibilityChanged.emit(name, visible)
            
    def get_layer_visibility(self, name: str) -> bool:
        """Get layer visibility"""
        layer = self.layers.get(name)
        return layer.visible if layer else False
        
    def set_current_layer(self, name: str):
        """Set current active layer"""
        if name in self.layers:
            self.current_layer = name
            self.currentLayerChanged.emit(name)
            
    def get_current_layer(self) -> Optional[str]:
        """Get current active layer name"""
        return self.current_layer
        
    def get_current_layer_object(self) -> Optional[Layer]:
        """Get current active layer object"""
        if self.current_layer:
            return self.layers.get(self.current_layer)
        return None
        
    def move_layer_up(self, name: str) -> bool:
        """Move layer up in z-order"""
        if name not in self.layer_order:
            return False
            
        index = self.layer_order.index(name)
        if index < len(self.layer_order) - 1:
            # Swap with layer above
            self.layer_order[index], self.layer_order[index + 1] = \
                self.layer_order[index + 1], self.layer_order[index]
            
            # Update z_order values
            self.update_z_orders()
            self.layerOrderChanged.emit()
            return True
        return False
        
    def move_layer_down(self, name: str) -> bool:
        """Move layer down in z-order"""
        if name not in self.layer_order:
            return False
            
        index = self.layer_order.index(name)
        if index > 0:
            # Swap with layer below
            self.layer_order[index], self.layer_order[index - 1] = \
                self.layer_order[index - 1], self.layer_order[index]
                
            # Update z_order values
            self.update_z_orders()
            self.layerOrderChanged.emit()
            return True
        return False
        
    def update_z_orders(self):
        """Update z_order values based on layer_order"""
        for i, layer_name in enumerate(self.layer_order):
            if layer_name in self.layers:
                self.layers[layer_name].z_order = i
                
    def get_layers_ordered(self) -> List[Layer]:
        """Get layers in z-order (bottom to top)"""
        return [self.layers[name] for name in self.layer_order if name in self.layers]
        
    def get_visible_layers(self) -> List[Layer]:
        """Get only visible layers"""
        return [layer for layer in self.get_layers_ordered() if layer.visible]
        
    def show_all_layers(self):
        """Show all layers"""
        for layer_name in self.layers:
            self.set_layer_visibility(layer_name, True)
            
    def hide_all_layers(self):
        """Hide all layers except background"""
        for layer_name in self.layers:
            if layer_name != "Background":
                self.set_layer_visibility(layer_name, False)
                
    def reset_layers(self):
        """Reset to default layers"""
        self.layers.clear()
        self.layer_order.clear()
        self.current_layer = None
        self.create_default_layers()
        
    def duplicate_layer(self, name: str, new_name: str = None) -> bool:
        """Duplicate a layer"""
        if name not in self.layers:
            return False
            
        original = self.layers[name]
        
        # Generate new name if not provided
        if not new_name:
            counter = 1
            new_name = f"{name}_copy"
            while new_name in self.layers:
                new_name = f"{name}_copy_{counter}"
                counter += 1
                
        # Create duplicate
        duplicate = Layer(new_name, original.visible, QColor(original.color), original.opacity)
        duplicate.layer_type = original.layer_type
        duplicate.locked = original.locked
        duplicate.z_order = len(self.layer_order)
        
        self.layers[new_name] = duplicate
        self.layer_order.append(new_name)
        
        self.layerAdded.emit(new_name)
        return True
        
    def set_layer_color(self, name: str, color: QColor):
        """Set layer color"""
        if name in self.layers:
            self.layers[name].color = color
            
    def set_layer_opacity(self, name: str, opacity: float):
        """Set layer opacity"""
        if name in self.layers:
            self.layers[name].opacity = max(0.0, min(1.0, opacity))
            
    def set_layer_locked(self, name: str, locked: bool):
        """Set layer locked status"""
        if name in self.layers:
            self.layers[name].locked = locked
            
    def is_layer_locked(self, name: str) -> bool:
        """Check if layer is locked"""
        layer = self.layers.get(name)
        return layer.locked if layer else False
        
    def get_layer_for_item(self, item) -> Optional[str]:
        """Get layer name for a graphics item"""
        # This would need to be implemented based on how items are tracked
        # For now, return current layer or components layer
        if hasattr(item, 'layer_name'):
            return item.layer_name
        return self.current_layer or "Components"
        
    def add_item_to_layer(self, item, layer_name: str = None):
        """Add graphics item to a layer"""
        target_layer = layer_name or self.current_layer or "Components"
        if target_layer in self.layers:
            layer = self.layers[target_layer]
            if item not in layer.items:
                layer.items.append(item)
            # Set layer reference on item
            if hasattr(item, 'layer_name'):
                item.layer_name = target_layer
                
    def remove_item_from_layer(self, item, layer_name: str = None):
        """Remove graphics item from layer"""
        if layer_name:
            layers_to_check = [layer_name]
        else:
            layers_to_check = list(self.layers.keys())
            
        for name in layers_to_check:
            layer = self.layers[name]
            if item in layer.items:
                layer.items.remove(item)
                break
                
    def export_layers(self) -> Dict[str, Any]:
        """Export layer configuration"""
        return {
            'layers': {name: layer.to_dict() for name, layer in self.layers.items()},
            'layer_order': self.layer_order.copy(),
            'current_layer': self.current_layer
        }
        
    def import_layers(self, data: Dict[str, Any]):
        """Import layer configuration"""
        if 'layers' in data:
            self.layers.clear()
            for name, layer_data in data['layers'].items():
                layer = Layer.from_dict(layer_data)
                self.layers[name] = layer
                
        if 'layer_order' in data:
            self.layer_order = data['layer_order'].copy()
        else:
            # Rebuild order from z_order
            self.layer_order = sorted(self.layers.keys(), 
                                    key=lambda name: self.layers[name].z_order)
                                    
        if 'current_layer' in data:
            self.current_layer = data['current_layer']
            
    def get_statistics(self) -> Dict[str, Any]:
        """Get layer statistics"""
        return {
            'total_layers': len(self.layers),
            'visible_layers': len(self.get_visible_layers()),
            'current_layer': self.current_layer,
            'layer_types': list(set(layer.layer_type for layer in self.layers.values())),
            'total_items': sum(len(layer.items) for layer in self.layers.values())
        }

class ProjectSettings:
    """Project settings configuration"""
    name: str = "Untitled Project"
    description: str = ""
    author: str = ""
    version: str = "1.0.0"
    created_date: str = ""
    modified_date: str = ""
    target_system: str = ""  # e.g., "C64", "Amiga", "Custom"

    # Visual settings
    grid_size: int = 20
    grid_visible: bool = True
    snap_to_grid: bool = True

    # Layer settings
    active_layer: str = "chip"
    layer_visibility: Dict[str, bool] = field(default_factory=lambda: {
        "chip": True,
        "pcb": False,
        "gerber": False
    })

    # Export settings
    export_format: str = "json"
    export_path: str = ""

    # Simulation settings
    simulation_speed: float = 1.0
    debug_mode: bool = False
