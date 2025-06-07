"""
SID 6581/8580 - Sound Interface Device Chip (SID)
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "c64_sid",
        "SID 6581/8580",
        "Audio",
        "Sound Interface Device Chip (SID)",
        width=200,
        height=180
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-28"  # Default package

    # Add pins
    pin_list = ["CAP1A", "CAP1B", "CAP2A", "CAP2B", "RES", "φ2", "R/W", "CS", "A0", "A1", "A2", "A3", "A4", "GND", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "AUDIO", "VCC", "POT X", "POT Y", "EXT IN", "VDD"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("c64_sid_qfp_44", "SID 6581/8580 (QFP-44)", "QFP-44")

    return comp
