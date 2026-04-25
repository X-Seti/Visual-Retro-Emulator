"""
TMS9901 - Programmable Systems Interface for TI-99/4A
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "ti99_tms9901",
        "TMS9901",
        "I/O",
        "Programmable Systems Interface for TI-99/4A",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["CRUOUT", "CRUIN", "CRUCLK", "CE", "S0", "S1", "S2", "S3", "S4", "INT1", "INT2", "INT3", "INT4", "INT5", "INT6", "INT7", "INT8", "INT9", "INT10", "INT11", "INT12", "INT13", "INT14", "INT15", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "INTREQ", "RESET", "φ1", "φ2", "VCC", "GND", "NC", "NC"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("ti99_tms9901_qfp_44", "TMS9901 (QFP-44)", "QFP-44")

    return comp
