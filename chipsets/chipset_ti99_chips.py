"""
X-Seti June13 2025 - Texas Instruments TI-99/4A Chipset Definitions
Visual Retro System Emulator Builder - TI-99/4A Core Chips
"""

def add_ti99_chips(generator):
    """Add Texas Instruments TI-99/4A chipset components"""
    
    # TMS9900 - 16-bit Microprocessor
    generator.add_chip(
        name="TMS9900 CPU",
        chip_id="ti99_tms9900",
        category="Processor",
        description="16-bit Microprocessor for TI-99/4A",
        package_types=["DIP-64", "QFP-64"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'CRUCLK'}, {'name': 'CRUOUT'}, {'name': 'CRUIN'}, {'name': 'IC0'},
            {'name': 'IC1'}, {'name': 'IC2'}, {'name': 'IC3'}, {'name': 'INTREQ'},
            {'name': 'WE'}, {'name': 'DBIN'}, {'name': 'READY'}, {'name': 'WAIT'},
            {'name': 'HOLD'}, {'name': 'HOLDA'}, {'name': 'LOAD'}, {'name': 'RESET'},
            {'name': 'IAQ'}, {'name': 'AS'}, {'name': 'MEMEN'}, {'name': 'φ1'},
            {'name': 'φ2'}, {'name': 'φ3'}, {'name': 'φ4'}, {'name': 'XOUT'},
            {'name': 'XIN'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VBB'},
            {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

    # TMS9901 - Programmable Systems Interface
    generator.add_chip(
        name="TMS9901 PSI",
        chip_id="ti99_tms9901",
        category="I/O",
        description="Programmable Systems Interface for TI-99/4A",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'}, {'name': 'P3'},
            {'name': 'P4'}, {'name': 'P5'}, {'name': 'P6'}, {'name': 'P7'},
            {'name': 'P8'}, {'name': 'P9'}, {'name': 'P10'}, {'name': 'P11'},
            {'name': 'P12'}, {'name': 'P13'}, {'name': 'P14'}, {'name': 'P15'},
            {'name': 'INT1'}, {'name': 'INT2'}, {'name': 'INT3'}, {'name': 'INT4'},
            {'name': 'INT5'}, {'name': 'INT6'}, {'name': 'INT7'}, {'name': 'INT8'},
            {'name': 'INT9'}, {'name': 'INT10'}, {'name': 'INT11'}, {'name': 'INT12'},
            {'name': 'INT13'}, {'name': 'INT14'}, {'name': 'INT15'}, {'name': 'INTREQ'},
            {'name': 'IC0'}, {'name': 'IC1'}, {'name': 'IC2'}, {'name': 'IC3'},
            {'name': 'CE'}, {'name': 'CRUCLK'}, {'name': 'CRUOUT'}, {'name': 'CRUIN'},
            {'name': 'φ4'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # TMS9918A - Video Display Processor (same as MSX)
    generator.add_chip(
        name="TMS9918A VDP",
        chip_id="ti99_tms9918a",
        category="Video",
        description="Video Display Processor for TI-99/4A",
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

    # SN76489 - Programmable Sound Generator
    generator.add_chip(
        name="SN76489 PSG",
        chip_id="ti99_sn76489",
        category="Audio",
        description="Programmable Sound Generator for TI-99/4A",
        package_types=["DIP-16"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'WE'}, {'name': 'CE'}, {'name': 'READY'}, {'name': 'CLOCK'},
            {'name': 'AUDIO'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # TMS9980 - Alternate CPU (8-bit data bus)
    generator.add_chip(
        name="TMS9980 CPU",
        chip_id="ti99_tms9980",
        category="Processor",
        description="16-bit Microprocessor with 8-bit data bus",
        package_types=["DIP-40"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'CRUCLK'}, {'name': 'CRUOUT'}, {'name': 'CRUIN'}, {'name': 'IC0'},
            {'name': 'IC1'}, {'name': 'IC2'}, {'name': 'IC3'}, {'name': 'INTREQ'},
            {'name': 'WE'}, {'name': 'DBIN'}, {'name': 'READY'}, {'name': 'WAIT'},
            {'name': 'HOLD'}, {'name': 'HOLDA'}, {'name': 'RESET'}, {'name': 'φ4'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("TI-99/4A chipset definitions loaded")
    print("Available chips: TMS9900, TMS9901, TMS9918A, SN76489, TMS9980")
