"""
X-Seti June13 2025 - ZX Spectrum 48K Complete System Definition
Visual Retro System Emulator Builder - Complete ZX Spectrum 48K Computer
"""

def add_zx_spectrum_48k_system(generator):
    """Add complete ZX Spectrum 48K system - all components needed to build the computer"""
    
    # System Information
    system_info = {
        'name': 'Sinclair ZX Spectrum 48K',
        'manufacturer': 'Sinclair Research',
        'year': 1982,
        'cpu_speed': '3.5 MHz',
        'ram': '48 KB',
        'rom': '16 KB',
        'display': '256×192, 8 colors',
        'sound': '1-bit beeper',
        'power': '+5V, +12V, -5V'
    }
    
    # === MAIN PROCESSORS ===
    
    # Z80A CPU - Main processor
    generator.add_component(
        name="Z80A CPU",
        component_id="ic4_z80a",
        category="Processor",
        description="Zilog Z80A 8-bit microprocessor - 3.5MHz",
        package_type="DIP-40",
        position=(100, 150),
        pins=[
            {'name': 'A11'}, {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'},
            {'name': 'A15'}, {'name': 'CLK'}, {'name': 'D4'}, {'name': 'D3'},
            {'name': 'D5'}, {'name': 'D6'}, {'name': 'VCC'}, {'name': 'D2'},
            {'name': 'D7'}, {'name': 'D0'}, {'name': 'D1'}, {'name': 'INT'},
            {'name': 'NMI'}, {'name': 'HALT'}, {'name': 'MREQ'}, {'name': 'IORQ'},
            {'name': 'RD'}, {'name': 'WR'}, {'name': 'BUSAK'}, {'name': 'WAIT'},
            {'name': 'BUSRQ'}, {'name': 'RESET'}, {'name': 'M1'}, {'name': 'RFSH'},
            {'name': 'GND'}, {'name': 'A0'}, {'name': 'A1'}, {'name': 'A2'},
            {'name': 'A3'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'A6'},
            {'name': 'A7'}, {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}
        ]
    )
    
    # === CUSTOM CHIPS ===
    
    # ULA - Uncommitted Logic Array (Heart of the Spectrum)
    generator.add_component(
        name="ULA 6C001E-7",
        component_id="ic5_ula",
        category="Custom",
        description="Custom ULA - Video, audio, keyboard, memory control",
        package_type="DIP-40",
        position=(200, 150),
        pins=[
            {'name': 'A6'}, {'name': 'A5'}, {'name': 'A4'}, {'name': 'A3'},
            {'name': 'A2'}, {'name': 'A1'}, {'name': 'A0'}, {'name': 'D0'},
            {'name': 'D1'}, {'name': 'D2'}, {'name': 'GND'}, {'name': 'D3'},
            {'name': 'D4'}, {'name': 'CAS'}, {'name': 'RAS'}, {'name': 'MUX'},
            {'name': 'ROMCS'}, {'name': 'Y'}, {'name': 'B-Y'}, {'name': 'VCC'},
            {'name': 'CSYNC'}, {'name': 'R-Y'}, {'name': 'φ2'}, {'name': 'φ1'},
            {'name': 'IORQGE'}, {'name': 'CPUClk'}, {'name': 'INT'}, {'name': 'D7'},
            {'name': 'D6'}, {'name': 'D5'}, {'name': 'A14'}, {'name': 'A15'},
            {'name': 'A13'}, {'name': 'A12'}, {'name': 'A11'}, {'name': 'A10'},
            {'name': 'A9'}, {'name': 'A8'}, {'name': 'A7'}, {'name': 'IORQ'}
        ]
    )
    
    # === MEMORY CHIPS ===
    
    # ROM - 16K System ROM
    generator.add_component(
        name="ROM 2364",
        component_id="ic2_rom",
        category="Memory",
        description="16K System ROM - BASIC interpreter and OS",
        package_type="DIP-28",
        position=(50, 100),
        pins=[
            {'name': 'A7'}, {'name': 'A6'}, {'name': 'A5'}, {'name': 'A4'},
            {'name': 'A3'}, {'name': 'A2'}, {'name': 'A1'}, {'name': 'A0'},
            {'name': 'D0'}, {'name': 'D1'}, {'name': 'D2'}, {'name': 'GND'},
            {'name': 'D3'}, {'name': 'D4'}, {'name': 'D5'}, {'name': 'D6'},
            {'name': 'D7'}, {'name': 'CE'}, {'name': 'A10'}, {'name': 'OE'},
            {'name': 'A11'}, {'name': 'A9'}, {'name': 'A8'}, {'name': 'A13'},
            {'name': 'VCC'}, {'name': 'A12'}, {'name': 'NC'}, {'name': 'VPP'}
        ]
    )
    
    # Lower RAM - 16K (0x4000-0x7FFF)
    for i in range(4):
        generator.add_component(
            name=f"RAM 4116 IC{14+i}",
            component_id=f"ic{14+i}_ram_lower",
            category="Memory", 
            description="16Kx1 Dynamic RAM - Lower 16K",
            package_type="DIP-16",
            position=(300 + i*30, 100),
            pins=[
                {'name': 'VBB'}, {'name': 'DIN'}, {'name': 'WRITE'}, {'name': 'RAS'},
                {'name': 'A0'}, {'name': 'A2'}, {'name': 'A1'}, {'name': 'VDD'},
                {'name': 'VCC'}, {'name': 'DOUT'}, {'name': 'CAS'}, {'name': 'A3'},
                {'name': 'A6'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'VSS'}
            ]
        )
    
    # Upper RAM - 32K (0x8000-0xFFFF) 
    for i in range(8):
        generator.add_component(
            name=f"RAM 4116 IC{18+i}",
            component_id=f"ic{18+i}_ram_upper",
            category="Memory",
            description="16Kx1 Dynamic RAM - Upper 32K", 
            package_type="DIP-16",
            position=(300 + i*30, 200),
            pins=[
                {'name': 'VBB'}, {'name': 'DIN'}, {'name': 'WRITE'}, {'name': 'RAS'},
                {'name': 'A0'}, {'name': 'A2'}, {'name': 'A1'}, {'name': 'VDD'},
                {'name': 'VCC'}, {'name': 'DOUT'}, {'name': 'CAS'}, {'name': 'A3'},
                {'name': 'A6'}, {'name': 'A4'}, {'name': 'A5'}, {'name': 'VSS'}
            ]
        )
    
    # === SUPPORT CHIPS ===
    
    # 74LS157 - Multiplexer for RAM addressing
    generator.add_component(
        name="74LS157",
        component_id="ic3_mux",
        category="Logic",
        description="Quad 2-to-1 multiplexer for RAM row/column addressing",
        package_type="DIP-16",
        position=(150, 250),
        pins=[
            {'name': 'SEL'}, {'name': '1A'}, {'name': '1B'}, {'name': '1Y'},
            {'name': '2A'}, {'name': '2B'}, {'name': '2Y'}, {'name': 'GND'},
            {'name': 'VCC'}, {'name': '3Y'}, {'name': '3B'}, {'name': '3A'},
            {'name': '4Y'}, {'name': '4B'}, {'name': '4A'}, {'name': 'G'}
        ]
    )
    
    # 74LS32 - OR gates
    generator.add_component(
        name="74LS32",
        component_id="ic30_or",
        category="Logic", 
        description="Quad 2-input OR gates",
        package_type="DIP-14",
        position=(250, 250),
        pins=[
            {'name': '1A'}, {'name': '1B'}, {'name': '1Y'}, {'name': '2A'},
            {'name': '2B'}, {'name': '2Y'}, {'name': 'GND'}, {'name': 'VCC'},
            {'name': '3Y'}, {'name': '3B'}, {'name': '3A'}, {'name': '4Y'},
            {'name': '4B'}, {'name': '4A'}
        ]
    )
    
    # === PASSIVE COMPONENTS ===
    
    # Main Crystal - 14MHz
    generator.add_component(
        name="Crystal 14MHz",
        component_id="xtal1",
        category="Timing",
        description="14.000MHz crystal oscillator",
        package_type="HC-49U",
        position=(80, 300),
        pins=[
            {'name': 'XTAL1'}, {'name': 'XTAL2'}
        ]
    )
    
    # Load capacitors for crystal
    generator.add_component(
        name="C34 22pF",
        component_id="c34",
        category="Passive",
        description="Crystal load capacitor",
        package_type="C0805",
        position=(60, 320),
        pins=[{'name': '1'}, {'name': '2'}]
    )
    
    generator.add_component(
        name="C35 22pF", 
        component_id="c35",
        category="Passive",
        description="Crystal load capacitor",
        package_type="C0805",
        position=(100, 320),
        pins=[{'name': '1'}, {'name': '2'}]
    )
    
    # Power supply filtering
    generator.add_component(
        name="C6 470µF",
        component_id="c6",
        category="Passive",
        description="Main power supply filter",
        package_type="Electrolytic",
        position=(20, 50),
        pins=[{'name': 'PLUS'}, {'name': 'MINUS'}]
    )
    
    # === CONNECTORS ===
    
    # Edge Connector
    generator.add_component(
        name="Edge Connector",
        component_id="conn1",
        category="Connector",
        description="28-way edge connector for expansion",
        package_type="Edge-28",
        position=(400, 150),
        pins=[
            {'name': '0V'}, {'name': '+5V'}, {'name': 'CLK'}, {'name': 'A15'},
            {'name': 'A14'}, {'name': 'A13'}, {'name': 'A12'}, {'name': 'A11'},
            {'name': 'A10'}, {'name': 'A9'}, {'name': 'A8'}, {'name': 'A7'},
            {'name': 'A6'}, {'name': 'A5'}, {'name': 'A4'}, {'name': 'A3'},
            {'name': 'A2'}, {'name': 'A1'}, {'name': 'A0'}, {'name': 'D0'},
            {'name': 'D1'}, {'name': 'D2'}, {'name': 'D3'}, {'name': 'D4'},
            {'name': 'D5'}, {'name': 'D6'}, {'name': 'D7'}, {'name': 'GND'}
        ]
    )
    
    # Keyboard Connector
    generator.add_component(
        name="Keyboard Connector",
        component_id="conn2", 
        category="Connector",
        description="8-way keyboard matrix connector",
        package_type="Molex-8",
        position=(50, 300),
        pins=[
            {'name': 'A8'}, {'name': 'A9'}, {'name': 'A10'}, {'name': 'A11'},
            {'name': 'A12'}, {'name': 'A13'}, {'name': 'A14'}, {'name': 'A15'}
        ]
    )
    
    # === SYSTEM CONFIGURATION ===
    
    system_config = {
        'memory_map': {
            '0x0000-0x3FFF': 'ROM (16K)',
            '0x4000-0x57FF': 'Screen RAM (6K)',
            '0x5800-0x5AFF': 'Attributes (768 bytes)', 
            '0x5B00-0x7FFF': 'User RAM (9K)',
            '0x8000-0xFFFF': 'User RAM (32K)'
        },
        'io_ports': {
            '0xFE': 'ULA (keyboard, border, speaker)',
            '0x7FFD': 'Memory banking (128K models only)',
            '0x1FFD': 'System control (128K models only)'
        },
        'interrupts': {
            'INT': 'Display interrupt every 20ms (50Hz)',
            'NMI': 'Non-maskable interrupt (edge connector)'
        },
        'display': {
            'resolution': '256x192 pixels',
            'colors': '8 colors (3-bit)',
            'attributes': '8x8 character cells',
            'border': 'Programmable color'
        }
    }
    
    # Register system with generator
    generator.register_system('zx_spectrum_48k', system_info, system_config)

if __name__ == "__main__":
    # Test function
    print("ZX Spectrum 48K complete system definition loaded")
    print("Components: Z80A CPU, ULA, ROM, 48K RAM, support logic, connectors")
    print("Ready for visual emulation and PCB layout")
