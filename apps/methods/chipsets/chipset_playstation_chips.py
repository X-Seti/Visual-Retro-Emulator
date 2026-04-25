"""
X-Seti June13 2025 - Sony PlayStation Chipset Definitions
Visual Retro System Emulator Builder - PlayStation 1 Core Chips
"""

def add_playstation_1_chips(generator):
    """Add Sony PlayStation 1 chipset components"""
    
    # CPU - R3000A RISC processor
    generator.add_chip(
        name="R3000A CPU",
        chip_id="psx_r3000a",
        category="Processor",
        description="32-bit RISC CPU - Main processor for PlayStation",
        package_types=["PGA-179", "QFP-208"],
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
            # Control Signals
            {'name': 'READ'}, {'name': 'WRITE'}, {'name': 'AS'}, {'name': 'DS'},
            {'name': 'INT0'}, {'name': 'INT1'}, {'name': 'INT2'}, {'name': 'INT3'},
            {'name': 'INT4'}, {'name': 'INT5'}, {'name': 'NMI'}, {'name': 'RESET'},
            {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'},
            {'name': 'VSS'}, {'name': 'VREF'}, {'name': 'TEST'}, {'name': 'NC'}
        ]
    )

    # GPU - Graphics Processing Unit
    generator.add_chip(
        name="GPU CXD8514Q",
        chip_id="psx_gpu",
        category="Video",
        description="Graphics Processing Unit - 2D/3D graphics acceleration",
        package_types=["QFP-208"],
        pins=[
            # Video RAM Interface
            {'name': 'VRA0'}, {'name': 'VRA1'}, {'name': 'VRA2'}, {'name': 'VRA3'},
            {'name': 'VRA4'}, {'name': 'VRA5'}, {'name': 'VRA6'}, {'name': 'VRA7'},
            {'name': 'VRA8'}, {'name': 'VRA9'}, {'name': 'VRA10'}, {'name': 'VRA11'},
            {'name': 'VRA12'}, {'name': 'VRA13'}, {'name': 'VRA14'}, {'name': 'VRA15'},
            {'name': 'VRA16'}, {'name': 'VRA17'}, {'name': 'VRA18'}, {'name': 'VRA19'},
            # Video RAM Data
            {'name': 'VRD0'}, {'name': 'VRD1'}, {'name': 'VRD2'}, {'name': 'VRD3'},
            {'name': 'VRD4'}, {'name': 'VRD5'}, {'name': 'VRD6'}, {'name': 'VRD7'},
            {'name': 'VRD8'}, {'name': 'VRD9'}, {'name': 'VRD10'}, {'name': 'VRD11'},
            {'name': 'VRD12'}, {'name': 'VRD13'}, {'name': 'VRD14'}, {'name': 'VRD15'},
            # Video Output
            {'name': 'RED0'}, {'name': 'RED1'}, {'name': 'RED2'}, {'name': 'RED3'},
            {'name': 'RED4'}, {'name': 'RED5'}, {'name': 'RED6'}, {'name': 'RED7'},
            {'name': 'GREEN0'}, {'name': 'GREEN1'}, {'name': 'GREEN2'}, {'name': 'GREEN3'},
            {'name': 'GREEN4'}, {'name': 'GREEN5'}, {'name': 'GREEN6'}, {'name': 'GREEN7'},
            {'name': 'BLUE0'}, {'name': 'BLUE1'}, {'name': 'BLUE2'}, {'name': 'BLUE3'},
            {'name': 'BLUE4'}, {'name': 'BLUE5'}, {'name': 'BLUE6'}, {'name': 'BLUE7'},
            # Sync Signals
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'FIELD'},
            # Control
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'INT'},
            {'name': 'DMA_REQ'}, {'name': 'DMA_ACK'}, {'name': 'CLK'}, {'name': 'RESET'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}
        ]
    )

    # SPU - Sound Processing Unit
    generator.add_chip(
        name="SPU CXD2922AQ",
        chip_id="psx_spu",
        category="Audio",
        description="Sound Processing Unit - 24-channel audio synthesis",
        package_types=["QFP-100"],
        pins=[
            # Sound RAM Interface
            {'name': 'SRA0'}, {'name': 'SRA1'}, {'name': 'SRA2'}, {'name': 'SRA3'},
            {'name': 'SRA4'}, {'name': 'SRA5'}, {'name': 'SRA6'}, {'name': 'SRA7'},
            {'name': 'SRA8'}, {'name': 'SRA9'}, {'name': 'SRA10'}, {'name': 'SRA11'},
            {'name': 'SRA12'}, {'name': 'SRA13'}, {'name': 'SRA14'}, {'name': 'SRA15'},
            {'name': 'SRA16'}, {'name': 'SRA17'}, {'name': 'SRA18'}, {'name': 'SRD0'},
            {'name': 'SRD1'}, {'name': 'SRD2'}, {'name': 'SRD3'}, {'name': 'SRD4'},
            {'name': 'SRD5'}, {'name': 'SRD6'}, {'name': 'SRD7'}, {'name': 'SRD8'},
            {'name': 'SRD9'}, {'name': 'SRD10'}, {'name': 'SRD11'}, {'name': 'SRD12'},
            {'name': 'SRD13'}, {'name': 'SRD14'}, {'name': 'SRD15'}, {'name': 'SRCS'},
            {'name': 'SROE'}, {'name': 'SRWE'}, {'name': 'SRRAS'}, {'name': 'SRCAS'},
            # Audio Output
            {'name': 'AOUT_L'}, {'name': 'AOUT_R'}, {'name': 'CD_L'}, {'name': 'CD_R'},
            # Control
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'INT'},
            {'name': 'DMA_REQ'}, {'name': 'DMA_ACK'}, {'name': 'CLK'}, {'name': 'RESET'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'AVCC'}, {'name': 'AGND'}
        ]
    )

    # MDEC - Motion Decoder
    generator.add_chip(
        name="MDEC CXD8530AQ",
        chip_id="psx_mdec",
        category="Video",
        description="Motion Decoder - MPEG video decompression",
        package_types=["QFP-100"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'D16'}, {'name': 'D17'}, {'name': 'D18'}, {'name': 'D19'},
            {'name': 'D20'}, {'name': 'D21'}, {'name': 'D22'}, {'name': 'D23'},
            {'name': 'D24'}, {'name': 'D25'}, {'name': 'D26'}, {'name': 'D27'},
            {'name': 'D28'}, {'name': 'D29'}, {'name': 'D30'}, {'name': 'D31'},
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'INT'},
            {'name': 'DMA_REQ'}, {'name': 'DMA_ACK'}, {'name': 'CLK'}, {'name': 'RESET'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}
        ]
    )

    # CD-ROM Controller
    generator.add_chip(
        name="CDROM Controller",
        chip_id="psx_cdrom",
        category="Storage",
        description="CD-ROM drive controller and interface",
        package_types=["QFP-80"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'INT'},
            {'name': 'SERVO'}, {'name': 'FOCUS'}, {'name': 'TRACKING'}, {'name': 'SLED'},
            {'name': 'SPINDLE'}, {'name': 'LASER'}, {'name': 'RF'}, {'name': 'EFM'},
            {'name': 'SUBQ'}, {'name': 'AUDIO_L'}, {'name': 'AUDIO_R'}, {'name': 'MUTE'},
            {'name': 'CLK'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Sony PlayStation 1 chipset definitions loaded")
    print("Available chips: R3000A CPU, GPU, SPU, MDEC, CD-ROM Controller")