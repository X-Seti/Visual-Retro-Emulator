"""
System VIA 6522 - System Versatile Interface Adapter for BBC Micro
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "bbc_system_via",
        "System VIA 6522",
        "I/O",
        "System Versatile Interface Adapter for BBC Micro",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["VSS", "PA0", "PA1", "PA2", "PA3", "PA4", "PA5", "PA6", "PA7", "PB0", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "CB1", "CB2", "CA1", "CA2", "RS0", "RS1", "RS2", "RS3", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "RES", "φ2", "CS1", "CS2", "R/W", "IRQ", "VCC"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("bbc_system_via_qfp_44", "System VIA 6522 (QFP-44)", "QFP-44")

    return comp
