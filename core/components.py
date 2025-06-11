"""
X-Seti - June07 2025 - Core Components Module
Base component system with robust error handling
"""

import os
import json
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid

try:
    from PyQt6.QtCore import QObject, pyqtSignal
    from PyQt6.QtWidgets import QGraphicsRectItem
    QT_AVAILABLE = True
except ImportError:
    print("⚠️ PyQt6 not available - using fallback base classes")
    QT_AVAILABLE = False
    
    # Create fallback classes
    class QObject:
        def __init__(self):
            pass
    
    class QGraphicsRectItem:
        def __init__(self, *args):
            self.rect_args = args
        
        def setRect(self, x, y, w, h):
            self.rect_args = (x, y, w, h)
    
    def pyqtSignal(*args):
        return None

class ComponentType(Enum):
    """Component type enumeration"""
    CPU = "cpu"
    MEMORY = "memory"
    IO = "io"
    LOGIC = "logic"
    CUSTOM = "custom"
    SOUND = "sound"
    VIDEO = "video"
    STORAGE = "storage"

@dataclass
class ComponentPort:
    """Represents a component port/pin"""
    name: str
    pin_number: int
    direction: str = "input"  # input, output, bidirectional
    signal_type: str = "digital"  # digital, analog, power, ground
    description: str = ""
    
    def __post_init__(self):
        if self.direction not in ["input", "output", "bidirectional"]:
            self.direction = "bidirectional"
        
        if self.signal_type not in ["digital", "analog", "power", "ground"]:
            self.signal_type = "digital"

@dataclass
class ComponentInfo:
    """Component information structure"""
    name: str
    category: str
    description: str = ""
    manufacturer: str = ""
    part_number: str = ""
    package_type: str = "DIP"
    pin_count: int = 40
    year: str = ""
    datasheet_url: str = ""
    image_path: str = ""
    ports: List[ComponentPort] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)

class BaseComponent(QGraphicsRectItem if QT_AVAILABLE else QObject):
    """Base component class"""
    
    def __init__(self, component_type: str, name: str = None, parent=None):
        if QT_AVAILABLE:
            super().__init__(parent)
        else:
            super().__init__()
        
        self.id = str(uuid.uuid4())
        self.component_type = component_type
        self.name = name or f"{component_type}_{self.id[:8]}"
        self.category = "Unknown"
        
        # Component properties
        self.manufacturer = ""
        self.part_number = ""
        self.package_type = "DIP"
        self.pin_count = 40
        self.year = ""
        self.datasheet_url = ""
        self.description = ""
        
        # Physical properties
        self.x = 0.0
        self.y = 0.0
        self.width = 60.0
        self.height = 40.0
        self.rotation = 0.0
        
        # Ports and connections
        self.ports: List[ComponentPort] = []
        self.connections: Dict[str, Any] = {}
        
        # Properties for emulation
        self.properties: Dict[str, Any] = {}
        
        # State
        self.selected = False
        self.enabled = True
        
        # Setup the component
        self.setup_component()
        
        if QT_AVAILABLE:
            self.setRect(0, 0, self.width, self.height)
    
    def setup_component(self):
        """Override this method to setup component-specific properties"""
        pass
    
    def add_port(self, name: str, pin_number: int, direction: str = "input", 
                 signal_type: str = "digital", description: str = ""):
        """Add a port to the component"""
        port = ComponentPort(name, pin_number, direction, signal_type, description)
        self.ports.append(port)
        return port
    
    def get_port(self, name: str) -> Optional[ComponentPort]:
        """Get port by name"""
        for port in self.ports:
            if port.name == name:
                return port
        return None
    
    def get_port_by_pin(self, pin_number: int) -> Optional[ComponentPort]:
        """Get port by pin number"""
        for port in self.ports:
            if port.pin_number == pin_number:
                return port
        return None
    
    def connect_to_component(self, other_component: 'BaseComponent', 
                           my_port: str, other_port: str) -> bool:
        """Connect this component to another component"""
        if my_port not in [p.name for p in self.ports]:
            print(f"⚠️ Port {my_port} not found in {self.name}")
            return False
        
        if other_port not in [p.name for p in other_component.ports]:
            print(f"⚠️ Port {other_port} not found in {other_component.name}")
            return False
        
        # Store connection
        connection_key = f"{my_port}->{other_component.id}:{other_port}"
        self.connections[connection_key] = {
            'component': other_component,
            'my_port': my_port,
            'other_port': other_port
        }
        
        print(f"✓ Connected {self.name}:{my_port} -> {other_component.name}:{other_port}")
        return True
    
    def disconnect_from_component(self, other_component: 'BaseComponent', 
                                my_port: str, other_port: str) -> bool:
        """Disconnect from another component"""
        connection_key = f"{my_port}->{other_component.id}:{other_port}"
        if connection_key in self.connections:
            del self.connections[connection_key]
            print(f"✓ Disconnected {self.name}:{my_port} from {other_component.name}:{other_port}")
            return True
        return False
    
    def get_connections(self) -> List[Dict[str, Any]]:
        """Get all connections for this component"""
        return list(self.connections.values())
    
    def set_property(self, key: str, value: Any):
        """Set a component property"""
        self.properties[key] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a component property"""
        return self.properties.get(key, default)
    
    def set_position(self, x: float, y: float):
        """Set component position"""
        self.x = x
        self.y = y
        if QT_AVAILABLE:
            self.setPos(x, y)
    
    def get_position(self) -> Tuple[float, float]:
        """Get component position"""
        return (self.x, self.y)
    
    def set_size(self, width: float, height: float):
        """Set component size"""
        self.width = width
        self.height = height
        if QT_AVAILABLE:
            self.setRect(0, 0, width, height)
    
    def get_size(self) -> Tuple[float, float]:
        """Get component size"""
        return (self.width, self.height)
    
    def set_rotation(self, angle: float):
        """Set component rotation"""
        self.rotation = angle % 360
        if QT_AVAILABLE:
            self.setRotation(self.rotation)
    
    def get_rotation(self) -> float:
        """Get component rotation"""
        return self.rotation
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate component configuration"""
        errors = []
        
        # Check basic properties
        if not self.name:
            errors.append("Component name is required")
        
        if not self.component_type:
            errors.append("Component type is required")
        
        # Check ports
        pin_numbers = [p.pin_number for p in self.ports]
        if len(pin_numbers) != len(set(pin_numbers)):
            errors.append("Duplicate pin numbers found")
        
        # Check for required ports based on component type
        if self.component_type == "cpu":
            required_ports = ["VCC", "GND", "CLK"]
            for port_name in required_ports:
                if not self.get_port(port_name):
                    errors.append(f"Required port missing: {port_name}")
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary"""
        return {
            'id': self.id,
            'component_type': self.component_type,
            'name': self.name,
            'category': self.category,
            'manufacturer': self.manufacturer,
            'part_number': self.part_number,
            'package_type': self.package_type,
            'pin_count': self.pin_count,
            'year': self.year,
            'datasheet_url': self.datasheet_url,
            'description': self.description,
            'position': {'x': self.x, 'y': self.y},
            'size': {'width': self.width, 'height': self.height},
            'rotation': self.rotation,
            'ports': [
                {
                    'name': p.name,
                    'pin_number': p.pin_number,
                    'direction': p.direction,
                    'signal_type': p.signal_type,
                    'description': p.description
                } for p in self.ports
            ],
            'properties': self.properties,
            'enabled': self.enabled
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Load component from dictionary"""
        self.id = data.get('id', self.id)
        self.component_type = data.get('component_type', self.component_type)
        self.name = data.get('name', self.name)
        self.category = data.get('category', self.category)
        self.manufacturer = data.get('manufacturer', '')
        self.part_number = data.get('part_number', '')
        self.package_type = data.get('package_type', 'DIP')
        self.pin_count = data.get('pin_count', 40)
        self.year = data.get('year', '')
        self.datasheet_url = data.get('datasheet_url', '')
        self.description = data.get('description', '')
        
        # Position and size
        if 'position' in data:
            pos = data['position']
            self.set_position(pos.get('x', 0), pos.get('y', 0))
        
        if 'size' in data:
            size = data['size']
            self.set_size(size.get('width', 60), size.get('height', 40))
        
        self.set_rotation(data.get('rotation', 0))
        
        # Ports
        self.ports = []
        for port_data in data.get('ports', []):
            port = ComponentPort(
                name=port_data['name'],
                pin_number=port_data['pin_number'],
                direction=port_data.get('direction', 'input'),
                signal_type=port_data.get('signal_type', 'digital'),
                description=port_data.get('description', '')
            )
            self.ports.append(port)
        
        # Properties
        self.properties = data.get('properties', {})
        self.enabled = data.get('enabled', True)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.component_type})"
    
    def __repr__(self) -> str:
        return f"BaseComponent(id='{self.id}', type='{self.component_type}', name='{self.name}')"

class ComponentManager:
    """Manages a collection of components"""
    
    def __init__(self):
        self.components: Dict[str, BaseComponent] = {}
        self.connections: List[Tuple[str, str, str, str]] = []  # comp1_id, port1, comp2_id, port2
        self.component_groups: Dict[str, List[str]] = {}
        
        print("✓ ComponentManager initialized")
    
    def add_component(self, component: BaseComponent) -> bool:
        """Add a component to the manager"""
        if component.id in self.components:
            print(f"⚠️ Component {component.id} already exists")
            return False
        
        self.components[component.id] = component
        print(f"✓ Added component: {component.name} ({component.id})")
        return True
    
    def remove_component(self, component_id: str) -> bool:
        """Remove a component from the manager"""
        if component_id not in self.components:
            print(f"⚠️ Component {component_id} not found")
            return False
        
        # Remove all connections involving this component
        self.disconnect_all(component_id)
        
        # Remove from groups
        for group_name in list(self.component_groups.keys()):
            if component_id in self.component_groups[group_name]:
                self.component_groups[group_name].remove(component_id)
                if not self.component_groups[group_name]:
                    del self.component_groups[group_name]
        
        # Remove component
        component = self.components.pop(component_id)
        print(f"✓ Removed component: {component.name} ({component_id})")
        return True
    
    def get_component(self, component_id: str) -> Optional[BaseComponent]:
        """Get a component by ID"""
        return self.components.get(component_id)
    
    def get_component_by_name(self, name: str) -> Optional[BaseComponent]:
        """Get a component by name"""
        for component in self.components.values():
            if component.name == name:
                return component
        return None
    
    def get_all_components(self) -> List[BaseComponent]:
        """Get all components"""
        return list(self.components.values())
    
    def get_components_by_type(self, component_type: str) -> List[BaseComponent]:
        """Get components by type"""
        return [comp for comp in self.components.values() 
                if comp.component_type == component_type]
    
    def connect_components(self, comp1_id: str, port1: str, comp2_id: str, port2: str) -> bool:
        """Connect two components"""
        comp1 = self.components.get(comp1_id)
        comp2 = self.components.get(comp2_id)
        
        if not comp1 or not comp2:
            print(f"⚠️ One or both components not found: {comp1_id}, {comp2_id}")
            return False
        
        if comp1.connect_to_component(comp2, port1, port2):
            connection = (comp1_id, port1, comp2_id, port2)
            if connection not in self.connections:
                self.connections.append(connection)
            return True
        
        return False
    
    def disconnect_components(self, comp1_id: str, port1: str, comp2_id: str, port2: str) -> bool:
        """Disconnect two components"""
        comp1 = self.components.get(comp1_id)
        comp2 = self.components.get(comp2_id)
        
        if comp1 and comp2:
            if comp1.disconnect_from_component(comp2, port1, port2):
                connection = (comp1_id, port1, comp2_id, port2)
                if connection in self.connections:
                    self.connections.remove(connection)
                return True
        return False
    
    def disconnect_all(self, component_id: str):
        """Disconnect all connections for a component"""
        connections_to_remove = []
        for connection in self.connections:
            comp1_id, port1, comp2_id, port2 = connection
            if comp1_id == component_id or comp2_id == component_id:
                self.disconnect_components(comp1_id, port1, comp2_id, port2)
                connections_to_remove.append(connection)
        
        for connection in connections_to_remove:
            if connection in self.connections:
                self.connections.remove(connection)
    
    def create_group(self, group_name: str, component_ids: List[str]):
        """Create a group of components"""
        # Validate all component IDs exist
        valid_ids = [cid for cid in component_ids if cid in self.components]
        if len(valid_ids) != len(component_ids):
            print(f"⚠️ Some component IDs not found when creating group {group_name}")
        
        self.component_groups[group_name] = valid_ids
        print(f"✓ Created group {group_name} with {len(valid_ids)} components")
    
    def add_to_group(self, group_name: str, component_id: str):
        """Add component to group"""
        if component_id not in self.components:
            print(f"⚠️ Component {component_id} not found")
            return False
        
        if group_name not in self.component_groups:
            self.component_groups[group_name] = []
        
        if component_id not in self.component_groups[group_name]:
            self.component_groups[group_name].append(component_id)
            print(f"✓ Added {component_id} to group {group_name}")
        
        return True
    
    def remove_from_group(self, group_name: str, component_id: str):
        """Remove component from group"""
        if group_name in self.component_groups:
            if component_id in self.component_groups[group_name]:
                self.component_groups[group_name].remove(component_id)
                print(f"✓ Removed {component_id} from group {group_name}")
                
                # Remove empty groups
                if not self.component_groups[group_name]:
                    del self.component_groups[group_name]
    
    def get_group(self, group_name: str) -> List[BaseComponent]:
        """Get components in a group"""
        if group_name not in self.component_groups:
            return []
        
        return [self.components[cid] for cid in self.component_groups[group_name] 
                if cid in self.components]
    
    def validate_system(self) -> Tuple[bool, List[str]]:
        """Validate the entire system"""
        errors = []
        
        # Validate each component
        for component in self.components.values():
            is_valid, comp_errors = component.validate()
            if not is_valid:
                for error in comp_errors:
                    errors.append(f"{component.name}: {error}")
        
        # Check for connection issues
        for comp1_id, port1, comp2_id, port2 in self.connections:
            comp1 = self.components.get(comp1_id)
            comp2 = self.components.get(comp2_id)
            
            if not comp1:
                errors.append(f"Connection refers to missing component: {comp1_id}")
            elif not comp1.get_port(port1):
                errors.append(f"Connection refers to missing port: {comp1.name}:{port1}")
            
            if not comp2:
                errors.append(f"Connection refers to missing component: {comp2_id}")
            elif not comp2.get_port(port2):
                errors.append(f"Connection refers to missing port: {comp2.name}:{port2}")
        
        return len(errors) == 0, errors
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        stats = {
            'total_components': len(self.components),
            'total_connections': len(self.connections),
            'total_groups': len(self.component_groups),
            'components_by_type': {},
            'components_by_category': {}
        }
        
        for component in self.components.values():
            # Count by type
            comp_type = component.component_type
            stats['components_by_type'][comp_type] = stats['components_by_type'].get(comp_type, 0) + 1
            
            # Count by category
            category = component.category
            stats['components_by_category'][category] = stats['components_by_category'].get(category, 0) + 1
        
        return stats
    
    def save_to_file(self, filename: str) -> bool:
        """Save system to file"""
        try:
            data = {
                'metadata': {
                    'version': '1.0',
                    'type': 'component_system'
                },
                'components': [comp.to_dict() for comp in self.components.values()],
                'connections': self.connections,
                'groups': self.component_groups
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ System saved to {filename}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error saving system: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """Load system from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clear current system
            self.components.clear()
            self.connections.clear()
            self.component_groups.clear()
            
            # Load components
            for comp_data in data.get('components', []):
                component = BaseComponent(comp_data['component_type'])
                component.from_dict(comp_data)
                self.components[component.id] = component
            
            # Load connections
            self.connections = data.get('connections', [])
            
            # Load groups
            self.component_groups = data.get('groups', {})
            
            print(f"✓ System loaded from {filename}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error loading system: {e}")
            return False
    
    def clear(self):
        """Clear all components and connections"""
        self.components.clear()
        self.connections.clear()
        self.component_groups.clear()
        print("✓ System cleared")

class ComponentFactory:
    """Factory for creating components"""
    
    _component_registry: Dict[str, type] = {}
    
    @classmethod
    def register_component_class(cls, component_type: str, component_class: type):
        """Register a component class"""
        cls._component_registry[component_type] = component_class
        print(f"✓ Registered component class: {component_type}")
    
    @classmethod
    def create_component(cls, component_type: str, name: str = None, **kwargs) -> Optional[BaseComponent]:
        """Create a component instance"""
        if component_type in cls._component_registry:
            component_class = cls._component_registry[component_type]
            return component_class(component_type, name, **kwargs)
        else:
            # Create generic component
            return BaseComponent(component_type, name, **kwargs)
    
    @classmethod
    def create_from_dict(cls, data: Dict[str, Any]) -> Optional[BaseComponent]:
        """Create component from dictionary data"""
        component_type = data.get('component_type')
        if not component_type:
            return None
        
        component = cls.create_component(component_type)
        if component:
            component.from_dict(data)
        
        return component
    
    @classmethod
    def get_registered_types(cls) -> List[str]:
        """Get list of registered component types"""
        return list(cls._component_registry.keys())

# Register the base component
ComponentFactory.register_component_class("base", BaseComponent)

# Export main classes
__all__ = [
    'BaseComponent', 
    'ComponentManager', 
    'ComponentFactory', 
    'ComponentPort', 
    'ComponentInfo', 
    'ComponentType'
]