#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Visual Retro System Emulator Builder - Main Application
Refactored modular architecture with fixed imports
"""

import sys
import os
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
        
    def initialize_systems(self):
        """Initialize core systems with error handling"""
        print("Initializing core systems...")
        
        # Initialize Component Manager
        from core.components import ComponentManager
        self.component_manager = ComponentManager()
        print("✓ Component Manager initialized")
        
        # Initialize Project Manager
        from managers.project_manager import ProjectManager
        from project_manager import ProjectManager
        print("✓ Project Manager loaded from root")
        self.project_manager = ProjectManager()
        print("✓ Project Manager initialized")

        # Initialize Simulation Engine
        from core.simulation import SimulationEngine
        self.simulation_engine = SimulationEngine(self.component_manager)
        print("✓ Simulation Engine initialized")

        # Initialize Component Loader
        from component_loader import get_global_loader
        self.component_loader = get_global_loader()
        print("✓ Component Loader initialized")

        
    def setup_main_window(self):
        """Setup the main application window with robust error handling"""
        print("Setting up main window...")
        
        try:
            # Try to import MainWindow from ui package
            from ui.main_window import MainWindow
            print("✓ MainWindow imported from ui package")
        except ImportError as e:
            print(f"⚠️ Could not import from ui.main_window: {e}")
            try:
                # Try importing from ui package init
                from ui import MainWindow
                if MainWindow is None:
                    raise ImportError("MainWindow is None in ui package")
                print("✓ MainWindow imported from ui package init")
            except ImportError as e2:
                print(f"⚠️ Could not import from ui package: {e2}")
                try:
                    # Try direct import from main_window
                    from main_window import MainWindow
                    print("✓ MainWindow imported from root")
                except ImportError as e3:
                    print(f"⚠️ Could not import MainWindow from root: {e3}")
                    self.show_error("Critical Error", 
                                  f"Could not import MainWindow:\n{e}\n{e2}\n{e3}")
                    sys.exit(1)
        
        try:
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
            if self.component_loader and hasattr(self.component_loader, 'refresh_library'):
                self.component_loader.refresh_library()
            
            # Update UI with loaded components if possible
            if (hasattr(self.main_window, 'refresh_component_palette') and 
                callable(self.main_window.refresh_component_palette)):
                self.main_window.refresh_component_palette()
                print("✓ Component palette refreshed")
            elif hasattr(self.main_window, 'component_palette'):
                if hasattr(self.main_window.component_palette, '_populate_tree'):
                    self.main_window.component_palette._populate_tree()
                    print("✓ Component tree populated")
                
        except Exception as e:
            print(f"⚠️ Error loading components: {e}")
            # Don't exit on component loading failure - continue with empty library
    
def main():
    """Main entry point with comprehensive error handling"""
    print("="*60)
    print("Visual Retro System Emulator Builder")
    print("="*60)
    
    # Enable high DPI scaling
    try:
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except:
        print("⚠️ High DPI scaling not available")
    
    # Create and run application
    app = None
    try:
        app = RetroEmulatorApp(sys.argv)
        print("✓ Application created successfully")
        
        # Run main loop
        return app.exec()
        
    except KeyboardInterrupt:
        print("\n⚠️ Application interrupted by user")
        return 0
    except Exception as e:
        print(f"💥 Critical application error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if app:
            try:
                app.quit()
            except:
                pass

if __name__ == "__main__":
    exit_code = main()
    print(f"\n🏁 Application exited with code: {exit_code}")
    sys.exit(exit_code)
