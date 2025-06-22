#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Component Palette with Bubble Interface
"""

#this belongs in ui/component_palette.py

import os
import sys
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget,
                           QTreeWidgetItem, QLineEdit, QComboBox, QPushButton,
                           QLabel, QFrame, QCheckBox, QToolTip, QGraphicsDropShadowEffect,
                           QDialog, QTextEdit, QSplitter, QScrollArea, QTabWidget)
from PyQt6.QtCore import (Qt, pyqtSignal, QTimer, QPoint, QRect, QPropertyAnimation,
                        QEasingCurve, QParallelAnimationGroup, QMimeData)
from PyQt6.QtGui import (QFont, QPixmap, QPainter, QColor, QPen, QBrush, 
                       QCursor, QPalette, QIcon, QDrag)

class ComponentBubble(QWidget):
    """Floating component information bubble"""
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.ToolTip)
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        # Remove the translucent background to avoid opacity issues
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Setup layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Component image
        self.image_label = QLabel()
        self.image_label.setFixedSize(120, 80)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 10px;
                color: #666;
            }
        """)
        layout.addWidget(self.image_label)
        
        # Component name
        self.name_label = QLabel()
        self.name_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("color: #2c3e50; background: transparent;")
        layout.addWidget(self.name_label)
        
        # Quick info
        self.info_label = QLabel()
        self.info_label.setFont(QFont("Arial", 9))
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.info_label.setStyleSheet("color: #34495e; background: transparent;")
        layout.addWidget(self.info_label)
        
        # Encyclopedia button
        self.encyclopedia_button = QPushButton("📖 More Info")
        self.encyclopedia_button.setFont(QFont("Arial", 8))
        self.encyclopedia_button.setFixedHeight(25)
        self.encyclopedia_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(self.encyclopedia_button)
        
        # Style the bubble - solid background instead of translucent
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 12px;
            }
        """)
        
        # Simple timer for hiding (no opacity animations to avoid issues)
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)
        
    def show_component_info(self, category, component, component_data, position):
        """Show component information bubble"""
        # Set content
        self.name_label.setText(f"{component}")
        
        # Build quick info
        info_text = f"Category: {category}\n"
        if 'package' in component_data:
            info_text += f"Package: {component_data['package']}\n"
        if 'pins' in component_data:
            info_text += f"Pins: {component_data['pins']}\n"
        if 'description' in component_data:
            desc = component_data['description'][:100] + "..." if len(component_data['description']) > 100 else component_data['description']
            info_text += f"\n{desc}"
        
        self.info_label.setText(info_text)
        
        # Set position
        self.move(position)
        
        # Show without opacity animation
        self.show()
        
        # Reset hide timer
        self.hide_timer.start(3000)  # Hide after 3 seconds
    
    def enterEvent(self, event):
        """Mouse entered - keep visible"""
        self.hide_timer.stop()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Mouse left - start hide timer"""
        self.hide_timer.start(1000)
        super().leaveEvent(event)

class ComponentEncyclopedia(QDialog):
    """Component encyclopedia dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Component Encyclopedia")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowMaximizeButtonHint)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search components...")
        search_layout.addWidget(self.search_box)
        layout.addLayout(search_layout)
        
        # Main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Component list
        self.component_list = QTreeWidget()
        self.component_list.setHeaderLabels(["Component", "Category", "Package"])
        self.component_list.setMaximumWidth(300)
        splitter.addWidget(self.component_list)
        
        # Details tabs
        self.details_tabs = QTabWidget()
        
        # Overview tab
        self.overview_text = QTextEdit()
        self.overview_text.setReadOnly(True)
        self.details_tabs.addTab(self.overview_text, "Overview")
        
        # Pinout tab
        self.pinout_text = QTextEdit()
        self.pinout_text.setReadOnly(True)
        self.details_tabs.addTab(self.pinout_text, "Pinout")
        
        # Specifications tab
        self.specs_text = QTextEdit()
        self.specs_text.setReadOnly(True)
        self.details_tabs.addTab(self.specs_text, "Specifications")
        
        # Applications tab
        self.applications_text = QTextEdit()
        self.applications_text.setReadOnly(True)
        self.details_tabs.addTab(self.applications_text, "Applications")
        
        splitter.addWidget(self.details_tabs)
        layout.addWidget(splitter)
        
        # Connect signals
        self.component_list.itemClicked.connect(self.show_component_details)
        self.search_box.textChanged.connect(self.filter_components)
        
        # Load data
        self.load_encyclopedia_data()
    
    def load_encyclopedia_data(self):
        """Load component encyclopedia data"""
        # This would load from a comprehensive component database
        sample_data = {
            "Z80": {
                "category": "CPU",
                "package": "DIP-40",
                "overview": "The Z80 is an 8-bit microprocessor designed by Zilog...",
                "pinout": "Pin 1: A11\nPin 2: A12\nPin 3: A13...",
                "specifications": "Clock Speed: 2.5-8 MHz\nData Bus: 8-bit\nAddress Bus: 16-bit...",
                "applications": "Used in computers like ZX Spectrum, MSX, Game Boy..."
            }
        }
        # Populate list...
    
    def show_component_details(self, item):
        """Show detailed component information"""
        # Implementation for showing detailed info
        pass
    
    def filter_components(self, text):
        """Filter components by search text"""
        # Implementation for filtering
        pass

class ComponentPalette(QWidget):
    """component palette with bubble tooltips"""
    
    component_selected = pyqtSignal(str, str)  # category, component
    component_double_clicked = pyqtSignal(str, str)  # category, component
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Component Palette")
        self.setMinimumWidth(280)
        self.setMaximumWidth(350)
        
        # Initialize data
        self.categories = {}
        self.bubble = ComponentBubble(self)
        self.encyclopedia = None
        
        # Setup UI
        self._create_ui()
        self._load_component_data()
        self._populate_tree()
        
        print("✅ Component Palette initialized")
    
    def _create_ui(self):
        """Create the main UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Title
        title_label = QLabel("🔧 Components")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background-color: rgba(52, 152, 219, 0.1);
                padding: 8px;
                border-radius: 6px;
                border: 1px solid rgba(52, 152, 219, 0.3);
            }
        """)
        layout.addWidget(title_label)
        
        # Search and filter
        search_layout = QHBoxLayout()
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search components... (Ctrl+F)")
        self.search_box.textChanged.connect(self._filter_components)
        search_layout.addWidget(self.search_box)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "CPUs", "Memory", "Custom ICs", "I/O"])
        self.type_filter.currentTextChanged.connect(self._filter_by_type)
        self.type_filter.setMaximumWidth(100)
        search_layout.addWidget(self.type_filter)
        
        layout.addLayout(search_layout)
        
        # Options
        options_layout = QHBoxLayout()
        
        self.show_icons = QCheckBox("Icons")
        self.show_icons.setChecked(True)
        self.show_icons.toggled.connect(self._update_display)
        options_layout.addWidget(self.show_icons)
        
        self.compact_view = QCheckBox("Compact")
        self.compact_view.toggled.connect(self._update_display)
        options_layout.addWidget(self.compact_view)
        
        options_layout.addStretch()
        
        # Encyclopedia button
        self.encyclopedia_btn = QPushButton("📚")
        self.encyclopedia_btn.setToolTip("Open Component Encyclopedia")
        self.encyclopedia_btn.setFixedSize(30, 25)
        self.encyclopedia_btn.clicked.connect(self._open_encyclopedia)
        self.encyclopedia_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        options_layout.addWidget(self.encyclopedia_btn)
        
        layout.addLayout(options_layout)
        
        # Component tree
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setRootIsDecorated(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.itemClicked.connect(self._on_item_clicked)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.tree.itemEntered.connect(self._on_item_hover)
        self.tree.setMouseTracking(True)
        
        # Enable drag and drop
        self.tree.setDragEnabled(True)
        self.tree.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        
        # Style the tree for better readability
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #ffffff;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 11px;
                font-family: 'Segoe UI', Arial, sans-serif;
                selection-background-color: #3498db;
                alternate-background-color: #f8f9fa;
            }
            QTreeWidget::item {
                padding: 6px 4px;
                border-bottom: 1px solid #ecf0f1;
                color: #2c3e50;
                font-weight: normal;
            }
            QTreeWidget::item:hover {
                background-color: rgba(52, 152, 219, 0.15);
                color: #2c3e50;
            }
            QTreeWidget::item:selected {
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }
            QTreeWidget::branch {
                background-color: transparent;
            }
            QTreeWidget::branch:has-children:closed {
                image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAABYSURBVBiVpY4xDgAgCEP7/w9nJ1YHJ+sQbpDQFhq6MC6+78sAUziGIwFJMWTgEWFE6w3g0bZSQEJAPE8DJBCBKxABEUhAJBJQiQQ0IgGdSEAnElCIBHSJf1LGABlqL4GiAAAAAElFTkSuQmCC);
            }
            QTreeWidget::branch:has-children:open {
                image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAABeSURBVBiVlY0xEgAgCAK7/w9TJ20HJ48F5QAhIsJaZyAdB8AKYDywA4BnhB2k3QUsA+yAZQBnhHOA+WGwAqgD2ACsA0YB7oBJgAkSsAIwDvABsAfwAXAH8AFwB/ABcADwA2AvAbj3AEAWAAAAAElFTkSuQmCC);
            }
        """)
        
        layout.addWidget(self.tree)
        
        # Override tree widget to handle drag operations
        self.tree.startDrag = self._start_drag_operation
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.add_custom_btn = QPushButton("➕")
        self.add_custom_btn.setToolTip("Add Custom Component")
        self.add_custom_btn.setFixedSize(35, 25)
        self.add_custom_btn.clicked.connect(self._add_custom_component)
        button_layout.addWidget(self.add_custom_btn)
        
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setToolTip("Refresh Palette")
        self.refresh_btn.setFixedSize(35, 25)
        self.refresh_btn.clicked.connect(self.refresh_palette)
        button_layout.addWidget(self.refresh_btn)
        
        self.import_btn = QPushButton("📁")
        self.import_btn.setToolTip("Import Components")
        self.import_btn.setFixedSize(35, 25)
        self.import_btn.clicked.connect(self._import_components)
        button_layout.addWidget(self.import_btn)
        
        button_layout.addStretch()
        
        # Apply consistent button styling
        for btn in [self.add_custom_btn, self.refresh_btn, self.import_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #7f8c8d;
                }
            """)
        
        layout.addLayout(button_layout)
    
    def _load_component_data(self):
        """Load component data from file or create sample data"""
        try:
            # Try to load from file
            if os.path.exists('components.json'):
                with open('components.json', 'r') as f:
                    self.categories = json.load(f)
            else:
                # Sample data
                self.categories = {
                    "CPUs": {
                        "Z80": {"package": "DIP-40", "pins": 40, "description": "8-bit microprocessor"},
                        "6502": {"package": "DIP-40", "pins": 40, "description": "8-bit microprocessor"},
                        "68000": {"package": "DIP-64", "pins": 64, "description": "16/32-bit microprocessor"}
                    },
                    "Memory": {
                        "ROM": {"package": "DIP-28", "pins": 28, "description": "Read-only memory"},
                        "RAM": {"package": "DIP-16", "pins": 16, "description": "Random access memory"},
                        "EEPROM": {"package": "DIP-28", "pins": 28, "description": "Electrically erasable PROM"}
                    },
                    "Custom ICs": {
                        "SID": {"package": "DIP-28", "pins": 28, "description": "Sound interface device"},
                        "VIC-II": {"package": "DIP-40", "pins": 40, "description": "Video interface chip"}
                    }
                }
            print(f"✅ Loaded {sum(len(comps) for comps in self.categories.values())} components")
        except Exception as e:
            print(f"⚠️ Error loading component data: {e}")
            self.categories = {}
    
    def _populate_tree(self):
        """Populate the component tree"""
        self.tree.clear()
        
        for category_name, components in self.categories.items():
            # Create category item
            category_item = QTreeWidgetItem([f"📁 {category_name}"])
            category_item.setFont(0, QFont("Arial", 10, QFont.Weight.Bold))
            self.tree.addTopLevelItem(category_item)
            
            # Add components
            for comp_name, comp_data in components.items():
                icon = "🔲" if self.show_icons.isChecked() else ""
                display_text = f"{icon} {comp_name}" if icon else comp_name
                
                if self.compact_view.isChecked():
                    display_text += f" ({comp_data.get('package', 'Unknown')})"
                
                comp_item = QTreeWidgetItem([display_text])
                comp_item.setData(0, Qt.ItemDataRole.UserRole, (category_name, comp_name, comp_data))
                
                # Set drag and drop data
                mime_data = f"component:{category_name}:{comp_name}:{comp_data.get('package', 'DIP-40')}"
                comp_item.setData(0, Qt.ItemDataRole.UserRole + 1, mime_data)
                
                category_item.addChild(comp_item)
        
        # Expand all categories
        self.tree.expandAll()
    
    def _on_item_clicked(self, item, column):
        """Handle item click"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            category, component, comp_data = data
            self.component_selected.emit(category, component)
    
    def _on_item_double_clicked(self, item, column):
        """Handle item double click"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            category, component, comp_data = data
            self.component_double_clicked.emit(category, component)
            print(f"🎯 Adding {component} to canvas")
    
    def _on_item_hover(self, item, column):
        """Handle item hover - show bubble"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            category, component, comp_data = data
            
            # Calculate bubble position
            item_rect = self.tree.visualItemRect(item)
            global_pos = self.tree.mapToGlobal(item_rect.topRight())
            bubble_pos = QPoint(global_pos.x() + 10, global_pos.y())
            
            # Show bubble
            self.bubble.show_component_info(category, component, comp_data, bubble_pos)
    
    def _filter_components(self, text):
        """Filter components by search text"""
        self._populate_tree()  # Refresh tree based on filters
    
    def _filter_by_type(self, type_name):
        """Filter components by type"""
        self._populate_tree()  # Refresh tree based on filters
    
    def _update_display(self):
        """Update display based on options"""
        self._populate_tree()
    
    def _open_encyclopedia(self):
        """Open component encyclopedia"""
        if not self.encyclopedia:
            self.encyclopedia = ComponentEncyclopedia(self)
        self.encyclopedia.show()
        self.encyclopedia.raise_()
    
    def _add_custom_component(self):
        """Add custom component"""
        print("➕ Adding custom component")
        # Implementation for custom component dialog
    
    def _import_components(self):
        """Import components from file"""
        print("📁 Importing components")
        # Implementation for component import
    
    def refresh_palette(self):
        """Refresh the component palette"""
        print("🔄 Refreshing component palette")
        self._load_component_data()
        self._populate_tree()
    
    def set_search_focus(self):
        """Set focus to search box (for Ctrl+F shortcut)"""
        self.search_box.setFocus()
        self.search_box.selectAll()
    
    def _start_drag_operation(self, supported_actions):
        """Start drag operation for component"""
        current_item = self.tree.currentItem()
        if current_item:
            # Get drag data
            drag_data = current_item.data(0, Qt.ItemDataRole.UserRole + 1)
            if drag_data:
                # Create drag object
                drag = QDrag(self.tree)
                mime_data = QMimeData()
                mime_data.setText(drag_data)
                drag.setMimeData(mime_data)
                
                # Create drag pixmap (visual feedback)
                pixmap = QPixmap(100, 30)
                pixmap.fill(QColor(52, 152, 219, 180))
                
                painter = QPainter(pixmap)
                painter.setPen(QPen(QColor(255, 255, 255)))
                painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
                
                # Get component name for display
                user_data = current_item.data(0, Qt.ItemDataRole.UserRole)
                if user_data:
                    category, component, comp_data = user_data
                    painter.drawText(5, 20, f"{component}")
                
                painter.end()
                
                drag.setPixmap(pixmap)
                drag.setHotSpot(QPoint(50, 15))
                
                # Execute drag
                result = drag.exec(Qt.DropAction.CopyAction)
                print(f"🎯 Drag operation completed: {drag_data}")
        
        # Call original method as fallback
        super(QTreeWidget, self.tree).startDrag(supported_actions)


# Export
__all__ = ['ComponentPalette',
           'ComponentBubble', 'ComponentEncyclopedia']
