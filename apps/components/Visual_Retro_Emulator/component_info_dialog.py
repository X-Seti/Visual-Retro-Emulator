"""
X-Seti - May23 2025 - Component Information Dialog - Displays rich historical and technical information
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                           QTextEdit, QLabel, QPushButton, QScrollArea,
                           QWidget, QFrame, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor


class ComponentInfoDialog(QDialog):
    """Dialog displaying comprehensive component information"""
    
    def __init__(self, component_def, parent=None):
        super().__init__(parent)
        self.component_def = component_def
        self.setWindowTitle(f"Component Information - {component_def.name}")
        self.setModal(True)
        self.resize(800, 600)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the dialog UI with tabs for different information"""
        layout = QVBoxLayout(self)
        
        # Title section
        title_frame = QFrame()
        title_frame.setFrameStyle(QFrame.Shape.Box)
        title_layout = QHBoxLayout(title_frame)
        
        # Chip visualization (simple representation)
        chip_pixmap = self._create_chip_pixmap()
        chip_label = QLabel()
        chip_label.setPixmap(chip_pixmap)
        title_layout.addWidget(chip_label)
        
        # Basic info
        info_layout = QVBoxLayout()
        
        title_label = QLabel(self.component_def.name)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        info_layout.addWidget(title_label)
        
        category_label = QLabel(f"Category: {self.component_def.category}")
        info_layout.addWidget(category_label)
        
        desc_label = QLabel(self.component_def.description)
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        title_layout.addLayout(info_layout)
        title_layout.addStretch()
        
        layout.addWidget(title_frame)
        
        # Tab widget for detailed information
        self.tab_widget = QTabWidget()
        
        # History tab
        if hasattr(self.component_def, 'history') and self.component_def.history:
            self._create_history_tab()
        
        # Technical specs tab
        if hasattr(self.component_def, 'technical_specs') and self.component_def.technical_specs:
            self._create_technical_tab()
        
        # Interesting facts tab
        if hasattr(self.component_def, 'interesting_facts') and self.component_def.interesting_facts:
            self._create_facts_tab()
        
        # Systems tab
        if hasattr(self.component_def, 'used_in_systems') and self.component_def.used_in_systems:
            self._create_systems_tab()
        
        # Variants tab
        if hasattr(self.component_def, 'variants') and self.component_def.variants:
            self._create_variants_tab()
        
        # Development tab
        if hasattr(self.component_def, 'development_info') and self.component_def.development_info:
            self._create_development_tab()
        
        # Pin diagram tab
        self._create_pinout_tab()
        
        layout.addWidget(self.tab_widget)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
    
    def _create_chip_pixmap(self):
        """Create a visual representation of the chip"""
        width = self.component_def.width // 2
        height = self.component_def.height // 2
        
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(240, 240, 240))
        
        painter = QPainter(pixmap)
        painter.drawRect(0, 0, width-1, height-1)
        painter.drawText(10, height//2, self.component_def.name)
        painter.end()
        
        return pixmap
    
    def _create_history_tab(self):
        """Create the history tab"""
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        history = self.component_def.history
        
        if history.get('designed_by'):
            group = QGroupBox("Designer")
            group_layout = QVBoxLayout(group)
            label = QLabel(history['designed_by'])
            label.setWordWrap(True)
            group_layout.addWidget(label)
            layout.addWidget(group)
        
        if history.get('release_date'):
            group = QGroupBox("Release Date")
            group_layout = QVBoxLayout(group)
            label = QLabel(history['release_date'])
            group_layout.addWidget(label)
            layout.addWidget(group)
        
        if history.get('development_story'):
            group = QGroupBox("Development Story")
            group_layout = QVBoxLayout(group)
            text_edit = QTextEdit()
            text_edit.setPlainText(history['development_story'])
            text_edit.setMaximumHeight(150)
            group_layout.addWidget(text_edit)
            layout.addWidget(group)
        
        if history.get('discontinuation_date'):
            group = QGroupBox("Discontinuation Date")
            group_layout = QVBoxLayout(group)
            label = QLabel(history['discontinuation_date'])
            group_layout.addWidget(label)
            layout.addWidget(group)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "📚 History")
    
    def _create_technical_tab(self):
        """Create the technical specifications tab"""
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QGridLayout(content_widget)
        
        specs = self.component_def.technical_specs
        row = 0
        
        for key, value in specs.items():
            # Format the key nicely
            display_key = key.replace('_', ' ').title()
            
            key_label = QLabel(f"{display_key}:")
            key_label.setStyleSheet("font-weight: bold;")
            
            value_label = QLabel(str(value))
            value_label.setWordWrap(True)
            
            layout.addWidget(key_label, row, 0, Qt.AlignmentFlag.AlignTop)
            layout.addWidget(value_label, row, 1)
            row += 1
        
        layout.setRowStretch(row, 1)  # Add stretch at bottom
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "🔧 Technical Specs")
    
    def _create_facts_tab(self):
        """Create the interesting facts tab"""
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        facts = self.component_def.interesting_facts
        
        facts_label = QLabel("💡 Interesting Facts")
        facts_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(facts_label)
        
        for i, fact in enumerate(facts, 1):
            fact_frame = QFrame()
            fact_frame.setFrameStyle(QFrame.Shape.Box)
            fact_frame.setStyleSheet("background-color: #f0f8ff; padding: 10px; margin: 5px;")
            
            fact_layout = QVBoxLayout(fact_frame)
            
            fact_label = QLabel(f"{i}. {fact}")
            fact_label.setWordWrap(True)
            fact_layout.addWidget(fact_label)
            
            layout.addWidget(fact_frame)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "💡 Fun Facts")
    
    def _create_systems_tab(self):
        """Create the systems that used this chip tab"""
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        systems = self.component_def.used_in_systems
        
        systems_label = QLabel("🖥️ Systems Using This Chip")
        systems_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(systems_label)
        
        for system in systems:
            system_frame = QFrame()
            system_frame.setFrameStyle(QFrame.Shape.Box)
            system_frame.setStyleSheet("background-color: #f0fff0; padding: 10px; margin: 5px;")
            
            system_layout = QVBoxLayout(system_frame)
            
            name_label = QLabel(system['system'])
            name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
            system_layout.addWidget(name_label)
            
            if system.get('years'):
                years_label = QLabel(f"Years: {system['years']}")
                years_label.setStyleSheet("color: #666;")
                system_layout.addWidget(years_label)
            
            if system.get('notes'):
                notes_label = QLabel(system['notes'])
                notes_label.setWordWrap(True)
                notes_label.setStyleSheet("margin-top: 5px;")
                system_layout.addWidget(notes_label)
            
            layout.addWidget(system_frame)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "🖥️ Systems")
    
    def _create_variants_tab(self):
        """Create the component variants tab"""
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        variants = self.component_def.variants
        
        variants_label = QLabel("🔄 Component Variants")
        variants_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(variants_label)
        
        for variant in variants:
            variant_frame = QFrame()
            variant_frame.setFrameStyle(QFrame.Shape.Box)
            variant_frame.setStyleSheet("background-color: #fff8dc; padding: 10px; margin: 5px;")
            
            variant_layout = QVBoxLayout(variant_frame)
            
            name_label = QLabel(variant['name'])
            name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
            variant_layout.addWidget(name_label)
            
            if variant.get('part_number'):
                part_label = QLabel(f"Part Number: {variant['part_number']}")
                part_label.setStyleSheet("color: #666; font-family: monospace;")
                variant_layout.addWidget(part_label)
            
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
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QGridLayout(content_widget)
        
        dev_info = self.component_def.development_info
        row = 0
        
        dev_fields = [
            ('project_name', 'Project Name'),
            ('team_size', 'Team Size'),
            ('development_time', 'Development Time'),
            ('cost_to_develop', 'Development Cost'),
            ('transistor_count', 'Transistor Count'),
            ('die_size', 'Die Size'),
            ('process_node', 'Process Node')
        ]
        
        layout.addWidget(QLabel("🏭 Development Information"), row, 0, 1, 2)
        layout.itemAt(layout.count()-1).widget().setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        row += 1
        
        for field_key, field_label in dev_fields:
            if dev_info.get(field_key):
                key_label = QLabel(f"{field_label}:")
                key_label.setStyleSheet("font-weight: bold;")
                
                value_label = QLabel(str(dev_info[field_key]))
                value_label.setWordWrap(True)
                
                layout.addWidget(key_label, row, 0, Qt.AlignmentFlag.AlignTop)
                layout.addWidget(value_label, row, 1)
                row += 1
        
        layout.setRowStretch(row, 1)  # Add stretch at bottom
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "🏭 Development")
    
    def _create_pinout_tab(self):
        """Create the pinout diagram tab"""
        scroll_area = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        pinout_label = QLabel("📌 Pin Configuration")
        pinout_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(pinout_label)
        
        # Create a visual pinout representation
        pinout_frame = QFrame()
        pinout_frame.setFrameStyle(QFrame.Shape.Box)
        pinout_frame.setStyleSheet("background-color: white; padding: 20px;")
        pinout_layout = QVBoxLayout(pinout_frame)
        
        # Group pins by type for better organization
        pin_types = {}
        for pin in self.component_def.pins:
            pin_type = pin['type']
            if pin_type not in pin_types:
                pin_types[pin_type] = []
            pin_types[pin_type].append(pin)
        
        # Display pins grouped by type
        for pin_type, pins in pin_types.items():
            type_label = QLabel(f"{pin_type.upper()} Pins:")
            type_label.setStyleSheet("font-weight: bold; color: #333; margin-top: 10px;")
            pinout_layout.addWidget(type_label)
            
            pins_text = ", ".join([f"{pin['name']} ({pin['direction']})" for pin in pins])
            pins_label = QLabel(pins_text)
            pins_label.setWordWrap(True)
            pins_label.setStyleSheet("margin-left: 20px; margin-bottom: 5px;")
            pinout_layout.addWidget(pins_label)
        
        layout.addWidget(pinout_frame)
        layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        self.tab_widget.addTab(scroll_area, "📌 Pinout")


def show_component_info(component_def, parent=None):
    """Convenience function to show component information"""
    dialog = ComponentInfoDialog(component_def, parent)
    dialog.exec()
            
