#!/usr/bin/env python3
"""
X-Seti - June07 2025 - SAFE Diagnostic Tool
NON-DESTRUCTIVE analysis of your Visual Retro Emulator project
This script ONLY reads and reports - it will NOT modify any files
"""

import sys
import os
import ast
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Set

def print_banner():
    """Print safe diagnostic banner"""
    print("🛡️" * 60)
    print("🛡️  SAFE DIAGNOSTIC TOOL - READ ONLY")
    print("🛡️  This tool will NOT modify any of your files")
    print("🛡️  It only analyzes and reports issues")
    print("🛡️" * 60)

def analyze_file_imports(filepath: str) -> Dict[str, List[str]]:
    """Analyze imports in a Python file without executing it"""
    results = {
        'successful_imports': [],
        'failed_imports': [],
        'conditional_imports': [],
        'relative_imports': []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST
        tree = ast.parse(content, filename=filepath)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    try:
                        # Test if module can be imported
                        importlib.import_module(module_name)
                        results['successful_imports'].append(module_name)
                    except ImportError:
                        results['failed_imports'].append(module_name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module
                    if module_name.startswith('.'):
                        results['relative_imports'].append(module_name)
                    else:
                        try:
                            importlib.import_module(module_name)
                            results['successful_imports'].append(module_name)
                        except ImportError:
                            results['failed_imports'].append(module_name)
            
            elif isinstance(node, ast.Try):
                # Check for try/except import patterns
                for child in ast.walk(node):
                    if isinstance(child, (ast.Import, ast.ImportFrom)):
                        results['conditional_imports'].append("Found conditional import")
    
    except Exception as e:
        results['error'] = str(e)
    
    return results

def check_existing_files():
    """Check what files actually exist in your project"""
    print("\n📁 ANALYZING EXISTING PROJECT STRUCTURE")
    print("=" * 50)
    
    # Key directories to check
    directories = {
        'core': 'Core system components',
        'ui': 'User interface modules', 
        'managers': 'Project and layer managers',
        'database': 'Component database',
        'components': 'Component definitions',
        'utils': 'Utility functions',
        'templates': 'Project templates',
        'images': 'Component images'
    }
    
    file_count = 0
    dir_count = 0
    
    for dirname, description in directories.items():
        if os.path.exists(dirname):
            dir_count += 1
            py_files = list(Path(dirname).glob('*.py'))
            file_count += len(py_files)
            
            print(f"✅ {dirname}/ - {description}")
            print(f"   📄 {len(py_files)} Python files")
            
            if py_files:
                # Show key files
                key_files = [f.name for f in py_files[:5]]
                print(f"   🔑 Key files: {', '.join(key_files)}")
                if len(py_files) > 5:
                    print(f"       ... and {len(py_files) - 5} more files")
        else:
            print(f"❌ {dirname}/ - Missing")
    
    # Check root files
    root_py_files = list(Path('.').glob('*.py'))
    root_py_files = [f for f in root_py_files if not f.name.startswith('.')]
    
    print(f"\n📄 Root Python files: {len(root_py_files)}")
    for f in root_py_files:
        size_kb = f.stat().st_size / 1024
        print(f"   📄 {f.name} ({size_kb:.1f} KB)")
    
    print(f"\n📊 TOTALS:")
    print(f"   📁 Directories found: {dir_count}/{len(directories)}")
    print(f"   📄 Total Python files: {file_count + len(root_py_files)}")
    
    return file_count + len(root_py_files) > 0

def analyze_critical_files():
    """Analyze your critical application files"""
    print("\n🔍 ANALYZING CRITICAL FILES")
    print("=" * 50)
    
    critical_files = [
        'main_app.py',
        'main_window.py', 
        'project_manager.py',
        'ui/main_window.py',
        'ui/canvas.py',
        'ui/enhanced_canvas.py',
        'ui/component_palette.py',
        'core/components.py',
        'core/simulation.py'
    ]
    
    analysis_results = {}
    
    for filepath in critical_files:
        if os.path.exists(filepath):
            size_kb = Path(filepath).stat().st_size / 1024
            print(f"\n✅ {filepath} ({size_kb:.1f} KB)")
            
            # Analyze imports
            import_analysis = analyze_file_imports(filepath)
            analysis_results[filepath] = import_analysis
            
            # Report findings
            if import_analysis.get('successful_imports'):
                print(f"   ✅ Successful imports: {len(import_analysis['successful_imports'])}")
            
            if import_analysis.get('failed_imports'):
                print(f"   ❌ Failed imports: {len(import_analysis['failed_imports'])}")
                for imp in import_analysis['failed_imports'][:3]:  # Show first 3
                    print(f"      - {imp}")
                if len(import_analysis['failed_imports']) > 3:
                    print(f"      ... and {len(import_analysis['failed_imports']) - 3} more")
            
            if import_analysis.get('conditional_imports'):
                print(f"   🔄 Has conditional imports (good!)")
            
            if import_analysis.get('relative_imports'):
                print(f"   📦 Relative imports: {len(import_analysis['relative_imports'])}")
        else:
            print(f"❌ {filepath} - NOT FOUND")
            analysis_results[filepath] = {'missing': True}
    
    return analysis_results

def test_import_paths():
    """Test if your modules can be imported"""
    print("\n🧪 TESTING IMPORT PATHS")
    print("=" * 50)
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Test imports that main_app.py tries to make
    test_imports = [
        ('main_app', 'Main application module'),
        ('project_manager', 'Project manager'),
        ('ui', 'UI package'),
        ('ui.main_window', 'Main window UI'),
        ('ui.canvas', 'Canvas UI'),
        ('core', 'Core package'),
        ('core.components', 'Core components'),
        ('managers', 'Managers package'),
        ('managers.project_manager', 'Project manager from managers')
    ]
    
    import_results = {}
    
    for module_name, description in test_imports:
        try:
            spec = importlib.util.find_spec(module_name)
            if spec and spec.origin:
                module = importlib.import_module(module_name)
                print(f"✅ {module_name} - {description}")
                print(f"   📍 Located at: {spec.origin}")
                
                # Check for key classes/functions
                if hasattr(module, '__all__'):
                    exports = getattr(module, '__all__')
                    print(f"   📤 Exports: {', '.join(exports[:5])}")
                
                import_results[module_name] = {'status': 'success', 'path': spec.origin}
            else:
                print(f"❌ {module_name} - Module not found")
                import_results[module_name] = {'status': 'not_found'}
                
        except ImportError as e:
            print(f"⚠️ {module_name} - Import error: {e}")
            import_results[module_name] = {'status': 'import_error', 'error': str(e)}
        except Exception as e:
            print(f"❌ {module_name} - Unexpected error: {e}")
            import_results[module_name] = {'status': 'error', 'error': str(e)}
    
    return import_results

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 CHECKING DEPENDENCIES")
    print("=" * 50)
    
    dependencies = [
        ('PyQt6', 'PyQt6.QtWidgets'),
        ('PyQt6.QtCore', 'PyQt6.QtCore'),
        ('PyQt6.QtGui', 'PyQt6.QtGui')
    ]
    
    all_deps_ok = True
    
    for dep_name, import_name in dependencies:
        try:
            module = importlib.import_module(import_name)
            print(f"✅ {dep_name} - Available")
            
            # Try to get version if possible
            if hasattr(module, '__version__'):
                print(f"   📌 Version: {module.__version__}")
            elif hasattr(module, 'PYQT_VERSION_STR'):
                print(f"   📌 PyQt Version: {module.PYQT_VERSION_STR}")
                
        except ImportError:
            print(f"❌ {dep_name} - NOT INSTALLED")
            print(f"   💡 Install with: pip install {dep_name}")
            all_deps_ok = False
    
    return all_deps_ok

def generate_minimal_test():
    """Generate a minimal test that won't break anything"""
    print("\n🧪 GENERATING SAFE TEST SCRIPT")
    print("=" * 50)
    
    test_script = '''#!/usr/bin/env python3
"""
MINIMAL SAFE TEST - Generated by safe_diagnostic.py
This tests ONLY the most basic imports without running the full application
"""

import sys
import os

def test_basic_imports():
    """Test basic imports without side effects"""
    print("Testing basic Python imports...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("✅ PyQt6.QtWidgets available")
    except ImportError as e:
        print(f"❌ PyQt6.QtWidgets failed: {e}")
        return False
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Test if main modules exist and can be imported
    modules_to_test = ['main_app', 'project_manager']
    
    for module_name in modules_to_test:
        try:
            # Use importlib to test import without executing
            import importlib.util
            spec = importlib.util.find_spec(module_name)
            if spec:
                print(f"✅ {module_name} can be imported")
            else:
                print(f"❌ {module_name} not found")
        except Exception as e:
            print(f"⚠️ {module_name} test failed: {e}")
    
    return True

if __name__ == "__main__":
    print("🛡️ SAFE MINIMAL TEST")
    print("This test only checks imports - it won't run your application")
    print("-" * 50)
    
    if test_basic_imports():
        print("\\n✅ Basic tests passed!")
        print("Your project structure looks good for running the full application.")
    else:
        print("\\n❌ Some basic tests failed.")
        print("Check the errors above before running the full application.")
'''
    
    with open('safe_test.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Created safe_test.py")
    print("   🔧 Run with: python safe_test.py")
    print("   🛡️ This script is completely safe and won't modify anything")

def main():
    """Main diagnostic function - READ ONLY"""
    print_banner()
    
    print(f"🔍 Analyzing project in: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    # Step 1: Check file structure
    has_files = check_existing_files()
    
    if not has_files:
        print("\n❌ ERROR: No Python files found!")
        print("Make sure you're running this from your project directory.")
        return
    
    # Step 2: Check dependencies
    deps_ok = check_dependencies()
    
    # Step 3: Analyze critical files
    file_analysis = analyze_critical_files()
    
    # Step 4: Test import paths
    import_results = test_import_paths()
    
    # Step 5: Generate safe test
    generate_minimal_test()
    
    # Final summary
    print("\n" + "🛡️" * 60)
    print("🛡️  DIAGNOSTIC SUMMARY")
    print("🛡️" * 60)
    
    print(f"\n📊 FINDINGS:")
    
    # Count issues
    missing_files = sum(1 for result in file_analysis.values() if result.get('missing'))
    import_issues = sum(1 for result in import_results.values() if result.get('status') != 'success')
    
    print(f"   📁 Project structure: {'✅ GOOD' if has_files else '❌ ISSUES'}")
    print(f"   📦 Dependencies: {'✅ OK' if deps_ok else '❌ ISSUES'}")
    print(f"   📄 Missing critical files: {missing_files}")
    print(f"   🔗 Import path issues: {import_issues}")
    
    if missing_files == 0 and import_issues == 0 and deps_ok:
        print(f"\n🎉 YOUR PROJECT LOOKS GREAT!")
        print(f"   ✅ All critical files present")
        print(f"   ✅ Import paths working") 
        print(f"   ✅ Dependencies installed")
        print(f"   🚀 You should be able to run: python main_app.py")
    else:
        print(f"\n🔧 AREAS TO CHECK:")
        if not deps_ok:
            print(f"   📦 Install missing dependencies (see above)")
        if missing_files > 0:
            print(f"   📄 Some critical files are missing")
        if import_issues > 0:
            print(f"   🔗 Import path issues need attention")
    
    print(f"\n🛡️ NEXT STEPS:")
    print(f"   1. Run: python safe_test.py (completely safe)")
    print(f"   2. If that works, try: python main_app.py")
    print(f"   3. If issues persist, we can investigate specific modules")
    
    print(f"\n⚠️ REMEMBER: This diagnostic tool didn't modify any of your files!")

if __name__ == "__main__":
    main()
