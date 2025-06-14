#!/usr/bin/env python3
"""
X-Seti - June07 2025 - Startup Validator
Final validation script to ensure the application can start successfully
"""

import sys
import os
import importlib
import traceback
from pathlib import Path

def print_status(message: str, status: str = "INFO"):
    """Print formatted status message"""
    symbols = {
        "OK": "✓",
        "ERROR": "❌", 
        "WARNING": "⚠️",
        "INFO": "ℹ️"
    }
    print(f"{symbols.get(status, 'ℹ️')} {message}")

def validate_environment():
    """Validate Python environment"""
    print("\n" + "="*60)
    print(" ENVIRONMENT VALIDATION")
    print("="*60)
    
    print_status(f"Python version: {sys.version}", "INFO")
    print_status(f"Current directory: {os.getcwd()}", "INFO")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print_status("Python 3.8+ is recommended", "WARNING")
    else:
        print_status("Python version is suitable", "OK")
    
    return True

def validate_dependencies():
    """Validate required dependencies"""
    print("\n" + "="*60)
    print(" DEPENDENCY VALIDATION")
    print("="*60)
    
    dependencies = [
        "PyQt6.QtWidgets",
        "PyQt6.QtCore", 
        "PyQt6.QtGui"
    ]
    
    all_good = True
    
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print_status(f"{dep} available", "OK")
        except ImportError as e:
            print_status(f"{dep} missing: {e}", "ERROR")
            all_good = False
    
    if not all_good:
        print_status("Install missing dependencies with: pip install PyQt6", "INFO")
    
    return all_good

def validate_project_structure():
    """Validate project directory structure"""
    print("\n" + "="*60)
    print(" PROJECT STRUCTURE VALIDATION")
    print("="*60)
    
    required_files = [
        "main_app.py",
        "main_window.py", 
        "project_manager.py"
    ]
    
    required_dirs = [
        "core",
        "ui", 
        "managers",
        "database"
    ]
    
    all_good = True
    
    # Check files
    for file in required_files:
        if os.path.exists(file):
            print_status(f"File {file} exists", "OK")
        else:
            print_status(f"File {file} missing", "ERROR")
            all_good = False
    
    # Check directories
    for directory in required_dirs:
        if os.path.exists(directory):
            print_status(f"Directory {directory}/ exists", "OK")
            
            # Check for __init__.py
            init_file = os.path.join(directory, "__init__.py")
            if os.path.exists(init_file):
                print_status(f"  {init_file} exists", "OK")
            else:
                print_status(f"  {init_file} missing", "WARNING")
        else:
            print_status(f"Directory {directory}/ missing", "ERROR")
            all_good = False
    
    return all_good

def validate_imports():
    """Validate critical imports"""
    print("\n" + "="*60)
    print(" IMPORT VALIDATION")
    print("="*60)
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    imports_to_test = [
        ("main_app", "RetroEmulatorApp"),
        ("main_window", "MainWindow"),
        ("project_manager", "ProjectManager")
    ]
    
    all_good = True
    
    for module_name, class_name in imports_to_test:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, class_name):
                print_status(f"{module_name}.{class_name} available", "OK")
            else:
                print_status(f"{module_name}.{class_name} not found", "ERROR")
                all_good = False
        except ImportError as e:
            print_status(f"Cannot import {module_name}: {e}", "ERROR")
            all_good = False
        except Exception as e:
            print_status(f"Error importing {module_name}: {e}", "ERROR")
            all_good = False
    
    # Test package imports with fallbacks
    package_imports = [
        ("core", ["BaseComponent", "SimulationEngine"]),
        ("ui", ["MainWindow", "PCBCanvas"]),
        ("managers", ["ProjectManager", "LayerManager"])
    ]
    
    for package, classes in package_imports:
        try:
            pkg = importlib.import_module(package)
            print_status(f"Package {package} imports successfully", "OK")
            
            for class_name in classes:
                if hasattr(pkg, class_name) and getattr(pkg, class_name) is not None:
                    print_status(f"  {package}.{class_name} available", "OK")
                else:
                    print_status(f"  {package}.{class_name} not available (using fallback)", "WARNING")
                    
        except ImportError as e:
            print_status(f"Package {package} import failed: {e}", "WARNING")
    
    return all_good

def validate_app_creation():
    """Validate application can be created"""
    print("\n" + "="*60)
    print(" APPLICATION CREATION VALIDATION")
    print("="*60)
    
    try:
        # Import required modules
        from PyQt6.QtWidgets import QApplication
        import main_app
        
        print_status("Imports successful", "OK")
        
        # Create QApplication (required for Qt)
        app = QApplication([])
        print_status("QApplication created", "OK")
        
        # Test RetroEmulatorApp creation
        retro_app_class = getattr(main_app, 'RetroEmulatorApp', None)
        if retro_app_class:
            print_status("RetroEmulatorApp class found", "OK")
            
            # Test initialization (without showing UI)
            print_status("Testing app initialization...", "INFO")
            
            # Create app instance
            retro_app = retro_app_class([])
            print_status("RetroEmulatorApp created successfully", "OK")
            
            # Test that main window was created
            if hasattr(retro_app, 'main_window') and retro_app.main_window:
                print_status("Main window created", "OK")
            else:
                print_status("Main window not created", "WARNING")
            
            # Clean exit
            app.quit()
            print_status("Application cleanup successful", "OK")
            
            return True
            
        else:
            print_status("RetroEmulatorApp class not found", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Application creation failed: {e}", "ERROR")
        print("Detailed error:")
        traceback.print_exc()
        return False

def create_quick_fixes():
    """Create quick fix files if needed"""
    print("\n" + "="*60)
    print(" CREATING QUICK FIXES")
    print("="*60)
    
    # Create missing __init__.py files
    dirs_needing_init = ["core", "ui", "managers", "database", "components"]
    
    for dirname in dirs_needing_init:
        if os.path.exists(dirname):
            init_file = os.path.join(dirname, "__init__.py")
            if not os.path.exists(init_file):
                try:
                    with open(init_file, 'w') as f:
                        f.write(f'"""\n{dirname.title()} Package\n"""\n')
                    print_status(f"Created {init_file}", "OK")
                except Exception as e:
                    print_status(f"Failed to create {init_file}: {e}", "ERROR")
    
    # Create simple startup script
    startup_script = '''#!/usr/bin/env python3
"""
Simple startup script for Visual Retro Emulator
"""

import sys
import os

def main():
    """Main entry point"""
    try:
        from PyQt6.QtWidgets import QApplication
        import main_app
        
        # Create and run application
        app = main_app.RetroEmulatorApp(sys.argv)
        return app.exec()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure PyQt6 is installed: pip install PyQt6")
        return 1
    except Exception as e:
        print(f"Application error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open('run.py', 'w') as f:
        f.write(startup_script)
    
    print_status("Created run.py startup script", "OK")

def main():
    """Main validation function"""
    print("Visual Retro System Emulator Builder - Startup Validator")
    print("X-Seti - June 2025")
    
    # Run all validations
    validations = [
        ("Environment", validate_environment),
        ("Dependencies", validate_dependencies), 
        ("Project Structure", validate_project_structure),
        ("Imports", validate_imports),
        ("Application Creation", validate_app_creation)
    ]
    
    results = {}
    
    for name, validator in validations:
        try:
            results[name] = validator()
        except Exception as e:
            print_status(f"Validation {name} failed with exception: {e}", "ERROR")
            results[name] = False
    
    # Create quick fixes
    create_quick_fixes()
    
    # Final summary
    print("\n" + "="*60)
    print(" VALIDATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, passed in results.items():
        status = "OK" if passed else "ERROR"
        print_status(f"{name}: {'PASSED' if passed else 'FAILED'}", status)
        if not passed:
            all_passed = False
    
    if all_passed:
        print_status("\n🎉 ALL VALIDATIONS PASSED!", "OK")
        print_status("Your application should be ready to run!", "INFO")
        print_status("Run with: python main_app.py", "INFO")
        print_status("Or use: python run.py", "INFO")
    else:
        print_status("\n⚠️ Some validations failed", "WARNING")
        print_status("Check the errors above and fix them", "INFO")
        print_status("You can still try: python run.py", "INFO")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)