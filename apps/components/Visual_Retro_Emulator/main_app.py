#!/usr/bin/env python3
"""
X-Seti - June23 2025 - Visual Retro System Emulator Builder - Main Application
Clean version with simplified imports and removed conflicts
"""
#this belongs in main_app.py

import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

class RetroEmulatorApp(QApplication):
    """Main application class with robust error handling"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Set application properties
        self.setApplicationName("Visual Retro System Emulator Builder")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("Retro Computing Project")
        
        self.component_manager = None
        self.project_manager = None
        self.simulation_engine = None
        self.component_loader = None
        
        # Initialize main window
        self.main_window = None
        
        # Load systems step by step
        self.initialize_systems()
        self.setup_main_window()
        
    def show_error(self, title, message):
        """Show error message dialog"""
        try:
            QMessageBox.critical(None, title, message)
        except Exception as e:
            print(f"💥 Critical error showing dialog: {e}")
            print(f"Original error - {title}: {message}")
        
    def initialize_systems(self):
        """Initialize core systems with error handling"""
        print("Initializing core systems...")
        
        try:
            # Initialize Component Manager
            from core.components import ComponentManager
            self.component_manager = ComponentManager()
            print("✓ Component Manager initialized")
        except ImportError as e:
            print(f"⚠️ Could not load ComponentManager: {e}")
            self.component_manager = None
        
        try:
            # Initialize Project Manager - clean single import
            from managers.project_manager import ProjectManager
            self.project_manager = ProjectManager()
            print("✓ Project Manager initialized")
        except ImportError as e:
            print(f"⚠️ Could not load ProjectManager: {e}")
            # Try fallback
            try:
                from project_manager import ProjectManager
                self.project_manager = ProjectManager()
                print("✓ Project Manager (fallback) initialized")
            except ImportError as e2:
                print(f"⚠️ ProjectManager not available: {e2}")
                self.project_manager = None

        try:
            # Initialize Simulation Engine
            from core.simulation import SimulationEngine
            self.simulation_engine = SimulationEngine(self.component_manager)
            print("✓ Simulation Engine initialized")
        except ImportError as e:
            print(f"⚠️ Could not load SimulationEngine: {e}")
            self.simulation_engine = None

        try:
            # Initialize Component Loader
            from component_loader import get_global_loader
            self.component_loader = get_global_loader()
            print("✓ Component Loader initialized")
        except ImportError as e:
            print(f"⚠️ Could not load ComponentLoader: {e}")
            self.component_loader = None

    def setup_main_window(self):
        """Setup the main application window with robust error handling"""
        print("Setting up main window...")
        
        try:
            # Simple, clean import
            from ui.main_window import MainWindow
            self.main_window = MainWindow()
            
            # Connect core systems to UI if methods exist
            if hasattr(self.main_window, 'set_component_manager'):
                self.main_window.set_component_manager(self.component_manager)
            
            if hasattr(self.main_window, 'set_project_manager'):
                self.main_window.set_project_manager(self.project_manager)
            
            if hasattr(self.main_window, 'set_simulation_engine'):
                self.main_window.set_simulation_engine(self.simulation_engine)
            
            # Set references for direct access
            if hasattr(self.main_window, 'component_manager'):
                self.main_window.component_manager = self.component_manager
            if hasattr(self.main_window, 'project_manager'):
                self.main_window.project_manager = self.project_manager
            if hasattr(self.main_window, 'simulation_engine'):
                self.main_window.simulation_engine = self.simulation_engine
                
            # Load initial components
            self.load_initial_components()
            
            # Show the window
            self.main_window.show()
            print("✓ Main window displayed")
            
        except Exception as e:
            self.show_error("Failed to initialize main window", str(e))
            import traceback
            traceback.print_exc()
            sys.exit(1)
            
    def load_initial_components(self):
        """Load initial component library with error handling"""
        print("Loading initial components...")
        
        try:
            if self.component_loader and hasattr(self.component_loader, 'load_all_components'):
                components = self.component_loader.load_all_components()
                print(f"✓ Loaded {len(components)} components")
                
                # Connect to main window if available
                if hasattr(self.main_window, 'load_components'):
                    self.main_window.load_components(components)
                    
        except Exception as e:
            print(f"⚠️ Error loading initial components: {e}")

def main():
    """Main entry point"""
    app = RetroEmulatorApp(sys.argv)
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
