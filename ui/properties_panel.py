"""
X-Seti - June05 2025 - Properties Panel Widget
Displays and allows editing of selected component properties
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QTextEdit, QPushButton, QCheckBox, QScrollArea, QFrame,
    QColorDialog, QSlider, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette
import json

class PropertyEditor(QWidget):
    """Base class for property editors"""
    
    valueChanged = pyqtSignal(str, object)  # property_name, new_value
    
    def __init__(self, property_name, initial_value, parent=None):
        super().__init__(parent)
        self.property_name = property_name
        self.initial_value = initial_value
        self.setupUI()
        
    def setupUI(self):
        """Override in subclasses"""
        pass
        
    def getValue(self):
        """Override in subclasses"""
        return None
        
    def setValue(self, value):
        """Override in subclasses"""
        pass

class StringPropertyEditor(PropertyEditor):
    """Editor for string properties"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.line_edit = QLineEdit(str(self.initial_value))
        self.line_edit.textChanged.connect(self.onValueChanged)
        layout.addWidget(self.line_edit)
        
    def onValueChanged(self, text):
        self.valueChanged.emit(self.property_name, text)
        
    def getValue(self):
        return self.line_edit.text()
        
    def setValue(self, value):
        self.line_edit.setText(str(value))

class IntPropertyEditor(PropertyEditor):
    """Editor for integer properties"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.spin_box = QSpinBox()
        self.spin_box.setRange(-999999, 999999)
        self.spin_box.setValue(int(self.initial_value) if isinstance(self.initial_value, (int, str)) else 0)
        self.spin_box.valueChanged.connect(self.onValueChanged)
        layout.addWidget(self.spin_box)
        
    def onValueChanged(self, value):
        self.valueChanged.emit(self.property_name, value)
        
    def getValue(self):
        return self.spin_box.value()
        
    def setValue(self, value):
        self.spin_box.setValue(int(value))

class FloatPropertyEditor(PropertyEditor):
    """Editor for float properties"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.spin_box = QDoubleSpinBox()
        self.spin_box.setRange(-999999.0, 999999.0)
        self.spin_box.setDecimals(3)
        self.spin_box.setValue(float(self.initial_value) if isinstance(self.initial_value, (int, float, str)) else 0.0)
        self.spin_box.valueChanged.connect(self.onValueChanged)
        layout.addWidget(self.spin_box)
        
    def onValueChanged(self, value):
        self.valueChanged.emit(self.property_name, value)
        
    def getValue(self):
        return self.spin_box.value()
        
    def setValue(self, value):
        self.spin_box.setValue(float(value))

class BoolPropertyEditor(PropertyEditor):
    """Editor for boolean properties"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(bool(self.initial_value))
        self.checkbox.toggled.connect(self.onValueChanged)
        layout.addWidget(self.checkbox)
        
    def onValueChanged(self, checked):
        self.valueChanged.emit(self.property_name, checked)
        
    def getValue(self):
        return self.checkbox.isChecked()
        
    def setValue(self, value):
        self.checkbox.setChecked(bool(value))

class ChoicePropertyEditor(PropertyEditor):
    """Editor for choice/enum properties"""
    
    def __init__(self, property_name, initial_value, choices, parent=None):
        self.choices = choices
        super().__init__(property_name, initial_value, parent)
        
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.combo_box = QComboBox()
        self.combo_box.addItems([str(choice) for choice in self.choices])
        
        # Set current value
        current_text = str(self.initial_value)
        index = self.combo_box.findText(current_text)
        if index >= 0:
            self.combo_box.setCurrentIndex(index)
            
        self.combo_box.currentTextChanged.connect(self.onValueChanged)
        layout.addWidget(self.combo_box)
        
    def onValueChanged(self, text):
        self.valueChanged.emit(self.property_name, text)
        
    def getValue(self):
        return self.combo_box.currentText()
        
    def setValue(self, value):
        index = self.combo_box.findText(str(value))
        if index >= 0:
            self.combo_box.setCurrentIndex(index)

class ColorPropertyEditor(PropertyEditor):
    """Editor for color properties"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.color_button = QPushButton()
        self.color_button.setFixedSize(50, 25)
        self.color_button.clicked.connect(self.chooseColor)
        
        self.color_label = QLabel()
        
        # Set initial color
        self.current_color = QColor(self.initial_value) if isinstance(self.initial_value, str) else QColor(255, 255, 255)
        self.updateColorDisplay()
        
        layout.addWidget(self.color_button)
        layout.addWidget(self.color_label)
        layout.addStretch()
        
    def updateColorDisplay(self):
        self.color_button.setStyleSheet(f"background-color: {self.current_color.name()};")
        self.color_label.setText(self.current_color.name())
        
    def chooseColor(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.updateColorDisplay()
            self.valueChanged.emit(self.property_name, color.name())
            
    def getValue(self):
        return self.current_color.name()
        
    def setValue(self, value):
        self.current_color = QColor(value)
        self.updateColorDisplay()

class PropertiesPanelWidget(QWidget):
    """Main properties panel widget"""
    
    propertyChanged = pyqtSignal(str, object)  # property_name, new_value
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_object = None
        self.property_editors = {}
        self.setupUI()
        
    def setupUI(self):
        """Setup the properties panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Object info section
        self.info_group = QGroupBox("Object Information")
        info_layout = QFormLayout(self.info_group)
        
        self.name_label = QLabel("No selection")
        self.type_label = QLabel("")
        self.id_label = QLabel("")
        
        info_layout.addRow("Name:", self.name_label)
        info_layout.addRow("Type:", self.type_label)
        info_layout.addRow("ID:", self.id_label)
        
        layout.addWidget(self.info_group)
        
        # Properties tabs
        self.tabs = QTabWidget()
        
        # Basic properties tab
        self.basic_tab = QWidget()
        self.basic_scroll = QScrollArea()
        self.basic_scroll.setWidgetResizable(True)
        self.basic_scroll.setWidget(self.basic_tab)
        self.basic_layout = QFormLayout(self.basic_tab)
        self.tabs.addTab(self.basic_scroll, "Basic")
        
        # Advanced properties tab
        self.advanced_tab = QWidget()
        self.advanced_scroll = QScrollArea()
        self.advanced_scroll.setWidgetResizable(True)
        self.advanced_scroll.setWidget(self.advanced_tab)
        self.advanced_layout = QFormLayout(self.advanced_tab)
        self.tabs.addTab(self.advanced_scroll, "Advanced")
        
        # Custom properties tab
        self.custom_tab = QWidget()
        self.custom_scroll = QScrollArea()
        self.custom_scroll.setWidgetResizable(True)
        self.custom_scroll.setWidget(self.custom_tab)
        self.custom_layout = QVBoxLayout(self.custom_tab)
        self.tabs.addTab(self.custom_scroll, "Custom")
        
        layout.addWidget(self.tabs)
        
        # Custom property controls
        custom_controls = QHBoxLayout()
        self.add_property_btn = QPushButton("Add Property")
        self.add_property_btn.clicked.connect(self.addCustomProperty)
        self.remove_property_btn = QPushButton("Remove Property")
        self.remove_property_btn.clicked.connect(self.removeCustomProperty)
        
        custom_controls.addWidget(self.add_property_btn)
        custom_controls.addWidget(self.remove_property_btn)
        
        self.custom_layout.addLayout(custom_controls)
        self.custom_properties_form = QFormLayout()
        self.custom_layout.addLayout(self.custom_properties_form)
        self.custom_layout.addStretch()
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.resetProperties)
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.applyProperties)
        
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.apply_btn)
        layout.addLayout(button_layout)
        
        # Initially hide tabs since no object is selected
        self.tabs.setVisible(False)
        
    def setObject(self, obj):
        """Set the object whose properties to display"""
        self.current_object = obj
        self.refreshProperties()
        
    def refreshProperties(self):
        """Refresh the properties display"""
        self.clearProperties()
        
        if not self.current_object:
            self.info_group.setTitle("Object Information")
            self.name_label.setText("No selection")
            self.type_label.setText("")
            self.id_label.setText("")
            self.tabs.setVisible(False)
            return
            
        # Update object info
        obj_name = getattr(self.current_object, 'name', 'Unknown')
        obj_type = getattr(self.current_object, 'component_type', type(self.current_object).__name__)
        obj_id = getattr(self.current_object, 'id', id(self.current_object))
        
        self.info_group.setTitle(f"Properties - {obj_name}")
        self.name_label.setText(obj_name)
        self.type_label.setText(obj_type)
        self.id_label.setText(str(obj_id))
        
        self.tabs.setVisible(True)
        
        # Load properties
        self.loadBasicProperties()
        self.loadAdvancedProperties()
        self.loadCustomProperties()
        
    def loadBasicProperties(self):
        """Load basic properties into the basic tab"""
        if not self.current_object:
            return
            
        basic_props = self.getBasicProperties()
        
        for prop_name, prop_info in basic_props.items():
            editor = self.createPropertyEditor(prop_name, prop_info)
            if editor:
                self.basic_layout.addRow(prop_info.get('label', prop_name) + ":", editor)
                self.property_editors[prop_name] = editor
                
    def loadAdvancedProperties(self):
        """Load advanced properties into the advanced tab"""
        if not self.current_object:
            return
            
        advanced_props = self.getAdvancedProperties()
        
        for prop_name, prop_info in advanced_props.items():
            editor = self.createPropertyEditor(prop_name, prop_info)
            if editor:
                self.advanced_layout.addRow(prop_info.get('label', prop_name) + ":", editor)
                self.property_editors[prop_name] = editor
                
    def loadCustomProperties(self):
        """Load custom properties into the custom tab"""
        if not self.current_object:
            return
            
        custom_props = getattr(self.current_object, 'custom_properties', {})
        
        for prop_name, prop_value in custom_props.items():
            prop_info = {
                'value': prop_value,
                'type': type(prop_value).__name__
            }
            editor = self.createPropertyEditor(prop_name, prop_info)
            if editor:
                self.custom_properties_form.addRow(prop_name + ":", editor)
                self.property_editors[prop_name] = editor
                
    def getBasicProperties(self):
        """Get basic properties for the current object"""
        if not self.current_object:
            return {}
            
        props = {}
        
        # Common properties for all objects
        if hasattr(self.current_object, 'name'):
            props['name'] = {
                'value': self.current_object.name,
                'type': 'string',
                'label': 'Name'
            }
            
        if hasattr(self.current_object, 'x'):
            props['x'] = {
                'value': self.current_object.x(),
                'type': 'float',
                'label': 'X Position'
            }
            
        if hasattr(self.current_object, 'y'):
            props['y'] = {
                'value': self.current_object.y(),
                'type': 'float',
                'label': 'Y Position'
            }
            
        if hasattr(self.current_object, 'rotation'):
            props['rotation'] = {
                'value': getattr(self.current_object, 'rotation', 0),
                'type': 'float',
                'label': 'Rotation (degrees)'
            }
            
        # Component-specific properties
        if hasattr(self.current_object, 'component_type'):
            comp_type = self.current_object.component_type
            
            if comp_type == 'Processor':
                props.update({
                    'clock_speed': {
                        'value': getattr(self.current_object, 'clock_speed', '1 MHz'),
                        'type': 'string',
                        'label': 'Clock Speed'
                    },
                    'architecture': {
                        'value': getattr(self.current_object, 'architecture', '8-bit'),
                        'type': 'choice',
                        'choices': ['8-bit', '16-bit', '32-bit', '64-bit'],
                        'label': 'Architecture'
                    }
                })
                
            elif comp_type == 'Memory':
                props.update({
                    'capacity': {
                        'value': getattr(self.current_object, 'capacity', '64KB'),
                        'type': 'string',
                        'label': 'Capacity'
                    },
                    'memory_type': {
                        'value': getattr(self.current_object, 'memory_type', 'RAM'),
                        'type': 'choice',
                        'choices': ['RAM', 'ROM', 'SRAM', 'DRAM', 'EPROM', 'EEPROM'],
                        'label': 'Memory Type'
                    }
                })
                
            elif comp_type == 'Graphics':
                props.update({
                    'resolution': {
                        'value': getattr(self.current_object, 'resolution', '320x200'),
                        'type': 'string',
                        'label': 'Resolution'
                    },
                    'colors': {
                        'value': getattr(self.current_object, 'colors', 16),
                        'type': 'int',
                        'label': 'Number of Colors'
                    }
                })
                
        return props
        
    def getAdvancedProperties(self):
        """Get advanced properties for the current object"""
        if not self.current_object:
            return {}
            
        props = {}
        
        # Advanced positioning and sizing
        if hasattr(self.current_object, 'boundingRect'):
            rect = self.current_object.boundingRect()
            props.update({
                'width': {
                    'value': rect.width(),
                    'type': 'float',
                    'label': 'Width'
                },
                'height': {
                    'value': rect.height(),
                    'type': 'float',
                    'label': 'Height'
                }
            })
            
        # Visibility and interaction
        props.update({
            'visible': {
                'value': getattr(self.current_object, 'isVisible', lambda: True)(),
                'type': 'bool',
                'label': 'Visible'
            },
            'enabled': {
                'value': getattr(self.current_object, 'isEnabled', lambda: True)(),
                'type': 'bool',
                'label': 'Enabled'
            },
            'selectable': {
                'value': getattr(self.current_object, 'isSelectable', lambda: True)(),
                'type': 'bool',
                'label': 'Selectable'
            }
        })
        
        # Component-specific advanced properties
        if hasattr(self.current_object, 'component_type'):
            comp_type = self.current_object.component_type
            
            if comp_type == 'Processor':
                props.update({
                    'instruction_set': {
                        'value': getattr(self.current_object, 'instruction_set', '6502'),
                        'type': 'string',
                        'label': 'Instruction Set'
                    },
                    'cache_size': {
                        'value': getattr(self.current_object, 'cache_size', 0),
                        'type': 'int',
                        'label': 'Cache Size (KB)'
                    },
                    'pipeline_stages': {
                        'value': getattr(self.current_object, 'pipeline_stages', 1),
                        'type': 'int',
                        'label': 'Pipeline Stages'
                    }
                })
                
        return props
        
    def createPropertyEditor(self, prop_name, prop_info):
        """Create appropriate property editor for the property"""
        prop_type = prop_info.get('type', 'string')
        prop_value = prop_info.get('value')
        
        if prop_type == 'string':
            editor = StringPropertyEditor(prop_name, prop_value)
        elif prop_type == 'int':
            editor = IntPropertyEditor(prop_name, prop_value)
        elif prop_type == 'float':
            editor = FloatPropertyEditor(prop_name, prop_value)
        elif prop_type == 'bool':
            editor = BoolPropertyEditor(prop_name, prop_value)
        elif prop_type == 'choice':
            choices = prop_info.get('choices', [])
            editor = ChoicePropertyEditor(prop_name, prop_value, choices)
        elif prop_type == 'color':
            editor = ColorPropertyEditor(prop_name, prop_value)
        else:
            # Default to string editor
            editor = StringPropertyEditor(prop_name, prop_value)
            
        # Connect value changed signal
        editor.valueChanged.connect(self.onPropertyChanged)
        
        return editor
        
    def onPropertyChanged(self, property_name, new_value):
        """Handle property value changes"""
        if self.current_object and hasattr(self.current_object, property_name):
            try:
                # Apply the change to the object
                if property_name in ['x', 'y']:
                    # Handle position changes
                    if property_name == 'x':
                        self.current_object.setX(float(new_value))
                    else:
                        self.current_object.setY(float(new_value))
                elif property_name == 'rotation':
                    self.current_object.setRotation(float(new_value))
                elif property_name in ['visible', 'enabled', 'selectable']:
                    # Handle boolean properties
                    if property_name == 'visible':
                        self.current_object.setVisible(bool(new_value))
                    elif property_name == 'enabled':
                        self.current_object.setEnabled(bool(new_value))
                    # Add more as needed
                else:
                    # Generic property setting
                    setattr(self.current_object, property_name, new_value)
                    
                # Emit signal for external handling
                self.propertyChanged.emit(property_name, new_value)
                
            except Exception as e:
                print(f"Error setting property {property_name}: {e}")
                
    def clearProperties(self):
        """Clear all property editors"""
        self.property_editors.clear()
        
        # Clear basic properties
        while self.basic_layout.count():
            child = self.basic_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Clear advanced properties
        while self.advanced_layout.count():
            child = self.advanced_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Clear custom properties
        while self.custom_properties_form.count():
            child = self.custom_properties_form.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def addCustomProperty(self):
        """Add a custom property"""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        
        if not self.current_object:
            QMessageBox.warning(self, "Warning", "No object selected")
            return
            
        # Get property name
        name, ok = QInputDialog.getText(self, 'Add Property', 'Property name:')
        if not ok or not name:
            return
            
        # Get property type
        types = ['string', 'int', 'float', 'bool', 'color']
        prop_type, ok = QInputDialog.getItem(self, 'Property Type', 'Select type:', types, 0, False)
        if not ok:
            return
            
        # Get initial value
        if prop_type == 'string':
            value, ok = QInputDialog.getText(self, 'Initial Value', 'Enter initial value:')
        elif prop_type == 'int':
            value, ok = QInputDialog.getInt(self, 'Initial Value', 'Enter initial value:', 0)
        elif prop_type == 'float':
            value, ok = QInputDialog.getDouble(self, 'Initial Value', 'Enter initial value:', 0.0)
        elif prop_type == 'bool':
            value = False
            ok = True
        elif prop_type == 'color':
            value = '#FFFFFF'
            ok = True
        else:
            value = ''
            ok = True
            
        if not ok:
            return
            
        # Add to object
        if not hasattr(self.current_object, 'custom_properties'):
            self.current_object.custom_properties = {}
            
        self.current_object.custom_properties[name] = value
        
        # Refresh display
        self.refreshProperties()
        
    def removeCustomProperty(self):
        """Remove a custom property"""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        
        if not self.current_object or not hasattr(self.current_object, 'custom_properties'):
            QMessageBox.warning(self, "Warning", "No custom properties to remove")
            return
            
        props = list(self.current_object.custom_properties.keys())
        if not props:
            QMessageBox.warning(self, "Warning", "No custom properties to remove")
            return
            
        prop_name, ok = QInputDialog.getItem(self, 'Remove Property', 'Select property:', props, 0, False)
        if ok and prop_name:
            del self.current_object.custom_properties[prop_name]
            self.refreshProperties()
            
    def resetProperties(self):
        """Reset all properties to their original values"""
        if self.current_object:
            # This would need to be implemented based on how you store original values
            # For now, just refresh the display
            self.refreshProperties()
            
    def applyProperties(self):
        """Apply all current property values"""
        # In a real implementation, you might batch changes and apply them here
        # For now, changes are applied immediately
        pass
        
    def exportProperties(self):
        """Export current properties to JSON"""
        if not self.current_object:
            return None
            
        props = {}
        for name, editor in self.property_editors.items():
            props[name] = editor.getValue()
            
        return json.dumps(props, indent=2)
        
    def importProperties(self, json_data):
        """Import properties from JSON"""
        try:
            props = json.loads(json_data)
            for name, value in props.items():
                if name in self.property_editors:
                    self.property_editors[name].setValue(value)
        except Exception as e:
            print(f"Error importing properties: {e}")
            
    def getPropertyValue(self, property_name):
        """Get the current value of a specific property"""
        if property_name in self.property_editors:
            return self.property_editors[property_name].getValue()
        return None
        
    def setPropertyValue(self, property_name, value):
        """Set the value of a specific property"""
        if property_name in self.property_editors:
            self.property_editors[property_name].setValue(value)
            
    def hasProperty(self, property_name):
        """Check if a property exists"""
        return property_name in self.property_editors
