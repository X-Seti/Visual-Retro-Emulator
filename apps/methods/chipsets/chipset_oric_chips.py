"""
X-Seti June13 2025 - Oric Atmos/1 Chipset Definitions
Visual Retro System Emulator Builder - Oric Computer Core Chips
"""

def add_oric_chips(generator):
    """Add Oric Atmos/1 chipset components"""
    
    # ULA - Custom Gate Array
    generator.add_chip(
        name="ULA Oric",
        chip_id="oric_ula",
        category="Custom",
        description="Custom ULA for Oric Atmos/1 - Video and system control",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RW'}, {'name': 'φ2'}, {'name': 'IRQ'}, {'name': 'NMI'},
            {'name': 'RESET'}, {'name': 'RDY'}, {'name': 'SYNC'}, {'name': 'SO'},
            {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'LUMA'},
            {'name': 'CHROMA'}, {'name': 'CSYNC'}, {'name': 'HSYNC'}, {'name': 'VSYNC'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # AY-3-8912 - Sound chip (same family as MSX)
    generator.add_chip(
        name="AY-3-8912",
        chip_id="oric_ay3_8912",
        category="Audio",
        description="Programmable Sound Generator for Oric",
        package_types=["DIP-28"],
        pins=[
            {'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'}, {'name': 'DA3'},
            {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'}, {'name': 'DA7'},
            {'name': 'BDIR'}, {'name': 'BC1'}, {'name': 'BC2'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'RESET'}, {'name': 'CLOCK'}, {'name': 'IOA0'},
            {'name': 'IOA1'}, {'name': 'IOA2'}, {'name': 'IOA3'}, {'name': 'IOA4'},
            {'name': 'IOA5'}, {'name': 'IOA6'}, {'name': 'IOA7'}, {'name': 'CHANNEL_A'},
            {'name': 'CHANNEL_B'}, {'name': 'CHANNEL_C'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # VIA 6522 - Versatile Interface Adapter
    generator.add_chip(
        name="VIA 6522",
        chip_id="oric_via",
        category="I/O",
        description="Versatile Interface Adapter for Oric keyboard and I/O",
        package_types=["DIP-40"],
        pins=[
            {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'},
            {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'},
            {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'}, {'name': 'PB3'},
            {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'}, {'name': 'PB7'},
            {'name': 'CA1'}, {'name': 'CA2'}, {'name': 'CB1'}, {'name': 'CB2'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RS0'}, {'name': 'RS1'}, {'name': 'RS2'}, {'name': 'RS3'},
            {'name': 'CS1'}, {'name': 'CS2'}, {'name': 'φ2'}, {'name': 'RW'},
            {'name': 'IRQ'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # 6502 CPU - Main processor
    generator.add_chip(
        name="CPU 6502",
        chip_id="oric_6502",
        category="Processor",
        description="MOS 6502 CPU for Oric Atmos/1",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RW'}, {'name': 'φ1'}, {'name': 'φ2'}, {'name': 'φ0'},
            {'name': 'IRQ'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'RDY'},
            {'name': 'SO'}, {'name': 'SYNC'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # BASIC ROM
    generator.add_chip(
        name="BASIC ROM",
        chip_id="oric_basic_rom",
        category="Memory",
        description="BASIC interpreter ROM for Oric",
        package_types=["DIP-28"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'CE'}, {'name': 'OE'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VPP'}, {'name': 'NC'}
        ]
    )

    # Character Generator ROM
    generator.add_chip(
        name="Character ROM",
        chip_id="oric_char_rom",
        category="Memory",
        description="Character generator ROM for Oric display",
        package_types=["DIP-24"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'D0'},
            {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'},
            {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CE'},
            {'name': 'OE'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # RAM - System Memory
    generator.add_chip(
        name="RAM 4116",
        chip_id="oric_ram_4116",
        category="Memory",
        description="16Kx1 Dynamic RAM for Oric system memory",
        package_types=["DIP-16"],
        pins=[
            {'name': 'VBB'}, {'name': 'DIN'}, {'name': 'WRITE'}, {'name': 'RAS'},
            {'name': 'A0'}, {'name': 'A2'}, {'name': 'A1'}, {'name': 'VDD'},
            {'name': 'VCC'}, {'name': 'DOUT'}, {'name': 'CAS'}, {'name': 'A3'},
            {'name': 'A6'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'VSS'}
        ]
    )

    # Disk Controller (for Microdisc)
    generator.add_chip(
        name="FDC 1793",
        chip_id="oric_fdc_1793",
        category="Storage",
        description="Floppy Disk Controller for Oric Microdisc",
        package_types=["DIP-40"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RE'},
            {'name': 'WE'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'},
            {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'},
            {'name': 'D7'}, {'name': 'CLK'}, {'name': 'RESET'}, {'name': 'READY'},
            {'name': 'WF'}, {'name': 'WG'}, {'name': 'TG00'}, {'name': 'IP'},
            {'name': 'WPRT'}, {'name': 'TR00'}, {'name': 'STEP'}, {'name': 'DIRC'},
            {'name': 'WD'}, {'name': 'RD'}, {'name': 'HLD'}, {'name': 'HLT'},
            {'name': 'ENBL'}, {'name': 'DRQ'}, {'name': 'DDEN'}, {'name': 'INTRQ'},
            {'name': 'MR'}, {'name': 'TEST'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VSS'}, {'name': 'VDD'}, {'name': 'VBB'}, {'name': 'NC'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Oric Atmos/1 chipset definitions loaded")
    print("Available chips: ULA, AY-3-8912, VIA 6522, 6502 CPU, BASIC ROM, Character ROM, RAM, FDC")
