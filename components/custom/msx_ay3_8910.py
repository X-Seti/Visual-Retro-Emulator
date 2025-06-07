"""
AY-3-8910 - Programmable Sound Generator for MSX
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "msx_ay3_8910",
        "AY-3-8910",
        "Audio",
        "Programmable Sound Generator for MSX",
        width=200,
        height=180
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-28"  # Default package

    # Add pins
    pin_list = ["DA0", "DA1", "DA2", "DA3", "DA4", "DA5", "DA6", "DA7", "BC1", "BC2", "BDIR", "A8", "A9", "TEST1", "TEST2", "IOA0", "IOA1", "IOA2", "IOA3", "IOA4", "IOA5", "IOA6", "IOA7", "ANALOG A", "ANALOG B", "ANALOG C", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("msx_ay3_8910_dip_40", "AY-3-8910 (DIP-40)", "DIP-40")

    return comp
