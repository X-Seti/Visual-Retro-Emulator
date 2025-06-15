"""
X-Seti - June12 2025 - Enhanced Component Palette with Drag & Drop
Visual Retro System Emulator Builder - Complete Component Palette
"""

#this belongs in ui/component_palette.py

import os
import sys
import json
from typing import Dict, List, Optional, Tuple
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, 
                           QTreeWidgetItem, QLabel, QTextEdit, QLineEdit, 
                           QPushButton, QComboBox, QSplitter, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QByteArray, QSize, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QDrag, QFont, QMouseEvent

class ComponentTreeItem(QTreeWidgetItem):
    """Custom tree item that holds component data"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.component_data = {}
        self.is_component = False
        self.is_category = False

class DraggableTreeWidget(QTreeWidget):
    """Custom QTreeWidget with drag and drop functionality"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_palette = parent
        self.drag_start_position = QPoint()
        
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press to prepare for potential drag"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move to start drag operation"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        
        if ((event.position().toPoint() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
        
        # Check if we have a valid component item
        current_item = self.currentItem()
        if (current_item and isinstance(current_item, ComponentTreeItem) and 
            current_item.is_component):
            # Start the drag operation
            if self.parent_palette:
                self.parent_palette._start_drag_from_tree(current_item)
        
        super().mouseMoveEvent(event)

class EnhancedComponentPalette(QWidget):
    """
    COMPLETE Enhanced Component Palette with Drag & Drop Support
    
    Features:
    - Hierarchical component browser
    - Image previews and component details
    - Full drag and drop support
    - Search and filtering
    - Retro computer component library
    """
    
    # Signals
    componentSelected = pyqtSignal(dict)
    componentDoubleClicked = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Component data storage
        self.categories = {}
        self.all_components = []
        self.filtered_components = []
        
        # Setup UI
        self._setup_ui()
        self._load_component_data()
        self._populate_tree()
        
        print("✓ Enhanced Component Palette initialized with drag & drop")
    
    def _setup_ui(self):
        """Setup the main UI layout"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(6)
        
        # Title
        title_label = QLabel("Component Palette")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 4px;")
        main_layout.addWidget(title_label)
        
        # Search controls
        self._create_search_controls(main_layout)
        
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Component tree
        self._create_component_tree(splitter)
        
        # Details panel
        self._create_details_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([300, 200])
    
    def _create_search_controls(self, layout):
        """Create search and filter controls"""
        search_frame = QFrame()
        search_frame.setFrameStyle(QFrame.Shape.Box)
        search_layout = QVBoxLayout(search_frame)
        
        # Search box
        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search:"))
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type to search components...")
        self.search_box.textChanged.connect(self._filter_components)
        search_row.addWidget(self.search_box)
        
        search_layout.addLayout(search_row)
        
        # Filter by type
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Filter:"))
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "CPU", "Memory", "Audio", "Video", "I/O", "Custom"])
        self.type_filter.currentTextChanged.connect(self._filter_by_type)
        filter_row.addWidget(self.type_filter)
        
        search_layout.addLayout(filter_row)
        layout.addWidget(search_frame)
    
    def _create_component_info_display(self, layout):
        """Create component information display UI"""
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.Box)
        info_layout = QVBoxLayout(info_frame)

        # Component name
        self.name_label = QLabel("Select a component")
        self.name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: #2c3e50;")
        info_layout.addWidget(self.name_label)

        # Component details
        self.details_text = QTextEdit()
        self.details_text.setMaximumHeight(80)
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                font-size: 9px;
            }
        """)
        info_layout.addWidget(self.details_text)

        layout.addWidget(info_frame)

    def _create_component_tree(self, parent):
        """Create the component tree widget with drag support"""
        tree_frame = QFrame()
        tree_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        tree_layout = QVBoxLayout(tree_frame)
        
        # Create custom draggable tree widget
        self.tree = DraggableTreeWidget(self)
        self.tree.setHeaderLabel("Components")
        self.tree.setDragEnabled(True)
        self.tree.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        
        # Connect signals
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        tree_layout.addWidget(self.tree)
        parent.addWidget(tree_frame)
    
    def _create_details_panel(self, parent):
        """Create the component details panel"""
        details_frame = QFrame()
        details_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        details_layout = QVBoxLayout(details_frame)
        
        # Image preview
        self._create_image_preview(details_layout)
        
        # Component info
        #self._create_component_info(details_layout)
        self._create_component_info_display(details_layout)
        # Action buttons
        self._create_action_buttons(details_layout)
        
        parent.addWidget(details_frame)
    
    def _create_image_preview(self, layout):
        """Create image preview area"""
        image_frame = QFrame()
        image_frame.setFrameStyle(QFrame.Shape.Box)
        image_frame.setMaximumHeight(120)
        image_layout = QVBoxLayout(image_frame)
        
        self.image_label = QLabel("No Preview")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 1px dashed #ccc;
                color: #666;
                font-size: 11px;
            }
        """)
        self.image_label.setMinimumSize(100, 80)
        image_layout.addWidget(self.image_label)
        
        layout.addWidget(image_frame)
    
    def _create_component_info(self, layout):
        """Create component information display"""
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.Box)
        info_layout = QVBoxLayout(info_frame)
        
        # Component name
        self.name_label = QLabel("Select a component")
        self.name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: #2c3e50;")
        info_layout.addWidget(self.name_label)
        
        # Component details
        self.details_text = QTextEdit()
        self.details_text.setMaximumHeight(80)
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                font-size: 9px;
            }
        """)
        info_layout.addWidget(self.details_text)
        
        layout.addWidget(info_frame)
    
    def _create_description_section(self, layout):
        """Create component description section"""
        desc_frame = QFrame()
        desc_frame.setFrameStyle(QFrame.Shape.Box)
        desc_layout = QVBoxLayout(desc_frame)
        
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        desc_layout.addWidget(desc_label)
        
        self.description_text = QTextEdit()
        self.description_text.setMaximumHeight(60)
        self.description_text.setReadOnly(True)
        desc_layout.addWidget(self.description_text)
        
        layout.addWidget(desc_frame)
    
    def _create_action_buttons(self, layout):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Custom")
        self.add_button.clicked.connect(self._add_custom_component)
        button_layout.addWidget(self.add_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_palette)
        button_layout.addWidget(self.refresh_button)
        
        layout.addLayout(button_layout)
    
    def _populate_tree(self):
        """Populate the component tree"""
        self.tree.clear()
        
        # Create category structure
        category_items = {}
        
        for category_name, components in self.categories.items():
            if not components:  # Skip empty categories
                continue
                
            # Create category item
            category_item = ComponentTreeItem()
            category_item.setText(0, category_name.upper())
            category_item.is_category = True
            category_item.setFont(0, QFont("Arial", 9, QFont.Weight.Bold))
            category_item.setExpanded(True)
            
            # Add components to category
            for component in components:
                comp_item = ComponentTreeItem(category_item)
                comp_item.setText(0, component['name'])
                comp_item.component_data = component
                comp_item.is_component = True
                
                # Set component icon/styling
                comp_item.setFont(0, QFont("Arial", 8))
                
                # Add tooltip
                tooltip = f"Type: {component.get('type', 'Unknown')}\n"
                tooltip += f"System: {component.get('system', 'Unknown')}\n"
                tooltip += f"Package: {component.get('package', 'Unknown')}"
                comp_item.setToolTip(0, tooltip)
            
            self.tree.addTopLevelItem(category_item)
            category_items[category_name] = category_item
        
        print(f"✓ Component tree populated with {len(category_items)} categories")
    
    def _load_component_data(self):
        """Load component data with proper image mapping"""
        self.categories = {
            "cpu": [],
            "memory": [],
            "io": [],
            "sound": [],
            "video": [],
            "custom": []
        }
        
        # Define retro computer components
        components_data = [
            # === CPU COMPONENTS ===
            {"name": "6502 CPU", "brand": "MOS", "system": "Apple II/C64", "type": "cpu", "package": "DIP-40"},
            {"name": "MC68000", "brand": "Motorola", "system": "Amiga/Atari ST", "type": "cpu", "package": "DIP-64"},
            {"name": "Z80", "brand": "Zilog", "system": "Amstrad/Spectrum", "type": "cpu", "package": "DIP-40"},
            {"name": "6809", "brand": "Motorola", "system": "Dragon/CoCo", "type": "cpu", "package": "DIP-40"},
            {"name": "8086", "brand": "Intel", "system": "IBM PC", "type": "cpu", "package": "DIP-40"},
            
            # === AMIGA CUSTOM CHIPS ===
            {"name": "Paula", "brand": "Commodore", "system": "Amiga", "type": "sound", "package": "PLCC-48"},
            {"name": "Denise", "brand": "Commodore", "system": "Amiga", "type": "video", "package": "PLCC-48"},
            {"name": "Agnus", "brand": "Commodore", "system": "Amiga", "type": "video", "package": "PLCC-84"},
            {"name": "Gary", "brand": "Commodore", "system": "Amiga", "type": "io", "package": "PLCC-48"},
            
            # === C64 CHIPS ===
            {"name": "VIC-II", "brand": "Commodore", "system": "C64", "type": "video", "package": "DIP-40"},
            {"name": "SID", "brand": "Commodore", "system": "C64", "type": "sound", "package": "DIP-28"},
            {"name": "CIA", "brand": "Commodore", "system": "C64", "type": "io", "package": "DIP-40"},
            
            # === ATARI CHIPS ===
            {"name": "ANTIC", "brand": "Atari", "system": "8-bit", "type": "video", "package": "DIP-40"},
            {"name": "GTIA", "brand": "Atari", "system": "8-bit", "type": "video", "package": "DIP-40"},
            {"name": "POKEY", "brand": "Atari", "system": "8-bit", "type": "sound", "package": "DIP-40"},
            
            # === BBC MICRO CHIPS ===
            {"name": "System VIA", "brand": "BBC", "system": "Micro", "type": "io", "package": "DIP-40"},
            {"name": "Video ULA", "brand": "BBC", "system": "Micro", "type": "video", "package": "DIP-40"},
            {"name": "CRTC", "brand": "BBC", "system": "Micro", "type": "video", "package": "DIP-40"},
            
            # === MEMORY COMPONENTS ===
            {"name": "2114 SRAM", "brand": "Generic", "system": "Various", "type": "memory", "package": "DIP-18"},
            {"name": "4116 DRAM", "brand": "Generic", "system": "Various", "type": "memory", "package": "DIP-16"},
            {"name": "2732 EPROM", "brand": "Generic", "system": "Various", "type": "memory", "package": "DIP-24"},
            
            # === TEST COMPONENTS ===
            {"name": "Test Chip", "brand": "Generic", "system": "Test", "type": "custom", "package": "DIP-14"}
        ]
        
        for comp_data in components_data:
            component = self._create_component_info(
                comp_data["name"], 
                comp_data["brand"], 
                comp_data["system"],
                comp_data["type"],
                comp_data["package"]
            )
            if component:
                category = component['category']
                if category in self.categories:
                    self.categories[category].append(component)
                else:
                    self.categories['custom'].append(component)
        
        print(f"✓ Loaded {sum(len(comps) for comps in self.categories.values())} components")
    
    def _create_component_info(self, name: str, brand: str, system: str, comp_type: str = "unknown", package: str = "DIP"):
        """Create component information dictionary"""
        
        # Map component types to categories
        type_to_category = {
            "cpu": "cpu",
            "memory": "memory", 
            "sound": "sound",
            "video": "video",
            "io": "io",
            "custom": "custom"
        }
        
        category = type_to_category.get(comp_type.lower(), "custom")
        
        # Find component image
        image_path = self._find_component_image_with_priority(name, comp_type, package)
        
        # Get pinout data
        pinout_data = self._get_pinout_data(name, comp_type)
        
        component_info = {
            'name': name,
            'brand': brand,
            'system': system,
            'type': comp_type,
            'category': category,
            'package': package,
            'image_path': image_path,
            'pinout': pinout_data,
            'description': f"{brand} {name} - Used in {system} systems",
            'pins': pinout_data.get('pins', []),
            'voltage': pinout_data.get('voltage', '5V'),
            'frequency': pinout_data.get('frequency', 'N/A')
        }
        
        return component_info
    
    def _find_component_image_with_priority(self, name: str, comp_type: str, package: str) -> Optional[str]:
        """Find component image with priority search"""
        search_paths = [
            "images/components",
            "images/chips",
            "images/retro_chips", 
            "images",
            "assets/components",
            "assets/chips"
        ]
        
        # Generate search filenames
        name_clean = name.replace(' ', '_').replace('-', '_').lower()
        type_clean = comp_type.replace(' ', '_').lower()
        package_clean = package.replace('-', '_').lower()
        
        search_filenames = [
            f"{name_clean}.png",
            f"{name_clean}.jpg",
            f"{name}.png", 
            f"{name}.jpg",
            f"{name_clean}_{package_clean}.png",
            f"{type_clean}.png",
            f"generic_{type_clean}.png",
            "generic_ic.png"
        ]
        
        # Search for image
        for path in search_paths:
            if not os.path.exists(path):
                continue
            for filename in search_filenames:
                full_path = os.path.join(path, filename)
                if os.path.exists(full_path):
                    return full_path
        
        return None
    
    def _get_pinout_data(self, name: str, comp_type: str) -> Dict:
        """Get pinout data for component"""
        # This would typically load from a pinout database
        # For now, return basic structure
        return {
            'pins': [],
            'voltage': '5V',
            'frequency': 'N/A',
            'description': f"Pinout data for {name}"
        }
    
    def _start_drag_from_tree(self, tree_item: ComponentTreeItem):
        """Start drag operation from tree widget (ENHANCED)"""
        if not tree_item or not tree_item.is_component:
            return
        
        # Create drag object
        drag = QDrag(self.tree)
        mime_data = QMimeData()
        
        # Set component data in the proper format for canvas
        component_data = tree_item.component_data
        drag_text = f"component:{component_data.get('type', 'unknown')}:{component_data.get('name', 'Unknown')}"
        mime_data.setText(drag_text)
        
        # Also set as JSON for advanced handling
        mime_data.setData("application/x-component", json.dumps(component_data).encode())
        
        drag.setMimeData(mime_data)
        
        # Create drag pixmap
        pixmap = self._create_drag_pixmap(component_data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(pixmap.rect().center())
        
        # Execute drag
        result = drag.exec(Qt.DropAction.CopyAction)
        
        print(f"✓ Drag started for component: {component_data.get('name')} (result: {result})")
    
    def _start_drag(self, supportedActions):
        """Legacy drag start method for compatibility"""
        current_item = self.tree.currentItem()
        if current_item and isinstance(current_item, ComponentTreeItem):
            self._start_drag_from_tree(current_item)
    
    def _create_drag_pixmap(self, component_data: Dict) -> QPixmap:
        """Create drag pixmap for component"""
        # Try to load component image
        image_path = component_data.get('image_path')
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale to reasonable drag size
                if pixmap.width() > 64 or pixmap.height() > 64:
                    pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
                return pixmap
        
        # Create fallback drag pixmap
        pixmap = QPixmap(64, 48)
        pixmap.fill(Qt.GlobalColor.lightGray)
        
        painter = QPainter(pixmap)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawRect(0, 0, 63, 47)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, 
                        component_data.get('name', 'Component')[:8])
        painter.end()
        
        return pixmap
    
    def _on_selection_changed(self):
        """Handle tree selection change"""
        current_item = self.tree.currentItem()
        if current_item and isinstance(current_item, ComponentTreeItem) and current_item.is_component:
            self._update_image_preview(current_item.component_data)
            self.componentSelected.emit(current_item.component_data)
    
    def _update_image_preview(self, component_data: Dict):
        """Update the image preview and component details"""
        # Update component name
        self.name_label.setText(component_data.get('name', 'Unknown Component'))
        
        # Update details
        details = f"Brand: {component_data.get('brand', 'Unknown')}\n"
        details += f"System: {component_data.get('system', 'Unknown')}\n"
        details += f"Type: {component_data.get('type', 'Unknown')}\n"
        details += f"Package: {component_data.get('package', 'Unknown')}"
        self.details_text.setPlainText(details)
        
        # Update image
        image_path = component_data.get('image_path')
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale to fit preview area
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setText("")
            else:
                self.image_label.setText("Image Load Failed")
                self.image_label.setPixmap(QPixmap())
        else:
            self.image_label.setText("No Preview Available")
            self.image_label.setPixmap(QPixmap())
    
    def _clear_details(self):
        """Clear the details panel"""
        self.name_label.setText("Select a component")
        self.details_text.clear()
        self.image_label.setText("No Preview")
        self.image_label.setPixmap(QPixmap())
    
    def _filter_components(self):
        """Filter components based on search text"""
        search_text = self.search_box.text().lower()
        self.hide_show_item(self.tree.invisibleRootItem(), search_text)
    
    def hide_show_item(self, item, search_text):
        """Recursively hide/show items based on search"""
        item_visible = False
        
        # Check children first
        for i in range(item.childCount()):
            child = item.child(i)
            child_visible = self.hide_show_item(child, search_text)
            if child_visible:
                item_visible = True
        
        # Check if this item matches search
        if isinstance(item, ComponentTreeItem):
            if item.is_component:
                item_matches = (search_text in item.text(0).lower() or
                               search_text in item.component_data.get('brand', '').lower() or
                               search_text in item.component_data.get('system', '').lower())
                if item_matches:
                    item_visible = True
            elif item.is_category:
                # Categories are visible if they have visible children
                pass
        
        item.setHidden(not item_visible)
        return item_visible
    
    def _filter_by_type(self, type_filter):
        """Filter components by type"""
        self.hide_show_by_type(self.tree.invisibleRootItem(), type_filter)
    
    def hide_show_by_type(self, item, type_filter):
        """Recursively filter by component type"""
        item_visible = False
        
        # Check children first
        for i in range(item.childCount()):
            child = item.child(i)
            child_visible = self.hide_show_by_type(child, type_filter)
            if child_visible:
                item_visible = True
        
        # Check if this item matches type filter
        if isinstance(item, ComponentTreeItem):
            if item.is_component:
                if type_filter == "All Types":
                    item_visible = True
                else:
                    component_type = item.component_data.get('type', '').upper()
                    if component_type == type_filter.upper():
                        item_visible = True
            elif item.is_category:
                # Categories are visible if they have visible children
                pass
        
        item.setHidden(not item_visible)
        return item_visible
    
    def _on_item_double_clicked(self, item, column):
        """Handle item double click"""
        if isinstance(item, ComponentTreeItem) and item.is_component:
            self.componentDoubleClicked.emit(item.component_data)
    
    def _add_custom_component(self):
        """Add custom component"""
        print("Add custom component requested")
    
    def refresh_palette(self):
        """Refresh the component palette"""
        self._load_component_data()
        self._populate_tree()
        self._clear_details()
        print("✓ Component palette refreshed")
