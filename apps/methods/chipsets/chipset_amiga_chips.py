"""
X-Seti June13 2025 - Amiga Chipset Definitions
Visual Retro System Emulator Builder - Core Amiga Chips
"""

def add_amiga_chips(generator):
    """Add Commodore Amiga chipset components"""
    
    # Agnus/Fat Agnus - Address Generator Unit
    generator.add_chip(
        name="Agnus 8367/8372",
        chip_id="amiga_agnus",
        category="Custom",
        description="Address Generator Unit (Agnus) - DMA Controller and Memory Management",
        package_types=["DIP-84", "PLCC-84"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'},
            {'name': 'OWN'}, {'name': 'BERR'}, {'name': 'HALT'}, {'name': 'RESET'},
            {'name': 'CIAA'}, {'name': 'CIAB'}, {'name': 'EXPNCS'}, {'name': 'AUTOCONF'},
            {'name': '7MHZ'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': 'C1'},
            {'name': 'C3'}, {'name': 'CDAC'}, {'name': 'CSYNC'}, {'name': 'VSYNC'},
            {'name': 'HSYNC'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'},
            {'name': 'GND2'}, {'name': 'VDDQ'}, {'name': 'VSSQ'}, {'name': 'VREF'},
            {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'},
            {'name': 'WE'}, {'name': 'DMAL'}, {'name': 'DMAG'}, {'name': 'DMAS'},
            {'name': 'DKRD'}, {'name': 'DKWD'}, {'name': 'INT2'}, {'name': 'INT6'},
            {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'BCLK'}, {'name': 'BDIR'}
        ]
    )
    
    # Paula - Ports, Audio, UART, and Logic
    generator.add_chip(
        name="Paula 8364",
        chip_id="amiga_paula",
        category="Audio",
        description="Ports, Audio, UART, and Logic (Paula) - Audio and I/O Controller",
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
    
    # Denise/Super Denise - Display Enable
    generator.add_chip(
        name="Denise 8362/8373",
        chip_id="amiga_denise",
        category="Video",
        description="Display Enable (Denise) - Video Output and Sprite Control",
        package_types=["DIP-48", "PLCC-48", "QFP-52"],
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
            {'name': 'BURST'}, {'name': 'GENLOCK'}, {'name': 'XCLK'}, {'name': 'XCLKEN'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )
    
    # Gary - Gate Array
    generator.add_chip(
        name="Gary 8365",
        chip_id="amiga_gary",
        category="Custom",
        description="Gate Array Logic Unit - System Control and Decoding",
        package_types=["PLCC-68", "QFP-68"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'},
            {'name': 'BR'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'IPL0'},
            {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'FC0'}, {'name': 'FC1'},
            {'name': 'FC2'}, {'name': 'BERR'}, {'name': 'HALT'}, {'name': 'RESET'},
            {'name': 'EXPAN'}, {'name': 'CIAA'}, {'name': 'CIAB'}, {'name': 'OVR'},
            {'name': 'KBRESET'}, {'name': 'POWER'}, {'name': 'LED'}, {'name': 'VCC'},
            {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VCC3'},
            {'name': 'GND3'}, {'name': 'VREF'}
        ]
    )
    
    # Alice - AGA Graphics Chip (A1200/A4000)
    generator.add_chip(
        name="Alice 8374",
        chip_id="amiga_alice",
        category="Video",
        description="Advanced Graphics Architecture (AGA) Alice Chip",
        package_types=["PLCC-84", "QFP-100"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'D16'}, {'name': 'D17'}, {'name': 'D18'}, {'name': 'D19'},
            {'name': 'D20'}, {'name': 'D21'}, {'name': 'D22'}, {'name': 'D23'},
            {'name': 'D24'}, {'name': 'D25'}, {'name': 'D26'}, {'name': 'D27'},
            {'name': 'D28'}, {'name': 'D29'}, {'name': 'D30'}, {'name': 'D31'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'A21'}, {'name': 'RAS0'}, {'name': 'RAS1'},
            {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'WE'}, {'name': 'OE'},
            {'name': 'DMAL'}, {'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'},
            {'name': 'RGA3'}, {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'},
            {'name': 'RGA7'}, {'name': 'RGA8'}, {'name': 'CCK'}, {'name': 'CCKQ'},
            {'name': '28MHZ'}, {'name': 'CDAC'}, {'name': 'CSYNC'}, {'name': 'VSYNC'},
            {'name': 'HSYNC'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDDQ'},
            {'name': 'VSSQ'}, {'name': 'VCC3'}, {'name': 'GND3'}, {'name': 'VREF'}
        ]
    )
    
    # Lisa - AGA Graphics Support Chip (A1200/A4000)
    generator.add_chip(
        name="Lisa 8375",
        chip_id="amiga_lisa",
        category="Custom",
        description="Advanced Graphics Architecture (AGA) Lisa Chip",
        package_types=["PLCC-68", "QFP-80"],
        pins=[
            {'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'},
            {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'},
            {'name': 'RGA8'}, {'name': 'RGA9'}, {'name': 'DMAL'}, {'name': 'DMA'},
            {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': 'CDAC'},
            {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'},
            {'name': 'R4'}, {'name': 'R5'}, {'name': 'R6'}, {'name': 'R7'},
            {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'},
            {'name': 'G4'}, {'name': 'G5'}, {'name': 'G6'}, {'name': 'G7'},
            {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'},
            {'name': 'B4'}, {'name': 'B5'}, {'name': 'B6'}, {'name': 'B7'},
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'}, {'name': 'BLANK'},
            {'name': 'BURST'}, {'name': 'GENLOCK'}, {'name': 'XCLK'}, {'name': 'XCLKEN'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )
    
    # Ramsey - RAM Controller (A3000/A4000)
    generator.add_chip(
        name="Ramsey 8372",
        chip_id="amiga_ramsey",
        category="Custom",
        description="RAM Controller and System Control",
        package_types=["PLCC-68", "QFP-80"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'RAS2'}, {'name': 'RAS3'},
            {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'CAS2'}, {'name': 'CAS3'},
            {'name': 'WE0'}, {'name': 'WE1'}, {'name': 'WE2'}, {'name': 'WE3'},
            {'name': 'OE'}, {'name': 'RAMEN'}, {'name': 'REFRESH'}, {'name': 'DRAM'},
            {'name': 'SRAM'}, {'name': 'ROM'}, {'name': 'FASTRAM'}, {'name': 'CHIPMEM'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )
    
    # Buster - Bus Controller (A2000)
    generator.add_chip(
        name="Buster 8364",
        chip_id="amiga_buster",
        category="Custom",
        description="Bus Controller and DMA Arbiter",
        package_types=["PLCC-52", "QFP-64"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'},
            {'name': 'BR'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'IPL0'},
            {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'FC0'}, {'name': 'FC1'},
            {'name': 'FC2'}, {'name': 'BERR'}, {'name': 'HALT'}, {'name': 'RESET'},
            {'name': 'EXPAN'}, {'name': 'AUTOCONF'}, {'name': 'BURST'}, {'name': 'SIZE0'},
            {'name': 'SIZE1'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'},
            {'name': 'GND2'}, {'name': 'VREF'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Amiga chipset definitions loaded")
    print("Available chips: Agnus, Paula, Denise, Gary, Alice, Lisa, Ramsey, Buster")
