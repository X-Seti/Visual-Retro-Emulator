"""
ANTIC CO12296 - Alphanumeric Television Interface Controller for Atari 8-bit
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "atari_antic",
        "ANTIC CO12296",
        "Video",
        "Alphanumeric Television Interface Controller for Atari 8-bit",
        width=240,
        height=260
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "RDY", "REF", "HALT", "R/W", "φ0", "φ2", "VSYNC", "HSYNC", "NMI", "IRQ", "RST", "AN0", "AN1", "AN2", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("atari_antic_qfp_44", "ANTIC CO12296 (QFP-44)", "QFP-44")

    return comp
