#!/usr/bin/env python3
"""
Quick test for chipsets integration
"""

from PyQt6.QtWidgets import QApplication
import sys

def test_chipsets():
    app = QApplication(sys.argv)
    
    # Test the component palette
    from ui.component_palette import ComponentPalette
    
    palette = ComponentPalette()
    palette.show()
    
    print("🧪 Chipsets Test Results:")
    print(f"   📦 Total components: {palette.get_total_components()}")
    print(f"   🖥️  Systems: {len(palette.palette.get_available_systems())}")
    print(f"   📂 Categories: {len(palette.palette.get_available_categories())}")
    
    # Test specific chip lookup
    z80_component = palette.get_component_by_id("z80")
    if z80_component:
        print(f"   ✅ Z80 found: {z80_component['name']}")
        if z80_component['has_image']:
            print(f"      🖼️  Has realistic image")
        else:
            print(f"      ⚠️  Using fallback rendering")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_chipsets()
    