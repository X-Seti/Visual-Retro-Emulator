"""
Denise 8362 - Display Encoder Chip (Denise)
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "amiga_denise",
        "Denise 8362",
        "Video",
        "Display Encoder Chip (Denise)",
        width=300,
        height=320
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-48"  # Default package

    # Add pins
    pin_list = ["R0", "R1", "R2", "R3", "G0", "G1", "G2", "G3", "B0", "B1", "B2", "B3", "M0", "M1", "M2", "M3", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "BURST", "RGA1", "RGA2", "RGA3", "RGA4", "RGA5", "RGA6", "RGA7", "RGA8", "CCK", "CDAC", "RESET", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("amiga_denise_plcc_48", "Denise 8362 (PLCC-48)", "PLCC-48")
    comp.add_variant("amiga_denise_qfp_52", "Denise 8362 (QFP-52)", "QFP-52")

    return comp
