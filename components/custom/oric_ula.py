"""
Oric ULA - Uncommitted Logic Array for Oric computers
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "oric_ula",
        "Oric ULA",
        "Custom",
        "Uncommitted Logic Array for Oric computers",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "R/W", "MUX", "CAS", "RAS", "MAP", "PHI", "WARP", "PHI2", "RED", "GREEN", "BLUE", "SYNC", "ROM CS", "I/O CS", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("oric_ula_qfp_44", "Oric ULA (QFP-44)", "QFP-44")

    return comp
