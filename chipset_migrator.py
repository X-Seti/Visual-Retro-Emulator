#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Chipset Migrator
Replaces old components with better-designed chipsets from chipsets/ folder
"""

#this belongs in chipset_migrator.py

import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import importlib.util

class ChipsetMigrator:
    """
    Migrates from old components/ to new chipsets/ 
    The chipsets/ folder has much better designed chips
    """
    
    def __init__(self):
        self.chipsets_dir = Path("chipsets")
        self.components_dir = Path("components")
        self.chip_registry = {}
        self.system_chips = {}
        
        print("🔄 ChipsetMigrator - Replacing old components with better chipsets")
        
    def load_all_chipsets(self):
        """Load all chipset definitions from chipsets/ folder"""
        print("📦 Loading better chipset designs...")
        
        if not self.chipsets_dir.exists():
            print(f"❌ Chipsets directory not found: {self.chipsets_dir}")
            return
        
        # Find all chipset files
        chipset_files = list(self.chipsets_dir.glob("chipset_*_chips.py"))
        
        if not chipset_files:
            print("⚠️ No chipset files found in chipsets/ directory")
            return
        
        for chipset_file in chipset_files:
            try:
                system_name = self._load_chipset_file(chipset_file)
                print(f"  ✅ Loaded {system_name} chipset")
            except Exception as e:
                print(f"  ⚠️ Error loading {chipset_file.name}: {e}")
        
        print(f"📊 Total chips loaded: {len(self.chip_registry)}")
        print(f"🖥️ Systems supported: {len(self.system_chips)}")
        
    def _load_chipset_file(self, chipset_path: Path) -> str:
        """Load a single chipset file"""
        # Extract system name from filename
        system_name = chipset_path.stem.replace("chipset_", "").replace("_chips", "")
        
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(chipset_path.stem, chipset_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Create a mock generator to capture chip definitions
            mock_generator = MockChipGenerator()
            
            # Call the add_chips function
            add_function_name = f"add_{system_name}_chips"
            if hasattr(module, add_function_name):
                getattr(module, add_function_name)(mock_generator)
            else:
                print(f"  ⚠️ No {add_function_name} function found in {chipset_path.name}")
                return system_name
            
            # Store the chips for this system
            self.system_chips[system_name] = mock_generator.chips
            
            # Add to global registry
            for chip in mock_generator.chips:
                self.chip_registry[chip['chip_id']] = chip
                # Also register by name for easier lookup
                self.chip_registry[chip['name'].lower()] = chip
            
            return system_name.replace("_", " ").title()
            
        except Exception as e:
            print(f"  ❌ Error processing {chipset_path.name}: {e}")
            return system_name
    
    def get_chip_definition(self, chip_name: str) -> Dict[str, Any]:
        """Get a chip definition by name or ID"""
        # Try exact match first
        if chip_name in self.chip_registry:
            return self.chip_registry[chip_name]
        
        # Try lowercase match
        if chip_name.lower() in self.chip_registry:
            return self.chip_registry[chip_name.lower()]
        
        # Try partial matches
        for key, chip in self.chip_registry.items():
            if chip_name.lower() in key.lower() or chip_name.lower() in chip['name'].lower():
                return chip
        
        return None
    
    def get_system_chips(self, system_name: str) -> List[Dict[str, Any]]:
        """Get all chips for a specific system"""
        return self.system_chips.get(system_name, [])
    
    def get_all_systems(self) -> List[str]:
        """Get list of all supported systems"""
        return list(self.system_chips.keys())
    
    def get_all_chips(self) -> List[Dict[str, Any]]:
        """Get all chip definitions"""
        all_chips = []
        for chips in self.system_chips.values():
            all_chips.extend(chips)
        return all_chips
    
    def get_chips_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get chips by category"""
        result = []
        for chip in self.get_all_chips():
            if chip.get('category', '').lower() == category.lower():
                result.append(chip)
        return result
    
    def create_component_library(self) -> Dict[str, Dict[str, Any]]:
        """Create a component library organized by category"""
        library = {
            "CPU": [],
            "Audio": [],
            "Video": [],
            "Custom": [],
            "Memory": [],
            "I/O": [],
            "Clock": []
        }
        
        for chip in self.get_all_chips():
            category = chip.get('category', 'Custom')
            if category in library:
                library[category].append(chip)
            else:
                library['Custom'].append(chip)
        
        return library
    
    def export_component_definitions(self, output_file: str = "migrated_components.py"):
        """Export all chip definitions to a single file"""
        print(f"📄 Exporting component definitions to {output_file}")
        
        with open(output_file, 'w') as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('"""\n')
            f.write('X-Seti - June22 2025 - Migrated Component Definitions\n')
            f.write('Generated from better chipsets/ folder designs\n')
            f.write('"""\n\n')
            
            f.write('# Component library organized by system\n')
            f.write('COMPONENT_LIBRARY = {\n')
            
            for system_name, chips in self.system_chips.items():
                f.write(f'    "{system_name}": [\n')
                for chip in chips:
                    f.write(f'        {{\n')
                    f.write(f'            "name": "{chip["name"]}",\n')
                    f.write(f'            "chip_id": "{chip["chip_id"]}",\n')
                    f.write(f'            "category": "{chip["category"]}",\n')
                    f.write(f'            "description": "{chip["description"]}",\n')
                    f.write(f'            "package_types": {chip["package_types"]},\n')
                    f.write(f'            "pins": {chip["pins"]}\n')
                    f.write(f'        }},\n')
                f.write(f'    ],\n')
            
            f.write('}\n\n')
            
            # Add helper functions
            f.write('def get_chip_by_name(name: str):\n')
            f.write('    """Get chip definition by name"""\n')
            f.write('    for chips in COMPONENT_LIBRARY.values():\n')
            f.write('        for chip in chips:\n')
            f.write('            if chip["name"].lower() == name.lower():\n')
            f.write('                return chip\n')
            f.write('    return None\n\n')
            
            f.write('def get_chips_by_category(category: str):\n')
            f.write('    """Get all chips in a category"""\n')
            f.write('    result = []\n')
            f.write('    for chips in COMPONENT_LIBRARY.values():\n')
            f.write('        for chip in chips:\n')
            f.write('            if chip["category"].lower() == category.lower():\n')
            f.write('                result.append(chip)\n')
            f.write('    return result\n\n')
            
            f.write('def get_all_chips():\n')
            f.write('    """Get all chip definitions"""\n')
            f.write('    result = []\n')
            f.write('    for chips in COMPONENT_LIBRARY.values():\n')
            f.write('        result.extend(chips)\n')
            f.write('    return result\n')
        
        print(f"✅ Exported {len(self.get_all_chips())} chip definitions")
    
    def show_comparison(self):
        """Show comparison between old and new components"""
        print("\n📊 COMPARISON: Old vs New Components")
        print("=" * 60)
        
        # Count old components
        old_components = []
        if self.components_dir.exists():
            for root, dirs, files in os.walk(self.components_dir):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        old_components.append(file)
        
        print(f"📁 Old components/ folder: {len(old_components)} files")
        print(f"📦 New chipsets/ folder: {len(self.get_all_chips())} chips")
        print(f"🖥️ Systems supported: {len(self.system_chips)}")
        
        print("\n🎯 New Chipsets by System:")
        for system_name, chips in self.system_chips.items():
            chip_names = [chip['name'] for chip in chips[:3]]  # Show first 3
            more = f" (+{len(chips)-3} more)" if len(chips) > 3 else ""
            print(f"  • {system_name.replace('_', ' ').title()}: {', '.join(chip_names)}{more}")
        
        print(f"\n✨ Benefits of New Chipsets:")
        print(f"  • Accurate pin definitions")
        print(f"  • Proper chip names and IDs")
        print(f"  • Multiple package types")
        print(f"  • Better categorization")
        print(f"  • Complete system coverage")


class MockChipGenerator:
    """Mock generator to capture chip definitions from chipset files"""
    
    def __init__(self):
        self.chips = []
    
    def add_chip(self, name, chip_id, category, description, package_types, pins=None):
        """Capture chip definition"""
        self.chips.append({
            'name': name,
            'chip_id': chip_id,
            'category': category,
            'description': description,
            'package_types': package_types,
            'pins': pins or []
        })


def main():
    """Main migration function"""
    print("🚀 CHIPSET MIGRATION TOOL")
    print("=" * 60)
    print("Replacing old components with better chipsets designs")
    
    migrator = ChipsetMigrator()
    
    # Load all chipsets
    migrator.load_all_chipsets()
    
    if migrator.get_all_chips():
        # Show comparison
        migrator.show_comparison()
        
        # Export component definitions
        migrator.export_component_definitions()
        
        # Show some examples
        print("\n🔍 Example Chip Lookups:")
        
        examples = ["SID", "VIC-II", "Agnus", "Paula", "Z80", "6502"]
        for chip_name in examples:
            chip = migrator.get_chip_definition(chip_name)
            if chip:
                print(f"  ✅ {chip_name}: {chip['name']} ({chip['category']})")
            else:
                print(f"  ❌ {chip_name}: Not found")
        
        print("\n🎉 Migration Complete!")
        print("📄 Use migrated_components.py in your application")
        print("🔧 Better chipsets are now available for your Visual Retro Emulator")
    else:
        print("❌ No chips loaded - check chipsets/ directory")
        migrator = None
    
    return migrator


if __name__ == "__main__":
    migrator = main()
