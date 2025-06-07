"""
Paula 8364 - Ports and Audio Chip (Paula)
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "amiga_paula",
        "Paula 8364",
        "Audio",
        "Ports and Audio Chip (Paula)",
        width=300,
        height=320
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-48"  # Default package

    # Add pins
    pin_list = ["POT0X", "POT0Y", "POT1X", "POT1Y", "DKRD", "DKWD", "DKWE", "TXD", "RXD", "AUD0", "AUD1", "AUD2", "AUD3", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "INT2", "INT3", "INT6", "RGA1", "RGA2", "RGA3", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("amiga_paula_plcc_48", "Paula 8364 (PLCC-48)", "PLCC-48")

    return comp
