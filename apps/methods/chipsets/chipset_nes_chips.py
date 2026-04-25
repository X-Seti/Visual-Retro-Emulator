"""
X-Seti June13 2025 - Nintendo NES Chipset Definitions
Visual Retro System Emulator Builder - Nintendo Entertainment System Core Chips
"""

def add_nintendo_nes_chips(generator):
    """Add Nintendo NES chipset components"""
    
    # PPU - Picture Processing Unit
    generator.add_chip(
        name="PPU 2C02",
        chip_id="nes_ppu",
        category="Video",
        description="Picture Processing Unit (PPU) for NES",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'},
            {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'},
            {'name': 'ALE'}, {'name': 'R/W'}, {'name': 'DB0'}, {'name': 'DB1'},
            {'name': 'DB2'}, {'name': 'DB3'}, {'name': 'DB4'}, {'name': 'DB5'},
            {'name': 'DB6'}, {'name': 'DB7'}, {'name': 'INT'}, {'name': 'VRAM /CE'},
            {'name': 'VRAM A10'}, {'name': 'VRAM A11'}, {'name': 'EXT0'}, {'name': 'EXT1'},
            {'name': 'EXT2'}, {'name': 'EXT3'}, {'name': 'EXT4'}, {'name': 'CLK'},
            {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'SYNC'},
            {'name': 'HBLANK'}, {'name': 'VBLANK'}, {'name': 'RES'}, {'name': 'VCC'},
            {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'NC'}
        ]
    )

    # APU - Audio Processing Unit
    generator.add_chip(
        name="APU 2A03",
        chip_id="nes_apu",
        category="Audio",
        description="Audio Processing Unit with 6502 core (APU) for NES",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'IRQ'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'RDY'},
            {'name': 'SO'}, {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'φ2'},
            {'name': 'R/W'}, {'name': 'SYNC'}, {'name': 'OUT0'}, {'name': 'OUT1'},
            {'name': 'OUT2'}, {'name': 'AUDIO'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # CIC - Checking Integrated Circuit (10NES)
    generator.add_chip(
        name="CIC 10NES",
        chip_id="nes_cic",
        category="Custom",
        description="Checking Integrated Circuit - Copy protection and region lockout",
        package_types=["DIP-16"],
        pins=[
            {'name': 'GND'}, {'name': 'KEY'}, {'name': 'HOST'}, {'name': 'VCC'},
            {'name': 'DATA0'}, {'name': 'DATA1'}, {'name': 'CLK'}, {'name': 'RESET'},
            {'name': 'SLAVE'}, {'name': 'LOCK'}, {'name': 'OUT0'}, {'name': 'OUT1'},
            {'name': 'OUT2'}, {'name': 'OUT3'}, {'name': 'MODE'}, {'name': 'SEED'}
        ]
    )

    # MMC1 - Memory Management Controller 1
    generator.add_chip(
        name="MMC1 Nintendo",
        chip_id="nes_mmc1",
        category="Custom",
        description="Memory Management Controller 1 - Bank switching controller",
        package_types=["DIP-24"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'D0'},
            {'name': 'R/W'}, {'name': 'PRG /CE'}, {'name': 'CHR /CE'}, {'name': 'WRAM /CE'},
            {'name': 'CIRAM A10'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'CLK'}
        ]
    )

    # MMC3 - Memory Management Controller 3
    generator.add_chip(
        name="MMC3 Nintendo",
        chip_id="nes_mmc3",
        category="Custom",
        description="Memory Management Controller 3 - Advanced bank switching with IRQ",
        package_types=["DIP-28"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'D0'},
            {'name': 'R/W'}, {'name': 'PRG /CE'}, {'name': 'CHR /CE'}, {'name': 'WRAM /CE'},
            {'name': 'CIRAM A10'}, {'name': 'IRQ'}, {'name': 'PPU A12'}, {'name': 'M2'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'CLK'}, {'name': 'NC'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Nintendo NES chipset definitions loaded")
    print("Available chips: PPU, APU, CIC, MMC1, MMC3")
