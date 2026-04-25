"""
Chip Editor Dialog
Specific dialog implementation for chip editing
"""

# Import from the package init (which handles the utils import)
try:
    from . import ChipEditorDialog as BaseChipEditorDialog
    from . import ChipEditor, ChipGenerator
    
    # Re-export the main classes
    ChipEditorDialog = BaseChipEditorDialog
    
    print("✅ Successfully imported ChipEditorDialog from package")
    
except ImportError as e:
    print(f"⚠️ Could not import from package init: {e}")
    
    # Import directly from utils as fallback
    import sys
    import os
    
    utils_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils')
    if utils_path not in sys.path:
        sys.path.append(utils_path)
    
    try:
        from utils.chip_editor import ChipEditorDialog, ChipEditor
        print("✅ Successfully imported ChipEditorDialog from utils")
        
    except ImportError as e2:
        print(f"⚠️ Could not import from utils: {e2}")
        
        # Create fallback implementation
        from PyQt6.QtWidgets import (
            QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
            QLineEdit, QSpinBox, QComboBox, QPushButton, QTextEdit,
            QGroupBox, QCheckBox, QMessageBox, QTabWidget, QWidget
        )
        from PyQt6.QtCore import pyqtSignal, Qt
        
        class ChipEditorDialog(QDialog):
            """Fallback chip editor dialog with basic functionality"""
            
            chipCreated = pyqtSignal(dict)
            chipModified = pyqtSignal(dict)
            chipDeleted = pyqtSignal(str)
            
            def __init__(self, parent=None, chip_data=None):
                super().__init__(parent)
                self.chip_data = chip_data or {}
                self.is_new_chip = chip_data is None
                self.setupUI()
                self.load_chip_data()
                
            def setupUI(self):
                """Setup the dialog UI"""
                self.setWindowTitle("Chip Editor" if self.is_new_chip else f"Edit Chip - {self.chip_data.get('name', 'Unknown')}")
                self.setModal(True)
                self.resize(600, 500)
                
                layout = QVBoxLayout(self)
                
                # Create tabs
                self.tabs = QTabWidget()
                
                # Basic info tab
                self.basic_tab = QWidget()
                self.setup_basic_tab()
                self.tabs.addTab(self.basic_tab, "Basic Info")
                
                # Pins tab
                self.pins_tab = QWidget()
                self.setup_pins_tab()
                self.tabs.addTab(self.pins_tab, "Pins")
                
                # Properties tab
                self.props_tab = QWidget()
                self.setup_properties_tab()
                self.tabs.addTab(self.props_tab, "Properties")
                
                layout.addWidget(self.tabs)
                
                # Buttons
                button_layout = QHBoxLayout()
                
                self.ok_button = QPushButton("OK")
                self.cancel_button = QPushButton("Cancel")
                self.apply_button = QPushButton("Apply")
                
                self.ok_button.clicked.connect(self.accept)
                self.cancel_button.clicked.connect(self.reject)
                self.apply_button.clicked.connect(self.apply_changes)
                
                button_layout.addStretch()
                button_layout.addWidget(self.apply_button)
                button_layout.addWidget(self.cancel_button)
                button_layout.addWidget(self.ok_button)
                
                layout.addLayout(button_layout)
                
            def setup_basic_tab(self):
                """Setup basic information tab"""
                layout = QFormLayout(self.basic_tab)
                
                self.name_edit = QLineEdit()
                self.type_combo = QComboBox()
                self.type_combo.addItems(['CPU', 'Memory', 'Graphics', 'Audio', 'I/O', 'Custom'])
                self.manufacturer_edit = QLineEdit()
                self.package_combo = QComboBox()
                self.package_combo.addItems(['DIP', 'PLCC', 'QFP', 'BGA', 'SOIC'])
                self.pin_count_spin = QSpinBox()
                self.pin_count_spin.setRange(4, 256)
                self.pin_count_spin.setValue(40)
                
                layout.addRow("Name:", self.name_edit)
                layout.addRow("Type:", self.type_combo)
                layout.addRow("Manufacturer:", self.manufacturer_edit)
                layout.addRow("Package:", self.package_combo)
                layout.addRow("Pin Count:", self.pin_count_spin)
                
                # Description
                self.description_edit = QTextEdit()
                self.description_edit.setMaximumHeight(100)
                layout.addRow("Description:", self.description_edit)
                
            def setup_pins_tab(self):
                """Setup pins configuration tab"""
                layout = QVBoxLayout(self.pins_tab)
                
                info_label = QLabel("Pin configuration functionality would be implemented here.\n"
                                   "This is a fallback implementation.")
                layout.addWidget(info_label)
                
                # Add basic pin info
                self.pins_info = QTextEdit()
                self.pins_info.setPlainText("Pin definitions would be edited here...")
                layout.addWidget(self.pins_info)
                
            def setup_properties_tab(self):
                """Setup properties tab"""
                layout = QFormLayout(self.props_tab)
                
                self.voltage_edit = QLineEdit("5V")
                self.frequency_edit = QLineEdit("1 MHz")
                self.power_edit = QLineEdit("500 mW")
                
                layout.addRow("Operating Voltage:", self.voltage_edit)
                layout.addRow("Max Frequency:", self.frequency_edit)
                layout.addRow("Power Consumption:", self.power_edit)
                
            def load_chip_data(self):
                """Load chip data into the form"""
                if self.chip_data:
                    self.name_edit.setText(self.chip_data.get('name', ''))
                    
                    chip_type = self.chip_data.get('type', 'Custom')
                    type_index = self.type_combo.findText(chip_type)
                    if type_index >= 0:
                        self.type_combo.setCurrentIndex(type_index)
                        
                    self.manufacturer_edit.setText(self.chip_data.get('manufacturer', ''))
                    
                    package = self.chip_data.get('package', 'DIP')
                    package_index = self.package_combo.findText(package)
                    if package_index >= 0:
                        self.package_combo.setCurrentIndex(package_index)
                        
                    self.pin_count_spin.setValue(self.chip_data.get('pins', 40))
                    self.description_edit.setPlainText(self.chip_data.get('description', ''))
                    
            def get_chip_data(self):
                """Get chip data from the form"""
                return {
                    'name': self.name_edit.text(),
                    'type': self.type_combo.currentText(),
                    'manufacturer': self.manufacturer_edit.text(),
                    'package': self.package_combo.currentText(),
                    'pins': self.pin_count_spin.value(),
                    'description': self.description_edit.toPlainText(),
                    'properties': {
                        'voltage': self.voltage_edit.text(),
                        'frequency': self.frequency_edit.text(),
                        'power': self.power_edit.text()
                    }
                }
                
            def apply_changes(self):
                """Apply changes"""
                data = self.get_chip_data()
                if self.is_new_chip:
                    self.chipCreated.emit(data)
                else:
                    self.chipModified.emit(data)
                    
            def accept(self):
                """Accept dialog"""
                self.apply_changes()
                super().accept()
        
        class ChipEditor(ChipEditorDialog):
            """Alias for compatibility"""
            pass
            
        print("⚠️ Created fallback ChipEditorDialog with basic functionality")

# Aliases for different naming conventions
ChipEditor = ChipEditorDialog if 'ChipEditor' not in globals() else ChipEditor
ChipDesigner = ChipEditorDialog
ChipCreator = ChipEditorDialog

__all__ = ['ChipEditorDialog', 'ChipEditor', 'ChipDesigner', 'ChipCreator']