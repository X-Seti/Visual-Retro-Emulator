"""
X-Seti June13 2025 - Nintendo Extended Chipset Definitions
Visual Retro System Emulator Builder - Nintendo Extended Systems
"""

def add_nintendo_snes_chips(generator):
    """Add Super Nintendo (SNES) chipset components"""
    
    # 5A22 CPU - Main processor (65816 based)
    generator.add_chip(
        name="5A22 CPU",
        chip_id="snes_5a22",
        category="Processor",
        description="Ricoh 5A22 - 65816 based CPU for SNES",
        package_types=["QFP-80"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RW'}, {'name': 'VDA'}, {'name': 'VPA'}, {'name': 'ML'},
            {'name': 'VP'}, {'name': 'SYNC'}, {'name': 'PHI2'}, {'name': 'BE'},
            {'name': 'IRQ'}, {'name': 'NMI'}, {'name': 'ABORT'}, {'name': 'RES'},
            {'name': 'RDY'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # PPU1 - Picture Processing Unit 1
    generator.add_chip(
        name="PPU1 5C77",
        chip_id="snes_ppu1",
        category="Video",
        description="Picture Processing Unit 1 - Background and sprite rendering",
        package_types=["QFP-100"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'RW'},
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'INT'},
            {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'},
            {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'},
            {'name': 'PARD'}, {'name': 'PAWR'}, {'name': 'HBLANK'}, {'name': 'VBLANK'},
            {'name': 'OVER'}, {'name': '5M'}, {'name': 'DOT'}, {'name': 'FIELD'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

    # PPU2 - Picture Processing Unit 2
    generator.add_chip(
        name="PPU2 5C78",
        chip_id="snes_ppu2",
        category="Video",
        description="Picture Processing Unit 2 - Video output and effects",
        package_types=["QFP-100"],
        pins=[
            {'name': 'PD0'}, {'name': 'PD1'}, {'name': 'PD2'}, {'name': 'PD3'},
            {'name': 'PD4'}, {'name': 'PD5'}, {'name': 'PD6'}, {'name': 'PD7'},
            {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'},
            {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'},
            {'name': 'PARD'}, {'name': 'PAWR'}, {'name': 'HBLANK'}, {'name': 'VBLANK'},
            {'name': 'OVER'}, {'name': '5M'}, {'name': 'DOT'}, {'name': 'FIELD'},
            {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'},
            {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'},
            {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'},
            {'name': 'CSYNC'}, {'name': 'BURST'}, {'name': 'HIRES'}, {'name': 'TOUMEI'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

    # APU - Audio Processing Unit
    generator.add_chip(
        name="APU SPC700",
        chip_id="snes_apu",
        category="Audio",
        description="Audio Processing Unit - SPC700 sound processor",
        package_types=["QFP-80"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RW'}, {'name': 'IRQ'}, {'name': 'RESET'}, {'name': 'CLK'},
            {'name': 'P00'}, {'name': 'P01'}, {'name': 'P02'}, {'name': 'P03'},
            {'name': 'P10'}, {'name': 'P11'}, {'name': 'P12'}, {'name': 'P13'},
            {'name': 'P20'}, {'name': 'P21'}, {'name': 'P22'}, {'name': 'P23'},
            {'name': 'P30'}, {'name': 'P31'}, {'name': 'P32'}, {'name': 'P33'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

    # DSP - Digital Sound Processor
    generator.add_chip(
        name="DSP S-DSP",
        chip_id="snes_dsp",
        category="Audio",
        description="Digital Sound Processor - 8-channel sample playback",
        package_types=["QFP-80"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'CS'},
            {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'CLK'},
            {'name': 'AOUT_L'}, {'name': 'AOUT_R'}, {'name': 'VIN_L'}, {'name': 'VIN_R'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'AVCC'}, {'name': 'AGND'}
        ]
    )

def add_nintendo_n64_chips(generator):
    """Add Nintendo 64 chipset components"""
    
    # VR4300 CPU - Main processor
    generator.add_chip(
        name="VR4300 CPU",
        chip_id="n64_vr4300",
        category="Processor",
        description="NEC VR4300 - 64-bit RISC CPU for N64",
        package_types=["QFP-196"],
        pins=[
            # Address Bus
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'},
            {'name': 'A24'}, {'name': 'A25'}, {'name': 'A26'}, {'name': 'A27'},
            {'name': 'A28'}, {'name': 'A29'}, {'name': 'A30'}, {'name': 'A31'},
            # Data Bus
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'D16'}, {'name': 'D17'}, {'name': 'D18'}, {'name': 'D19'},
            {'name': 'D20'}, {'name': 'D21'}, {'name': 'D22'}, {'name': 'D23'},
            {'name': 'D24'}, {'name': 'D25'}, {'name': 'D26'}, {'name': 'D27'},
            {'name': 'D28'}, {'name': 'D29'}, {'name': 'D30'}, {'name': 'D31'},
            # Control
            {'name': 'INT0'}, {'name': 'INT1'}, {'name': 'INT2'}, {'name': 'INT3'},
            {'name': 'INT4'}, {'name': 'INT5'}, {'name': 'NMI'}, {'name': 'RESET'},
            {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}
        ]
    )

    # RCP - Reality Coprocessor
    generator.add_chip(
        name="RCP NUS-GPU",
        chip_id="n64_rcp",
        category="Video",
        description="Reality Coprocessor - Graphics and audio processing",
        package_types=["BGA-256"],
        pins=[
            # RDRAM Interface
            {'name': 'RA0'}, {'name': 'RA1'}, {'name': 'RA2'}, {'name': 'RA3'},
            {'name': 'RA4'}, {'name': 'RA5'}, {'name': 'RA6'}, {'name': 'RA7'},
            {'name': 'RA8'}, {'name': 'RA9'}, {'name': 'RD0'}, {'name': 'RD1'},
            {'name': 'RD2'}, {'name': 'RD3'}, {'name': 'RD4'}, {'name': 'RD5'},
            {'name': 'RD6'}, {'name': 'RD7'}, {'name': 'RD8'}, {'name': 'RD9'},
            {'name': 'RCLK'}, {'name': 'RRAS'}, {'name': 'RCAS'}, {'name': 'RWE'},
            # Video Output
            {'name': 'VID_CLK'}, {'name': 'DSYNC'}, {'name': 'VSYNC'}, {'name': 'HSYNC'},
            {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'},
            {'name': 'R4'}, {'name': 'R5'}, {'name': 'R6'}, {'name': 'G0'},
            {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'}, {'name': 'G4'},
            {'name': 'G5'}, {'name': 'G6'}, {'name': 'B0'}, {'name': 'B1'},
            {'name': 'B2'}, {'name': 'B3'}, {'name': 'B4'}, {'name': 'B5'},
            {'name': 'B6'}, {'name': 'LRCK'}, {'name': 'SCLK'}, {'name': 'SDATA'},
            # System
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

def add_nintendo_gamecube_chips(generator):
    """Add Nintendo GameCube chipset components"""
    
    # Gekko CPU - PowerPC based
    generator.add_chip(
        name="Gekko CPU",
        chip_id="gcn_gekko",
        category="Processor",
        description="IBM Gekko - PowerPC 750 based CPU for GameCube",
        package_types=["BGA-256"],
        pins=[
            # Address Bus
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'},
            {'name': 'A24'}, {'name': 'A25'}, {'name': 'A26'}, {'name': 'A27'},
            {'name': 'A28'}, {'name': 'A29'}, {'name': 'A30'}, {'name': 'A31'},
            # Data Bus
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'D16'}, {'name': 'D17'}, {'name': 'D18'}, {'name': 'D19'},
            {'name': 'D20'}, {'name': 'D21'}, {'name': 'D22'}, {'name': 'D23'},
            {'name': 'D24'}, {'name': 'D25'}, {'name': 'D26'}, {'name': 'D27'},
            {'name': 'D28'}, {'name': 'D29'}, {'name': 'D30'}, {'name': 'D31'},
            # Control
            {'name': 'INT'}, {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'VCC'},
            {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VREF'}
        ]
    )

    # Flipper GPU - Graphics and system functions
    generator.add_chip(
        name="Flipper GPU",
        chip_id="gcn_flipper",
        category="Video",
        description="ATI Flipper - Graphics and system controller for GameCube",
        package_types=["BGA-476"],
        pins=[
            # Memory Interface
            {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'}, {'name': 'MA3'},
            {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'}, {'name': 'MA7'},
            {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'}, {'name': 'MA11'},
            {'name': 'MA12'}, {'name': 'MA13'}, {'name': 'MA14'}, {'name': 'MA15'},
            {'name': 'MD0'}, {'name': 'MD1'}, {'name': 'MD2'}, {'name': 'MD3'},
            {'name': 'MD4'}, {'name': 'MD5'}, {'name': 'MD6'}, {'name': 'MD7'},
            {'name': 'MD8'}, {'name': 'MD9'}, {'name': 'MD10'}, {'name': 'MD11'},
            {'name': 'MD12'}, {'name': 'MD13'}, {'name': 'MD14'}, {'name': 'MD15'},
            # Video Output
            {'name': 'VID_CLK'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'},
            {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'},
            {'name': 'R4'}, {'name': 'R5'}, {'name': 'R6'}, {'name': 'R7'},
            {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'},
            {'name': 'G4'}, {'name': 'G5'}, {'name': 'G6'}, {'name': 'G7'},
            {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'},
            {'name': 'B4'}, {'name': 'B5'}, {'name': 'B6'}, {'name': 'B7'},
            # Audio
            {'name': 'AUD_L'}, {'name': 'AUD_R'}, {'name': 'AUD_CLK'}, {'name': 'AUD_LRCK'},
            # System
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

def add_nintendo_gameboy_chips(generator):
    """Add Nintendo Game Boy chipset components"""
    
    # DMG CPU - Sharp LR35902
    generator.add_chip(
        name="DMG CPU LR35902",
        chip_id="gb_dmg_cpu",
        category="Processor",
        description="Sharp LR35902 - Game Boy CPU (Z80-like with custom video)",
        package_types=["QFP-80"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RD'}, {'name': 'WR'}, {'name': 'CS'}, {'name': 'RESET'},
            {'name': 'CLK'}, {'name': 'INT'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Nintendo Extended chipset definitions loaded")
    print("SNES chips: 5A22, PPU1, PPU2, APU, DSP")
    print("N64 chips: VR4300, RCP")
    print("GameCube chips: Gekko, Flipper")
    print("Game Boy chips: DMG CPU")
