"""
Chip Editor Module
Provides chip editing functionality for the retro emulator
"""

import sys
import os

# Add utils directory to path
utils_path = os.path.join(os.path.dirname(__file__), 'utils')
if utils_path not in sys.path:
    sys.path.append(utils_path)

# Try to import from utils directory
try:
    from utils.chip_editor import *
    print("✅ Successfully imported chip editor from utils")
    
except ImportError as e:
    print(f"⚠️ Could not import from utils.chip_editor: {e}")
    
    # Try direct import if utils version doesn't work
    try:
        import chip_editor as utils_chip_editor
        # Re-export everything from the utils version
        for attr_name in dir(utils_chip_editor):
            if not attr_name.startswith('_'):
                globals()[attr_name] = getattr(utils_chip_editor, attr_name)
        print("✅ Successfully imported chip editor directly")
        
    except ImportError as e2:
        print(f"⚠️ Could not import chip_editor directly: {e2}")
        
        # Create fallback chip editor classes
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

# Ensure we have some basic exports
if 'ChipEditor' not in globals():
    # Create minimal fallback if nothing was imported
    class ChipEditor:
        def __init__(self):
            print("⚠️ Minimal ChipEditor fallback")
            
if 'ChipGenerator' not in globals():
    class ChipGenerator:
        def __init__(self):
            print("⚠️ Minimal ChipGenerator fallback")
            
        def generate_chip(self, chip_type: str):
            return {'name': f'Fallback {chip_type}', 'type': chip_type}

# Common aliases for different naming conventions
ChipEditorDialog = ChipEditor if 'ChipEditorDialog' not in globals() else ChipEditorDialog
ChipDesigner = ChipEditor if 'ChipDesigner' not in globals() else ChipDesigner
ChipCreator = ChipEditor if 'ChipCreator' not in globals() else ChipCreator

__all__ = [
    'ChipEditor',
    'ChipEditorDialog', 
    'ChipDesigner',
    'ChipCreator',
    'ChipGenerator'
]