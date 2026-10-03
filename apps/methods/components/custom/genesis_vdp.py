"""
VDP YM7101 - Video Display Processor (VDP) for Sega Genesis
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "genesis_vdp",
        "VDP YM7101",
        "Video",
        "Video Display Processor (VDP) for Sega Genesis",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "QFP-64"  # Default package

    # Add pins
    pin_list = ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "A16", "CE", "OE", "WE", "UB", "LB", "CAS0", "CAS1", "RAS", "CLK", "IPL0", "IPL1", "IPL2", "HSYNC", "VSYNC", "CSYNC", "MCLK", "SCLK", "RED", "GREEN", "BLUE", "VCC", "GND", "VCC2", "GND2", "NC", "NC", "NC"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("genesis_vdp_qfp_68", "VDP YM7101 (QFP-68)", "QFP-68")

    return comp
