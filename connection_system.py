"""
X-Seti - June07 2025 - Connection System
Handles connections between components in the visual editor
"""

from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsItem
from PyQt6.QtCore import Qt, QPointF, pyqtSignal, QObject
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QPolygonF
import math
from typing import Optional, Tuple, List

class ConnectionSignals(QObject):
    """Signals for connection events"""
    connectionCreated = pyqtSignal(object)  # Connection object
    connectionDeleted = pyqtSignal(object)  # Connection object
    connectionSelected = pyqtSignal(object)  # Connection object

class Connection(QGraphicsLineItem):
    """Basic connection between two points"""
    
    def __init__(self, start_point: QPointF, end_point: QPointF, parent=None):
        super().__init__(parent)
        self.start_point = start_point
        self.end_point = end_point
        self.connection_type = "wire"
        self.signal_name = ""
        self.start_component = None
        self.end_component = None
        self.start_pin = None
        self.end_pin = None
        
        # Visual properties
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        
        # Connection appearance
        self.normal_color = QColor(0, 0, 0)
        self.selected_color = QColor(255, 0, 0)
        self.signal_colors = {
            'power': QColor(255, 0, 0),      # Red
            'ground': QColor(0, 0, 0),       # Black
            'clock': QColor(255, 165, 0),    # Orange
            'data': QColor(0, 0, 255),       # Blue
            'address': QColor(0, 128, 0),    # Green
            'control': QColor(128, 0, 128),  # Purple
            'analog': QColor(255, 192, 203), # Pink
        }
        
        self.updateLine()
        self.updateAppearance()
        
    def updateLine(self):
        """Update the line geometry"""
        self.setLine(self.start_point.x(), self.start_point.y(),
                    self.end_point.x(), self.end_point.y())
                    
    def updateAppearance(self):
        """Update visual appearance based on state and type"""
        color = self.signal_colors.get(self.connection_type, self.normal_color)
        
        if self.isSelected():
            color = self.selected_color
            
        pen = QPen(color, 2)
        if self.connection_type in ['power', 'ground']:
            pen.setWidth(3)  # Thicker for power connections
            
        self.setPen(pen)
        
    def setStartPoint(self, point: QPointF):
        """Set start point and update line"""
        self.start_point = point
        self.updateLine()
        
    def setEndPoint(self, point: QPointF):
        """Set end point and update line"""
        self.end_point = point
        self.updateLine()
        
    def setConnectionType(self, conn_type: str):
        """Set connection type and update appearance"""
        self.connection_type = conn_type
        self.updateAppearance()
        
    def setSignalName(self, name: str):
        """Set signal name for this connection"""
        self.signal_name = name
        
    def connectComponents(self, start_comp, start_pin, end_comp, end_pin):
        """Connect two component pins"""
        self.start_component = start_comp
        self.start_pin = start_pin
        self.end_component = end_comp
        self.end_pin = end_pin
        
        # Update connection type based on pin types
        if hasattr(start_pin, 'pin_type'):
            self.setConnectionType(start_pin.pin_type)
            
    def getLength(self) -> float:
        """Get connection length"""
        dx = self.end_point.x() - self.start_point.x()
        dy = self.end_point.y() - self.start_point.y()
        return math.sqrt(dx * dx + dy * dy)
        
    def getMidpoint(self) -> QPointF:
        """Get midpoint of connection"""
        return QPointF(
            (self.start_point.x() + self.end_point.x()) / 2,
            (self.start_point.y() + self.end_point.y()) / 2
        )
        
    def itemChange(self, change, value):
        """Handle item changes"""
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            self.updateAppearance()
        return super().itemChange(change, value)

class EnhancedConnection(Connection):
    """Enhanced connection with routing and visual improvements"""
    
    def __init__(self, start_point: QPointF, end_point: QPointF, parent=None):
        super().__init__(start_point, end_point, parent)
        self.routing_points: List[QPointF] = []
        self.connection_style = "orthogonal"  # "direct", "orthogonal", "curved"
        self.show_direction = True
        self.show_signal_name = True
        
    def setRoutingStyle(self, style: str):
        """Set connection routing style"""
        self.connection_style = style
        self.updatePath()
        
    def addRoutingPoint(self, point: QPointF):
        """Add a routing point for the connection"""
        self.routing_points.append(point)
        self.updatePath()
        
    def clearRoutingPoints(self):
        """Clear all routing points"""
        self.routing_points.clear()
        self.updatePath()
        
    def updatePath(self):
        """Update connection path based on routing style"""
        if self.connection_style == "direct":
            self.updateLine()
        elif self.connection_style == "orthogonal":
            self.createOrthogonalPath()
        elif self.connection_style == "curved":
            self.createCurvedPath()
            
    def createOrthogonalPath(self):
        """Create orthogonal (right-angle) path"""
        # For now, create a simple L-shaped path
        if self.routing_points:
            # Use routing points if available
            points = [self.start_point] + self.routing_points + [self.end_point]
        else:
            # Create automatic orthogonal routing
            mid_x = (self.start_point.x() + self.end_point.x()) / 2
            mid_point = QPointF(mid_x, self.start_point.y())
            points = [self.start_point, mid_point, 
                     QPointF(mid_x, self.end_point.y()), self.end_point]
        
        # Create path through points
        self.setLine(self.start_point.x(), self.start_point.y(),
                    self.end_point.x(), self.end_point.y())
                    
    def createCurvedPath(self):
        """Create curved path"""
        # For now, use direct line - could be enhanced with QPainterPath
        self.updateLine()
        
    def paint(self, painter: QPainter, option, widget):
        """Custom paint method"""
        super().paint(painter, option, widget)
        
        # Draw direction arrow if enabled
        if self.show_direction:
            self.drawDirectionArrow(painter)
            
        # Draw signal name if enabled
        if self.show_signal_name and self.signal_name:
            self.drawSignalName(painter)
            
    def drawDirectionArrow(self, painter: QPainter):
        """Draw direction arrow on the connection"""
        # Calculate arrow position (75% along the line)
        t = 0.75
        arrow_pos = QPointF(
            self.start_point.x() + t * (self.end_point.x() - self.start_point.x()),
            self.start_point.y() + t * (self.end_point.y() - self.start_point.y())
        )
        
        # Calculate arrow direction
        dx = self.end_point.x() - self.start_point.x()
        dy = self.end_point.y() - self.start_point.y()
        length = math.sqrt(dx * dx + dy * dy)
        
        if length > 0:
            # Normalize direction
            dx /= length
            dy /= length
            
            # Arrow size
            arrow_size = 8
            
            # Arrow points
            arrow_head = QPolygonF([
                QPointF(arrow_pos.x(), arrow_pos.y()),
                QPointF(arrow_pos.x() - arrow_size * dx + arrow_size * 0.3 * dy,
                       arrow_pos.y() - arrow_size * dy - arrow_size * 0.3 * dx),
                QPointF(arrow_pos.x() - arrow_size * dx - arrow_size * 0.3 * dy,
                       arrow_pos.y() - arrow_size * dy + arrow_size * 0.3 * dx)
            ])
            
            # Draw arrow
            painter.setBrush(QBrush(self.pen().color()))
            painter.drawPolygon(arrow_head)
            
    def drawSignalName(self, painter: QPainter):
        """Draw signal name on the connection"""
        mid_point = self.getMidpoint()
        
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawText(mid_point, self.signal_name)

class ConnectionManager:
    """Manages all connections in the scene"""
    
    def __init__(self):
        self.connections: List[Connection] = []
        self.signals = ConnectionSignals()
        self.auto_route = True
        self.connection_validation = True
        
    def createConnection(self, start_point: QPointF, end_point: QPointF, 
                        enhanced: bool = True) -> Connection:
        """Create a new connection"""
        if enhanced:
            connection = EnhancedConnection(start_point, end_point)
        else:
            connection = Connection(start_point, end_point)
            
        self.connections.append(connection)
        self.signals.connectionCreated.emit(connection)
        return connection
        
    def deleteConnection(self, connection: Connection):
        """Delete a connection"""
        if connection in self.connections:
            self.connections.remove(connection)
            self.signals.connectionDeleted.emit(connection)
            
    def getConnectionsForComponent(self, component) -> List[Connection]:
        """Get all connections for a component"""
        component_connections = []
        for conn in self.connections:
            if (conn.start_component == component or 
                conn.end_component == component):
                component_connections.append(conn)
        return component_connections
        
    def validateConnection(self, start_comp, start_pin, end_comp, end_pin) -> Tuple[bool, str]:
        """Validate if a connection is valid"""
        if not self.connection_validation:
            return True, "Validation disabled"
            
        # Check if components are different
        if start_comp == end_comp:
            return False, "Cannot connect component to itself"
            
        # Check pin compatibility
        if hasattr(start_pin, 'pin_type') and hasattr(end_pin, 'pin_type'):
            start_type = start_pin.pin_type
            end_type = end_pin.pin_type
            
            # Check for compatible pin types
            compatible_types = {
                'output': ['input'],
                'input': ['output'], 
                'bidirectional': ['input', 'output', 'bidirectional'],
                'power': ['power'],
                'ground': ['ground']
            }
            
            if start_type in compatible_types:
                if end_type not in compatible_types[start_type]:
                    return False, f"Incompatible pin types: {start_type} -> {end_type}"
                    
        # Check if pin is already connected
        existing_connections = self.getConnectionsForPin(start_comp, start_pin)
        if existing_connections and hasattr(start_pin, 'pin_type'):
            if start_pin.pin_type in ['input', 'output']:
                return False, "Pin already connected"
                
        return True, "Connection valid"
        
    def getConnectionsForPin(self, component, pin) -> List[Connection]:
        """Get connections for a specific pin"""
        pin_connections = []
        for conn in self.connections:
            if ((conn.start_component == component and conn.start_pin == pin) or
                (conn.end_component == component and conn.end_pin == pin)):
                pin_connections.append(conn)
        return pin_connections
        
    def autoRouteConnections(self):
        """Automatically route all connections"""
        for conn in self.connections:
            if isinstance(conn, EnhancedConnection):
                conn.setRoutingStyle("orthogonal")
                
    def getConnectionStatistics(self) -> dict:
        """Get connection statistics"""
        stats = {
            'total_connections': len(self.connections),
            'connection_types': {},
            'average_length': 0.0,
            'longest_connection': 0.0
        }
        
        total_length = 0.0
        max_length = 0.0
        
        for conn in self.connections:
            # Count by type
            conn_type = conn.connection_type
            stats['connection_types'][conn_type] = stats['connection_types'].get(conn_type, 0) + 1
            
            # Calculate lengths
            length = conn.getLength()
            total_length += length
            max_length = max(max_length, length)
            
        if self.connections:
            stats['average_length'] = total_length / len(self.connections)
        stats['longest_connection'] = max_length
        
        return stats
        
    def clearAllConnections(self):
        """Clear all connections"""
        for conn in self.connections[:]:
            self.deleteConnection(conn)
            
    def exportConnections(self) -> List[dict]:
        """Export connections to dictionary format"""
        exported = []
        for conn in self.connections:
            conn_data = {
                'start_point': {'x': conn.start_point.x(), 'y': conn.start_point.y()},
                'end_point': {'x': conn.end_point.x(), 'y': conn.end_point.y()},
                'connection_type': conn.connection_type,
                'signal_name': conn.signal_name,
                'start_component': conn.start_component.id if conn.start_component else None,
                'end_component': conn.end_component.id if conn.end_component else None,
            }
            
            if isinstance(conn, EnhancedConnection):
                conn_data['enhanced'] = True
                conn_data['routing_style'] = conn.connection_style
                conn_data['routing_points'] = [
                    {'x': p.x(), 'y': p.y()} for p in conn.routing_points
                ]
            else:
                conn_data['enhanced'] = False
                
            exported.append(conn_data)
            
        return exported
        
    def importConnections(self, connections_data: List[dict]) -> List[Connection]:
        """Import connections from dictionary format"""
        imported_connections = []
        
        for conn_data in connections_data:
            start_point = QPointF(conn_data['start_point']['x'], conn_data['start_point']['y'])
            end_point = QPointF(conn_data['end_point']['x'], conn_data['end_point']['y'])
            
            if conn_data.get('enhanced', False):
                conn = EnhancedConnection(start_point, end_point)
                conn.setRoutingStyle(conn_data.get('routing_style', 'orthogonal'))
                
                # Restore routing points
                routing_points = conn_data.get('routing_points', [])
                for point_data in routing_points:
                    point = QPointF(point_data['x'], point_data['y'])
                    conn.addRoutingPoint(point)
            else:
                conn = Connection(start_point, end_point)
                
            conn.setConnectionType(conn_data.get('connection_type', 'wire'))
            conn.setSignalName(conn_data.get('signal_name', ''))
            
            self.connections.append(conn)
            imported_connections.append(conn)
            
        return imported_connections

# Global connection manager instance
connection_manager = ConnectionManager()
