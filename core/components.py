"""
X-Seti - June07 2025 - Core Components Module
Base component system with robust error handling
"""
#this goes in core/
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
        self.image_path = ""
        
        # Visual properties
        self.width = 120
        self.height = 80
        
        # Connection ports
        self.ports: List[ComponentPort] = []
        self.connections: List[Any] = []
        
        # Component state
        self.enabled = True
        self.properties: Dict[str, Any] = {}
        
        # Set initial rectangle if Qt is available
        if QT_AVAILABLE and hasattr(self, 'setRect'):
            self.setRect(0, 0, self.width, self.height)
    
    def add_port(self, name: str, pin_number: int, direction: str = "bidirectional", 
                 signal_type: str = "digital", description: str = ""):
        """Add a port to the component"""
        port = ComponentPort(name, pin_number, direction, signal_type, description)
        self.ports.append(port)
        return port
    
    def get_port(self, name: str) -> Optional[ComponentPort]:
        """Get a port by name"""
        for port in self.ports:
            if port.name == name:
                return port
        return None
    
    def get_port_by_pin(self, pin_number: int) -> Optional[ComponentPort]:
        """Get a port by pin number"""
        for port in self.ports:
            if port.pin_number == pin_number:
                return port
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Export component to dictionary"""
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
            'image_path': self.image_path,
            'width': self.width,
            'height': self.height,
            'enabled': self.enabled,
            'properties': self.properties,
            'ports': [
                {
                    'name': port.name,
                    'pin_number': port.pin_number,
                    'direction': port.direction,
                    'signal_type': port.signal_type,
                    'description': port.description
                }
                for port in self.ports
            ]
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
        self.image_path = data.get('image_path', '')
        self.width = data.get('width', 120)
        self.height = data.get('height', 80)
        self.enabled = data.get('enabled', True)
        self.properties = data.get('properties', {})
        
        # Load ports
        self.ports.clear()
        for port_data in data.get('ports', []):
            port = ComponentPort(
                port_data['name'],
                port_data['pin_number'],
                port_data.get('direction', 'bidirectional'),
                port_data.get('signal_type', 'digital'),
                port_data.get('description', '')
            )
            self.ports.append(port)
        
        # Update rectangle if Qt is available
        if QT_AVAILABLE and hasattr(self, 'setRect'):
            self.setRect(0, 0, self.width, self.height)

class ProcessorComponent(BaseComponent):
    """Processor component with CPU-specific functionality"""
    
    def __init__(self, component_type: str = "cpu", name: str = None, parent=None):
        super().__init__(component_type, name, parent)
        self.category = "Processors"
        
        # CPU-specific properties
        self.clock_speed = 1.0  # MHz
        self.data_width = 8     # bits
        self.address_width = 16 # bits
        self.instruction_set = "Unknown"
        
        # Set default dimensions for CPU chips
        self.width = 120
        self.height = 80
        
        # Set rectangle bounds if Qt is available
        if QT_AVAILABLE and hasattr(self, 'setRect'):
            self.setRect(0, 0, self.width, self.height)

class MemoryComponent(BaseComponent):
    """Memory component with RAM/ROM functionality"""
    
    def __init__(self, component_type: str = "memory", name: str = None, parent=None):
        super().__init__(component_type, name, parent)
        self.category = "Memory"
        
        # Memory-specific properties
        self.memory_size = 1024  # bytes
        self.memory_type = "RAM"  # RAM, ROM, EPROM, etc.
        self.access_time = 100    # nanoseconds
        
        # Set default dimensions
        self.width = 100
        self.height = 60
        
        if QT_AVAILABLE and hasattr(self, 'setRect'):
            self.setRect(0, 0, self.width, self.height)

class HardwareComponent(BaseComponent):
    """Generic hardware component"""
    
    def __init__(self, component_type: str = "hardware", name: str = None, parent=None):
        super().__init__(component_type, name, parent)
        self.category = "Hardware"
        
        # Generic hardware properties
        self.voltage = 5.0  # volts
        self.current = 0.1  # amps
        
        # Set default dimensions
        self.width = 100
        self.height = 60
        
        if QT_AVAILABLE and hasattr(self, 'setRect'):
            self.setRect(0, 0, self.width, self.height)



class GraphicsComponent(HardwareComponent):
    """Graphics/Video component"""
    
    def __init__(self, component_type: str = "graphics", name: str = None, parent=None):
        super().__init__(component_type, name, parent)
        self.graphics_mode = "text"
        self.resolution = (320, 240)
        self.colors = 16
        self.video_memory = 16384  # 16KB default
        
        # Common graphics ports
        self.add_port("VIDEO_OUT", "output", "analog")
        self.add_port("H_SYNC", "output", "digital")
        self.add_port("V_SYNC", "output", "digital")
        self.add_port("PIXEL_CLK", "input", "digital")
        
    def set_resolution(self, width: int, height: int):
        """Set display resolution"""
        self.resolution = (width, height)
        self.mark_modified()
    
    def set_color_depth(self, colors: int):
        """Set number of colors"""
        self.colors = colors
        self.mark_modified()

class AudioComponent(HardwareComponent):
    """Audio/Sound component"""
    
    def __init__(self, component_type: str = "audio", name: str = None, parent=None):
        super().__init__(component_type, name, parent)
        self.channels = 3  # Default to 3 channels
        self.sample_rate = 44100
        self.bit_depth = 16
        
        # Common audio ports
        self.add_port("AUDIO_L", "output", "analog")
        self.add_port("AUDIO_R", "output", "analog") 
        self.add_port("AUDIO_CLK", "input", "digital")
        
    def set_channels(self, channels: int):
        """Set number of audio channels"""
        self.channels = channels
        self.mark_modified()

class IOComponent(HardwareComponent):
    """Input/Output component"""
    
    def __init__(self, component_type: str = "io", name: str = None, parent=None):
        super().__init__(component_type, name, parent)
        self.io_ports = 8  # Default number of I/O ports
        
        # Create configurable I/O ports
        for i in range(self.io_ports):
            self.add_port(f"IO_{i}", "bidirectional", "digital")
        
    def configure_port(self, port_num: int, direction: str):
        """Configure I/O port direction"""
        if 0 <= port_num < self.io_ports:
            port_name = f"IO_{port_num}"
            if port_name in self.ports:
                self.ports[port_name].direction = direction
                self.mark_modified()

class ComponentManager:
    """Manages component instances and connections"""
    
    def __init__(self):
        self.components: Dict[str, BaseComponent] = {}
        self.connections: List[Dict[str, Any]] = []
        self.component_groups: Dict[str, List[str]] = {}
        
    def add_component(self, component: BaseComponent) -> bool:
        """Add a component to the manager"""
        if not component or not hasattr(component, 'id'):
            return False
        
        self.components[component.id] = component
        print(f"✓ Added component: {component.name} ({component.id})")
        return True
    
    def remove_component(self, component_id: str) -> bool:
        """Remove a component by ID"""
        if component_id in self.components:
            component = self.components[component_id]
            del self.components[component_id]
            
            # Remove related connections
            self.connections = [
                conn for conn in self.connections
                if conn.get('from_component') != component_id and 
                conn.get('to_component') != component_id
            ]
            
            print(f"✓ Removed component: {component.name}")
            return True
        return False
    
    def get_component(self, component_id: str) -> Optional[BaseComponent]:
        """Get a component by ID"""
        return self.components.get(component_id)
    
    def list_components(self) -> List[BaseComponent]:
        """Get list of all components"""
        return list(self.components.values())
    
    def add_connection(self, from_component_id: str, from_port: str, 
                      to_component_id: str, to_port: str) -> bool:
        """Add a connection between components"""
        if (from_component_id not in self.components or 
            to_component_id not in self.components):
            return False
        
        connection = {
            'from_component': from_component_id,
            'from_port': from_port,
            'to_component': to_component_id,
            'to_port': to_port,
            'id': str(uuid.uuid4())
        }
        
        self.connections.append(connection)
        print(f"✓ Connected {from_component_id}:{from_port} to {to_component_id}:{to_port}")
        return True
    
    def save_to_file(self, filename: str) -> bool:
        """Save system to file"""
        try:
            data = {
                'components': [comp.to_dict() for comp in self.components.values()],
                'connections': self.connections,
                'groups': self.component_groups
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✓ System saved to {filename}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error saving system: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """Load system from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Clear current state
            self.clear()
            
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

# Register all component classes
ComponentFactory.register_component_class("base", BaseComponent)
ComponentFactory.register_component_class("processor", ProcessorComponent)
ComponentFactory.register_component_class("cpu", ProcessorComponent)  # Alias
ComponentFactory.register_component_class("memory", MemoryComponent)
ComponentFactory.register_component_class("hardware", HardwareComponent)

# Export main classes
__all__ = [
    'BaseComponent', 
    'ProcessorComponent',
    'MemoryComponent', 
    'HardwareComponent',
    'ComponentManager', 
    'ComponentFactory', 
    'ComponentPort', 
    'ComponentInfo', 
    'ComponentType'
, 'GraphicsComponent', 'AudioComponent', 'IOComponent']
