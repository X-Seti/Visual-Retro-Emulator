#!/usr/bin/env python3
"""
Project Cleanup Script
X-Seti - May21 2025 - Identifies and optionally removes unnecessary files from the retro emulator project

No longer Needed.
"""

import os
import shutil
from pathlib import Path


class ProjectCleaner:
    """Identifies and removes unnecessary files"""
    
    def __init__(self):
        self.to_remove = []
        self.to_keep = []
        self.duplicates = []
        self.empty_dirs = []
    
    def analyze_project(self):
        """Analyze the project and categorize files"""
        print("🔍 ANALYZING PROJECT FILES")
        print("=" * 40)
        
        self._find_duplicates()
        self._find_unnecessary_files()
        self._find_empty_directories()
        self._categorize_files()
    
    def _find_duplicates(self):
        """Find duplicate component files"""
        print("\n📁 Checking for duplicate components...")
        
        # MC68000 duplicates
        mc68000_files = [
            "components/cpu/motorola_68000.py",
            "components/cpu/motorola_68000_enhanced.py",
            "components/amiga/motorola_68000_a500.py"
        ]
        
        existing_mc68000 = [f for f in mc68000_files if os.path.exists(f)]
        if len(existing_mc68000) > 1:
            print(f"⚠️  Multiple MC68000 files found:")
            for f in existing_mc68000:
                print(f"    {f}")
            # Keep the Amiga version, remove others
            for f in existing_mc68000:
                if f != "components/amiga/motorola_68000_a500.py":
                    self.duplicates.append(f)
        
        # Other duplicates
        duplicate_patterns = [
            ("components/amiga/amiga_agnus.py", "components/amiga/amiga_agnus_8372a.py"),
            ("components/amiga/amiga_denise.py", "components/amiga/amiga_denise_8373.py"),
            ("components/amiga/amiga_paula.py", "components/amiga/amiga_paula_8364.py"),
            ("components/amiga/paula_8364.py", "components/amiga/amiga_paula_8364.py")
        ]
        
        for old_file, new_file in duplicate_patterns:
            if os.path.exists(old_file) and os.path.exists(new_file):
                print(f"⚠️  Duplicate found: {old_file} vs {new_file}")
                self.duplicates.append(old_file)  # Remove the older version
    
    def _find_unnecessary_files(self):
        """Find files that are no longer needed"""
        print("\n🗑️  Identifying unnecessary files...")
        
        # Old/test scripts that are no longer needed
        unnecessary_files = [
            "amiga_500_plus_chips.py",  # Original generator (we have the fixed version)
            "fix_chip_pins.py",  # Old pin fixer (we have enhanced version)
            "sample_components.py",  # Test file
            "prototype_code.py",  # Prototype/test code
            "verify_component_library.py",  # Test script
            "component_info.py",  # Seems unused
            "component_info_dialog.py",  # Seems unused
            "component_image_viewer.py",  # Seems unused
            "image_integration.py",  # Old integration script
            "image_integration_script.py",  # Old integration script
            "integration_component_loader.py",  # Old integration
            "integration_main.py",  # Old integration
            "final_integrated_app.py",  # Old version
            "main_app.py.backup",  # Backup file
            "retro_chip_generator.py",  # Old generator
            "setup_components_db.sh",  # Setup script no longer needed
            "vertical_text_chip_fix.py",  # Test script
        ]
        
        for file in unnecessary_files:
            if os.path.exists(file):
                self.to_remove.append(file)
        
        # Image files that might be unused
        unused_images = [
            "images/cpu_6502_dip_40.png",  # Duplicate
            "images/cpu_6502_qfp_44.png",  # Duplicate  
            "images/cpu_68000_dip_64.png",  # Duplicate
            "images/cpu_68000_pga_68.png",  # Duplicate
            "images/cpu_68000_qfp_68.png",  # Duplicate
            "images/cpu_z80_dip_40.png",   # Duplicate
            "images/cpu_z80_plcc_44.png",  # Duplicate
            "images/cpu_z80_qfp_44.png",   # Duplicate
        ]
        
        for img in unused_images:
            if os.path.exists(img):
                self.to_remove.append(img)
    
    def _find_empty_directories(self):
        """Find empty component directories"""
        print("\n📂 Checking for empty directories...")
        
        component_dirs = [
            "components/amstrad",
            "components/apple", 
            "components/arcade",
            "components/atari",
            "components/bbc",
            "components/dragon",
            "components/msx",
            "components/nintendo",
            "components/oric",
            "components/sega",
            "components/ti"
        ]
        
        for dir_path in component_dirs:
            if os.path.exists(dir_path):
                contents = [f for f in os.listdir(dir_path) if f != "README.md" and f != "__pycache__"]
                if not contents:
                    print(f"📂 Empty directory: {dir_path}")
                    self.empty_dirs.append(dir_path)
    
    def _categorize_files(self):
        """Categorize essential vs non-essential files"""
        print("\n📋 Categorizing files...")
        
        # Essential files that must be kept
        essential_files = [
            "main_app.py",
            "rendering.py", 
            "component_library.py",
            "retro_component_database.py",
            "connection_system.py",
            "project_manager.py",
            "property_dialog.py",
            "enhanced_pin_fixer.py",
            "realistic_chip_renderer.py"
        ]
        
        # Enhanced/new files to keep
        enhanced_files = [
            "enhanced_chip_renderer.py",
            "debug_chip_issues.py",
            "amiga_500_plus_chips_fixed.py",
            "enhanced_chip_renderer_vertical.py",
            "enhanced_main_app_hotkeys.py"
        ]
        
        self.to_keep.extend(essential_files + enhanced_files)
    
    def show_analysis(self):
        """Show the analysis results"""
        print(f"\n📊 CLEANUP ANALYSIS RESULTS")
        print("=" * 40)
        
        print(f"🗑️  Files to remove: {len(self.to_remove)}")
        for f in sorted(self.to_remove):
            print(f"    {f}")
        
        print(f"\n🔄 Duplicate files: {len(self.duplicates)}")
        for f in sorted(self.duplicates):
            print(f"    {f}")
        
        print(f"\n📂 Empty directories: {len(self.empty_dirs)}")
        for d in sorted(self.empty_dirs):
            print(f"    {d}")
        
        total_removable = len(self.to_remove) + len(self.duplicates) + len(self.empty_dirs)
        print(f"\n📈 Total items that can be removed: {total_removable}")
        
        return total_removable
    
    def create_removal_script(self):
        """Create a script to safely remove files"""
        script_content = '''#!/bin/bash
# Auto-generated cleanup script
# Review before running!

echo "🧹 Retro Emulator Project Cleanup"
echo "================================="
echo "This will remove unnecessary files. Press Ctrl+C to cancel."
read -p "Continue? (y/N): " confirm

if [[ $confirm != [yY] ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Create backup directory
mkdir -p cleanup_backup
echo "📦 Creating backup in cleanup_backup/"

'''
        
        # Add file removals
        for file in self.to_remove + self.duplicates:
            script_content += f'# Remove {file}\n'
            script_content += f'if [ -f "{file}" ]; then\n'
            script_content += f'    cp "{file}" cleanup_backup/$(basename "{file}").backup\n'
            script_content += f'    rm "{file}"\n'
            script_content += f'    echo "✅ Removed {file}"\n'
            script_content += f'fi\n\n'
        
        # Add directory removals  
        for directory in self.empty_dirs:
            script_content += f'# Remove empty directory {directory}\n'
            script_content += f'if [ -d "{directory}" ] && [ -z "$(ls -A "{directory}" 2>/dev/null | grep -v README.md)" ]; then\n'
            script_content += f'    rmdir "{directory}" 2>/dev/null || true\n'
            script_content += f'    echo "✅ Removed empty directory {directory}"\n'
            script_content += f'fi\n\n'
        
        script_content += '''
# Remove Python cache files
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
echo "✅ Removed Python cache files"

echo "🎉 Cleanup complete!"
echo "📦 Backups saved in cleanup_backup/"
'''
        
        with open("cleanup_project.sh", "w") as f:
            f.write(script_content)
        
        os.chmod("cleanup_project.sh", 0o755)
        print("📝 Created cleanup_project.sh script")
    
    def safe_remove_files(self, confirm=True):
        """Safely remove files with confirmation"""
        if confirm:
            print(f"\n⚠️  About to remove {len(self.to_remove + self.duplicates)} files")
            response = input("Continue? (y/N): ")
            if response.lower() != 'y':
                print("Cleanup cancelled.")
                return False
        
        # Create backup directory
        backup_dir = "cleanup_backup"
        os.makedirs(backup_dir, exist_ok=True)
        
        removed_count = 0
        
        # Remove files
        for file_path in self.to_remove + self.duplicates:
            if os.path.exists(file_path):
                try:
                    # Backup first
                    backup_name = f"{os.path.basename(file_path)}.backup"
                    shutil.copy2(file_path, os.path.join(backup_dir, backup_name))
                    
                    # Remove original
                    os.remove(file_path)
                    print(f"✅ Removed: {file_path}")
                    removed_count += 1
                    
                except Exception as e:
                    print(f"❌ Failed to remove {file_path}: {e}")
        
        # Remove empty directories
        for dir_path in self.empty_dirs:
            if os.path.exists(dir_path):
                try:
                    # Only remove if truly empty (except README.md)
                    contents = [f for f in os.listdir(dir_path) if f not in ["README.md", "__pycache__"]]
                    if not contents:
                        # Keep README.md but remove directory structure isn't needed
                        print(f"⚠️  Keeping {dir_path} (has README.md)")
                except Exception as e:
                    print(f"❌ Error checking {dir_path}: {e}")
        
        print(f"\n🎉 Cleanup complete! Removed {removed_count} files")
        print(f"📦 Backups saved in {backup_dir}/")
        
        return True


def main():
    """Main cleanup function"""
    print("🧹 RETRO EMULATOR PROJECT CLEANUP")
    print("=" * 50)
    print("This tool will identify unnecessary files in your project.")
    print()
    
    cleaner = ProjectCleaner()
    cleaner.analyze_project()
    
    total_removable = cleaner.show_analysis()
    
    if total_removable == 0:
        print("✅ Project is already clean!")
        return 0
    
    print(f"\n💾 Estimated space that can be freed: ~{total_removable * 50}KB")
    print("\n🎯 Cleanup options:")
    print("1. Create cleanup script (safe)")
    print("2. Remove files now (with backup)")
    print("3. Just show analysis (no changes)")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        cleaner.create_removal_script()
        print("\n✅ Created cleanup_project.sh")
        print("Review the script, then run: ./cleanup_project.sh")
        
    elif choice == "2":
        cleaner.safe_remove_files()
        
    elif choice == "3":
        print("✅ Analysis complete, no changes made.")
        
    else:
        print("Invalid option. No changes made.")
    
    return 0


if __name__ == "__main__":
    exit(main())
