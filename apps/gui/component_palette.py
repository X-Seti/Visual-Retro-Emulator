#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Component Palette
Updated to use better chipsets from chipsets/ folder with realistic images
"""

#this belongs in ui/component_palette.py

import sys
import os
from typing import Dict, List, Any, Optional
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, 
                           QTreeWidgetItem, QComboBox, QLineEdit, QPushButton,
                           QCheckBox, QLabel, QSplitter, QTabWidget, QScrollArea,
                           QGroupBox, QButtonGroup, QRadioButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor

# Import the integration system
sys.path.append('..')
try:
    from chipset_integration import IntegratedChipsetManager, ChipsetComponentFactory
    CHIPSETS_AVAILABLE = True
except ImportError:
    print("⚠️ Chipset integration not available - using fallback")
    CHIPSETS_AVAILABLE = False

class ComponentPalette(QWidget):
    """
    Component palette using better chipsets with realistic images
    Replaces old rectangular components with proper chip images
    """
    
    # Signals
    component_selected = pyqtSignal(str, dict)  # component_id, component_data
    component_double_clicked = pyqtSignal(str, dict)  # for adding to canvas
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        if CHIPSETS_AVAILABLE:
            # Initialize the chipset integration
            self.chipset_manager = IntegratedChipsetManager()
            self.component_factory = ChipsetComponentFactory(self.chipset_manager)
            
            # Get enhanced component data
            self.palette_data = self.chipset_manager.create_enhanced_component_palette_data()
            
            print(f"🎨 Component Palette initialized with chipsets")
            print(f"📦 Loaded {self.palette_data['total_chips']} chips from {self.palette_data['total_systems']} systems")
        else:
            # Fallback mode
            self.chipset_manager = None
            self.component_factory = None
            self.palette_data = self._create_fallback_data()
            print("🎨 Component Palette initialized in fallback mode")
        
        # UI state
        self.current_view = "category"  # "category" or "system"
        self.search_text = ""
        self.selected_category = "All"
        
        # Setup UI
        self._setup_ui()
        self._populate_components()
        
        # Track current selection
        self.current_component = None
    
    def _create_fallback_data(self):
        """Create fallback data when chipsets are not available"""
        return {
            "by_category": {
                "CPU": [{"name": "Generic CPU", "chip_id": "generic_cpu", "category": "CPU", 
                        "description": "Generic CPU chip", "package_types": ["DIP-40"], "pins": []}],
                "Custom": []
            },
            "by_system": {},
            "total_chips": 1,
            "total_systems": 0,
            "image_mappings": {}
        }
    
    def _setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Title and stats
        self._create_header(layout)
        
        # View controls (only if chipsets available)
        if CHIPSETS_AVAILABLE:
            self._create_view_controls(layout)
        
        # Search and filter
        self._create_search_filter(layout)
        
        # Main content area
        self._create_main_content(layout)
        
        # Component info panel
        self._create_info_panel(layout)
    
    def _create_header(self, layout):
        """Create header with title and stats"""
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Component Library")
        title_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #2c3e50;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        stats_label = QLabel(f"{self.palette_data['total_chips']} chips • {self.palette_data['total_systems']} systems")
        stats_label.setStyleSheet("font-size: 9px; color: #7f8c8d;")
        header_layout.addWidget(stats_label)
        
        layout.addLayout(header_layout)
    
    def _create_view_controls(self, layout):
        """Create view mode controls"""
        view_group = QGroupBox("View Mode")
        view_layout = QHBoxLayout(view_group)
        
        self.view_button_group = QButtonGroup()
        
        # Category view
        self.category_radio = QRadioButton("By Category")
        self.category_radio.setChecked(True)
        self.category_radio.toggled.connect(lambda checked: self._set_view_mode("category") if checked else None)
        self.view_button_group.addButton(self.category_radio)
        view_layout.addWidget(self.category_radio)
        
        # System view
        self.system_radio = QRadioButton("By System")
        self.system_radio.toggled.connect(lambda checked: self._set_view_mode("system") if checked else None)
        self.view_button_group.addButton(self.system_radio)
        view_layout.addWidget(self.system_radio)
        
        layout.addWidget(view_group)
    
    def _create_search_filter(self, layout):
        """Create search and filter controls"""
        search_layout = QHBoxLayout()
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search chips...")
        self.search_box.textChanged.connect(self._on_search_changed)
        search_layout.addWidget(self.search_box)
        
        # Category filter
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.addItems(list(self.palette_data['by_category'].keys()))
        self.category_filter.currentTextChanged.connect(self._on_category_filter_changed)
        search_layout.addWidget(self.category_filter)
        
        layout.addLayout(search_layout)
    
    def _create_main_content(self, layout):
        """Create main content area with component tree"""
        # Create component tree
        self.component_tree = QTreeWidget()
        self.component_tree.setHeaderLabels(["Component", "Package", "Description"])
        self.component_tree.setRootIsDecorated(True)
        self.component_tree.setAlternatingRowColors(True)
        self.component_tree.itemClicked.connect(self._on_item_clicked)
        self.component_tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # Set column widths
        self.component_tree.setColumnWidth(0, 150)
        self.component_tree.setColumnWidth(1, 80)
        self.component_tree.setColumnWidth(2, 200)
        
        layout.addWidget(self.component_tree)
    
    def _create_info_panel(self, layout):
        """Create component info panel"""
        self.info_panel = QGroupBox("Component Info")
        info_layout = QVBoxLayout(self.info_panel)
        
        # Component name and category
        self.info_name_label = QLabel("No component selected")
        self.info_name_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        info_layout.addWidget(self.info_name_label)
        
        self.info_category_label = QLabel("")
        self.info_category_label.setStyleSheet("color: #7f8c8d; font-size: 9px;")
        info_layout.addWidget(self.info_category_label)
        
        # Description
        self.info_description_label = QLabel("")
        self.info_description_label.setWordWrap(True)
        self.info_description_label.setStyleSheet("color: #34495e; margin: 5px 0px;")
        info_layout.addWidget(self.info_description_label)
        
        # Package types
        package_layout = QHBoxLayout()
        package_layout.addWidget(QLabel("Package:"))
        self.package_combo = QComboBox()
        self.package_combo.currentTextChanged.connect(self._on_package_changed)
        package_layout.addWidget(self.package_combo)
        info_layout.addLayout(package_layout)
        
        # Pin count
        self.info_pins_label = QLabel("")
        self.info_pins_label.setStyleSheet("color: #7f8c8d; font-size: 9px;")
        info_layout.addWidget(self.info_pins_label)
        
        # Add to canvas button
        self.add_button = QPushButton("Add to Canvas")
        self.add_button.clicked.connect(self._add_current_component)
        self.add_button.setEnabled(False)
        info_layout.addWidget(self.add_button)
        
        layout.addWidget(self.info_panel)
    
    def _set_view_mode(self, mode: str):
        """Set view mode (category or system)"""
        if mode != self.current_view:
            self.current_view = mode
            self._populate_components()
    
    def _on_search_changed(self, text: str):
        """Handle search text change"""
        self.search_text = text.lower()
        self._populate_components()
    
    def _on_category_filter_changed(self, category: str):
        """Handle category filter change"""
        self.selected_category = category if category != "All Categories" else "All"
        self._populate_components()
    
    def _populate_components(self):
        """Populate the component tree"""
        self.component_tree.clear()
        
        if not CHIPSETS_AVAILABLE:
            self._populate_fallback()
            return
        
        if self.current_view == "category":
            self._populate_by_category()
        else:
            self._populate_by_system()
    
    def _populate_fallback(self):
        """Populate with fallback components"""
        category_item = QTreeWidgetItem(["Fallback Components", "", ""])
        self.component_tree.addTopLevelItem(category_item)
        
        fallback_item = QTreeWidgetItem(["Generic CPU", "DIP-40", "Fallback component"])
        category_item.addChild(fallback_item)
        category_item.setExpanded(True)
    
    def _populate_by_category(self):
        """Populate components organized by category"""
        categories = self.palette_data['by_category']
        
        for category_name, chips in categories.items():
            # Skip if category filter is active and doesn't match
            if self.selected_category != "All" and category_name != self.selected_category:
                continue
            
            # Filter chips based on search
            filtered_chips = self._filter_chips(chips)
            if not filtered_chips:
                continue
            
            # Create category item
            category_item = QTreeWidgetItem([f"{category_name} ({len(filtered_chips)})", "", ""])
            category_item.setIcon(0, self._get_category_icon(category_name))
            self.component_tree.addTopLevelItem(category_item)
            
            # Add chips
            for chip in filtered_chips:
                self._add_chip_item(category_item, chip)
            
            category_item.setExpanded(True)
    
    def _populate_by_system(self):
        """Populate components organized by system"""
        systems = self.palette_data['by_system']
        
        for system_name, chips in systems.items():
            # Filter chips based on search and category
            filtered_chips = self._filter_chips(chips)
            if not filtered_chips:
                continue
            
            # Create system item
            system_item = QTreeWidgetItem([f"{system_name} ({len(filtered_chips)})", "", ""])
            system_item.setIcon(0, self._get_system_icon(system_name))
            self.component_tree.addTopLevelItem(system_item)
            
            # Add chips
            for chip in filtered_chips:
                self._add_chip_item(system_item, chip)
            
            system_item.setExpanded(True)
    
    def _filter_chips(self, chips: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter chips based on search and category"""
        filtered = []
        
        for chip in chips:
            # Search filter
            if self.search_text:
                searchable_text = f"{chip['name']} {chip['description']} {chip['category']}".lower()
                if self.search_text not in searchable_text:
                    continue
            
            # Category filter (when in system view)
            if (self.current_view == "system" and 
                self.selected_category != "All" and 
                chip.get('category', '') != self.selected_category):
                continue
            
            filtered.append(chip)
        
        return filtered
    
    def _add_chip_item(self, parent_item: QTreeWidgetItem, chip: Dict[str, Any]):
        """Add a chip item to the tree"""
        # Get default package type
        package_type = chip.get('package_types', ['DIP-40'])[0] if chip.get('package_types') else 'DIP-40'
        
        # Create component from chip definition
        if CHIPSETS_AVAILABLE:
            component = self.component_factory.create_component(chip, package_type)
        else:
            component = chip  # Use chip data directly in fallback
        
        # Create tree item
        chip_item = QTreeWidgetItem([
            chip['name'],
            package_type,
            chip['description'][:50] + "..." if len(chip['description']) > 50 else chip['description']
        ])
        
        # Set icon (use chip image if available)
        if CHIPSETS_AVAILABLE and component.get('has_image'):
            icon = QIcon(component['image'])
            chip_item.setIcon(0, icon)
        else:
            chip_item.setIcon(0, self._get_category_icon(chip['category']))
        
        # Store component data
        chip_item.setData(0, Qt.ItemDataRole.UserRole, component)
        
        parent_item.addChild(chip_item)
    
    def _get_category_icon(self, category: str) -> QIcon:
        """Get icon for category"""
        # Create simple colored icon for category
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        colors = {
            "CPU": QColor(220, 50, 50),
            "Video": QColor(50, 150, 220),
            "Audio": QColor(150, 50, 220),
            "Memory": QColor(50, 220, 50),
            "Custom": QColor(220, 150, 50),
            "I/O": QColor(220, 220, 50)
        }
        
        color = colors.get(category, QColor(128, 128, 128))
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, 12, 12)
        painter.end()
        
        return QIcon(pixmap)
    
    def _get_system_icon(self, system: str) -> QIcon:
        """Get icon for system"""
        # Use category icon for now
        return self._get_category_icon("Custom")
    
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item click"""
        component_data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if component_data:
            self.current_component = component_data
            self._update_info_panel(component_data)
            self.component_selected.emit(component_data.get('id', component_data.get('chip_id', '')), component_data)
    
    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item double click - add to canvas"""
        component_data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if component_data:
            self.component_double_clicked.emit(component_data.get('id', component_data.get('chip_id', '')), component_data)
            print(f"🎯 Adding {component_data['name']} to canvas")
    
    def _update_info_panel(self, component: Dict[str, Any]):
        """Update the info panel with component details"""
        # Component name and category
        self.info_name_label.setText(component['name'])
        self.info_category_label.setText(f"Category: {component.get('category', 'Unknown')}")
        
        # Description
        self.info_description_label.setText(component.get('description', 'No description available'))
        
        # Package types
        self.package_combo.blockSignals(True)
        self.package_combo.clear()
        package_types = component.get('package_types', ['DIP-40'])
        self.package_combo.addItems(package_types)
        current_package = component.get('package_type', package_types[0] if package_types else 'DIP-40')
        self.package_combo.setCurrentText(current_package)
        self.package_combo.blockSignals(False)
        
        # Pin count
        pin_count = component.get('pin_count', len(component.get('pins', [])))
        self.info_pins_label.setText(f"Pins: {pin_count}")
        
        # Enable add button
        self.add_button.setEnabled(True)
    
    def _on_package_changed(self, package_type: str):
        """Handle package type change"""
        if self.current_component and CHIPSETS_AVAILABLE:
            # Recreate component with new package type
            chip_def = self.chipset_manager.migrator.get_chip_definition(self.current_component.get('id', self.current_component.get('chip_id', '')))
            if chip_def:
                updated_component = self.component_factory.create_component(chip_def, package_type)
                self.current_component = updated_component
                
                # Update pin count display
                self.info_pins_label.setText(f"Pins: {updated_component['pin_count']}")
                
                # Emit signal about the change
                self.component_selected.emit(updated_component['id'], updated_component)
    
    def _add_current_component(self):
        """Add current component to canvas"""
        if self.current_component:
            component_id = self.current_component.get('id', self.current_component.get('chip_id', ''))
            self.component_double_clicked.emit(component_id, self.current_component)
            print(f"🎯 Adding {self.current_component['name']} to canvas")
    
    def get_component_by_id(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get component by ID"""
        if CHIPSETS_AVAILABLE:
            chip_def = self.chipset_manager.migrator.get_chip_definition(component_id)
            if chip_def:
                return self.component_factory.create_component(chip_def)
        return None
    
    def get_total_components(self) -> int:
        """Get total number of components"""
        return self.palette_data['total_chips']
    
    def refresh_palette(self):
        """Refresh the component palette"""
        print("🔄 Refreshing component palette...")
        self._populate_components()
    
    def refresh(self):
        """Refresh the palette (alias)"""
        self.refresh_palette()


# Export
__all__ = ['ComponentPalette']


# Test function
def test_component_palette():
    """Test the component palette"""
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    palette = ComponentPalette()
    palette.show()
    
    print("🧪 Component Palette Test")
    print(f"📦 Total components: {palette.get_total_components()}")
    
    if CHIPSETS_AVAILABLE:
        print(f"🖥️ Available systems: {len(palette.palette_data['by_system'])}")
        print(f"📂 Available categories: {len(palette.palette_data['by_category'])}")
    else:
        print("⚠️ Running in fallback mode")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_component_palette()
