#!/usr/bin/env python3
"""
X-Seti - June07 2025 - Debug Startup Script
Diagnostic tool to identify and fix import issues
"""

import sys
import os
import traceback
from pathlib import Path

def print_separator(title):
    """Print a formatted separator"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def check_python_environment():
    """Check Python environment"""
    print_separator("PYTHON ENVIRONMENT")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Python Path: {sys.path[:3]}...")  # Show first 3 entries

def check_pyqt6():
    """Check PyQt6 installation"""
    print_separator("PYQT6 CHECK")
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt, QTimer
        from PyQt6.QtGui import QIcon
        print("✓ PyQt6 successfully imported")
        print(f"✓ PyQt6 available widgets: QApplication, Qt, QTimer, QIcon")
        return True
    except ImportError as e:
        print(f"❌ PyQt6 import failed: {e}")
        print("   Install with: pip install PyQt6")
        return False

def check_project_structure():
    """Check project directory structure"""
    print_separator("PROJECT STRUCTURE")
    
    current_dir = Path.cwd()
    print(f"Project Root: {current_dir}")
    
    # Required directories
    required_dirs = ["ui", "core", "managers", "database", "components"]
    for dir_name in required_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ directory found")
            # List key files
            py_files = list(dir_path.glob("*.py"))
            if py_files:
                print(f"  Contains: {', '.join([f.name for f in py_files[:5]])}")
                if len(py_files) > 5:
                    print(f"  ... and {len(py_files) - 5} more files")
        else:
            print(f"⚠️ {dir_name}/ directory missing")
    
    # Key files
    key_files = ["main_app.py", "project_manager.py", "component_library.py"]
    for file_name in key_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print(f"✓ {file_name} found")
        else:
            print(f"⚠️ {file_name} missing")

def test_core_imports():
    """Test core module imports"""
    print_separator("CORE IMPORTS TEST")
    
    # Test core components
    try:
        from core.components import BaseComponent, ComponentManager
        print("✓ core.components imported successfully")
    except ImportError as e:
        print(f"❌ core.components failed: {e}")
        try:
            # Check if file exists
            if os.path.exists("core/components.py"):
                print("  File exists, checking syntax...")
                with open("core/components.py", 'r') as f:
                    compile(f.read(), "core/components.py", "exec")
                print("  Syntax OK, import path issue")
            else:
                print("  File missing: core/components.py")
        except SyntaxError as se:
            print(f"  Syntax error: {se}")
    
    # Test project manager
    try:
        from project_manager import ProjectManager
        print("✓ project_manager imported successfully")
    except ImportError as e:
        print(f"❌ project_manager failed: {e}")
    
    # Test component library
    try:
        from component_library import ComponentLibrary
        print("✓ component_library imported successfully")
    except ImportError as e:
        print(f"❌ component_library failed: {e}")

def test_ui_imports():
    """Test UI module imports"""
    print_separator("UI IMPORTS TEST")
    
    ui_modules = [
        ("ui.main_window", "MainWindow"),
        ("ui.canvas", "EnhancedPCBCanvas"),
        ("ui.component_palette", "EnhancedComponentPalette"),
        ("ui.status_bar", "StatusBarManager"),
        ("ui.menu_bar", "MenuBarManager")
    ]
    
    for module_name, class_name in ui_modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✓ {module_name}.{class_name} imported successfully")
        except ImportError as e:
            print(f"❌ {module_name} failed: {e}")
        except AttributeError as e:
            print(f"⚠️ {module_name} imported but {class_name} not found: {e}")

def test_main_app():
    """Test main application import and creation"""
    print_separator("MAIN APPLICATION TEST")
    
    try:
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Test import
        print("Testing main_app import...")
        import main_app
        print("✓ main_app module imported")
        
        # Test app class
        print("Testing RetroEmulatorApp class...")
        app_class = getattr(main_app, 'RetroEmulatorApp', None)
        if app_class:
            print("✓ RetroEmulatorApp class found")
        else:
            print("❌ RetroEmulatorApp class not found")
        
    except ImportError as e:
        print(f"❌ main_app import failed: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"❌ main_app test failed: {e}")
        traceback.print_exc()

def create_minimal_test():
    """Create and run minimal application test"""
    print_separator("MINIMAL APPLICATION TEST")
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
        from PyQt6.QtCore import Qt
        
        print("Creating minimal QApplication...")
        app = QApplication([])
        
        print("Creating test window...")
        window = QMainWindow()
        window.setWindowTitle("Visual Retro Emulator - Debug Test")
        window.resize(400, 300)
        
        label = QLabel("Debug test successful!\nPress Ctrl+C to exit")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        window.setCentralWidget(label)
        
        print("✓ Minimal application created successfully")
        print("✓ Ready to show window")
        
        # Don't actually show window in debug mode
        # window.show()
        # return app.exec()
        
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ Minimal application test failed: {e}")
        traceback.print_exc()
        return False

def generate_fix_recommendations():
    """Generate fix recommendations based on test results"""
    print_separator("FIX RECOMMENDATIONS")
    
    fixes = []
    
    # Check for common issues
    if not os.path.exists("core/__init__.py"):
        fixes.append("Create core/__init__.py file (can be empty)")
    
    if not os.path.exists("ui/__init__.py"):
        fixes.append("Create ui/__init__.py file (can be empty)")
    
    if not os.path.exists("managers/__init__.py"):
        fixes.append("Create managers/__init__.py file (can be empty)")
    
    # Check for circular imports
    if os.path.exists("main_window.py") and os.path.exists("ui/main_window.py"):
        fixes.append("Remove duplicate main_window.py from root (keep only ui/main_window.py)")
    
    # Check for missing core modules
    if not os.path.exists("core/components.py"):
        fixes.append("Create core/components.py with BaseComponent class")
    
    if not os.path.exists("core/simulation.py"):
        fixes.append("Create core/simulation.py with SimulationEngine class")
    
    if fixes:
        print("Recommended fixes:")
        for i, fix in enumerate(fixes, 1):
            print(f"{i}. {fix}")
    else:
        print("✓ No obvious issues detected")
    
    print("\nGeneral recommendations:")
    print("1. Ensure all __init__.py files exist in package directories")
    print("2. Use absolute imports where possible")
    print("3. Add fallback imports for missing modules")
    print("4. Check for circular import dependencies")

def create_missing_init_files():
    """Create missing __init__.py files"""
    print_separator("CREATING MISSING INIT FILES")
    
    dirs_to_check = ["core", "ui", "managers", "database", "components", "utils"]
    
    for dir_name in dirs_to_check:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                try:
                    init_file.write_text("# Auto-generated __init__.py\n")
                    print(f"✓ Created {init_file}")
                except Exception as e:
                    print(f"❌ Failed to create {init_file}: {e}")
            else:
                print(f"✓ {init_file} already exists")