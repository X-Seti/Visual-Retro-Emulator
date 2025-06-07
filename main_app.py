#!/usr/bin/env python3
"""
X-Seti - June07 2025 - Visual Retro System Emulator Builder - Main Application
Refactored modular architecture
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.main_window import MainWindow  # Changed from EnhancedMainWindow
    from core.components import ComponentManager
    from core.project_manager import ProjectManager
    from core.simulation import SimulationEngine
    from component_library import component_library, ComponentDefinition  # Added ComponentDefinition
    from integration_component_loader import get_global_loader
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are present")
    sys.exit(1)

class RetroEmulatorApp(QApplication):
    """Main application class"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Set application properties
        self.setApplicationName("Visual Retro System Emulator Builder")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("Retro Computing Project")
        
        # Initialize core systems
        self.component_manager = ComponentManager()
        self.project_manager = ProjectManager()
        self.simulation_engine = SimulationEngine(self.component_manager)
        self.component_loader = get_global_loader()
        
        # Initialize main window
        self.main_window = None
        self.setup_main_window()
        
        # Load components
        self.load_initial_components()
        
    def setup_main_window(self):
        """Setup the main application window"""
        try:
            self.main_window = MainWindow()
            
            # Connect core systems to UI
            if hasattr(self.main_window, 'set_component_manager'):
                self.main_window.set_component_manager(self.component_manager)
            if hasattr(self.main_window, 'set_project_manager'):
                self.main_window.set_project_manager(self.project_manager)
            if hasattr(self.main_window, 'set_simulation_engine'):
                self.main_window.set_simulation_engine(self.simulation_engine)
                
            # Show the window
            self.main_window.show()
            
        except Exception as e:
            self.show_error("Failed to initialize main window", str(e))
            sys.exit(1)
            
    def load_initial_components(self):
        """Load initial component library"""
        try:
            # Refresh the component library
            self.component_loader.refresh_library()
            
            # Update UI with loaded components
            if hasattr(self.main_window, 'refresh_component_palette'):
                self.main_window.refresh_component_palette()
                
        except Exception as e:
            self.show_error("Failed to load components", str(e))
            
    def show_error(self, title: str, message: str):
        """Show error message"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

def main():
    """Main entry point"""
    # Enable high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Create and run application
    app = RetroEmulatorApp(sys.argv)
    
    try:
        return app.exec()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 0
    except Exception as e:
        print(f"Application error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
