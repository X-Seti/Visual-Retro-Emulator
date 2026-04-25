"""
X-Seti June13 2025 - Acorn BBC Micro Chipset Definitions
Visual Retro System Emulator Builder - BBC Micro Core Chips
"""

def add_bbc_micro_chips(generator):
    """Add BBC Micro chipset components"""
    
    # 6845 CRTC - Cathode Ray Tube Controller
    generator.add_chip(
        name="6845 CRTC",
        chip_id="bbc_crtc",
        category="Video",
        description="Cathode Ray Tube Controller for BBC Micro",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'}, {'name': 'MA3'},
            {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'}, {'name': 'MA7'},
            {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'}, {'name': 'MA11'},
            {'name': 'MA12'}, {'name': 'MA13'}, {'name': 'RA0'}, {'name': 'RA1'},
            {'name': 'RA2'}, {'name': 'RA3'}, {'name': 'RA4'}, {'name': 'HSYNC'},
            {'name': 'VSYNC'}, {'name': 'DE'}, {'name': 'CURSOR'}, {'name': 'LPSTB'},
            {'name': 'CS'}, {'name': 'RS'}, {'name': 'RW'}, {'name': 'E'},
            {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # Video ULA - Video processing
    generator.add_chip(
        name="Video ULA 12C021",
        chip_id="bbc_video_ula",
        category="Video",
        description="Video ULA for BBC Micro display processing",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'RW'}, {'name': 'φ2'}, {'name': 'ROMSEL'}, {'name': 'RAMSEL'},
            {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'CSYNC'},
            {'name': 'CURSOR'}, {'name': 'LPSTB'}, {'name': 'CRTC_E'}, {'name': 'CRTC_RS'},
            {'name': 'CRTC_RW'}, {'name': 'CRTC_CS'}, {'name': 'RA0'}, {'name': 'RA1'},
            {'name': 'RA2'}, {'name': 'RA3'}, {'name': 'MA0'}, {'name': 'MA12'},
            {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # System VIA - 6522 Versatile Interface Adapter
    generator.add_chip(
        name="System VIA 6522",
        chip_id="bbc_system_via",
        category="I/O",
        description="System VIA 6522 - Keyboard and system I/O",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'},
            {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'},
            {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'}, {'name': 'PB3'},
            {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'}, {'name': 'PB7'},
            {'name': 'CA1'}, {'name': 'CA2'}, {'name': 'CB1'}, {'name': 'CB2'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RS0'}, {'name': 'RS1'}, {'name': 'RS2'}, {'name': 'RS3'},
            {'name': 'CS1'}, {'name': 'CS2'}, {'name': 'φ2'}, {'name': 'RW'},
            {'name': 'IRQ'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # Electron ULA - For Acorn Electron
    generator.add_chip(
        name="Electron ULA",
        chip_id="bbc_electron_ula",
        category="Custom",
        description="ULA for Acorn Electron - combined video and system control",
        package_types=["DIP-40", "QFP-44"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'RW'}, {'name': 'φ2'}, {'name': 'IRQ'}, {'name': 'NMI'},
            {'name': 'RESET'}, {'name': 'RDY'}, {'name': 'RED'}, {'name': 'GREEN'},
            {'name': 'BLUE'}, {'name': 'CSYNC'}, {'name': 'SOUND'}, {'name': 'CAPS'},
            {'name': 'MOTOR'}, {'name': 'CASSETTE'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # Integra-B - BBC Master series
    generator.add_chip(
        name="Integra-B",
        chip_id="bbc_integra_b",
        category="Custom",
        description="Integra-B chip for BBC Master series",
        package_types=["PLCC-84", "QFP-84"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'RW'}, {'name': 'φ2'}, {'name': 'IRQ'}, {'name': 'NMI'},
            {'name': 'RESET'}, {'name': 'RDY'}, {'name': 'SYNC'}, {'name': 'BE'},
            {'name': 'ML'}, {'name': 'VP'}, {'name': 'VDA'}, {'name': 'VPA'},
            {'name': 'ROMSEL0'}, {'name': 'ROMSEL1'}, {'name': 'ROMSEL2'}, {'name': 'ROMSEL3'},
            {'name': 'RAMSEL0'}, {'name': 'RAMSEL1'}, {'name': 'RAMSEL2'}, {'name': 'RAMSEL3'},
            {'name': 'ACCCON0'}, {'name': 'ACCCON1'}, {'name': 'ACCCON2'}, {'name': 'ACCCON3'},
            {'name': 'ACCCON4'}, {'name': 'ACCCON5'}, {'name': 'ACCCON6'}, {'name': 'ACCCON7'},
            {'name': 'HAZEL0'}, {'name': 'HAZEL1'}, {'name': 'HAZEL2'}, {'name': 'HAZEL3'},
            {'name': 'TUBE'}, {'name': 'FC'}, {'name': 'FRQ'}, {'name': 'JIM'},
            {'name': 'FRED'}, {'name': 'SHEILA'}, {'name': 'OS'}, {'name': 'BASIC'},
            {'name': 'LANG'}, {'name': 'DFS'}, {'name': 'ADFS'}, {'name': 'ANFS'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'},
            {'name': 'VCC3'}, {'name': 'GND3'}, {'name': 'VDD'}, {'name': 'VSS'},
            {'name': 'CLK'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'PLL'},
            {'name': 'TEST'}, {'name': 'NC1'}, {'name': 'NC2'}, {'name': 'NC3'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("BBC Micro chipset definitions loaded")
    print("Available chips: 6845 CRTC, Video ULA, System VIA, Electron ULA, Integra-B")
