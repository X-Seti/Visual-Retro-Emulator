"""
X-Seti June13 2025 - Commodore 64 Chipset Definitions
Visual Retro System Emulator Builder - C64 Core Chips
"""

def add_c64_chips(generator):
    """Add Commodore 64 chipset components"""
    
    # SID - Sound Interface Device
    generator.add_chip(
        name="SID 6581/8580",
        chip_id="c64_sid",
        category="Audio",
        description="Sound Interface Device Chip (SID) - 3-channel synthesizer",
        package_types=["DIP-28", "QFP-44"],
        pins=[
            {'name': 'CAP1A'}, {'name': 'CAP1B'}, {'name': 'CAP2A'}, {'name': 'CAP2B'},
            {'name': 'RES'}, {'name': 'φ2'}, {'name': 'R/W'}, {'name': 'CS'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'GND'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'AUDIO'}, {'name': 'VCC'},
            {'name': 'POT X'}, {'name': 'POT Y'}, {'name': 'EXT IN'}, {'name': 'VDD'}
        ]
    )

    # VIC-II - Video Interface Chip
    generator.add_chip(
        name="VIC-II 6567/6569",
        chip_id="c64_vic2",
        category="Video",
        description="Video Interface Chip II (VIC-II) - Graphics and video controller",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'R/W'}, {'name': 'AEC'},
            {'name': 'IRQ'}, {'name': 'COLOR'}, {'name': 'SYNC'}, {'name': 'BA'},
            {'name': 'φ0'}, {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'LP'},
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # CIA - Complex Interface Adapter
    generator.add_chip(
        name="CIA 6526",
        chip_id="c64_cia",
        category="I/O",
        description="Complex Interface Adapter (CIA) - I/O and timer controller",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'VSS'}, {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'},
            {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'},
            {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'},
            {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'},
            {'name': 'PB7'}, {'name': 'PC'}, {'name': 'TOD'}, {'name': 'VDD'},
            {'name': 'IRQ'}, {'name': 'R/W'}, {'name': 'CS'}, {'name': 'φ2'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'FLAG'}, {'name': 'SP'}, {'name': 'CNT'}, {'name': 'RES'}
        ]
    )

    # PLA - Programmable Logic Array
    generator.add_chip(
        name="PLA 906114-01",
        chip_id="c64_pla",
        category="Custom",
        description="Programmable Logic Array - Memory and I/O decoding",
        package_types=["DIP-28", "PLCC-28"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'CASRAM'}, {'name': 'BASIC'}, {'name': 'KERNAL'}, {'name': 'CHAROM'},
            {'name': 'GR/W'}, {'name': 'HIRAM'}, {'name': 'LORAM'}, {'name': 'GAME'},
            {'name': 'EXROM'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}
        ]
    )

    # Color RAM - Static Color Memory
    generator.add_chip(
        name="Color RAM 2114",
        chip_id="c64_colorram",
        category="Memory",
        description="Static Color Memory - 4-bit color information storage",
        package_types=["DIP-18"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'CS'}, {'name': 'WE'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # 6510 CPU - Main processor (6502 with I/O port)
    generator.add_chip(
        name="CPU 6510",
        chip_id="c64_6510",
        category="Processor", 
        description="MOS 6510 CPU - 6502 with built-in I/O port",
        package_types=["DIP-40"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RW'}, {'name': 'φ1'}, {'name': 'φ2'}, {'name': 'φ0'},
            {'name': 'IRQ'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'RDY'},
            {'name': 'SO'}, {'name': 'SYNC'}, {'name': 'P0'}, {'name': 'P1'},
            {'name': 'P2'}, {'name': 'P3'}, {'name': 'P4'}, {'name': 'P5'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Commodore 64 chipset definitions loaded")
    print("Available chips: SID, VIC-II, CIA, PLA, Color RAM, 6510 CPU")
