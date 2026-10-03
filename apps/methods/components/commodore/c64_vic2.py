"""
VIC-II 6567/6569 - Video Interface Chip II (VIC-II)
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "c64_vic2",
        "VIC-II 6567/6569",
        "Video",
        "Video Interface Chip II (VIC-II)",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "R/W", "AEC", "IRQ", "COLOR", "SYNC", "BA", "φ0", "RAS", "CAS", "LP", "VDD", "VSS", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("c64_vic2_qfp_44", "VIC-II 6567/6569 (QFP-44)", "QFP-44")

    return comp
