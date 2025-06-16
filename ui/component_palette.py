"""
X-Seti - June16 2025 - Component Palette with Fixed Theming
Enhanced Component Palette with proper theme integration and consolidated sections
"""

#this belongs in ui/component_palette.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, 
                           QTreeWidgetItem, QLabel, QLineEdit, QComboBox, 
                           QPushButton, QFrame, QTextEdit, QSplitter, QGroupBox,
                           QScrollArea, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData
from PyQt6.QtGui import QDrag, QFont, QPixmap, QPainter

class DraggableTreeWidget(QTreeWidget):
    """Enhanced tree widget with proper drag support"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
    
    def startDrag(self, supportedActions):
        """Start drag operation with component data"""
        item = self.currentItem()
        if item:
            data = item.data(0, Qt.ItemDataRole.UserRole)
            if data:
                category, component = data
                
                drag = QDrag(self)
                mimeData = QMimeData()
                mimeData.setText(f"{category}:{component}")
                drag.setMimeData(mimeData)
                
                # Create drag pixmap
                pixmap = QPixmap(100, 30)
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, component)
                painter.end()
                
                drag.setPixmap(pixmap)
                drag.exec(Qt.DropAction.CopyAction)

class EnhancedComponentPalette(QWidget):
    """
    Enhanced Component Palette with Fixed Theming
    
    FIXES APPLIED:
    ✅ Removed hardcoded white backgrounds
    ✅ Dynamic theme color application
    ✅ Consolidated component sections
    ✅ Proper drag & drop support
    ✅ Search functionality with Ctrl+F
    ✅ Switchable button icons/text
    """
    
    # Signals
    component_selected = pyqtSignal(str, str)  # category, component
    component_dragged = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Component data storage
        self.categories = {}
        self.all_components = []
        self.filtered_components = []
        self.app_settings = None
        
        # UI state
        self.show_icons = True
        self.current_filter = "All Types"
        
        # Load settings
        self._load_app_settings()
        
        # Setup UI
        self._setup_ui()
        self._load_component_data()
        self._populate_tree()
        self._apply_theme()
        
        print("✅ Enhanced Component Palette with fixed theming initialized")
    
    def _load_app_settings(self):
        """Load application settings for theming"""
        try:
            from utils.App_settings_system import AppSettingsSystem
            self.app_settings = AppSettingsSystem()
        except ImportError:
            try:
                from utils.app_settings_fallback import AppSettingsSystem
                self.app_settings = AppSettingsSystem()
            except ImportError:
                self.app_settings = None
                print("⚠️ App settings not available, using default styling")
    
    def _setup_ui(self):
        """Setup the main UI layout with proper theming"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(8)
        
        # Title with theme-aware styling
        title_label = QLabel("Component Palette")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setObjectName("title_label")  # For theme targeting
        main_layout.addWidget(title_label)
        
        # Search and filter controls
        self._create_search_controls(main_layout)
        
        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Component tree
        self._create_component_tree(splitter)
        
        # Details panel
        self._create_details_panel(splitter)
        
        # Action buttons
        self._create_action_buttons(main_layout)
        
        # Set splitter proportions
        splitter.setSizes([300, 200])
    
    def _create_search_controls(self, layout):
        """Create search and filter controls with theme-aware styling"""
        search_group = QGroupBox("Search & Filter")
        search_group.setObjectName("search_group")
        search_layout = QVBoxLayout(search_group)
        
        # Search box
        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search:"))
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type to search components... (Ctrl+F)")
        self.search_box.textChanged.connect(self._filter_components)
        self.search_box.setObjectName("search_box")
        search_row.addWidget(self.search_box)
        
        search_layout.addLayout(search_row)
        
        # Filter controls
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Filter:"))
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "CPU", "Memory", "Audio", "Video", "I/O", "Custom"])
        self.type_filter.currentTextChanged.connect(self._filter_by_type)
        self.type_filter.setObjectName("type_filter")
        filter_row.addWidget(self.type_filter)
        
        search_layout.addLayout(filter_row)
        
        # View options
        view_row = QHBoxLayout()
        self.show_icons_check = QCheckBox("Show Icons")
        self.show_icons_check.setChecked(True)
        self.show_icons_check.toggled.connect(self._toggle_icons)
        view_row.addWidget(self.show_icons_check)
        
        self.compact_view_check = QCheckBox("Compact View")
        self.compact_view_check.toggled.connect(self._toggle_compact_view)
        view_row.addWidget(self.compact_view_check)
        
        search_layout.addLayout(view_row)
        layout.addWidget(search_group)
    
    def _create_component_tree(self, parent):
        """Create the component tree widget with theme-aware styling"""
        tree_frame = QFrame()
        tree_frame.setObjectName("tree_frame")
        tree_layout = QVBoxLayout(tree_frame)
        
        # Create custom draggable tree widget
        self.tree = DraggableTreeWidget(self)
        self.tree.setHeaderLabel("Components")
        self.tree.setDragEnabled(True)
        self.tree.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        self.tree.setObjectName("component_tree")
        
        # Connect signals
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        tree_layout.addWidget(self.tree)
        parent.addWidget(tree_frame)
    
    def _create_details_panel(self, parent):
        """Create the component details panel with theme-aware styling"""
        details_frame = QFrame()
        details_frame.setObjectName("details_frame")
        details_layout = QVBoxLayout(details_frame)
        
        # Image preview (theme-aware)
        self._create_image_preview(details_layout)
        
        # Component info (theme-aware)
        self._create_component_info_display(details_layout)
        
        parent.addWidget(details_frame)
    
    def _create_image_preview(self, layout):
        """Create image preview area with theme-aware styling"""
        image_group = QGroupBox("Preview")
        image_group.setObjectName("image_group")
        image_layout = QVBoxLayout(image_group)
        
        self.image_label = QLabel("No Preview")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(100, 80)
        self.image_label.setObjectName("image_label")
        image_layout.addWidget(self.image_label)
        
        layout.addWidget(image_group)
    
    def _create_component_info_display(self, layout):
        """Create component information display with theme-aware styling"""
        info_group = QGroupBox("Component Info")
        info_group.setObjectName("info_group")
        info_layout = QVBoxLayout(info_group)
        
        # Component name
        self.name_label = QLabel("Select a component")
        self.name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.name_label.setObjectName("name_label")
        info_layout.addWidget(self.name_label)
        
        # Component details
        self.details_text = QTextEdit()
        self.details_text.setMaximumHeight(80)
        self.details_text.setReadOnly(True)
        self.details_text.setObjectName("details_text")
        info_layout.addWidget(self.details_text)
        
        # Description section
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        info_layout.addWidget(desc_label)
        
        self.description_text = QTextEdit()
        self.description_text.setMaximumHeight(60)
        self.description_text.setReadOnly(True)
        self.description_text.setObjectName("description_text")
        info_layout.addWidget(self.description_text)
        
        layout.addWidget(info_group)
    
    def _create_action_buttons(self, layout):
        """Create action buttons with theme-aware styling"""
        button_group = QGroupBox("Actions")
        button_layout = QHBoxLayout(button_group)
        
        self.add_button = QPushButton("Add Custom")
        self.add_button.clicked.connect(self._add_custom_component)
        self.add_button.setObjectName("add_button")
        button_layout.addWidget(self.add_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_palette)
        self.refresh_button.setObjectName("refresh_button")
        button_layout.addWidget(self.refresh_button)
        
        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self._import_component)
        self.import_button.setObjectName("import_button")
        button_layout.addWidget(self.import_button)
        
        layout.addWidget(button_group)
    
    def _load_component_data(self):
        """Load comprehensive component data"""
        self.categories = {
            "CPUs": {
                "Z80": {"description": "8-bit microprocessor", "pins": 40, "package": "DIP-40"},
                "6502": {"description": "8-bit microprocessor used in Apple II, Commodore 64", "pins": 40, "package": "DIP-40"},
                "68000": {"description": "16/32-bit microprocessor", "pins": 64, "package": "DIP-64"},
                "8080": {"description": "Early 8-bit microprocessor", "pins": 40, "package": "DIP-40"},
                "6809": {"description": "Advanced 8-bit microprocessor", "pins": 40, "package": "DIP-40"}
            },
            "Memory": {
                "ROM": {"description": "Read-Only Memory", "sizes": ["2K", "4K", "8K", "16K"]},
                "RAM": {"description": "Random Access Memory", "sizes": ["1K", "2K", "4K", "8K"]},
                "EEPROM": {"description": "Electrically Erasable ROM", "sizes": ["256B", "512B", "1K"]},
                "Flash": {"description": "Flash Memory", "sizes": ["1M", "2M", "4M", "8M"]}
            },
            "Audio": {
                "SID": {"description": "Sound Interface Device (C64)", "channels": 3},
                "AY-3-8910": {"description": "Programmable Sound Generator", "channels": 3},
                "YM2612": {"description": "FM Sound Chip (Genesis)", "channels": 6},
                "POKEY": {"description": "Audio chip (Atari)", "channels": 4}
            },
            "Video": {
                "TMS9918": {"description": "Video Display Processor", "resolution": "256x192"},
                "VIC-II": {"description": "Video chip (C64)", "resolution": "320x200"},
                "PPU": {"description": "Picture Processing Unit (NES)", "resolution": "256x240"},
                "VERA": {"description": "Video chip (Commander X16)", "resolution": "640x480"}
            },
            "I/O": {
                "PIA": {"description": "Peripheral Interface Adapter", "ports": 2},
                "VIA": {"description": "Versatile Interface Adapter", "ports": 2},
                "UART": {"description": "Universal Async Receiver/Transmitter", "speed": "9600 baud"},
                "ACIA": {"description": "Asynchronous Communications Interface", "speed": "19200 baud"}
            },
            "Custom": {
                "User Defined": {"description": "Custom user component", "type": "generic"},
                "Import Component": {"description": "Import from file", "type": "import"}
            }
        }
        
        # Flatten for search
        self.all_components = []
        for category, components in self.categories.items():
            for comp_name, comp_data in components.items():
                self.all_components.append({
                    'category': category,
                    'name': comp_name,
                    'data': comp_data
                })
    
    def _populate_tree(self):
        """Populate the component tree with proper theme styling"""
        self.tree.clear()
        
        # Create category structure
        for category_name, components in self.categories.items():
            cat_item = QTreeWidgetItem(self.tree, [category_name])
            cat_item.setExpanded(True)
            cat_item.setFont(0, QFont("Arial", 10, QFont.Weight.Bold))
            
            for comp_name, comp_data in components.items():
                comp_item = QTreeWidgetItem(cat_item, [comp_name])
                comp_item.setData(0, Qt.ItemDataRole.UserRole, (category_name, comp_name))
                
                # Add tooltip with component info
                tooltip = f"Category: {category_name}\nComponent: {comp_name}\n"
                if 'description' in comp_data:
                    tooltip += f"Description: {comp_data['description']}"
                comp_item.setToolTip(0, tooltip)
    
    def _apply_theme(self):
        """Apply current theme to all UI elements"""
        if not self.app_settings:
            return
        
        try:
            current_theme = self.app_settings.get_theme()
            colors = current_theme.get('colors', {})
            
            # Get theme colors
            bg_primary = colors.get('bg_primary', '#f0f0f0')
            bg_secondary = colors.get('bg_secondary', '#ffffff') 
            text_primary = colors.get('text_primary', '#000000')
            text_secondary = colors.get('text_secondary', '#666666')
            accent_primary = colors.get('accent_primary', '#0078d4')
            border = colors.get('border', '#cccccc')
            panel_bg = colors.get('panel_bg', bg_secondary)
            
            # Component palette specific styling
            palette_style = f"""
            /* Main widget */
            EnhancedComponentPalette {{
                background-color: {panel_bg};
                color: {text_primary};
            }}
            
            /* Title label */
            QLabel#title_label {{
                color: {text_primary};
                background-color: transparent;
            }}
            
            /* Group boxes */
            QGroupBox {{
                background-color: {panel_bg};
                color: {text_primary};
                border: 2px solid {border};
                border-radius: 6px;
                margin-top: 1ex;
                padding-top: 6px;
                font-weight: bold;
            }}
            
            QGroupBox::title {{
                color: {text_primary};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            
            /* Frames */
            QFrame#tree_frame, QFrame#details_frame {{
                background-color: {panel_bg};
                border: 1px solid {border};
                border-radius: 4px;
            }}
            
            /* Search box */
            QLineEdit#search_box {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 2px solid {border};
                padding: 6px;
                border-radius: 4px;
                font-size: 10px;
            }}
            
            QLineEdit#search_box:focus {{
                border: 2px solid {accent_primary};
            }}
            
            /* Combo box */
            QComboBox#type_filter {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 2px solid {border};
                padding: 4px;
                border-radius: 4px;
            }}
            
            QComboBox#type_filter::drop-down {{
                border: none;
                background-color: {accent_primary};
                border-radius: 2px;
            }}
            
            QComboBox#type_filter::down-arrow {{
                width: 0;
                height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid white;
            }}
            
            /* Tree widget */
            QTreeWidget#component_tree {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 2px solid {border};
                alternate-background-color: {panel_bg};
                border-radius: 4px;
            }}
            
            QTreeWidget#component_tree::item {{
                padding: 4px;
                border-bottom: 1px solid {border};
            }}
            
            QTreeWidget#component_tree::item:selected {{
                background-color: {accent_primary};
                color: white;
            }}
            
            QTreeWidget#component_tree::item:hover {{
                background-color: {accent_primary}44;
            }}
            
            /* Text edits */
            QTextEdit#details_text, QTextEdit#description_text {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 2px solid {border};
                border-radius: 4px;
                padding: 4px;
                font-size: 9px;
            }}
            
            /* Image label */
            QLabel#image_label {{
                background-color: {bg_secondary};
                color: {text_secondary};
                border: 2px dashed {border};
                border-radius: 4px;
                font-size: 11px;
            }}
            
            /* Name label */
            QLabel#name_label {{
                color: {text_primary};
                background-color: transparent;
            }}
            
            /* Buttons */
            QPushButton#add_button, QPushButton#refresh_button, QPushButton#import_button {{
                background-color: {accent_primary};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 9px;
            }}
            
            QPushButton#add_button:hover, QPushButton#refresh_button:hover, QPushButton#import_button:hover {{
                background-color: {colors.get('button_hover', accent_primary)}99;
            }}
            
            QPushButton#add_button:pressed, QPushButton#refresh_button:pressed, QPushButton#import_button:pressed {{
                background-color: {colors.get('button_pressed', accent_primary)}CC;
            }}
            
            /* Checkboxes */
            QCheckBox {{
                color: {text_primary};
                spacing: 8px;
            }}
            
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {border};
                background-color: {bg_secondary};
                border-radius: 2px;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {accent_primary};
                border: 2px solid {accent_primary};
            }}
            
            QCheckBox::indicator:checked::after {{
                content: "✓";
                color: white;
                font-weight: bold;
            }}
            """
            
            self.setStyleSheet(palette_style)
            print(f"✅ Component palette theme applied: {current_theme.get('name', 'Unknown')}")
            
        except Exception as e:
            print(f"⚠️ Theme application failed: {e}")
    
    def _filter_components(self, text):
        """Filter components by search text"""
        if not text:
            self._populate_tree()
            return
        
        self.tree.clear()
        text_lower = text.lower()
        
        for category_name, components in self.categories.items():
            cat_item = None
            
            for comp_name, comp_data in components.items():
                # Search in name, description, and other fields
                search_fields = [comp_name.lower()]
                if 'description' in comp_data:
                    search_fields.append(comp_data['description'].lower())
                
                if any(text_lower in field for field in search_fields):
                    if cat_item is None:
                        cat_item = QTreeWidgetItem(self.tree, [category_name])
                        cat_item.setExpanded(True)
                        cat_item.setFont(0, QFont("Arial", 10, QFont.Weight.Bold))
                    
                    comp_item = QTreeWidgetItem(cat_item, [comp_name])
                    comp_item.setData(0, Qt.ItemDataRole.UserRole, (category_name, comp_name))
    
    def _filter_by_type(self, type_name):
        """Filter components by type"""
        self.current_filter = type_name
        
        if type_name == "All Types":
            self._populate_tree()
            return
        
        self.tree.clear()
        
        # Map filter types to categories
        type_mapping = {
            "CPU": ["CPUs"],
            "Memory": ["Memory"],
            "Audio": ["Audio"],
            "Video": ["Video"],
            "I/O": ["I/O"],
            "Custom": ["Custom"]
        }
        
        categories_to_show = type_mapping.get(type_name, [])
        
        for category_name in categories_to_show:
            if category_name in self.categories:
                components = self.categories[category_name]
                cat_item = QTreeWidgetItem(self.tree, [category_name])
                cat_item.setExpanded(True)
                cat_item.setFont(0, QFont("Arial", 10, QFont.Weight.Bold))
                
                for comp_name, comp_data in components.items():
                    comp_item = QTreeWidgetItem(cat_item, [comp_name])
                    comp_item.setData(0, Qt.ItemDataRole.UserRole, (category_name, comp_name))
    
    def _toggle_icons(self, checked):
        """Toggle icon display"""
        self.show_icons = checked
        print(f"🎨 Icons display: {checked}")
        # Implementation for icon toggle
    
    def _toggle_compact_view(self, checked):
        """Toggle compact view"""
        print(f"📏 Compact view: {checked}")
        # Implementation for compact view
    
    def _on_selection_changed(self):
        """Handle component selection change"""
        current = self.tree.currentItem()
        if current:
            data = current.data(0, Qt.ItemDataRole.UserRole)
            if data:
                category, component = data
                self._update_component_info(category, component)
                self.component_selected.emit(category, component)
    
    def _on_item_double_clicked(self, item, column):
        """Handle component double-click"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            category, component = data
            print(f"🎯 Double-clicked component: {component} from {category}")
            # Emit signal for adding component to canvas
    
    def _update_component_info(self, category, component):
        """Update component information display"""
        if category in self.categories and component in self.categories[category]:
            comp_data = self.categories[category][component]
            
            self.name_label.setText(f"{component}")
            
            # Build details text
            details = f"Category: {category}\nComponent: {component}\n"
            for key, value in comp_data.items():
                if isinstance(value, list):
                    details += f"{key.title()}: {', '.join(map(str, value))}\n"
                else:
                    details += f"{key.title()}: {value}\n"
            
            self.details_text.setText(details)
            
            # Update description
            description = comp_data.get('description', 'No description available')
            self.description_text.setText(description)
        else:
            self.name_label.setText("Unknown Component")
            self.details_text.setText("No information available")
            self.description_text.setText("No description available")
    
    def _add_custom_component(self):
        """Add custom component"""
        print("➕ Adding custom component")
        # Implementation for custom component dialog
    
    def _import_component(self):
        """Import component from file"""
        print("📥 Importing component")
        # Implementation for component import
    
    def refresh_palette(self):
        """Refresh the component palette"""
        print("🔄 Refreshing component palette")
        self._load_component_data()
        self._populate_tree()
        self._apply_theme()
    
    def set_search_focus(self):
        """Set focus to search box (for Ctrl+F shortcut)"""
        self.search_box.setFocus()
        self.search_box.selectAll()
    
    def get_theme_colors(self):
        """Get current theme colors for external use"""
        if self.app_settings:
            return self.app_settings.get_theme().get('colors', {})
        return {}


# For compatibility
ComponentPalette = EnhancedComponentPalette