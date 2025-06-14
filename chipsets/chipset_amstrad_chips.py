"""
X-Seti June13 2025 - Amstrad CPC Chipset Definitions
Visual Retro System Emulator Builder - Amstrad CPC Core Chips
"""

def add_amstrad_cpc_chips(generator):
    """Add Amstrad CPC chipset components"""
    
    # Gate Array - Custom ASIC
    generator.add_chip(
        name="Gate Array 40007",
        chip_id="amstrad_gate_array",
        category="Custom",
        description="Custom Gate Array - Memory management and video control",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': '6MHZ'}, {'name': 'φ'}, {'name': 'RAS'}, {'name': 'CAS'},
            {'name': 'READY'}, {'name': 'CASAD'}, {'name': 'CPUClock'}, {'name': 'CCLK'},
            {'name': 'DISPEN'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'INT'},
            {'name': 'IORQ'}, {'name': 'M1'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # CRTC - Cathode Ray Tube Controller
    generator.add_chip(
        name="CRTC 6845",
        chip_id="amstrad_crtc",
        category="Video",
        description="Cathode Ray Tube Controller for CPC display",
        package_types=["DIP-40"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'}, {'name': 'MA3'},
            {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'}, {'name': 'MA7'},
            {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'}, {'name': 'MA11'},
            {'name': 'MA12'}, {'name': 'MA13'}, {'name': 'RA0'}, {'name': 'RA1'},
            {'name': 'RA2'}, {'name': 'RA3'}, {'name': 'RA4'}, {'name': 'HSYNC'},
            {'name': 'VSYNC'}, {'name': 'DE'}, {'name': 'CURSOR'}, {'name': 'LPSTB'},
            {'name': 'CS'}, {'name': 'RS'}, {'name': 'RW'}, {'name': 'E'},
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # PSG - Programmable Sound Generator
    generator.add_chip(
        name="AY-3-8912",
        chip_id="amstrad_psg",
        category="Audio",
        description="Programmable Sound Generator for CPC audio",
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

    # PPI - Programmable Peripheral Interface
    generator.add_chip(
        name="PPI 8255",
        chip_id="amstrad_ppi",
        category="I/O",
        description="Programmable Peripheral Interface - Keyboard and peripherals",
        package_types=["DIP-40"],
        pins=[
            {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'},
            {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'},
            {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'}, {'name': 'PB3'},
            {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'}, {'name': 'PB7'},
            {'name': 'PC0'}, {'name': 'PC1'}, {'name': 'PC2'}, {'name': 'PC3'},
            {'name': 'PC4'}, {'name': 'PC5'}, {'name': 'PC6'}, {'name': 'PC7'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RD'},
            {'name': 'WR'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # Z80 CPU - Main processor
    generator.add_chip(
        name="Z80A CPU",
        chip_id="amstrad_z80",
        category="Processor",
        description="Zilog Z80A CPU for Amstrad CPC",
        package_types=["DIP-40", "PLCC-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'M1'}, {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'},
            {'name': 'WR'}, {'name': 'RFSH'}, {'name': 'HALT'}, {'name': 'WAIT'},
            {'name': 'INT'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'BUSRQ'},
            {'name': 'BUSAK'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # FDC - Floppy Disk Controller (CPC664/6128)
    generator.add_chip(
        name="FDC µPD765",
        chip_id="amstrad_fdc",
        category="Storage",
        description="Floppy Disk Controller for CPC664/6128",
        package_types=["DIP-40"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'TC'}, {'name': 'IDX'},
            {'name': 'RDY'}, {'name': 'WP'}, {'name': 'TRK00'}, {'name': 'WG'},
            {'name': 'WD'}, {'name': 'STEP'}, {'name': 'DIR'}, {'name': 'RD_DATA'},
            {'name': 'DRQ'}, {'name': 'DACK'}, {'name': 'INT'}, {'name': 'US0'},
            {'name': 'US1'}, {'name': 'MO'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VBB'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'NC'},
            {'name': 'NC2'}, {'name': 'NC3'}, {'name': 'NC4'}, {'name': 'TEST'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Amstrad CPC chipset definitions loaded")
    print("Available chips: Gate Array, CRTC, PSG, PPI, Z80, FDC")
