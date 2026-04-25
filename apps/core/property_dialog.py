"""
X-Seti - June04 2025 - Property Editor Dialog (SIMPLIFIED)
Allows editing of component properties without complex imports
"""
#this gpes in core/
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                           QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox,
                           QComboBox, QTextEdit, QLabel, QPushButton,
                           QGroupBox, QTabWidget, QWidget, QScrollArea,
                           QMessageBox, QDialogButtonBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PropertyEditorDialog(QDialog):
    """Simplified dialog for editing component properties"""
    
    def __init__(self, component, parent=None):
        super().__init__(parent)
        self.component = component
        self.property_widgets = {}
        
        self.setWindowTitle(f"Properties - {getattr(component, 'name', 'Component')}")
        self.setModal(True)
        self.resize(500, 400)
        
        self._setup_ui()
        self._load_component_data()
    
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Basic info group
        info_group = QGroupBox("Component Information")
        info_layout = QFormLayout(info_group)
        
        self.name_label = QLabel()
        self.name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        info_layout.addRow("Name:", self.name_label)
        
        self.id_label = QLabel()
        info_layout.addRow("ID:", self.id_label)
        
        self.category_label = QLabel()
        info_layout.addRow("Category:", self.category_label)
        
        self.package_label = QLabel()
        info_layout.addRow("Package:", self.package_label)
        
        layout.addWidget(info_group)
        
        # Position group
        pos_group = QGroupBox("Position")
        pos_layout = QFormLayout(pos_group)
        
        self.pos_x_spin = QDoubleSpinBox()
        self.pos_x_spin.setRange(-10000, 10000)
        self.pos_x_spin.setDecimals(1)
        pos_layout.addRow("X:", self.pos_x_spin)
        
        self.pos_y_spin = QDoubleSpinBox()
        self.pos_y_spin.setRange(-10000, 10000)
        self.pos_y_spin.setDecimals(1)
        pos_layout.addRow("Y:", self.pos_y_spin)
        
        layout.addWidget(pos_group)
        
        # Properties group
        self.props_group = QGroupBox("Properties")
        self.props_layout = QFormLayout(self.props_group)
        layout.addWidget(self.props_group)
        
        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def _load_component_data(self):
        """Load component data into the dialog"""
        # Basic info
        self.name_label.setText(getattr(self.component, 'name', 'Unknown'))
        self.id_label.setText(getattr(self.component, 'component_id', 'Unknown'))
        self.category_label.setText(getattr(self.component, 'category', 'Unknown'))
        self.package_label.setText(getattr(self.component, 'package_type', 'Unknown'))
        
        # Position
        pos = self.component.pos()
        self.pos_x_spin.setValue(pos.x())
        self.pos_y_spin.setValue(pos.y())
        
        # Load properties if they exist
        if hasattr(self.component, 'component_def') and hasattr(self.component.component_def, 'properties'):
            for prop in self.component.component_def.properties:
                prop_name = prop["name"]
                prop_type = prop["type"]
                prop_value = self.component.properties.get(prop_name, prop["default"])
                
                widget = None
                
                if prop_type == "string":
                    widget = QLineEdit()
                    widget.setText(str(prop_value))
                elif prop_type == "integer":
                    widget = QSpinBox()
                    widget.setRange(-1000000, 1000000)
                    widget.setValue(int(prop_value))
                elif prop_type == "float":
                    widget = QDoubleSpinBox()
                    widget.setRange(-1000000.0, 1000000.0)
                    widget.setDecimals(3)
                    widget.setValue(float(prop_value))
                elif prop_type == "boolean":
                    widget = QCheckBox()
                    widget.setChecked(bool(prop_value))
                
                if widget:
                    self.property_widgets[prop_name] = widget
                    self.props_layout.addRow(prop_name + ":", widget)
    
    def get_property_values(self):
        """Get the current property values from the dialog"""
        values = {}
        
        for prop_name, widget in self.property_widgets.items():
            if isinstance(widget, QLineEdit):
                values[prop_name] = widget.text()
            elif isinstance(widget, QSpinBox):
                values[prop_name] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                values[prop_name] = widget.value()
            elif isinstance(widget, QCheckBox):
                values[prop_name] = widget.isChecked()
        
        return values
    
    def get_position(self):
        """Get the position values"""
        return (self.pos_x_spin.value(), self.pos_y_spin.value())
    
    def accept(self):
        """Accept the dialog and apply changes"""
        try:
            # Update component properties
            new_props = self.get_property_values()
            if hasattr(self.component, 'properties'):
                self.component.properties.update(new_props)
            
            # Update position
            x, y = self.get_position()
            self.component.setPos(x, y)
            
            super().accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply changes:\n{str(e)}")


def show_component_properties(component, parent=None):
    """Show properties dialog for a component"""
    try:
        dialog = PropertyEditorDialog(component, parent)
        return dialog.exec() == QDialog.DialogCode.Accepted
    except Exception as e:
        print(f"Error showing properties dialog: {e}")
        return False


# Simple test function
def test_property_dialog():
    """Test the property dialog"""
    print("Property dialog module loaded successfully")
    return True


if __name__ == "__main__":
    test_property_dialog()
