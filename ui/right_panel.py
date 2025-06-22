"""
X-Seti - June22 2025 - Properties Panel Widget
"""

#this belongs in ui/properties_panel.py

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
        return self.initial_value
        
    def setValue(self, value):
        """Override in subclasses"""
        pass

class StringPropertyEditor(PropertyEditor):
    """String property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.line_edit = QLineEdit(str(self.initial_value))
        self.line_edit.textChanged.connect(self.onTextChanged)
        layout.addWidget(self.line_edit)
        
    def onTextChanged(self, text):
        self.valueChanged.emit(self.property_name, text)
        
    def getValue(self):
        return self.line_edit.text()
        
    def setValue(self, value):
        self.line_edit.setText(str(value))

class IntPropertyEditor(PropertyEditor):
    """Integer property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.spin_box = QSpinBox()
        self.spin_box.setRange(-999999, 999999)
        self.spin_box.setValue(int(self.initial_value) if self.initial_value else 0)
        self.spin_box.valueChanged.connect(self.onValueChanged)
        layout.addWidget(self.spin_box)
        
    def onValueChanged(self, value):
        self.valueChanged.emit(self.property_name, value)
        
    def getValue(self):
        return self.spin_box.value()
        
    def setValue(self, value):
        self.spin_box.setValue(int(value) if value else 0)

class FloatPropertyEditor(PropertyEditor):
    """Float property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.double_spin_box = QDoubleSpinBox()
        self.double_spin_box.setRange(-999999.0, 999999.0)
        self.double_spin_box.setDecimals(3)
        self.double_spin_box.setValue(float(self.initial_value) if self.initial_value else 0.0)
        self.double_spin_box.valueChanged.connect(self.onValueChanged)
        layout.addWidget(self.double_spin_box)
        
    def onValueChanged(self, value):
        self.valueChanged.emit(self.property_name, value)
        
    def getValue(self):
        return self.double_spin_box.value()
        
    def setValue(self, value):
        self.double_spin_box.setValue(float(value) if value else 0.0)

class BoolPropertyEditor(PropertyEditor):
    """Boolean property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.check_box = QCheckBox()
        self.check_box.setChecked(bool(self.initial_value))
        self.check_box.toggled.connect(self.onToggled)
        layout.addWidget(self.check_box)
        
    def onToggled(self, checked):
        self.valueChanged.emit(self.property_name, checked)
        
    def getValue(self):
        return self.check_box.isChecked()
        
    def setValue(self, value):
        self.check_box.setChecked(bool(value))

class ChoicePropertyEditor(PropertyEditor):
    """Choice/dropdown property editor"""
    
    def __init__(self, property_name, initial_value, choices, parent=None):
        self.choices = choices
        super().__init__(property_name, initial_value, parent)
        
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(self.choices)
        
        # Set current value
        if self.initial_value in self.choices:
            self.combo_box.setCurrentText(str(self.initial_value))
        
        self.combo_box.currentTextChanged.connect(self.onCurrentTextChanged)
        layout.addWidget(self.combo_box)
        
    def onCurrentTextChanged(self, text):
        self.valueChanged.emit(self.property_name, text)
        
    def getValue(self):
        return self.combo_box.currentText()
        
    def setValue(self, value):
        if str(value) in self.choices:
            self.combo_box.setCurrentText(str(value))

class ColorPropertyEditor(PropertyEditor):
    """Color property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.color_button = QPushButton()
        self.color_button.setFixedSize(60, 25)
        self.current_color = QColor(self.initial_value) if self.initial_value else QColor(255, 255, 255)
        self.updateButtonColor()
        self.color_button.clicked.connect(self.openColorDialog)
        layout.addWidget(self.color_button)
        
        self.color_label = QLabel(self.current_color.name())
        layout.addWidget(self.color_label)
        
    def updateButtonColor(self):
        palette = self.color_button.palette()
        palette.setColor(QPalette.ColorRole.Button, self.current_color)
        self.color_button.setPalette(palette)
        self.color_button.setAutoFillBackground(True)
        
    def openColorDialog(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.updateButtonColor()
            self.color_label.setText(color.name())
            self.valueChanged.emit(self.property_name, color.name())
            
    def getValue(self):
        return self.current_color.name()
        
    def setValue(self, value):
        self.current_color = QColor(value) if value else QColor(255, 255, 255)
        self.updateButtonColor()
        self.color_label.setText(self.current_color.name())

class PropertiesPanel(QWidget):
    """
    Properties Panel
    
    Features:
    - Dynamic property editing for any selected object
    - Multiple property types (string, int, float, bool, choice, color)
    - Tabbed interface for basic/advanced properties
    - Real-time property change notifications
    - JSON serialization support
    """
    
    propertyChanged = pyqtSignal(str, object)  # property_name, new_value
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Current object being edited
        self.current_object = None
        self.property_editors = {}
        
        # Setup UI
        self._setup_ui()
        
        print("✓ Properties Panel initialized")
    
    def _setup_ui(self):
        """Setup the properties panel UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(6)
        
        # Title
        title_label = QLabel("Properties")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 4px;")
        main_layout.addWidget(title_label)
        
        # Object info
        self.object_info_label = QLabel("No object selected")
        self.object_info_label.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 4px;
                font-size: 9px;
                color: #7f8c8d;
            }
        """)
        main_layout.addWidget(self.object_info_label)
        
        # Tab widget for basic/advanced properties
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Basic properties tab
        self.basic_tab = QScrollArea()
        self.basic_tab.setWidgetResizable(True)
        self.basic_tab.setFrameShape(QFrame.Shape.NoFrame)
        self.tab_widget.addTab(self.basic_tab, "Basic")
        
        # Advanced properties tab
        self.advanced_tab = QScrollArea()
        self.advanced_tab.setWidgetResizable(True)
        self.advanced_tab.setFrameShape(QFrame.Shape.NoFrame)
        self.tab_widget.addTab(self.advanced_tab, "Advanced")
        
        # Create empty content widgets
        self._create_empty_content()
        
        # Action buttons
        self._create_action_buttons(main_layout)
    
    def _create_empty_content(self):
        """Create empty content for tabs"""
        # Basic tab content
        basic_content = QWidget()
        basic_layout = QVBoxLayout(basic_content)
        self.basic_properties_layout = QFormLayout()
        basic_layout.addLayout(self.basic_properties_layout)
        basic_layout.addStretch()
        self.basic_tab.setWidget(basic_content)
        
        # Advanced tab content
        advanced_content = QWidget()
        advanced_layout = QVBoxLayout(advanced_content)
        self.advanced_properties_layout = QFormLayout()
        advanced_layout.addLayout(self.advanced_properties_layout)
        advanced_layout.addStretch()
        self.advanced_tab.setWidget(advanced_content)
    
    def _create_action_buttons(self, layout):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.resetProperties)
        self.reset_button.setEnabled(False)
        button_layout.addWidget(self.reset_button)
        
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.applyProperties)
        self.apply_button.setEnabled(False)
        button_layout.addWidget(self.apply_button)
        
        layout.addLayout(button_layout)
    
    def setObject(self, obj):
        """Set the object to edit properties for"""
        self.current_object = obj
        self.property_editors.clear()
        
        if obj is None:
            self.object_info_label.setText("No object selected")
            self._clear_properties()
            self.reset_button.setEnabled(False)
            self.apply_button.setEnabled(False)
        else:
            # Update object info
            obj_name = getattr(obj, 'component_name', getattr(obj, 'name', 'Unknown Object'))
            obj_type = getattr(obj, 'component_type', type(obj).__name__)
            self.object_info_label.setText(f"{obj_name} ({obj_type})")
            
            # Load properties
            self._load_properties()
            self.reset_button.setEnabled(True)
            self.apply_button.setEnabled(True)
    
    def _clear_properties(self):
        """Clear all property editors"""
        # Clear basic properties
        while self.basic_properties_layout.rowCount() > 0:
            self.basic_properties_layout.removeRow(0)
        
        # Clear advanced properties
        while self.advanced_properties_layout.rowCount() > 0:
            self.advanced_properties_layout.removeRow(0)
    
    def _load_properties(self):
        """Load properties for the current object"""
        if not self.current_object:
            return
        
        # Clear existing properties
        self._clear_properties()
        
        # Get basic properties
        basic_props = self.getBasicProperties()
        for prop_name, prop_info in basic_props.items():
            editor = self._create_property_editor(prop_name, prop_info)
            if editor:
                self.property_editors[prop_name] = editor
                self.basic_properties_layout.addRow(prop_info.get('label', prop_name), editor)
        
        # Get advanced properties
        advanced_props = self.getAdvancedProperties()
        for prop_name, prop_info in advanced_props.items():
            editor = self._create_property_editor(prop_name, prop_info)
            if editor:
                self.property_editors[prop_name] = editor
                self.advanced_properties_layout.addRow(prop_info.get('label', prop_name), editor)
    
    def _create_property_editor(self, prop_name, prop_info):
        """Create appropriate property editor based on property type"""
        prop_type = prop_info.get('type', 'string')
        prop_value = prop_info.get('value')
        
        editor = None
        
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
        
        if editor:
            editor.valueChanged.connect(self.onPropertyChanged)
        
        return editor
    
    def getBasicProperties(self):
        """Get basic properties for the current object"""
        if not self.current_object:
            return {}
        
        props = {}
        
        # Common properties for all objects
        if hasattr(self.current_object, 'pos'):
            pos = self.current_object.pos()
            props.update({
                'x': {
                    'value': pos.x(),
                    'type': 'float',
                    'label': 'X Position'
                },
                'y': {
                    'value': pos.y(),
                    'type': 'float',
                    'label': 'Y Position'
                }
            })
        
        # Component-specific properties
        if hasattr(self.current_object, 'component_name'):
            props.update({
                'name': {
                    'value': getattr(self.current_object, 'component_name', 'Unknown'),
                    'type': 'string',
                    'label': 'Component Name'
                },
                'type': {
                    'value': getattr(self.current_object, 'component_type', 'Unknown'),
                    'type': 'string',
                    'label': 'Component Type'
                }
            })
        
        # Package type if available
        if hasattr(self.current_object, 'package_type'):
            props.update({
                'package': {
                    'value': getattr(self.current_object, 'package_type', 'DIP'),
                    'type': 'choice',
                    'choices': ['DIP-8', 'DIP-14', 'DIP-16', 'DIP-18', 'DIP-20', 'DIP-24', 'DIP-28', 'DIP-40', 'DIP-64', 'PLCC-44', 'PLCC-48', 'PLCC-84', 'QFP-44', 'QFP-64', 'QFP-100'],
                    'label': 'Package Type'
                }
            })
        
        # Processor-specific properties
        if hasattr(self.current_object, 'component_type') and self.current_object.component_type == 'Processor':
            props.update({
                'clock_speed': {
                    'value': getattr(self.current_object, 'clock_speed', 1.0),
                    'type': 'float',
                    'label': 'Clock Speed (MHz)'
                },
                'bit_width': {
                    'value': getattr(self.current_object, 'bit_width', 8),
                    'type': 'choice',
                    'choices': ['8', '16', '32', '64'],
                    'label': 'Bit Width'
                }
            })
        
        # Memory-specific properties
        if hasattr(self.current_object, 'component_type') and 'memory' in self.current_object.component_type.lower():
            props.update({
                'size': {
                    'value': getattr(self.current_object, 'memory_size', 1024),
                    'type': 'int',
                    'label': 'Memory Size (bytes)'
                },
                'access_time': {
                    'value': getattr(self.current_object, 'access_time', 100),
                    'type': 'int',
                    'label': 'Access Time (ns)'
                }
            })
        
        # Audio-specific properties
        if hasattr(self.current_object, 'component_type') and 'audio' in self.current_object.component_type.lower():
            props.update({
                'channels': {
                    'value': getattr(self.current_object, 'channels', 2),
                    'type': 'int',
                    'label': 'Audio Channels'
                },
                'sample_rate': {
                    'value': getattr(self.current_object, 'sample_rate', 44100),
                    'type': 'int',
                    'label': 'Sample Rate (Hz)'
                }
            })
        
        # Video-specific properties
        if hasattr(self.current_object, 'component_type') and 'video' in self.current_object.component_type.lower():
            props.update({
                'resolution_x': {
                    'value': getattr(self.current_object, 'resolution_x', 640),
                    'type': 'int',
                    'label': 'Resolution X'
                },
                'resolution_y': {
                    'value': getattr(self.current_object, 'resolution_y', 480),
                    'type': 'int',
                    'label': 'Resolution Y'
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
            
            elif 'memory' in comp_type.lower():
                props.update({
                    'read_only': {
                        'value': getattr(self.current_object, 'read_only', False),
                        'type': 'bool',
                        'label': 'Read Only'
                    },
                    'volatile': {
                        'value': getattr(self.current_object, 'volatile', True),
                        'type': 'bool',
                        'label': 'Volatile'
                    },
                    'error_correction': {
                        'value': getattr(self.current_object, 'error_correction', False),
                        'type': 'bool',
                        'label': 'Error Correction'
                    }
                })
        
        # Pin configuration
        if hasattr(self.current_object, 'pins'):
            pins = getattr(self.current_object, 'pins', [])
            props.update({
                'pin_count': {
                    'value': len(pins),
                    'type': 'int',
                    'label': 'Pin Count'
                }
            })
        
        return props
    
    def onPropertyChanged(self, property_name, new_value):
        """Handle property change"""
        if self.current_object:
            # Try to set the property on the object
            try:
                if hasattr(self.current_object, property_name):
                    setattr(self.current_object, property_name, new_value)
                elif property_name == 'x' and hasattr(self.current_object, 'setPos'):
                    pos = self.current_object.pos()
                    self.current_object.setPos(new_value, pos.y())
                elif property_name == 'y' and hasattr(self.current_object, 'setPos'):
                    pos = self.current_object.pos()
                    self.current_object.setPos(pos.x(), new_value)
                
                # Emit signal for external handling
                self.propertyChanged.emit(property_name, new_value)
                
                print(f"✓ Property changed: {property_name} = {new_value}")
                
            except Exception as e:
                print(f"❌ Error setting property {property_name}: {e}")
    
    def resetProperties(self):
        """Reset properties to original values"""
        if self.current_object:
            self._load_properties()
            print("✓ Properties reset")
    
    def applyProperties(self):
        """Apply all current property values"""
        for prop_name, editor in self.property_editors.items():
            value = editor.getValue()
            self.onPropertyChanged(prop_name, value)
        print("✓ All properties applied")
    
    def getPropertyValues(self):
        """Get all current property values as a dictionary"""
        values = {}
        for prop_name, editor in self.property_editors.items():
            values[prop_name] = editor.getValue()
        return values
    
    def setPropertyValues(self, values):
        """Set property values from a dictionary"""
        for prop_name, value in values.items():
            if prop_name in self.property_editors:
                self.property_editors[prop_name].setValue(value)

# Backward compatibility alias
PropertiesPanelWidget = PropertiesPanel

# Export
__all__ = [
    'PropertiesPanel', 'PropertiesPanelWidget', 'PropertyEditor',
    'StringPropertyEditor', 'IntPropertyEditor', 'FloatPropertyEditor',
    'BoolPropertyEditor', 'ChoicePropertyEditor', 'ColorPropertyEditor'
]
