"""
X-Seti - June07 2025 - Chip Image Loader
Connects retro_chip_generator images with canvas display
"""

import os
from pathlib import Path
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ChipImageLoader:
    """Enhanced loader for chip images"""
    
    def __init__(self):
        self.images_dir = Path("images/components")
        self.image_cache = {}
        self.load_image_mappings()
    
    def load_image_mappings(self):
        """Load mappings from component names to image files"""
        self.mappings = {
            # CPU mappings
            "6502": "cpu_6502_dip_40.png",
            "65c02": "cpu_6502_dip_40.png",
            "68000": "cpu_68000_dip_64.png",
            "mc68000": "cpu_68000_dip_64.png",
            "z80": "cpu_z80_dip_40.png",
            "zilog z80": "cpu_z80_dip_40.png",
            
            # Commodore 64 chips
            "vic-ii": "c64_vic2_dip_40.png",
            "vic2": "c64_vic2_dip_40.png",
            "6569": "c64_vic2_dip_40.png",
            "sid": "c64_sid_dip_28.png",
            "6581": "c64_sid_dip_28.png",
            "8580": "c64_sid_dip_28.png",
            "cia": "c64_cia_dip_40.png",
            "6526": "c64_cia_dip_40.png",
            
            # Amiga chips
            "agnus": "amiga_agnus_plcc_84.png",
            "8370": "amiga_agnus_plcc_84.png",
            "8371": "amiga_agnus_plcc_84.png",
            "denise": "amiga_denise_plcc_48.png",
            "8362": "amiga_denise_plcc_48.png",
            "paula": "amiga_paula_dip_48.png",
            "8364": "amiga_paula_dip_48.png",
            
            # ZX Spectrum
            "ula": "spectrum_ula_dip_40.png",
            "zx spectrum ula": "spectrum_ula_dip_40.png",
            
            # Nintendo NES
            "ppu": "nes_ppu_dip_40.png",
            "2c02": "nes_ppu_dip_40.png",
            "apu": "nes_apu_dip_40.png",
            "2a03": "nes_apu_dip_40.png",
            
            # BBC Micro
            "video ula": "bbc_video_ula_dip_40.png",
            "sn76489": "bbc_sn76489_dip_16.png",
            
            # Sega Genesis
            "genesis vdp": "genesis_vdp_qfp_64.png",
            "ym2612": "genesis_ym2612_dip_24.png",
            
            # MSX
            "tms9918a": "msx_tms9918a_dip_40.png",
            "ay-3-8910": "msx_ay3_8910_dip_28.png",
            "s1985": "msx_s1985_dip_64.png",
            
            # TI-99/4A
            "tms9900": "ti99_tms9900_dip_64.png",
            "tms9901": "ti99_tms9901_dip_40.png",
            
            # Dragon/CoCo
            "sam": "dragon_sam_dip_40.png",
            "mc6883": "dragon_sam_dip_40.png",
            
            # Oric
            "oric ula": "oric_ula_dip_40.png",
        }
    
    def find_chip_image(self, component_name: str) -> str:
        """Find the best matching chip image for a component"""
        if not component_name:
            return None
        
        # Clean the component name
        clean_name = component_name.lower().strip()
        clean_name = clean_name.replace("-", " ").replace("_", " ").replace("  ", " ")
        
        print(f"🔍 Looking for image for: '{component_name}' -> '{clean_name}'")
        
        # Try exact mapping first
        if clean_name in self.mappings:
            image_file = self.mappings[clean_name]
            image_path = self.images_dir / image_file
            if image_path.exists():
                print(f"✅ Found exact match: {image_file}")
                return str(image_path)
        
        # Try partial matches
        for key, image_file in self.mappings.items():
            if key in clean_name or clean_name in key:
                image_path = self.images_dir / image_file
                if image_path.exists():
                    print(f"✅ Found partial match: {key} -> {image_file}")
                    return str(image_path)
        
        # Try scanning all files for similar names
        if self.images_dir.exists():
            for image_file in self.images_dir.glob("*.png"):
                file_name = image_file.stem.lower()
                # Remove package type suffixes for matching
                file_base = file_name.replace("_dip_40", "").replace("_dip_28", "").replace("_plcc_84", "")
                file_base = file_base.replace("_qfp_44", "").replace("_dip_64", "").replace("_dip_48", "")
                
                if clean_name in file_base or file_base in clean_name:
                    print(f"✅ Found file scan match: {file_base} -> {image_file.name}")
                    return str(image_file)
        
        print(f"❌ No image found for: {component_name}")
        return None
    
    def load_chip_image(self, component_name: str, target_width: int = 200, target_height: int = 150) -> QPixmap:
        """Load and scale a chip image"""
        # Check cache first
        cache_key = f"{component_name}_{target_width}_{target_height}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        # Find the image file
        image_path = self.find_chip_image(component_name)
        if not image_path:
            return QPixmap()  # Return null pixmap
        
        try:
            # Load the original image
            original_pixmap = QPixmap(image_path)
            if original_pixmap.isNull():
                print(f"⚠️ Failed to load pixmap from: {image_path}")
                return QPixmap()
            
            print(f"📏 Original size: {original_pixmap.width()}x{original_pixmap.height()}")
            
            # Scale with high quality
            scaled_pixmap = original_pixmap.scaled(
                target_width, target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            print(f"📏 Scaled to: {scaled_pixmap.width()}x{scaled_pixmap.height()}")
            
            # Cache the result
            self.image_cache[cache_key] = scaled_pixmap
            
            return scaled_pixmap
            
        except Exception as e:
            print(f"⚠️ Error loading image {image_path}: {e}")
            return QPixmap()
    
    def get_available_chips(self):
        """Get list of available chip images"""
        if not self.images_dir.exists():
            return []
        
        chips = []
        for image_file in self.images_dir.glob("*.png"):
            chips.append(image_file.stem)
        
        return sorted(chips)

# Global instance
chip_image_loader = ChipImageLoader()
