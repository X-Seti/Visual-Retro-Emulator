"""
X-Seti June13 2025 - Microsoft Xbox Chipset Definitions
Visual Retro System Emulator Builder - Original Xbox Core Chips
"""

def add_xbox_original_chips(generator):
    """Add Microsoft Xbox (original) chipset components"""
    
    # Pentium III CPU - Main processor
    generator.add_chip(
        name="Pentium III 733MHz",
        chip_id="xbox_pentium3",
        category="Processor",
        description="Intel Pentium III CPU - Modified for Xbox",
        package_types=["FC-PGA370"],
        pins=[
            # Address Bus
            {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'},
            {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'},
            {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'},
            {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'},
            {'name': 'A19'}, {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'},
            {'name': 'A23'}, {'name': 'A24'}, {'name': 'A25'}, {'name': 'A26'},
            {'name': 'A27'}, {'name': 'A28'}, {'name': 'A29'}, {'name': 'A30'},
            {'name': 'A31'}, {'name': 'BE0'}, {'name': 'BE1'}, {'name': 'BE2'},
            {'name': 'BE3'}, {'name': 'ADS'}, {'name': 'REQ0'}, {'name': 'REQ1'},
            {'name': 'REQ2'}, {'name': 'REQ3'}, {'name': 'REQ4'}, {'name': 'GNT0'},
            {'name': 'GNT1'}, {'name': 'GNT2'}, {'name': 'GNT3'}, {'name': 'GNT4'},
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
            {'name': 'BCLK'}, {'name': 'RESET'}, {'name': 'INIT'}, {'name': 'NMI'},
            {'name': 'SMI'}, {'name': 'INTR'}, {'name': 'IGNNE'}, {'name': 'A20M'},
            {'name': 'FERR'}, {'name': 'BERR'}, {'name': 'BINIT'}, {'name': 'LINT0'},
            {'name': 'LINT1'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VTT'}
        ]
    )

    # nForce 420 - System chipset (MCPX)
    generator.add_chip(
        name="nForce 420 MCPX",
        chip_id="xbox_nforce420",
        category="Chipset",
        description="NVIDIA nForce 420 - Xbox Media Communications Processor",
        package_types=["BGA-352"],
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
            {'name': 'MRAS'}, {'name': 'MCAS'}, {'name': 'MWE'}, {'name': 'MOE'},
            # Audio
            {'name': 'AC97_SDATA_OUT'}, {'name': 'AC97_SDATA_IN'}, {'name': 'AC97_SYNC'},
            {'name': 'AC97_BIT_CLK'}, {'name': 'AC97_RESET'}, {'name': 'SPDIF_OUT'},
            # USB
            {'name': 'USB0_DP'}, {'name': 'USB0_DM'}, {'name': 'USB1_DP'}, {'name': 'USB1_DM'},
            {'name': 'USB2_DP'}, {'name': 'USB2_DM'}, {'name': 'USB3_DP'}, {'name': 'USB3_DM'},
            # IDE
            {'name': 'IDE_D0'}, {'name': 'IDE_D1'}, {'name': 'IDE_D2'}, {'name': 'IDE_D3'},
            {'name': 'IDE_D4'}, {'name': 'IDE_D5'}, {'name': 'IDE_D6'}, {'name': 'IDE_D7'},
            {'name': 'IDE_D8'}, {'name': 'IDE_D9'}, {'name': 'IDE_D10'}, {'name': 'IDE_D11'},
            {'name': 'IDE_D12'}, {'name': 'IDE_D13'}, {'name': 'IDE_D14'}, {'name': 'IDE_D15'},
            # Ethernet
            {'name': 'ETH_TXD0'}, {'name': 'ETH_TXD1'}, {'name': 'ETH_TXD2'}, {'name': 'ETH_TXD3'},
            {'name': 'ETH_RXD0'}, {'name': 'ETH_RXD1'}, {'name': 'ETH_RXD2'}, {'name': 'ETH_RXD3'},
            {'name': 'ETH_TX_EN'}, {'name': 'ETH_RX_DV'}, {'name': 'ETH_TX_CLK'}, {'name': 'ETH_RX_CLK'},
            # System
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VREF'}, {'name': 'NC'}
        ]
    )

    # GeForce 3 NV2A - Graphics processor
    generator.add_chip(
        name="GeForce 3 NV2A",
        chip_id="xbox_nv2a",
        category="Video",
        description="NVIDIA GeForce 3 NV2A - Xbox Graphics Processing Unit",
        package_types=["BGA-476"],
        pins=[
            # Memory Interface
            {'name': 'GMA0'}, {'name': 'GMA1'}, {'name': 'GMA2'}, {'name': 'GMA3'},
            {'name': 'GMA4'}, {'name': 'GMA5'}, {'name': 'GMA6'}, {'name': 'GMA7'},
            {'name': 'GMA8'}, {'name': 'GMA9'}, {'name': 'GMA10'}, {'name': 'GMA11'},
            {'name': 'GMA12'}, {'name': 'GMA13'}, {'name': 'GMA14'}, {'name': 'GMA15'},
            {'name': 'GMA16'}, {'name': 'GMA17'}, {'name': 'GMA18'}, {'name': 'GMA19'},
            {'name': 'GMA20'}, {'name': 'GMA21'}, {'name': 'GMA22'}, {'name': 'GMA23'},
            {'name': 'GMA24'}, {'name': 'GMA25'}, {'name': 'GMA26'}, {'name': 'GMA27'},
            {'name': 'GMA28'}, {'name': 'GMA29'}, {'name': 'GMA30'}, {'name': 'GMA31'},
            # Video Memory Data
            {'name': 'GMD0'}, {'name': 'GMD1'}, {'name': 'GMD2'}, {'name': 'GMD3'},
            {'name': 'GMD4'}, {'name': 'GMD5'}, {'name': 'GMD6'}, {'name': 'GMD7'},
            {'name': 'GMD8'}, {'name': 'GMD9'}, {'name': 'GMD10'}, {'name': 'GMD11'},
            {'name': 'GMD12'}, {'name': 'GMD13'}, {'name': 'GMD14'}, {'name': 'GMD15'},
            {'name': 'GMD16'}, {'name': 'GMD17'}, {'name': 'GMD18'}, {'name': 'GMD19'},
            {'name': 'GMD20'}, {'name': 'GMD21'}, {'name': 'GMD22'}, {'name': 'GMD23'},
            {'name': 'GMD24'}, {'name': 'GMD25'}, {'name': 'GMD26'}, {'name': 'GMD27'},
            {'name': 'GMD28'}, {'name': 'GMD29'}, {'name': 'GMD30'}, {'name': 'GMD31'},
            # Video Output
            {'name': 'DAC_R0'}, {'name': 'DAC_R1'}, {'name': 'DAC_R2'}, {'name': 'DAC_R3'},
            {'name': 'DAC_R4'}, {'name': 'DAC_R5'}, {'name': 'DAC_R6'}, {'name': 'DAC_R7'},
            {'name': 'DAC_G0'}, {'name': 'DAC_G1'}, {'name': 'DAC_G2'}, {'name': 'DAC_G3'},
            {'name': 'DAC_G4'}, {'name': 'DAC_G5'}, {'name': 'DAC_G6'}, {'name': 'DAC_G7'},
            {'name': 'DAC_B0'}, {'name': 'DAC_B1'}, {'name': 'DAC_B2'}, {'name': 'DAC_B3'},
            {'name': 'DAC_B4'}, {'name': 'DAC_B5'}, {'name': 'DAC_B6'}, {'name': 'DAC_B7'},
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'PCLK'},
            # System
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVCC'}, {'name': 'AGND'}
        ]
    )

    # Xbox System Management Controller (SMC)
    generator.add_chip(
        name="SMC PIC16LC63A",
        chip_id="xbox_smc",
        category="Custom",
        description="System Management Controller - Power, thermal, LED control",
        package_types=["SOIC-28"],
        pins=[
            {'name': 'RA0'}, {'name': 'RA1'}, {'name': 'RA2'}, {'name': 'RA3'},
            {'name': 'RA4'}, {'name': 'RA5'}, {'name': 'RB0'}, {'name': 'RB1'},
            {'name': 'RB2'}, {'name': 'RB3'}, {'name': 'RB4'}, {'name': 'RB5'},
            {'name': 'RB6'}, {'name': 'RB7'}, {'name': 'RC0'}, {'name': 'RC1'},
            {'name': 'RC2'}, {'name': 'RC3'}, {'name': 'RC4'}, {'name': 'RC5'},
            {'name': 'RC6'}, {'name': 'RC7'}, {'name': 'MCLR'}, {'name': 'OSC1'},
            {'name': 'OSC2'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'NC'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Microsoft Xbox chipset definitions loaded")
    print("Available chips: Pentium III, nForce 420, GeForce 3 NV2A, SMC")
