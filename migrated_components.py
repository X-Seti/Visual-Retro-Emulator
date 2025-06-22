#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Migrated Component Definitions
Generated from better chipsets/ folder designs
"""

# Component library organized by system
COMPONENT_LIBRARY = {
    "amiga": [
        {
            "name": "Agnus 8367/8372",
            "chip_id": "amiga_agnus",
            "category": "Custom",
            "description": "Address Generator Unit (Agnus) - DMA Controller and Memory Management",
            "package_types": ['DIP-84', 'PLCC-84'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'OWN'}, {'name': 'BERR'}, {'name': 'HALT'}, {'name': 'RESET'}, {'name': 'CIAA'}, {'name': 'CIAB'}, {'name': 'EXPNCS'}, {'name': 'AUTOCONF'}, {'name': '7MHZ'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': 'C1'}, {'name': 'C3'}, {'name': 'CDAC'}, {'name': 'CSYNC'}, {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VDDQ'}, {'name': 'VSSQ'}, {'name': 'VREF'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'WE'}, {'name': 'DMAL'}, {'name': 'DMAG'}, {'name': 'DMAS'}, {'name': 'DKRD'}, {'name': 'DKWD'}, {'name': 'INT2'}, {'name': 'INT6'}, {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'BCLK'}, {'name': 'BDIR'}]
        },
        {
            "name": "Paula 8364",
            "chip_id": "amiga_paula",
            "category": "Audio",
            "description": "Ports, Audio, UART, and Logic (Paula) - Audio and I/O Controller",
            "package_types": ['DIP-48', 'PLCC-48'],
            "pins": [{'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'INT2'}, {'name': 'INT3'}, {'name': 'INT6'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': 'DMAL'}, {'name': 'DMAG'}, {'name': 'LEFT'}, {'name': 'RIGHT'}, {'name': 'LPEN'}, {'name': 'LPENCLK'}, {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'AVDD'}, {'name': 'AGND'}]
        },
        {
            "name": "Denise 8362/8373",
            "chip_id": "amiga_denise",
            "category": "Video",
            "description": "Display Enable (Denise) - Video Output and Sprite Control",
            "package_types": ['DIP-48', 'PLCC-48', 'QFP-52'],
            "pins": [{'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'}, {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'}, {'name': 'RGA8'}, {'name': 'RGA9'}, {'name': 'DMAL'}, {'name': 'DMA'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': 'CDAC'}, {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'}, {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'}, {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'}, {'name': 'I0'}, {'name': 'I1'}, {'name': 'I2'}, {'name': 'I3'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'}, {'name': 'BLANK'}, {'name': 'BURST'}, {'name': 'GENLOCK'}, {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}]
        },
        {
            "name": "Gary 8365",
            "chip_id": "amiga_gary",
            "category": "Custom",
            "description": "Gate Array Logic Unit - System Control and Decoding",
            "package_types": ['PLCC-68', 'QFP-68'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'BR'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'FC0'}, {'name': 'FC1'}, {'name': 'FC2'}, {'name': 'BERR'}, {'name': 'HALT'}, {'name': 'RESET'}, {'name': 'EXPAN'}, {'name': 'CIAA'}, {'name': 'CIAB'}, {'name': 'OVR'}, {'name': 'KBRESET'}, {'name': 'POWER'}, {'name': 'LED'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VCC3'}, {'name': 'GND3'}, {'name': 'VREF'}]
        },
        {
            "name": "Alice 8374",
            "chip_id": "amiga_alice",
            "category": "Video",
            "description": "Advanced Graphics Architecture (AGA) Alice Chip",
            "package_types": ['PLCC-84', 'QFP-100'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'D16'}, {'name': 'D17'}, {'name': 'D18'}, {'name': 'D19'}, {'name': 'D20'}, {'name': 'D21'}, {'name': 'D22'}, {'name': 'D23'}, {'name': 'D24'}, {'name': 'D25'}, {'name': 'D26'}, {'name': 'D27'}, {'name': 'D28'}, {'name': 'D29'}, {'name': 'D30'}, {'name': 'D31'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'}, {'name': 'A21'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'WE'}, {'name': 'OE'}, {'name': 'DMAL'}, {'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'}, {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'}, {'name': 'RGA8'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': 'CDAC'}, {'name': 'CSYNC'}, {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDDQ'}, {'name': 'VSSQ'}, {'name': 'VCC3'}, {'name': 'GND3'}, {'name': 'VREF'}]
        },
        {
            "name": "Lisa 8375",
            "chip_id": "amiga_lisa",
            "category": "Custom",
            "description": "Advanced Graphics Architecture (AGA) Lisa Chip",
            "package_types": ['PLCC-68', 'QFP-80'],
            "pins": [{'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'}, {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'}, {'name': 'RGA8'}, {'name': 'RGA9'}, {'name': 'DMAL'}, {'name': 'DMA'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': 'CDAC'}, {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'}, {'name': 'R4'}, {'name': 'R5'}, {'name': 'R6'}, {'name': 'R7'}, {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'}, {'name': 'G4'}, {'name': 'G5'}, {'name': 'G6'}, {'name': 'G7'}, {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'}, {'name': 'B4'}, {'name': 'B5'}, {'name': 'B6'}, {'name': 'B7'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'}, {'name': 'BLANK'}, {'name': 'BURST'}, {'name': 'GENLOCK'}, {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}]
        },
        {
            "name": "Ramsey 8372",
            "chip_id": "amiga_ramsey",
            "category": "Custom",
            "description": "RAM Controller and System Control",
            "package_types": ['PLCC-68', 'QFP-80'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'RAS2'}, {'name': 'RAS3'}, {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'CAS2'}, {'name': 'CAS3'}, {'name': 'WE0'}, {'name': 'WE1'}, {'name': 'WE2'}, {'name': 'WE3'}, {'name': 'OE'}, {'name': 'RAMEN'}, {'name': 'REFRESH'}, {'name': 'DRAM'}, {'name': 'SRAM'}, {'name': 'ROM'}, {'name': 'FASTRAM'}, {'name': 'CHIPMEM'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}]
        },
        {
            "name": "Buster 8364",
            "chip_id": "amiga_buster",
            "category": "Custom",
            "description": "Bus Controller and DMA Arbiter",
            "package_types": ['PLCC-52', 'QFP-64'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'BR'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'FC0'}, {'name': 'FC1'}, {'name': 'FC2'}, {'name': 'BERR'}, {'name': 'HALT'}, {'name': 'RESET'}, {'name': 'EXPAN'}, {'name': 'AUTOCONF'}, {'name': 'BURST'}, {'name': 'SIZE0'}, {'name': 'SIZE1'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VREF'}]
        },
    ],
    "apple_ii": [
        {
            "name": "IOU 344-0020",
            "chip_id": "apple2_iou",
            "category": "I/O",
            "description": "Input/Output Unit for Apple IIe/IIc",
            "package_types": ['DIP-28', 'QFP-32'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'R/W'}, {'name': 'DEV'}, {'name': 'STR'}, {'name': 'KBD'}, {'name': 'GAME'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}]
        },
        {
            "name": "MMU 344-0030",
            "chip_id": "apple2_mmu",
            "category": "Custom",
            "description": "Memory Management Unit for Apple IIe/IIc",
            "package_types": ['DIP-28', 'QFP-32'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'BANK1'}, {'name': 'BANK2'}, {'name': 'AUXSEL'}, {'name': 'R/W'}, {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'RAMRD'}, {'name': 'RAMWR'}, {'name': 'INTCX'}, {'name': 'SLOTC3'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "Video Scanner 344-0024",
            "chip_id": "apple2_video",
            "category": "Video",
            "description": "Video Scanner and Character Generator",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'TEXT'}, {'name': 'MIX'}, {'name': 'PAGE2'}, {'name': 'HIRES'}, {'name': 'AN0'}, {'name': 'AN1'}, {'name': 'AN2'}, {'name': 'AN3'}, {'name': 'COMP'}, {'name': 'COLOR'}, {'name': 'LUM'}, {'name': 'SERR'}, {'name': '14M'}, {'name': '7M'}, {'name': 'φ0'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}]
        },
        {
            "name": "Disk II Controller P5A",
            "chip_id": "apple2_disk",
            "category": "Storage",
            "description": "Disk II Floppy Drive Controller",
            "package_types": ['DIP-20'],
            "pins": [{'name': 'PHASE0'}, {'name': 'PHASE1'}, {'name': 'PHASE2'}, {'name': 'PHASE3'}, {'name': 'MOTOR'}, {'name': 'DRIVE1'}, {'name': 'DRIVE2'}, {'name': 'Q3'}, {'name': 'DATA'}, {'name': 'WRITE'}, {'name': 'PROTECT'}, {'name': 'TRACK0'}, {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'ENABLE'}, {'name': 'READY'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC1'}, {'name': 'NC2'}]
        },
        {
            "name": "Language Card",
            "chip_id": "apple2_langcard",
            "category": "Memory",
            "description": "16K RAM Expansion Card",
            "package_types": ['Card Edge'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'R/W'}, {'name': 'φ0'}, {'name': 'φ1'}, {'name': 'RESET'}, {'name': 'IRQ'}, {'name': 'NMI'}, {'name': '+5V'}, {'name': '+12V'}, {'name': '-5V'}, {'name': '-12V'}, {'name': 'GND'}, {'name': 'SLOT'}]
        },
    ],
    "atari": [
        {
            "name": "ANTIC CO12296",
            "chip_id": "atari_antic",
            "category": "Video",
            "description": "Alphanumeric Television Interface Controller for Atari 8-bit",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'RDY'}, {'name': 'REF'}, {'name': 'HALT'}, {'name': 'R/W'}, {'name': 'φ0'}, {'name': 'φ2'}, {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'NMI'}, {'name': 'IRQ'}, {'name': 'RST'}, {'name': 'AN0'}, {'name': 'AN1'}, {'name': 'AN2'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "POKEY C012294",
            "chip_id": "atari_pokey",
            "category": "Audio",
            "description": "Pot Keyboard Integrated Circuit for Atari 8-bit",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'}, {'name': 'P3'}, {'name': 'P4'}, {'name': 'P5'}, {'name': 'P6'}, {'name': 'P7'}, {'name': 'K0'}, {'name': 'K1'}, {'name': 'K2'}, {'name': 'K3'}, {'name': 'K4'}, {'name': 'K5'}, {'name': 'POT0'}, {'name': 'POT1'}, {'name': 'POT2'}, {'name': 'POT3'}, {'name': 'POT4'}, {'name': 'POT5'}, {'name': 'POT6'}, {'name': 'POT7'}, {'name': 'AUDIO'}, {'name': 'BID'}, {'name': 'CS'}, {'name': 'R/W'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "GTIA CO14889",
            "chip_id": "atari_gtia",
            "category": "Video",
            "description": "Graphics Television Interface Adapter for Atari 8-bit",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'LUM0'}, {'name': 'LUM1'}, {'name': 'LUM2'}, {'name': 'LUM3'}, {'name': 'COL0'}, {'name': 'COL1'}, {'name': 'COL2'}, {'name': 'COL3'}, {'name': 'R'}, {'name': 'G'}, {'name': 'B'}, {'name': 'SYNC'}, {'name': 'LUMI'}, {'name': 'CHROMA'}, {'name': 'COMPOSITE'}, {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'}, {'name': 'P3'}, {'name': 'M0'}, {'name': 'M1'}, {'name': 'M2'}, {'name': 'M3'}, {'name': 'PF0'}, {'name': 'PF1'}, {'name': 'PF2'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "PIA 6520",
            "chip_id": "atari_pia",
            "category": "I/O",
            "description": "Peripheral Interface Adapter - Keyboard and joystick interface",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'VSS'}, {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'}, {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'}, {'name': 'PB7'}, {'name': 'CB1'}, {'name': 'CB2'}, {'name': 'VDD'}, {'name': 'IRQA'}, {'name': 'IRQB'}, {'name': 'RS0'}, {'name': 'RS1'}, {'name': 'RESET'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'E'}, {'name': 'CS0'}, {'name': 'CS1'}, {'name': 'CS2'}, {'name': 'R/W'}, {'name': 'CA1'}, {'name': 'CA2'}]
        },
    ],
    "c64": [
        {
            "name": "SID 6581/8580",
            "chip_id": "c64_sid",
            "category": "Audio",
            "description": "Sound Interface Device Chip (SID) - 3-channel synthesizer",
            "package_types": ['DIP-28', 'QFP-44'],
            "pins": [{'name': 'CAP1A'}, {'name': 'CAP1B'}, {'name': 'CAP2A'}, {'name': 'CAP2B'}, {'name': 'RES'}, {'name': 'φ2'}, {'name': 'R/W'}, {'name': 'CS'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'GND'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'AUDIO'}, {'name': 'VCC'}, {'name': 'POT X'}, {'name': 'POT Y'}, {'name': 'EXT IN'}, {'name': 'VDD'}]
        },
        {
            "name": "VIC-II 6567/6569",
            "chip_id": "c64_vic2",
            "category": "Video",
            "description": "Video Interface Chip II (VIC-II) - Graphics and video controller",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'R/W'}, {'name': 'AEC'}, {'name': 'IRQ'}, {'name': 'COLOR'}, {'name': 'SYNC'}, {'name': 'BA'}, {'name': 'φ0'}, {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'LP'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "CIA 6526",
            "chip_id": "c64_cia",
            "category": "I/O",
            "description": "Complex Interface Adapter (CIA) - I/O and timer controller",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'VSS'}, {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'}, {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'}, {'name': 'PB7'}, {'name': 'PC'}, {'name': 'TOD'}, {'name': 'VDD'}, {'name': 'IRQ'}, {'name': 'R/W'}, {'name': 'CS'}, {'name': 'φ2'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'FLAG'}, {'name': 'SP'}, {'name': 'CNT'}, {'name': 'RES'}]
        },
        {
            "name": "PLA 906114-01",
            "chip_id": "c64_pla",
            "category": "Custom",
            "description": "Programmable Logic Array - Memory and I/O decoding",
            "package_types": ['DIP-28', 'PLCC-28'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'CASRAM'}, {'name': 'BASIC'}, {'name': 'KERNAL'}, {'name': 'CHAROM'}, {'name': 'GR/W'}, {'name': 'HIRAM'}, {'name': 'LORAM'}, {'name': 'GAME'}, {'name': 'EXROM'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}]
        },
        {
            "name": "Color RAM 2114",
            "chip_id": "c64_colorram",
            "category": "Memory",
            "description": "Static Color Memory - 4-bit color information storage",
            "package_types": ['DIP-18'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'CS'}, {'name': 'WE'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "CPU 6510",
            "chip_id": "c64_6510",
            "category": "Processor",
            "description": "MOS 6510 CPU - 6502 with built-in I/O port",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'RW'}, {'name': 'φ1'}, {'name': 'φ2'}, {'name': 'φ0'}, {'name': 'IRQ'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'RDY'}, {'name': 'SO'}, {'name': 'SYNC'}, {'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'}, {'name': 'P3'}, {'name': 'P4'}, {'name': 'P5'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
    ],
    "cd32": [
        {
            "name": "Alice 8374",
            "chip_id": "cd32_alice",
            "category": "Video",
            "description": "Advanced Graphics Architecture (AGA) Alice Chip - Main graphics controller",
            "package_types": ['PLCC-84', 'QFP-100'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'D16'}, {'name': 'D17'}, {'name': 'D18'}, {'name': 'D19'}, {'name': 'D20'}, {'name': 'D21'}, {'name': 'D22'}, {'name': 'D23'}, {'name': 'D24'}, {'name': 'D25'}, {'name': 'D26'}, {'name': 'D27'}, {'name': 'D28'}, {'name': 'D29'}, {'name': 'D30'}, {'name': 'D31'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'}, {'name': 'A21'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'WE'}, {'name': 'OE'}, {'name': 'DMAL'}, {'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'}, {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'}, {'name': 'RGA8'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': 'CDAC'}, {'name': 'CSYNC'}, {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDDQ'}, {'name': 'VSSQ'}, {'name': 'VCC3'}, {'name': 'GND3'}, {'name': 'VREF'}]
        },
        {
            "name": "Lisa 8375",
            "chip_id": "cd32_lisa",
            "category": "Custom",
            "description": "Advanced Graphics Architecture (AGA) Lisa Support Chip",
            "package_types": ['PLCC-68', 'QFP-80'],
            "pins": [{'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'}, {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'}, {'name': 'RGA8'}, {'name': 'RGA9'}, {'name': 'RGA10'}, {'name': 'RGA11'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'WE'}, {'name': 'OE'}, {'name': 'DRAM_CLK'}, {'name': 'AGA_EN'}, {'name': 'BURST'}, {'name': 'FAST'}, {'name': 'SLOW'}, {'name': 'BLANK'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': '14MHZ'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'RESET'}, {'name': 'TEST'}]
        },
        {
            "name": "Paula 8364 (CD32)",
            "chip_id": "cd32_paula",
            "category": "Audio",
            "description": "Enhanced Paula - Audio, I/O and CD32 controller interface",
            "package_types": ['DIP-48', 'PLCC-48'],
            "pins": [{'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'INT2'}, {'name': 'INT3'}, {'name': 'INT6'}, {'name': 'CD32_INT'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'LEFT'}, {'name': 'RIGHT'}, {'name': 'AUDIO_CLK'}, {'name': 'JOY0_CLK'}, {'name': 'JOY0_LOAD'}, {'name': 'JOY0_DATA'}, {'name': 'JOY1_CLK'}, {'name': 'JOY1_LOAD'}, {'name': 'JOY1_DATA'}, {'name': 'DMAL'}, {'name': 'DMAG'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'AVDD'}, {'name': 'AGND'}]
        },
        {
            "name": "Akiko 8421",
            "chip_id": "cd32_akiko",
            "category": "Custom",
            "description": "CD32 System Controller - CD-ROM, chunky-to-planar conversion, joypad interface",
            "package_types": ['PLCC-84', 'QFP-100'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'CS'}, {'name': 'IRQ'}, {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'CD_D0'}, {'name': 'CD_D1'}, {'name': 'CD_D2'}, {'name': 'CD_D3'}, {'name': 'CD_D4'}, {'name': 'CD_D5'}, {'name': 'CD_D6'}, {'name': 'CD_D7'}, {'name': 'CD_CLK'}, {'name': 'CD_REQ'}, {'name': 'CD_ACK'}, {'name': 'CD_ATN'}, {'name': 'CD_RST'}, {'name': 'CD_SEL'}, {'name': 'CD_BSY'}, {'name': 'CD_MSG'}, {'name': 'CD_IO'}, {'name': 'CD_CMD'}, {'name': 'CD_SUBCODE'}, {'name': 'CD_AUDIO_L'}, {'name': 'CD_AUDIO_R'}, {'name': 'CD_MUTE'}, {'name': 'JOY0_CLK'}, {'name': 'JOY0_LOAD'}, {'name': 'JOY0_DATA'}, {'name': 'JOY1_CLK'}, {'name': 'JOY1_LOAD'}, {'name': 'JOY1_DATA'}, {'name': 'JOY_SHIFT_CLK'}, {'name': 'JOY_POWER'}, {'name': 'C2P_CLK'}, {'name': 'C2P_EN'}, {'name': 'C2P_BUSY'}, {'name': 'CHUNKY_D0'}, {'name': 'CHUNKY_D1'}, {'name': 'CHUNKY_D2'}, {'name': 'CHUNKY_D3'}, {'name': 'CHUNKY_D4'}, {'name': 'CHUNKY_D5'}, {'name': 'CHUNKY_D6'}, {'name': 'CHUNKY_D7'}, {'name': 'NVRAM_CS'}, {'name': 'NVRAM_CLK'}, {'name': 'NVRAM_DI'}, {'name': 'NVRAM_DO'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC_3V3'}, {'name': 'GND_3V3'}, {'name': 'TEST'}, {'name': 'JTAG_TDI'}, {'name': 'JTAG_TDO'}, {'name': 'JTAG_TCK'}]
        },
        {
            "name": "TDA1387 Audio DAC",
            "chip_id": "cd32_audio_dac",
            "category": "Audio",
            "description": "16-bit Stereo Audio DAC for CD32 audio output",
            "package_types": ['DIP-18', 'SOIC-18'],
            "pins": [{'name': 'WS'}, {'name': 'BCK'}, {'name': 'DATA'}, {'name': 'MUTE'}, {'name': 'OUTL+'}, {'name': 'OUTL-'}, {'name': 'OUTR+'}, {'name': 'OUTR-'}, {'name': 'VREF'}, {'name': 'BIAS'}, {'name': 'FILT'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'}, {'name': 'RESET'}, {'name': 'TEST'}, {'name': 'FS0'}]
        },
        {
            "name": "CD32 Joypad Controller",
            "chip_id": "cd32_joypad_controller",
            "category": "I/O",
            "description": "CD32 joypad interface controller with shift register support",
            "package_types": ['DIP-20', 'SOIC-20'],
            "pins": [{'name': 'JOY0_UP'}, {'name': 'JOY0_DOWN'}, {'name': 'JOY0_LEFT'}, {'name': 'JOY0_RIGHT'}, {'name': 'JOY0_RED'}, {'name': 'JOY0_BLUE'}, {'name': 'JOY0_GREEN'}, {'name': 'JOY0_YELLOW'}, {'name': 'JOY0_FORWARD'}, {'name': 'JOY0_REVERSE'}, {'name': 'JOY0_PLAY'}, {'name': 'JOY1_DATA'}, {'name': 'JOY1_CLK'}, {'name': 'JOY1_LOAD'}, {'name': 'SERIAL_CLK'}, {'name': 'SERIAL_LOAD'}, {'name': 'SERIAL_DATA'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'RESET'}]
        },
        {
            "name": "CL450 MPEG Decoder",
            "chip_id": "cd32_mpeg_cl450",
            "category": "Video",
            "description": "C-Cube CL450 MPEG-1 Video Decoder for Full Motion Video",
            "package_types": ['PLCC-84', 'QFP-100'],
            "pins": [{'name': 'HD0'}, {'name': 'HD1'}, {'name': 'HD2'}, {'name': 'HD3'}, {'name': 'HD4'}, {'name': 'HD5'}, {'name': 'HD6'}, {'name': 'HD7'}, {'name': 'HD8'}, {'name': 'HD9'}, {'name': 'HD10'}, {'name': 'HD11'}, {'name': 'HD12'}, {'name': 'HD13'}, {'name': 'HD14'}, {'name': 'HD15'}, {'name': 'HA0'}, {'name': 'HA1'}, {'name': 'HA2'}, {'name': 'HA3'}, {'name': 'HCS'}, {'name': 'HRD'}, {'name': 'HWR'}, {'name': 'HINT'}, {'name': 'HRDY'}, {'name': 'HRST'}, {'name': 'MD0'}, {'name': 'MD1'}, {'name': 'MD2'}, {'name': 'MD3'}, {'name': 'MD4'}, {'name': 'MD5'}, {'name': 'MD6'}, {'name': 'MD7'}, {'name': 'MD8'}, {'name': 'MD9'}, {'name': 'MD10'}, {'name': 'MD11'}, {'name': 'MD12'}, {'name': 'MD13'}, {'name': 'MD14'}, {'name': 'MD15'}, {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'}, {'name': 'MA3'}, {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'}, {'name': 'MA7'}, {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'}, {'name': 'MA11'}, {'name': 'MRAS'}, {'name': 'MCAS'}, {'name': 'MWE'}, {'name': 'MOE'}, {'name': 'Y0'}, {'name': 'Y1'}, {'name': 'Y2'}, {'name': 'Y3'}, {'name': 'Y4'}, {'name': 'Y5'}, {'name': 'Y6'}, {'name': 'Y7'}, {'name': 'U0'}, {'name': 'U1'}, {'name': 'U2'}, {'name': 'U3'}, {'name': 'U4'}, {'name': 'U5'}, {'name': 'U6'}, {'name': 'U7'}, {'name': 'V0'}, {'name': 'V1'}, {'name': 'V2'}, {'name': 'V3'}, {'name': 'V4'}, {'name': 'V5'}, {'name': 'V6'}, {'name': 'V7'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'PIXEL_CLK'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'PLL_VDD'}, {'name': 'PLL_VSS'}, {'name': 'RESET'}, {'name': 'TEST'}, {'name': 'IRQ_OUT'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'}]
        },
        {
            "name": "CL480 Video Controller",
            "chip_id": "cd32_mpeg_cl480",
            "category": "Video",
            "description": "C-Cube CL480 Video Timing Controller for MPEG playback",
            "package_types": ['PLCC-68', 'QFP-80'],
            "pins": [{'name': 'Y_IN0'}, {'name': 'Y_IN1'}, {'name': 'Y_IN2'}, {'name': 'Y_IN3'}, {'name': 'Y_IN4'}, {'name': 'Y_IN5'}, {'name': 'Y_IN6'}, {'name': 'Y_IN7'}, {'name': 'U_IN0'}, {'name': 'U_IN1'}, {'name': 'U_IN2'}, {'name': 'U_IN3'}, {'name': 'U_IN4'}, {'name': 'U_IN5'}, {'name': 'U_IN6'}, {'name': 'U_IN7'}, {'name': 'V_IN0'}, {'name': 'V_IN1'}, {'name': 'V_IN2'}, {'name': 'V_IN3'}, {'name': 'V_IN4'}, {'name': 'V_IN5'}, {'name': 'V_IN6'}, {'name': 'V_IN7'}, {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'}, {'name': 'R4'}, {'name': 'R5'}, {'name': 'R6'}, {'name': 'R7'}, {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'}, {'name': 'G4'}, {'name': 'G5'}, {'name': 'G6'}, {'name': 'G7'}, {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'}, {'name': 'B4'}, {'name': 'B5'}, {'name': 'B6'}, {'name': 'B7'}, {'name': 'HSYNC_IN'}, {'name': 'VSYNC_IN'}, {'name': 'BLANK_IN'}, {'name': 'HSYNC_OUT'}, {'name': 'VSYNC_OUT'}, {'name': 'BLANK_OUT'}, {'name': 'PIXEL_CLK'}, {'name': 'LINE_CLK'}, {'name': 'MODE0'}, {'name': 'MODE1'}, {'name': 'MODE2'}, {'name': 'ENABLE'}, {'name': 'OVERLAY'}, {'name': 'KEYING'}, {'name': 'ALPHA'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'}]
        },
        {
            "name": "MPEG DRAM Controller",
            "chip_id": "cd32_mpeg_dram_controller",
            "category": "Memory",
            "description": "DRAM controller for MPEG video buffer memory",
            "package_types": ['PLCC-52', 'QFP-64'],
            "pins": [{'name': 'MD0'}, {'name': 'MD1'}, {'name': 'MD2'}, {'name': 'MD3'}, {'name': 'MD4'}, {'name': 'MD5'}, {'name': 'MD6'}, {'name': 'MD7'}, {'name': 'MD8'}, {'name': 'MD9'}, {'name': 'MD10'}, {'name': 'MD11'}, {'name': 'MD12'}, {'name': 'MD13'}, {'name': 'MD14'}, {'name': 'MD15'}, {'name': 'MA0'}, {'name': 'MA1'}, {'name': 'MA2'}, {'name': 'MA3'}, {'name': 'MA4'}, {'name': 'MA5'}, {'name': 'MA6'}, {'name': 'MA7'}, {'name': 'MA8'}, {'name': 'MA9'}, {'name': 'MA10'}, {'name': 'MA11'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'WE'}, {'name': 'OE'}, {'name': 'REFRESH'}, {'name': 'CLK'}, {'name': 'CL450_REQ'}, {'name': 'CL450_ACK'}, {'name': 'CL450_BUSY'}, {'name': 'CS'}, {'name': 'RESET'}, {'name': 'IRQ'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "MPEG Cart Interface",
            "chip_id": "cd32_mpeg_interface",
            "category": "I/O",
            "description": "Interface controller between MPEG cartridge and CD32 system",
            "package_types": ['PLCC-44', 'QFP-48'],
            "pins": [{'name': 'CD32_D0'}, {'name': 'CD32_D1'}, {'name': 'CD32_D2'}, {'name': 'CD32_D3'}, {'name': 'CD32_D4'}, {'name': 'CD32_D5'}, {'name': 'CD32_D6'}, {'name': 'CD32_D7'}, {'name': 'CD32_D8'}, {'name': 'CD32_D9'}, {'name': 'CD32_D10'}, {'name': 'CD32_D11'}, {'name': 'CD32_D12'}, {'name': 'CD32_D13'}, {'name': 'CD32_D14'}, {'name': 'CD32_D15'}, {'name': 'CD32_A0'}, {'name': 'CD32_A1'}, {'name': 'CD32_A2'}, {'name': 'CD32_A3'}, {'name': 'CD32_CS'}, {'name': 'CD32_RD'}, {'name': 'CD32_WR'}, {'name': 'CD32_IRQ'}, {'name': 'MPEG_CS'}, {'name': 'MPEG_RD'}, {'name': 'MPEG_WR'}, {'name': 'MPEG_IRQ'}, {'name': 'MPEG_READY'}, {'name': 'MPEG_BUSY'}, {'name': 'VIDEO_EN'}, {'name': 'OVERLAY_EN'}, {'name': 'KEYING_EN'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'RESET'}, {'name': 'CLK'}]
        },
        {
            "name": "CD32 RF Modulator",
            "chip_id": "cd32_rf_modulator",
            "category": "Video",
            "description": "RF modulator for TV output (PAL/NTSC)",
            "package_types": ['DIP-16', 'SOIC-16'],
            "pins": [{'name': 'CVBS_IN'}, {'name': 'Y_IN'}, {'name': 'C_IN'}, {'name': 'RGB_R'}, {'name': 'RGB_G'}, {'name': 'RGB_B'}, {'name': 'SYNC'}, {'name': 'AUDIO_L'}, {'name': 'AUDIO_R'}, {'name': 'RF_OUT'}, {'name': 'RF_GND'}, {'name': 'CH_SEL'}, {'name': 'PAL_NTSC'}, {'name': 'ENABLE'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "CD32 Power Controller",
            "chip_id": "cd32_power_controller",
            "category": "Power",
            "description": "Power management and reset controller for CD32 system",
            "package_types": ['DIP-14', 'SOIC-14'],
            "pins": [{'name': 'VIN'}, {'name': 'GND_IN'}, {'name': '5V_OUT'}, {'name': '3V3_OUT'}, {'name': '12V_OUT'}, {'name': '-12V_OUT'}, {'name': 'POWER_BTN'}, {'name': 'RESET_BTN'}, {'name': 'CD_POWER'}, {'name': 'RESET_OUT'}, {'name': 'POWER_GOOD'}, {'name': 'STANDBY'}, {'name': 'LED_POWER'}, {'name': 'LED_ACTIVITY'}]
        },
    ],
    "cdtv": [
        {
            "name": "Agnus 8370",
            "chip_id": "cdtv_agnus",
            "category": "Custom",
            "description": "Address Generator Unit (Agnus) - DMA Controller and Memory Management for CDTV",
            "package_types": ['DIP-84', 'PLCC-84'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'OWN'}, {'name': 'BERR'}, {'name': 'HALT'}, {'name': 'RESET'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': 'C1'}, {'name': 'C3'}, {'name': 'CDAC'}, {'name': 'CSYNC'}, {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'WE'}, {'name': 'DMAL'}, {'name': 'DMAG'}, {'name': 'DMAS'}, {'name': 'DKRD'}, {'name': 'DKWD'}, {'name': 'INT2'}, {'name': 'INT6'}, {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'BCLK'}, {'name': 'BDIR'}, {'name': '7MHZ'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VDDQ'}, {'name': 'VSSQ'}]
        },
        {
            "name": "Paula 8364",
            "chip_id": "cdtv_paula",
            "category": "Audio",
            "description": "Ports, Audio, UART, and Logic (Paula) - Enhanced for CDTV multimedia",
            "package_types": ['DIP-48', 'PLCC-48'],
            "pins": [{'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'INT2'}, {'name': 'INT3'}, {'name': 'INT6'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': 'DMAL'}, {'name': 'DMAG'}, {'name': 'LEFT'}, {'name': 'RIGHT'}, {'name': 'LPEN'}, {'name': 'LPENCLK'}, {'name': 'XCLK'}, {'name': 'XCLKEN'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'AVDD'}, {'name': 'AGND'}]
        },
        {
            "name": "Denise 8362",
            "chip_id": "cdtv_denise",
            "category": "Video",
            "description": "Display Enable (Denise) - Video Output and Sprite Control for CDTV",
            "package_types": ['DIP-48', 'PLCC-48'],
            "pins": [{'name': 'RGA0'}, {'name': 'RGA1'}, {'name': 'RGA2'}, {'name': 'RGA3'}, {'name': 'RGA4'}, {'name': 'RGA5'}, {'name': 'RGA6'}, {'name': 'RGA7'}, {'name': 'RGA8'}, {'name': 'RGA9'}, {'name': 'DMAL'}, {'name': 'DMA'}, {'name': 'CCK'}, {'name': 'CCKQ'}, {'name': '28MHZ'}, {'name': 'CDAC'}, {'name': 'R0'}, {'name': 'R1'}, {'name': 'R2'}, {'name': 'R3'}, {'name': 'G0'}, {'name': 'G1'}, {'name': 'G2'}, {'name': 'G3'}, {'name': 'B0'}, {'name': 'B1'}, {'name': 'B2'}, {'name': 'B3'}, {'name': 'I0'}, {'name': 'I1'}, {'name': 'I2'}, {'name': 'I3'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'CSYNC'}, {'name': 'BLANK'}, {'name': 'LACE'}, {'name': 'DBLSCAN'}, {'name': 'HAM'}, {'name': 'EHB'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'AVDD'}, {'name': 'AGND'}, {'name': 'VREF'}, {'name': 'COMP'}]
        },
        {
            "name": "CDTV Controller",
            "chip_id": "cdtv_controller",
            "category": "Custom",
            "description": "CDTV System Controller - CD-ROM interface and multimedia control",
            "package_types": ['PLCC-68', 'QFP-80'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'CS'}, {'name': 'IRQ'}, {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'CD_DATA0'}, {'name': 'CD_DATA1'}, {'name': 'CD_DATA2'}, {'name': 'CD_DATA3'}, {'name': 'CD_DATA4'}, {'name': 'CD_DATA5'}, {'name': 'CD_DATA6'}, {'name': 'CD_DATA7'}, {'name': 'CD_CLK'}, {'name': 'CD_LRCK'}, {'name': 'CD_BCK'}, {'name': 'CD_REQ'}, {'name': 'CD_ACK'}, {'name': 'CD_ATN'}, {'name': 'CD_RST'}, {'name': 'CD_MSG'}, {'name': 'CD_IO'}, {'name': 'CD_SEL'}, {'name': 'CD_BSY'}, {'name': 'CD_CMD'}, {'name': 'AUDIO_L'}, {'name': 'AUDIO_R'}, {'name': 'AUDIO_CLK'}, {'name': 'AUDIO_EN'}, {'name': 'REMOTE_IN'}, {'name': 'REMOTE_OUT'}, {'name': 'LED_POWER'}, {'name': 'LED_ACTIVITY'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC_5V'}, {'name': 'VCC_3V3'}, {'name': 'GND_A'}, {'name': 'GND_D'}]
        },
        {
            "name": "CDTV DMAC",
            "chip_id": "cdtv_dmac",
            "category": "Custom",
            "description": "Enhanced DMA Controller for CD-ROM data transfer",
            "package_types": ['PLCC-52', 'QFP-64'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'BR'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'DRQ0'}, {'name': 'DRQ1'}, {'name': 'DRQ2'}, {'name': 'DRQ3'}, {'name': 'DACK0'}, {'name': 'DACK1'}, {'name': 'DACK2'}, {'name': 'DACK3'}, {'name': 'TC'}, {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'IRQ'}, {'name': 'CS'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "PCM56 Audio DAC",
            "chip_id": "cdtv_audio_dac",
            "category": "Audio",
            "description": "16-bit Stereo Audio DAC for CD-quality sound output",
            "package_types": ['DIP-28', 'SOIC-28'],
            "pins": [{'name': 'DL0'}, {'name': 'DL1'}, {'name': 'DL2'}, {'name': 'DL3'}, {'name': 'DL4'}, {'name': 'DL5'}, {'name': 'DL6'}, {'name': 'DL7'}, {'name': 'DL8'}, {'name': 'DL9'}, {'name': 'DL10'}, {'name': 'DL11'}, {'name': 'DL12'}, {'name': 'DL13'}, {'name': 'DL14'}, {'name': 'DL15'}, {'name': 'DR0'}, {'name': 'DR1'}, {'name': 'DR2'}, {'name': 'DR3'}, {'name': 'DR4'}, {'name': 'DR5'}, {'name': 'DR6'}, {'name': 'DR7'}, {'name': 'BCK'}, {'name': 'LRCK'}, {'name': 'DATA'}, {'name': 'CLK'}, {'name': 'AOUTL'}, {'name': 'AOUTR'}, {'name': 'VREF'}, {'name': 'AGND'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'}]
        },
        {
            "name": "Audio Mixer",
            "chip_id": "cdtv_audio_mixer",
            "category": "Audio",
            "description": "Audio mixing chip for combining Amiga and CD audio sources",
            "package_types": ['DIP-16', 'SOIC-16'],
            "pins": [{'name': 'AMIGA_L'}, {'name': 'AMIGA_R'}, {'name': 'CD_L'}, {'name': 'CD_R'}, {'name': 'OUT_L'}, {'name': 'OUT_R'}, {'name': 'MIX_CTL0'}, {'name': 'MIX_CTL1'}, {'name': 'MIX_CTL2'}, {'name': 'MUTE'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'AVCC'}, {'name': 'AGND'}]
        },
        {
            "name": "CXD1199Q CD Controller",
            "chip_id": "cdtv_cd_controller",
            "category": "Storage",
            "description": "Sony CXD1199Q CD-ROM Controller for CDTV drive interface",
            "package_types": ['QFP-80', 'PLCC-84'],
            "pins": [{'name': 'HD0'}, {'name': 'HD1'}, {'name': 'HD2'}, {'name': 'HD3'}, {'name': 'HD4'}, {'name': 'HD5'}, {'name': 'HD6'}, {'name': 'HD7'}, {'name': 'HA0'}, {'name': 'HA1'}, {'name': 'HA2'}, {'name': 'HA3'}, {'name': 'HCS'}, {'name': 'HRD'}, {'name': 'HWR'}, {'name': 'HINT'}, {'name': 'HRDY'}, {'name': 'HRST'}, {'name': 'HCLK'}, {'name': 'RF+'}, {'name': 'RF-'}, {'name': 'TE'}, {'name': 'FE'}, {'name': 'AS'}, {'name': 'MIRR'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'TRO'}, {'name': 'TRO_N'}, {'name': 'FOO'}, {'name': 'FOO_N'}, {'name': 'SL'}, {'name': 'SL_N'}, {'name': 'SO'}, {'name': 'SO_N'}, {'name': 'SLED+'}, {'name': 'SLED-'}, {'name': 'FOCUS+'}, {'name': 'FOCUS-'}, {'name': 'CLV'}, {'name': 'CAV'}, {'name': 'BRAKE'}, {'name': 'DISC'}, {'name': 'SDATA'}, {'name': 'SLRCK'}, {'name': 'SBCK'}, {'name': 'SCKI'}, {'name': 'SENS0'}, {'name': 'SENS1'}, {'name': 'SENS2'}, {'name': 'DOOR'}, {'name': 'EJECT'}, {'name': 'PLAY'}, {'name': 'STOP'}, {'name': 'PAUSE'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'AVDD'}, {'name': 'AVSS'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "CXD2500Q Signal Processor",
            "chip_id": "cdtv_cd_signal_processor",
            "category": "Storage",
            "description": "Sony CXD2500Q CD Signal Processor and Error Correction",
            "package_types": ['QFP-100', 'PLCC-100'],
            "pins": [{'name': 'RF_IN+'}, {'name': 'RF_IN-'}, {'name': 'AGC'}, {'name': 'SLICE'}, {'name': 'EFM_DATA'}, {'name': 'EFM_CLK'}, {'name': 'SYNC'}, {'name': 'FRAME'}, {'name': 'TE_OUT'}, {'name': 'FE_OUT'}, {'name': 'AS_OUT'}, {'name': 'MIRR_OUT'}, {'name': 'HOST_D0'}, {'name': 'HOST_D1'}, {'name': 'HOST_D2'}, {'name': 'HOST_D3'}, {'name': 'HOST_D4'}, {'name': 'HOST_D5'}, {'name': 'HOST_D6'}, {'name': 'HOST_D7'}, {'name': 'HOST_CS'}, {'name': 'HOST_RD'}, {'name': 'HOST_WR'}, {'name': 'HOST_INT'}, {'name': 'AUDIO_L'}, {'name': 'AUDIO_R'}, {'name': 'AUDIO_CLK'}, {'name': 'AUDIO_LRCK'}, {'name': 'MODE0'}, {'name': 'MODE1'}, {'name': 'MODE2'}, {'name': 'RESET'}, {'name': 'TEST'}, {'name': 'CLK_IN'}, {'name': 'CLK_OUT'}, {'name': 'PLL_VCC'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'AVCC'}, {'name': 'AGND'}, {'name': 'VDD'}, {'name': 'VSS'}]
        },
        {
            "name": "Remote Control Interface",
            "chip_id": "cdtv_remote_interface",
            "category": "I/O",
            "description": "Infrared remote control receiver and decoder",
            "package_types": ['DIP-18', 'SOIC-18'],
            "pins": [{'name': 'IR_IN'}, {'name': 'IR_GND'}, {'name': 'IR_VCC'}, {'name': 'DATA_OUT'}, {'name': 'CLOCK_OUT'}, {'name': 'VALID'}, {'name': 'IRQ'}, {'name': 'HOST_D0'}, {'name': 'HOST_D1'}, {'name': 'HOST_D2'}, {'name': 'HOST_D3'}, {'name': 'HOST_CS'}, {'name': 'HOST_RD'}, {'name': 'HOST_WR'}, {'name': 'RESET'}, {'name': 'ENABLE'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "Front Panel Controller",
            "chip_id": "cdtv_front_panel",
            "category": "I/O",
            "description": "Front panel LED and button controller",
            "package_types": ['DIP-20', 'SOIC-20'],
            "pins": [{'name': 'POWER_BTN'}, {'name': 'EJECT_BTN'}, {'name': 'PLAY_BTN'}, {'name': 'STOP_BTN'}, {'name': 'PAUSE_BTN'}, {'name': 'FWD_BTN'}, {'name': 'REW_BTN'}, {'name': 'POWER_LED'}, {'name': 'ACTIVITY_LED'}, {'name': 'PLAY_LED'}, {'name': 'PAUSE_LED'}, {'name': 'HOST_D0'}, {'name': 'HOST_D1'}, {'name': 'HOST_D2'}, {'name': 'HOST_D3'}, {'name': 'HOST_CS'}, {'name': 'HOST_RD'}, {'name': 'HOST_WR'}, {'name': 'HOST_IRQ'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "Extended Memory Controller",
            "chip_id": "cdtv_memory_controller",
            "category": "Memory",
            "description": "Extended memory controller for CDTV additional RAM expansion",
            "package_types": ['PLCC-52', 'QFP-64'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS0'}, {'name': 'CAS1'}, {'name': 'WE'}, {'name': 'OE'}, {'name': 'REFRESH'}, {'name': 'CLK'}, {'name': 'CS'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
    ],
    "dragon": [
        {
            "name": "SAM MC6883",
            "chip_id": "dragon_sam",
            "category": "Custom",
            "description": "Synchronous Address Multiplexer for Dragon 32/64",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'Z0'}, {'name': 'Z1'}, {'name': 'Z2'}, {'name': 'Z3'}, {'name': 'Z4'}, {'name': 'Z5'}, {'name': 'Z6'}, {'name': 'Z7'}, {'name': 'Z8'}, {'name': 'Z9'}, {'name': 'Z10'}, {'name': 'Z11'}, {'name': 'Z12'}, {'name': 'Z13'}, {'name': 'Z14'}, {'name': 'Z15'}, {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'WE'}, {'name': 'OE'}, {'name': 'HS'}, {'name': 'FS'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}]
        },
        {
            "name": "VDG MC6847",
            "chip_id": "dragon_vdg",
            "category": "Video",
            "description": "Video Display Generator for Dragon 32/64",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'}, {'name': 'DA3'}, {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'}, {'name': 'DA7'}, {'name': 'DA8'}, {'name': 'DA9'}, {'name': 'DA10'}, {'name': 'DA11'}, {'name': 'RP'}, {'name': 'HS'}, {'name': 'FS'}, {'name': 'AS'}, {'name': 'INTEXT'}, {'name': 'INV'}, {'name': 'GM0'}, {'name': 'GM1'}, {'name': 'GM2'}, {'name': 'AG'}, {'name': 'CSS'}, {'name': 'Y'}, {'name': 'φA'}, {'name': 'φB'}, {'name': 'CVBS'}, {'name': 'MS'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}]
        },
        {
            "name": "PIA MC6821",
            "chip_id": "dragon_pia",
            "category": "I/O",
            "description": "Peripheral Interface Adapter for Dragon 32/64",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'VSS'}, {'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'}, {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'}, {'name': 'PB7'}, {'name': 'CB1'}, {'name': 'CB2'}, {'name': 'VDD'}, {'name': 'IRQA'}, {'name': 'IRQB'}, {'name': 'RS0'}, {'name': 'RS1'}, {'name': 'RESET'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'E'}, {'name': 'CS0'}, {'name': 'CS1'}, {'name': 'CS2'}, {'name': 'R/W'}, {'name': 'CA1'}, {'name': 'CA2'}]
        },
        {
            "name": "ACIA MC6850",
            "chip_id": "dragon_acia",
            "category": "I/O",
            "description": "Asynchronous Communications Interface Adapter for Dragon 32/64",
            "package_types": ['DIP-24'],
            "pins": [{'name': 'VSS'}, {'name': 'RXD'}, {'name': 'RXC'}, {'name': 'TXC'}, {'name': 'RTS'}, {'name': 'TXD'}, {'name': 'IRQ'}, {'name': 'CS0'}, {'name': 'CS2'}, {'name': 'CS1'}, {'name': 'RS'}, {'name': 'VDD'}, {'name': 'R/W'}, {'name': 'E'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CTS'}, {'name': 'DCD'}]
        },
        {
            "name": "CPU MC6809",
            "chip_id": "dragon_6809",
            "category": "Processor",
            "description": "Motorola 6809 CPU for Dragon 32/64",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'VSS'}, {'name': 'NMI'}, {'name': 'IRQ'}, {'name': 'FIRQ'}, {'name': 'BS'}, {'name': 'BA'}, {'name': 'VCC'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D7'}, {'name': 'D6'}, {'name': 'D5'}, {'name': 'D4'}, {'name': 'D3'}, {'name': 'D2'}, {'name': 'D1'}, {'name': 'D0'}, {'name': 'R/W'}, {'name': 'VMA'}, {'name': 'E'}, {'name': 'Q'}, {'name': 'AVMA'}, {'name': 'RESET'}, {'name': 'LIC'}, {'name': 'TSC'}, {'name': 'HALT'}]
        },
    ],
    "msx": [
        {
            "name": "TMS9918A",
            "chip_id": "msx_tms9918a",
            "category": "Video",
            "description": "Video Display Processor for MSX",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'}, {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'}, {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'AD8'}, {'name': 'AD9'}, {'name': 'AD10'}, {'name': 'AD11'}, {'name': 'AD12'}, {'name': 'AD13'}, {'name': 'CD0'}, {'name': 'CD1'}, {'name': 'CD2'}, {'name': 'CD3'}, {'name': 'CD4'}, {'name': 'CD5'}, {'name': 'CD6'}, {'name': 'CD7'}, {'name': 'MODE'}, {'name': 'CSW'}, {'name': 'CSR'}, {'name': 'INT'}, {'name': 'GROMCLK'}, {'name': 'CPUCLK'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'Y'}, {'name': 'RY'}, {'name': 'R'}, {'name': 'G'}, {'name': 'B'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}]
        },
        {
            "name": "AY-3-8910",
            "chip_id": "msx_ay3_8910",
            "category": "Audio",
            "description": "Programmable Sound Generator for MSX",
            "package_types": ['DIP-28', 'DIP-40'],
            "pins": [{'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'}, {'name': 'DA3'}, {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'}, {'name': 'DA7'}, {'name': 'BDIR'}, {'name': 'BC1'}, {'name': 'BC2'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'RESET'}, {'name': 'CLOCK'}, {'name': 'IOA0'}, {'name': 'IOA1'}, {'name': 'IOA2'}, {'name': 'IOA3'}, {'name': 'IOA4'}, {'name': 'IOA5'}, {'name': 'IOA6'}, {'name': 'IOA7'}, {'name': 'IOB0'}, {'name': 'IOB1'}, {'name': 'IOB2'}, {'name': 'IOB3'}, {'name': 'IOB4'}, {'name': 'IOB5'}, {'name': 'IOB6'}, {'name': 'IOB7'}, {'name': 'CHANNEL_A'}, {'name': 'CHANNEL_B'}, {'name': 'CHANNEL_C'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'ANALOG_A'}, {'name': 'ANALOG_B'}, {'name': 'ANALOG_C'}, {'name': 'TEST1'}]
        },
        {
            "name": "S1985 MSX Engine",
            "chip_id": "msx_s1985",
            "category": "Custom",
            "description": "MSX Engine - System controller for MSX2+",
            "package_types": ['DIP-64', 'QFP-64'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'MREQ'}, {'name': 'IORQ'}, {'name': 'M1'}, {'name': 'RFSH'}, {'name': 'HALT'}, {'name': 'BUSREQ'}, {'name': 'BUSACK'}, {'name': 'WAIT'}, {'name': 'INT'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'SLOT0'}, {'name': 'SLOT1'}, {'name': 'SLOT2'}, {'name': 'SLOT3'}, {'name': 'SLTSL0'}, {'name': 'SLTSL1'}, {'name': 'SLTSL2'}, {'name': 'SLTSL3'}, {'name': 'RAMENB'}, {'name': 'RAMDIS'}, {'name': 'KANJI'}, {'name': 'CAPS'}, {'name': 'KANA'}, {'name': 'VDP'}, {'name': 'PSG'}, {'name': 'PPI'}, {'name': 'RTC'}, {'name': 'PRINTER'}, {'name': 'RS232'}, {'name': 'MODEM'}, {'name': 'MIDI'}, {'name': 'MOUSE'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}]
        },
        {
            "name": "PPI 8255",
            "chip_id": "msx_ppi_8255",
            "category": "I/O",
            "description": "Programmable Peripheral Interface - Keyboard and joystick controller",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'}, {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'}, {'name': 'PB7'}, {'name': 'PC0'}, {'name': 'PC1'}, {'name': 'PC2'}, {'name': 'PC3'}, {'name': 'PC4'}, {'name': 'PC5'}, {'name': 'PC6'}, {'name': 'PC7'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "V9938 VDP",
            "chip_id": "msx_v9938",
            "category": "Video",
            "description": "Video Display Processor for MSX2",
            "package_types": ['DIP-64', 'QFP-64'],
            "pins": [{'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'}, {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'}, {'name': 'AD8'}, {'name': 'AD9'}, {'name': 'AD10'}, {'name': 'AD11'}, {'name': 'AD12'}, {'name': 'AD13'}, {'name': 'AD14'}, {'name': 'AD15'}, {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'WE'}, {'name': 'OE'}, {'name': 'CD0'}, {'name': 'CD1'}, {'name': 'CD2'}, {'name': 'CD3'}, {'name': 'CD4'}, {'name': 'CD5'}, {'name': 'CD6'}, {'name': 'CD7'}, {'name': 'MODE'}, {'name': 'CSW'}, {'name': 'CSR'}, {'name': 'INT'}, {'name': 'WAIT'}, {'name': 'RESET'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'CPUCLK'}, {'name': 'DHCLK'}, {'name': 'DLCLK'}, {'name': 'R'}, {'name': 'G'}, {'name': 'B'}, {'name': 'Y'}, {'name': 'S'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'COLORCLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VCC2'}, {'name': 'GND2'}, {'name': 'VREF'}, {'name': 'COMP'}]
        },
    ],
    "oric": [
        {
            "name": "ULA Oric",
            "chip_id": "oric_ula",
            "category": "Custom",
            "description": "Custom ULA for Oric Atmos/1 - Video and system control",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'RW'}, {'name': 'φ2'}, {'name': 'IRQ'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'RDY'}, {'name': 'SYNC'}, {'name': 'SO'}, {'name': 'RED'}, {'name': 'GREEN'}, {'name': 'BLUE'}, {'name': 'LUMA'}, {'name': 'CHROMA'}, {'name': 'CSYNC'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "AY-3-8912",
            "chip_id": "oric_ay3_8912",
            "category": "Audio",
            "description": "Programmable Sound Generator for Oric",
            "package_types": ['DIP-28'],
            "pins": [{'name': 'DA0'}, {'name': 'DA1'}, {'name': 'DA2'}, {'name': 'DA3'}, {'name': 'DA4'}, {'name': 'DA5'}, {'name': 'DA6'}, {'name': 'DA7'}, {'name': 'BDIR'}, {'name': 'BC1'}, {'name': 'BC2'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'RESET'}, {'name': 'CLOCK'}, {'name': 'IOA0'}, {'name': 'IOA1'}, {'name': 'IOA2'}, {'name': 'IOA3'}, {'name': 'IOA4'}, {'name': 'IOA5'}, {'name': 'IOA6'}, {'name': 'IOA7'}, {'name': 'CHANNEL_A'}, {'name': 'CHANNEL_B'}, {'name': 'CHANNEL_C'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "VIA 6522",
            "chip_id": "oric_via",
            "category": "I/O",
            "description": "Versatile Interface Adapter for Oric keyboard and I/O",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'PA0'}, {'name': 'PA1'}, {'name': 'PA2'}, {'name': 'PA3'}, {'name': 'PA4'}, {'name': 'PA5'}, {'name': 'PA6'}, {'name': 'PA7'}, {'name': 'PB0'}, {'name': 'PB1'}, {'name': 'PB2'}, {'name': 'PB3'}, {'name': 'PB4'}, {'name': 'PB5'}, {'name': 'PB6'}, {'name': 'PB7'}, {'name': 'CA1'}, {'name': 'CA2'}, {'name': 'CB1'}, {'name': 'CB2'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'RS0'}, {'name': 'RS1'}, {'name': 'RS2'}, {'name': 'RS3'}, {'name': 'CS1'}, {'name': 'CS2'}, {'name': 'φ2'}, {'name': 'RW'}, {'name': 'IRQ'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "CPU 6502",
            "chip_id": "oric_6502",
            "category": "Processor",
            "description": "MOS 6502 CPU for Oric Atmos/1",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'RW'}, {'name': 'φ1'}, {'name': 'φ2'}, {'name': 'φ0'}, {'name': 'IRQ'}, {'name': 'NMI'}, {'name': 'RESET'}, {'name': 'RDY'}, {'name': 'SO'}, {'name': 'SYNC'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "BASIC ROM",
            "chip_id": "oric_basic_rom",
            "category": "Memory",
            "description": "BASIC interpreter ROM for Oric",
            "package_types": ['DIP-28'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CE'}, {'name': 'OE'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VPP'}, {'name': 'NC'}]
        },
        {
            "name": "Character ROM",
            "chip_id": "oric_char_rom",
            "category": "Memory",
            "description": "Character generator ROM for Oric display",
            "package_types": ['DIP-24'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CE'}, {'name': 'OE'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}]
        },
        {
            "name": "RAM 4116",
            "chip_id": "oric_ram_4116",
            "category": "Memory",
            "description": "16Kx1 Dynamic RAM for Oric system memory",
            "package_types": ['DIP-16'],
            "pins": [{'name': 'VBB'}, {'name': 'DIN'}, {'name': 'WRITE'}, {'name': 'RAS'}, {'name': 'A0'}, {'name': 'A2'}, {'name': 'A1'}, {'name': 'VDD'}, {'name': 'VCC'}, {'name': 'DOUT'}, {'name': 'CAS'}, {'name': 'A3'}, {'name': 'A6'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'VSS'}]
        },
        {
            "name": "FDC 1793",
            "chip_id": "oric_fdc_1793",
            "category": "Storage",
            "description": "Floppy Disk Controller for Oric Microdisc",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RE'}, {'name': 'WE'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CLK'}, {'name': 'RESET'}, {'name': 'READY'}, {'name': 'WF'}, {'name': 'WG'}, {'name': 'TG00'}, {'name': 'IP'}, {'name': 'WPRT'}, {'name': 'TR00'}, {'name': 'STEP'}, {'name': 'DIRC'}, {'name': 'WD'}, {'name': 'RD'}, {'name': 'HLD'}, {'name': 'HLT'}, {'name': 'ENBL'}, {'name': 'DRQ'}, {'name': 'DDEN'}, {'name': 'INTRQ'}, {'name': 'MR'}, {'name': 'TEST'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VSS'}, {'name': 'VDD'}, {'name': 'VBB'}, {'name': 'NC'}]
        },
    ],
    "sinclair_ql": [
        {
            "name": "MC68008 CPU",
            "chip_id": "ql_68008",
            "category": "Processor",
            "description": "Motorola 68008 CPU - 32-bit processor with 8-bit data bus",
            "package_types": ['DIP-48', 'PLCC-52'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'R/W'}, {'name': 'DTACK'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'BR'}, {'name': 'FC0'}, {'name': 'FC1'}, {'name': 'FC2'}, {'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'BERR'}, {'name': 'VPA'}, {'name': 'VMA'}, {'name': 'E'}, {'name': 'RESET'}, {'name': 'HALT'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}]
        },
        {
            "name": "IPC 8049",
            "chip_id": "ql_ipc",
            "category": "I/O",
            "description": "Intel 8049 - Intelligent Peripheral Controller for keyboard/sound",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'P10'}, {'name': 'P11'}, {'name': 'P12'}, {'name': 'P13'}, {'name': 'P14'}, {'name': 'P15'}, {'name': 'P16'}, {'name': 'P17'}, {'name': 'P20'}, {'name': 'P21'}, {'name': 'P22'}, {'name': 'P23'}, {'name': 'P24'}, {'name': 'P25'}, {'name': 'P26'}, {'name': 'P27'}, {'name': 'T0'}, {'name': 'T1'}, {'name': 'INT'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'ALE'}, {'name': 'PSEN'}, {'name': 'PROG'}, {'name': 'EA'}, {'name': 'SS'}, {'name': 'TO'}, {'name': 'SYNC'}, {'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'}, {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VBB'}]
        },
        {
            "name": "ZX8301 Master",
            "chip_id": "ql_zx8301",
            "category": "Custom",
            "description": "ZX8301 Master Chip - CPU interface, DRAM control, video timing",
            "package_types": ['PLCC-84'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'AS'}, {'name': 'DS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'RAS0'}, {'name': 'RAS1'}, {'name': 'CAS'}, {'name': 'WE'}, {'name': 'OE'}, {'name': 'MUX'}, {'name': 'REF'}, {'name': 'RFSH'}, {'name': 'CSYNC'}, {'name': 'VSYNC'}, {'name': 'HSYNC'}, {'name': 'BLANK'}, {'name': 'DISEN'}, {'name': 'FLASH'}, {'name': 'VDATA'}, {'name': 'VCLK'}, {'name': 'COMDATA'}, {'name': 'COMCLK'}, {'name': 'BAUDX16'}, {'name': 'CTS1'}, {'name': 'CTS2'}, {'name': 'DTR1'}, {'name': 'DTR2'}, {'name': 'TXD1'}, {'name': 'TXD2'}, {'name': 'RXD1'}, {'name': 'RXD2'}, {'name': 'RTXC1'}, {'name': 'RTXC2'}, {'name': 'TRXC1'}, {'name': 'TRXC2'}, {'name': 'IPL2'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'CLK'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}]
        },
        {
            "name": "ZX8302 Peripheral",
            "chip_id": "ql_zx8302",
            "category": "Custom",
            "description": "ZX8302 Peripheral Chip - Real time clock, RS232, network interface",
            "package_types": ['PLCC-68'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'CS'}, {'name': 'RW'}, {'name': 'DS'}, {'name': 'DTACK'}, {'name': 'IPL7'}, {'name': 'RESET'}, {'name': 'TXD1'}, {'name': 'RXD1'}, {'name': 'RTS1'}, {'name': 'CTS1'}, {'name': 'DTR1'}, {'name': 'DSR1'}, {'name': 'DCD1'}, {'name': 'TXD2'}, {'name': 'RXD2'}, {'name': 'RTS2'}, {'name': 'CTS2'}, {'name': 'DTR2'}, {'name': 'DSR2'}, {'name': 'DCD2'}, {'name': 'BAUDX16'}, {'name': 'BAUDX1'}, {'name': 'NET1'}, {'name': 'NET2'}, {'name': 'NETCK'}, {'name': 'NETDIR'}, {'name': 'RTCX1'}, {'name': 'RTCX2'}, {'name': 'RTCDATA'}, {'name': 'VBAT'}, {'name': 'MDV1_DATA'}, {'name': 'MDV2_DATA'}, {'name': 'MDV1_CLK'}, {'name': 'MDV2_CLK'}, {'name': 'MDV1_ERASE'}, {'name': 'MDV2_ERASE'}, {'name': 'MDV1_RW'}, {'name': 'MDV2_RW'}, {'name': 'MDV1_WP'}, {'name': 'MDV2_WP'}, {'name': 'MDV_SEL'}, {'name': 'MDV_MOTOR'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'CLK'}, {'name': 'TEST'}]
        },
        {
            "name": "OS ROM",
            "chip_id": "ql_os_rom",
            "category": "Memory",
            "description": "48KB Operating System ROM (QDOS)",
            "package_types": ['DIP-28'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CE'}, {'name': 'OE'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "DRAM 4164",
            "chip_id": "ql_dram_4164",
            "category": "Memory",
            "description": "64Kx1 Dynamic RAM - 8 chips for 128KB system",
            "package_types": ['DIP-16'],
            "pins": [{'name': 'VBB'}, {'name': 'DIN'}, {'name': 'WRITE'}, {'name': 'RAS'}, {'name': 'A0'}, {'name': 'A2'}, {'name': 'A1'}, {'name': 'VDD'}, {'name': 'VCC'}, {'name': 'DOUT'}, {'name': 'CAS'}, {'name': 'A3'}, {'name': 'A6'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'VSS'}]
        },
    ],
    "spectrum_next": [
        {
            "name": "FPGA XC6SLX16",
            "chip_id": "specnext_fpga",
            "category": "FPGA",
            "description": "Xilinx Spartan-6 FPGA - Main system implementation",
            "package_types": ['TQFP-144', 'CSBGA-196'],
            "pins": [{'name': 'PROGRAM_B'}, {'name': 'INIT_B'}, {'name': 'DONE'}, {'name': 'CCLK'}, {'name': 'DIN'}, {'name': 'DOUT'}, {'name': 'M0'}, {'name': 'M1'}, {'name': 'M2'}, {'name': 'TCK'}, {'name': 'TDI'}, {'name': 'TDO'}, {'name': 'TMS'}, {'name': 'HSWAPEN'}, {'name': 'SUSPEND'}, {'name': 'AWAKE'}, {'name': 'VCCINT'}, {'name': 'VCCAUX'}, {'name': 'VCCO_0'}, {'name': 'VCCO_1'}, {'name': 'VCCO_2'}, {'name': 'VCCO_3'}, {'name': 'GND'}, {'name': 'GNDINT'}, {'name': 'GCLK0'}, {'name': 'GCLK1'}, {'name': 'GCLK2'}, {'name': 'GCLK3'}, {'name': 'IO_L1P_0'}, {'name': 'IO_L1N_0'}, {'name': 'IO_L2P_0'}, {'name': 'IO_L2N_0'}, {'name': 'IO_L3P_0'}, {'name': 'IO_L3N_0'}, {'name': 'IO_L4P_0'}, {'name': 'IO_L4N_0'}, {'name': 'IO_L1P_1'}, {'name': 'IO_L1N_1'}, {'name': 'IO_L2P_1'}, {'name': 'IO_L2N_1'}, {'name': 'IO_L3P_1'}, {'name': 'IO_L3N_1'}, {'name': 'IO_L4P_1'}, {'name': 'IO_L4N_1'}, {'name': 'IO_L1P_2'}, {'name': 'IO_L1N_2'}, {'name': 'IO_L2P_2'}, {'name': 'IO_L2N_2'}, {'name': 'IO_L3P_2'}, {'name': 'IO_L3N_2'}, {'name': 'IO_L4P_2'}, {'name': 'IO_L4N_2'}, {'name': 'IO_L1P_3'}, {'name': 'IO_L1N_3'}, {'name': 'IO_L2P_3'}, {'name': 'IO_L2N_3'}, {'name': 'IO_L3P_3'}, {'name': 'IO_L3N_3'}, {'name': 'IO_L4P_3'}, {'name': 'IO_L4N_3'}]
        },
        {
            "name": "Pi Zero Module",
            "chip_id": "specnext_pi_zero",
            "category": "Accelerator",
            "description": "Raspberry Pi Zero - Accelerator and WiFi module",
            "package_types": ['Module'],
            "pins": [{'name': '3V3'}, {'name': '5V'}, {'name': 'SDA'}, {'name': 'SCL'}, {'name': 'GPIO4'}, {'name': 'GND'}, {'name': 'GPIO17'}, {'name': 'GPIO18'}, {'name': 'GPIO27'}, {'name': 'GPIO22'}, {'name': 'GPIO23'}, {'name': 'GPIO24'}, {'name': 'GPIO10'}, {'name': 'GPIO9'}, {'name': 'GPIO25'}, {'name': 'GPIO11'}, {'name': 'GPIO8'}, {'name': 'GPIO7'}, {'name': 'GPIO1'}, {'name': 'GPIO12'}, {'name': 'GND2'}, {'name': 'GPIO16'}, {'name': 'GPIO20'}, {'name': 'GPIO21'}, {'name': 'USB_DP'}, {'name': 'USB_DM'}, {'name': 'USB_ID'}, {'name': 'USB_5V'}, {'name': 'HDMI_HPD'}, {'name': 'HDMI_SDA'}, {'name': 'HDMI_SCL'}, {'name': 'HDMI_CEC'}, {'name': 'CAM_GPIO'}, {'name': 'CAM_SCL'}, {'name': 'CAM_SDA'}, {'name': 'DSI_D0P'}, {'name': 'DSI_D0N'}, {'name': 'DSI_D1P'}, {'name': 'DSI_D1N'}, {'name': 'DSI_CKP'}, {'name': 'DSI_CKN'}]
        },
        {
            "name": "Audio Codec WM8731",
            "chip_id": "specnext_audio_codec",
            "category": "Audio",
            "description": "Cirrus Logic WM8731 - High quality audio codec",
            "package_types": ['SSOP-28'],
            "pins": [{'name': 'LOUT'}, {'name': 'ROUT'}, {'name': 'LHPOUT'}, {'name': 'RHPOUT'}, {'name': 'LINEIN'}, {'name': 'RINEIN'}, {'name': 'MICIN'}, {'name': 'MICBIAS'}, {'name': 'DACDAT'}, {'name': 'DACLRCK'}, {'name': 'BCLK'}, {'name': 'ADCDAT'}, {'name': 'ADCLRCK'}, {'name': 'MCLK'}, {'name': 'SDIN'}, {'name': 'SCLK'}, {'name': 'MODE'}, {'name': 'CSB'}, {'name': 'XTI'}, {'name': 'XTO'}, {'name': 'AVDD'}, {'name': 'DVDD'}, {'name': 'DCVDD'}, {'name': 'DBVDD'}, {'name': 'AGND'}, {'name': 'DGND'}, {'name': 'HPGND'}, {'name': 'VMID'}]
        },
        {
            "name": "RTC DS1307",
            "chip_id": "specnext_rtc",
            "category": "Timing",
            "description": "Dallas DS1307 - Real Time Clock with battery backup",
            "package_types": ['DIP-8', 'SOIC-8'],
            "pins": [{'name': 'X1'}, {'name': 'X2'}, {'name': 'VBAT'}, {'name': 'GND'}, {'name': 'SDA'}, {'name': 'SCL'}, {'name': 'SQW'}, {'name': 'VCC'}]
        },
        {
            "name": "ESP-07S WiFi",
            "chip_id": "specnext_esp07s",
            "category": "Wireless",
            "description": "ESP8266 WiFi module for Next connectivity",
            "package_types": ['Module'],
            "pins": [{'name': 'RESET'}, {'name': 'ADC'}, {'name': 'CH_PD'}, {'name': 'GPIO16'}, {'name': 'GPIO14'}, {'name': 'GPIO12'}, {'name': 'GPIO13'}, {'name': 'VCC'}, {'name': 'CS0'}, {'name': 'MISO'}, {'name': 'GPIO9'}, {'name': 'GPIO10'}, {'name': 'MOSI'}, {'name': 'SCLK'}, {'name': 'GND'}, {'name': 'GPIO15'}, {'name': 'GPIO2'}, {'name': 'GPIO0'}, {'name': 'GPIO4'}, {'name': 'GPIO5'}, {'name': 'RXD'}, {'name': 'TXD'}, {'name': 'GPIO1'}, {'name': 'GPIO3'}]
        },
        {
            "name": "SD Card Slot",
            "chip_id": "specnext_sd_slot",
            "category": "Storage",
            "description": "MicroSD card slot for Next storage",
            "package_types": ['Connector'],
            "pins": [{'name': 'DAT2'}, {'name': 'DAT3'}, {'name': 'CMD'}, {'name': 'VDD'}, {'name': 'CLK'}, {'name': 'VSS'}, {'name': 'DAT0'}, {'name': 'DAT1'}, {'name': 'CD'}, {'name': 'WP'}, {'name': 'SHELL1'}, {'name': 'SHELL2'}]
        },
        {
            "name": "USB Hub FE1.1s",
            "chip_id": "specnext_usb_hub",
            "category": "Interface",
            "description": "4-port USB 2.0 Hub Controller",
            "package_types": ['SSOP-28'],
            "pins": [{'name': 'USBDM'}, {'name': 'USBDP'}, {'name': 'RREF'}, {'name': 'AVDD33'}, {'name': 'AVSS'}, {'name': 'DVDD33'}, {'name': 'DVSS'}, {'name': 'TEST'}, {'name': 'DN1DM'}, {'name': 'DN1DP'}, {'name': 'DN2DM'}, {'name': 'DN2DP'}, {'name': 'DN3DM'}, {'name': 'DN3DP'}, {'name': 'DN4DM'}, {'name': 'DN4DP'}, {'name': 'RSTB'}, {'name': 'SUSP'}, {'name': 'SCLK'}, {'name': 'SDAT'}, {'name': 'GANGED'}, {'name': 'PWRON1'}, {'name': 'PWRON2'}, {'name': 'PWRON3'}, {'name': 'PWRON4'}, {'name': 'OVRCUR1'}, {'name': 'OVRCUR2'}, {'name': 'OVRCUR3'}]
        },
        {
            "name": "Joystick Interface",
            "chip_id": "specnext_joystick",
            "category": "Interface",
            "description": "Atari-style DB9 joystick connectors",
            "package_types": ['DB9-Connector'],
            "pins": [{'name': 'J1_UP'}, {'name': 'J1_DOWN'}, {'name': 'J1_LEFT'}, {'name': 'J1_RIGHT'}, {'name': 'J1_FIRE1'}, {'name': 'J1_FIRE2'}, {'name': 'J1_FIRE3'}, {'name': 'J1_5V'}, {'name': 'J1_GND'}, {'name': 'J2_UP'}, {'name': 'J2_DOWN'}, {'name': 'J2_LEFT'}, {'name': 'J2_RIGHT'}, {'name': 'J2_FIRE1'}, {'name': 'J2_FIRE2'}, {'name': 'J2_FIRE3'}, {'name': 'J2_5V'}, {'name': 'J2_GND'}]
        },
        {
            "name": "SRAM AS6C4008",
            "chip_id": "specnext_sram",
            "category": "Memory",
            "description": "512KB SRAM for Next extended memory",
            "package_types": ['SOP-32'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CE1'}, {'name': 'CE2'}, {'name': 'OE'}, {'name': 'WE'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
    ],
    "ti99": [
        {
            "name": "TMS9900 CPU",
            "chip_id": "ti99_tms9900",
            "category": "Processor",
            "description": "16-bit Microprocessor for TI-99/4A",
            "package_types": ['DIP-64', 'QFP-64'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'CRUCLK'}, {'name': 'CRUOUT'}, {'name': 'CRUIN'}, {'name': 'IC0'}, {'name': 'IC1'}, {'name': 'IC2'}, {'name': 'IC3'}, {'name': 'INTREQ'}, {'name': 'WE'}, {'name': 'DBIN'}, {'name': 'READY'}, {'name': 'WAIT'}, {'name': 'HOLD'}, {'name': 'HOLDA'}, {'name': 'LOAD'}, {'name': 'RESET'}, {'name': 'IAQ'}, {'name': 'AS'}, {'name': 'MEMEN'}, {'name': 'φ1'}, {'name': 'φ2'}, {'name': 'φ3'}, {'name': 'φ4'}, {'name': 'XOUT'}, {'name': 'XIN'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VBB'}, {'name': 'VDD'}, {'name': 'VSS'}, {'name': 'VCC2'}, {'name': 'GND2'}]
        },
        {
            "name": "TMS9901 PSI",
            "chip_id": "ti99_tms9901",
            "category": "I/O",
            "description": "Programmable Systems Interface for TI-99/4A",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'P0'}, {'name': 'P1'}, {'name': 'P2'}, {'name': 'P3'}, {'name': 'P4'}, {'name': 'P5'}, {'name': 'P6'}, {'name': 'P7'}, {'name': 'P8'}, {'name': 'P9'}, {'name': 'P10'}, {'name': 'P11'}, {'name': 'P12'}, {'name': 'P13'}, {'name': 'P14'}, {'name': 'P15'}, {'name': 'INT1'}, {'name': 'INT2'}, {'name': 'INT3'}, {'name': 'INT4'}, {'name': 'INT5'}, {'name': 'INT6'}, {'name': 'INT7'}, {'name': 'INT8'}, {'name': 'INT9'}, {'name': 'INT10'}, {'name': 'INT11'}, {'name': 'INT12'}, {'name': 'INT13'}, {'name': 'INT14'}, {'name': 'INT15'}, {'name': 'INTREQ'}, {'name': 'IC0'}, {'name': 'IC1'}, {'name': 'IC2'}, {'name': 'IC3'}, {'name': 'CE'}, {'name': 'CRUCLK'}, {'name': 'CRUOUT'}, {'name': 'CRUIN'}, {'name': 'φ4'}, {'name': 'RESET'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "TMS9918A VDP",
            "chip_id": "ti99_tms9918a",
            "category": "Video",
            "description": "Video Display Processor for TI-99/4A",
            "package_types": ['DIP-40', 'QFP-44'],
            "pins": [{'name': 'AD0'}, {'name': 'AD1'}, {'name': 'AD2'}, {'name': 'AD3'}, {'name': 'AD4'}, {'name': 'AD5'}, {'name': 'AD6'}, {'name': 'AD7'}, {'name': 'RAS'}, {'name': 'CAS'}, {'name': 'AD8'}, {'name': 'AD9'}, {'name': 'AD10'}, {'name': 'AD11'}, {'name': 'AD12'}, {'name': 'AD13'}, {'name': 'CD0'}, {'name': 'CD1'}, {'name': 'CD2'}, {'name': 'CD3'}, {'name': 'CD4'}, {'name': 'CD5'}, {'name': 'CD6'}, {'name': 'CD7'}, {'name': 'MODE'}, {'name': 'CSW'}, {'name': 'CSR'}, {'name': 'INT'}, {'name': 'GROMCLK'}, {'name': 'CPUCLK'}, {'name': 'XTAL1'}, {'name': 'XTAL2'}, {'name': 'Y'}, {'name': 'RY'}, {'name': 'R'}, {'name': 'G'}, {'name': 'B'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}]
        },
        {
            "name": "SN76489 PSG",
            "chip_id": "ti99_sn76489",
            "category": "Audio",
            "description": "Programmable Sound Generator for TI-99/4A",
            "package_types": ['DIP-16'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'WE'}, {'name': 'CE'}, {'name': 'READY'}, {'name': 'CLOCK'}, {'name': 'AUDIO'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}]
        },
        {
            "name": "TMS9980 CPU",
            "chip_id": "ti99_tms9980",
            "category": "Processor",
            "description": "16-bit Microprocessor with 8-bit data bus",
            "package_types": ['DIP-40'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CRUCLK'}, {'name': 'CRUOUT'}, {'name': 'CRUIN'}, {'name': 'IC0'}, {'name': 'IC1'}, {'name': 'IC2'}, {'name': 'IC3'}, {'name': 'INTREQ'}, {'name': 'WE'}, {'name': 'DBIN'}, {'name': 'READY'}, {'name': 'WAIT'}, {'name': 'HOLD'}, {'name': 'HOLDA'}, {'name': 'RESET'}, {'name': 'φ4'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
    ],
    "x68000": [
        {
            "name": "MC68000 CPU",
            "chip_id": "x68k_68000",
            "category": "Processor",
            "description": "Motorola 68000 CPU - 16/32-bit processor for X68000",
            "package_types": ['DIP-64', 'PGA-68', 'QFP-68'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'}, {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'}, {'name': 'AS'}, {'name': 'UDS'}, {'name': 'LDS'}, {'name': 'R/W'}, {'name': 'DTACK'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'BR'}, {'name': 'FC0'}, {'name': 'FC1'}, {'name': 'FC2'}, {'name': 'IPL0'}, {'name': 'IPL1'}, {'name': 'IPL2'}, {'name': 'BERR'}, {'name': 'VPA'}, {'name': 'VMA'}, {'name': 'E'}, {'name': 'RESET'}, {'name': 'HALT'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}]
        },
        {
            "name": "CRTC HD63484",
            "chip_id": "x68k_crtc",
            "category": "Video",
            "description": "Advanced CRT Controller for X68000 graphics",
            "package_types": ['QFP-100'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'INT'}, {'name': 'RDY'}, {'name': 'VA0'}, {'name': 'VA1'}, {'name': 'VA2'}, {'name': 'VA3'}, {'name': 'VA4'}, {'name': 'VA5'}, {'name': 'VA6'}, {'name': 'VA7'}, {'name': 'VA8'}, {'name': 'VA9'}, {'name': 'VA10'}, {'name': 'VA11'}, {'name': 'VA12'}, {'name': 'VA13'}, {'name': 'VA14'}, {'name': 'VA15'}, {'name': 'VA16'}, {'name': 'VA17'}, {'name': 'VA18'}, {'name': 'VA19'}, {'name': 'VD0'}, {'name': 'VD1'}, {'name': 'VD2'}, {'name': 'VD3'}, {'name': 'VD4'}, {'name': 'VD5'}, {'name': 'VD6'}, {'name': 'VD7'}, {'name': 'VD8'}, {'name': 'VD9'}, {'name': 'VD10'}, {'name': 'VD11'}, {'name': 'VD12'}, {'name': 'VD13'}, {'name': 'VD14'}, {'name': 'VD15'}, {'name': 'VRAS'}, {'name': 'VCAS'}, {'name': 'VWE'}, {'name': 'VOE'}, {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'DCLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}]
        },
        {
            "name": "VSOP HD63450",
            "chip_id": "x68k_vsop",
            "category": "Video",
            "description": "Video System On-chip Processor for sprites and text",
            "package_types": ['QFP-120'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'INT'}, {'name': 'DMA_REQ'}, {'name': 'DMA_ACK'}, {'name': 'CLK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}]
        },
        {
            "name": "PCM8 MSM6258V",
            "chip_id": "x68k_pcm8",
            "category": "Audio",
            "description": "8-bit PCM sound chip for X68000",
            "package_types": ['DIP-18'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CS'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'AOUT'}, {'name': 'VR'}, {'name': 'VREF'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}]
        },
        {
            "name": "FM YM2151",
            "chip_id": "x68k_ym2151",
            "category": "Audio",
            "description": "FM Sound Synthesizer for X68000",
            "package_types": ['DIP-24'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'A0'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'IC'}, {'name': 'IRQ'}, {'name': 'φM'}, {'name': 'SO'}, {'name': 'SH1'}, {'name': 'SH2'}, {'name': 'CT1'}, {'name': 'CT2'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}]
        },
        {
            "name": "DMAC HD63450",
            "chip_id": "x68k_dmac",
            "category": "Custom",
            "description": "DMA Controller for X68000 system",
            "package_types": ['QFP-68'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'}, {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'CS'}, {'name': 'UDS'}, {'name': 'LDS'}, {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'AS'}, {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'INT'}, {'name': 'IACK'}, {'name': 'BR'}, {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'DREQ0'}, {'name': 'DREQ1'}, {'name': 'DREQ2'}, {'name': 'DREQ3'}, {'name': 'DACK0'}, {'name': 'DACK1'}, {'name': 'DACK2'}, {'name': 'DACK3'}, {'name': 'DONE0'}, {'name': 'DONE1'}, {'name': 'DONE2'}, {'name': 'DONE3'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "MFP MC68901",
            "chip_id": "x68k_mfp",
            "category": "I/O",
            "description": "Multi Function Peripheral - Timers, UART, parallel I/O",
            "package_types": ['DIP-48', 'QFP-52'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'RS1'}, {'name': 'RS2'}, {'name': 'RS3'}, {'name': 'RS4'}, {'name': 'RS5'}, {'name': 'CS'}, {'name': 'RW'}, {'name': 'DS'}, {'name': 'DTACK'}, {'name': 'IEI'}, {'name': 'IEO'}, {'name': 'IACK'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'CLK'}, {'name': 'RESET'}, {'name': 'I0'}, {'name': 'I1'}, {'name': 'I2'}, {'name': 'I3'}, {'name': 'I4'}, {'name': 'I5'}, {'name': 'I6'}, {'name': 'I7'}, {'name': 'GPIP0'}, {'name': 'GPIP1'}, {'name': 'GPIP2'}, {'name': 'GPIP3'}, {'name': 'GPIP4'}, {'name': 'GPIP5'}, {'name': 'GPIP6'}, {'name': 'GPIP7'}, {'name': 'TAI'}, {'name': 'TBI'}, {'name': 'TAO'}, {'name': 'TBO'}, {'name': 'TCO'}, {'name': 'TDO'}, {'name': 'SI'}, {'name': 'SO'}, {'name': 'RC'}, {'name': 'TC'}, {'name': 'RR'}, {'name': 'TR'}]
        },
        {
            "name": "FDC MB89311",
            "chip_id": "x68k_fdc",
            "category": "Storage",
            "description": "Floppy Disk Controller for X68000",
            "package_types": ['QFP-44'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'INT'}, {'name': 'DRQ'}, {'name': 'DACK'}, {'name': 'CLK'}, {'name': 'STEP'}, {'name': 'DIR'}, {'name': 'WGATE'}, {'name': 'WDATA'}, {'name': 'RDATA'}, {'name': 'READY'}, {'name': 'INDEX'}, {'name': 'TRK00'}, {'name': 'WPRT'}, {'name': 'DS0'}, {'name': 'DS1'}, {'name': 'MOTOR'}, {'name': 'VCC'}, {'name': 'GND'}]
        },
        {
            "name": "RTC RP5C15",
            "chip_id": "x68k_rtc",
            "category": "Custom",
            "description": "Real Time Clock for X68000 system",
            "package_types": ['DIP-18'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'CLK'}, {'name': 'ALARM'}, {'name': 'VBAT'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'OSC'}]
        },
        {
            "name": "SASI Controller",
            "chip_id": "x68k_sasi",
            "category": "Storage",
            "description": "SASI/SCSI hard disk controller for X68000",
            "package_types": ['QFP-68'],
            "pins": [{'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'INT'}, {'name': 'DRQ'}, {'name': 'DACK'}, {'name': 'CLK'}, {'name': 'BSY'}, {'name': 'SEL'}, {'name': 'CD'}, {'name': 'IO'}, {'name': 'MSG'}, {'name': 'REQ'}, {'name': 'ACK'}, {'name': 'ATN'}, {'name': 'RST'}, {'name': 'DB0'}, {'name': 'DB1'}, {'name': 'DB2'}, {'name': 'DB3'}, {'name': 'DB4'}, {'name': 'DB5'}, {'name': 'DB6'}, {'name': 'DB7'}, {'name': 'DBP'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'TERM_PWR'}]
        },
    ],
    "zx80": [
        {
            "name": "ULA ZX80",
            "chip_id": "zx80_ula",
            "category": "Custom",
            "description": "Uncommitted Logic Array for ZX80",
            "package_types": ['DIP-28'],
            "pins": [{'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CLK'}, {'name': 'SYNC'}, {'name': 'VIDEO'}, {'name': 'VCC'}, {'name': 'GND'}, {'name': 'NC'}]
        },
    ],
}

def get_chip_by_name(name: str):
    """Get chip definition by name"""
    for chips in COMPONENT_LIBRARY.values():
        for chip in chips:
            if chip["name"].lower() == name.lower():
                return chip
    return None

def get_chips_by_category(category: str):
    """Get all chips in a category"""
    result = []
    for chips in COMPONENT_LIBRARY.values():
        for chip in chips:
            if chip["category"].lower() == category.lower():
                result.append(chip)
    return result

def get_all_chips():
    """Get all chip definitions"""
    result = []
    for chips in COMPONENT_LIBRARY.values():
        result.extend(chips)
    return result
