"""
TMS9918A - Video Display Processor for MSX/Coleco/TI99
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "msx_tms9918a",
        "TMS9918A",
        "Video",
        "Video Display Processor for MSX/Coleco/TI99",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["AD0", "AD1", "AD2", "AD3", "AD4", "AD5", "AD6", "AD7", "BD0", "BD1", "BD2", "BD3", "BD4", "BD5", "BD6", "BD7", "MODE", "CSW", "CSR", "INT", "RD", "CD", "EXTVDP", "COMVID", "GROM", "CPUCLK", "XIN", "XOUT", "R", "G", "B", "Y", "HSYNC", "VSYNC", "VCC", "GND", "RESET", "VRAM /CS", "NC", "NC"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    comp.add_variant("msx_tms9918a_qfp_44", "TMS9918A (QFP-44)", "QFP-44")

    return comp
