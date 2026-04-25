"""
X-Seti June13 2025 - Sharp X68000 Chipset Definitions
Visual Retro System Emulator Builder - Sharp X68000 Core Chips
"""

def add_x68000_chips(generator):
    """Add Sharp X68000 chipset components"""
    
    # 68000 CPU - Main processor
    generator.add_chip(
        name="MC68000 CPU",
        chip_id="x68k_68000",
        category="Processor",
        description="Motorola 68000 CPU - 16/32-bit processor for X68000",
        package_types=["DIP-64", "PGA-68", "QFP-68"],
        pins=[
            # Data Bus
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            # Address Bus
            {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'},
            {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'}, {'name': 'A8'},
            {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'}, {'name': 'A12'},
            {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}, {'name': 'A16'},
            {'name': 'A17'}, {'name': 'A18'}, {'name': 'A19'}, {'name': 'A20'},
            {'name': 'A21'}, {'name': 'A22'}, {'name': 'A23'}, {'name': 'AS'},
            # Control Signals
            {'name': 'UDS'}, {'name': 'LDS'}, {'name': 'R/W'}, {'name': 'DTACK'},
            {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'BR'}, {'name': 'FC0'},
            {'name': 'FC1'}, {'name': 'FC2'}, {'name': 'IPL0'}, {'name': 'IPL1'},
            {'name': 'IPL2'}, {'name': 'BERR'}, {'name': 'VPA'}, {'name': 'VMA'},
            {'name': 'E'}, {'name': 'RESET'}, {'name': 'HALT'}, {'name': 'CLK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VCC2'}, {'name': 'GND2'}
        ]
    )

    # Custom Chips - Video Controller 1
    generator.add_chip(
        name="CRTC HD63484",
        chip_id="x68k_crtc",
        category="Video",
        description="Advanced CRT Controller for X68000 graphics",
        package_types=["QFP-100"],
        pins=[
            # CPU Interface
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RD'},
            {'name': 'WR'}, {'name': 'RESET'}, {'name': 'INT'}, {'name': 'RDY'},
            # VRAM Interface
            {'name': 'VA0'}, {'name': 'VA1'}, {'name': 'VA2'}, {'name': 'VA3'},
            {'name': 'VA4'}, {'name': 'VA5'}, {'name': 'VA6'}, {'name': 'VA7'},
            {'name': 'VA8'}, {'name': 'VA9'}, {'name': 'VA10'}, {'name': 'VA11'},
            {'name': 'VA12'}, {'name': 'VA13'}, {'name': 'VA14'}, {'name': 'VA15'},
            {'name': 'VA16'}, {'name': 'VA17'}, {'name': 'VA18'}, {'name': 'VA19'},
            {'name': 'VD0'}, {'name': 'VD1'}, {'name': 'VD2'}, {'name': 'VD3'},
            {'name': 'VD4'}, {'name': 'VD5'}, {'name': 'VD6'}, {'name': 'VD7'},
            {'name': 'VD8'}, {'name': 'VD9'}, {'name': 'VD10'}, {'name': 'VD11'},
            {'name': 'VD12'}, {'name': 'VD13'}, {'name': 'VD14'}, {'name': 'VD15'},
            {'name': 'VRAS'}, {'name': 'VCAS'}, {'name': 'VWE'}, {'name': 'VOE'},
            # Video Output
            {'name': 'HSYNC'}, {'name': 'VSYNC'}, {'name': 'BLANK'}, {'name': 'DCLK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}
        ]
    )

    # Video Controller 2 - Sprite/Text
    generator.add_chip(
        name="VSOP HD63450",
        chip_id="x68k_vsop",
        category="Video",
        description="Video System On-chip Processor for sprites and text",
        package_types=["QFP-120"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'},
            {'name': 'INT'}, {'name': 'DMA_REQ'}, {'name': 'DMA_ACK'}, {'name': 'CLK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}
        ]
    )

    # PCM Sound Chip
    generator.add_chip(
        name="PCM8 MSM6258V",
        chip_id="x68k_pcm8",
        category="Audio",
        description="8-bit PCM sound chip for X68000",
        package_types=["DIP-18"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'CS'}, {'name': 'WR'}, {'name': 'RESET'}, {'name': 'CLK'},
            {'name': 'AOUT'}, {'name': 'VR'}, {'name': 'VREF'}, {'name': 'VCC'},
            {'name': 'GND'}, {'name': 'NC'}
        ]
    )

    # FM Sound Synthesizer
    generator.add_chip(
        name="FM YM2151",
        chip_id="x68k_ym2151",
        category="Audio",
        description="FM Sound Synthesizer for X68000",
        package_types=["DIP-24"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'IC'}, {'name': 'IRQ'}, {'name': 'φM'}, {'name': 'SO'},
            {'name': 'SH1'}, {'name': 'SH2'}, {'name': 'CT1'}, {'name': 'CT2'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'VDD'}, {'name': 'VSS'}
        ]
    )

    # DMAC - DMA Controller
    generator.add_chip(
        name="DMAC HD63450",
        chip_id="x68k_dmac",
        category="Custom",
        description="DMA Controller for X68000 system",
        package_types=["QFP-68"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'D8'}, {'name': 'D9'}, {'name': 'D10'}, {'name': 'D11'},
            {'name': 'D12'}, {'name': 'D13'}, {'name': 'D14'}, {'name': 'D15'},
            {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'}, {'name': 'A4'},
            {'name': 'A5'}, {'name': 'CS'}, {'name': 'UDS'}, {'name': 'LDS'},
            {'name': 'RW'}, {'name': 'DTACK'}, {'name': 'AS'}, {'name': 'RESET'},
            {'name': 'CLK'}, {'name': 'INT'}, {'name': 'IACK'}, {'name': 'BR'},
            {'name': 'BG'}, {'name': 'BGACK'}, {'name': 'DREQ0'}, {'name': 'DREQ1'},
            {'name': 'DREQ2'}, {'name': 'DREQ3'}, {'name': 'DACK0'}, {'name': 'DACK1'},
            {'name': 'DACK2'}, {'name': 'DACK3'}, {'name': 'DONE0'}, {'name': 'DONE1'},
            {'name': 'DONE2'}, {'name': 'DONE3'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # MFP - Multi Function Peripheral
    generator.add_chip(
        name="MFP MC68901",
        chip_id="x68k_mfp",
        category="I/O",
        description="Multi Function Peripheral - Timers, UART, parallel I/O",
        package_types=["DIP-48", "QFP-52"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'RS1'}, {'name': 'RS2'}, {'name': 'RS3'}, {'name': 'RS4'},
            {'name': 'RS5'}, {'name': 'CS'}, {'name': 'RW'}, {'name': 'DS'},
            {'name': 'DTACK'}, {'name': 'IEI'}, {'name': 'IEO'}, {'name': 'IACK'},
            {'name': 'VCC'}, {'name': 'GND'}, {'name': 'CLK'}, {'name': 'RESET'},
            {'name': 'I0'}, {'name': 'I1'}, {'name': 'I2'}, {'name': 'I3'},
            {'name': 'I4'}, {'name': 'I5'}, {'name': 'I6'}, {'name': 'I7'},
            {'name': 'GPIP0'}, {'name': 'GPIP1'}, {'name': 'GPIP2'}, {'name': 'GPIP3'},
            {'name': 'GPIP4'}, {'name': 'GPIP5'}, {'name': 'GPIP6'}, {'name': 'GPIP7'},
            {'name': 'TAI'}, {'name': 'TBI'}, {'name': 'TAO'}, {'name': 'TBO'},
            {'name': 'TCO'}, {'name': 'TDO'}, {'name': 'SI'}, {'name': 'SO'},
            {'name': 'RC'}, {'name': 'TC'}, {'name': 'RR'}, {'name': 'TR'}
        ]
    )

    # FDC - Floppy Disk Controller
    generator.add_chip(
        name="FDC MB89311",
        chip_id="x68k_fdc",
        category="Storage",
        description="Floppy Disk Controller for X68000",
        package_types=["QFP-44"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'CS'}, {'name': 'RD'},
            {'name': 'WR'}, {'name': 'RESET'}, {'name': 'INT'}, {'name': 'DRQ'},
            {'name': 'DACK'}, {'name': 'CLK'}, {'name': 'STEP'}, {'name': 'DIR'},
            {'name': 'WGATE'}, {'name': 'WDATA'}, {'name': 'RDATA'}, {'name': 'READY'},
            {'name': 'INDEX'}, {'name': 'TRK00'}, {'name': 'WPRT'}, {'name': 'DS0'},
            {'name': 'DS1'}, {'name': 'MOTOR'}, {'name': 'VCC'}, {'name': 'GND'}
        ]
    )

    # RTC - Real Time Clock
    generator.add_chip(
        name="RTC RP5C15",
        chip_id="x68k_rtc",
        category="Custom",
        description="Real Time Clock for X68000 system",
        package_types=["DIP-18"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'}, {'name': 'RESET'},
            {'name': 'CLK'}, {'name': 'ALARM'}, {'name': 'VBAT'}, {'name': 'VCC'},
            {'name': 'GND'}, {'name': 'OSC'}
        ]
    )

    # SASI/SCSI Controller
    generator.add_chip(
        name="SASI Controller",
        chip_id="x68k_sasi",
        category="Storage",
        description="SASI/SCSI hard disk controller for X68000",
        package_types=["QFP-68"],
        pins=[
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'},
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'CS'}, {'name': 'RD'}, {'name': 'WR'},
            {'name': 'RESET'}, {'name': 'INT'}, {'name': 'DRQ'}, {'name': 'DACK'},
            {'name': 'CLK'}, {'name': 'BSY'}, {'name': 'SEL'}, {'name': 'CD'},
            {'name': 'IO'}, {'name': 'MSG'}, {'name': 'REQ'}, {'name': 'ACK'},
            {'name': 'ATN'}, {'name': 'RST'}, {'name': 'DB0'}, {'name': 'DB1'},
            {'name': 'DB2'}, {'name': 'DB3'}, {'name': 'DB4'}, {'name': 'DB5'},
            {'name': 'DB6'}, {'name': 'DB7'}, {'name': 'DBP'}, {'name': 'VCC'},
            {'name': 'GND'}, {'name': 'TERM_PWR'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("Sharp X68000 chipset definitions loaded")
    print("Available chips: MC68000, CRTC, VSOP, PCM8, YM2151, DMAC, MFP, FDC, RTC, SASI")