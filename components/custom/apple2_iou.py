"""
IOU 341-0020 - Input/Output Unit (IOU) for Apple II
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "apple2_iou",
        "IOU 341-0020",
        "I/O",
        "Input/Output Unit (IOU) for Apple II",
        width=200,
        height=180
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-28"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "R/W", "SYNC", "φ0", "φ1", "Q3", "KEYLE", "DMA", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("apple2_iou_qfp_32", "IOU 341-0020 (QFP-32)", "QFP-32")

    return comp
