"""
Chip Editor Package
Provides chip editing functionality for the retro emulator
"""

import sys
import os

# Try to import directly from the chip_editor.py file in utils
utils_chip_editor_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'chip_editor.py')

try:
    # Import specific file without triggering utils/__init__.py
    import importlib.util
    spec = importlib.util.spec_from_file_location("utils_chip_editor", utils_chip_editor_path)
    utils_chip_editor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utils_chip_editor)
    
    # Extract classes from the loaded module
    for attr_name in dir(utils_chip_editor):
        if not attr_name.startswith('_'):
            attr_value = getattr(utils_chip_editor, attr_name)
            if isinstance(attr_value, type):  # Only import classes
                globals()[attr_name] = attr_value
                
    print("✅ Successfully imported chip editor classes directly from file")
    
except Exception as e:
    print(f"⚠️ Could not import from utils/chip_editor.py directly: {e}")
    
    # Create fallback classes
    from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
    from PyQt6.QtCore import pyqtSignal
    
    class ChipEditor(QDialog):
        """Fallback chip editor dialog"""
        
        chipCreated = pyqtSignal(dict)  # chip_data
        chipModified = pyqtSignal(dict)  # chip_data
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUI()
            print("⚠️ Using fallback ChipEditor")
            
        def setupUI(self):
            """Setup basic UI"""
            self.setWindowTitle("Chip Editor")
            self.setModal(True)
            self.resize(400, 300)
            
            layout = QVBoxLayout(self)
            
            info_label = QLabel("Chip Editor functionality not available.\n"
                               "Please ensure utils/chip_editor.py is properly configured.")
            layout.addWidget(info_label)
            
            close_button = QPushButton("Close")
            close_button.clicked.connect(self.close)
            layout.addWidget(close_button)
            
        def edit_chip(self, chip_data: dict = None):
            """Edit chip - fallback implementation"""
            QMessageBox.information(self, "Info", 
                                  "Chip editor functionality is not available.\n"
                                  "Please check utils/chip_editor.py")
            return None
            
        def create_new_chip(self):
            """Create new chip - fallback implementation"""
            QMessageBox.information(self, "Info", 
                                  "Chip creation functionality is not available.\n"
                                  "Please check utils/chip_editor.py")
            return None
    
    class ChipEditorDialog(ChipEditor):
        """Alias for backward compatibility"""
        pass
        
    class ChipDesigner(ChipEditor):
        """Alias for chip designer"""
        pass
        
    class ChipGenerator:
        """Fallback chip generator"""
        
        def __init__(self):
            print("⚠️ Using fallback ChipGenerator")
            
        def generate_chip(self, chip_type: str, **kwargs):
            """Generate chip - fallback implementation"""
            print(f"ChipGenerator.generate_chip called with type: {chip_type}")
            return {
                'name': f'Generated {chip_type}',
                'type': chip_type,
                'pins': 40,
                'package': 'DIP',
                'fallback': True
            }
            
        def get_supported_types(self):
            """Get supported chip types"""
            return ['CPU', 'Memory', 'Graphics', 'Audio', 'I/O', 'Custom']
    
    print("⚠️ Created fallback chip editor classes")

# Ensure we have the expected classes
if 'ChipEditorDialog' not in globals():
    if 'ChipEditor' in globals():
        ChipEditorDialog = ChipEditor
    else:
        from PyQt6.QtWidgets import QDialog
        class ChipEditorDialog(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle("Chip Editor Dialog")

# Common aliases for different naming conventions - only if base class exists
if 'ChipEditor' in globals():
    ChipDesigner = globals().get('ChipDesigner', ChipEditor)
    ChipCreator = globals().get('ChipCreator', ChipEditor)

__all__ = [
    'ChipEditor',
    'ChipEditorDialog', 
    'ChipDesigner',
    'ChipCreator',
    'ChipGenerator'
]

__version__ = '1.0.0'