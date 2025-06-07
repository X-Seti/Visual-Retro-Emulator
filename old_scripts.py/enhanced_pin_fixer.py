#!/usr/bin/env python3
"""
Enhanced Pin Fixer with Realistic Chip Scaling
Fixes pin positions while accounting for proper DIP width scaling and historical chip sizes
"""

import os
import re
from pathlib import Path


class EnhancedChipPinFixer:
    """Enhanced pin fixer with realistic chip scaling"""
    
    def __init__(self):
        self.fixed_files = []
        self.error_files = []
        
        # Era-based scale factors
        self.era_scale_factors = {
            "1970-1975": 1.3,  # Early large chips
            "1975-1980": 1.2,
            "1980-1985": 1.1,
            "1985-1990": 1.0,  # Standard era
            "1990-1995": 0.9,
            "1995-2000": 0.8,
            "2000+": 0.7       # Modern small chips
        }
        
        # Realistic package dimensions (width, height) - base size
        self.package_dimensions = {
            "DIP-8": (120, 80),
            "DIP-14": (140, 100),
            "DIP-16": (140, 120),
            "DIP-18": (160, 120),
            "DIP-20": (160, 140),
            "DIP-22": (180, 140),
            "DIP-24": (180, 160),
            "DIP-28": (200, 180),
            "DIP-32": (220, 200),
            "DIP-40": (240, 260),
            "DIP-48": (300, 320),   # Wider for more pins
            "DIP-64": (360, 420),   # Much wider for 64 pins
            
            "QFP-32": (180, 180),
            "QFP-44": (200, 200),
            "QFP-48": (220, 220),
            "QFP-52": (240, 240),
            "QFP-64": (260, 260),
            "QFP-68": (280, 280),
            "QFP-84": (320, 320),
            "QFP-100": (360, 360),
            "QFP-132": (400, 400),
            
            "PLCC-20": (160, 160),
            "PLCC-28": (180, 180),
            "PLCC-32": (200, 200),
            "PLCC-44": (240, 240),
            "PLCC-52": (260, 260),
            "PLCC-68": (300, 300),
            "PLCC-84": (340, 340),
            
            "BGA-64": (200, 200),
            "BGA-100": (240, 240),
            "BGA-144": (280, 280),
            "BGA-256": (320, 320),
        }

    def get_era_from_year(self, year_str):
        """Extract era from year string or number"""
        if not year_str:
            return "1985-1990"  # Default
        
        try:
            year = int(str(year_str).strip('"\''))
        except (ValueError, TypeError):
            return "1985-1990"
        
        if year < 1975:
            return "1970-1975"
        elif year < 1980:
            return "1975-1980"
        elif year < 1985:
            return "1980-1985"
        elif year < 1990:
            return "1985-1990"
        elif year < 1995:
            return "1990-1995"
        elif year < 2000:
            return "1995-2000"
        else:
            return "2000+"

    def get_chip_dimensions(self, package_type, year=None, category=None):
        """Get realistic chip dimensions with era and complexity scaling"""
        # Get base dimensions
        base_width, base_height = self.package_dimensions.get(
            package_type, (200, 200)
        )
        
        # Apply era scaling
        if year:
            era = self.get_era_from_year(year)
            scale_factor = self.era_scale_factors.get(era, 1.0)
        else:
            scale_factor = 1.0
        
        # Apply category scaling
        complexity_scale = 1.0
        if category:
            category_lower = category.lower()
            if category_lower in ['cpu', 'mpu', 'processor']:
                complexity_scale = 1.2  # CPUs are larger
            elif category_lower in ['custom', 'asic', 'ula']:
                complexity_scale = 1.1  # Custom chips often larger
            elif category_lower in ['memory', 'ram', 'rom']:
                complexity_scale = 0.9  # Memory often more compact
        
        # Calculate final dimensions
        final_width = int(base_width * scale_factor * complexity_scale)
        final_height = int(base_height * scale_factor * complexity_scale)
        
        return final_width, final_height

    def calculate_pin_positions(self, package_type, pin_count, width, height):
        """Calculate realistic pin positions for different package types"""
        positions = []
        
        if package_type.startswith('DIP'):
            # DIP packages - dual in-line with proper spacing
            pins_per_side = pin_count // 2
            
            # Calculate pin spacing based on actual package height
            usable_height = height - 40  # Leave top/bottom margins
            pin_spacing = usable_height / (pins_per_side + 1) if pins_per_side > 0 else 20
            
            # Left side pins (1 to pins_per_side)
            for i in range(pins_per_side):
                x = 15  # Fixed margin from left edge
                y = 20 + (i + 1) * pin_spacing
                positions.append((int(x), int(y)))
            
            # Right side pins (pins_per_side + 1 to pin_count)
            for i in range(pins_per_side):
                x = width - 15  # Fixed margin from right edge  
                y = 20 + (pins_per_side - i) * pin_spacing  # Reverse order
                positions.append((int(x), int(y)))
        
        elif package_type.startswith('QFP'):
            # QFP packages - quad flat pack
            pins_per_side = pin_count // 4
            
            usable_width = width - 40
            usable_height = height - 40
            pin_spacing_x = usable_width / (pins_per_side + 1) if pins_per_side > 0 else 20
            pin_spacing_y = usable_height / (pins_per_side + 1) if pins_per_side > 0 else 20
            
            # Bottom side (1 to pins_per_side)
            for i in range(pins_per_side):
                x = 20 + (i + 1) * pin_spacing_x
                y = height - 10
                positions.append((int(x), int(y)))
            
            # Right side
            for i in range(pins_per_side):
                x = width - 10
                y = height - 20 - (i + 1) * pin_spacing_y
                positions.append((int(x), int(y)))
            
            # Top side 
            for i in range(pins_per_side):
                x = width - 20 - (i + 1) * pin_spacing_x
                y = 10
                positions.append((int(x), int(y)))
            
            # Left side
            for i in range(pins_per_side):
                x = 10
                y = 20 + (i + 1) * pin_spacing_y
                positions.append((int(x), int(y)))
        
        elif package_type.startswith('PLCC'):
            # PLCC packages - plastic leaded chip carrier
            pins_per_side = pin_count // 4
            
            usable_width = width - 30
            usable_height = height - 30
            pin_spacing_x = usable_width / (pins_per_side + 1) if pins_per_side > 0 else 15
            pin_spacing_y = usable_height / (pins_per_side + 1) if pins_per_side > 0 else 15
            
            # Bottom side
            for i in range(pins_per_side):
                x = 15 + (i + 1) * pin_spacing_x
                y = height - 8
                positions.append((int(x), int(y)))
            
            # Right side
            for i in range(pins_per_side):
                x = width - 8
                y = height - 15 - (i + 1) * pin_spacing_y
                positions.append((int(x), int(y)))
            
            # Top side
            for i in range(pins_per_side):
                x = width - 15 - (i + 1) * pin_spacing_x
                y = 8
                positions.append((int(x), int(y)))
            
            # Left side
            for i in range(pins_per_side):
                x = 8
                y = 15 + (i + 1) * pin_spacing_y
                positions.append((int(x), int(y)))
        
        else:
            # Default to DIP-style for unknown packages
            pins_per_side = pin_count // 2
            pin_spacing = (height - 40) / (pins_per_side + 1) if pins_per_side > 0 else 20
            
            for i in range(pins_per_side):
                x = 15
                y = 20 + (i + 1) * pin_spacing
                positions.append((int(x), int(y)))
            
            for i in range(pins_per_side):
                x = width - 15
                y = 20 + (pins_per_side - i) * pin_spacing
                positions.append((int(x), int(y)))
        
        return positions

    def get_pin_type(self, pin_name):
        """Determine pin type based on pin name"""
        pin_name_upper = pin_name.upper()
        
        if any(x in pin_name_upper for x in ['VCC', 'VDD', '+5V', '+3V', 'POWER']):
            return 'power'
        elif any(x in pin_name_upper for x in ['GND', 'VSS', 'GROUND']):
            return 'ground'
        elif any(x in pin_name_upper for x in ['CLK', 'CLOCK', 'OSC', 'XTAL']):
            return 'clock'
        elif pin_name_upper.startswith('A') and pin_name_upper[1:].isdigit():
            return 'address'
        elif pin_name_upper.startswith('D') and pin_name_upper[1:].isdigit():
            return 'data'
        elif any(x in pin_name_upper for x in ['CTRL', 'CS', 'RD', 'WR', 'R/W', 'RESET', 'IRQ', 'NMI']):
            return 'control'
        elif any(x in pin_name_upper for x in ['AUDIO', 'SOUND', 'AUD']):
            return 'audio'
        elif any(x in pin_name_upper for x in ['VIDEO', 'RGB', 'RED', 'GREEN', 'BLUE', 'SYNC']):
            return 'video'
        elif any(x in pin_name_upper for x in ['ANALOG', 'POT', 'AIN']):
            return 'analog'
        else:
            return 'io'

    def extract_chip_metadata(self, content):
        """Extract chip metadata from file content"""
        metadata = {}
        
        # Extract package type
        package_match = re.search(r'package_type.*?["\'](.*?)["\']', content)
        if package_match:
            metadata['package_type'] = package_match.group(1)
        
        # Extract year
        year_matches = [
            re.search(r'year.*?["\']*(\d{4})["\']*', content),
            re.search(r'["\']\d{4}["\']\s*#.*year', content, re.IGNORECASE),
            re.search(r'set_property\(["\']year["\'],\s*["\']?(\d{4})["\']?\)', content)
        ]
        
        for match in year_matches:
            if match:
                metadata['year'] = match.group(1)
                break
        
        # Extract category from component definition or file path
        category_match = re.search(r'ComponentDefinition\([^,]*,[^,]*,\s*["\'](.*?)["\']', content)
        if category_match:
            metadata['category'] = category_match.group(1)
        
        return metadata

    def fix_file(self, filepath):
        """Fix a single chip file with enhanced scaling"""
        try:
            print(f"  🔧 Fixing: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            metadata = self.extract_chip_metadata(content)
            
            package_type = metadata.get('package_type', 'DIP-40')
            year = metadata.get('year')
            category = metadata.get('category')
            
            # Count existing add_pin calls
            pin_matches = re.findall(r'comp\.add_pin\([^)]+\)', content)
            pin_count = len(pin_matches)
            
            if pin_count == 0:
                print(f"    ⚠️  No add_pin calls found in {filepath}")
                return False
            
            print(f"    📦 Package: {package_type}, Pins: {pin_count}")
            if year:
                era = self.get_era_from_year(year)
                print(f"    📅 Year: {year} (Era: {era})")
            
            # Get realistic chip dimensions
            width, height = self.get_chip_dimensions(package_type, year, category)
            print(f"    📏 Dimensions: {width}x{height} pixels")
            
            # Calculate pin positions with proper scaling
            pin_positions = self.calculate_pin_positions(package_type, pin_count, width, height)
            
            if len(pin_positions) != pin_count:
                print(f"    ⚠️  Pin position mismatch: expected {pin_count}, got {len(pin_positions)}")
                # Pad with default positions if needed
                while len(pin_positions) < pin_count:
                    pin_positions.append((15, 20 + len(pin_positions) * 15))
            
            # Replace add_pin calls with enhanced positioning
            def replace_add_pin(match, positions=pin_positions):
                old_call = match.group(0)
                
                # Extract existing arguments
                args_match = re.search(r'add_pin\((.*?)\)', old_call)
                if not args_match:
                    return old_call
                
                args = args_match.group(1).strip()
                
                # Find pin index
                pin_index = len([m.start() for m in re.finditer(r'comp\.add_pin\(', content[:match.start()])])
                
                if pin_index >= len(positions):
                    x, y = (15, 20 + pin_index * 15)  # Fallback
                else:
                    x, y = positions[pin_index]
                
                # Parse pin name from existing arguments
                if args.count(',') >= 1:
                    parts = [part.strip() for part in args.split(',')]
                    pin_name = parts[-1]
                else:
                    pin_name = args
                
                # Clean up pin name and determine type
                pin_name_clean = pin_name.strip('"\'')
                pin_type = self.get_pin_type(pin_name_clean)
                
                # Create new add_pin call
                new_call = f'comp.add_pin({pin_name}, {x}, {y}, "{pin_type}")'
                
                return new_call
            
            # Update component width/height if present
            width_match = re.search(r'width\s*=\s*\d+', content)
            if width_match:
                content = re.sub(r'width\s*=\s*\d+', f'width={width}', content)
            
            height_match = re.search(r'height\s*=\s*\d+', content)
            if height_match:
                content = re.sub(r'height\s*=\s*\d+', f'height={height}', content)
            
            # Replace all add_pin calls
            new_content = re.sub(r'comp\.add_pin\([^)]+\)', replace_add_pin, content)
            
            # Add era information as a comment if year is present
            if year and 'Era:' not in content:
                era = self.get_era_from_year(year)
                scale_factor = self.era_scale_factors.get(era, 1.0)
                era_comment = f'# Era: {era} (Scale: {scale_factor}x)\n'
                
                # Insert after the first docstring
                docstring_end = new_content.find('"""', new_content.find('"""') + 3)
                if docstring_end != -1:
                    new_content = (new_content[:docstring_end + 3] + '\n' + era_comment + 
                                 new_content[docstring_end + 3:])
            
            # Write the fixed content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"    ✅ Fixed {pin_count} pins with realistic {width}x{height} scaling")
            self.fixed_files.append(str(filepath))
            return True
            
        except Exception as e:
            print(f"    ❌ Error fixing {filepath}: {e}")
            self.error_files.append(str(filepath))
            return False

    def fix_all_chips(self, base_path="components"):
        """Fix all chip files with enhanced scaling"""
        base_path = Path(base_path)
        
        if not base_path.exists():
            print(f"❌ Components directory not found: {base_path}")
            return False
        
        print(f"🔍 Searching for chip files in: {base_path}")
        
        # Find all Python files
        chip_files = []
        for subdir in base_path.iterdir():
            if subdir.is_dir():
                for py_file in subdir.glob("*.py"):
                    if py_file.name != "__init__.py":
                        chip_files.append(py_file)
        
        print(f"📁 Found {len(chip_files)} chip files to fix")
        
        if not chip_files:
            print("⚠️  No chip files found")
            return False
        
        # Group files by era for better reporting
        era_groups = {}
        
        for chip_file in chip_files:
            try:
                with open(chip_file, 'r') as f:
                    content = f.read()
                metadata = self.extract_chip_metadata(content)
                year = metadata.get('year', '1985')
                era = self.get_era_from_year(year)
                
                if era not in era_groups:
                    era_groups[era] = []
                era_groups[era].append(chip_file)
            except:
                # Default era if we can't read the file
                if 'Unknown' not in era_groups:
                    era_groups['Unknown'] = []
                era_groups['Unknown'].append(chip_file)
        
        print("\n📊 Chips by Era:")
        for era, files in era_groups.items():
            scale = self.era_scale_factors.get(era, 1.0)
            print(f"  {era}: {len(files)} chips (Scale: {scale}x)")
        
        print("\n🔧 Fixing chips...")
        
        # Fix each file
        for chip_file in chip_files:
            self.fix_file(chip_file)
        
        # Report results
        print(f"\n📊 Fix Results:")
        print(f"  ✅ Successfully fixed: {len(self.fixed_files)}")
        print(f"  ❌ Failed to fix: {len(self.error_files)}")
        
        if self.fixed_files:
            print(f"\n✅ Fixed files:")
            for file in self.fixed_files:
                print(f"    {file}")
        
        if self.error_files:
            print(f"\n❌ Error files:")
            for file in self.error_files:
                print(f"    {file}")
        
        return len(self.error_files) == 0

    def create_test_chips(self):
        """Create test chips showing different eras and packages"""
        test_chips = [
            {
                'filename': 'test_early_cpu.py',
                'name': 'Early CPU 1970s',
                'package': 'DIP-40',
                'year': '1974',
                'category': 'CPU'
            },
            {
                'filename': 'test_classic_cpu.py', 
                'name': 'Classic CPU 1980s',
                'package': 'DIP-40',
                'year': '1985',
                'category': 'CPU'
            },
            {
                'filename': 'test_wide_cpu.py',
                'name': 'Wide CPU 1980s',
                'package': 'DIP-64',
                'year': '1979',
                'category': 'CPU'
            },
            {
                'filename': 'test_modern_cpu.py',
                'name': 'Modern CPU 1990s',
                'package': 'QFP-100',
                'year': '1995',
                'category': 'CPU'
            }
        ]
        
        for chip in test_chips:
            content = f'''"""
{chip['name']} - Test chip showing {chip['year']} era scaling
Package: {chip['package']}
"""

from component_library import ComponentDefinition

def create_component():
    comp = ComponentDefinition(
        "test_{chip['name'].lower().replace(' ', '_')}",
        "{chip['name']}",
        "{chip['category']}",
        "Test chip from {chip['year']} showing era-appropriate scaling",
        width=200,
        height=100
    )
    
    comp.package_type = "{chip['package']}"
    
    # Set year for era scaling
    comp.set_property("year", "{chip['year']}")
    comp.set_property("manufacturer", "Test Corp")
    
    # Add sample pins (will be positioned by the fixer)
    comp.add_pin("VCC")
    comp.add_pin("A0") 
    comp.add_pin("A1")
    comp.add_pin("A2")
    comp.add_pin("D0")
    comp.add_pin("D1")
    comp.add_pin("D2")
    comp.add_pin("D3")
    comp.add_pin("CLK")
    comp.add_pin("RESET")
    comp.add_pin("CS")
    comp.add_pin("RD")
    comp.add_pin("WR")
    comp.add_pin("GND")
    
    return comp
'''
            
            with open(chip['filename'], 'w') as f:
                f.write(content)
            
            print(f"📝 Created test chip: {chip['filename']}")


def main():
    """Main function"""
    print("🛠️  Enhanced Retro Chip Pin Fixer")
    print("=" * 50)
    print("Fixes pin positions with realistic scaling:")
    print("• Proper DIP-64 width scaling")
    print("• Historical chip size variations")
    print("• Era-appropriate dimensions")
    print()
    
    fixer = EnhancedChipPinFixer()
    
    # Check components directory
    components_dir = Path("components")
    if not components_dir.exists():
        print("❌ Components directory not found!")
        print("Creating test chips to demonstrate the fixer...")
        fixer.create_test_chips()
        
        print("\n💡 Test chips created. Run the fixer on them:")
        print("   python enhanced_pin_fixer.py")
        return 1
    
    # Fix all chip files
    success = fixer.fix_all_chips()
    
    if success:
        print("\n🎉 All chip files fixed with realistic scaling!")
        print("Key improvements:")
        print("  • DIP-64 packages are now properly wider")
        print("  • 1970s chips are larger (early fab processes)")
        print("  • 1990s+ chips are smaller (advanced processes)")
        print("  • Pin positions scaled to match chip dimensions")
        
    else:
        print("\n⚠️  Some files could not be fixed.")
    
    print("\n💡 Now your chips will have:")
    print("  📏 Realistic package scaling")
    print("  📅 Historical size accuracy") 
    print("  📍 Properly positioned pins")
    print("  🎨 Era-appropriate appearance")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())