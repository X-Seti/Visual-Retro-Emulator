"""
GTIA CO14889 - Graphics Television Interface Adapter for Atari 8-bit
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "atari_gtia",
        "GTIA CO14889",
        "Video",
        "Graphics Television Interface Adapter for Atari 8-bit",
        width=240,
        height=260
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "CS", "R/W", "φ0", "AN0", "AN1", "AN2", "AN3", "CONT", "TRIG0", "TRIG1", "TRIG2", "TRIG3", "CONS", "PAL", "LUMA0", "LUMA1", "LUMA2", "CHROMA", "BURST", "OSC", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("atari_gtia_qfp_44", "GTIA CO14889 (QFP-44)", "QFP-44")

    return comp
