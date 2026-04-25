"""
X-Seti June13 2025 - Sinclair QL Chipset Definitions
Visual Retro System Emulator Builder - Sinclair QL Core Chips
"""

def add_sinclair_ql_chips(generator):
    """Add Sinclair QL chipset components"""
    
    # 68008 CPU - Main processor
    generator.add_chip(
        name="MC68008 CPU",
        chip_id="ql_68008",
        category="Processor",
        description="Motorola 68008 CPU - 32-bit processor with 8-bit data bus",
        package_types=["DIP-48", "PLCC-52"],
        pins=[
            # Data Bus (8-bit external)
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            # Address Bus
            {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'},
            {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'},
            {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'},
            {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'},
            # Control Signals
            {'name': 'AS'}, {'name': 'DS'}, {'name': 'R/W'}, {'name': 'DTACK'},
            {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'BR'}, {'name': 'FC0'},
            {'name': 'FC1'}, {'name': 'FC2'}, {'name': 'IPL0'}, {'name': 'IPL1'},
            {'name': 'IPL2'}, {'name': 'BERR'}, {'name': 'VPA'}, {'name': 'VMA'},
            {'name': 'E'}, {'name': 'RESET'}, {'name': 'HALT'}, {'name': 'CLK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )
    
    # IPC - Intelligent Peripheral Controller (8049)
    generator.add_chip(
        name="IPC 8049",
        chip_id="ql_ipc",
        category="I/O",
        description="Intel 8049 - Intelligent Peripheral Controller for keyboard/sound",
        package_types=["DIP-40"],
        pins=[
            # I/O Ports
            {'name': 'P10'}, {'name': 'P11'}, {'name': 'P12'}, {'name': 'P13'},
            {'name': 'P14'}, {'name': 'P15'}, {'name': 'P16'}, {'name': 'P17'},
            {'name': 'P20'}, {'name': 'P21'}, {'name': 'P22'}, {'name': 'P23'},
            {'name': 'P24'}, {'name': 'P25'}, {'name': 'P26'}, {'name': 'P27'},
            # External Interface
            {'name': 'T0'}, {'name': 'T1'}, {'name': 'INT'}, {'name': 'RD'},
            {'name': 'WR'}, {'name': 'ALE'}, {'name': 'PSEN'}, {'name': 'PROG'},
            {'name': 'EA'}, {'name': 'SS'}, {'name': 'TO'}, {'name': 'SYNC'},
            # Data/Address Bus
            {'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'},
            {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'},
            # Power/Clock
            {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'RESET'}, {'name': 'VCC'},
            {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VBB'}
        ]
    )
    
    # ZX8301 - Master Chip (ULA equivalent)
    generator.add_chip(
        name="ZX8301 Master",
        chip_id="ql_zx8301",
        category="Custom",
        description="ZX8301 Master Chip - CPU interface, DRAM control, video timing",
        package_types=["PLCC-84"],
        pins=[
            # CPU Interface
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'},
            # DRAM Interface
            {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS'}, {'name': 'WE'},
            {'name': 'OE'}, {'name': 'MUX'}, {'name': 'REF'}, {'name': 'RFSH'},
            # Video Interface
            {'name': 'CSYNC'}, {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'BLANK'},
            {'name': 'DISEN'}, {'name': 'FLASH'}, {'name': 'VDATA'}, {'name': 'VCLK'},
            # Serial Interface
            {'name': 'COMDATA'}, {'name': 'COMCLK'}, {'name': 'BAUDX16'}, {'name': 'CTS1'},
            {'name': 'CTS2'}, {'name': 'DTR1'}, {'name': 'DTR2'}, {'name': 'TXD1'},
            {'name': 'TXD2'}, {'name': 'RXD1'}, {'name': 'RXD2'}, {'name': 'RTXC1'},
            {'name': 'RTXC2'}, {'name': 'TRXC1'}, {'name': 'TRXC2'}, {'name': 'IPL2'},
            # Clock/Control
            {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'CLK'}, {'name': 'RESET'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}
        ]
    )
    
    # ZX8302 - Peripheral Chip
    generator.add_chip(
        name="ZX8302 Peripheral",
        chip_id="ql_zx8302",
        category="Custom", 
        description="ZX8302 Peripheral Chip - Real time clock, RS232, network interface",
        package_types=["PLCC-68"],
        pins=[
            # CPU Interface
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'CS'}, {'name': 'RW'},
            {'name': 'DS'}, {'name': 'DTACK'}, {'name': 'IPL7'}, {'name': 'RESET'},
            # Serial Ports
            {'name': 'TXD1'}, {'name': 'RXD1'}, {'name': 'RTS1'}, {'name': 'CTS1'},
            {'name': 'DTR1'}, {'name': 'DSR1'}, {'name': 'DCD1'}, {'name': 'TXD2'},
            {'name': 'RXD2'}, {'name': 'RTS2'}, {'name': 'CTS2'}, {'name': 'DTR2'},
            {'name': 'DSR2'}, {'name': 'DCD2'}, {'name': 'BAUDX16'}, {'name': 'BAUDX1'},
            # Network Interface
            {'name': 'NET1'}, {'name': 'NET2'}, {'name': 'NETCK'}, {'name': 'NETDIR'},
            # Real Time Clock
            {'name': 'RTCX1'}, {'name': 'RTCX2'}, {'name': 'RTCDATA'}, {'name': 'VBAT'},
            # Microdrive Interface
            {'name': 'MDV1_DATA'}, {'name': 'MDV2_DATA'}, {'name': 'MDV1_CLK'}, {'name': 'MDV2_CLK'},
            {'name': 'MDV1_ERASE'}, {'name': 'MDV2_ERASE'}, {'name': 'MDV1_RW'}, {'name': 'MDV2_RW'},
            {'name': 'MDV1_WP'}, {'name': 'MDV2_WP'}, {'name': 'MDV_SEL'}, {'name': 'MDV_MOTOR'},
            # Power/Control
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'},
            {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'CLK'}, {'name': 'TEST'}
        ]
    )
    
    # ROM - Operating System
    generator.add_chip(
        name="OS ROM",
        chip_id="ql_os_rom",
        category="Memory",
        description="48KB Operating System ROM (QDOS)",
        package_types=["DIP-28"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'CE'}, {'name': 'OE'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # DRAM - System Memory
    generator.add_chip(
        name="DRAM 4164",
        chip_id="ql_dram_4164",
        category="Memory",
        description="64Kx1 Dynamic RAM - 8 chips for 128KB system",
        package_types=["DIP-16"],
        pins=[
            {'name': 'VBB'}, {'name': 'DIN'}, {'name': 'WRITE'}, {'name': 'RAS'},
            {'name': 'A0'}, {'name': 'A2'}, {'name': 'A1'}, {'name': 'VDD'},
            {'name': 'VCC'}, {'name': 'DOUT'}, {'name': 'CAS'}, {'name': 'A3'},
            {'name': 'A6'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'VSS'}
        ]
    )

def add_ql_trump_card_chips(generator):
    """Add QL Trump Card disk interface components"""
    
    # WD1772 - Floppy Disk Controller
    generator.add_chip(
        name="FDC WD1772",
        chip_id="ql_trump_wd1772",
        category="Storage",
        description="Western Digital WD1772 - Floppy disk controller for Trump Card",
        package_types=["DIP-28"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RE'},
            {'name': 'WE'}, {'name': 'CLK'}, {'name': 'RESET'}, {'name': 'READY'},
            {'name': 'WF'}, {'name': 'WG'}, {'name': 'TG00'}, {'name': 'IP'},
            {'name': 'WPRT'}, {'name': 'TR00'}, {'name': 'STEP'}, {'name': 'DIRC'},
            {'name': 'WD'}, {'name': 'RD'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

def add_ql_gold_card_chips(generator):
    """Add QL Gold Card accelerator components"""
    
    # 68000 CPU - Accelerator processor
    generator.add_chip(
        name="MC68000 Accelerator",
        chip_id="ql_gold_68000",
        category="Processor",
        description="Motorola 68000 CPU for Gold Card acceleration",
        package_types=["DIP-64", "PLCC-68"],
        pins=[
            # Data Bus
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            # Address Bus
            {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'},
            {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'},
            {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'},
            {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'},
            {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'}, {'name': 'AS'},
            # Control Signals
            {'name': 'UDS'}, {'name': 'LDS'}, {'name': 'R/W'}, {'name': 'DTACK'},
            {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'BR'}, {'name': 'FC0'},
            {'name': 'FC1'}, {'name': 'FC2'}, {'name': 'IPL0'}, {'name': 'IPL1'},
            {'name': 'IPL2'}, {'name': 'BERR'}, {'name': 'VPA'}, {'name': 'VMA'},
            {'name': 'E'}, {'name': 'RESET'}, {'name': 'HALT'}, {'name': 'CLK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Sinclair QL chipset definitions loaded")
    print("Base QL chips: MC68008, IPC 8049, ZX8301, ZX8302, ROM, DRAM")
    print("Trump Card chips: WD1772")
    print("Gold Card chips: MC68000")
