"""
PPU 2C02 - Picture Processing Unit (PPU) for NES
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "nes_ppu",
        "PPU 2C02",
        "Video",
        "Picture Processing Unit (PPU) for NES",
        width=240,
        height=260
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["AD0", "AD1", "AD2", "AD3", "AD4", "AD5", "AD6", "AD7", "ALE", "R/W", "DB0", "DB1", "DB2", "DB3", "DB4", "DB5", "DB6", "DB7", "INT", "VRAM /CE", "VRAM A10", "VRAM A11", "EXT0", "EXT1", "EXT2", "EXT3", "EXT4", "CLK", "RED", "GREEN", "BLUE", "SYNC", "HBLANK", "VBLANK", "RES", "VCC", "GND", "VCC2", "GND2", "NC"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("nes_ppu_qfp_44", "PPU 2C02 (QFP-44)", "QFP-44")

    return comp
