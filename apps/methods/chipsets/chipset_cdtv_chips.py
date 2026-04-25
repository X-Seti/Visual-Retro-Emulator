"""
X-Seti June15 2025 - Commodore CDTV Chipset Definitions
Visual Retro System Emulator Builder - CDTV Multimedia System Chips
"""

#this belongs in chipsets/chipset_cdtv_chips.py

def add_cdtv_chips(generator):
    """Add Commodore CDTV (Commodore Dynamic Total Vision) chipset components"""
    
    # ============================================================================
    # CORE AMIGA CHIPSET (OCS - Original Chip Set)
    # ============================================================================
    
    # Agnus 8370 - Address Generator Unit (CDTV uses 8370 revision)
    generator.add_chip(
        name="Agnus 8370",
        chip_id="cdtv_agnus",
        category="Custom",
        description="Address Generator Unit (Agnus) - DMA Controller and Memory Management for CDTV",
        package_types=["DIP-84", "PLCC-84"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'},
            {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'},
            {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'},
            {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'},
            {'name': 'D15'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'},
            {'name': 'DTACK'}, {'name': 'OWN'}, {'name': 'BERR'}, {'name': 'HALT'},
            {'name': 'RESET'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': 'C1'},
            {'name': 'C3'}, {'name': 'CDAC'}, {'name': 'CSYNC'}, {'name': 'VSYNC'},
            {'name': 'HSYNC'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'},
            {'name': 'CAS1'}, {'name': 'WE'}, {'name': 'DMAL'}, {'name': 'DMAG'},
            {'name': 'DMAS'}, {'name': 'DKRD'}, {'name': 'DKWD'}, {'name': 'INT2'},
            {'name': 'INT6'}, {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'BCLK'},
            {'name': 'BDIR'}, {'name': '7MHZ'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VDDQ'}, {'name': 'VSSQ'}
        ]
    )
    
    # Paula 8364 - Ports, Audio, UART, and Logic
    generator.add_chip(
        name="Paula 8364",
        chip_id="cdtv_paula",
        category="Audio",
        description="Ports, Audio, UART, and Logic (Paula) - Enhanced for CDTV multimedia",
        package_types=["DIP-48", "PLCC-48"],
        pins=[
            {'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'INT2'},
            {'name': 'INT3'}, {'name': 'INT6'}, {'name': 'A1'}, {'name': 'A2'},
            {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'},
            {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'},
            {'name': 'A11'}, {'name': 'A12'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'},
            {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'},
            {'name': 'D14'}, {'name': 'D15'}, {'name': 'CCK'}, {'name': 'CCKQ'},
            {'name': 'DMAL'}, {'name': 'DMAG'}, {'name': 'LEFT'}, {'name': 'RIGHT'},
            {'name': 'LPEN'}, {'name': 'LPENCLK'}, {'name': 'XCLK'}, {'name': 'XCLKEN'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'},
            {'name': 'AVDD'}, {'name': 'AGND'}
        ]
    )
    
    # Denise 8362 - Display Enable (Original CDTV version)
    generator.add_chip(
        name="Denise 8362",
        chip_id="cdtv_denise",
        category="Video",
        description="Display Enable (Denise) - Video Output and Sprite Control for CDTV",
        package_types=["DIP-48", "PLCC-48"],
        pins=[
            {'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'},
            {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'},
            {'name': 'RGA8'}, {'name': 'RGA9'}, {'name': 'DMAL'}, {'name': 'DMA'},
            {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': 'CDAC'},
            {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'},
            {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'},
            {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'},
            {'name': 'I0'}, {'name': 'I1'}, {'name': 'I2'}, {'name': 'I3'},
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'}, {'name': 'BLANK'},
            {'name': 'LACE'}, {'name': 'DBLSCAN'}, {'name': 'HAM'}, {'name': 'EHB'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'},
            {'name': 'AVDD'}, {'name': 'AGND'}, {'name': 'VREF'}, {'name': 'COMP'}
        ]
    )
    
    # ============================================================================
    # CDTV-SPECIFIC CUSTOM CHIPS
    # ============================================================================
    
    # CDTV Controller - Main CDTV System Controller
    generator.add_chip(
        name="CDTV Controller",
        chip_id="cdtv_controller",
        category="Custom",
        description="CDTV System Controller - CD-ROM interface and multimedia control",
        package_types=["PLCC-68", "QFP-80"],
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
            {'name': 'CD_DATA0'}, {'name': 'CD_DATA1'}, {'name': 'CD_DATA2'}, {'name': 'CD_DATA3'},
            {'name': 'CD_DATA4'}, {'name': 'CD_DATA5'}, {'name': 'CD_DATA6'}, {'name': 'CD_DATA7'},
            {'name': 'CD_CLK'}, {'name': 'CD_LRCK'}, {'name': 'CD_BCK'}, {'name': 'CD_REQ'},
            {'name': 'CD_ACK'}, {'name': 'CD_ATN'}, {'name': 'CD_RST'}, {'name': 'CD_MSG'},
            {'name': 'CD_IO'}, {'name': 'CD_SEL'}, {'name': 'CD_BSY'}, {'name': 'CD_CMD'},
            # Audio Interface  
            {'name': 'AUDIO_L'}, {'name': 'AUDIO_R'}, {'name': 'AUDIO_CLK'}, {'name': 'AUDIO_EN'},
            # Control Interface
            {'name': 'REMOTE_IN'}, {'name': 'REMOTE_OUT'}, {'name': 'LED_POWER'}, {'name': 'LED_ACTIVITY'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC_5V'}, {'name': 'VCC_3V3'},
            {'name': 'GND_A'}, {'name': 'GND_D'}
        ]
    )
    
    # DMAC (DMA Controller) - Enhanced for CD-ROM
    generator.add_chip(
        name="CDTV DMAC",
        chip_id="cdtv_dmac",
        category="Custom", 
        description="Enhanced DMA Controller for CD-ROM data transfer",
        package_types=["PLCC-52", "QFP-64"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'},
            {'name': 'BR'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'DRQ0'},
            {'name': 'DRQ1'}, {'name': 'DRQ2'}, {'name': 'DRQ3'}, {'name': 'DACK0'},
            {'name': 'DACK1'}, {'name': 'DACK2'}, {'name': 'DACK3'}, {'name': 'TC'},
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'IRQ'}, {'name': 'CS'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # ============================================================================
    # AUDIO PROCESSING
    # ============================================================================
    
    # Audio DAC - 16-bit Stereo DAC for CD Audio
    generator.add_chip(
        name="PCM56 Audio DAC",
        chip_id="cdtv_audio_dac",
        category="Audio",
        description="16-bit Stereo Audio DAC for CD-quality sound output",
        package_types=["DIP-28", "SOIC-28"],
        pins=[
            # Digital Audio Interface
            {'name': 'DL0'}, {'name': 'DL1'}, {'name': 'DL2'}, {'name': 'DL3'},
            {'name': 'DL4'}, {'name': 'DL5'}, {'name': 'DL6'}, {'name': 'DL7'},
            {'name': 'DL8'}, {'name': 'DL9'}, {'name': 'DL10'}, {'name': 'DL11'},
            {'name': 'DL12'}, {'name': 'DL13'}, {'name': 'DL14'}, {'name': 'DL15'},
            {'name': 'DR0'}, {'name': 'DR1'}, {'name': 'DR2'}, {'name': 'DR3'},
            {'name': 'DR4'}, {'name': 'DR5'}, {'name': 'DR6'}, {'name': 'DR7'},
            {'name': 'BCK'}, {'name': 'LRCK'}, {'name': 'DATA'}, {'name': 'CLK'},
            # Analog Output
            {'name': 'AOUTL'}, {'name': 'AOUTR'}, {'name': 'VREF'}, {'name': 'AGND'},
            # Power and Control
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'}
        ]
    )
    
    # Audio Mixer - Combines Amiga audio with CD audio
    generator.add_chip(
        name="Audio Mixer",
        chip_id="cdtv_audio_mixer",
        category="Audio",
        description="Audio mixing chip for combining Amiga and CD audio sources",
        package_types=["DIP-16", "SOIC-16"],
        pins=[
            # Amiga Audio Input
            {'name': 'AMIGA_L'}, {'name': 'AMIGA_R'},
            # CD Audio Input
            {'name': 'CD_L'}, {'name': 'CD_R'},
            # Mixed Output
            {'name': 'OUT_L'}, {'name': 'OUT_R'},
            # Control
            {'name': 'MIX_CTL0'}, {'name': 'MIX_CTL1'}, {'name': 'MIX_CTL2'}, {'name': 'MUTE'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'AVCC'}, {'name': 'AGND'}
        ]
    )
    
    # ============================================================================
    # CD-ROM SUBSYSTEM
    # ============================================================================
    
    # CD-ROM Controller - Sony/Philips compatible
    generator.add_chip(
        name="CXD1199Q CD Controller",
        chip_id="cdtv_cd_controller",
        category="Storage",
        description="Sony CXD1199Q CD-ROM Controller for CDTV drive interface",
        package_types=["QFP-80", "PLCC-84"],
        pins=[
            # Host Interface
            {'name': 'HD0'}, {'name': 'HD1'}, {'name': 'HD2'}, {'name': 'HD3'},
            {'name': 'HD4'}, {'name': 'HD5'}, {'name': 'HD6'}, {'name': 'HD7'},
            {'name': 'HA0'}, {'name': 'HA1'}, {'name': 'HA2'}, {'name': 'HA3'},
            {'name': 'HCS'}, {'name': 'HRD'}, {'name': 'HWR'}, {'name': 'HINT'},
            {'name': 'HRDY'}, {'name': 'HRST'}, {'name': 'HCLK'},
            # RF Interface
            {'name': 'RF+'}, {'name': 'RF-'}, {'name': 'TE'}, {'name': 'FE'},
            {'name': 'AS'}, {'name': 'MIRR'}, {'name': 'XTAL1'}, {'name': 'XTAL2'},
            # Servo Interface
            {'name': 'TRO'}, {'name': 'TRO_N'}, {'name': 'FOO'}, {'name': 'FOO_N'},
            {'name': 'SL'}, {'name': 'SL_N'}, {'name': 'SO'}, {'name': 'SO_N'},
            {'name': 'SLED+'}, {'name': 'SLED-'}, {'name': 'FOCUS+'}, {'name': 'FOCUS-'},
            # Motor Control
            {'name': 'CLV'}, {'name': 'CAV'}, {'name': 'BRAKE'}, {'name': 'DISC'},
            # Digital Audio
            {'name': 'SDATA'}, {'name': 'SLRCK'}, {'name': 'SBCK'}, {'name': 'SCKI'},
            # Control
            {'name': 'SENS0'}, {'name': 'SENS1'}, {'name': 'SENS2'}, {'name': 'DOOR'},
            {'name': 'EJECT'}, {'name': 'PLAY'}, {'name': 'STOP'}, {'name': 'PAUSE'},
            # Power
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # CD Signal Processor
    generator.add_chip(
        name="CXD2500Q Signal Processor",
        chip_id="cdtv_cd_signal_processor",
        category="Storage",
        description="Sony CXD2500Q CD Signal Processor and Error Correction",
        package_types=["QFP-100", "PLCC-100"],
        pins=[
            # RF Input
            {'name': 'RF_IN+'}, {'name': 'RF_IN-'}, {'name': 'AGC'}, {'name': 'SLICE'},
            # Digital Output
            {'name': 'EFM_DATA'}, {'name': 'EFM_CLK'}, {'name': 'SYNC'}, {'name': 'FRAME'},
            # Servo Control
            {'name': 'TE_OUT'}, {'name': 'FE_OUT'}, {'name': 'AS_OUT'}, {'name': 'MIRR_OUT'},
            # Host Interface  
            {'name': 'HOST_D0'}, {'name': 'HOST_D1'}, {'name': 'HOST_D2'}, {'name': 'HOST_D3'},
            {'name': 'HOST_D4'}, {'name': 'HOST_D5'}, {'name': 'HOST_D6'}, {'name': 'HOST_D7'},
            {'name': 'HOST_CS'}, {'name': 'HOST_RD'}, {'name': 'HOST_WR'}, {'name': 'HOST_INT'},
            # Audio Interface
            {'name': 'AUDIO_L'}, {'name': 'AUDIO_R'}, {'name': 'AUDIO_CLK'}, {'name': 'AUDIO_LRCK'},
            # Control
            {'name': 'MODE0'}, {'name': 'MODE1'}, {'name': 'MODE2'}, {'name': 'RESET'},
            {'name': 'TEST'}, {'name': 'CLK_IN'}, {'name': 'CLK_OUT'}, {'name': 'PLL_VCC'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'AVCC'}, {'name': 'AGND'},
            {'name': 'VDD'}, {'name': 'VSS'}
        ]
    )
    
    # ============================================================================
    # INTERFACE AND CONTROL
    # ============================================================================
    
    # Remote Control Interface
    generator.add_chip(
        name="Remote Control Interface",
        chip_id="cdtv_remote_interface",
        category="I/O",
        description="Infrared remote control receiver and decoder",
        package_types=["DIP-18", "SOIC-18"],
        pins=[
            # IR Input
            {'name': 'IR_IN'}, {'name': 'IR_GND'}, {'name': 'IR_VCC'},
            # Decoded Output
            {'name': 'DATA_OUT'}, {'name': 'CLOCK_OUT'}, {'name': 'VALID'}, {'name': 'IRQ'},
            # Host Interface
            {'name': 'HOST_D0'}, {'name': 'HOST_D1'}, {'name': 'HOST_D2'}, {'name': 'HOST_D3'},
            {'name': 'HOST_CS'}, {'name': 'HOST_RD'}, {'name': 'HOST_WR'},
            # Control
            {'name': 'RESET'}, {'name': 'ENABLE'}, {'name': 'CLK'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # Front Panel Controller
    generator.add_chip(
        name="Front Panel Controller",
        chip_id="cdtv_front_panel",
        category="I/O",
        description="Front panel LED and button controller",
        package_types=["DIP-20", "SOIC-20"],
        pins=[
            # Button Inputs
            {'name': 'POWER_BTN'}, {'name': 'EJECT_BTN'}, {'name': 'PLAY_BTN'}, {'name': 'STOP_BTN'},
            {'name': 'PAUSE_BTN'}, {'name': 'FWD_BTN'}, {'name': 'REW_BTN'},
            # LED Outputs
            {'name': 'POWER_LED'}, {'name': 'ACTIVITY_LED'}, {'name': 'PLAY_LED'}, {'name': 'PAUSE_LED'},
            # Host Interface
            {'name': 'HOST_D0'}, {'name': 'HOST_D1'}, {'name': 'HOST_D2'}, {'name': 'HOST_D3'},
            {'name': 'HOST_CS'}, {'name': 'HOST_RD'}, {'name': 'HOST_WR'}, {'name': 'HOST_IRQ'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # ============================================================================
    # MEMORY CONTROLLERS  
    # ============================================================================
    
    # Extended Memory Controller - For additional CDTV RAM
    generator.add_chip(
        name="Extended Memory Controller",
        chip_id="cdtv_memory_controller",
        category="Memory",
        description="Extended memory controller for CDTV additional RAM expansion",
        package_types=["PLCC-52", "QFP-64"],
        pins=[
            # Address Bus
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            # Data Bus
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            # DRAM Control
            {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'},
            {'name': 'WE'}, {'name': 'OE'}, {'name': 'REFRESH'}, {'name': 'CLK'},
            # Control
            {'name': 'CS'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'},
            {'name': 'DTACK'}, {'name': 'RESET'},
            # Power
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

if __name__ == "__main__":
    # Test the CDTV chipset definitions
    print("CDTV chipset definitions loaded")
    print("Chips included: Core Amiga OCS, CDTV Controller, CD-ROM subsystem, Audio processing")
    print("Multimedia features: CD Audio, Remote Control, Front Panel, Extended Memory")