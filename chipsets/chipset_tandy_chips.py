"""
X-Seti June13 2025 - Tandy/Radio Shack Chipset Definitions
Visual Retro System Emulator Builder - TRS-80 and Tandy Core Chips
"""

def add_tandy_coco_chips(generator):
    """Add Tandy Color Computer (CoCo) chipset components"""
    
    # SAM - Synchronous Address Multiplexer
    generator.add_chip(
        name="SAM MC6883",
        chip_id="tandy_sam",
        category="Custom", 
        description="Synchronous Address Multiplexer for Tandy CoCo",
        package_types=["DIP-40"],
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
        chip_id="tandy_vdg",
        category="Video",
        description="Video Display Generator for Tandy CoCo",
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

    # PIA - Peripheral Interface Adapter
    generator.add_chip(
        name="PIA MC6821",
        chip_id="tandy_pia",
        category="I/O",
        description="Peripheral Interface Adapter for Tandy CoCo",
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

    # 6809 CPU - Main processor
    generator.add_chip(
        name="CPU MC6809",
        chip_id="tandy_6809",
        category="Processor",
        description="Motorola 6809 CPU for Tandy CoCo",
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

def add_tandy_1000_chips(generator):
    """Add Tandy 1000 PC-compatible chipset components"""
    
    # Video Gate Array - Tandy graphics
    generator.add_chip(
        name="Tandy Video GA",
        chip_id="tandy1000_video_ga",
        category="Video",
        description="Tandy 1000 Video Gate Array - Enhanced CGA graphics",
        package_types=["PLCC-68"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RED0'}, {'name': 'RED1'}, {'name': 'RED2'}, {'name': 'RED3'},
            {'name': 'GREEN0'}, {'name': 'GREEN1'}, {'name': 'GREEN2'}, {'name': 'GREEN3'},
            {'name': 'BLUE0'}, {'name': 'BLUE1'}, {'name': 'BLUE2'}, {'name': 'BLUE3'},
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'BORDER'},
            {'name': 'DCLK'}, {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'WE'},
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'ALE'},
            {'name': 'INT'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VDD'}, {'name': 'VSS'},
            {'name': 'NC1'}, {'name': 'NC2'}, {'name': 'NC3'}, {'name': 'NC4'},
            {'name': 'NC5'}, {'name': 'NC6'}, {'name': 'NC7'}, {'name': 'NC8'},
            {'name': 'NC9'}, {'name': 'NC10'}, {'name': 'NC11'}, {'name': 'NC12'}
        ]
    )

    # Sound Chip - SN76496 compatible
    generator.add_chip(
        name="SN76496 PSG",
        chip_id="tandy1000_sn76496",
        category="Audio",
        description="Programmable Sound Generator for Tandy 1000",
        package_types=["DIP-16"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'WE'}, {'name': 'CE'}, {'name': 'READY'}, {'name': 'CLOCK'},
            {'name': 'AUDIO'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # 8088 CPU - Main processor
    generator.add_chip(
        name="CPU 8088",
        chip_id="tandy1000_8088",
        category="Processor",
        description="Intel 8088 CPU for Tandy 1000",
        package_types=["DIP-40"],
        pins=[
            {'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'},
            {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'SS0'}, {'name': 'MN/MX'}, {'name': 'RD'}, {'name': 'HOLD'},
            {'name': 'HLDA'}, {'name': 'WR'}, {'name': 'M/IO'}, {'name': 'DT/R'},
            {'name': 'DEN'}, {'name': 'ALE'}, {'name': 'INTA'}, {'name': 'INTR'},
            {'name': 'CLK'}, {'name': 'RESET'}, {'name': 'READY'}, {'name': 'TEST'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VBB'}, {'name': 'NC'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Tandy chipset definitions loaded")
    print("CoCo chips: SAM, VDG, PIA, 6809")
    print("Tandy 1000 chips: Video GA, SN76496, 8088")
