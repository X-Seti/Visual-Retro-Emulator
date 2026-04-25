"""
X-Seti June13 2025 - ZX Spectrum/ZX80 Chipset Definitions
Visual Retro System Emulator Builder - Sinclair ZX Core Chips
"""

def add_zx_spectrum_chips(generator):
    """Add ZX Spectrum chipset components"""
    
    # ULA - Uncommitted Logic Array
    generator.add_chip(
        name="ULA 6C001E-7",
        chip_id="spectrum_ula",
        category="Custom",
        description="Uncommitted Logic Array for ZX Spectrum",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'M1'}, {'name': 'RFSH'}, {'name': 'INT'}, {'name': 'CLK'},
            {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'BRIGHT'},
            {'name': 'SYNC'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CAS'},
            {'name': 'RAS'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

def add_zx80_chips(generator):
    """Add ZX80 chipset components"""
    
    # ZX80 ULA
    generator.add_chip(
        name="ULA ZX80",
        chip_id="zx80_ula",
        category="Custom",
        description="Uncommitted Logic Array for ZX80",
        package_types=["DIP-28"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'CLK'}, {'name': 'SYNC'},
            {'name': 'VIDEO'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

def add_zx81_chips(generator):
    """Add ZX81 chipset components"""
    
    # ZX81 ULA
    generator.add_chip(
        name="ULA ZX81",
        chip_id="zx81_ula",
        category="Custom",
        description="Uncommitted Logic Array for ZX81",
        package_types=["DIP-28"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'CLK'}, {'name': 'SYNC'},
            {'name': 'VIDEO'}, {'name': 'KBD'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("ZX Spectrum/ZX80/ZX81 chipset definitions loaded")
    print("Available chips: ZX Spectrum ULA, ZX80 ULA, ZX81 ULA")
