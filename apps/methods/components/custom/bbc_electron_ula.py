"""
Electron ULA - Uncommitted Logic Array for Acorn Electron
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "bbc_electron_ula",
        "Electron ULA",
        "Custom",
        "Uncommitted Logic Array for Acorn Electron",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "φ0", "φ1", "φ2", "R/W", "IRQ", "CAS", "RAS", "SYNC", "RED", "GREEN", "BLUE", "CSYNC", "ROM", "RAM", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("bbc_electron_ula_qfp_44", "Electron ULA (QFP-44)", "QFP-44")

    return comp
