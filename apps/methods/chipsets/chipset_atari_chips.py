"""
X-Seti June13 2025 - Atari Chipset Definitions
Visual Retro System Emulator Builder - Atari 8-bit Core Chips
"""

def add_atari_chips(generator):
    """Add Atari 8-bit chipset components"""
    
    # ANTIC - Alphanumeric Television Interface Controller
    generator.add_chip(
        name="ANTIC CO12296",
        chip_id="atari_antic",
        category="Video",
        description="Alphanumeric Television Interface Controller for Atari 8-bit",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RDY'}, {'name': 'REF'}, {'name': 'HALT'}, {'name': 'R/W'},
            {'name': 'φ0'}, {'name': 'φ2'}, {'name': 'VSYNC'}, {'name': 'HSYNC'},
            {'name': 'NMI'}, {'name': 'IRQ'}, {'name': 'RST'}, {'name': 'AN0'},
            {'name': 'AN1'}, {'name': 'AN2'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # POKEY - Pot Keyboard Integrated Circuit
    generator.add_chip(
        name="POKEY C012294",
        chip_id="atari_pokey",
        category="Audio",
        description="Pot Keyboard Integrated Circuit for Atari 8-bit",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'}, {'name': 'P3'},
            {'name': 'P4'}, {'name': 'P5'}, {'name': 'P6'}, {'name': 'P7'},
            {'name': 'K0'}, {'name': 'K1'}, {'name': 'K2'}, {'name': 'K3'},
            {'name': 'K4'}, {'name': 'K5'}, {'name': 'POT0'}, {'name': 'POT1'},
            {'name': 'POT2'}, {'name': 'POT3'}, {'name': 'POT4'}, {'name': 'POT5'},
            {'name': 'POT6'}, {'name': 'POT7'}, {'name': 'AUDIO'}, {'name': 'BID'},
            {'name': 'CS'}, {'name': 'R/W'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # GTIA - Graphics Television Interface Adapter
    generator.add_chip(
        name="GTIA CO14889",
        chip_id="atari_gtia",
        category="Video",
        description="Graphics Television Interface Adapter for Atari 8-bit",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'LUM0'}, {'name': 'LUM1'},
            {'name': 'LUM2'}, {'name': 'LUM3'}, {'name': 'COL0'}, {'name': 'COL1'},
            {'name': 'COL2'}, {'name': 'COL3'}, {'name': 'R'}, {'name': 'G'},
            {'name': 'B'}, {'name': 'SYNC'}, {'name': 'LUMI'}, {'name': 'CHROMA'},
            {'name': 'COMPOSITE'}, {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'},
            {'name': 'P3'}, {'name': 'M0'}, {'name': 'M1'}, {'name': 'M2'},
            {'name': 'M3'}, {'name': 'PF0'}, {'name': 'PF1'}, {'name': 'PF2'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # PIA - Peripheral Interface Adapter
    generator.add_chip(
        name="PIA 6520",
        chip_id="atari_pia",
        category="I/O",
        description="Peripheral Interface Adapter - Keyboard and joystick interface",
        package_types=["DIP-40"],
        pins=[
            {'name': 'VSS'}, {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'},
            {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'},
            {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'},
            {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'},
            {'name': 'PB7'}, {'name': 'CB1'}, {'name': 'CB2'}, {'name': 'VDD'},
            {'name': 'IRQA'}, {'name': 'IRQB'}, {'name': 'RS0'}, {'name': 'RS1'},
            {'name': 'RESET'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'},
            {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'},
            {'name': 'D7'}, {'name': 'E'}, {'name': 'CS0'}, {'name': 'CS1'},
            {'name': 'CS2'}, {'name': 'R/W'}, {'name': 'CA1'}, {'name': 'CA2'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Atari 8-bit chipset definitions loaded")
    print("Available chips: ANTIC, POKEY, GTIA, PIA")
