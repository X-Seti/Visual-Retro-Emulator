"""
MMU 341-0021 - Memory Management Unit (MMU) for Apple II
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "apple2_mmu",
        "MMU 341-0021",
        "Memory",
        "Memory Management Unit (MMU) for Apple II",
        width=180,
        height=162
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-28"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "R/W", "φ0", "VCC", "GND"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("apple2_mmu_qfp_32", "MMU 341-0021 (QFP-32)", "QFP-32")

    return comp
