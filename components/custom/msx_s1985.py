"""
Yamaha S1985 - MSX-Engine for MSX2 and up (integrated circuits)
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "msx_s1985",
        "Yamaha S1985",
        "Custom",
        "MSX-Engine for MSX2 and up (integrated circuits)",
        width=396,
        height=462
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-64"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "IORQ", "MREQ", "RD", "WR", "INT", "BUSDIR", "CSROM", "SLTSL0", "SLTSL1", "SLTSL2", "SLTSL3", "RESET", "RFSH", "WAIT", "M1", "BUSAK", "CLK", "SW1", "SW2", "CAPS", "KANA", "CAS", "RAS", "ROMCS", "MUX", "KAN", "CS12", "CS3", "CASW", "VCC", "GND", "NC", "NC", "NC", "NC", "NC"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("msx_s1985_qfp_64", "Yamaha S1985 (QFP-64)", "QFP-64")

    return comp
