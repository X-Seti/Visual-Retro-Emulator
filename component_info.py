"""
X-Seti - May26, 2025 - Component Information Dialog
Displays comprehensive information for retro computer components with accurate package visualization
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                           QTextEdit, QLabel, QPushButton, QScrollArea,
                           QWidget, QFrame, QGroupBox, QGridLayout, QTableWidget,
                           QTableWidgetItem, QHeaderView, QSplitter, QTreeWidget,
                           QTreeWidgetItem, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QBrush
from rendering import ICPackage
import math


class ComponentInfoDialog(QDialog):
    """dialog displaying comprehensive component information with package visualization"""
    
    def __init__(self, component_def, parent=None):
        super().__init__(parent)
        self.component_def = component_def
        self.setWindowTitle(f"Component Information - {component_def.name}")
        self.setModal(True)
        self.resize(900, 700)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the enhanced dialog UI"""
        layout = QHBoxLayout(self)
        
        # Left side - Component visualization and basic info
        left_panel = QWidget()
        left_panel.setMaximumWidth(350)
        left_layout = QVBoxLayout(left_panel)
        
        # Component header
        self._create_component_header(left_layout)
        
        # Package visualization
        self._create_package_visualization(left_layout)
        
        # Pin information
        self._create_pin_info(left_layout)
        
        layout.addWidget(left_panel)
        
        # Right side - Detailed information tabs
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Tab widget for detailed information
        self.tab_widget = QTabWidget()
        
        # Create information tabs
        self._create_history_tab()
        self._create_technical_tab()
        self._create_systems_tab()
        self._create_variants_tab()
        self._create_development_tab()
        self._create_facts_tab()
        
        right_layout.addWidget(self.tab_widget)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        right_layout.addWidget(close_button)
        
        layout.addWidget(right_panel)
    
    def _create_component_header(self, layout):
        """Create the component header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.Box)
        header_frame.setStyleSheet("background-color: #f8f9fa; padding: 10px; border-radius: 5px;")
        header_layout = QVBoxLayout(header_frame)
        
        # Component name
        name_label = QLabel(self.component_def.name)
        name_font = QFont()
        name_font.setPointSize(16)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(name_label)
        
        # Category and package
        info_layout = QGridLayout()
        
        info_layout.addWidget(QLabel("Category:"), 0, 0)
        category_label = QLabel(self.component_def.category)
        category_label.setStyleSheet("font-weight: bold; color: #0066cc;")
        info_layout.addWidget(category_label, 0, 1)
        
        package_type = getattr(self.component_def, 'package_type', 'DIP-40')
        info_layout.addWidget(QLabel("Package:"), 1, 0)
        package_label = QLabel(package_type)
        package_label.setStyleSheet("font-weight: bold; color: #006600;")
        info_layout.addWidget(package_label, 1, 1)
        
        info_layout.addWidget(QLabel("Component ID:"), 2, 0)
        id_label = QLabel(self.component_def.component_id)
        id_label.setStyleSheet("font-family: monospace; color: #666;")
        info_layout.addWidget(id_label, 2, 1)
        
        header_layout.addLayout(info_layout)
        
        # Description
        desc_label = QLabel(self.component_def.description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-style: italic; color: #555; margin-top: 10px;")
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
    
    def _create_package_visualization(self, layout):
        """Create accurate package visualization"""
        viz_group = QGroupBox("Package Visualization")
        viz_layout = QVBoxLayout(viz_group)
        
        # Get package information
        package_type = getattr(self.component_def, 'package_type', 'DIP-40')
        package_info = ICPackage.get_package_info(package_type)
        
        # Create package pixmap
        scale_factor = 2.0  # Scale up for better visibility
        pixmap_width = int(package_info["width"] * scale_factor)
        pixmap_height = int(package_info["height"] * scale_factor)
        
        pixmap = QPixmap(pixmap_width, pixmap_height)
        pixmap.fill(QColor(245, 245, 245))
        
        self._draw_package_visualization(pixmap, package_info, scale_factor)
        
        # Display the visualization
        viz_label = QLabel()
        viz_label.setPixmap(pixmap)
        viz_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        viz_layout.addWidget(viz_label)
        
        # Package specifications
        specs_layout = QGridLayout()
        specs_layout.addWidget(QLabel("Package Type:"), 0, 0)
        specs_layout.addWidget(QLabel(package_type), 0, 1)
        
        specs_layout.addWidget(QLabel("Pin Count:"), 1, 0)
        specs_layout.addWidget(QLabel(str(package_info["pins"])), 1, 1)
        
        if "pin_spacing" in package_info:
            specs_layout.addWidget(QLabel("Pin Pitch:"), 2, 0)
            specs_layout.addWidget(QLabel(f"{package_info['pin_spacing']}mm"), 2, 1)
        
        viz_layout.addLayout(specs_layout)
        
        layout.addWidget(viz_group)
    
    def _draw_package_visualization(self, pixmap, package_info, scale_factor):
        """Draw accurate package visualization"""
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = package_info["width"] * scale_factor
        height = package_info["height"] * scale_factor
        
        # Draw package body
        package_color = QColor(40, 40, 40)  # Dark ceramic color
        painter.setBrush(QBrush(package_color))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawRect(10, 10, width-20, height-20)
        
        # Draw component label
        painter.setPen(QPen(Qt.GlobalColor.white))
        font = QFont("Arial", 8, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(15, 25, self.component_def.name)
        
        # Draw package type
        painter.setFont(QFont("Arial", 6))
        package_type = getattr(self.component_def, 'package_type', 'DIP-40')
        painter.drawText(15, height-15, package_type)
        
        # Draw pins
        pin_positions = ICPackage.calculate_pin_positions(package_type)
        
        for i, pin_pos in enumerate(pin_positions):
            # Scale pin position
            pin_x = pin_pos["x"] * scale_factor
            pin_y = pin_pos["y"] * scale_factor
            
            # Determine pin type and color
            pin_color = self._get_pin_color(i)
            
            # Draw pin
            painter.setBrush(QBrush(pin_color))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            
            if package_info.get("quad") or package_info.get("grid"):
                # Small square pins for surface mount
                painter.drawRect(pin_x-2, pin_y-2, 4, 4)
            else:
                # Round pins for through-hole
                painter.drawEllipse(pin_x-3, pin_y-3, 6, 6)
            
            # Draw pin number
            painter.setPen(QPen(Qt.GlobalColor.white))
            painter.setFont(QFont("Arial", 4))
            painter.drawText(pin_x-5, pin_y+10, str(pin_pos["number"]))
        
        # Draw pin 1 indicator (notch or dot)
        if package_type.startswith("DIP"):
            # Notch for DIP packages
            painter.setBrush(QBrush(Qt.GlobalColor.darkGray))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            notch_x = width * 0.15
            painter.drawEllipse(notch_x-5, 5, 10, 10)
        
        painter.end()
    
    def _get_pin_color(self, pin_index):
        """Get color for a pin based on its function"""
        # Try to match logical pins to physical pins
        if pin_index < len(self.component_def.pins):
            pin_def = self.component_def.pins[pin_index]
            pin_type = pin_def.get("type", "default")
            
            type_colors = {
                "power": QColor(255, 0, 0),      # Red
                "ground": QColor(0, 0, 0),       # Black
                "address": QColor(255, 165, 0),   # Orange
                "data": QColor(0, 100, 255),     # Blue
                "control": QColor(128, 0, 128),   # Purple
                "clock": QColor(0, 255, 0),      # Green
                "analog": QColor(255, 192, 203),  # Pink
                "video": QColor(255, 255, 0),    # Yellow
                "audio": QColor(0, 255, 255),    # Cyan
                "unused": QColor(128, 128, 128), # Gray
                "default": QColor(100, 100, 100) # Dark gray
            }
            
            return type_colors.get(pin_type, type_colors["default"])
        
        return QColor(100, 100, 100)  # Default gray
    
    def _create_pin_info(self, layout):
        """Create pin information table"""
        pin_group = QGroupBox("Pin Configuration")
        pin_layout = QVBoxLayout(pin_group)
        
        # Pin table
        self.pin_table = QTableWidget()
        self.pin_table.setColumnCount(4)
        self.pin_table.setHorizontalHeaderLabels(["Pin", "Name", "Type", "Direction"])
        
        # Populate pin table
        pins = self.component_def.pins
        self.pin_table.setRowCount(len(pins))
        
        for row, pin in enumerate(pins):
            self.pin_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.pin_table.setItem(row, 1, QTableWidgetItem(pin.get("name", "N/A")))
            self.pin_table.setItem(row, 2, QTableWidgetItem(pin.get("type", "N/A")))
            self.pin_table.setItem(row, 3, QTableWidgetItem(pin.get("direction", "N/A")))
            
            # Color code the type cell
            type_item = self.pin_table.item(row, 2)
            color = self._get_pin_color(row)
            type_item.setBackground(color)
        
        # Configure table
        self.pin_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header = self.pin_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.pin_table.setMaximumHeight(200)
        
        pin_layout.addWidget(self.pin_table)
        
        # Pin statistics
        stats_label = QLabel(f"Total Pins: {len(pins)}")
        stats_label.setStyleSheet("font-weight: bold; color: #666;")
        pin_layout.addWidget(stats_label)
        
        layout.addWidget(pin_group)
    
    def _create_history_tab(self):
        """Create the history information tab"""
        if not hasattr(self.component_def, 'history') or not self.component_def.history:
            return
        
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        history = self.component_def.history
        
        # Timeline visualization
        timeline_frame = QFrame()
        timeline_frame.setFrameStyle(QFrame.Shape.Box)
        timeline_frame.setStyleSheet("background-color: #f8f9fa; padding: 15px;")
        timeline_layout = QVBoxLayout(timeline_frame)
        
        if history.get('release_date'):
            date_label = QLabel(f"📅 Released: {history['release_date']}")
            date_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #0066cc;")
            timeline_layout.addWidget(date_label)
        
        if history.get('designed_by'):
            designer_label = QLabel(f"👨‍💻 Designed by: {history['designed_by']}")
            designer_label.setStyleSheet("font-size: 12px; color: #333;")
            timeline_layout.addWidget(designer_label)
        
        if history.get('discontinuation_date'):
            disc_label = QLabel(f"🚫 Discontinued: {history['discontinuation_date']}")
            disc_label.setStyleSheet("font-size: 12px; color: #cc6600;")
            timeline_layout.addWidget(disc_label)
        
        layout.addWidget(timeline_frame)
        
        # Development story
        if history.get('development_story'):
            story_group = QGroupBox("Development Story")
            story_layout = QVBoxLayout(story_group)
            
            story_text = QTextEdit()
            story_text.setPlainText(history['development_story'])
            story_text.setReadOnly(True)
            story_text.setMaximumHeight(200)
            story_layout.addWidget(story_text)
            
            layout.addWidget(story_group)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "📚 History")
    
    def _create_technical_tab(self):
        """Create the technical specifications tab"""
        if not hasattr(self.component_def, 'technical_specs') or not self.component_def.technical_specs:
            return
        
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        specs = self.component_def.technical_specs
        
        # Create specification groups
        spec_groups = {
            "General": [],
            "Performance": [],
            "Physical": [],
            "Electrical": []
        }
        
        # Categorize specifications
        for key, value in specs.items():
            key_lower = key.lower()
            if any(word in key_lower for word in ['transistor', 'process', 'die', 'size']):
                spec_groups["Physical"].append((key, value))
            elif any(word in key_lower for word in ['clock', 'speed', 'frequency', 'access', 'time']):
                spec_groups["Performance"].append((key, value))
            elif any(word in key_lower for word in ['voltage', 'power', 'current']):
                spec_groups["Electrical"].append((key, value))
            else:
                spec_groups["General"].append((key, value))
        
        # Create UI for each group
        for group_name, group_specs in spec_groups.items():
            if not group_specs:
                continue
            
            group_box = QGroupBox(group_name)
            group_layout = QGridLayout(group_box)
            
            for row, (key, value) in enumerate(group_specs):
                # Format the key nicely
                display_key = key.replace('_', ' ').title()
                
                key_label = QLabel(f"{display_key}:")
                key_label.setStyleSheet("font-weight: bold;")
                
                value_label = QLabel(str(value))
                value_label.setWordWrap(True)
                
                group_layout.addWidget(key_label, row, 0, Qt.AlignmentFlag.AlignTop)
                group_layout.addWidget(value_label, row, 1)
            
            layout.addWidget(group_box)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "🔧 Technical Specs")
    
    def _create_systems_tab(self):
        """Create the systems usage tab"""
        if not hasattr(self.component_def, 'used_in_systems') or not self.component_def.used_in_systems:
            return
        
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        systems = self.component_def.used_in_systems
        
        # Systems overview
        overview_label = QLabel(f"🖥️ Used in {len(systems)} different systems:")
        overview_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(overview_label)
        
        # Create system cards
        for system in systems:
            system_frame = QFrame()
            system_frame.setFrameStyle(QFrame.Shape.Box)
            system_frame.setStyleSheet("""
                QFrame {
                    background-color: #f0fff0; 
                    padding: 15px; 
                    margin: 5px;
                    border-radius: 8px;
                    border: 2px solid #90EE90;
                }
            """)
            
            system_layout = QVBoxLayout(system_frame)
            
            # System name
            name_label = QLabel(system['system'])
            name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #006400;")
            system_layout.addWidget(name_label)
            
            # Years and usage info
            info_layout = QHBoxLayout()
            
            if system.get('years'):
                years_label = QLabel(f"📅 {system['years']}")
                years_label.setStyleSheet("color: #666; font-size: 11px;")
                info_layout.addWidget(years_label)
            
            info_layout.addStretch()
            system_layout.addLayout(info_layout)
            
            # Notes
            if system.get('notes'):
                notes_label = QLabel(system['notes'])
                notes_label.setWordWrap(True)
                notes_label.setStyleSheet("margin-top: 8px; font-style: italic;")
                system_layout.addWidget(notes_label)
            
            layout.addWidget(system_frame)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "🖥️ Systems")
    
    def _create_variants_tab(self):
        """Create the variants tab"""
        if not hasattr(self.component_def, 'variants') or not self.component_def.variants:
            return
        
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        variants = self.component_def.variants
        
        variants_label = QLabel(f"🔄 {len(variants)} variants available:")
        variants_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(variants_label)
        
        for variant in variants:
            variant_frame = QFrame()
            variant_frame.setFrameStyle(QFrame.Shape.Box)
            variant_frame.setStyleSheet("""
                QFrame {
                    background-color: #fff8dc; 
                    padding: 12px; 
                    margin: 5px;
                    border-radius: 6px;
                    border: 1px solid #ddd;
                }
            """)
            
            variant_layout = QVBoxLayout(variant_frame)
            
            # Variant name and part number
            header_layout = QHBoxLayout()
            
            name_label = QLabel(variant['name'])
            name_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #8B4513;")
            header_layout.addWidget(name_label)
            
            if variant.get('part_number'):
                part_label = QLabel(f"P/N: {variant['part_number']}")
                part_label.setStyleSheet("color: #666; font-family: monospace; font-size: 10px;")
                header_layout.addWidget(part_label)
            
            header_layout.addStretch()
            variant_layout.addLayout(header_layout)
            
            # Differences
            if variant.get('differences'):
                diff_label = QLabel(variant['differences'])
                diff_label.setWordWrap(True)
                diff_label.setStyleSheet("margin-top: 5px;")
                variant_layout.addWidget(diff_label)
            
            layout.addWidget(variant_frame)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "🔄 Variants")
    
    def _create_development_tab(self):
        """Create the development information tab"""
        if not hasattr(self.component_def, 'development_info') or not self.component_def.development_info:
            return
        
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        dev_info = self.component_def.development_info
        
        # Development overview
        dev_label = QLabel("🏭 Development Information")
        dev_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(dev_label)
        
        # Development metrics
        metrics_group = QGroupBox("Project Metrics")
        metrics_layout = QGridLayout(metrics_group)
        
        dev_fields = [
            ('project_name', 'Project Name', '🎯'),
            ('team_size', 'Team Size', '👥'),
            ('development_time', 'Development Time', '⏱️'),
            ('cost_to_develop', 'Development Cost', '💰'),
            ('transistor_count', 'Transistor Count', '🔬'),
            ('die_size', 'Die Size', '📏'),
            ('process_node', 'Process Node', '⚙️')
        ]
        
        row = 0
        for field_key, field_label, icon in dev_fields:
            if dev_info.get(field_key):
                icon_label = QLabel(icon)
                icon_label.setStyleSheet("font-size: 16px;")
                metrics_layout.addWidget(icon_label, row, 0)
                
                key_label = QLabel(f"{field_label}:")
                key_label.setStyleSheet("font-weight: bold;")
                metrics_layout.addWidget(key_label, row, 1)
                
                value_label = QLabel(str(dev_info[field_key]))
                value_label.setWordWrap(True)
                metrics_layout.addWidget(value_label, row, 2)
                
                row += 1
        
        layout.addWidget(metrics_group)
        layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "🏭 Development")
    
    def _create_facts_tab(self):
        """Create the interesting facts tab"""
        if not hasattr(self.component_def, 'interesting_facts') or not self.component_def.interesting_facts:
            return
        
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        facts = self.component_def.interesting_facts
        
        facts_label = QLabel(f"💡 {len(facts)} Interesting Facts")
        facts_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(facts_label)
        
        for i, fact in enumerate(facts, 1):
            fact_frame = QFrame()
            fact_frame.setFrameStyle(QFrame.Shape.Box)
            fact_frame.setStyleSheet("""
                QFrame {
                    background-color: #f0f8ff; 
                    padding: 15px; 
                    margin: 8px;
                    border-radius: 8px;
                    border-left: 4px solid #1e90ff;
                }
            """)
            
            fact_layout = QHBoxLayout(fact_frame)
            
            # Fact number
            number_label = QLabel(f"{i}")
            number_label.setStyleSheet("""
                font-size: 18px; 
                font-weight: bold; 
                color: #1e90ff;
                min-width: 30px;
                text-align: center;
            """)
            fact_layout.addWidget(number_label)
            
            # Fact text
            fact_label = QLabel(fact)
            fact_label.setWordWrap(True)
            fact_label.setStyleSheet("font-size: 12px; line-height: 1.4;")
            fact_layout.addWidget(fact_label)
            
            layout.addWidget(fact_frame)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "💡 Fun Facts")


def show_enhanced_component_info(component_def, parent=None):
    """Convenience function to show enhanced component information"""
    dialog = ComponentInfoDialog(component_def, parent)
    dialog.exec()
