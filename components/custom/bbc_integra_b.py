"""
INTEGRA-B - ASIC for BBC Master Integrating Multiple Functions
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "bbc_integra_b",
        "INTEGRA-B",
        "Custom",
        "ASIC for BBC Master Integrating Multiple Functions",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "QFP-84"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "ROMSEL", "ACCCON", "VDUSEL", "SHEILASEL", "CLK2MHZ", "CLK1MHZ", "VIDPROC", "SOUND", "DISEN", "CSY", "CS", "RW", "IRQ", "16MHZ", "8MHZ", "4MHZ", "2MHZ", "1MHZ", "RST", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("bbc_integra_b_plcc_84", "INTEGRA-B (PLCC-84)", "PLCC-84")

    return comp
