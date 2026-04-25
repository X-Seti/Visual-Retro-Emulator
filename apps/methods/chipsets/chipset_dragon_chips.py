"""
X-Seti June13 2025 - Dragon 32/64 Chipset Definitions
Visual Retro System Emulator Builder - Dragon Computer Core Chips
"""

def add_dragon_chips(generator):
    """Add Dragon 32/64 chipset components"""
    
    # SAM - Synchronous Address Multiplexer
    generator.add_chip(
        name="SAM MC6883",
        chip_id="dragon_sam",
        category="Custom",
        description="Synchronous Address Multiplexer for Dragon 32/64",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'Z0'}, {'name': 'Z1'}, {'name': 'Z2'}, {'name': 'Z3'},
            {'name': 'Z4'}, {'name': 'Z5'}, {'name': 'Z6'}, {'name': 'Z7'},
            {'name': 'Z8'}, {'name': 'Z9'}, {'name': 'Z10'}, {'name': 'Z11'},
            {'name': 'Z12'}, {'name': 'Z13'}, {'name': 'Z14'}, {'name': 'Z15'},
            {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'WE'}, {'name': 'OE'},
            {'name': 'HS'}, {'name': 'FS'}, {'name': 'CLK'}, {'name': 'VCC'},
            {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # VDG - Video Display Generator
    generator.add_chip(
        name="VDG MC6847",
        chip_id="dragon_vdg",
        category="Video",
        description="Video Display Generator for Dragon 32/64",
        package_types=["DIP-40"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'}, {'name': 'DA3'},
            {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'}, {'name': 'DA7'},
            {'name': 'DA8'}, {'name': 'DA9'}, {'name': 'DA10'}, {'name': 'DA11'},
            {'name': 'RP'}, {'name': 'HS'}, {'name': 'FS'}, {'name': 'AS'},
            {'name': 'INTEXT'}, {'name': 'INV'}, {'name': 'GM0'}, {'name': 'GM1'},
            {'name': 'GM2'}, {'name': 'AG'}, {'name': 'CSS'}, {'name': 'Y'},
            {'name': 'φA'}, {'name': 'φB'}, {'name': 'CVBS'}, {'name': 'MS'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}
        ]
    )

    # PIA - Peripheral Interface Adapter (6821)
    generator.add_chip(
        name="PIA MC6821",
        chip_id="dragon_pia",
        category="I/O",
        description="Peripheral Interface Adapter for Dragon 32/64",
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

    # ACIA - Asynchronous Communications Interface Adapter (6850)
    generator.add_chip(
        name="ACIA MC6850",
        chip_id="dragon_acia",
        category="I/O",
        description="Asynchronous Communications Interface Adapter for Dragon 32/64",
        package_types=["DIP-24"],
        pins=[
            {'name': 'VSS'}, {'name': 'RXD'}, {'name': 'RXC'}, {'name': 'TXC'},
            {'name': 'RTS'}, {'name': 'TXD'}, {'name': 'IRQ'}, {'name': 'CS0'},
            {'name': 'CS2'}, {'name': 'CS1'}, {'name': 'RS'}, {'name': 'VDD'},
            {'name': 'R/W'}, {'name': 'E'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'CTS'}, {'name': 'DCD'}
        ]
    )

    # 6809 CPU - Main processor
    generator.add_chip(
        name="CPU MC6809",
        chip_id="dragon_6809",
        category="Processor",
        description="Motorola 6809 CPU for Dragon 32/64",
        package_types=["DIP-40"],
        pins=[
            {'name': 'VSS'}, {'name': 'NMI'}, {'name': 'IRQ'}, {'name': 'FIRQ'},
            {'name': 'BS'}, {'name': 'BA'}, {'name': 'VCC'}, {'name': 'A0'},
            {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'},
            {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'},
            {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D7'},
            {'name': 'D6'}, {'name': 'D5'}, {'name': 'D4'}, {'name': 'D3'},
            {'name': 'D2'}, {'name': 'D1'}, {'name': 'D0'}, {'name': 'R/W'},
            {'name': 'VMA'}, {'name': 'E'}, {'name': 'Q'}, {'name': 'AVMA'},
            {'name': 'RESET'}, {'name': 'LIC'}, {'name': 'TSC'}, {'name': 'HALT'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Dragon 32/64 chipset definitions loaded")
    print("Available chips: SAM, VDG, PIA, ACIA, 6809 CPU")
