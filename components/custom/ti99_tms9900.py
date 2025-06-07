"""
TMS9900 - 16-bit CPU for TI-99/4A
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "ti99_tms9900",
        "TMS9900",
        "CPU",
        "16-bit CPU for TI-99/4A",
        width=432,
        height=504
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-64"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "MEMEN", "WE", "DBIN", "IAQ", "INTREQ", "READY", "WAIT", "LOAD", "HOLD", "HOLDA", "RESET", "CRUCLK", "CRUOUT", "CRUIN", "φ1", "φ2", "φ3", "φ4", "VCC", "GND", "NC", "NC", "NC", "NC", "NC", "NC", "NC", "NC"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("ti99_tms9900_qfp_64", "TMS9900 (QFP-64)", "QFP-64")

    return comp
