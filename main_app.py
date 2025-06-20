#!/usr/bin/env python3
"""
X-Seti - June07 2025 - Visual Retro System Emulator Builder - Main Application
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
        
        # Initialize core systems with fallbacks
        self.component_manager = None
        self.project_manager = None
        self.simulation_engine = None
        self.component_loader = None
        
        # Initialize main window
        self.main_window = None
        self.fallback_window = None
        
        # Load systems step by step
        self.initialize_systems()
        self.setup_main_window()
        
    def initialize_systems(self):
        """Initialize core systems with error handling"""
        print("Initializing core systems...")
        
        # Initialize Component Manager
        try:
            from core.components import ComponentManager
            self.component_manager = ComponentManager()
            print("✓ Component Manager initialized")
        except ImportError as e:
            print(f"⚠️ Using fallback ComponentManager: {e}")
            self.component_manager = self.create_fallback_component_manager()
        
        # Initialize Project Manager
        try:
            # Try multiple import paths
            try:
                from managers.project_manager import ProjectManager
                print("✓ Project Manager loaded from managers")
            except ImportError:
                from project_manager import ProjectManager
                print("✓ Project Manager loaded from root")
            
            self.project_manager = ProjectManager()
            print("✓ Project Manager initialized")
        except ImportError as e:
            print(f"⚠️ Using fallback ProjectManager: {e}")
            self.project_manager = self.create_fallback_project_manager()
        
        # Initialize Simulation Engine
        try:
            from core.simulation import SimulationEngine
            self.simulation_engine = SimulationEngine(self.component_manager)
            print("✓ Simulation Engine initialized")
        except ImportError as e:
            print(f"⚠️ Using fallback SimulationEngine: {e}")
            self.simulation_engine = self.create_fallback_simulation_engine()
        
        # Initialize Component Loader
        try:
            from integration_component_loader import get_global_loader
            self.component_loader = get_global_loader()
            print("✓ Component Loader initialized")
        except ImportError as e:
            print(f"⚠️ Using fallback ComponentLoader: {e}")
            self.component_loader = self.create_fallback_component_loader()
        
    def setup_main_window(self):
        """Setup the main application window with robust error handling"""
        print("Setting up main window...")
        
        try:
            # Try to import MainWindow from ui package
            from ui.main_window import MainWindow
            from ui.fallback_window import MainWindow
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
    
    def create_fallback_component_manager(self):
        """Create fallback component manager"""
        class FallbackComponentManager:
            def __init__(self):
                self.components = {}
                self.connections = []
                print("⚠️ Using fallback ComponentManager")
            
            def add_component(self, component):
                if hasattr(component, 'id'):
                    self.components[component.id] = component
                return True
            
            def remove_component(self, component_id):
                return self.components.pop(component_id, None) is not None
            
            def get_component(self, component_id):
                return self.components.get(component_id)
            
            def get_all_components(self):
                return list(self.components.values())
        
        return FallbackComponentManager()
    
    def create_fallback_project_manager(self):
        """Create fallback project manager"""
        class FallbackProjectManager:
            def __init__(self):
                self.current_project = None
                self.project_file = None
                self.modified = False
                print("⚠️ Using fallback ProjectManager")
            
            def new_project(self, name: str = "Untitled"):
                print(f"Creating new project: {name}")
                self.current_project = {"name": name, "components": {}, "connections": []}
                self.modified = False
                return True
            
            def open_project(self, path: str):
                print(f"Opening project: {path}")
                self.project_file = path
                return True
            
            def save_project(self, path: str = None):
                if path:
                    self.project_file = path
                print(f"Saving project: {self.project_file}")
                self.modified = False
                return True
            
            def close_project(self):
                print("Closing project")
                self.current_project = None
                self.project_file = None
                self.modified = False
            
            def is_modified(self):
                return self.modified
            
            def get_current_file(self):
                return self.project_file
        
        return FallbackProjectManager()
    
    def create_fallback_simulation_engine(self):
        """Create fallback simulation engine"""
        class FallbackSimulationEngine:
            def __init__(self, component_manager=None):
                self.component_manager = component_manager
                self.running = False
                print("⚠️ Using fallback SimulationEngine")
            
            def start_simulation(self):
                print("Starting simulation...")
                self.running = True
                return True
            
            def stop_simulation(self):
                print("Stopping simulation...")
                self.running = False
                return True
            
            def is_running(self):
                return self.running
        
        return FallbackSimulationEngine(self.component_manager)
    
    def create_fallback_component_loader(self):
        """Create fallback component loader"""
        class FallbackComponentLoader:
            def __init__(self):
                print("⚠️ Using fallback ComponentLoader")
            
            def refresh_library(self):
                print("Refreshing component library (fallback)")
                return []
            
            def load_from_directory(self, directory):
                print(f"Loading from directory: {directory} (fallback)")
                return []
        
        return FallbackComponentLoader()
            
    def show_error(self, title: str, message: str):
        """Show error message"""
        print(f"ERROR: {title}: {message}")
        
        # Try to show GUI message box if possible
        try:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle(title)
            msg_box.setText(message)
            msg_box.exec()
        except:
            # Fallback to console output
            print(f"GUI Error Dialog Failed - Console output only")

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
