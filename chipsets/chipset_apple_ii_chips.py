"""
X-Seti June13 2025 - Apple II Chipset Definitions
Visual Retro System Emulator Builder - Apple II Core Chips
"""

def add_apple_ii_chips(generator):
    """Add Apple II chipset components"""
    
    # IOU - Input/Output Unit
    generator.add_chip(
        name="IOU 344-0020",
        chip_id="apple2_iou",
        category="I/O",
        description="Input/Output Unit for Apple IIe/IIc",
        package_types=["DIP-28", "QFP-32"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'D0'}, {'name': 'D1'},
            {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
            {'name': 'D6'}, {'name': 'D7'}, {'name': 'φ0'}, {'name': 'φ1'},
            {'name': 'R/W'}, {'name': 'DEV'}, {'name': 'STR'}, {'name': 'KBD'},
            {'name': 'GAME'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # MMU - Memory Management Unit
    generator.add_chip(
        name="MMU 344-0030",
        chip_id="apple2_mmu",
        category="Custom",
        description="Memory Management Unit for Apple IIe/IIc",
        package_types=["DIP-28", "QFP-32"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'BANK1'}, {'name': 'BANK2'}, {'name': 'AUXSEL'}, {'name': 'R/W'},
            {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'RAMRD'}, {'name': 'RAMWR'},
            {'name': 'INTCX'}, {'name': 'SLOTC3'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # Video Scanner
    generator.add_chip(
        name="Video Scanner 344-0024",
        chip_id="apple2_video",
        category="Video",
        description="Video Scanner and Character Generator",
        package_types=["DIP-40"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'TEXT'}, {'name': 'MIX'}, {'name': 'PAGE2'}, {'name': 'HIRES'},
            {'name': 'AN0'}, {'name': 'AN1'}, {'name': 'AN2'}, {'name': 'AN3'},
            {'name': 'COMP'}, {'name': 'COLOR'}, {'name': 'LUM'}, {'name': 'SERR'},
            {'name': '14M'}, {'name': '7M'}, {'name': 'φ0'}, {'name': 'HSYNC'},
            {'name': 'VSYNC'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # Disk II Controller
    generator.add_chip(
        name="Disk II Controller P5A",
        chip_id="apple2_disk",
        category="Storage",
        description="Disk II Floppy Drive Controller",
        package_types=["DIP-20"],
        pins=[
            {'name': 'PHASE0'}, {'name': 'PHASE1'}, {'name': 'PHASE2'}, {'name': 'PHASE3'},
            {'name': 'MOTOR'}, {'name': 'DRIVE1'}, {'name': 'DRIVE2'}, {'name': 'Q3'},
            {'name': 'DATA'}, {'name': 'WRITE'}, {'name': 'PROTECT'}, {'name': 'TRACK0'},
            {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'ENABLE'}, {'name': 'READY'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC1'}, {'name': 'NC2'}
        ]
    )

    # Language Card (16K RAM expansion)
    generator.add_chip(
        name="Language Card",
        chip_id="apple2_langcard",
        category="Memory",
        description="16K RAM Expansion Card",
        package_types=["Card Edge"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'R/W'}, {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'RESET'},
            {'name': 'IRQ'}, {'name': 'NMI'}, {'name': '+5V'}, {'name': '+12V'},
            {'name': '-5V'}, {'name': '-12V'}, {'name': 'GND'}, {'name': 'SLOT'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Apple II chipset definitions loaded")
    print("Available chips: IOU, MMU, Video Scanner, Disk II Controller, Language Card")
