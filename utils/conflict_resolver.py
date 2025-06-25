#!/usr/bin/env python3
"""
X-Seti - June24 2025 - Visual Retro Emulator Function Conflict Resolver
Identifies and resolves function/class naming conflicts

#this belongs in utils/conflict_resolver.py
"""

import os
import ast
import importlib.util
from pathlib import Path
from typing import Dict, List, Set, Tuple

class ConflictResolver:
    """Finds and resolves function/class conflicts in the project"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.conflicts = {}
        self.duplicate_files = []
        self.python_files = []
        
    def scan_project(self):
        """Scan all Python files for conflicts"""
        print("🔍 Scanning Visual Retro Emulator for conflicts...")
        
        # Find all Python files
        self._find_python_files()
        
        # Find function/class conflicts
        self._find_function_conflicts()
        
        # Find duplicate files
        self._find_duplicate_files()
        
        return self.conflicts
    
    def _find_python_files(self):
        """Find all Python files in project"""
        for py_file in self.project_root.rglob("*.py"):
            if not any(skip in str(py_file) for skip in ['.git', '__pycache__', '.venv']):
                self.python_files.append(py_file)
        
        print(f"📁 Found {len(self.python_files)} Python files")
    
    def _find_function_conflicts(self):
        """Find function and class naming conflicts"""
        functions = {}  # function_name -> [files]
        classes = {}    # class_name -> [files]
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        if func_name not in functions:
                            functions[func_name] = []
                        functions[func_name].append(str(py_file))
                    
                    elif isinstance(node, ast.ClassDef):
                        class_name = node.name
                        if class_name not in classes:
                            classes[class_name] = []
                        classes[class_name].append(str(py_file))
                        
            except Exception as e:
                print(f"⚠️ Error parsing {py_file}: {e}")
        
        # Find conflicts (same name in multiple files)
        self.conflicts['functions'] = {
            name: files for name, files in functions.items() 
            if len(files) > 1 and not name.startswith('_')
        }
        
        self.conflicts['classes'] = {
            name: files for name, files in classes.items() 
            if len(files) > 1
        }
    
    def _find_duplicate_files(self):
        """Find duplicate or similar files"""
        known_duplicates = [
            # CAD Tools conflicts
            ('ui/cad_tools_panel.py', 'ui/cad_tools.py'),
            
            # Project manager conflicts  
            ('project_manager.py', 'core/project_manager.py'),
            
            # Component conflicts
            ('components/cpu/motorola_68000.py', 'components/amiga/motorola_68000_a500.py'),
            ('components/amiga/amiga_agnus.py', 'components/amiga/amiga_agnus_8372a.py'),
            
            # Main app variants
            ('main_app.py', 'enhanced_main_app_hotkeys.py'),
        ]
        
        for file1, file2 in known_duplicates:
            path1 = self.project_root / file1
            path2 = self.project_root / file2
            
            if path1.exists() and path2.exists():
                self.duplicate_files.append((str(path1), str(path2)))
    
    def print_conflicts(self):
        """Print detailed conflict report"""
        print("\n📊 CONFLICT ANALYSIS REPORT")
        print("=" * 50)
        
        # Function conflicts
        if self.conflicts.get('functions'):
            print(f"\n⚠️ FUNCTION CONFLICTS ({len(self.conflicts['functions'])})")
            for func_name, files in self.conflicts['functions'].items():
                print(f"\n🔴 Function '{func_name}' found in:")
                for file in files:
                    print(f"   • {file}")
        
        # Class conflicts  
        if self.conflicts.get('classes'):
            print(f"\n⚠️ CLASS CONFLICTS ({len(self.conflicts['classes'])})")
            for class_name, files in self.conflicts['classes'].items():
                print(f"\n🔴 Class '{class_name}' found in:")
                for file in files:
                    print(f"   • {file}")
        
        # Duplicate files
        if self.duplicate_files:
            print(f"\n⚠️ DUPLICATE FILES ({len(self.duplicate_files)})")
            for file1, file2 in self.duplicate_files:
                print(f"\n🔴 Duplicate files:")
                print(f"   • {file1}")
                print(f"   • {file2}")
    
    def generate_fixes(self):
        """Generate recommended fixes"""
        print("\n🔧 RECOMMENDED FIXES")
        print("=" * 50)
        
        # CAD Tools fix
        if any('cad_tools' in str(f) for f in self.duplicate_files):
            print("\n1. CAD TOOLS CONFLICT:")
            print("   Keep: ui/cad_tools_panel.py (most complete)")
            print("   Remove: ui/cad_tools.py")
            print("   Remove: Built-in CAD in main_window.py")
        
        # Project Manager fix
        if any('project_manager' in str(f) for f in self.duplicate_files):
            print("\n2. PROJECT MANAGER CONFLICT:")
            print("   Keep: core/project_manager.py (proper location)")
            print("   Remove: project_manager.py (root level)")
        
        # Component conflicts
        if any('motorola_68000' in str(f) for f in self.duplicate_files):
            print("\n3. COMPONENT CONFLICTS:")
            print("   Keep: components/amiga/motorola_68000_a500.py (system-specific)")
            print("   Remove: components/cpu/motorola_68000.py (generic)")
        
        # Import fixes
        print("\n4. IMPORT FIXES NEEDED:")
        print("   Update imports to use single source for each component")
        print("   Use absolute imports: from ui.cad_tools_panel import CADToolsPanel")
        
    def create_cleanup_script(self):
        """Create script to automatically fix conflicts"""
        script_content = '''#!/bin/bash
# Auto-generated conflict cleanup script
# Review before running!

echo "🧹 Visual Retro Emulator Conflict Cleanup"
echo "========================================="
echo "This will remove duplicate files. Press Ctrl+C to cancel."
read -p "Continue? (y/N): " confirm

if [[ $confirm != [yY] ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Backup files before removal
mkdir -p cleanup_backup
'''
        
        # Add file removals
        files_to_remove = [
            'ui/cad_tools.py',  # Keep cad_tools_panel.py
            'project_manager.py',  # Keep core/project_manager.py
            'components/cpu/motorola_68000.py',  # Keep Amiga version
        ]
        
        for file in files_to_remove:
            script_content += f'''
if [ -f "{file}" ]; then
    echo "📦 Backing up {file}"
    cp "{file}" cleanup_backup/
    echo "🗑️  Removing {file}"
    rm "{file}"
fi'''
        
        script_content += '''

echo "✅ Cleanup complete!"
echo "📦 Backups saved in cleanup_backup/"
echo "🔧 Now update your imports to use single sources"
'''
        
        with open('cleanup_conflicts.sh', 'w') as f:
            f.write(script_content)
        
        os.chmod('cleanup_conflicts.sh', 0o755)
        print("\n📝 Created cleanup_conflicts.sh script")

def main():
    """Main conflict resolution process"""
    print("🎯 Visual Retro Emulator - Conflict Resolver")
    print("=" * 50)
    
    resolver = ConflictResolver()
    conflicts = resolver.scan_project()
    
    if not conflicts.get('functions') and not conflicts.get('classes') and not resolver.duplicate_files:
        print("✅ No conflicts found! Your project is clean.")
        return
    
    # Show conflicts
    resolver.print_conflicts()
    
    # Show fixes
    resolver.generate_fixes()
    
    # Create cleanup script
    resolver.create_cleanup_script()
    
    print(f"\n📊 SUMMARY:")
    print(f"   Functions: {len(conflicts.get('functions', {}))}")
    print(f"   Classes: {len(conflicts.get('classes', {}))}")
    print(f"   Duplicates: {len(resolver.duplicate_files)}")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Review the conflicts above")
    print(f"2. Run './cleanup_conflicts.sh' to auto-fix")
    print(f"3. Update imports in your code")
    print(f"4. Test the application")

if __name__ == "__main__":
    main()