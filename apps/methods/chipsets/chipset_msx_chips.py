"""
X-Seti June13 2025 - MSX Chipset Definitions
Visual Retro System Emulator Builder - MSX Core Chips
"""

def add_msx_chips(generator):
    """Add MSX chipset components"""
    
    # TMS9918A - Video Display Processor
    generator.add_chip(
        name="TMS9918A",
        chip_id="msx_tms9918a",
        category="Video",
        description="Video Display Processor for MSX",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'},
            {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'},
            {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'AD8'}, {'name': 'AD9'},
            {'name': 'AD10'}, {'name': 'AD11'}, {'name': 'AD12'}, {'name': 'AD13'},
            {'name': 'CD0'}, {'name': 'CD1'}, {'name': 'CD2'}, {'name': 'CD3'},
            {'name': 'CD4'}, {'name': 'CD5'}, {'name': 'CD6'}, {'name': 'CD7'},
            {'name': 'MODE'}, {'name': 'CSW'}, {'name': 'CSR'}, {'name': 'INT'},
            {'name': 'GROMCLK'}, {'name': 'CPUCLK'}, {'name': 'XTAL1'}, {'name': 'XTAL2'},
            {'name': 'Y'}, {'name': 'RY'}, {'name': 'R'}, {'name': 'G'},
            {'name': 'B'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}
        ]
    )

    # AY-3-8910 - Programmable Sound Generator
    generator.add_chip(
        name="AY-3-8910",
        chip_id="msx_ay3_8910",
        category="Audio",
        description="Programmable Sound Generator for MSX",
        package_types=["DIP-28", "DIP-40"],
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

    # S1985 - MSX Engine (MSX2+)
    generator.add_chip(
        name="S1985 MSX Engine",
        chip_id="msx_s1985",
        category="Custom",
        description="MSX Engine - System controller for MSX2+",
        package_types=["DIP-64", "QFP-64"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RD'}, {'name': 'WR'}, {'name': 'MREQ'}, {'name': 'IORQ'},
            {'name': 'M1'}, {'name': 'RFSH'}, {'name': 'HALT'}, {'name': 'BUSREQ'},
            {'name': 'BUSACK'}, {'name': 'WAIT'}, {'name': 'INT'}, {'name': 'NMI'},
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'SLOT0'}, {'name': 'SLOT1'},
            {'name': 'SLOT2'}, {'name': 'SLOT3'}, {'name': 'SLTSL0'}, {'name': 'SLTSL1'},
            {'name': 'SLTSL2'}, {'name': 'SLTSL3'}, {'name': 'RAMENB'}, {'name': 'RAMDIS'},
            {'name': 'KANJI'}, {'name': 'CAPS'}, {'name': 'KANA'}, {'name': 'VDP'},
            {'name': 'PSG'}, {'name': 'PPI'}, {'name': 'RTC'}, {'name': 'PRINTER'},
            {'name': 'RS232'}, {'name': 'MODEM'}, {'name': 'MIDI'}, {'name': 'MOUSE'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

    # PPI 8255 - Programmable Peripheral Interface
    generator.add_chip(
        name="PPI 8255",
        chip_id="msx_ppi_8255",
        category="I/O",
        description="Programmable Peripheral Interface - Keyboard and joystick controller",
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

    # V9938 - Video Display Processor (MSX2)
    generator.add_chip(
        name="V9938 VDP",
        chip_id="msx_v9938",
        category="Video",
        description="Video Display Processor for MSX2",
        package_types=["DIP-64", "QFP-64"],
        pins=[
            {'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'},
            {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'},
            {'name': 'AD8'}, {'name': 'AD9'}, {'name': 'AD10'}, {'name': 'AD11'},
            {'name': 'AD12'}, {'name': 'AD13'}, {'name': 'AD14'}, {'name': 'AD15'},
            {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'WE'}, {'name': 'OE'},
            {'name': 'CD0'}, {'name': 'CD1'}, {'name': 'CD2'}, {'name': 'CD3'},
            {'name': 'CD4'}, {'name': 'CD5'}, {'name': 'CD6'}, {'name': 'CD7'},
            {'name': 'MODE'}, {'name': 'CSW'}, {'name': 'CSR'}, {'name': 'INT'},
            {'name': 'WAIT'}, {'name': 'RESET'}, {'name': 'XTAL1'}, {'name': 'XTAL2'},
            {'name': 'CPUCLK'}, {'name': 'DHCLK'}, {'name': 'DLCLK'}, {'name': 'R'},
            {'name': 'G'}, {'name': 'B'}, {'name': 'Y'}, {'name': 'S'},
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'COLORCLK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'},
            {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VREF'}, {'name': 'COMP'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("MSX chipset definitions loaded")
    print("Available chips: TMS9918A, AY-3-8910, S1985, PPI 8255, V9938")