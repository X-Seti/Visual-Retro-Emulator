"""
X-Seti June13 2025 - Sega Genesis/Mega Drive Chipset Definitions
Visual Retro System Emulator Builder - Sega Genesis Core Chips
"""

def add_sega_genesis_chips(generator):
    """Add Sega Genesis/Mega Drive chipset components"""
    
    # VDP - Video Display Processor (315-5313)
    generator.add_chip(
        name="VDP 315-5313",
        chip_id="genesis_vdp",
        category="Video",
        description="Video Display Processor for Sega Genesis",
        package_types=["QFP-64", "QFP-68"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'},
            {'name': 'AS'}, {'name': 'UDS'}, {'name': 'LDS'}, {'name': 'RW'},
            {'name': 'DTACK'}, {'name': 'CE0'}, {'name': 'OE0'}, {'name': 'WE0'},
            {'name': 'TIME'}, {'name': 'CART'}, {'name': 'CAS0'}, {'name': 'RAS0'},
            {'name': 'VA0'}, {'name': 'VA1'}, {'name': 'VA2'}, {'name': 'VA3'},
            {'name': 'VA4'}, {'name': 'VA5'}, {'name': 'VA6'}, {'name': 'VA7'},
            {'name': 'VA8'}, {'name': 'VA9'}, {'name': 'VA10'}, {'name': 'VA11'},
            {'name': 'VA12'}, {'name': 'VA13'}, {'name': 'VA14'}, {'name': 'VA15'},
            {'name': 'VD0'}, {'name': 'VD1'}, {'name': 'VD2'}, {'name': 'VD3'},
            {'name': 'VD4'}, {'name': 'VD5'}, {'name': 'VD6'}, {'name': 'VD7'},
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'EDCLK'}, {'name': 'MCLK'},
            {'name': 'ZCLK'}, {'name': 'VCLK'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VREF'}, {'name': 'NC'}
        ]
    )

    # YM2612 - FM Sound Synthesizer
    generator.add_chip(
        name="YM2612 FM",
        chip_id="genesis_ym2612",
        category="Audio",
        description="FM Sound Synthesizer for Sega Genesis",
        package_types=["DIP-24", "QFP-44"],
        pins=[
            {'name': 'GND'}, {'name': 'Vss'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'A0'}, {'name': 'A1'},
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'IC'},
            {'name': 'φM'}, {'name': 'SH1'}, {'name': 'SH2'}, {'name': 'SO'},
            {'name': 'MO'}, {'name': 'RO'}, {'name': 'LO'}, {'name': 'Vdd'}
        ]
    )

    # SN76489 - PSG (same as TI-99/4A)
    generator.add_chip(
        name="SN76489 PSG",
        chip_id="genesis_sn76489",
        category="Audio",
        description="Programmable Sound Generator for Sega Genesis",
        package_types=["DIP-16"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'WE'}, {'name': 'CE'}, {'name': 'READY'}, {'name': 'CLOCK'},
            {'name': 'AUDIO'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # Z80 - Secondary CPU
    generator.add_chip(
        name="Z80 CPU",
        chip_id="genesis_z80",
        category="Processor",
        description="Z80 CPU for sound processing in Sega Genesis",
        package_types=["DIP-40", "PLCC-44", "QFP-44"],
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

    # 68000 - Main CPU
    generator.add_chip(
        name="MC68000 CPU",
        chip_id="genesis_68000",
        category="Processor",
        description="Motorola 68000 main CPU for Sega Genesis",
        package_types=["DIP-64", "PGA-68", "QFP-68"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'},
            {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'},
            {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'},
            {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'},
            {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'}, {'name': 'AS'},
            {'name': 'UDS'}, {'name': 'LDS'}, {'name': 'R/W'}, {'name': 'DTACK'},
            {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'BR'}, {'name': 'FC0'},
            {'name': 'FC1'}, {'name': 'FC2'}, {'name': 'IPL0'}, {'name': 'IPL1'},
            {'name': 'IPL2'}, {'name': 'BERR'}, {'name': 'VPA'}, {'name': 'VMA'},
            {'name': 'E'}, {'name': 'RESET'}, {'name': 'HALT'}, {'name': 'CLK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Sega Genesis chipset definitions loaded")
    print("Available chips: VDP, YM2612, SN76489, Z80, MC68000")