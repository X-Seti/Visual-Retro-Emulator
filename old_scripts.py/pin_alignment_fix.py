#!/usr/bin/env python3
"""
Pin Alignment Fix - Ensures even pin spacing
Fixes the uneven pin grouping issue
"""

def calculate_even_pin_positions(package_type, chip_width, chip_height, pin_count):
    """Calculate evenly spaced pin positions"""
    pins = []
    grid_spacing = 10  # Match perfboard spacing
    
    if package_type.startswith('DIP'):
        pins_per_side = pin_count // 2
        
        # Calculate spacing to distribute pins evenly
        usable_height = chip_height - 40  # Leave margins
        if pins_per_side > 1:
            pin_spacing = usable_height / (pins_per_side - 1)
        else:
            pin_spacing = 0
        
        # Snap spacing to grid
        pin_spacing = round(pin_spacing / grid_spacing) * grid_spacing
        if pin_spacing < grid_spacing:
            pin_spacing = grid_spacing
        
        # Calculate start position to center pins
        total_span = (pins_per_side - 1) * pin_spacing
        start_y = (chip_height - total_span) / 2
        
        # Snap start position to grid
        start_y = round(start_y / grid_spacing) * grid_spacing
        
        # Left side pins (1 to pins_per_side)
        for i in range(pins_per_side):
            y_pos = start_y + i * pin_spacing
            pins.append({
                'number': i + 1,
                'name': f'Pin{i + 1}',
                'type': 'unused',
                'x': 0,
                'y': y_pos,
                'side': 'left'
            })
        
        # Right side pins (pins_per_side+1 to pin_count)
        for i in range(pins_per_side):
            y_pos = start_y + i * pin_spacing
            pins.append({
                'number': pin_count - i,  # Reverse numbering
                'name': f'Pin{pin_count - i}',
                'type': 'unused',
                'x': chip_width,
                'y': y_pos,
                'side': 'right'
            })
    
    elif package_type.startswith('QFP'):
        pins_per_side = pin_count // 4
        
        # Calculate even spacing for each side
        usable_width = chip_width - 20
        usable_height = chip_height - 20
        
        if pins_per_side > 1:
            spacing_x = usable_width / (pins_per_side - 1)
            spacing_y = usable_height / (pins_per_side - 1)
        else:
            spacing_x = spacing_y = 0
        
        # Snap to grid
        spacing_x = round(spacing_x / grid_spacing) * grid_spacing
        spacing_y = round(spacing_y / grid_spacing) * grid_spacing
        
        pin_num = 1
        
        # Top side (left to right)
        start_x = 10
        for i in range(pins_per_side):
            x_pos = start_x + i * spacing_x
            pins.append({
                'number': pin_num,
                'name': f'Pin{pin_num}',
                'type': 'unused',
                'x': x_pos,
                'y': 0,
                'side': 'top'
            })
            pin_num += 1
        
        # Right side (top to bottom)
        start_y = 10
        for i in range(pins_per_side):
            y_pos = start_y + i * spacing_y
            pins.append({
                'number': pin_num,
                'name': f'Pin{pin_num}',
                'type': 'unused',
                'x': chip_width,
                'y': y_pos,
                'side': 'right'
            })
            pin_num += 1
        
        # Bottom side (right to left)
        for i in range(pins_per_side):
            x_pos = chip_width - 10 - i * spacing_x
            pins.append({
                'number': pin_num,
                'name': f'Pin{pin_num}',
                'type': 'unused',
                'x': x_pos,
                'y': chip_height,
                'side': 'bottom'
            })
            pin_num += 1
        
        # Left side (bottom to top)
        for i in range(pins_per_side):
            y_pos = chip_height - 10 - i * spacing_y
            pins.append({
                'number': pin_num,
                'name': f'Pin{pin_num}',
                'type': 'unused',
                'x': 0,
                'y': y_pos,
                'side': 'left'
            })
            pin_num += 1
    
    return pins
