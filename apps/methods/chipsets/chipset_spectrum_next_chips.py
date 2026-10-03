"""
X-Seti June13 2025 - ZX Spectrum Next Chipset Definitions
Visual Retro System Emulator Builder - ZX Spectrum Next Core Chips
"""

def add_spectrum_next_chips(generator):
    """Add ZX Spectrum Next chipset components"""
    
    # FPGA - Main System FPGA (Xilinx Spartan-6)
    generator.add_chip(
        name="FPGA XC6SLX16",
        chip_id="specnext_fpga",
        category="FPGA",
        description="Xilinx Spartan-6 FPGA - Main system implementation",
        package_types=["TQFP-144", "CSBGA-196"],
        pins=[
            # Configuration
            {'name': 'PROGRAM_B'}, {'name': 'INIT_B'}, {'name': 'DONE'}, {'name': 'CCLK'},
            {'name': 'DIN'}, {'name': 'DOUT'}, {'name': 'M0'}, {'name': 'M1'},
            {'name': 'M2'}, {'name': 'TCK'}, {'name': 'TDI'}, {'name': 'TDO'},
            {'name': 'TMS'}, {'name': 'HSWAPEN'}, {'name': 'SUSPEND'}, {'name': 'AWAKE'},
            # Power
            {'name': 'VCCINT'}, {'name': 'VCCAUX'}, {'name': 'VCCO_0'}, {'name': 'VCCO_1'},
            {'name': 'VCCO_2'}, {'name': 'VCCO_3'}, {'name': 'GND'}, {'name': 'GNDINT'},
            # Clock
            {'name': 'GCLK0'}, {'name': 'GCLK1'}, {'name': 'GCLK2'}, {'name': 'GCLK3'},
            # I/O Banks
            {'name': 'IO_L1P_0'}, {'name': 'IO_L1N_0'}, {'name': 'IO_L2P_0'}, {'name': 'IO_L2N_0'},
            {'name': 'IO_L3P_0'}, {'name': 'IO_L3N_0'}, {'name': 'IO_L4P_0'}, {'name': 'IO_L4N_0'},
            {'name': 'IO_L1P_1'}, {'name': 'IO_L1N_1'}, {'name': 'IO_L2P_1'}, {'name': 'IO_L2N_1'},
            {'name': 'IO_L3P_1'}, {'name': 'IO_L3N_1'}, {'name': 'IO_L4P_1'}, {'name': 'IO_L4N_1'},
            {'name': 'IO_L1P_2'}, {'name': 'IO_L1N_2'}, {'name': 'IO_L2P_2'}, {'name': 'IO_L2N_2'},
            {'name': 'IO_L3P_2'}, {'name': 'IO_L3N_2'}, {'name': 'IO_L4P_2'}, {'name': 'IO_L4N_2'},
            {'name': 'IO_L1P_3'}, {'name': 'IO_L1N_3'}, {'name': 'IO_L2P_3'}, {'name': 'IO_L2N_3'},
            {'name': 'IO_L3P_3'}, {'name': 'IO_L3N_3'}, {'name': 'IO_L4P_3'}, {'name': 'IO_L4N_3'}
        ]
    )
    
    # Raspberry Pi Accelerator Module
    generator.add_chip(
        name="Pi Zero Module",
        chip_id="specnext_pi_zero",
        category="Accelerator",
        description="Raspberry Pi Zero - Accelerator and WiFi module",
        package_types=["Module"],
        pins=[
            # GPIO Header
            {'name': '3V3'}, {'name': '5V'}, {'name': 'SDA'}, {'name': 'SCL'},
            {'name': 'GPIO4'}, {'name': 'GND'}, {'name': 'GPIO17'}, {'name': 'GPIO18'},
            {'name': 'GPIO27'}, {'name': 'GPIO22'}, {'name': 'GPIO23'}, {'name': 'GPIO24'},
            {'name': 'GPIO10'}, {'name': 'GPIO9'}, {'name': 'GPIO25'}, {'name': 'GPIO11'},
            {'name': 'GPIO8'}, {'name': 'GPIO7'}, {'name': 'GPIO1'}, {'name': 'GPIO12'},
            {'name': 'GND2'}, {'name': 'GPIO16'}, {'name': 'GPIO20'}, {'name': 'GPIO21'},
            # USB/Power
            {'name': 'USB_DP'}, {'name': 'USB_DM'}, {'name': 'USB_ID'}, {'name': 'USB_5V'},
            # HDMI
            {'name': 'HDMI_HPD'}, {'name': 'HDMI_SDA'}, {'name': 'HDMI_SCL'}, {'name': 'HDMI_CEC'},
            # Camera/Display
            {'name': 'CAM_GPIO'}, {'name': 'CAM_SCL'}, {'name': 'CAM_SDA'}, {'name': 'DSI_D0P'},
            {'name': 'DSI_D0N'}, {'name': 'DSI_D1P'}, {'name': 'DSI_D1N'}, {'name': 'DSI_CKP'},
            {'name': 'DSI_CKN'}
        ]
    )
    
    # Audio Codec - Cirrus Logic
    generator.add_chip(
        name="Audio Codec WM8731",
        chip_id="specnext_audio_codec",
        category="Audio",
        description="Cirrus Logic WM8731 - High quality audio codec",
        package_types=["SSOP-28"],
        pins=[
            # Audio Interface
            {'name': 'LOUT'}, {'name': 'ROUT'}, {'name': 'LHPOUT'}, {'name': 'RHPOUT'},
            {'name': 'LINEIN'}, {'name': 'RINEIN'}, {'name': 'MICIN'}, {'name': 'MICBIAS'},
            # Digital Interface
            {'name': 'DACDAT'}, {'name': 'DACLRCK'}, {'name': 'BCLK'}, {'name': 'ADCDAT'},
            {'name': 'ADCLRCK'}, {'name': 'MCLK'}, {'name': 'SDIN'}, {'name': 'SCLK'},
            {'name': 'MODE'}, {'name': 'CSB'}, {'name': 'XTI'}, {'name': 'XTO'},
            # Power
            {'name': 'AVDD'}, {'name': 'DVDD'}, {'name': 'DCVDD'}, {'name': 'DBVDD'},
            {'name': 'AGND'}, {'name': 'DGND'}, {'name': 'HPGND'}, {'name': 'VMID'}
        ]
    )
    
    # Real Time Clock
    generator.add_chip(
        name="RTC DS1307",
        chip_id="specnext_rtc",
        category="Timing",
        description="Dallas DS1307 - Real Time Clock with battery backup",
        package_types=["DIP-8", "SOIC-8"],
        pins=[
            {'name': 'X1'}, {'name': 'X2'}, {'name': 'VBAT'}, {'name': 'GND'},
            {'name': 'SDA'}, {'name': 'SCL'}, {'name': 'SQW'}, {'name': 'VCC'}
        ]
    )
    
    # ESP WiFi Module
    generator.add_chip(
        name="ESP-07S WiFi",
        chip_id="specnext_esp07s",
        category="Wireless",
        description="ESP8266 WiFi module for Next connectivity",
        package_types=["Module"],
        pins=[
            {'name': 'RESET'}, {'name': 'ADC'}, {'name': 'CH_PD'}, {'name': 'GPIO16'},
            {'name': 'GPIO14'}, {'name': 'GPIO12'}, {'name': 'GPIO13'}, {'name': 'VCC'},
            {'name': 'CS0'}, {'name': 'MISO'}, {'name': 'GPIO9'}, {'name': 'GPIO10'},
            {'name': 'MOSI'}, {'name': 'SCLK'}, {'name': 'GND'}, {'name': 'GPIO15'},
            {'name': 'GPIO2'}, {'name': 'GPIO0'}, {'name': 'GPIO4'}, {'name': 'GPIO5'},
            {'name': 'RXD'}, {'name': 'TXD'}, {'name': 'GPIO1'}, {'name': 'GPIO3'}
        ]
    )
    
    # SD Card Controller
    generator.add_chip(
        name="SD Card Slot",
        chip_id="specnext_sd_slot",
        category="Storage",
        description="MicroSD card slot for Next storage",
        package_types=["Connector"],
        pins=[
            {'name': 'DAT2'}, {'name': 'DAT3'}, {'name': 'CMD'}, {'name': 'VDD'},
            {'name': 'CLK'}, {'name': 'VSS'}, {'name': 'DAT0'}, {'name': 'DAT1'},
            {'name': 'CD'}, {'name': 'WP'}, {'name': 'SHELL1'}, {'name': 'SHELL2'}
        ]
    )
    
    # USB Hub Controller
    generator.add_chip(
        name="USB Hub FE1.1s",
        chip_id="specnext_usb_hub", 
        category="Interface",
        description="4-port USB 2.0 Hub Controller",
        package_types=["SSOP-28"],
        pins=[
            # USB Upstream
            {'name': 'USBDM'}, {'name': 'USBDP'}, {'name': 'RREF'}, {'name': 'AVDD33'},
            {'name': 'AVSS'}, {'name': 'DVDD33'}, {'name': 'DVSS'}, {'name': 'TEST'},
            # USB Downstream Ports
            {'name': 'DN1DM'}, {'name': 'DN1DP'}, {'name': 'DN2DM'}, {'name': 'DN2DP'},
            {'name': 'DN3DM'}, {'name': 'DN3DP'}, {'name': 'DN4DM'}, {'name': 'DN4DP'},
            # Control
            {'name': 'RSTB'}, {'name': 'SUSP'}, {'name': 'SCLK'}, {'name': 'SDAT'},
            {'name': 'GANGED'}, {'name': 'PWRON1'}, {'name': 'PWRON2'}, {'name': 'PWRON3'},
            {'name': 'PWRON4'}, {'name': 'OVRCUR1'}, {'name': 'OVRCUR2'}, {'name': 'OVRCUR3'}
        ]
    )
    
    # Joystick Interface - DB9 Connectors
    generator.add_chip(
        name="Joystick Interface",
        chip_id="specnext_joystick",
        category="Interface",
        description="Atari-style DB9 joystick connectors",
        package_types=["DB9-Connector"],
        pins=[
            # Joystick 1
            {'name': 'J1_UP'}, {'name': 'J1_DOWN'}, {'name': 'J1_LEFT'}, {'name': 'J1_RIGHT'},
            {'name': 'J1_FIRE1'}, {'name': 'J1_FIRE2'}, {'name': 'J1_FIRE3'}, {'name': 'J1_5V'},
            {'name': 'J1_GND'},
            # Joystick 2
            {'name': 'J2_UP'}, {'name': 'J2_DOWN'}, {'name': 'J2_LEFT'}, {'name': 'J2_RIGHT'},
            {'name': 'J2_FIRE1'}, {'name': 'J2_FIRE2'}, {'name': 'J2_FIRE3'}, {'name': 'J2_5V'},
            {'name': 'J2_GND'}
        ]
    )
    
    # Memory - SRAM
    generator.add_chip(
        name="SRAM AS6C4008",
        chip_id="specnext_sram",
        category="Memory",
        description="512KB SRAM for Next extended memory",
        package_types=["SOP-32"],
        pins=[
            {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'}, {'name': 'A3'},
            {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'}, {'name': 'A7'},
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A16'}, {'name': 'A17'}, {'name': 'A18'}, {'name': 'D0'},
            {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'},
            {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'CE1'},
            {'name': 'CE2'}, {'name': 'OE'}, {'name': 'WE'}, {'name': 'VCC'},
            {'name': 'GND'}
        ]
    )

if __name__ == "__main__":
    # Test function
    print("ZX Spectrum Next chipset definitions loaded")
    print("Available chips: FPGA, Pi Zero, Audio Codec, RTC, ESP WiFi, SD Card, USB Hub, Joystick, SRAM")
