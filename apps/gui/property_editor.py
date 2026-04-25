"""
X-Seti - June22 2025 - Property Editor System
Advanced property editing widgets and dialogs
"""

#this goes in ui/
from PyQt6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QPushButton, QTextEdit, QSlider, QColorDialog, QFileDialog,
    QGroupBox, QTabWidget, QScrollArea, QFrame, QSizePolicy,
    QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QToolButton, QMenu, QButtonGroup, QRadioButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer, QSize
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap, QPainter, QBrush, QPen
from typing import Any, Dict, List, Optional, Union, Callable
import json
import os

class PropertyEditorSignals(QObject):
    """Signals for property editor events"""
    valueChanged = pyqtSignal(str, object)  # property_name, new_value
    propertyAdded = pyqtSignal(str, object)  # property_name, initial_value
    propertyRemoved = pyqtSignal(str)  # property_name
    editorClosed = pyqtSignal()
    validationFailed = pyqtSignal(str, str)  # property_name, error_message

class BasePropertyEditor(QWidget):
    """Base class for property editors"""
    
    valueChanged = pyqtSignal(str, object)  # property_name, new_value
    
    def __init__(self, property_name: str, initial_value: Any, parent=None):
        super().__init__(parent)
        self.property_name = property_name
        self.initial_value = initial_value
        self.current_value = initial_value
        self.validation_rules = {}
        self.is_readonly = False
        self.setupUI()
        
    def setupUI(self):
        """Setup the editor UI - override in subclasses"""
        pass
        
    def getValue(self) -> Any:
        """Get current value - override in subclasses"""
        return self.current_value
        
    def setValue(self, value: Any):
        """Set value - override in subclasses"""
        self.current_value = value
        
    def setReadOnly(self, readonly: bool):
        """Set read-only mode"""
        self.is_readonly = readonly
        
    def validate(self, value: Any) -> tuple[bool, str]:
        """Validate value"""
        # Basic validation - override for specific rules
        return True, ""
        
    def reset(self):
        """Reset to initial value"""
        self.setValue(self.initial_value)
        
    def onValueChanged(self, value: Any):
        """Handle value change"""
        is_valid, error_msg = self.validate(value)
        if is_valid:
            self.current_value = value
            self.valueChanged.emit(self.property_name, value)
        else:
            self.showValidationError(error_msg)
            
    def showValidationError(self, message: str):
        """Show validation error"""
        # Could be implemented with tooltips or status messages
        print(f"Validation error for {self.property_name}: {message}")

class StringPropertyEditor(BasePropertyEditor):
    """String property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.line_edit = QLineEdit(str(self.initial_value))
        self.line_edit.textChanged.connect(self.onValueChanged)
        layout.addWidget(self.line_edit)
        
    def getValue(self) -> str:
        return self.line_edit.text()
        
    def setValue(self, value: Any):
        self.line_edit.setText(str(value))
        super().setValue(value)
        
    def setReadOnly(self, readonly: bool):
        super().setReadOnly(readonly)
        self.line_edit.setReadOnly(readonly)

class IntPropertyEditor(BasePropertyEditor):
    """Integer property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.spin_box = QSpinBox()
        self.spin_box.setRange(-999999, 999999)
        self.spin_box.setValue(int(self.initial_value) if isinstance(self.initial_value, (int, str)) else 0)
        self.spin_box.valueChanged.connect(self.onValueChanged)
        layout.addWidget(self.spin_box)
        
    def getValue(self) -> int:
        return self.spin_box.value()
        
    def setValue(self, value: Any):
        self.spin_box.setValue(int(value))
        super().setValue(value)
        
    def setReadOnly(self, readonly: bool):
        super().setReadOnly(readonly)
        self.spin_box.setReadOnly(readonly)

class FloatPropertyEditor(BasePropertyEditor):
    """Float property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.double_spin_box = QDoubleSpinBox()
        self.double_spin_box.setRange(-999999.0, 999999.0)
        self.double_spin_box.setDecimals(3)
        self.double_spin_box.setValue(float(self.initial_value) if isinstance(self.initial_value, (int, float, str)) else 0.0)
        self.double_spin_box.valueChanged.connect(self.onValueChanged)
        layout.addWidget(self.double_spin_box)
        
    def getValue(self) -> float:
        return self.double_spin_box.value()
        
    def setValue(self, value: Any):
        self.double_spin_box.setValue(float(value))
        super().setValue(value)
        
    def setReadOnly(self, readonly: bool):
        super().setReadOnly(readonly)
        self.double_spin_box.setReadOnly(readonly)

class BoolPropertyEditor(BasePropertyEditor):
    """Boolean property editor"""
    
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(bool(self.initial_value))
        self.checkbox.toggled.connect(self.onValueChanged)
        layout.addWidget(self.checkbox)
        
    def getValue(self) -> bool:
        return self.checkbox.isChecked()
        
    def setValue(self, value: Any):
        self.checkbox.setChecked(bool(value))
        super().setValue(value)
        
    def setReadOnly(self, readonly: bool):
        super().setReadOnly(readonly)
        self.checkbox.setEnabled(not readonly)

class ChoicePropertyEditor(BasePropertyEditor):
    """Choice/Enum property editor"""
    
    def __init__(self, property_name: str, initial_value: Any, choices: List[str], parent=None):
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
        
    def getValue(self) -> str:
        return self.combo_box.currentText()
        
    def setValue(self, value: Any):
        index = self.combo_box.findText(str(value))
        if index >= 0:
            self.combo_box.setCurrentIndex(index)
        super().setValue(value)
        
    def setReadOnly(self, readonly: bool):
        super().setReadOnly(readonly)
        self.combo_box.setEnabled(not readonly)

class ColorPropertyEditor(BasePropertyEditor):
    """Color property editor"""
    
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
        """Update color display"""
        self.color_button.setStyleSheet(f"background-color: {self.current_color.name()};")
        self.color_label.setText(self.current_color.name())
        
    def chooseColor(self):
        """Choose color dialog"""
        if not self.is_readonly:
            color = QColorDialog.getColor(self.current_color, self)
            if color.isValid():
                self.current_color = color
                self.updateColorDisplay()
                self.onValueChanged(color.name())
                
    def getValue(self) -> str:
        return self.current_color.name()
        
    def setValue(self, value: Any):
        self.current_color = QColor(value)
        self.updateColorDisplay()
        super().setValue(value)
        
    def setReadOnly(self, readonly: bool):
        super().setReadOnly(readonly)
        self.color_button.setEnabled(not readonly)

class FilePropertyEditor(BasePropertyEditor):
    """File path property editor"""
    
    def __init__(self, property_name: str, initial_value: Any, file_filter: str = "All Files (*)", parent=None):
        self.file_filter = file_filter
        super().__init__(property_name, initial_value, parent)
        
    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.path_edit = QLineEdit(str(self.initial_value))
        self.path_edit.textChanged.connect(self.onValueChanged)
        layout.addWidget(self.path_edit)
        
        self.browse_button = QPushButton("...")
        self.browse_button.setFixedWidth(30)
        self.browse_button.clicked.connect(self.browsePath)
        layout.addWidget(self.browse_button)
        
    def browsePath(self):
        """Browse for file path"""
        if not self.is_readonly:
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select {self.property_name}", 
                                                     self.path_edit.text(), self.file_filter)
            if file_path:
                self.path_edit.setText(file_path)
                
    def getValue(self) -> str:
        return self.path_edit.text()
        
    def setValue(self, value: Any):
        self.path_edit.setText(str(value))
        super().setValue(value)
        
    def setReadOnly(self, readonly: bool):
        super().setReadOnly(readonly)
        self.path_edit.setReadOnly(readonly)
        self.browse_button.setEnabled(not readonly)

class ListPropertyEditor(BasePropertyEditor):
    """List/Array property editor"""
    
    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(100)
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")
        self.edit_button = QPushButton("Edit")
        
        self.add_button.clicked.connect(self.addItem)
        self.remove_button.clicked.connect(self.removeItem)
        self.edit_button.clicked.connect(self.editItem)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.edit_button)
        layout.addLayout(button_layout)
        
        # Load initial values
        if isinstance(self.initial_value, list):
            for item in self.initial_value:
                self.list_widget.addItem(str(item))
                
    def addItem(self):
        """Add item to list"""
        if not self.is_readonly:
            from PyQt6.QtWidgets import QInputDialog
            text, ok = QInputDialog.getText(self, 'Add Item', 'Enter value:')
            if ok and text:
                self.list_widget.addItem(text)
                self.updateValue()
                
    def removeItem(self):
        """Remove selected item"""
        if not self.is_readonly:
            current_row = self.list_widget.currentRow()
            if current_row >= 0:
                self.list_widget.takeItem(current_row)
                self.updateValue()
                
    def editItem(self):
        """Edit selected item"""
        if not self.is_readonly:
            current_item = self.list_widget.currentItem()
            if current_item:
                from PyQt6.QtWidgets import QInputDialog
                text, ok = QInputDialog.getText(self, 'Edit Item', 'Enter value:', 
                                              text=current_item.text())
                if ok:
                    current_item.setText(text)
                    self.updateValue()
                    
    def updateValue(self):
        """Update value from list widget"""
        items = []
        for i in range(self.list_widget.count()):
            items.append(self.list_widget.item(i).text())
        self.onValueChanged(items)
        
    def getValue(self) -> List[str]:
        items = []
        for i in range(self.list_widget.count()):
            items.append(self.list_widget.item(i).text())
        return items
        
    def setValue(self, value: Any):
        self.list_widget.clear()
        if isinstance(value, list):
            for item in value:
                self.list_widget.addItem(str(item))
        super().setValue(value)
        
    def setReadOnly(self, readonly: bool):
        super().setReadOnly(readonly)
        self.add_button.setEnabled(not readonly)
        self.remove_button.setEnabled(not readonly)
        self.edit_button.setEnabled(not readonly)

class PropertyEditorFactory:
    """Factory for creating property editors"""
    
    @staticmethod
    def create_editor(property_name: str, value: Any, property_type: str = None, 
                     options: Dict[str, Any] = None) -> BasePropertyEditor:
        """Create appropriate property editor"""
        options = options or {}
        
        # Auto-detect type if not specified
        if property_type is None:
            if isinstance(value, bool):
                property_type = 'bool'
            elif isinstance(value, int):
                property_type = 'int'
            elif isinstance(value, float):
                property_type = 'float'
            elif isinstance(value, list):
                property_type = 'list'
            else:
                property_type = 'string'
                
        # Create editor based on type
        if property_type == 'string':
            return StringPropertyEditor(property_name, value)
        elif property_type == 'int':
            return IntPropertyEditor(property_name, value)
        elif property_type == 'float':
            return FloatPropertyEditor(property_name, value)
        elif property_type == 'bool':
            return BoolPropertyEditor(property_name, value)
        elif property_type == 'choice':
            choices = options.get('choices', [])
            return ChoicePropertyEditor(property_name, value, choices)
        elif property_type == 'color':
            return ColorPropertyEditor(property_name, value)
        elif property_type == 'file':
            file_filter = options.get('filter', "All Files (*)")
            return FilePropertyEditor(property_name, value, file_filter)
        elif property_type == 'list':
            return ListPropertyEditor(property_name, value)
        else:
            # Default to string editor
            return StringPropertyEditor(property_name, value)

class PropertyEditorDialog(QDialog):
    """Dialog for editing object properties"""
    
    def __init__(self, obj=None, properties: Dict[str, Any] = None, parent=None):
        super().__init__(parent)
        self.target_object = obj
        self.properties = properties or {}
        self.property_editors = {}
        self.setupUI()
        self.loadProperties()
        
    def setupUI(self):
        """Setup dialog UI"""
        self.setWindowTitle("Property Editor")
        self.setModal(True)
        self.resize(400, 500)
        
        layout = QVBoxLayout(self)
        
        # Properties area
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.properties_layout = QFormLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.apply_button = QPushButton("Apply")
        self.reset_button = QPushButton("Reset")
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.apply_button.clicked.connect(self.applyChanges)
        self.reset_button.clicked.connect(self.resetProperties)
        
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        layout.addLayout(button_layout)
        
    def loadProperties(self):
        """Load properties into editors"""
        # Clear existing editors
        for i in reversed(range(self.properties_layout.count())):
            self.properties_layout.itemAt(i).widget().setParent(None)
        self.property_editors.clear()
        
        # Create editors for each property
        for prop_name, prop_value in self.properties.items():
            editor = PropertyEditorFactory.create_editor(prop_name, prop_value)
            editor.valueChanged.connect(self.onPropertyChanged)
            
            self.properties_layout.addRow(prop_name + ":", editor)
            self.property_editors[prop_name] = editor
            
    def onPropertyChanged(self, property_name: str, new_value: Any):
        """Handle property change"""
        self.properties[property_name] = new_value
        
    def applyChanges(self):
        """Apply changes to target object"""
        if self.target_object:
            for prop_name, editor in self.property_editors.items():
                value = editor.getValue()
                if hasattr(self.target_object, prop_name):
                    setattr(self.target_object, prop_name, value)
                    
    def resetProperties(self):
        """Reset all properties"""
        for editor in self.property_editors.values():
            editor.reset()
            
    def getProperties(self) -> Dict[str, Any]:
        """Get current property values"""
        result = {}
        for prop_name, editor in self.property_editors.items():
            result[prop_name] = editor.getValue()
        return result

# Convenience functions
def edit_object_properties(obj, parent=None) -> bool:
    """Edit object properties in dialog"""
    if not obj:
        return False
        
    # Extract properties from object
    properties = {}
    for attr_name in dir(obj):
        if not attr_name.startswith('_') and not callable(getattr(obj, attr_name)):
            try:
                properties[attr_name] = getattr(obj, attr_name)
            except:
                pass
                
    dialog = PropertyEditorDialog(obj, properties, parent)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        dialog.applyChanges()
        return True
    return False

def edit_properties_dict(properties: Dict[str, Any], parent=None) -> Optional[Dict[str, Any]]:
    """Edit properties dictionary in dialog"""
    dialog = PropertyEditorDialog(None, properties.copy(), parent)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        return dialog.getProperties()
    return None

# Aliases for backward compatibility
PropertyEditor = BasePropertyEditor
PropertyEditorWidget = PropertyEditorDialog
PropertyManager = PropertyEditorFactory
