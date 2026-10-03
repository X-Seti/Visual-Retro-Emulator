#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Chipset Integration
Integrates migrated chipsets with chip_image_loader and component palette
"""

#this belongs in chipset_integration.py

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Import the migrator
from chipset_migrator import ChipsetMigrator

class IntegratedChipsetManager:
    """
    Integrates the better chipsets with existing image loader and component systems
    """
    
    def __init__(self):
        # Load the migrated chipsets
        self.migrator = ChipsetMigrator()
        self.migrator.load_all_chipsets()
        
        # Enhanced image mappings for better chipsets
        self.enhanced_image_mappings = self._create_enhanced_mappings()
        
        # Image cache
        self.image_cache = {}
        
        # Image directories
        self.image_dirs = [
            Path("images/components"),
            Path("images"),
            Path("../images/components"),
            Path("../images")
        ]
        
        print("🔗 IntegratedChipsetManager initialized")
        print(f"📦 Loaded {len(self.migrator.get_all_chips())} chips from {len(self.migrator.get_all_systems())} systems")
    
    def _create_enhanced_mappings(self) -> Dict[str, str]:
        """Create enhanced image mappings for the new chipsets"""
        mappings = {}
        
        # Only create mappings if we have chips loaded
        if not self.migrator.get_all_chips():
            print("⚠️ No chips loaded for creating mappings")
            return mappings
        
        # Amiga chips - using existing images
        amiga_chips = self.migrator.get_system_chips("amiga")
        for chip in amiga_chips:
            chip_name = chip['name'].lower()
            chip_id = chip['chip_id'].lower()
            
            if "agnus" in chip_name:
                mappings[chip_id] = "amiga_agnus_plcc_84.png"
                mappings[chip_name] = "amiga_agnus_plcc_84.png"
            elif "paula" in chip_name:
                mappings[chip_id] = "amiga_paula_dip_48.png"
                mappings[chip_name] = "amiga_paula_dip_48.png"
            elif "denise" in chip_name:
                mappings[chip_id] = "amiga_denise_plcc_48.png"
                mappings[chip_name] = "amiga_denise_plcc_48.png"
            elif "gary" in chip_name:
                mappings[chip_id] = "amiga_gary_plcc_68.png"
                mappings[chip_name] = "amiga_gary_plcc_68.png"
            elif "alice" in chip_name:
                mappings[chip_id] = "amiga_alice_plcc_84.png"
                mappings[chip_name] = "amiga_alice_plcc_84.png"
            elif "lisa" in chip_name:
                mappings[chip_id] = "amiga_lisa_plcc_68.png"
                mappings[chip_name] = "amiga_lisa_plcc_68.png"
            elif "ramsey" in chip_name:
                mappings[chip_id] = "amiga_ramsey_plcc_68.png"
                mappings[chip_name] = "amiga_ramsey_plcc_68.png"
            elif "buster" in chip_name:
                mappings[chip_id] = "amiga_buster_plcc_52.png"
                mappings[chip_name] = "amiga_buster_plcc_52.png"
        
        # C64 chips
        c64_chips = self.migrator.get_system_chips("c64")
        for chip in c64_chips:
            chip_name = chip['name'].lower()
            chip_id = chip['chip_id'].lower()
            
            if "sid" in chip_name:
                mappings[chip_id] = "c64_sid_dip_28.png"
                mappings[chip_name] = "c64_sid_dip_28.png"
            elif "vic" in chip_name or "6569" in chip_name or "6567" in chip_name:
                mappings[chip_id] = "c64_vic2_dip_40.png"
                mappings[chip_name] = "c64_vic2_dip_40.png"
        
        # CPU chips
        all_chips = self.migrator.get_all_chips()
        for chip in all_chips:
            chip_name = chip['name'].lower()
            chip_id = chip['chip_id'].lower()
            category = chip.get('category', '').lower()
            
            if category in ['cpu', 'processor'] or 'cpu' in chip_name:
                if "z80" in chip_name:
                    mappings[chip_id] = "cpu_z80_dip_40.png"
                    mappings[chip_name] = "cpu_z80_dip_40.png"
                elif "6502" in chip_name:
                    mappings[chip_id] = "cpu_6502_dip_40.png"
                    mappings[chip_name] = "cpu_6502_dip_40.png"
                elif "68000" in chip_name:
                    mappings[chip_id] = "cpu_68000_dip_64.png"
                    mappings[chip_name] = "cpu_68000_dip_64.png"
        
        print(f"🗺️ Created {len(mappings)} enhanced image mappings")
        return mappings
    
    def get_chips_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get chips by category from migrated chipsets"""
        return self.migrator.get_chips_by_category(category)
    
    def find_chip_image(self, chip_name_or_id: str, package_type: str = None) -> Optional[Path]:
        """Find chip image using enhanced mappings"""
        search_key = chip_name_or_id.lower()
        
        # Try enhanced mappings first
        if search_key in self.enhanced_image_mappings:
            image_name = self.enhanced_image_mappings[search_key]
            
            # Search in image directories
            for image_dir in self.image_dirs:
                if image_dir.exists():
                    image_path = image_dir / image_name
                    if image_path.exists():
                        return image_path
        
        # Fallback to pattern matching
        patterns = [
            f"{search_key.replace(' ', '_')}_{package_type.lower().replace('-', '_')}.png" if package_type else None,
            f"{search_key.replace(' ', '_')}_dip_40.png",
            f"{search_key.replace(' ', '_')}_plcc_84.png",
            f"{search_key.replace(' ', '_')}_qfp_44.png",
            f"cpu_{search_key.replace(' ', '_')}_dip_40.png",
            f"{search_key.replace(' ', '_')}.png"
        ]
        
        for image_dir in self.image_dirs:
            if not image_dir.exists():
                continue
                
            for pattern in patterns:
                if pattern:
                    image_path = image_dir / pattern
                    if image_path.exists():
                        return image_path
        
        return None
    
    def load_chip_image(self, chip_name_or_id: str, package_type: str = None, 
                       target_size: tuple = (120, 80)) -> Optional[QPixmap]:
        """Load chip image with caching"""
        cache_key = f"{chip_name_or_id}_{package_type}_{target_size[0]}x{target_size[1]}"
        
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        image_path = self.find_chip_image(chip_name_or_id, package_type)
        
        if image_path:
            try:
                original_pixmap = QPixmap(str(image_path))
                if not original_pixmap.isNull():
                    # Scale to target size
                    scaled_pixmap = original_pixmap.scaled(
                        target_size[0], target_size[1],
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    
                    self.image_cache[cache_key] = scaled_pixmap
                    print(f"✅ Loaded chip image: {image_path.name}")
                    return scaled_pixmap
            except Exception as e:
                print(f"⚠️ Error loading image {image_path}: {e}")
        
        return None
    
    def get_component_library_for_palette(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get organized component library for the component palette"""
        library = {
            "CPU": [],
            "Video": [],
            "Audio": [],
            "Memory": [],
            "Custom": [],
            "I/O": [],
            "Clock": []
        }
        
        # Organize chips by category
        all_chips = self.migrator.get_all_chips()
        for chip in all_chips:
            category = chip.get('category', 'Custom')
            
            # Map some categories
            if category.lower() in ['processor', 'cpu']:
                category = 'CPU'
            elif category.lower() in ['graphics', 'video']:
                category = 'Video'
            elif category.lower() in ['sound', 'audio']:
                category = 'Audio'
            
            if category in library:
                library[category].append(chip)
            else:
                library['Custom'].append(chip)
        
        return library
    
    def get_systems_library(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get library organized by computer systems"""
        systems_lib = {}
        
        for system_name, chips in self.migrator.system_chips.items():
            display_name = system_name.replace('_', ' ').title()
            systems_lib[display_name] = chips
        
        return systems_lib
    
    def create_enhanced_component_palette_data(self) -> Dict[str, Any]:
        """Create enhanced data structure for component palette"""
        return {
            "by_category": self.get_component_library_for_palette(),
            "by_system": self.get_systems_library(),
            "total_chips": len(self.migrator.get_all_chips()),
            "total_systems": len(self.migrator.get_all_systems()),
            "image_mappings": self.enhanced_image_mappings
        }


class ChipsetComponentFactory:
    """Factory for creating components from chipset definitions"""
    
    def __init__(self, chipset_manager: IntegratedChipsetManager):
        self.chipset_manager = chipset_manager
    
    def create_component(self, chip_def: Dict[str, Any], package_type: str = None) -> Dict[str, Any]:
        """Create a component from chipset definition"""
        # Use the first package type if none specified
        if not package_type and chip_def.get('package_types'):
            package_type = chip_def['package_types'][0]
        
        # Load the image
        chip_image = self.chipset_manager.load_chip_image(
            chip_def['chip_id'], 
            package_type
        )
        
        # Create component data structure
        component = {
            'id': chip_def['chip_id'],
            'name': chip_def['name'],
            'category': chip_def['category'],
            'description': chip_def['description'],
            'package_type': package_type,
            'package_types': chip_def['package_types'],
            'pins': chip_def.get('pins', []),
            'pin_count': len(chip_def.get('pins', [])),
            'image': chip_image,
            'has_image': chip_image is not None,
            'properties': {
                'selectable_packages': chip_def['package_types'],
                'pin_definitions': chip_def.get('pins', [])
            }
        }
        
        return component
    
    def create_component_by_name(self, chip_name: str, package_type: str = None) -> Optional[Dict[str, Any]]:
        """Create component by chip name"""
        chip_def = self.chipset_manager.migrator.get_chip_definition(chip_name)
        if chip_def:
            return self.create_component(chip_def, package_type)
        return None


def integrate_with_existing_systems():
    """Integration function to update existing systems"""
    print("🔗 Integrating chipsets with existing systems...")
    
    # Create integrated manager
    manager = IntegratedChipsetManager()
    
    # Create factory
    factory = ChipsetComponentFactory(manager)
    
    # Get enhanced palette data
    palette_data = manager.create_enhanced_component_palette_data()
    
    print("✅ Integration complete!")
    print(f"📊 Available for component palette:")
    print(f"   • {palette_data['total_chips']} chips")
    print(f"   • {palette_data['total_systems']} systems") 
    print(f"   • {len(palette_data['by_category'])} categories")
    
    return manager, factory, palette_data


if __name__ == "__main__":
    manager, factory, palette_data = integrate_with_existing_systems()
