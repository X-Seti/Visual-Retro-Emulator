"""
X-Seti June13 2025 - Russian Computer Chipset Definitions
Visual Retro System Emulator Builder - Soviet/Russian Computer Core Chips
"""

def add_agat_chips(generator):
    """Add Agat (Apple II clone) chipset components"""
    
    # KR580VM80A - Z80 equivalent
    generator.add_chip(
        name="KR580VM80A CPU",
        chip_id="agat_kr580vm80a",
        category="Processor",
        description="Soviet Z80 equivalent processor for Agat",
        package_types=["DIP-40"],
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
    
    # K155RE3 - Character generator ROM
    generator.add_chip(
        name="K155RE3 CharROM",
        chip_id="agat_k155re3",
        category="Memory",
        description="Soviet character generator ROM",
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

def add_elektronika_bk_chips(generator):
    """Add Elektronika BK chipset components"""
    
    # K1801VM2 - PDP-11 compatible CPU
    generator.add_chip(
        name="K1801VM2 CPU",
        chip_id="bk_k1801vm2",
        category="Processor",
        description="Soviet PDP-11 compatible 16-bit processor",
        package_types=["DIP-40"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'SYNC'}, {'name': 'DIN'}, {'name': 'DOUT'}, {'name': 'WR'},
            {'name': 'IRQ4'}, {'name': 'IRQ5'}, {'name': 'IRQ6'}, {'name': 'IRQ7'},
            {'name': 'CLK'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # K1801RE2 - System ROM
    generator.add_chip(
        name="K1801RE2 ROM",
        chip_id="bk_k1801re2",
        category="Memory",
        description="Soviet system ROM for BK series",
        package_types=["DIP-28"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'},
            {'name': 'D10'}, {'name': 'D11'}, {'name': 'CE'}, {'name': 'OE'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

def add_pentagon_chips(generator):
    """Add Pentagon (ZX Spectrum clone) chipset components"""
    
    # Z80H - High speed Z80
    generator.add_chip(
        name="Z80H CPU",
        chip_id="pentagon_z80h",
        category="Processor",
        description="High-speed Z80 CPU for Pentagon",
        package_types=["DIP-40"],
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
    
    # Pentagon Gate Array - Custom ULA replacement
    generator.add_chip(
        name="Pentagon Gate Array",
        chip_id="pentagon_ga",
        category="Custom",
        description="Custom gate array for Pentagon - enhanced ZX Spectrum",
        package_types=["PLCC-68"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'M1'}, {'name': 'RFSH'}, {'name': 'INT'}, {'name': 'CLK'},
            {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'WE'}, {'name': 'OE'},
            {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'BRIGHT'},
            {'name': 'SYNC'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BORDER'},
            {'name': 'BEEP'}, {'name': 'TAPE_IN'}, {'name': 'TAPE_OUT'}, {'name': 'KEMPSTON'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )
    
    # AY-3-8910 - Sound chip
    generator.add_chip(
        name="AY-3-8910",
        chip_id="pentagon_ay8910",
        category="Audio",
        description="Sound synthesizer for Pentagon",
        package_types=["DIP-40"],
        pins=[
            {'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'}, {'name': 'DA3'},
            {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'}, {'name': 'DA7'},
            {'name': 'BDIR'}, {'name': 'BC1'}, {'name': 'BC2'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'RESET'}, {'name': 'CLOCK'}, {'name': 'IOA0'},
            {'name': 'IOA1'}, {'name': 'IOA2'}, {'name': 'IOA3'}, {'name': 'IOA4'},
            {'name': 'IOA5'}, {'name': 'IOA6'}, {'name': 'IOA7'}, {'name': 'IOB0'},
            {'name': 'IOB1'}, {'name': 'IOB2'}, {'name': 'IOB3'}, {'name': 'IOB4'},
            {'name': 'IOB5'}, {'name': 'IOB6'}, {'name': 'IOB7'}, {'name': 'CHANNEL_A'},
            {'name': 'CHANNEL_B'}, {'name': 'CHANNEL_C'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'ANALOG_A'}, {'name': 'ANALOG_B'},
            {'name': 'ANALOG_C'}, {'name': 'TEST1'}
        ]
    )

def add_radio86rk_chips(generator):
    """Add Radio-86RK chipset components"""
    
    # KR580VM80A - Main CPU
    generator.add_chip(
        name="KR580VM80A CPU",
        chip_id="radio86_kr580vm80a",
        category="Processor",
        description="Soviet 8080 equivalent processor for Radio-86RK",
        package_types=["DIP-40"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'READY'}, {'name': 'WAIT'}, {'name': 'WR'}, {'name': 'DBIN'},
            {'name': 'SYNC'}, {'name': 'VBB'}, {'name': 'VCC'}, {'name': 'VDD'},
            {'name': 'VSS'}, {'name': 'VBB'}, {'name': 'PHI1'}, {'name': 'PHI2'},
            {'name': 'RESET'}, {'name': 'INT'}, {'name': 'INTE'}, {'name': 'HLDA'},
            {'name': 'HOLD'}, {'name': 'GND'}
        ]
    )
    
    # KR580VV55A - PPI equivalent
    generator.add_chip(
        name="KR580VV55A PPI",
        chip_id="radio86_kr580vv55a",
        category="I/O",
        description="Soviet 8255 equivalent - Programmable Peripheral Interface",
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

def add_vector06c_chips(generator):
    """Add Vector-06C chipset components"""
    
    # KR580VM80A - Main CPU
    generator.add_chip(
        name="KR580VM80A CPU",
        chip_id="vector06_kr580vm80a",
        category="Processor",
        description="Main processor for Vector-06C",
        package_types=["DIP-40"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'READY'}, {'name': 'WAIT'}, {'name': 'WR'}, {'name': 'DBIN'},
            {'name': 'SYNC'}, {'name': 'VBB'}, {'name': 'VCC'}, {'name': 'VDD'},
            {'name': 'VSS'}, {'name': 'VBB'}, {'name': 'PHI1'}, {'name': 'PHI2'},
            {'name': 'RESET'}, {'name': 'INT'}, {'name': 'INTE'}, {'name': 'HLDA'},
            {'name': 'HOLD'}, {'name': 'GND'}
        ]
    )
    
    # KR580VG75 - CRT Controller
    generator.add_chip(
        name="KR580VG75 CRTC",
        chip_id="vector06_kr580vg75",
        category="Video",
        description="Soviet CRT controller for Vector-06C",
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

if __name__ == "__main__":
    # Test function
    print("Russian computer chipset definitions loaded")
    print("Agat chips: KR580VM80A, K155RE3")
    print("Elektronika BK chips: K1801VM2, K1801RE2")
    print("Pentagon chips: Z80H, Pentagon Gate Array, AY-3-8910")
    print("Radio-86RK chips: KR580VM80A, KR580VV55A")
    print("Vector-06C chips: KR580VM80A, KR580VG75")
