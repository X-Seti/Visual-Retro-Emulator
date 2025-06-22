            def _create_component(self, name, category, package, position):
                """Create a highly realistic visual component with authentic chip styling"""
                try:
                    from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsLineItem
                    from PyQt6.QtCore import QRectF

                    # Create component group
                    component_group = QGraphicsItemGroup()

                    # Get package information
                    package_info = self._get_package_info(package, name, category)
                    width = package_info['width']
                    height = package_info['height']
                    pin_count = package_info['pin_count']
                    pin_spacing = package_info['pin_spacing']
                    pin_width = package_info['pin_width']
                    pin_height = package_info['pin_height']

                    # Create main chip body with rounded corners and gradient effect
                    body_rect = QGraphicsRectItem(-width/2, -height/2, width, height)

                    # Enhanced realistic chip colors and styling
                    body_color, outline_color, text_color = self._get_chip_colors(name, category, package)

                    # Create gradient-like effect with subtle shading
                    body_rect.setBrush(QBrush(body_color))
                    body_rect.setPen(QPen(outline_color, 1.8))
                    component_group.addToGroup(body_rect)

                    # Add subtle inner border for depth
                    inner_border = QGraphicsRectItem(-width/2 + 1, -height/2 + 1, width - 2, height - 2)
                    inner_border.setBrush(QBrush(Qt.BrushStyle.NoBrush))
                    inner_border.setPen(QPen(body_color.lighter(120), 0.8))
                    component_group.addToGroup(inner_border)

                    # Add package-specific identification features
                    if package.startswith("DIP"):
                        self._add_dip_features(component_group, width, height, body_color)
                    elif package.startswith("QFP"):
                        self._add_qfp_features(component_group, width, height, body_color)
                    elif package.startswith("PLCC"):
                        self._add_plcc_features(component_group, width, height, body_color)
                    elif package == "TO-220":
                        self._add_to220_features(component_group, width, height, body_color)

                    # Create highly detailed pins
                    if package.startswith("DIP"):
                        self._create_enhanced_dip_pins(component_group, width, height, pin_count, pin_spacing, pin_width, pin_height)
                    elif package.startswith("QFP"):
                        self._create_enhanced_qfp_pins(component_group, width, height, pin_count, pin_width)
                    elif package.startswith("PLCC"):
                        self._create_enhanced_plcc_pins(component_group, width, height, pin_count, pin_width)
                    elif package == "TO-220":
                        self._create_enhanced_to220_pins(component_group, width, height, pin_width)

                    # Enhanced component labeling
                    self._add_enhanced_labels(component_group, name, package, width, height, text_color, category)

                    # Position the component group
                    component_group.setPos(position)

                    # Enhanced interactivity
                    component_group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
                    component_group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)
                    component_group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemSendsGeometryChanges, True)

                    # Add hover effects
                    component_group.setAcceptHoverEvents(True)

                    # Add to scene
                    self.scene().addItem(component_group)

                    # Enhanced component tracking
                    comp_id = f"{name}_{len(self.components)}"
                    self.components[comp_id] = {
                        'group': component_group,
                        'name': name,
                        'category': category,
                        'package': package,
                        'position': position,
                        'width': width,
                        'height': height,
                        'pin_count': pin_count,
                        'body_color': body_color,
                        'outline_color': outline_color
                    }

                    print(f"✅ Enhanced realistic component created: {name} ({package}) - {pin_count} pins")
                    return comp_id

                except Exception as e:
                    print(f"❌ Error creating enhanced component: {e}")
                    import traceback
                    traceback.print_exc()
                    return None

            def _get_package_info(self, package, name, category):
                """Get detailed package information with enhanced realism"""
                # Base measurements in real-world scale (adjusted for screen)
                info = {
                    'width': 60,
                    'height': 120,
                    'pin_count': 40,
                    'pin_spacing': 6,
                    'pin_width': 8,
                    'pin_height': 2.5
                }

                if package.startswith("DIP"):
                    # Extract pin count
                    try:
                        pin_count = int(package.split("-")[1])
                    except:
                        pin_count = 40

                    # Real DIP package dimensions (scaled for visibility)
                    if pin_count == 8:
                        info.update({'width': 32, 'height': 40, 'pin_count': 8, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 14:
                        info.update({'width': 32, 'height': 56, 'pin_count': 14, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 16:
                        info.update({'width': 32, 'height': 64, 'pin_count': 16, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 18:
                        info.update({'width': 32, 'height': 72, 'pin_count': 18, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 20:
                        info.update({'width': 32, 'height': 80, 'pin_count': 20, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 22:
                        info.update({'width': 32, 'height': 88, 'pin_count': 22, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 24:
                        info.update({'width': 32, 'height': 96, 'pin_count': 24, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 28:
                        info.update({'width': 32, 'height': 112, 'pin_count': 28, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 40:
                        info.update({'width': 32, 'height': 160, 'pin_count': 40, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 48:
                        info.update({'width': 32, 'height': 192, 'pin_count': 48, 'pin_spacing': 4, 'pin_width': 6, 'pin_height': 2})
                    elif pin_count == 64:
                        info.update({'width': 38, 'height': 256, 'pin_count': 64, 'pin_spacing': 4, 'pin_width': 7, 'pin_height': 2})

                elif package.startswith("QFP"):
                    try:
                        pin_count = int(package.split("-")[1])
                    except:
                        pin_count = 44

                    # QFP packages are square with finer pin pitch
                    side_length = max(48, pin_count * 1.3)
                    info.update({
                        'width': side_length,
                        'height': side_length,
                        'pin_count': pin_count,
                        'pin_spacing': 2,
                        'pin_width': 4,
                        'pin_height': 1.5
                    })

                elif package.startswith("PLCC"):
                    try:
                        pin_count = int(package.split("-")[1])
                    except:
                        pin_count = 68

                    # PLCC packages with J-lead pins
                    side_length = max(44, pin_count * 1.1)
                    info.update({
                        'width': side_length,
                        'height': side_length,
                        'pin_count': pin_count,
                        'pin_spacing': 2.5,
                        'pin_width': 3,
                        'pin_height': 2
                    })

                elif package == "TO-220":
                    info.update({
                        'width': 24,
                        'height': 40,
                        'pin_count': 3,
                        'pin_spacing': 10,
                        'pin_width': 3,
                        'pin_height': 12
                    })

                return info

            def _get_chip_colors(self, name, category, package):
                """Get authentic chip colors based on era and type"""
                # Default colors
                body_color = QColor(50, 50, 60)
                outline_color = QColor(175, 175, 175)
                text_color = QColor(255, 255, 255)

                # Historic chip colors by category and era
                if category == "CPUs":
                    if name in ["Z80", "Z80A", "Z80B"]:
                        body_color = QColor(35, 35, 45)  # Dark Zilog ceramic
                        outline_color = QColor(190, 190, 190)
                    elif name in ["6502", "6510", "65C02"]:
                        body_color = QColor(45, 35, 35)  # MOS Technology brownish
                        outline_color = QColor(180, 170, 170)
                    elif name in ["68000", "68020", "68030"]:
                        body_color = QColor(40, 40, 50)  # Motorola dark ceramic
                        outline_color = QColor(185, 185, 185)
                    elif name in ["8080", "8086", "8088"]:
                        body_color = QColor(45, 45, 55)  # Intel ceramic
                        outline_color = QColor(180, 180, 180)
                    else:
                        body_color = QColor(40, 40, 50)
                        outline_color = QColor(180, 180, 180)

                elif category == "Memory":
                    if "27" in name:  # EPROM
                        body_color = QColor(55, 45, 65)  # Purple-tinted ceramic
                        outline_color = QColor(170, 160, 180)
                    elif "62" in name:  # SRAM
                        body_color = QColor(50, 55, 50)  # Greenish tint
                        outline_color = QColor(160, 170, 160)
                    else:
                        body_color = QColor(55, 55, 65)
                        outline_color = QColor(170, 170, 170)

                elif category == "Graphics":
                    if "VIC" in name or "6567" in name or "6569" in name:
                        body_color = QColor(45, 35, 55)  # Commodore purple-brown
                        outline_color = QColor(175, 165, 185)
                    elif "TMS" in name:
                        body_color = QColor(40, 50, 40)  # TI greenish
                        outline_color = QColor(160, 180, 160)
                    elif name in ["Agnus", "Denise", "Paula"]:
                        body_color = QColor(35, 45, 35)  # Amiga custom green
                        outline_color = QColor(155, 185, 155)
                    else:
                        body_color = QColor(45, 45, 55)
                        outline_color = QColor(175, 175, 175)

                elif category == "Audio":
                    if "SID" in name or "6581" in name or "8580" in name:
                        body_color = QColor(45, 35, 55)  # Commodore SID
                        outline_color = QColor(175, 165, 185)
                    elif "AY" in name or "YM" in name:
                        body_color = QColor(40, 50, 50)  # Yamaha/GI teal
                        outline_color = QColor(160, 180, 180)
                    else:
                        body_color = QColor(50, 45, 55)
                        outline_color = QColor(170, 165, 175)

                elif category == "Logic":
                    # Classic 74-series black plastic
                    body_color = QColor(25, 25, 25)
                    outline_color = QColor(140, 140, 140)
                    text_color = QColor(220, 220, 220)

                elif category == "Power":
                    # Metal can packages
                    body_color = QColor(80, 80, 90)
                    outline_color = QColor(120, 120, 130)
                    text_color = QColor(255, 255, 255)

                elif category == "Analog":
                    # Classic op-amp colors
                    body_color = QColor(40, 40, 45)
                    outline_color = QColor(160, 160, 165)

                # Package-specific color adjustments
                if package == "TO-220":
                    body_color = QColor(60, 65, 70)  # Metal package
                    outline_color = QColor(100, 110, 120)
                elif package.startswith("QFP"):
                    body_color = body_color.darker(110)  # Slightly darker for surface mount

                return body_color, outline_color, text_color

            def _add_dip_features(self, group, width, height, body_color):
                """Add DIP package specific features"""
                # Classic DIP notch (semicircle cutout)
                notch_width = min(width * 0.4, 12)
                notch_height = 4

                # Create notch as a dark rectangle
                notch = QGraphicsRectItem(-notch_width/2, -height/2 - 1, notch_width, notch_height)
                notch.setBrush(QBrush(QColor(15, 15, 15)))
                notch.setPen(QPen(QColor(80, 80, 80), 0.8))
                group.addToGroup(notch)

                # Add subtle molding lines
                for i in range(3):
                    line_y = -height/2 + 8 + (i * height/4)
                    mold_line = QGraphicsLineItem(-width/2 + 2, line_y, width/2 - 2, line_y)
                    mold_line.setPen(QPen(body_color.darker(130), 0.3))
                    group.addToGroup(mold_line)

            def _add_qfp_features(self, group, width, height, body_color):
                """Add QFP package specific features"""
                # Pin 1 indicator dot
                dot_size = 3
                dot = QGraphicsEllipseItem(-width/2 + 6, -height/2 + 6, dot_size, dot_size)
                dot.setBrush(QBrush(QColor(255, 255, 255)))
                dot.setPen(QPen(QColor(200, 200, 200), 0.5))
                group.addToGroup(dot)

                # Corner chamfers (small cut corners)
                chamfer_size = 3
                for corner in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
                    x = corner[0] * (width/2 - chamfer_size/2)
                    y = corner[1] * (height/2 - chamfer_size/2)
                    chamfer = QGraphicsRectItem(x, y, chamfer_size, chamfer_size)
                    chamfer.setBrush(QBrush(body_color.darker(120)))
                    chamfer.setPen(QPen(Qt.PenStyle.NoPen))
                    group.addToGroup(chamfer)

            def _add_plcc_features(self, group, width, height, body_color):
                """Add PLCC package specific features"""
                # Pin 1 indicator beveled corner
                bevel_size = 6
                bevel = QGraphicsRectItem(-width/2, -height/2, bevel_size, bevel_size)
                bevel.setBrush(QBrush(body_color.darker(140)))
                bevel.setPen(QPen(body_color.darker(160), 1))
                group.addToGroup(bevel)

            def _add_to220_features(self, group, width, height, body_color):
                """Add TO-220 package specific features"""
                # Metal tab with mounting hole
                tab_width = width - 4
                tab_height = 8
                tab = QGraphicsRectItem(-tab_width/2, -height/2 - tab_height, tab_width, tab_height)
                tab.setBrush(QBrush(QColor(100, 110, 120)))
                tab.setPen(QPen(QColor(80, 90, 100), 1))
                group.addToGroup(tab)

                # Mounting hole
                hole = QGraphicsEllipseItem(-2, -height/2 - tab_height/2 - 2, 4, 4)
                hole.setBrush(QBrush(QColor(20, 20, 20)))
                hole.setPen(QPen(QColor(60, 60, 60), 0.5))
                group.addToGroup(hole)

            def _create_enhanced_dip_pins(self, group, width, height, pin_count, spacing, pin_width, pin_height):
                """Create enhanced DIP pins with realistic appearance"""
                pins_per_side = pin_count // 2
                start_y = -height/2 + (height - (pins_per_side - 1) * spacing) / 2

                # Left side pins (1 to N/2)
                for i in range(pins_per_side):
                    y_pos = start_y + (i * spacing)

                    # Main pin body
                    pin = QGraphicsRectItem(-width/2 - pin_width, y_pos - pin_height/2, pin_width, pin_height)
                    pin.setBrush(QBrush(QColor(220, 220, 230)))  # Bright silver
                    pin.setPen(QPen(QColor(180, 180, 190), 0.8))
                    group.addToGroup(pin)

                    # Pin highlight (metallic effect)
                    highlight = QGraphicsRectItem(-width/2 - pin_width + 0.5, y_pos - pin_height/2 + 0.3,
                                                pin_width - 1, pin_height/3)
                    highlight.setBrush(QBrush(QColor(245, 245, 255)))
                    highlight.setPen(QPen(Qt.PenStyle.NoPen))
                    group.addToGroup(highlight)

                    # Pin number (small, readable)
                    if pin_count <= 28 or i % 2 == 0:  # Show all numbers for small chips, every other for large
                        pin_num = QGraphicsTextItem(str(i + 1))
                        pin_num.setDefaultTextColor(QColor(255, 255, 255))
                        pin_num.setFont(QFont("Arial", max(5, min(7, spacing - 1)), QFont.Weight.Bold))
                        pin_rect = pin_num.boundingRect()
                        pin_num.setPos(-width/2 + 2, y_pos - pin_rect.height()/2)
                        group.addToGroup(pin_num)

                # Right side pins (N/2+1 to N)
                for i in range(pins_per_side):
                    y_pos = start_y + ((pins_per_side - 1 - i) * spacing)

                    # Main pin body
                    pin = QGraphicsRectItem(width/2, y_pos - pin_height/2, pin_width, pin_height)
                    pin.setBrush(QBrush(QColor(220, 220, 230)))
                    pin.setPen(QPen(QColor(180, 180, 190), 0.8))
                    group.addToGroup(pin)

                    # Pin highlight
                    highlight = QGraphicsRectItem(width/2 + 0.5, y_pos - pin_height/2 + 0.3,
                                                pin_width - 1, pin_height/3)
                    highlight.setBrush(QBrush(QColor(245, 245, 255)))
                    highlight.setPen(QPen(Qt.PenStyle.NoPen))
                    group.addToGroup(highlight)

                    # Pin number
                    if pin_count <= 28 or i % 2 == 0:
                        pin_num = QGraphicsTextItem(str(pins_per_side + i + 1))
                        pin_num.setDefaultTextColor(QColor(255, 255, 255))
                        pin_num.setFont(QFont("Arial", max(5, min(7, spacing - 1)), QFont.Weight.Bold))
                        pin_rect = pin_num.boundingRect()
                        pin_num.setPos(width/2 - pin_rect.width() - 2, y_pos - pin_rect.height()/2)
                        group.addToGroup(pin_num)

            def _create_enhanced_qfp_pins(self, group, width, height, pin_count, pin_width):
                """Create enhanced QFP pins with gull-wing leads"""
                pins_per_side = pin_count // 4

                for side in range(4):
                    for i in range(pins_per_side):
                        # Calculate pin position based on side
                        if side == 0:  # Top
                            x_pos = -width/2 + (width / (pins_per_side + 1)) * (i + 1)
                            y_pos = -height/2 - pin_width
                            pin_rect = QRectF(x_pos - pin_width/2, y_pos, pin_width, pin_width)
                        elif side == 1:  # Right
                            x_pos = width/2
                            y_pos = -height/2 + (height / (pins_per_side + 1)) * (i + 1)
                            pin_rect = QRectF(x_pos, y_pos - pin_width/2, pin_width, pin_width)
                        elif side == 2:  # Bottom
                            x_pos = width/2 - (width / (pins_per_side + 1)) * (i + 1)
                            y_pos = height/2
                            pin_rect = QRectF(x_pos - pin_width/2, y_pos, pin_width, pin_width)
                        else:  # Left
                            x_pos = -width/2 - pin_width
                            y_pos = height/2 - (height / (pins_per_side + 1)) * (i + 1)
                            pin_rect = QRectF(x_pos, y_pos - pin_width/2, pin_width, pin_width)

                        # Create pin with metallic appearance
                        pin = QGraphicsRectItem(pin_rect)
                        pin.setBrush(QBrush(QColor(210, 210, 220)))
                        pin.setPen(QPen(QColor(170, 170, 180), 0.6))
                        group.addToGroup(pin)

            def _create_enhanced_plcc_pins(self, group, width, height, pin_count, pin_width):
                """Create enhanced PLCC pins with J-leads"""
                pins_per_side = pin_count // 4

                for side in range(4):
                    for i in range(pins_per_side):
                        # Similar to QFP but with J-lead styling
                        if side == 0:  # Top
                            x_pos = -width/2 + (width / (pins_per_side + 1)) * (i + 1)
                            y_pos = -height/2
                            # J-lead extends inward
                            pin_rect = QRectF(x_pos - pin_width/2, y_pos - pin_width/2, pin_width, pin_width * 1.5)
                        elif side == 1:  # Right
                            x_pos = width/2
                            y_pos = -height/2 + (height / (pins_per_side + 1)) * (i + 1)
                            pin_rect = QRectF(x_pos - pin_width/2, y_pos - pin_width/2, pin_width * 1.5, pin_width)
                        elif side == 2:  # Bottom
                            x_pos = width/2 - (width / (pins_per_side + 1)) * (i + 1)
                            y_pos = height/2
                            pin_rect = QRectF(x_pos - pin_width/2, y_pos - pin_width/2, pin_width, pin_width * 1.5)
                        else:  # Left
                            x_pos = -width/2
                            y_pos = height/2 - (height / (pins_per_side + 1)) * (i + 1)
                            pin_rect = QRectF(x_pos - pin_width/2, y_pos - pin_width/2, pin_width * 1.5, pin_width)

                        pin = QGraphicsRectItem(pin_rect)
                        pin.setBrush(QBrush(QColor(200, 200, 210)))
                        pin.setPen(QPen(QColor(160, 160, 170), 0.8))
                        group.addToGroup(pin)

            def _create_enhanced_to220_pins(self, group, width, height, pin_width):
                """Create enhanced TO-220 pins"""
                pin_positions = [-8, 0, 8]  # Three pins spread out

                for i, x_pos in enumerate(pin_positions):
                    # Thick rectangular pins
                    pin = QGraphicsRectItem(x_pos - pin_width/2, height/2, pin_width, 12)
                    pin.setBrush(QBrush(QColor(210, 210, 220)))
                    pin.setPen(QPen(QColor(170, 170, 180), 1))
                    group.addToGroup(pin)

                    # Pin labels (E, C, B for transistors or similar)
                    labels = ["1", "2", "3"]
                    pin_label = QGraphicsTextItem(labels[i])
                    pin_label.setDefaultTextColor(QColor(255, 255, 255))
                    pin_label.setFont(QFont("Arial", 6, QFont.Weight.Bold))
                    pin_rect = pin_label.boundingRect()
                    pin_label.setPos(x_pos - pin_rect.width()/2, height/2 + 13)
                    group.addToGroup(pin_label)

            def _add_enhanced_labels(self, group, name, package, width, height, text_color, category):
                """Add enhanced component labels with better typography"""
                # Main component name with smart formatting
                display_name = name
                if len(name) > 10 and category != "Logic":  # Don't split 74LS numbers
                    # Smart text wrapping for long names
                    if "-" in name:
                        parts = name.split("-", 1)
                        display_name = parts[0] + "\n" + parts[1]
                    elif len(name) > 15:
                        mid = len(name) // 2
                        space_near_mid = name.find(" ", mid-3, mid+3)
                        if space_near_mid != -1:
                            display_name = name[:space_near_mid] + "\n" + name[space_near_mid+1:]

                # Main label
                text_item = QGraphicsTextItem(display_name)
                text_item.setDefaultTextColor(text_color)

                # Enhanced font sizing
                base_font_size = max(6, min(12, int(min(width, height) / 8)))
                if category == "Logic":
                    base_font_size = max(7, base_font_size)  # Logic chips need readable text

                font = QFont("Arial", base_font_size, QFont.Weight.Bold)
                text_item.setFont(font)

                # Center the text perfectly
                text_rect = text_item.boundingRect()
                text_item.setPos(-text_rect.width()/2, -text_rect.height()/2)
                group.addToGroup(text_item)

                # Package label (smaller, positioned appropriately)
                if package not in ["DIP-40", "DIP-16", "DIP-14"]:  # Don't show common packages
                    package_text = QGraphicsTextItem(package)
                    package_text.setDefaultTextColor(text_color.darker(130))
                    package_font = QFont("Arial", max(4, base_font_size - 3))
                    package_text.setFont(package_font)

                    pkg_rect = package_text.boundingRect()
                    # Position at bottom, but check if there's room
                    y_offset = height/2 - pkg_rect.height() - 2
                    if y_offset > text_rect.height()/2 + 2:  # Only show if there's room
                        package_text.setPos(-pkg_rect.width()/2, y_offset)
                        group.addToGroup(package_text)

                # Add manufacturer or series info for some chips
                if category == "CPUs" and name in ["Z80", "6502", "68000"]:
                    # Add subtle manufacturer marking
                    mfg_text = ""
                    if "Z80" in name:
                        mfg_text = "ZILOG"
                    elif "6502" in name or "6510" in name:
                        mfg_text = "MOS"
                    elif "68000" in name:
                        mfg_text = "MOTOROLA"

                    if mfg_text and height > 80:  # Only for larger chips
                        mfg_label = QGraphicsTextItem(mfg_text)
                        mfg_label.setDefaultTextColor(text_color.darker(160))
                        mfg_font = QFont("Arial", max(4, base_font_size - 4))
                        mfg_label.setFont(mfg_font)

                        mfg_rect = mfg_label.boundingRect()
                        mfg_label.setPos(-mfg_rect.width()/2, text_rect.height()/2 + 2)
                        group.addToGroup(mfg_label)
