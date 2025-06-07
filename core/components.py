"""
X-Seti - June07 2025 - Core Component System
Defines the base classes and systems for hardware components
"""

from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QObject, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QFont, QPainter
from abc import ABCMeta, abstractmethod
import uuid
import json
from typing import Dict, List, Any, Optional, Tuple

class ComponentPort:
    """Represents a connection port on a component"""
    
    def __init__(self, name: str, port_type: str, direction: str, position: QPointF, bit_width: int = 1):
        self.name = name
        self.port_type = port_type  # 'data', 'address', 'control', 'power', 'clock'
        self.direction = direction  # 'input', 'output', 'bidirectional'
        self.position = position  # Relative to component
        self.bit_width = bit_width
        self.connected_to: List['ComponentPort'] = []
        self.signals: List[str] = []  # Signal names for multi-bit ports
        
    def connect(self, other_port: 'ComponentPort') -> bool:
        """Connect this port to another port"""
        if self.can_connect_to(other_port):
            self.connected_to.append(other_port)
            other_port.connected_to.append(self)
            return True
        return False
        
    def disconnect(self, other_port: 'ComponentPort') -> bool:
        """Disconnect from another port"""
        if other_port in self.connected_to:
            self.connected_to.remove(other_port)
            other_port.connected_to.remove(self)
            return True
        return False
        
    def can_connect_to(self, other_port: 'ComponentPort') -> bool:
        """Check if this port can connect to another port"""
        # Basic connection rules
        if self.direction == 'output' and other_port.direction == 'input':
            return True
        if self.direction == 'input' and other_port.direction == 'output':
            return True
        if self.direction == 'bidirectional' or other_port.direction == 'bidirectional':
            return True
        return False
        
    def get_absolute_position(self, component_pos: QPointF) -> QPointF:
        """Get absolute position of port given component position"""
        return component_pos + self.position
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert port to dictionary for serialization"""
        return {
            'name': self.name,
            'type': self.port_type,
            'direction': self.direction,
            'position': {'x': self.position.x(), 'y': self.position.y()},
            'bit_width': self.bit_width,
            'signals': self.signals
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComponentPort':
        """Create port from dictionary"""
        port = cls(
            data['name'],
            data['type'],
            data['direction'],
            QPointF(data['position']['x'], data['position']['y']),
            data.get('bit_width', 1)
        )
        port.signals = data.get('signals', [])
        return port

class ComponentSignals(QObject):
    """Signal emitter for component events"""
    
    positionChanged = pyqtSignal(QPointF)
    propertiesChanged = pyqtSignal(dict)
    connectionMade = pyqtSignal(str, str)  # from_port, to_port
    connectionBroken = pyqtSignal(str, str)
    stateChanged = pyqtSignal(dict)

class QGraphicsABCMeta(type(QGraphicsRectItem), ABCMeta):
    """Metaclass that resolves the conflict between QGraphicsRectItem and ABC"""
    pass

class BaseComponent(QGraphicsRectItem, metaclass=QGraphicsABCMeta):
    """Base class for all hardware components"""
    
    def __init__(self, component_type: str, name: str = None, parent=None):
        super().__init__(parent)
        
        # Basic properties
        self.id = str(uuid.uuid4())
        self.component_type = component_type
        self.name = name or f"{component_type}_{self.id[:8]}"
        
        # Graphics properties
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        
        # Component properties
        self.properties: Dict[str, Any] = {}
        self.custom_properties: Dict[str, Any] = {}
        self.ports: Dict[str, ComponentPort] = {}
        
        # State and simulation
        self.state: Dict[str, Any] = {}
        self.enabled = True
        self.simulation_active = False
        
        # Signals
        self.signals = ComponentSignals()
        
        # Visual properties
        self.selected_color = QColor(255, 215, 0)  # Gold
        self.normal_color = QColor(200, 200, 200)  # Light gray
        self.error_color = QColor(255, 100, 100)   # Light red
        self.current_color = self.normal_color
        
        # Initialize component
        self.setupComponent()
        self.updateAppearance()
        
    @abstractmethod
    def setupComponent(self):
        """Setup component-specific properties and ports"""
        pass
        
    def addPort(self, port: ComponentPort):
        """Add a port to this component"""
        self.ports[port.name] = port
        
    def removePort(self, port_name: str):
        """Remove a port from this component"""
        if port_name in self.ports:
            port = self.ports[port_name]
            # Disconnect all connections
            for connected_port in port.connected_to[:]:
                port.disconnect(connected_port)
            del self.ports[port_name]
            
    def getPort(self, port_name: str) -> Optional[ComponentPort]:
        """Get a port by name"""
        return self.ports.get(port_name)
        
    def getAllPorts(self) -> List[ComponentPort]:
        """Get all ports"""
        return list(self.ports.values())
        
    def getPortsOfType(self, port_type: str) -> List[ComponentPort]:
        """Get all ports of a specific type"""
        return [port for port in self.ports.values() if port.port_type == port_type]
        
    def connectToComponent(self, other_component: 'BaseComponent', 
                          my_port: str, other_port: str) -> bool:
        """Connect to another component"""
        if my_port in self.ports and other_port in other_component.ports:
            port1 = self.ports[my_port]
            port2 = other_component.ports[other_port]
            if port1.connect(port2):
                self.signals.connectionMade.emit(my_port, other_port)
                return True
        return False
        
    def disconnectFromComponent(self, other_component: 'BaseComponent',
                               my_port: str, other_port: str) -> bool:
        """Disconnect from another component"""
        if my_port in self.ports and other_port in other_component.ports:
            port1 = self.ports[my_port]
            port2 = other_component.ports[other_port]
            if port1.disconnect(port2):
                self.signals.connectionBroken.emit(my_port, other_port)
                return True
        return False
        
    def setProperty(self, key: str, value: Any):
        """Set a component property"""
        old_value = self.properties.get(key)
        self.properties[key] = value
        if old_value != value:
            self.signals.propertiesChanged.emit(self.properties)
            self.updateAppearance()
            
    def getProperty(self, key: str, default: Any = None) -> Any:
        """Get a component property"""
        return self.properties.get(key, default)
        
    def setState(self, key: str, value: Any):
        """Set component state"""
        self.state[key] = value
        self.signals.stateChanged.emit(self.state)
        
    def getState(self, key: str, default: Any = None) -> Any:
        """Get component state"""
        return self.state.get(key, default)
        
    def updateAppearance(self):
        """Update component visual appearance"""
        # Set colors based on state
        if not self.enabled:
            self.current_color = self.error_color
        elif self.isSelected():
            self.current_color = self.selected_color
        else:
            self.current_color = self.normal_color
            
        # Update graphics
        pen = QPen(QColor(0, 0, 0), 2)
        brush = QBrush(self.current_color)
        self.setPen(pen)
        self.setBrush(brush)
        
        self.update()
        
    def itemChange(self, change, value):
        """Handle item changes"""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            self.signals.positionChanged.emit(value)
        elif change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            self.updateAppearance()
        return super().itemChange(change, value)
        
    def paint(self, painter: QPainter, option, widget):
        """Custom paint method"""
        super().paint(painter, option, widget)
        
        # Draw component name
        painter.setFont(QFont("Arial", 8))
        painter.setPen(QPen(QColor(0, 0, 0)))
        
        rect = self.boundingRect()
        text_rect = QRectF(rect.x(), rect.y() - 15, rect.width(), 15)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.name)
        
        # Draw ports
        for port in self.ports.values():
            self.drawPort(painter, port)
            
    def drawPort(self, painter: QPainter, port: ComponentPort):
        """Draw a port on the component"""
        pos = port.position
        
        # Port colors based on type
        colors = {
            'data': QColor(0, 0, 255),     # Blue
            'address': QColor(255, 0, 0),   # Red
            'control': QColor(0, 255, 0),   # Green
            'power': QColor(255, 165, 0),   # Orange
            'clock': QColor(255, 0, 255)    # Magenta
        }
        
        color = colors.get(port.port_type, QColor(128, 128, 128))
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        
        # Draw port as small circle
        port_rect = QRectF(pos.x() - 3, pos.y() - 3, 6, 6)
        painter.drawEllipse(port_rect)
        
        # Draw port name
        painter.setFont(QFont("Arial", 6))
        text_rect = QRectF(pos.x() - 15, pos.y() + 5, 30, 8)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, port.name)
        
    def clone(self) -> 'BaseComponent':
        """Create a copy of this component"""
        # This would need to be implemented by subclasses
        raise NotImplementedError("Subclasses must implement clone method")
        
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate component configuration"""
        errors = []
        
        # Basic validation
        if not self.name:
            errors.append("Component name is required")
            
        # Check for unconnected required ports
        for port in self.ports.values():
            if port.port_type == 'power' and not port.connected_to:
                errors.append(f"Power port '{port.name}' is not connected")
                
        return len(errors) == 0, errors
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary for serialization"""
        return {
            'id': self.id,
            'type': self.component_type,
            'name': self.name,
            'position': {'x': self.x(), 'y': self.y()},
            'rotation': self.rotation(),
            'properties': self.properties,
            'custom_properties': self.custom_properties,
            'ports': {name: port.to_dict() for name, port in self.ports.items()},
            'state': self.state,
            'enabled': self.enabled
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseComponent':
        """Create component from dictionary"""
        # This would need to be implemented by subclasses
        raise NotImplementedError("Subclasses must implement from_dict method")
        
    def reset(self):
        """Reset component to initial state"""
        self.state.clear()
        self.simulation_active = False
        self.updateAppearance()
        
    def simulate_step(self, clock_cycle: int):
        """Perform one simulation step"""
        if not self.enabled or not self.simulation_active:
            return
            
        # Implement in subclasses
        pass
        
    def getConnectedComponents(self) -> List['BaseComponent']:
        """Get all components connected to this one"""
        connected = set()
        for port in self.ports.values():
            for connected_port in port.connected_to:
                # Find the component that owns this port
                # This would need to be implemented based on your component management system
                pass
        return list(connected)
        
    def getConnectionCount(self) -> int:
        """Get total number of connections"""
        return sum(len(port.connected_to) for port in self.ports.values())
        
    def isFullyConnected(self) -> bool:
        """Check if all required ports are connected"""
        for port in self.ports.values():
            if port.port_type == 'power' and not port.connected_to:
                return False
        return True
        
    def __str__(self) -> str:
        return f"{self.component_type}({self.name})"
        
    def __repr__(self) -> str:
        return f"<{self.component_type} '{self.name}' at {self.x()},{self.y()}>"

class ProcessorComponent(BaseComponent):
    """Processor/CPU component"""
    
    def setupComponent(self):
        """Setup processor-specific properties and ports"""
        self.setRect(0, 0, 80, 60)
        
        # Processor properties
        self.setProperty('architecture', '8-bit')
        self.setProperty('clock_speed', '1 MHz')
        self.setProperty('instruction_set', '6502')
        self.setProperty('cache_size', 0)
        self.setProperty('pipeline_stages', 1)
        
        # Add standard processor ports
        self.addPort(ComponentPort('CLK', 'clock', 'input', QPointF(-5, 0)))
        self.addPort(ComponentPort('RST', 'control', 'input', QPointF(-5, 15)))
        self.addPort(ComponentPort('IRQ', 'control', 'input', QPointF(-5, 30)))
        self.addPort(ComponentPort('NMI', 'control', 'input', QPointF(-5, 45)))
        
        # Data and address buses
        self.addPort(ComponentPort('D0-D7', 'data', 'bidirectional', QPointF(85, 0), 8))
        self.addPort(ComponentPort('A0-A15', 'address', 'output', QPointF(85, 30), 16))
        
        # Control signals
        self.addPort(ComponentPort('RW', 'control', 'output', QPointF(40, -5)))
        self.addPort(ComponentPort('RDY', 'control', 'input', QPointF(40, 65)))
        
        # Power
        self.addPort(ComponentPort('VCC', 'power', 'input', QPointF(0, -5)))
        self.addPort(ComponentPort('GND', 'power', 'input', QPointF(0, 65)))

class MemoryComponent(BaseComponent):
    """Memory component (RAM/ROM)"""
    
    def setupComponent(self):
        """Setup memory-specific properties and ports"""
        self.setRect(0, 0, 60, 40)
        
        # Memory properties
        self.setProperty('capacity', '64KB')
        self.setProperty('memory_type', 'RAM')
        self.setProperty('access_time', '150ns')
        self.setProperty('data_width', 8)
        self.setProperty('address_width', 16)
        
        # Memory ports
        self.addPort(ComponentPort('D0-D7', 'data', 'bidirectional', QPointF(65, 10), 8))
        self.addPort(ComponentPort('A0-A15', 'address', 'input', QPointF(-5, 10), 16))
        self.addPort(ComponentPort('CS', 'control', 'input', QPointF(-5, 25)))
        self.addPort(ComponentPort('WE', 'control', 'input', QPointF(30, -5)))
        self.addPort(ComponentPort('OE', 'control', 'input', QPointF(30, 45)))
        
        # Power
        self.addPort(ComponentPort('VCC', 'power', 'input', QPointF(0, -5)))
        self.addPort(ComponentPort('GND', 'power', 'input', QPointF(0, 45)))

class GraphicsComponent(BaseComponent):
    """Graphics/Video component"""
    
    def setupComponent(self):
        """Setup graphics-specific properties and ports"""
        self.setRect(0, 0, 70, 50)
        
        # Graphics properties
        self.setProperty('resolution', '320x200')
        self.setProperty('colors', 16)
        self.setProperty('sprites', 8)
        self.setProperty('video_ram', '16KB')
        self.setProperty('refresh_rate', '60Hz')
        
        # Graphics ports
        self.addPort(ComponentPort('CLK', 'clock', 'input', QPointF(-5, 0)))
        self.addPort(ComponentPort('D0-D7', 'data', 'bidirectional', QPointF(75, 10), 8))
        self.addPort(ComponentPort('A0-A13', 'address', 'input', QPointF(-5, 15), 14))
        self.addPort(ComponentPort('CS', 'control', 'input', QPointF(-5, 30)))
        self.addPort(ComponentPort('RW', 'control', 'input', QPointF(-5, 45)))
        
        # Video output
        self.addPort(ComponentPort('HSYNC', 'control', 'output', QPointF(75, 25)))
        self.addPort(ComponentPort('VSYNC', 'control', 'output', QPointF(75, 40)))
        self.addPort(ComponentPort('RGB', 'data', 'output', QPointF(35, 55), 3))
        
        # Power
        self.addPort(ComponentPort('VCC', 'power', 'input', QPointF(0, -5)))
        self.addPort(ComponentPort('GND', 'power', 'input', QPointF(0, 55)))

class AudioComponent(BaseComponent):
    """Audio/Sound component"""
    
    def setupComponent(self):
        """Setup audio-specific properties and ports"""
        self.setRect(0, 0, 60, 45)
        
        # Audio properties
        self.setProperty('voices', 3)
        self.setProperty('waveforms', ['Square', 'Sawtooth', 'Triangle', 'Noise'])
        self.setProperty('frequency_range', '20Hz-20kHz')
        self.setProperty('bit_depth', 8)
        self.setProperty('sample_rate', '44.1kHz')
        
        # Audio ports
        self.addPort(ComponentPort('CLK', 'clock', 'input', QPointF(-5, 0)))
        self.addPort(ComponentPort('D0-D7', 'data', 'input', QPointF(-5, 15), 8))
        self.addPort(ComponentPort('A0-A4', 'address', 'input', QPointF(-5, 30), 5))
        self.addPort(ComponentPort('CS', 'control', 'input', QPointF(-5, 45)))
        
        # Audio output
        self.addPort(ComponentPort('AUDIO_L', 'data', 'output', QPointF(65, 15)))
        self.addPort(ComponentPort('AUDIO_R', 'data', 'output', QPointF(65, 30)))
        
        # Power
        self.addPort(ComponentPort('VCC', 'power', 'input', QPointF(0, -5)))
        self.addPort(ComponentPort('GND', 'power', 'input', QPointF(0, 50)))

class IOComponent(BaseComponent):
    """Input/Output component"""
    
    def setupComponent(self):
        """Setup I/O-specific properties and ports"""
        self.setRect(0, 0, 65, 55)
        
        # I/O properties
        self.setProperty('ports', '3x8-bit')
        self.setProperty('modes', ['Input', 'Output', 'Bidirectional'])
        self.setProperty('interrupt_capable', True)
        self.setProperty('handshake_support', True)
        
        # I/O ports
        self.addPort(ComponentPort('CLK', 'clock', 'input', QPointF(-5, 0)))
        self.addPort(ComponentPort('D0-D7', 'data', 'bidirectional', QPointF(-5, 15), 8))
        self.addPort(ComponentPort('A0-A1', 'address', 'input', QPointF(-5, 30), 2))
        self.addPort(ComponentPort('CS', 'control', 'input', QPointF(-5, 45)))
        self.addPort(ComponentPort('RW', 'control', 'input', QPointF(-5, 60)))
        
        # External I/O ports
        self.addPort(ComponentPort('PA0-PA7', 'data', 'bidirectional', QPointF(70, 0), 8))
        self.addPort(ComponentPort('PB0-PB7', 'data', 'bidirectional', QPointF(70, 20), 8))
        self.addPort(ComponentPort('PC0-PC7', 'data', 'bidirectional', QPointF(70, 40), 8))
        
        # Interrupt
        self.addPort(ComponentPort('IRQ', 'control', 'output', QPointF(35, -5)))
        
        # Power
        self.addPort(ComponentPort('VCC', 'power', 'input', QPointF(0, -5)))
        self.addPort(ComponentPort('GND', 'power', 'input', QPointF(0, 60)))

class ComponentFactory:
    """Factory for creating components"""
    
    _component_types = {
        'Processor': ProcessorComponent,
        'Memory': MemoryComponent,
        'Graphics': GraphicsComponent,
        'Audio': AudioComponent,
        'I/O': IOComponent
    }
    
    @classmethod
    def create_component(cls, component_type: str, name: str = None, **kwargs) -> Optional[BaseComponent]:
        """Create a component of the specified type"""
        if component_type in cls._component_types:
            component_class = cls._component_types[component_type]
            component = component_class(component_type, name)
            
            # Set any additional properties
            for key, value in kwargs.items():
                component.setProperty(key, value)
                
            return component
        return None
        
    @classmethod
    def get_available_types(cls) -> List[str]:
        """Get list of available component types"""
        return list(cls._component_types.keys())
        
    @classmethod
    def register_component_type(cls, type_name: str, component_class):
        """Register a new component type"""
        cls._component_types[type_name] = component_class
        
    @classmethod
    def create_from_dict(cls, data: Dict[str, Any]) -> Optional[BaseComponent]:
        """Create component from dictionary data"""
        component_type = data.get('type')
        if component_type in cls._component_types:
            component_class = cls._component_types[component_type]
            component = component_class(component_type, data.get('name'))
            
            # Restore position and rotation
            if 'position' in data:
                pos = data['position']
                component.setPos(pos['x'], pos['y'])
            if 'rotation' in data:
                component.setRotation(data['rotation'])
                
            # Restore properties
            if 'properties' in data:
                component.properties.update(data['properties'])
            if 'custom_properties' in data:
                component.custom_properties.update(data['custom_properties'])
                
            # Restore state
            if 'state' in data:
                component.state.update(data['state'])
            if 'enabled' in data:
                component.enabled = data['enabled']
                
            # Restore ports (connections will be restored separately)
            if 'ports' in data:
                component.ports.clear()
                for port_name, port_data in data['ports'].items():
                    port = ComponentPort.from_dict(port_data)
                    component.ports[port_name] = port
                    
            component.updateAppearance()
            return component
        return None

class ComponentManager:
    """Manages components in the system"""
    
    def __init__(self):
        self.components: Dict[str, BaseComponent] = {}
        self.component_groups: Dict[str, List[str]] = {}
        self.connections: List[Tuple[str, str, str, str]] = []  # (comp1_id, port1, comp2_id, port2)
        
    def add_component(self, component: BaseComponent):
        """Add a component to the manager"""
        self.components[component.id] = component
        
    def remove_component(self, component_id: str):
        """Remove a component from the manager"""
        if component_id in self.components:
            component = self.components[component_id]
            
            # Remove all connections
            self.disconnect_all(component_id)
            
            # Remove from groups
            for group_components in self.component_groups.values():
                if component_id in group_components:
                    group_components.remove(component_id)
                    
            del self.components[component_id]
            
    def get_component(self, component_id: str) -> Optional[BaseComponent]:
        """Get a component by ID"""
        return self.components.get(component_id)
        
    def get_components_by_type(self, component_type: str) -> List[BaseComponent]:
        """Get all components of a specific type"""
        return [comp for comp in self.components.values() 
                if comp.component_type == component_type]
                
    def connect_components(self, comp1_id: str, port1: str, comp2_id: str, port2: str) -> bool:
        """Connect two components"""
        comp1 = self.components.get(comp1_id)
        comp2 = self.components.get(comp2_id)
        
        if comp1 and comp2:
            if comp1.connectToComponent(comp2, port1, port2):
                self.connections.append((comp1_id, port1, comp2_id, port2))
                return True
        return False
        
    def disconnect_components(self, comp1_id: str, port1: str, comp2_id: str, port2: str) -> bool:
        """Disconnect two components"""
        comp1 = self.components.get(comp1_id)
        comp2 = self.components.get(comp2_id)
        
        if comp1 and comp2:
            if comp1.disconnectFromComponent(comp2, port1, port2):
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
        self.component_groups[group_name] = component_ids[:]
        
    def add_to_group(self, group_name: str, component_id: str):
        """Add component to group"""
        if group_name not in self.component_groups:
            self.component_groups[group_name] = []
        if component_id not in self.component_groups[group_name]:
            self.component_groups[group_name].append(component_id)
            
    def remove_from_group(self, group_name: str, component_id: str):
        """Remove component from group"""
        if group_name in self.component_groups:
            if component_id in self.component_groups[group_name]:
                self.component_groups[group_name].remove(component_id)
                
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
                errors.append(f"Connection references missing component: {comp1_id}")
            elif not comp2:
                errors.append(f"Connection references missing component: {comp2_id}")
            elif port1 not in comp1.ports:
                errors.append(f"Component {comp1.name} missing port: {port1}")
            elif port2 not in comp2.ports:
                errors.append(f"Component {comp2.name} missing port: {port2}")
                
        return len(errors) == 0, errors
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire system to dictionary"""
        return {
            'components': {comp_id: comp.to_dict() for comp_id, comp in self.components.items()},
            'connections': self.connections,
            'groups': self.component_groups
        }
        
    def from_dict(self, data: Dict[str, Any]):
        """Load system from dictionary"""
        self.clear()
        
        # Load components
        if 'components' in data:
            for comp_id, comp_data in data['components'].items():
                component = ComponentFactory.create_from_dict(comp_data)
                if component:
                    component.id = comp_id  # Preserve original ID
                    self.components[comp_id] = component
                    
        # Restore connections
        if 'connections' in data:
            for comp1_id, port1, comp2_id, port2 in data['connections']:
                self.connect_components(comp1_id, port1, comp2_id, port2)
                
        # Restore groups
        if 'groups' in data:
            self.component_groups = data['groups'].copy()
            
    def clear(self):
        """Clear all components and connections"""
        self.components.clear()
        self.connections.clear()
        self.component_groups.clear()
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        type_counts = {}
        for component in self.components.values():
            comp_type = component.component_type
            type_counts[comp_type] = type_counts.get(comp_type, 0) + 1
            
        return {
            'total_components': len(self.components),
            'total_connections': len(self.connections),
            'component_types': type_counts,
            'groups': len(self.component_groups)
        }
