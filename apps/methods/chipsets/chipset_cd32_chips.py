"""
X-Seti June15 2025 - Amiga CD32 Chipset Definitions
Visual Retro System Emulator Builder - CD32 Game Console & MPEG Cart
"""

#this belongs in chipsets/chipset_cd32_chips.py

def add_cd32_chips(generator):
    """Add Amiga CD32 (32-bit game console) chipset components including MPEG cartridge"""
    
    # ============================================================================
    # CORE AGA CHIPSET (Advanced Graphics Architecture)
    # ============================================================================
    
    # Alice 8374 - AGA Graphics Chip (from A1200)
    generator.add_chip(
        name="Alice 8374",
        chip_id="cd32_alice",
        category="Video",
        description="Advanced Graphics Architecture (AGA) Alice Chip - Main graphics controller",
        package_types=["PLCC-84", "QFP-100"],
        pins=[
            # 32-bit Data Bus
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'D16'}, {'name': 'D17'}, {'name': 'D18'}, {'name': 'D19'},
            {'name': 'D20'}, {'name': 'D21'}, {'name': 'D22'}, {'name': 'D23'},
            {'name': 'D24'}, {'name': 'D25'}, {'name': 'D26'}, {'name': 'D27'},
            {'name': 'D28'}, {'name': 'D29'}, {'name': 'D30'}, {'name': 'D31'},
            # Address Bus
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'A21'}, 
            # Memory Control
            {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'},
            {'name': 'WE'}, {'name': 'OE'}, {'name': 'DMAL'}, 
            # Graphics Bus
            {'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'},
            {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'},
            {'name': 'RGA8'}, 
            # Clocks and Control
            {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': 'CDAC'},
            {'name': 'CSYNC'}, {'name': 'VSYNC'}, {'name': 'HSYNC'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDDQ'}, {'name': 'VSSQ'},
            {'name': 'VCC3'}, {'name': 'GND3'}, {'name': 'VREF'}
        ]
    )
    
    # Lisa 8375 - AGA Graphics Support Chip  
    generator.add_chip(
        name="Lisa 8375",
        chip_id="cd32_lisa",
        category="Custom",
        description="Advanced Graphics Architecture (AGA) Lisa Support Chip",
        package_types=["PLCC-68", "QFP-80"],
        pins=[
            # Graphics Bus Interface
            {'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'},
            {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'},
            {'name': 'RGA8'}, {'name': 'RGA9'}, {'name': 'RGA10'}, {'name': 'RGA11'},
            # Data Bus
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            # Memory Interface
            {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'RAS0'}, {'name': 'RAS1'},
            {'name': 'WE'}, {'name': 'OE'}, {'name': 'DRAM_CLK'},
            # AGA Control
            {'name': 'AGA_EN'}, {'name': 'BURST'}, {'name': 'FAST'}, {'name': 'SLOW'},
            # Video Interface
            {'name': 'BLANK'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'},
            # Clocks
            {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': '14MHZ'},
            # Power and Control
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'},
            {'name': 'RESET'}, {'name': 'TEST'}
        ]
    )
    
    # Paula 8364 - Enhanced for CD32
    generator.add_chip(
        name="Paula 8364 (CD32)",
        chip_id="cd32_paula",
        category="Audio",
        description="Enhanced Paula - Audio, I/O and CD32 controller interface",
        package_types=["DIP-48", "PLCC-48"],
        pins=[
            # Interrupt Control
            {'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'INT2'},
            {'name': 'INT3'}, {'name': 'INT6'}, {'name': 'CD32_INT'},
            # Address Bus
            {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'},
            {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'},
            # Data Bus
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            # Audio Output
            {'name': 'LEFT'}, {'name': 'RIGHT'}, {'name': 'AUDIO_CLK'},
            # CD32 Controller Interface
            {'name': 'JOY0_CLK'}, {'name': 'JOY0_LOAD'}, {'name': 'JOY0_DATA'},
            {'name': 'JOY1_CLK'}, {'name': 'JOY1_LOAD'}, {'name': 'JOY1_DATA'},
            # DMA and Clocks
            {'name': 'DMAL'}, {'name': 'DMAG'}, {'name': 'CCK'}, {'name': 'CCKQ'},
            {'name': 'XCLK'}, {'name': 'XCLKEN'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'},
            {'name': 'AVDD'}, {'name': 'AGND'}
        ]
    )
    
    # ============================================================================
    # CD32-SPECIFIC CHIPS
    # ============================================================================
    
    # Akiko - The heart of CD32 specific functionality
    generator.add_chip(
        name="Akiko 8421",
        chip_id="cd32_akiko",
        category="Custom",
        description="CD32 System Controller - CD-ROM, chunky-to-planar conversion, joypad interface",
        package_types=["PLCC-84", "QFP-100"],
        pins=[
            # CPU Interface
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'},
            {'name': 'CS'}, {'name': 'IRQ'}, {'name': 'RESET'}, {'name': 'CLK'},
            # CD-ROM Interface
            {'name': 'CD_D0'}, {'name': 'CD_D1'}, {'name': 'CD_D2'}, {'name': 'CD_D3'},
            {'name': 'CD_D4'}, {'name': 'CD_D5'}, {'name': 'CD_D6'}, {'name': 'CD_D7'},
            {'name': 'CD_CLK'}, {'name': 'CD_REQ'}, {'name': 'CD_ACK'}, {'name': 'CD_ATN'},
            {'name': 'CD_RST'}, {'name': 'CD_SEL'}, {'name': 'CD_BSY'}, {'name': 'CD_MSG'},
            {'name': 'CD_IO'}, {'name': 'CD_CMD'}, {'name': 'CD_SUBCODE'}, {'name': 'CD_AUDIO_L'},
            {'name': 'CD_AUDIO_R'}, {'name': 'CD_MUTE'},
            # Joypad Interface (CD32 Controllers)
            {'name': 'JOY0_CLK'}, {'name': 'JOY0_LOAD'}, {'name': 'JOY0_DATA'},
            {'name': 'JOY1_CLK'}, {'name': 'JOY1_LOAD'}, {'name': 'JOY1_DATA'},
            {'name': 'JOY_SHIFT_CLK'}, {'name': 'JOY_POWER'},
            # Chunky-to-Planar Interface  
            {'name': 'C2P_CLK'}, {'name': 'C2P_EN'}, {'name': 'C2P_BUSY'},
            {'name': 'CHUNKY_D0'}, {'name': 'CHUNKY_D1'}, {'name': 'CHUNKY_D2'}, {'name': 'CHUNKY_D3'},
            {'name': 'CHUNKY_D4'}, {'name': 'CHUNKY_D5'}, {'name': 'CHUNKY_D6'}, {'name': 'CHUNKY_D7'},
            # NVRAM Interface
            {'name': 'NVRAM_CS'}, {'name': 'NVRAM_CLK'}, {'name': 'NVRAM_DI'}, {'name': 'NVRAM_DO'},
            # Power and Test
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC_3V3'}, {'name': 'GND_3V3'},
            {'name': 'TEST'}, {'name': 'JTAG_TDI'}, {'name': 'JTAG_TDO'}, {'name': 'JTAG_TCK'}
        ]
    )
    
    # CD32 Audio DAC - 16-bit Stereo for CD Audio
    generator.add_chip(
        name="TDA1387 Audio DAC",
        chip_id="cd32_audio_dac",
        category="Audio",
        description="16-bit Stereo Audio DAC for CD32 audio output",
        package_types=["DIP-18", "SOIC-18"],
        pins=[
            # Digital Audio Interface
            {'name': 'WS'}, {'name': 'BCK'}, {'name': 'DATA'}, {'name': 'MUTE'},
            # Analog Outputs  
            {'name': 'OUTL+'}, {'name': 'OUTL-'}, {'name': 'OUTR+'}, {'name': 'OUTR-'},
            # Reference and Bias
            {'name': 'VREF'}, {'name': 'BIAS'}, {'name': 'FILT'},
            # Power Supply
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'},
            # Control
            {'name': 'RESET'}, {'name': 'TEST'}, {'name': 'FS0'}
        ]
    )
    
    # CD32 Joypad Controller Interface
    generator.add_chip(
        name="CD32 Joypad Controller",
        chip_id="cd32_joypad_controller",
        category="I/O",
        description="CD32 joypad interface controller with shift register support",
        package_types=["DIP-20", "SOIC-20"],
        pins=[
            # Joypad 0 Interface
            {'name': 'JOY0_UP'}, {'name': 'JOY0_DOWN'}, {'name': 'JOY0_LEFT'}, {'name': 'JOY0_RIGHT'},
            {'name': 'JOY0_RED'}, {'name': 'JOY0_BLUE'}, {'name': 'JOY0_GREEN'}, {'name': 'JOY0_YELLOW'},
            {'name': 'JOY0_FORWARD'}, {'name': 'JOY0_REVERSE'}, {'name': 'JOY0_PLAY'},
            # Joypad 1 Interface  
            {'name': 'JOY1_DATA'}, {'name': 'JOY1_CLK'}, {'name': 'JOY1_LOAD'},
            # Serial Interface to Akiko
            {'name': 'SERIAL_CLK'}, {'name': 'SERIAL_LOAD'}, {'name': 'SERIAL_DATA'},
            # Power and Control
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'RESET'}
        ]
    )
    
    # ============================================================================
    # MPEG CARTRIDGE (FMV - Full Motion Video)
    # ============================================================================
    
    # CL450 MPEG Video Decoder - The heart of the MPEG cart
    generator.add_chip(
        name="CL450 MPEG Decoder",
        chip_id="cd32_mpeg_cl450",
        category="Video",
        description="C-Cube CL450 MPEG-1 Video Decoder for Full Motion Video",
        package_types=["PLCC-84", "QFP-100"],
        pins=[
            # Host Interface (to CD32)
            {'name': 'HD0'}, {'name': 'HD1'}, {'name': 'HD2'}, {'name': 'HD3'},
            {'name': 'HD4'}, {'name': 'HD5'}, {'name': 'HD6'}, {'name': 'HD7'},
            {'name': 'HD8'}, {'name': 'HD9'}, {'name': 'HD10'}, {'name': 'HD11'},
            {'name': 'HD12'}, {'name': 'HD13'}, {'name': 'HD14'}, {'name': 'HD15'},
            {'name': 'HA0'}, {'name': 'HA1'}, {'name': 'HA2'}, {'name': 'HA3'},
            {'name': 'HCS'}, {'name': 'HRD'}, {'name': 'HWR'}, {'name': 'HINT'},
            {'name': 'HRDY'}, {'name': 'HRST'},
            # DRAM Interface (MPEG buffer memory)
            {'name': 'MD0'}, {'name': 'MD1'}, {'name': 'MD2'}, {'name': 'MD3'},
            {'name': 'MD4'}, {'name': 'MD5'}, {'name': 'MD6'}, {'name': 'MD7'},
            {'name': 'MD8'}, {'name': 'MD9'}, {'name': 'MD10'}, {'name': 'MD11'},
            {'name': 'MD12'}, {'name': 'MD13'}, {'name': 'MD14'}, {'name': 'MD15'},
            {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'}, {'name': 'MA3'},
            {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'}, {'name': 'MA7'},
            {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'}, {'name': 'MA11'},
            {'name': 'MRAS'}, {'name': 'MCAS'}, {'name': 'MWE'}, {'name': 'MOE'},
            # Video Output Interface
            {'name': 'Y0'}, {'name': 'Y1'}, {'name': 'Y2'}, {'name': 'Y3'},
            {'name': 'Y4'}, {'name': 'Y5'}, {'name': 'Y6'}, {'name': 'Y7'},
            {'name': 'U0'}, {'name': 'U1'}, {'name': 'U2'}, {'name': 'U3'},
            {'name': 'U4'}, {'name': 'U5'}, {'name': 'U6'}, {'name': 'U7'},
            {'name': 'V0'}, {'name': 'V1'}, {'name': 'V2'}, {'name': 'V3'},
            {'name': 'V4'}, {'name': 'V5'}, {'name': 'V6'}, {'name': 'V7'},
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'PIXEL_CLK'},
            # Control and Clocks
            {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'PLL_VDD'}, {'name': 'PLL_VSS'},
            {'name': 'RESET'}, {'name': 'TEST'}, {'name': 'IRQ_OUT'},
            # Power
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'}
        ]
    )
    
    # CL480 Video Controller - MPEG cart video timing and control
    generator.add_chip(
        name="CL480 Video Controller",
        chip_id="cd32_mpeg_cl480",
        category="Video",
        description="C-Cube CL480 Video Timing Controller for MPEG playback",
        package_types=["PLCC-68", "QFP-80"],
        pins=[
            # Video Input from CL450
            {'name': 'Y_IN0'}, {'name': 'Y_IN1'}, {'name': 'Y_IN2'}, {'name': 'Y_IN3'},
            {'name': 'Y_IN4'}, {'name': 'Y_IN5'}, {'name': 'Y_IN6'}, {'name': 'Y_IN7'},
            {'name': 'U_IN0'}, {'name': 'U_IN1'}, {'name': 'U_IN2'}, {'name': 'U_IN3'},
            {'name': 'U_IN4'}, {'name': 'U_IN5'}, {'name': 'U_IN6'}, {'name': 'U_IN7'},
            {'name': 'V_IN0'}, {'name': 'V_IN1'}, {'name': 'V_IN2'}, {'name': 'V_IN3'},
            {'name': 'V_IN4'}, {'name': 'V_IN5'}, {'name': 'V_IN6'}, {'name': 'V_IN7'},
            # RGB Video Output
            {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'},
            {'name': 'R4'}, {'name': 'R5'}, {'name': 'R6'}, {'name': 'R7'},
            {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'},
            {'name': 'G4'}, {'name': 'G5'}, {'name': 'G6'}, {'name': 'G7'},
            {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'},
            {'name': 'B4'}, {'name': 'B5'}, {'name': 'B6'}, {'name': 'B7'},
            # Sync Signals
            {'name': 'HSYNC_IN'}, {'name': 'VSYNC_IN'}, {'name': 'BLANK_IN'},
            {'name': 'HSYNC_OUT'}, {'name': 'VSYNC_OUT'}, {'name': 'BLANK_OUT'},
            {'name': 'PIXEL_CLK'}, {'name': 'LINE_CLK'},
            # Control Interface
            {'name': 'MODE0'}, {'name': 'MODE1'}, {'name': 'MODE2'}, {'name': 'ENABLE'},
            {'name': 'OVERLAY'}, {'name': 'KEYING'}, {'name': 'ALPHA'},
            # Power
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'}
        ]
    )
    
    # MPEG Cart DRAM Controller - Manages video buffer memory
    generator.add_chip(
        name="MPEG DRAM Controller",
        chip_id="cd32_mpeg_dram_controller",
        category="Memory",
        description="DRAM controller for MPEG video buffer memory",
        package_types=["PLCC-52", "QFP-64"],
        pins=[
            # DRAM Interface
            {'name': 'MD0'}, {'name': 'MD1'}, {'name': 'MD2'}, {'name': 'MD3'},
            {'name': 'MD4'}, {'name': 'MD5'}, {'name': 'MD6'}, {'name': 'MD7'},
            {'name': 'MD8'}, {'name': 'MD9'}, {'name': 'MD10'}, {'name': 'MD11'},
            {'name': 'MD12'}, {'name': 'MD13'}, {'name': 'MD14'}, {'name': 'MD15'},
            {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'}, {'name': 'MA3'},
            {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'}, {'name': 'MA7'},
            {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'}, {'name': 'MA11'},
            {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'},
            {'name': 'WE'}, {'name': 'OE'}, {'name': 'REFRESH'}, {'name': 'CLK'},
            # CL450 Interface
            {'name': 'CL450_REQ'}, {'name': 'CL450_ACK'}, {'name': 'CL450_BUSY'},
            # Control
            {'name': 'CS'}, {'name': 'RESET'}, {'name': 'IRQ'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # MPEG Cart Interface Controller - Connects cart to CD32
    generator.add_chip(
        name="MPEG Cart Interface",
        chip_id="cd32_mpeg_interface",
        category="I/O",
        description="Interface controller between MPEG cartridge and CD32 system",
        package_types=["PLCC-44", "QFP-48"],
        pins=[
            # CD32 System Interface
            {'name': 'CD32_D0'}, {'name': 'CD32_D1'}, {'name': 'CD32_D2'}, {'name': 'CD32_D3'},
            {'name': 'CD32_D4'}, {'name': 'CD32_D5'}, {'name': 'CD32_D6'}, {'name': 'CD32_D7'},
            {'name': 'CD32_D8'}, {'name': 'CD32_D9'}, {'name': 'CD32_D10'}, {'name': 'CD32_D11'},
            {'name': 'CD32_D12'}, {'name': 'CD32_D13'}, {'name': 'CD32_D14'}, {'name': 'CD32_D15'},
            {'name': 'CD32_A0'}, {'name': 'CD32_A1'}, {'name': 'CD32_A2'}, {'name': 'CD32_A3'},
            {'name': 'CD32_CS'}, {'name': 'CD32_RD'}, {'name': 'CD32_WR'}, {'name': 'CD32_IRQ'},
            # MPEG Chip Interface
            {'name': 'MPEG_CS'}, {'name': 'MPEG_RD'}, {'name': 'MPEG_WR'}, {'name': 'MPEG_IRQ'},
            {'name': 'MPEG_READY'}, {'name': 'MPEG_BUSY'},
            # Video Control
            {'name': 'VIDEO_EN'}, {'name': 'OVERLAY_EN'}, {'name': 'KEYING_EN'},
            # Power and Control
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'RESET'}, {'name': 'CLK'}
        ]
    )
    
    # ============================================================================
    # ADDITIONAL CD32 SYSTEM CHIPS
    # ============================================================================
    
    # CD32 RF Modulator - TV output
    generator.add_chip(
        name="CD32 RF Modulator",
        chip_id="cd32_rf_modulator",
        category="Video",
        description="RF modulator for TV output (PAL/NTSC)",
        package_types=["DIP-16", "SOIC-16"],
        pins=[
            # Video Input
            {'name': 'CVBS_IN'}, {'name': 'Y_IN'}, {'name': 'C_IN'}, {'name': 'RGB_R'},
            {'name': 'RGB_G'}, {'name': 'RGB_B'}, {'name': 'SYNC'},
            # Audio Input
            {'name': 'AUDIO_L'}, {'name': 'AUDIO_R'},
            # RF Output
            {'name': 'RF_OUT'}, {'name': 'RF_GND'},
            # Control
            {'name': 'CH_SEL'}, {'name': 'PAL_NTSC'}, {'name': 'ENABLE'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # CD32 Power Management
    generator.add_chip(
        name="CD32 Power Controller",
        chip_id="cd32_power_controller",
        category="Power",
        description="Power management and reset controller for CD32 system",
        package_types=["DIP-14", "SOIC-14"],
        pins=[
            # Power Input
            {'name': 'VIN'}, {'name': 'GND_IN'},
            # Regulated Outputs
            {'name': '5V_OUT'}, {'name': '3V3_OUT'}, {'name': '12V_OUT'}, {'name': '-12V_OUT'},
            # Control Inputs
            {'name': 'POWER_BTN'}, {'name': 'RESET_BTN'}, {'name': 'CD_POWER'},
            # System Control
            {'name': 'RESET_OUT'}, {'name': 'POWER_GOOD'}, {'name': 'STANDBY'},
            # Status
            {'name': 'LED_POWER'}, {'name': 'LED_ACTIVITY'}
        ]
    )

if __name__ == "__main__":
    # Test the CD32 chipset definitions
    print("Amiga CD32 chipset definitions loaded")
    print("Core AGA: Alice, Lisa, Paula (enhanced), Akiko")
    print("MPEG Cart: CL450, CL480, DRAM Controller, Interface")
    print("System: Audio DAC, Joypad Controller, RF Modulator, Power Management")
    print("Total chips: 12 + MPEG cartridge components")