"""
APU 2A03 - Audio Processing Unit with 6502 core (APU) for NES
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "nes_apu",
        "APU 2A03",
        "Audio",
        "Audio Processing Unit with 6502 core (APU) for NES",
        width=240,
        height=260
    )

    # Package type (supports multiple variants)
    comp.package_type = "DIP-40"  # Default package

    # Add pins
    pin_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "R/W", "IRQ", "NMI", "CLK", "OUT1", "OUT2", "M2", "PHI0", "PHI1", "PHI2", "RES", "VCC", "GND", "VCC2", "GND2", "NC"]
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(pin_name, 15, 20, "io")

    # Add variants
    comp.add_variant("nes_apu_qfp_44", "APU 2A03 (QFP-44)", "QFP-44")

    return comp
