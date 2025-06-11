"""
X-Seti - June11 2025 - Component Palette with Drag/Drop Support
Computer type and chip pinout support
"""

import os
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, 
                           QLineEdit, QLabel, QSplitter, QTextEdit, QGroupBox,
                           QHBoxLayout, QPushButton, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData
from PyQt6.QtGui import QDrag, QPainter, QPixmap, QIcon

class ComponentTreeItem(QTreeWidgetItem):
    """Custom tree item that stores component data"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.component_data = {}
        self.component_type = ""
        self.is_component = False
        
    def set_component_data(self, data: Dict):
        """Set component data for this item"""
        self.component_data = data
        self.component_type = data.get('type', 'unknown')
        self.is_component = True

class EnhancedComponentPalette(QWidget):
    """Enhanced component palette with drag/drop and organized structure"""
    
    # Signals
    componentSelected = pyqtSignal(dict)  # component_data
    componentDoubleClicked = pyqtSignal(dict)  # component_data
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(280)
        
        # Component organization structure
        self.computer_systems = {
            "Commodore": {
                "icon": "🖥️",
                "systems": {
                    "C64": ["6502 CPU", "6581 SID", "6567 VIC-II", "6526 CIA"],
                    "C128": ["8502 CPU", "Z80 CPU", "8563 VDC", "6581 SID"],
                    "Amiga": ["68000 CPU", "68020 CPU", "Paula", "Denise", "Agnus"],
                    "PET": ["6502 CPU", "6520 PIA", "6522 VIA"]
                }
            },
            "Atari": {
                "icon": "🕹️", 
                "systems": {
                    "2600": ["6507 CPU", "TIA", "6532 RIOT"],
                    "800/XL": ["6502 CPU", "ANTIC", "GTIA", "POKEY"],
                    "ST": ["68000 CPU", "YM2149", "Shifter"]
                }
            },
            "Apple": {
                "icon": "🍎",
                "systems": {
                    "II": ["6502 CPU", "6502A CPU"],
                    "IIe": ["65C02 CPU"],
                    "Mac": ["68000 CPU", "68020 CPU"]
                }
            },
            "Generic": {
                "icon": "🔧",
                "systems": {
                    "TEST": ["TEST COMPONENT", "BRIGHT RED CHIP", "YELLOW BORDER CHIP"],
                    "CPU": ["Z80 CPU", "6502 CPU", "68000 CPU", "8080 CPU"],
                    "Memory": ["RAM 6464", "ROM 2764", "EPROM 2732"],
                    "I/O": ["6520 PIA", "6522 VIA", "8255 PPI"],
                    "Logic": ["74LS00", "74LS04", "74LS08", "74LS32"]
                }
            }
        }
        
        # Initialize UI
        self._create_ui()
        self._populate_tree()
        
        print("✓ Enhanced Component Palette initialized")
    
    def _create_ui(self):
        """Create the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title_label = QLabel("Component Palette")
        title_label.setStyleSheet("font-weight: bold; font-size: 12px; padding: 5px;")
        layout.addWidget(title_label)
        
        # Search box
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search Components...")
        self.search_edit.textChanged.connect(self._filter_components)
        search_layout.addWidget(self.search_edit)
        
        # Filter combo
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "CPU", "Memory", "I/O", "Logic", "Sound", "Video"])
        self.filter_combo.currentTextChanged.connect(self._filter_by_type)
        search_layout.addWidget(self.filter_combo)
        
        layout.addLayout(search_layout)
        
        # Create splitter for tree and details
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)
        
        # Component tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Components")
        self.tree.setDragEnabled(True)
        self.tree.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # Enable custom drag handling
        self.tree.startDrag = self._start_drag
        
        splitter.addWidget(self.tree)
        
        # Component details section
        details_widget = self._create_details_section()
        splitter.addWidget(details_widget)
        
        # Set splitter proportions
        splitter.setSizes([400, 200])
        
        # Add component button
        add_button = QPushButton("+ Add Custom Component")
        add_button.clicked.connect(self._add_custom_component)
        layout.addWidget(add_button)
    
    def _create_details_section(self):
        """Create component details section"""
        details_group = QGroupBox("Component Details")
        layout = QVBoxLayout(details_group)
        
        # Component info labels
        self.name_label = QLabel("Name: Select a component")
        self.type_label = QLabel("Type: -")
        self.pins_label = QLabel("Pins: -")
        self.package_label = QLabel("Package: -")
        
        layout.addWidget(self.name_label)
        layout.addWidget(self.type_label) 
        layout.addWidget(self.pins_label)
        layout.addWidget(self.package_label)
        
        # Description text
        self.description_text = QTextEdit()
        self.description_text.setMaximumHeight(80)
        self.description_text.setPlaceholderText("Component description will appear here...")
        layout.addWidget(self.description_text)
        
        return details_group
    
    def _populate_tree(self):
        """Populate the component tree with organized structure"""
        self.tree.clear()
        
        for brand, brand_data in self.computer_systems.items():
            # Create brand-level item
            brand_item = ComponentTreeItem()
            brand_item.setText(0, f"{brand_data['icon']} {brand}")
            brand_item.setExpanded(True)
            self.tree.addTopLevelItem(brand_item)
            
            # Add systems under each brand
            for system, components in brand_data["systems"].items():
                system_item = ComponentTreeItem(brand_item)
                system_item.setText(0, f"📦 {system}")
                system_item.setExpanded(True)
                
                # Add components under each system
                for component_name in components:
                    comp_item = ComponentTreeItem(system_item)
                    comp_item.setText(0, f"🔧 {component_name}")
                    
                    # Set component data
                    component_data = self._get_component_data(component_name, brand, system)
                    comp_item.set_component_data(component_data)
                    
                    # Set icon based on component type
                    icon = self._get_component_icon(component_data.get('category', 'unknown'))
                    comp_item.setText(0, f"{icon} {component_name}")
        
        print("✓ Component tree populated with organized structure")
    
    def _get_component_data(self, name: str, brand: str, system: str) -> Dict:
        """Get component data including pinout information"""
        # Extract component type and details
        component_type = "unknown"
        pin_count = 40
        package = "DIP"
        category = "unknown"
        
        name_lower = name.lower()
        
        # Determine component type and properties
        if "cpu" in name_lower or any(x in name_lower for x in ["6502", "68000", "z80", "8080"]):
            category = "cpu"
            component_type = "processor"
            pin_count = 40 if "6502" in name_lower else 64 if "68000" in name_lower else 40
        elif "sid" in name_lower or "pokey" in name_lower or "ym" in name_lower:
            category = "sound"
            component_type = "sound_chip"
            pin_count = 28
        elif "vic" in name_lower or "antic" in name_lower or "gtia" in name_lower:
            category = "video"
            component_type = "video_chip" 
            pin_count = 40
        elif "cia" in name_lower or "pia" in name_lower or "via" in name_lower:
            category = "io"
            component_type = "io_chip"
            pin_count = 40
        elif "ram" in name_lower or "rom" in name_lower or "eprom" in name_lower:
            category = "memory"
            component_type = "memory_chip"
            pin_count = 28
        elif "74ls" in name_lower:
            category = "logic"
            component_type = "logic_gate"
            pin_count = 14
        
        # Look for pinout image
        image_path = self._find_component_image(name, brand, system)
        
        return {
            'name': name,
            'type': component_type,
            'category': category,
            'brand': brand,
            'system': system,
            'pin_count': pin_count,
            'package': package,
            'image_path': image_path,
            'description': f"{name} - {category.title()} component for {brand} {system}",
            'pinout_data': self._get_pinout_data(name)
        }
    
    def _find_component_image(self, name: str, brand: str, system: str) -> Optional[str]:
        """Find component image in images/ directory"""
        # Clean name for filename matching
        clean_name = name.lower().replace(" ", "_").replace("-", "_")
        
        # Try various image path combinations
        image_patterns = [
            f"images/{clean_name}.png",
            f"images/components/{clean_name}.png", 
            f"images/{brand.lower()}/{clean_name}.png",
            f"images/{brand.lower()}/{system.lower()}/{clean_name}.png",
            f"images/chips/{clean_name}.png"
        ]
        
        for pattern in image_patterns:
            if os.path.exists(pattern):
                return pattern
        
        return None
    
    def _get_pinout_data(self, component_name: str) -> Dict:
        """Get pinout data for component with color coding"""
        # This would ideally load from a database, but for now return structured data
        pinouts = {
            "6502 CPU": {
                "pins": {
                    1: {"name": "VSS", "type": "power", "color": "#000000"},
                    2: {"name": "RDY", "type": "control", "color": "#FF6600"},
                    3: {"name": "φ1", "type": "clock", "color": "#0066FF"},
                    4: {"name": "IRQ", "type": "interrupt", "color": "#FF0066"},
                    5: {"name": "NC", "type": "unused", "color": "#CCCCCC"},
                    6: {"name": "NMI", "type": "interrupt", "color": "#FF0066"},
                    7: {"name": "SYNC", "type": "control", "color": "#FF6600"},
                    8: {"name": "VCC", "type": "power", "color": "#FF0000"},
                    # ... more pins would be defined here
                }
            },
            "68000 CPU": {
                "pins": {
                    1: {"name": "D4", "type": "data", "color": "#00FF00"},
                    2: {"name": "D3", "type": "data", "color": "#00FF00"},
                    3: {"name": "D2", "type": "data", "color": "#00FF00"},
                    # ... more pins
                }
            }
        }
        
        return pinouts.get(component_name, {})
    
    def _get_component_icon(self, category: str) -> str:
        """Get icon for component category"""
        icons = {
            "cpu": "🧠",
            "memory": "💾", 
            "io": "🔌",
            "sound": "🔊",
            "video": "📺",
            "logic": "⚡",
            "unknown": "🔧"
        }
        return icons.get(category, "🔧")
    
    def _start_drag(self, supportedActions):
        """Custom drag start implementation"""
        current_item = self.tree.currentItem()
        if not current_item or not isinstance(current_item, ComponentTreeItem):
            return
        
        if not current_item.is_component:
            return  # Only allow dragging actual components
        
        # Create drag object
        drag = QDrag(self.tree)
        mime_data = QMimeData()
        
        # Set component data as JSON
        import json
        component_json = json.dumps(current_item.component_data)
        mime_data.setText(component_json)
        mime_data.setData("application/x-component", component_json.encode())
        
        drag.setMimeData(mime_data)
        
        # Create drag pixmap
        pixmap = self._create_drag_pixmap(current_item.component_data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(pixmap.rect().center())
        
        # Execute drag
        drag.exec(Qt.DropAction.CopyAction)
        
        print(f"✓ Started drag for component: {current_item.component_data.get('name')}")
    
    def _create_drag_pixmap(self, component_data: Dict) -> QPixmap:
        """Create pixmap for drag operation"""
        # Try to load component image first
        image_path = component_data.get('image_path')
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale to reasonable drag size
                return pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, 
                                   Qt.TransformationMode.SmoothTransformation)
        
        # Create text-based pixmap as fallback
        pixmap = QPixmap(80, 40)
        pixmap.fill(Qt.GlobalColor.lightGray)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, 
                        component_data.get('name', 'Component'))
        painter.end()
        
        return pixmap
    
    def _filter_components(self, text: str):
        """Filter components based on search text"""
        def hide_show_item(item: QTreeWidgetItem, show_parent: bool = False):
            if isinstance(item, ComponentTreeItem) and item.is_component:
                # Component item - check if it matches
                matches = text.lower() in item.text(0).lower()
                item.setHidden(not matches and not show_parent)
                return matches
            else:
                # Category item - check children
                has_visible_children = False
                for i in range(item.childCount()):
                    child_matches = hide_show_item(item.child(i), show_parent)
                    has_visible_children = has_visible_children or child_matches
                
                item.setHidden(not has_visible_children and not show_parent)
                return has_visible_children
        
        # If no search text, show all
        if not text.strip():
            for i in range(self.tree.topLevelItemCount()):
                hide_show_item(self.tree.topLevelItem(i), True)
        else:
            for i in range(self.tree.topLevelItemCount()):
                hide_show_item(self.tree.topLevelItem(i))
    
    def _filter_by_type(self, type_filter: str):
        """Filter components by type"""
        def filter_item(item: QTreeWidgetItem):
            if isinstance(item, ComponentTreeItem) and item.is_component:
                if type_filter == "All":
                    item.setHidden(False)
                else:
                    category = item.component_data.get('category', '').lower()
                    matches = type_filter.lower() in category
                    item.setHidden(not matches)
                    return matches
            else:
                # Category item
                has_visible = False
                for i in range(item.childCount()):
                    child_visible = filter_item(item.child(i))
                    has_visible = has_visible or child_visible
                
                if type_filter == "All":
                    item.setHidden(False)
                else:
                    item.setHidden(not has_visible)
                return has_visible
        
        for i in range(self.tree.topLevelItemCount()):
            filter_item(self.tree.topLevelItem(i))
    
    def _on_selection_changed(self):
        """Handle selection change"""
        current_item = self.tree.currentItem()
        if isinstance(current_item, ComponentTreeItem) and current_item.is_component:
            self._update_details(current_item.component_data)
            self.componentSelected.emit(current_item.component_data)
        else:
            self._clear_details()
    
    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item double click"""
        if isinstance(item, ComponentTreeItem) and item.is_component:
            self.componentDoubleClicked.emit(item.component_data)
    
    def _update_details(self, component_data: Dict):
        """Update component details display"""
        self.name_label.setText(f"Name: {component_data.get('name', 'Unknown')}")
        self.type_label.setText(f"Type: {component_data.get('category', 'Unknown').title()}")
        self.pins_label.setText(f"Pins: {component_data.get('pin_count', 'Unknown')}")
        self.package_label.setText(f"Package: {component_data.get('package', 'Unknown')}")
        self.description_text.setText(component_data.get('description', 'No description available.'))
    
    def _clear_details(self):
        """Clear component details display"""
        self.name_label.setText("Name: Select a component")
        self.type_label.setText("Type: -")
        self.pins_label.setText("Pins: -") 
        self.package_label.setText("Package: -")
        self.description_text.clear()
    
    def _add_custom_component(self):
        """Add custom component (placeholder)"""
        print("Add custom component dialog would open here")
        # This would open a dialog to add custom components
    
    def get_all_components(self) -> List[Dict]:
        """Get list of all components"""
        components = []
        
        def collect_components(item: QTreeWidgetItem):
            if isinstance(item, ComponentTreeItem) and item.is_component:
                components.append(item.component_data)
            
            for i in range(item.childCount()):
                collect_components(item.child(i))
        
        for i in range(self.tree.topLevelItemCount()):
            collect_components(self.tree.topLevelItem(i))
        
        return components
    
    def refresh_components(self):
        """Refresh component list"""
        self._populate_tree()
        print("✓ Component palette refreshed")

# Backward compatibility
ComponentPalette = EnhancedComponentPalette
