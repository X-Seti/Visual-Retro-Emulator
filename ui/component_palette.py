"""
X-Seti - June07 2025 - Component Palette Widget
Provides drag-and-drop interface for hardware components
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLabel, QPushButton, QLineEdit, QTextEdit, QGroupBox, QScrollArea,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QByteArray
from PyQt6.QtGui import QDrag, QPainter, QPixmap, QFont
import json

class DraggableComponentItem(QFrame):
    """Individual draggable component item"""
    
    def __init__(self, component_data, parent=None):
        super().__init__(parent)
        self.component_data = component_data
        self.setupUI()
        
    def setupUI(self):
        """Setup the component item UI"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.setFixedHeight(60)
        self.setStyleSheet("""
            DraggableComponentItem {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                margin: 2px;
            }
            DraggableComponentItem:hover {
                background-color: #e0e0e0;
                border: 1px solid #999;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Component icon/placeholder
        icon_label = QLabel("📦")
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 16px;")
        
        # Component info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        name_label = QLabel(self.component_data.get('name', 'Unknown'))
        name_label.setFont(QFont("", 9, QFont.Weight.Bold))
        
        type_label = QLabel(self.component_data.get('type', 'Unknown Type'))
        type_label.setFont(QFont("", 8))
        type_label.setStyleSheet("color: #666;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(type_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(info_layout)
        layout.addStretch()
        
    def mousePressEvent(self, event):
        """Handle mouse press for drag initiation"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
            
    def mouseMoveEvent(self, event):
        """Handle mouse move for drag operation"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
            
        if not hasattr(self, 'drag_start_position'):
            return
            
        if ((event.pos() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
            
        self.startDrag()
        
    def startDrag(self):
        """Start drag operation"""
        drag = QDrag(self)
        mimeData = QMimeData()
        
        # Set component data as JSON
        component_json = json.dumps(self.component_data)
        mimeData.setText(component_json)
        mimeData.setData("application/x-component", QByteArray(component_json.encode()))
        
        drag.setMimeData(mimeData)
        
        # Create drag pixmap
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setOpacity(0.7)
        self.render(painter)
        painter.end()
        
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.drag_start_position)
        
        # Execute drag
        drag.exec(Qt.DropAction.CopyAction)


class ComponentPaletteWidget(QWidget):
    """Main component palette widget"""
    
    componentSelected = pyqtSignal(dict)  # Emitted when component is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.components_data = {}
        self.setupUI()
        self.loadDefaultComponents()
        
    def setupUI(self):
        """Setup the palette UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Search/filter section
        search_group = QGroupBox("Search Components")
        search_layout = QVBoxLayout(search_group)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search components...")
        self.search_input.textChanged.connect(self.filterComponents)
        search_layout.addWidget(self.search_input)
        
        layout.addWidget(search_group)
        
        # Components tree/list
        components_group = QGroupBox("Components")
        components_layout = QVBoxLayout(components_group)
        
        # Create scrollable area for components
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.components_widget = QWidget()
        self.components_layout = QVBoxLayout(self.components_widget)
        self.components_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.components_widget)
        components_layout.addWidget(scroll_area)
        
        layout.addWidget(components_group)
        
        # Component details section
        details_group = QGroupBox("Component Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setMaximumHeight(100)
        self.details_text.setReadOnly(True)
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_group)
        
        # Add component button
        self.add_component_btn = QPushButton("Add Custom Component")
        self.add_component_btn.clicked.connect(self.addCustomComponent)
        layout.addWidget(self.add_component_btn)
        
    def loadDefaultComponents(self):
        """Load default hardware components"""
        default_components = {
            "Processors": [
                {
                    "name": "6502 CPU",
                    "type": "Processor",
                    "description": "8-bit microprocessor used in Apple II, Commodore 64",
                    "pins": 40,
                    "properties": {
                        "clock_speed": "1-2 MHz",
                        "architecture": "8-bit",
                        "instruction_set": "6502"
                    }
                },
                {
                    "name": "Z80 CPU",
                    "type": "Processor", 
                    "description": "8-bit microprocessor used in many retro computers",
                    "pins": 40,
                    "properties": {
                        "clock_speed": "2-8 MHz",
                        "architecture": "8-bit",
                        "instruction_set": "Z80"
                    }
                },
                {
                    "name": "68000 CPU",
                    "type": "Processor",
                    "description": "16/32-bit processor used in Amiga, Atari ST",
                    "pins": 64,
                    "properties": {
                        "clock_speed": "8-16 MHz",
                        "architecture": "16/32-bit",
                        "instruction_set": "68000"
                    }
                }
            ],
            "Memory": [
                {
                    "name": "RAM 64KB",
                    "type": "Memory",
                    "description": "64KB Random Access Memory",
                    "pins": 28,
                    "properties": {
                        "capacity": "64KB",
                        "type": "SRAM",
                        "access_time": "150ns"
                    }
                },
                {
                    "name": "ROM 32KB",
                    "type": "Memory",
                    "description": "32KB Read-Only Memory",
                    "pins": 28,
                    "properties": {
                        "capacity": "32KB",
                        "type": "EPROM",
                        "access_time": "200ns"
                    }
                }
            ],
            "Graphics": [
                {
                    "name": "VIC-II",
                    "type": "Graphics",
                    "description": "Video Interface Chip from Commodore 64",
                    "pins": 40,
                    "properties": {
                        "resolution": "320x200",
                        "colors": "16",
                        "sprites": "8"
                    }
                },
                {
                    "name": "TMS9918",
                    "type": "Graphics",
                    "description": "Texas Instruments Video Display Processor",
                    "pins": 40,
                    "properties": {
                        "resolution": "256x192",
                        "colors": "16",
                        "modes": "Graphics/Text"
                    }
                }
            ],
            "Audio": [
                {
                    "name": "SID 6581",
                    "type": "Audio",
                    "description": "Sound Interface Device from Commodore 64",
                    "pins": 28,
                    "properties": {
                        "voices": "3",
                        "waveforms": "4",
                        "filters": "Multi-mode"
                    }
                },
                {
                    "name": "AY-3-8910",
                    "type": "Audio",
                    "description": "Programmable Sound Generator",
                    "pins": 40,
                    "properties": {
                        "voices": "3",
                        "waveforms": "Square",
                        "noise": "Yes"
                    }
                }
            ],
            "I/O": [
                {
                    "name": "6522 VIA",
                    "type": "I/O",
                    "description": "Versatile Interface Adapter",
                    "pins": 40,
                    "properties": {
                        "ports": "2x8-bit",
                        "timers": "2",
                        "shift_register": "Yes"
                    }
                },
                {
                    "name": "8255 PPI",
                    "type": "I/O",
                    "description": "Programmable Peripheral Interface",
                    "pins": 40,
                    "properties": {
                        "ports": "3x8-bit",
                        "modes": "3",
                        "bidirectional": "Yes"
                    }
                }
            ]
        }
        
        self.components_data = default_components
        self.refreshComponentsList()
        
    def refreshComponentsList(self):
        """Refresh the components list display"""
        # Clear existing components
        for i in reversed(range(self.components_layout.count())):
            child = self.components_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                
        # Add components by category
        for category, components in self.components_data.items():
            # Category header
            category_label = QLabel(category)
            category_label.setFont(QFont("", 10, QFont.Weight.Bold))
            category_label.setStyleSheet("""
                QLabel {
                    background-color: #ddd;
                    padding: 4px;
                    border-radius: 2px;
                    margin-top: 4px;
                }
            """)
            self.components_layout.addWidget(category_label)
            
            # Components in category
            for component in components:
                component_item = DraggableComponentItem(component)
                component_item.mousePressEvent = lambda event, comp=component: self.selectComponent(comp, event)
                self.components_layout.addWidget(component_item)
                
    def selectComponent(self, component, event):
        """Handle component selection"""
        self.updateComponentDetails(component)
        self.componentSelected.emit(component)
        
        # Call original mouse press event for drag functionality
        super(DraggableComponentItem, event.widget()).mousePressEvent(event)
        
    def updateComponentDetails(self, component):
        """Update component details display"""
        details = f"Name: {component.get('name', 'Unknown')}\n"
        details += f"Type: {component.get('type', 'Unknown')}\n"
        details += f"Pins: {component.get('pins', 'Unknown')}\n"
        details += f"Description: {component.get('description', 'No description')}\n\n"
        
        if 'properties' in component:
            details += "Properties:\n"
            for key, value in component['properties'].items():
                details += f"  {key.replace('_', ' ').title()}: {value}\n"
                
        self.details_text.setText(details)
        
    def filterComponents(self, text):
        """Filter components based on search text"""
        # This is a simple implementation - you could make it more sophisticated
        search_text = text.lower()
        
        for i in range(self.components_layout.count()):
            item = self.components_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, DraggableComponentItem):
                    component_name = widget.component_data.get('name', '').lower()
                    component_type = widget.component_data.get('type', '').lower()
                    should_show = (search_text in component_name or 
                                 search_text in component_type or 
                                 not search_text)
                    widget.setVisible(should_show)
                    
    def addCustomComponent(self):
        """Add a custom component (placeholder for future implementation)"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, 'Add Component', 'Component name:')
        if ok and name:
            # Simple custom component - in a real implementation,
            # you'd want a proper dialog for all properties
            custom_component = {
                "name": name,
                "type": "Custom",
                "description": "User-defined component",
                "pins": 40,
                "properties": {}
            }
            
            if "Custom" not in self.components_data:
                self.components_data["Custom"] = []
            self.components_data["Custom"].append(custom_component)
            self.refreshComponentsList()
            
    def getSelectedComponent(self):
        """Get currently selected component"""
        # Implementation depends on your selection mechanism
        return None
        
    def addComponentCategory(self, category_name, components_list):
        """Add a new category of components"""
        self.components_data[category_name] = components_list
        self.refreshComponentsList()
        
    def removeComponent(self, component_name, category=None):
        """Remove a component"""
        if category and category in self.components_data:
            self.components_data[category] = [
                comp for comp in self.components_data[category] 
                if comp.get('name') != component_name
            ]
        else:
            # Search all categories
            for cat_components in self.components_data.values():
                cat_components[:] = [
                    comp for comp in cat_components 
                    if comp.get('name') != component_name
                ]
        self.refreshComponentsList()

# Alias for backward compatibility
EnhancedComponentPalette = ComponentPaletteWidget
