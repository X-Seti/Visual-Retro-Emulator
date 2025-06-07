#!/usr/bin/env python3
"""
May27, 2025 X-Seti - Retro Chip Image Generator
Generates realistic chip images for various retro computer components
Uses the fixed ChipPackageRenderer to create images for the component database
"""

import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QColor, QFont
from pathlib import Path

# Import the fixed chip renderer
try:
    from realistic_chip_renderer import ChipPackageRenderer
except ImportError:
    print("❌ Error: realistic_chip_renderer.py not found or has errors.")
    print("Please ensure you have the fixed version of the renderer.")
    sys.exit(1)


class RetroChipGenerator:
    """Generates realistic chip images for retro computer components"""

    def __init__(self):
        """Initialize the generator"""
        self.renderer = ChipPackageRenderer()
        self.chip_definitions = []
        self.output_dir = Path("images/components")

    def add_chip(self, name, chip_id, category, description, package_types, pins=None):
        """Add a chip definition to the generator

        Args:
            name: Display name of the chip
            chip_id: Unique component ID (used for filename)
            category: Component category (CPU, GPU, Sound, etc.)
            description: Short description
            package_types: List of package types (e.g. ['DIP-40', 'QFP-44'])
            pins: List of pin dictionaries (optional)
        """
        # Create a default pins list if not provided
        if pins is None:
            pins = []
            # Add default pins based on largest package
            max_pins = 0
            for pkg in package_types:
                try:
                    pin_count = int(pkg.split('-')[1])
                    max_pins = max(max_pins, pin_count)
                except (IndexError, ValueError):
                    continue

            # Generate generic pin names
            for i in range(1, max_pins + 1):
                pins.append({'name': f'P{i}'})

        # Add to our chip definitions
        self.chip_definitions.append({
            'name': name,
            'id': chip_id,
            'category': category,
            'description': description,
            'packages': package_types,
            'pins': pins
        })

        return self  # Allow chaining

    def add_amiga_chips(self):
        """Add Commodore Amiga chipset"""
        # Agnus - Address Generator
        self.add_chip(
            name="Agnus 8370/8371",
            chip_id="amiga_agnus",
            category="Custom",
            description="Address Generator / Animation Chip (Agnus)",
            package_types=["DIP-84", "PLCC-84"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
                {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
                {'name': 'RESET'}, {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'CSYNC'},
                {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '7M'}, {'name': 'XCLK'},
                {'name': 'XCLKEN'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'},
                {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'},
                {'name': 'RGA8'}, {'name': 'DMAL'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        # Denise - Display Encoder
        self.add_chip(
            name="Denise 8362",
            chip_id="amiga_denise",
            category="Video",
            description="Display Encoder Chip (Denise)",
            package_types=["DIP-48", "PLCC-48", "QFP-52"],
            pins=[
                {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'},
                {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'},
                {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'},
                {'name': 'M0'}, {'name': 'M1'}, {'name': 'M2'}, {'name': 'M3'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
                {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
                {'name': 'BURST'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'},
                {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'},
                {'name': 'RGA8'}, {'name': 'CCK'}, {'name': 'CDAC'}, {'name': 'RESET'},
                {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        # Paula - Ports and Audio
        self.add_chip(
            name="Paula 8364",
            chip_id="amiga_paula",
            category="Audio",
            description="Ports and Audio Chip (Paula)",
            package_types=["DIP-48", "PLCC-48"],
            pins=[
                {'name': 'POT0X'}, {'name': 'POT0Y'}, {'name': 'POT1X'}, {'name': 'POT1Y'},
                {'name': 'DKRD'}, {'name': 'DKWD'}, {'name': 'DKWE'}, {'name': 'TXD'},
                {'name': 'RXD'}, {'name': 'AUD0'}, {'name': 'AUD1'}, {'name': 'AUD2'},
                {'name': 'AUD3'}, {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'},
                {'name': 'P3'}, {'name': 'P4'}, {'name': 'P5'}, {'name': 'P6'},
                {'name': 'P7'}, {'name': 'P8'}, {'name': 'P9'}, {'name': 'D0'},
                {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'},
                {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'},
                {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'},
                {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'INT2'},
                {'name': 'INT3'}, {'name': 'INT6'}, {'name': 'RGA1'}, {'name': 'RGA2'},
                {'name': 'RGA3'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        return self

    def add_c64_chips(self):
        """Add Commodore 64 chipset"""
        # SID - Sound Interface Device
        self.add_chip(
            name="SID 6581/8580",
            chip_id="c64_sid",
            category="Audio",
            description="Sound Interface Device Chip (SID)",
            package_types=["DIP-28", "QFP-44"],
            pins=[
                {'name': 'CAP1A'}, {'name': 'CAP1B'}, {'name': 'CAP2A'}, {'name': 'CAP2B'},
                {'name': 'RES'}, {'name': 'φ2'}, {'name': 'R/W'}, {'name': 'CS'},
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'GND'}, {'name': 'D0'}, {'name': 'D1'},
                {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
                {'name': 'D6'}, {'name': 'D7'}, {'name': 'AUDIO'}, {'name': 'VCC'},
                {'name': 'POT X'}, {'name': 'POT Y'}, {'name': 'EXT IN'}, {'name': 'VDD'}
            ]
        )

        # VIC-II - Video Interface Chip
        self.add_chip(
            name="VIC-II 6567/6569",
            chip_id="c64_vic2",
            category="Video",
            description="Video Interface Chip II (VIC-II)",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'R/W'}, {'name': 'AEC'},
                {'name': 'IRQ'}, {'name': 'COLOR'}, {'name': 'SYNC'}, {'name': 'BA'},
                {'name': 'φ0'}, {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'LP'},
                {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        return self

        # CIA - Complex Interface Adapter
        self.add_chip(
            name="CIA 6526",
            chip_id="c64_cia",
            category="I/O",
            description="Complex Interface Adapter (CIA)",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'VSS'}, {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'},
                {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'},
                {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'},
                {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'},
                {'name': 'PB7'}, {'name': 'PC'}, {'name': 'TOD'}, {'name': 'RD'},
                {'name': 'CS'}, {'name': 'R/W'}, {'name': 'DB0'}, {'name': 'DB1'},
                {'name': 'DB2'}, {'name': 'DB3'}, {'name': 'DB4'}, {'name': 'DB5'},
                {'name': 'DB6'}, {'name': 'DB7'}, {'name': 'DC0'}, {'name': 'DC1'},
                {'name': 'DC2'}, {'name': 'DC3'}, {'name': 'FLAG'}, {'name': 'SP'},
                {'name': 'CNT'}, {'name': 'IRQ'}, {'name': 'RES'}, {'name': 'VCC'}
            ]
        )

        return self

    def add_bbc_chips(self):
        """Add BBC Micro and Master chipset"""
        # Acorn Electron ULA
        self.add_chip(
            name="Electron ULA",
            chip_id="bbc_electron_ula",
            category="Custom",
            description="Uncommitted Logic Array for Acorn Electron",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'φ2'}, {'name': 'R/W'},
                {'name': 'IRQ'}, {'name': 'CAS'}, {'name': 'RAS'}, {'name': 'SYNC'},
                {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'CSYNC'},
                {'name': 'ROM'}, {'name': 'RAM'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        # BBC Video ULA
        self.add_chip(
            name="Video ULA 6845",
            chip_id="bbc_video_ula",
            category="Video",
            description="Video ULA for BBC Micro",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'VSS'}, {'name': 'CLK'}, {'name': 'R/W'}, {'name': 'RS'},
                {'name': 'CS'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'},
                {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'},
                {'name': 'D7'}, {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'},
                {'name': 'MA3'}, {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'},
                {'name': 'MA7'}, {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'},
                {'name': 'MA11'}, {'name': 'MA12'}, {'name': 'MA13'}, {'name': 'RA0'},
                {'name': 'RA1'}, {'name': 'RA2'}, {'name': 'RA3'}, {'name': 'RA4'},
                {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'DE'}, {'name': 'CURSOR'},
                {'name': 'LPSTB'}, {'name': 'E'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        # BBC Master System VIA
        self.add_chip(
            name="System VIA 6522",
            chip_id="bbc_system_via",
            category="I/O",
            description="System Versatile Interface Adapter for BBC Micro",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'VSS'}, {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'},
                {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'},
                {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'},
                {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'},
                {'name': 'PB7'}, {'name': 'CB1'}, {'name': 'CB2'}, {'name': 'CA1'},
                {'name': 'CA2'}, {'name': 'RS0'}, {'name': 'RS1'}, {'name': 'RS2'},
                {'name': 'RS3'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'},
                {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'},
                {'name': 'D7'}, {'name': 'RES'}, {'name': 'φ2'}, {'name': 'CS1'},
                {'name': 'CS2'}, {'name': 'R/W'}, {'name': 'IRQ'}, {'name': 'VCC'}
            ]
        )

        # BBC Master CRTC
        self.add_chip(
            name="CRTC 6845",
            chip_id="bbc_crtc",
            category="Video",
            description="Cathode Ray Tube Controller for BBC Micro",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'VSS'}, {'name': 'CLK'}, {'name': 'R/W'}, {'name': 'RS'},
                {'name': 'CS'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'},
                {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'},
                {'name': 'D7'}, {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'},
                {'name': 'MA3'}, {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'},
                {'name': 'MA7'}, {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'},
                {'name': 'MA11'}, {'name': 'MA12'}, {'name': 'MA13'}, {'name': 'RA0'},
                {'name': 'RA1'}, {'name': 'RA2'}, {'name': 'RA3'}, {'name': 'RA4'},
                {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'DE'}, {'name': 'CURSOR'},
                {'name': 'LPSTB'}, {'name': 'E'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        # BBC Master INTEGRA-B
        self.add_chip(
            name="INTEGRA-B",
            chip_id="bbc_integra_b",
            category="Custom",
            description="ASIC for BBC Master Integrating Multiple Functions",
            package_types=["QFP-84", "PLCC-84"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'ROMSEL'}, {'name': 'ACCCON'}, {'name': 'VDUSEL'}, {'name': 'SHEILASEL'},
                {'name': 'CLK2MHZ'}, {'name': 'CLK1MHZ'}, {'name': 'VIDPROC'}, {'name': 'SOUND'},
                {'name': 'DISEN'}, {'name': 'CSY'}, {'name': 'CS'}, {'name': 'RW'},
                {'name': 'IRQ'}, {'name': '16MHZ'}, {'name': '8MHZ'}, {'name': '4MHZ'},
                {'name': '2MHZ'}, {'name': '1MHZ'}, {'name': 'RST'}, {'name': 'VCC'},
                {'name': 'GND'}
            ]
        )

        return self

    def add_zx_spectrum_chips(self):
        """Add ZX Spectrum chipset"""
        # ULA - Uncommitted Logic Array
        self.add_chip(
            name="ULA Ferranti",
            chip_id="spectrum_ula",
            category="Custom",
            description="Uncommitted Logic Array (ULA) for ZX Spectrum",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'RD'}, {'name': 'WR'},
                {'name': 'INT'}, {'name': 'CLOCK'}, {'name': 'CAS'}, {'name': 'RAS'},
                {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'BRIGHT'},
                {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        return self

    def add_nintendo_nes_chips(self):
        """Add Nintendo NES chipset"""
        # PPU - Picture Processing Unit
        self.add_chip(
            name="PPU 2C02",
            chip_id="nes_ppu",
            category="Video",
            description="Picture Processing Unit (PPU) for NES",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'},
                {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'},
                {'name': 'ALE'}, {'name': 'R/W'}, {'name': 'DB0'}, {'name': 'DB1'},
                {'name': 'DB2'}, {'name': 'DB3'}, {'name': 'DB4'}, {'name': 'DB5'},
                {'name': 'DB6'}, {'name': 'DB7'}, {'name': 'INT'}, {'name': 'VRAM /CE'},
                {'name': 'VRAM A10'}, {'name': 'VRAM A11'}, {'name': 'EXT0'}, {'name': 'EXT1'},
                {'name': 'EXT2'}, {'name': 'EXT3'}, {'name': 'EXT4'}, {'name': 'CLK'},
                {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'SYNC'},
                {'name': 'HBLANK'}, {'name': 'VBLANK'}, {'name': 'RES'}, {'name': 'VCC'},
                {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'NC'}
            ]
        )

        # APU - Audio Processing Unit
        self.add_chip(
            name="APU 2A03",
            chip_id="nes_apu",
            category="Audio",
            description="Audio Processing Unit with 6502 core (APU) for NES",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'R/W'}, {'name': 'IRQ'}, {'name': 'NMI'}, {'name': 'CLK'},
                {'name': 'OUT1'}, {'name': 'OUT2'}, {'name': 'M2'}, {'name': 'PHI0'},
                {'name': 'PHI1'}, {'name': 'PHI2'}, {'name': 'RES'}, {'name': 'VCC'},
                {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'NC'}
            ]
        )

        return self

    def add_sega_chips(self):
        """Add Sega Genesis/Mega Drive chipset"""
        # VDP - Video Display Processor
        self.add_chip(
            name="VDP YM7101",
            chip_id="genesis_vdp",
            category="Video",
            description="Video Display Processor (VDP) for Sega Genesis",
            package_types=["QFP-64", "QFP-68"],
            pins=[
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
                {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'A16'}, {'name': 'CE'}, {'name': 'OE'}, {'name': 'WE'},
                {'name': 'UB'}, {'name': 'LB'}, {'name': 'CAS0'}, {'name': 'CAS1'},
                {'name': 'RAS'}, {'name': 'CLK'}, {'name': 'IPL0'}, {'name': 'IPL1'},
                {'name': 'IPL2'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'},
                {'name': 'MCLK'}, {'name': 'SCLK'}, {'name': 'RED'}, {'name': 'GREEN'},
                {'name': 'BLUE'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'},
                {'name': 'GND2'}, {'name': 'NC'}, {'name': 'NC'}, {'name': 'NC'}

                ]
            )

        return self

    def add_atari_chips(self):
        """Add Atari chipset"""
        # ANTIC - Alphanumeric Television Interface Controller
        self.add_chip(
            name="ANTIC CO12296",
            chip_id="atari_antic",
            category="Video",
            description="Alphanumeric Television Interface Controller for Atari 8-bit",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'RDY'}, {'name': 'REF'}, {'name': 'HALT'}, {'name': 'R/W'},
                {'name': 'φ0'}, {'name': 'φ2'}, {'name': 'VSYNC'}, {'name': 'HSYNC'},
                {'name': 'NMI'}, {'name': 'IRQ'}, {'name': 'RST'}, {'name': 'AN0'},
                {'name': 'AN1'}, {'name': 'AN2'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        # POKEY - Pot Keyboard Integrated Circuit
        self.add_chip(
            name="POKEY C012294",
            chip_id="atari_pokey",
            category="Audio",
            description="Pot Keyboard Integrated Circuit for Atari 8-bit",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'}, {'name': 'P3'},
                {'name': 'P4'}, {'name': 'P5'}, {'name': 'P6'}, {'name': 'P7'},
                {'name': 'K0'}, {'name': 'K1'}, {'name': 'K2'}, {'name': 'K3'},
                {'name': 'K4'}, {'name': 'K5'}, {'name': 'POT0'}, {'name': 'POT1'},
                {'name': 'POT2'}, {'name': 'POT3'}, {'name': 'POT4'}, {'name': 'POT5'},
                {'name': 'POT6'}, {'name': 'POT7'}, {'name': 'AUDIO'}, {'name': 'BID'},
                {'name': 'CS'}, {'name': 'R/W'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        # GTIA - Graphics Television Interface Adapter
        self.add_chip(
            name="GTIA CO14889",
            chip_id="atari_gtia",
            category="Video",
            description="Graphics Television Interface Adapter for Atari 8-bit",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'D0'}, {'name': 'D1'},
                {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'},
                {'name': 'D6'}, {'name': 'D7'}, {'name': 'CS'}, {'name': 'R/W'},
                {'name': 'φ0'}, {'name': 'AN0'}, {'name': 'AN1'}, {'name': 'AN2'},
                {'name': 'AN3'}, {'name': 'CONT'}, {'name': 'TRIG0'}, {'name': 'TRIG1'},
                {'name': 'TRIG2'}, {'name': 'TRIG3'}, {'name': 'CONS'}, {'name': 'PAL'},
                {'name': 'LUMA0'}, {'name': 'LUMA1'}, {'name': 'LUMA2'}, {'name': 'CHROMA'},
                {'name': 'BURST'}, {'name': 'OSC'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        return self

    def add_oric_chips(self):
        """Add Oric-1/Atmos chipset"""
        # ULA - Uncommitted Logic Array
        self.add_chip(
            name="Oric ULA",
            chip_id="oric_ula",
            category="Custom",
            description="Uncommitted Logic Array for Oric computers",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'R/W'}, {'name': 'MUX'}, {'name': 'CAS'}, {'name': 'RAS'},
                {'name': 'MAP'}, {'name': 'PHI'}, {'name': 'WARP'}, {'name': 'PHI2'},
                {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'SYNC'},
                {'name': 'ROM CS'}, {'name': 'I/O CS'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        return self


        # YM2612 - FM Sound Generator
        self.add_chip(
            name="YM2612 FM",
            chip_id="genesis_ym2612",
            category="Audio",
            description="FM Sound Generator for Sega Genesis",
            package_types=["DIP-24", "QFP-28"],
            pins=[
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'IC'}, {'name': 'CS'},
                {'name': 'WR'}, {'name': 'RD'}, {'name': 'IRQ'}, {'name': 'φM'},
                {'name': 'φC'}, {'name': 'MO'}, {'name': 'SO'}, {'name': 'VCC'},
                {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'NC'}
            ]
        )

        return self

    def add_apple_ii_chips(self):
        """Add Apple II chipset"""
        # IOU - Input/Output Unit
        self.add_chip(
            name="IOU 341-0020",
            chip_id="apple2_iou",
            category="I/O",
            description="Input/Output Unit (IOU) for Apple II",
            package_types=["DIP-28", "QFP-32"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'D0'},
                {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'},
                {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'R/W'},
                {'name': 'SYNC'}, {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'Q3'},
                {'name': 'KEYLE'}, {'name': 'DMA'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        # MMU - Memory Management Unit
        self.add_chip(
            name="MMU 341-0021",
            chip_id="apple2_mmu",
            category="Memory",
            description="Memory Management Unit (MMU) for Apple II",
            package_types=["DIP-28", "QFP-32"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'R/W'}, {'name': 'φ0'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        return self

    def add_msx_chips(self):
        """Add MSX chipset"""
        # TMS9918A - Video Display Processor
        self.add_chip(
            name="TMS9918A",
            chip_id="msx_tms9918a",
            category="Video",
            description="Video Display Processor for MSX/Coleco/TI99",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'},
                {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'},
                {'name': 'BD0'}, {'name': 'BD1'}, {'name': 'BD2'}, {'name': 'BD3'},
                {'name': 'BD4'}, {'name': 'BD5'}, {'name': 'BD6'}, {'name': 'BD7'},
                {'name': 'MODE'}, {'name': 'CSW'}, {'name': 'CSR'}, {'name': 'INT'},
                {'name': 'RD'}, {'name': 'CD'}, {'name': 'EXTVDP'}, {'name': 'COMVID'},
                {'name': 'GROM'}, {'name': 'CPUCLK'}, {'name': 'XIN'}, {'name': 'XOUT'},
                {'name': 'R'}, {'name': 'G'}, {'name': 'B'}, {'name': 'Y'},
                {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'VCC'}, {'name': 'GND'},
                {'name': 'RESET'}, {'name': 'VRAM /CS'}, {'name': 'NC'}, {'name': 'NC'}
            ]
        )
        # AY-3-8910 - Programmable Sound Generator
        self.add_chip(
            name="AY-3-8910",
            chip_id="msx_ay3_8910",
            category="Audio",
            description="Programmable Sound Generator for MSX",
            package_types=["DIP-28", "DIP-40"],
            pins=[
                {'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'}, {'name': 'DA3'},
                {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'}, {'name': 'DA7'},
                {'name': 'BC1'}, {'name': 'BC2'}, {'name': 'BDIR'}, {'name': 'A8'},
                {'name': 'A9'}, {'name': 'TEST1'}, {'name': 'TEST2'}, {'name': 'IOA0'},
                {'name': 'IOA1'}, {'name': 'IOA2'}, {'name': 'IOA3'}, {'name': 'IOA4'},
                {'name': 'IOA5'}, {'name': 'IOA6'}, {'name': 'IOA7'}, {'name': 'ANALOG A'},
                {'name': 'ANALOG B'}, {'name': 'ANALOG C'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )
        # S1985 - MSX Engine (S1985)
        self.add_chip(
            name="Yamaha S1985",
            chip_id="msx_s1985",
            category="Custom",
            description="MSX-Engine for MSX2 and up (integrated circuits)",
            package_types=["DIP-64", "QFP-64"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'IORQ'}, {'name': 'MREQ'}, {'name': 'RD'}, {'name': 'WR'},
                {'name': 'INT'}, {'name': 'BUSDIR'}, {'name': 'CSROM'}, {'name': 'SLTSL0'},
                {'name': 'SLTSL1'}, {'name': 'SLTSL2'}, {'name': 'SLTSL3'}, {'name': 'RESET'},
                {'name': 'RFSH'}, {'name': 'WAIT'}, {'name': 'M1'}, {'name': 'BUSAK'},
                {'name': 'CLK'}, {'name': 'SW1'}, {'name': 'SW2'}, {'name': 'CAPS'},
                {'name': 'KANA'}, {'name': 'CAS'}, {'name': 'RAS'}, {'name': 'ROMCS'},
                {'name': 'MUX'}, {'name': 'KAN'}, {'name': 'CS12'}, {'name': 'CS3'},
                {'name': 'CASW'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'},
                {'name': 'NC'}, {'name': 'NC'}, {'name': 'NC'}, {'name': 'NC'}
            ]
        )

        return self

    def add_ti99_chips(self):
        """Add TI-99/4A chipset"""
        # TMS9900 - 16-bit CPU
        self.add_chip(
            name="TMS9900",
            chip_id="ti99_tms9900",
            category="CPU",
            description="16-bit CPU for TI-99/4A",
            package_types=["DIP-64", "QFP-64"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
                {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
                {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
                {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
                {'name': 'MEMEN'}, {'name': 'WE'}, {'name': 'DBIN'}, {'name': 'IAQ'},
                {'name': 'INTREQ'}, {'name': 'READY'}, {'name': 'WAIT'}, {'name': 'LOAD'},
                {'name': 'HOLD'}, {'name': 'HOLDA'}, {'name': 'RESET'}, {'name': 'CRUCLK'},
                {'name': 'CRUOUT'}, {'name': 'CRUIN'}, {'name': 'φ1'}, {'name': 'φ2'},
                {'name': 'φ3'}, {'name': 'φ4'}, {'name': 'VCC'}, {'name': 'GND'},
                {'name': 'NC'}, {'name': 'NC'}, {'name': 'NC'}, {'name': 'NC'},
                {'name': 'NC'}, {'name': 'NC'}, {'name': 'NC'}, {'name': 'NC'}
            ]
        )
        # TMS9901 - Programmable Systems Interface
        self.add_chip(
            name="TMS9901",
            chip_id="ti99_tms9901",
            category="I/O",
            description="Programmable Systems Interface for TI-99/4A",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'CRUOUT'}, {'name': 'CRUIN'}, {'name': 'CRUCLK'}, {'name': 'CE'},
                {'name': 'S0'}, {'name': 'S1'}, {'name': 'S2'}, {'name': 'S3'},
                {'name': 'S4'}, {'name': 'INT1'}, {'name': 'INT2'}, {'name': 'INT3'},
                {'name': 'INT4'}, {'name': 'INT5'}, {'name': 'INT6'}, {'name': 'INT7'},
                {'name': 'INT8'}, {'name': 'INT9'}, {'name': 'INT10'}, {'name': 'INT11'},
                {'name': 'INT12'}, {'name': 'INT13'}, {'name': 'INT14'}, {'name': 'INT15'},
                {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'}, {'name': 'P3'},
                {'name': 'P4'}, {'name': 'P5'}, {'name': 'P6'}, {'name': 'P7'},
                {'name': 'INTREQ'}, {'name': 'RESET'}, {'name': 'φ1'}, {'name': 'φ2'},
                {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}, {'name': 'NC'}
            ]
        )

        return self

    def add_dragon_chips(self):
        """Add Dragon 32/64 chipset"""
        # SAM - Synchronous Address Multiplexer
        self.add_chip(
            name="MC6883/SN74LS783 (SAM)",
            chip_id="dragon_sam",
            category="Custom",
            description="Synchronous Address Multiplexer for Dragon/CoCo",
            package_types=["DIP-40", "QFP-44"],
            pins=[
                {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
                {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
                {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
                {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
                {'name': 'Z80'}, {'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'},
                {'name': 'DA3'}, {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'},
                {'name': 'DA7'}, {'name': 'Q'}, {'name': 'E'}, {'name': 'HS'},
                {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'S1'}, {'name': 'S0'},
                {'name': 'R/W'}, {'name': 'SLENB'}, {'name': 'FIELD'}, {'name': 'RAS0'},
                {'name': 'RASE'}, {'name': 'RAS1'}, {'name': 'VCC'}, {'name': 'GND'}
            ]
        )

        return self

    def generate_images(self):
        """Generate images for all defined chips"""
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True, parents=True)

        # Create a dummy component definition class
        class ComponentDef:
            def __init__(self, name, comp_id, category, pins):
                self.name = name
                self.component_id = comp_id
                self.category = category
                self.pins = pins

        # Initialize QApplication if needed
        if not QApplication.instance():
            app = QApplication([])

        print(f"🎨 Generating realistic chip images for {len(self.chip_definitions)} components...")

        for chip in self.chip_definitions:
            print(f"  🔧 Creating images for {chip['name']}...")

            comp_def = ComponentDef(
                chip['name'],
                chip['id'],
                chip['category'],
                chip['pins']
            )

            for package in chip['packages']:
                print(f"    📦 Package: {package}")

                # Generate image
                pixmap = self.renderer.create_chip_image(comp_def, package, 400)

                # Save image
                filename = f"{self.output_dir}/{chip['id']}_{package.lower().replace('-', '_')}.png"
                pixmap.save(filename)
                print(f"      💾 Saved: {filename}")

        print("✅ All chip images generated!")
        print(f"📁 Images saved in: {self.output_dir}/")

        return True

    def get_component_definitions(self):
        """Get component definitions that can be used for creating component files"""
        component_templates = []

        for chip in self.chip_definitions:
            template = f'''"""
{chip['name']} - {chip['description']}
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "{chip['id']}",
        "{chip['name']}",
        "{chip['category']}",
        "{chip['description']}",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "{chip['packages'][0]}"  # Default package

    # Add pins
    pin_list = {str([p['name'] for p in chip['pins']]).replace("'", '"')}
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    {self._generate_variants_code(chip)}

    return comp
'''
            component_templates.append((chip['id'], template))

        return component_templates

    def _generate_variants_code(self, chip):
        """Generate code for package variants"""
        if len(chip['packages']) <= 1:
            return "# No variants"

        variants_code = []
        for pkg in chip['packages'][1:]:
            variant_id = f"{chip['id']}_{pkg.lower().replace('-', '_')}"
            variant_name = f"{chip['name']} ({pkg})"
            variants_code.append(f'comp.add_variant("{variant_id}", "{variant_name}", "{pkg}")')

        return "\n    ".join(variants_code)

    def create_component_files(self, base_dir="components"):
        """Create component definition files in the appropriate directories"""
        print(f"📝 Creating component definition files...")

        component_defs = self.get_component_definitions()
        created_files = []

        for comp_id, template in component_defs:
            # Determine the appropriate directory based on ID prefix
            directory = None

            if comp_id.startswith("amiga_"):
                directory = Path(base_dir) / "amiga"
            elif comp_id.startswith("c64_"):
                directory = Path(base_dir) / "commodore"
            else:
                directory = Path(base_dir) / "custom"

            # Ensure directory exists
            directory.mkdir(exist_ok=True, parents=True)

            # Create filename
            filename = directory / f"{comp_id}.py"

            # Write file
            with open(filename, "w") as f:
                f.write(template)

            created_files.append(str(filename))
            print(f"  ✅ Created: {filename}")

        print(f"📁 Created {len(created_files)} component definition files")
        return created_files


def main():
    """Main function"""
    print("🖥️  Retro Chip Image Generator")
    print("=" * 60)

    # Create generator
    generator = RetroChipGenerator()

    # Add chip definitions for various systems
    print("🔍 Adding chip definitions...")

    # Only use the methods that are known to work
    generator.add_amiga_chips()
    generator.add_c64_chips()
    generator.add_bbc_chips()
    generator.add_zx_spectrum_chips()
    generator.add_nintendo_nes_chips()
    generator.add_sega_chips()
    if hasattr(generator, 'add_atari_chips'):
        generator.add_atari_chips()

    # Check if these methods exist before calling
    if hasattr(generator, 'add_apple_ii_chips'):
        generator.add_apple_ii_chips()
    elif hasattr(generator, 'add_apple2_chips'):  # Try alternative name
        generator.add_apple2_chips()

    # Check if these methods exist before calling
    if hasattr(generator, 'add_msx_chips'):
        generator.add_msx_chips()

    if hasattr(generator, 'add_ti99_chips'):
        generator.add_ti99_chips()

    if hasattr(generator, 'add_dragon_chips'):
        generator.add_dragon_chips()

    if hasattr(generator, 'add_oric_chips'):
        generator.add_oric_chips()

    # Generate images
    print("\n🎨 Generating images...")
    generator.generate_images()

    # Create component definition files
    print("\n📄 Creating component definition files...")
    generator.create_component_files()

    print("\n🎉 All done! Your retro chip collection is ready.")
    print("=" * 60)
    print("💡 TIP: Add these components to your projects to use the realistic chip images.")

    return 0


if __name__ == "__main__":
    sys.exit(main())




