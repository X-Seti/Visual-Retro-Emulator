"""
MC6883/SN74LS783 (SAM) - Synchronous Address Multiplexer for Dragon/CoCo
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "dragon_sam",
        "MC6883/SN74LS783 (SAM)",
        "Custom",
        "Synchronous Address Multiplexer for Dragon/CoCo",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "Z80", "DA0", "DA1", "DA2", "DA3", "DA4", "DA5", "DA6", "DA7", "Q", "E", "HS", "RAS", "CAS", "S1", "S0", "R/W", "SLENB", "FIELD", "RAS0", "RASE", "RAS1", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("dragon_sam_qfp_44", "MC6883/SN74LS783 (SAM) (QFP-44)", "QFP-44")

    return comp
