"""
POKEY C012294 - Pot Keyboard Integrated Circuit for Atari 8-bit
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "atari_pokey",
        "POKEY C012294",
        "Audio",
        "Pot Keyboard Integrated Circuit for Atari 8-bit",
        width=240,
        height=260
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "K0", "K1", "K2", "K3", "K4", "K5", "POT0", "POT1", "POT2", "POT3", "POT4", "POT5", "POT6", "POT7", "AUDIO", "BID", "CS", "R/W", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("atari_pokey_qfp_44", "POKEY C012294 (QFP-44)", "QFP-44")

    return comp
