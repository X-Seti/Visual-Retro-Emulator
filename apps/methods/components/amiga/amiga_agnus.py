"""
Agnus 8370/8371 - Address Generator / Animation Chip (Agnus)
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "amiga_agnus",
        "Agnus 8370/8371",
        "Custom",
        "Address Generator / Animation Chip (Agnus)",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-84"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "A16", "A17", "A18", "A19", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "RESET", "VSYNC", "HSYNC", "CSYNC", "CCK", "CCKQ", "7M", "XCLK", "XCLKEN", "RGA1", "RGA2", "RGA3", "RGA4", "RGA5", "RGA6", "RGA7", "RGA8", "DMAL", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("amiga_agnus_plcc_84", "Agnus 8370/8371 (PLCC-84)", "PLCC-84")

    return comp
