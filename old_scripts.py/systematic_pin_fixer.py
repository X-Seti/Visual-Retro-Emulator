#!/usr/bin/env python3
"""
Systematic Pin Color and Spacing Fixer
Mr. Spock would approve of this logical approach to fixing chip pins
"""

import os
import re
from pathlib import Path


class LogicalPinFixer:
    """A systematic approach to fixing pin colors and spacing - most logical"""
    
    def __init__(self):
        self.pin_color_standards = {
            # Power pins
            'VCC': 'power', 'VDD': 'power', '+5V': 'power', '+3V': 'power', 
            'POWER': 'power', 'VPP': 'power',
            
            # Ground pins  
            'GND': 'ground', 'VSS': 'ground', 'GROUND': 'ground', '-5V': 'ground',
            
            # Clock signals
            'CLK': 'clock', 'CLOCK': 'clock', 'OSC': 'clock', 'XTAL': 'clock',
            'ECLK': 'clock', 'MCLK': 'clock', 'PCLK': 'clock', 'PHI1': 'clock', 
            'PHI2': 'clock', 'E': 'clock', '28M': 'clock', '7M': 'clock',
            
            # Control signals
            'RESET': 'control', 'RES': 'control', 'AS': 'control', 'DS': 'control',
            'RW': 'control', 'R/W': 'control', 'RD': 'control', 'WR': 'control',
            'CS': 'control', 'CE': 'control', 'OE': 'control', 'WE': 'control',
            'DTACK': 'control', 'READY': 'control', 'WAIT': 'control',
            'IRQ': 'control', 'NMI': 'control', 'INT': 'control', 'HALT': 'control',
            'BR': 'control', 'BG': 'control', 'BGACK': 'control',
            'UDS': 'control', 'LDS': 'control', 'BERR': 'control',
            'VPA': 'control', 'VMA': 'control', 'DMAL': 'control',
            
            # Video signals
            'HSYNC': 'video', 'VSYNC': 'video', 'CSYNC': 'video', 'SYNC': 'video',
            'RED': 'video', 'GREEN': 'video', 'BLUE': 'video', 'BURST': 'video',
            'VIDEO': 'video', 'BLANK': 'video', 'LUMA': 'video', 'CHROMA': 'video',
            'R0': 'video', 'R1': 'video', 'R2': 'video', 'R3': 'video',
            'G0': 'video', 'G1': 'video', 'G2': 'video', 'G3': 'video',
            'B0': 'video', 'B1': 'video', 'B2': 'video', 'B3': 'video',
            
            # Audio signals
            'AUDIO': 'audio', 'SOUND': 'audio', 'AUD0': 'audio', 'AUD1': 'audio',
            'AUD2': 'audio', 'AUD3': 'audio', 'AUDR': 'audio', 'AUDL': 'audio',
            'MO': 'audio', 'SO': 'audio',
            
            # Analog signals
            'POT0X': 'analog', 'POT0Y': 'analog', 'POT1X': 'analog', 'POT1Y': 'analog',
            'ANALOG': 'analog', 'AIN': 'analog', 'AOUT': 'analog',
            
            # Memory control
            'RAS': 'control', 'CAS': 'control', 'RAS0': 'control', 'CAS0': 'control',
            'CAS1': 'control', 'CAS2': 'control', 'CAS3': 'control',
            'CASU': 'control', 'CASL': 'control',
            
            # Special function pins
            'TXD': 'control', 'RXD': 'control', 'DKWD': 'control', 'DKRD': 'control',
            'DKWE': 'control', 'INDEX': 'control', 'WPRT': 'control',
            'NC': 'unused', 'N/C': 'unused', 'NO CONNECT': 'unused'
        }
        
        self.package_standards = {
            'DIP-8': {'width': 24, 'height': 40, 'pin_spacing': 5},
            'DIP-14': {'width': 24, 'height': 72, 'pin_spacing': 5},
            'DIP-16': {'width': 24, 'height': 80, 'pin_spacing': 5},
            'DIP-18': {'width': 24, 'height': 88, 'pin_spacing': 5},
            'DIP-20': {'width': 24, 'height': 96, 'pin_spacing': 5},
            'DIP-24': {'width': 24, 'height': 112, 'pin_spacing': 4.5},
            'DIP-28': {'width': 24, 'height': 128, 'pin_spacing': 4.5},
            'DIP-40': {'width': 40, 'height': 200, 'pin_spacing': 5},
            'DIP-48': {'width': 40, 'height': 240, 'pin_spacing': 5},
            'DIP-64': {'width': 60, 'height': 320, 'pin_spacing': 5},  # Reasonable width
            
            'QFP-44': {'width': 80, 'height': 80, 'pin_spacing': 4},
            'QFP-48': {'width': 80, 'height': 80, 'pin_spacing': 4},
            'QFP-52': {'width': 90, 'height': 90, 'pin_spacing': 4},
            'QFP-64': {'width': 100, 'height': 100, 'pin_spacing': 4},
            'QFP-68': {'width': 100, 'height': 100, 'pin_spacing': 3.5},
            'QFP-84': {'width': 120, 'height': 120, 'pin_spacing': 3.5},
            'QFP-100': {'width': 140, 'height': 140, 'pin_spacing': 3},
            
            'PLCC-44': {'width': 80, 'height': 80, 'pin_spacing': 4},
            'PLCC-68': {'width': 100, 'height': 100, 'pin_spacing': 3.5},
            'PLCC-84': {'width': 120, 'height': 120, 'pin_spacing': 3.5}
        }
        
        self.fixed_files = []
        self.error_files = []
    
    def analyze_pin_name(self, pin_name):
        """Logical analysis of pin name to determine type"""
        pin_upper = pin_name.upper().strip()
        
        # Direct match first
        if pin_upper in self.pin_color_standards:
            return self.pin_color_standards[pin_upper]
        
        # Pattern matching for numbered pins
        if re.match(r'^A\d+$', pin_upper):  # Address lines A0, A1, etc.
            return 'address'
        elif re.match(r'^D\d+$', pin_upper):  # Data lines D0, D1, etc.
            return 'data'
        elif re.match(r'^P\d+$', pin_upper):  # Port pins P0, P1, etc.
            return 'io'
        elif re.match(r'^PA\d+$', pin_upper):  # Port A pins
            return 'io'
        elif re.match(r'^PB\d+$', pin_upper):  # Port B pins
            return 'io'
        elif re.match(r'^INT\d+$', pin_upper):  # Interrupt pins
            return 'control'
        elif re.match(r'^IPL\d+$', pin_upper):  # Interrupt priority level
            return 'control'
        elif re.match(r'^FC\d+$', pin_upper):  # Function code pins
            return 'control'
        elif re.match(r'^RGA\d+$', pin_upper):  # Register access pins
            return 'control'
        elif pin_upper.startswith('DB'):  # Data bus pins
            return 'data'
        elif pin_upper.startswith('AB'):  # Address bus pins
            return 'address'
        
        # Substring matching
        for standard_pin, pin_type in self.pin_color_standards.items():
            if standard_pin in pin_upper:
                return pin_type
        
        # Default to I/O
        return 'io'
    
    def calculate_logical_pin_positions(self, package, pin_count, width, height):
        """Calculate logical pin positions based on package type"""
        
        positions = []
        
        if package.startswith('DIP'):
            # DIP packages - dual in-line
            pins_per_side = pin_count // 2
            
            # Calculate vertical spacing
            usable_height = height - 20  # Leave margins
            pin_spacing = usable_height / (pins_per_side + 1) if pins_per_side > 0 else 10
            
            # Left side pins (1 to pins_per_side)
            for i in range(pins_per_side):
                x = 10  # Standard margin
                y = 10 + (i + 1) * pin_spacing
                positions.append((x, y))
            
            # Right side pins (pins_per_side+1 to pin_count) - bottom to top
            for i in range(pins_per_side):
                x = width - 10  # Right margin
                y = 10 + (pins_per_side - i) * pin_spacing
                positions.append((x, y))
        
        elif package.startswith('QFP') or package.startswith('PLCC'):
            # Quad packages
            pins_per_side = pin_count // 4
            
            # Bottom side (1 to pins_per_side)
            spacing_x = (width - 20) / (pins_per_side + 1) if pins_per_side > 0 else 10
            for i in range(pins_per_side):
                x = 10 + (i + 1) * spacing_x
                y = height - 5
                positions.append((x, y))
            
            # Right side
            spacing_y = (height - 20) / (pins_per_side + 1) if pins_per_side > 0 else 10
            for i in range(pins_per_side):
                x = width - 5
                y = height - 10 - (i + 1) * spacing_y
                positions.append((x, y))
            
            # Top side (right to left)
            for i in range(pins_per_side):
                x = width - 10 - (i + 1) * spacing_x
                y = 5
                positions.append((x, y))
            
            # Left side (top to bottom)
            for i in range(pins_per_side):
                x = 5
                y = 10 + (i + 1) * spacing_y
                positions.append((x, y))
        
        return positions
    
    def fix_chip_file(self, file_path):
        """Fix a single chip file with logical precision"""
        
        print(f"🔧 Processing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract package and dimensions
            package_match = re.search(r'package_type\s*=\s*["\']([^"\']+)["\']', content)
            package = package_match.group(1) if package_match else 'DIP-40'
            
            width_match = re.search(r'width\s*=\s*(\d+)', content)
            height_match = re.search(r'height\s*=\s*(\d+)', content)
            
            if width_match and height_match:
                width = int(width_match.group(1))
                height = int(height_match.group(1))
            else:
                # Use standard dimensions
                standard = self.package_standards.get(package, self.package_standards['DIP-40'])
                width = standard['width']
                height = standard['height']
                
                # Update dimensions in file
                if width_match:
                    content = re.sub(r'width\s*=\s*\d+', f'width={width}', content)
                if height_match:
                    content = re.sub(r'height\s*=\s*\d+', f'height={height}', content)
            
            # Find all add_pin lines
            pin_lines = re.findall(r'comp\.add_pin\([^)]+\)', content)
            pin_count = len(pin_lines)
            
            if pin_count == 0:
                print(f"  ⚠️  No pins found in {file_path}")
                return False
            
            # Calculate logical pin positions
            positions = self.calculate_logical_pin_positions(package, pin_count, width, height)
            
            # Process each pin
            updated_content = content
            pin_index = 0
            
            def replace_pin(match):
                nonlocal pin_index
                
                if pin_index >= len(positions):
                    return match.group(0)  # Keep original if we run out of positions
                
                # Extract pin name
                pin_call = match.group(0)
                pin_name_match = re.search(r'add_pin\(\s*["\']([^"\']+)["\']', pin_call)
                
                if not pin_name_match:
                    return match.group(0)
                
                pin_name = pin_name_match.group(1)
                pin_type = self.analyze_pin_name(pin_name)
                x, y = positions[pin_index]
                
                # Create new pin call
                new_pin_call = f'comp.add_pin("{pin_name}", {int(x)}, {int(y)}, "{pin_type}")'
                
                pin_index += 1
                return new_pin_call
            
            # Replace all pin calls
            updated_content = re.sub(r'comp\.add_pin\([^)]+\)', replace_pin, updated_content)
            
            # Write the updated file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"  ✅ Fixed {pin_count} pins in {package} package")
            self.fixed_files.append(str(file_path))
            return True
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.error_files.append(str(file_path))
            return False
    
    def fix_all_chips(self):
        """Fix all chip files systematically"""
        
        print("🖖 INITIATING LOGICAL PIN FIXING SEQUENCE")
        print("=" * 45)
        
        component_dirs = [
            "components/cpu",
            "components/amiga", 
            "components/commodore",
            "components/custom",
            "components/memory",
            "components/spectrum",
            "components/support"
        ]
        
        all_files = []
        for comp_dir in component_dirs:
            if os.path.exists(comp_dir):
                for py_file in Path(comp_dir).glob("*.py"):
                    if py_file.name != "__init__.py":
                        all_files.append(py_file)
        
        print(f"📊 Found {len(all_files)} chip files to process")
        
        for file_path in all_files:
            self.fix_chip_file(file_path)
        
        print(f"\n📈 PROCESSING COMPLETE")
        print(f"  ✅ Successfully fixed: {len(self.fixed_files)}")
        print(f"  ❌ Errors encountered: {len(self.error_files)}")
        
        if self.error_files:
            print(f"\n⚠️  Files with errors:")
            for file in self.error_files:
                print(f"    {file}")
        
        return len(self.error_files) == 0
    
    def update_rendering_standards(self):
        """Update rendering.py with logical package standards"""
        
        print("\n🔧 UPDATING RENDERING STANDARDS")
        print("-" * 30)
        
        if not os.path.exists("rendering.py"):
            print("❌ rendering.py not found")
            return False
        
        try:
            with open("rendering.py", 'r') as f:
                content = f.read()
            
            # Update DIP-64 to reasonable dimensions
            if '"DIP-64"' in content:
                # Replace with logical dimensions
                pattern = r'"DIP-64":\s*\{[^}]*\}'
                replacement = '"DIP-64": {"width": 60, "height": 320, "pins": 64, "pin_spacing": 8, "row_spacing": 15.24}'
                content = re.sub(pattern, replacement, content)
                
                with open("rendering.py", 'w') as f:
                    f.write(content)
                
                print("✅ Updated DIP-64 to logical dimensions (60x320)")
                return True
            else:
                print("⚠️  DIP-64 definition not found")
                return False
                
        except Exception as e:
            print(f"❌ Error updating rendering: {e}")
            return False


def main():
    """Execute the logical pin fixing sequence"""
    
    print("🖖 SYSTEMATIC PIN CORRECTION PROTOCOL")
    print("=====================================")
    print('"Logic is the beginning of wisdom, not the end." - Spock')
    print()
    print("Initiating comprehensive pin analysis and correction...")
    print()
    
    fixer = LogicalPinFixer()
    
    # Update rendering standards first
    rendering_updated = fixer.update_rendering_standards()
    
    # Fix all chip files
    success = fixer.fix_all_chips()
    
    if success and rendering_updated:
        print("\n🎉 LOGICAL ANALYSIS COMPLETE - ALL SYSTEMS NOMINAL")
        print("\n🔧 Applied systematic corrections:")
        print("  📏 Standardized package dimensions")
        print("  📍 Logical pin positioning")
        print("  🌈 Accurate color coding")
        print("  ⚡ Proper spacing calculations")
        
        print("\n🚀 Ready for testing:")
        print("  python main_app.py")
        
        print("\n💡 Pin color legend:")
        print("  🔴 Red: Power (VCC, VDD)")
        print("  ⚫ Black: Ground (GND, VSS)")
        print("  🟢 Green: Clock (CLK, OSC)")
        print("  🟠 Orange: Address (A0-A23)")
        print("  🔵 Blue: Data (D0-D15)")
        print("  🟣 Purple: Control (RESET, CS)")
        print("  🟡 Yellow: Video (HSYNC, RGB)")
        print("  🩵 Cyan: Audio (AUD0-3)")
        print("  🩷 Pink: Analog (POT, AIN)")
        print("  🩶 Gray: I/O, Unused")
        
    else:
        print("\n⚠️  Some issues encountered during processing")
        print("Review error messages above and re-run if needed")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
