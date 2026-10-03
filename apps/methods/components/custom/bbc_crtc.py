"""
CRTC 6845 - Cathode Ray Tube Controller for BBC Micro
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "bbc_crtc",
        "CRTC 6845",
        "Video",
        "Cathode Ray Tube Controller for BBC Micro",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["VSS", "CLK", "R/W", "RS", "CS", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "MA0", "MA1", "MA2", "MA3", "MA4", "MA5", "MA6", "MA7", "MA8", "MA9", "MA10", "MA11", "MA12", "MA13", "RA0", "RA1", "RA2", "RA3", "RA4", "HSYNC", "VSYNC", "DE", "CURSOR", "LPSTB", "E", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("bbc_crtc_qfp_44", "CRTC 6845 (QFP-44)", "QFP-44")

    return comp
