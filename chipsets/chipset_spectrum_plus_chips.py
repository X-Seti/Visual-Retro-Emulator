"""
X-Seti June13 2025 - ZX Spectrum Plus Series Chipset Definitions
Visual Retro System Emulator Builder - Spectrum +2/+2A/+2B/+3 Core Chips
"""

def add_spectrum_plus2_chips(generator):
    """Add ZX Spectrum +2 chipset components (Amstrad era)"""
    
    # Z80A CPU - Main processor
    generator.add_chip(
        name="Z80A CPU",
        chip_id="specplus2_z80a",
        category="Processor",
        description="Zilog Z80A CPU for Spectrum +2",
        package_types=["DIP-40", "PLCC-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'M1'}, {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'},
            {'name': 'WR'}, {'name': 'RFSH'}, {'name': 'HALT'}, {'name': 'WAIT'},
            {'name': 'INT'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'BUSRQ'},
            {'name': 'BUSAK'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # Amstrad Gate Array - Custom chip
    generator.add_chip(
        name="Amstrad Gate Array",
        chip_id="specplus2_gate_array",
        category="Custom",
        description="Amstrad custom gate array for +2 - Video, memory, I/O control",
        package_types=["PLCC-68"],
        pins=[
            # CPU Interface
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'M1'}, {'name': 'RFSH'}, {'name': 'INT'}, {'name': 'CLK'},
            # Memory Control
            {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'WE'}, {'name': 'OE'},
            {'name': 'ROMCS'}, {'name': 'RAMCS'}, {'name': 'A14_A15'}, {'name': 'CASAD'},
            # Video Output
            {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'BRIGHT'},
            {'name': 'SYNC'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BORDER'},
            # Audio/Tape
            {'name': 'BEEP'}, {'name': 'MIC'}, {'name': 'EAR'}, {'name': 'TAPE_IN'},
            {'name': 'TAPE_OUT'}, {'name': 'SOUND'}, {'name': 'AUDIO_L'}, {'name': 'AUDIO_R'},
            # System
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )
    
    # AY-3-8912 - Sound chip
    generator.add_chip(
        name="AY-3-8912",
        chip_id="specplus2_ay_8912",
        category="Audio",
        description="Programmable Sound Generator for +2 enhanced audio",
        package_types=["DIP-28"],
        pins=[
            {'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'}, {'name': 'DA3'},
            {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'}, {'name': 'DA7'},
            {'name': 'BDIR'}, {'name': 'BC1'}, {'name': 'BC2'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'RESET'}, {'name': 'CLOCK'}, {'name': 'IOA0'},
            {'name': 'IOA1'}, {'name': 'IOA2'}, {'name': 'IOA3'}, {'name': 'IOA4'},
            {'name': 'IOA5'}, {'name': 'IOA6'}, {'name': 'IOA7'}, {'name': 'CHANNEL_A'},
            {'name': 'CHANNEL_B'}, {'name': 'CHANNEL_C'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # Built-in Tape Deck Controller
    generator.add_chip(
        name="Tape Controller",
        chip_id="specplus2_tape_ctrl",
        category="Storage",
        description="Built-in cassette tape deck controller",
        package_types=["Custom"],
        pins=[
            {'name': 'PLAY'}, {'name': 'STOP'}, {'name': 'REW'}, {'name': 'FF'},
            {'name': 'REC'}, {'name': 'PAUSE'}, {'name': 'MOTOR'}, {'name': 'HEAD_L'},
            {'name': 'HEAD_R'}, {'name': 'TAPE_SENSE'}, {'name': 'COUNTER'}, {'name': 'LED'},
            {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

def add_spectrum_plus3_chips(generator):
    """Add ZX Spectrum +3 chipset components (with disk drive)"""
    
    # Gate Array +3 - Enhanced version
    generator.add_chip(
        name="Gate Array +3",
        chip_id="specplus3_gate_array",
        category="Custom",
        description="Enhanced gate array for +3 with disk interface support",
        package_types=["PLCC-84"],
        pins=[
            # CPU Interface
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'M1'}, {'name': 'RFSH'}, {'name': 'INT'}, {'name': 'CLK'},
            # Memory Banking
            {'name': 'ROMCS'}, {'name': 'RAMCS'}, {'name': 'BANK0'}, {'name': 'BANK1'},
            {'name': 'BANK2'}, {'name': 'BANK3'}, {'name': 'BANK4'}, {'name': 'BANK5'},
            {'name': 'BANK6'}, {'name': 'BANK7'}, {'name': 'MREQ_T23'}, {'name': 'A14_A15_T'},
            # Disk Interface
            {'name': 'DISK_MOTOR'}, {'name': 'DISK_SELECT'}, {'name': 'DISK_SIDE'},
            {'name': 'DISK_DIR'}, {'name': 'DISK_STEP'}, {'name': 'DISK_WDATA'},
            {'name': 'DISK_WGATE'}, {'name': 'DISK_RDATA'}, {'name': 'DISK_READY'},
            {'name': 'DISK_WPROT'}, {'name': 'DISK_TRK0'}, {'name': 'DISK_INDEX'},
            # System
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )
    
    # µPD765 - Floppy Disk Controller
    generator.add_chip(
        name="FDC µPD765A",
        chip_id="specplus3_upd765",
        category="Storage",
        description="NEC µPD765A Floppy Disk Controller for +3",
        package_types=["DIP-40"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'TC'}, {'name': 'IDX'},
            {'name': 'RDY'}, {'name': 'WP'}, {'name': 'TRK00'}, {'name': 'WG'},
            {'name': 'WD'}, {'name': 'STEP'}, {'name': 'DIR'}, {'name': 'RD_DATA'},
            {'name': 'DRQ'}, {'name': 'DACK'}, {'name': 'INT'}, {'name': 'US0'},
            {'name': 'US1'}, {'name': 'MO'}, {'name': 'VCC'}, {'name': 'GND'},
            {'name': 'VBB'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'NC'},
            {'name': 'NC2'}, {'name': 'NC3'}, {'name': 'NC4'}, {'name': 'TEST'}
        ]
    )

def add_spectrum_plus2a_chips(generator):
    """Add ZX Spectrum +2A chipset components (cost-reduced +2)"""
    
    # +2A Gate Array - Simplified version
    generator.add_chip(
        name="Gate Array +2A",
        chip_id="specplus2a_gate_array", 
        category="Custom",
        description="Cost-reduced gate array for +2A",
        package_types=["PLCC-68"],
        pins=[
            # CPU Interface
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'M1'}, {'name': 'RFSH'}, {'name': 'INT'}, {'name': 'CLK'},
            # Memory Control
            {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'WE'}, {'name': 'OE'},
            {'name': 'ROMCS'}, {'name': 'RAMCS'}, {'name': 'BANK_SEL'}, {'name': 'PAGE'},
            # Video Output
            {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'BRIGHT'},
            {'name': 'SYNC'}, {'name': 'BORDER'}, {'name': 'FLASH'}, {'name': 'BLANK'},
            # System
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

def add_sam_coupe_chips(generator):
    """Add SAM Coupé chipset components (Spectrum successor)"""
    
    # Z80B CPU - Enhanced processor
    generator.add_chip(
        name="Z80B CPU",
        chip_id="sam_z80b",
        category="Processor", 
        description="Zilog Z80B CPU for SAM Coupé - 6MHz operation",
        package_types=["DIP-40", "PLCC-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'M1'}, {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'},
            {'name': 'WR'}, {'name': 'RFSH'}, {'name': 'HALT'}, {'name': 'WAIT'},
            {'name': 'INT'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'BUSRQ'},
            {'name': 'BUSAK'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )
    
    # ASIC - Application Specific Integrated Circuit
    generator.add_chip(
        name="SAM ASIC",
        chip_id="sam_asic",
        category="Custom",
        description="Custom ASIC for SAM Coupé - Video, memory, I/O control",
        package_types=["PLCC-84"],
        pins=[
            # CPU Interface
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            # Memory Control
            {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'},
            {'name': 'WE'}, {'name': 'OE'}, {'name': 'ROMCS'}, {'name': 'RAMCS'},
            {'name': 'PAGE0'}, {'name': 'PAGE1'}, {'name': 'PAGE2'}, {'name': 'PAGE3'},
            # Video Interface
            {'name': 'RED0'}, {'name': 'RED1'}, {'name': 'RED2'}, {'name': 'RED3'},
            {'name': 'GREEN0'}, {'name': 'GREEN1'}, {'name': 'GREEN2'}, {'name': 'GREEN3'},
            {'name': 'BLUE0'}, {'name': 'BLUE1'}, {'name': 'BLUE2'}, {'name': 'BLUE3'},
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'}, {'name': 'BLANK'},
            # Disk Interface
            {'name': 'DISK_INDEX'}, {'name': 'DISK_TRK0'}, {'name': 'DISK_WPROT'}, {'name': 'DISK_RDATA'},
            {'name': 'DISK_WDATA'}, {'name': 'DISK_WGATE'}, {'name': 'DISK_STEP'}, {'name': 'DISK_DIR'},
            {'name': 'DISK_SIDE'}, {'name': 'DISK_MOTOR'}, {'name': 'DISK_SELECT'}, {'name': 'DISK_READY'},
            # System
            {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )
    
    # SAA1099 - Sound chip
    generator.add_chip(
        name="SAA1099",
        chip_id="sam_saa1099",
        category="Audio",
        description="Philips SAA1099 - 6-channel sound synthesizer",
        package_types=["DIP-28"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'CS'}, {'name': 'WR'}, {'name': 'RESET'},
            {'name': 'CLK'}, {'name': 'OUT_L'}, {'name': 'OUT_R'}, {'name': 'DTACK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'AVCC'}, {'name': 'AGND'},
            {'name': 'VREF'}, {'name': 'NC1'}, {'name': 'NC2'}, {'name': 'NC3'},
            {'name': 'NC4'}, {'name': 'NC5'}, {'name': 'NC6'}, {'name': 'TEST'}
        ]
    )
    
    # WD1772 - Floppy Disk Controller
    generator.add_chip(
        name="FDC WD1772",
        chip_id="sam_wd1772",
        category="Storage",
        description="Western Digital WD1772 - Floppy disk controller",
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

if __name__ == "__main__":
    # Test function
    print("ZX Spectrum Plus series chipset definitions loaded")
    print("Spectrum +2 chips: Z80A, Amstrad Gate Array, AY-3-8912, Tape Controller")
    print("Spectrum +3 chips: Gate Array +3, µPD765A FDC")
    print("Spectrum +2A chips: Gate Array +2A (cost-reduced)")
    print("SAM Coupé chips: Z80B, SAM ASIC, SAA1099, WD1772")
