#!/usr/bin/env python3
"""
Pin Alignment Tool for Visual Retro System Emulator Builder
Fixes existing chip scaling and pin positioning issues
"""

import os
import sys
import re
import json
import math
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                           QListWidget, QListWidgetItem, QTextEdit, QProgressBar,
                           QGroupBox, QSpinBox, QDoubleSpinBox, QComboBox,
                           QCheckBox, QMessageBox, QFileDialog, QTabWidget,
                           QTableWidget, QTableWidgetItem, QSplitter,
                           QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                           QGraphicsEllipseItem, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QFont


class ChipAnalyzer:
    """Analyzes existing chip files and identifies scaling/positioning issues"""
    
    def __init__(self):
        self.issues_found = []
        self.chips_analyzed = []
        
        # Known good dimensions for reference
        self.reference_dimensions = {
            "DIP-8": {"width": 80, "height": 60, "pin_spacing": 8},
            "DIP-14": {"width": 80, "height": 80, "pin_spacing": 8},
            "DIP-16": {"width": 80, "height": 90, "pin_spacing": 8},
            "DIP-20": {"width": 80, "height": 110, "pin_spacing": 8},
            "DIP-24": {"width": 80, "height": 130, "pin_spacing": 8},
            "DIP-28": {"width": 80, "height": 150, "pin_spacing": 8},
            "DIP-40": {"width": 80, "height": 200, "pin_spacing": 8},
            "DIP-48": {"width": 100, "height": 200, "pin_spacing": 7},
            "DIP-64": {"width": 120, "height": 220, "pin_spacing": 6},
            "PLCC-44": {"width": 120, "height": 120, "pin_spacing": 6},
            "PLCC-68": {"width": 150, "height": 150, "pin_spacing": 5},
            "PLCC-84": {"width": 180, "height": 180, "pin_spacing": 5},
            "QFP-44": {"width": 100, "height": 100, "pin_spacing": 5},
            "QFP-68": {"width": 140, "height": 140, "pin_spacing": 4},
            "QFP-100": {"width": 140, "height": 140, "pin_spacing": 3},
        }
    
    def analyze_chip_file(self, filepath):
        """Analyze a single chip file for issues"""
        issues = []
        chip_data = {"filepath": str(filepath), "issues": []}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract chip metadata
            metadata = self._extract_metadata(content)
            chip_data.update(metadata)
            
            # Check for issues
            if self._check_scaling_issues(metadata):
                issues.append("Scaling issues detected")
            
            if self._check_pin_positioning_issues(content, metadata):
                issues.append("Pin positioning issues detected")
            
            if self._check_dimension_issues(metadata):
                issues.append("Dimension issues detected")
            
            if self._check_pin_count_mismatch(content, metadata):
                issues.append("Pin count mismatch detected")
            
            chip_data["issues"] = issues
            self.chips_analyzed.append(chip_data)
            
            if issues:
                self.issues_found.extend([{"file": filepath, "issue": issue} for issue in issues])
            
            return chip_data
            
        except Exception as e:
            error_data = {
                "filepath": str(filepath),
                "issues": [f"File read error: {str(e)}"],
                "error": True
            }
            self.chips_analyzed.append(error_data)
            return error_data
    
    def _extract_metadata(self, content):
        """Extract metadata from chip file content"""
        metadata = {}
        
        # Extract package type
        package_match = re.search(r'package_type.*?["\'](.*?)["\']', content)
        if package_match:
            metadata['package_type'] = package_match.group(1)
        
        # Extract dimensions
        width_match = re.search(r'width\s*=\s*(\d+)', content)
        if width_match:
            metadata['width'] = int(width_match.group(1))
        
        height_match = re.search(r'height\s*=\s*(\d+)', content)
        if height_match:
            metadata['height'] = int(height_match.group(1))
        
        # Extract component name
        name_match = re.search(r'ComponentDefinition\([^,]*,\s*["\'](.*?)["\']', content)
        if name_match:
            metadata['name'] = name_match.group(1)
        
        # Count add_pin calls
        pin_matches = re.findall(r'comp\.add_pin\([^)]+\)', content)
        metadata['pin_count'] = len(pin_matches)
        
        # Extract pin positions
        metadata['pin_positions'] = self._extract_pin_positions(content)
        
        return metadata
    
    def _extract_pin_positions(self, content):
        """Extract pin positions from add_pin calls"""
        positions = []
        
        # Look for add_pin calls with coordinates
        pin_pattern = r'comp\.add_pin\([^,]*,\s*(\d+),\s*(\d+)[^)]*\)'
        matches = re.findall(pin_pattern, content)
        
        for match in matches:
            x, y = int(match[0]), int(match[1])
            positions.append((x, y))
        
        return positions
    
    def _check_scaling_issues(self, metadata):
        """Check for scaling issues"""
        package_type = metadata.get('package_type')
        width = metadata.get('width')
        height = metadata.get('height')
        
        if not all([package_type, width, height]):
            return True  # Missing data is an issue
        
        if package_type in self.reference_dimensions:
            ref = self.reference_dimensions[package_type]
            
            # Check if dimensions are too far off
            width_ratio = width / ref['width']
            height_ratio = height / ref['height']
            
            # Flag if more than 50% off from reference
            if width_ratio < 0.5 or width_ratio > 2.0:
                return True
            if height_ratio < 0.5 or height_ratio > 2.0:
                return True
        
        return False
    
    def _check_pin_positioning_issues(self, content, metadata):
        """Check for pin positioning issues"""
        positions = metadata.get('pin_positions', [])
        package_type = metadata.get('package_type', '')
        
        if not positions:
            return True  # No positions found
        
        # Check for overlapping pins
        for i, pos1 in enumerate(positions):
            for j, pos2 in enumerate(positions[i+1:], i+1):
                if abs(pos1[0] - pos2[0]) < 2 and abs(pos1[1] - pos2[1]) < 2:
                    return True  # Pins too close
        
        # Check for pins outside chip boundaries
        width = metadata.get('width', 100)
        height = metadata.get('height', 100)
        
        for x, y in positions:
            if x < -20 or x > width + 20 or y < -20 or y > height + 20:
                return True  # Pin outside reasonable bounds
        
        return False
    
    def _check_dimension_issues(self, metadata):
        """Check for dimension issues"""
        width = metadata.get('width')
        height = metadata.get('height')
        package_type = metadata.get('package_type', '')
        
        if not width or not height:
            return True
        
        # Check for unreasonable dimensions
        if width < 20 or width > 1000 or height < 20 or height > 1000:
            return True
        
        # Check aspect ratio for DIP packages
        if package_type.startswith('DIP'):
            aspect_ratio = height / width
            if aspect_ratio < 0.5 or aspect_ratio > 10:  # DIP should be taller than wide
                return True
        
        return False
    
    def _check_pin_count_mismatch(self, content, metadata):
        """Check for pin count mismatches"""
        package_type = metadata.get('package_type', '')
        pin_count = metadata.get('pin_count', 0)
        
        # Extract expected pin count from package name
        if '-' in package_type:
            try:
                expected_pins = int(package_type.split('-')[1])
                if pin_count != expected_pins:
                    return True
            except (ValueError, IndexError):
                pass
        
        return False


class ChipFixEngine:
    """Engine for fixing chip scaling and pin positioning issues"""
    
    def __init__(self):
        self.analyzer = ChipAnalyzer()
    
    def fix_chip_file(self, filepath, fix_options):
        """Fix a single chip file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze current state
            metadata = self.analyzer._extract_metadata(content)
            
            # Apply fixes based on options
            new_content = content
            
            if fix_options.get('fix_dimensions', False):
                new_content = self._fix_dimensions(new_content, metadata)
            
            if fix_options.get('fix_pin_positions', False):
                new_content = self._fix_pin_positions(new_content, metadata)
            
            if fix_options.get('fix_pin_spacing', False):
                new_content = self._fix_pin_spacing(new_content, metadata)
            
            if fix_options.get('add_missing_pins', False):
                new_content = self._add_missing_pins(new_content, metadata)
            
            # Create backup
            if fix_options.get('create_backup', True):
                backup_path = str(filepath) + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Write fixed content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, "File fixed successfully"
            
        except Exception as e:
            return False, f"Error fixing file: {str(e)}"
    
    def _fix_dimensions(self, content, metadata):
        """Fix chip dimensions"""
        package_type = metadata.get('package_type')
        
        if package_type in self.analyzer.reference_dimensions:
            ref = self.analyzer.reference_dimensions[package_type]
            
            # Replace width
            content = re.sub(r'width\s*=\s*\d+', f'width={ref["width"]}', content)
            
            # Replace height
            content = re.sub(r'height\s*=\s*\d+', f'height={ref["height"]}', content)
        
        return content
    
    def _fix_pin_positions(self, content, metadata):
        """Fix pin positions"""
        package_type = metadata.get('package_type', '')
        pin_count = metadata.get('pin_count', 0)
        
        if not package_type or not pin_count:
            return content
        
        # Generate correct pin positions
        new_positions = self._generate_pin_positions(package_type, pin_count)
        
        # Replace add_pin calls
        def replace_pin(match):
            nonlocal position_index
            if position_index < len(new_positions):
                x, y = new_positions[position_index]
                position_index += 1
                
                # Extract pin name from original call
                original = match.group(0)
                name_match = re.search(r'add_pin\(\s*["\']([^"\']+)["\']', original)
                if name_match:
                    pin_name = name_match.group(1)
                else:
                    pin_name = f"Pin{position_index}"
                
                return f'comp.add_pin("{pin_name}", "{self._guess_pin_type(pin_name)}", {x}, {y})'
            
            return match.group(0)
        
        position_index = 0
        new_content = re.sub(r'comp\.add_pin\([^)]+\)', replace_pin, content)
        
        return new_content
    
    def _generate_pin_positions(self, package_type, pin_count):
        """Generate correct pin positions for a package"""
        positions = []
        
        if package_type in self.analyzer.reference_dimensions:
            ref = self.analyzer.reference_dimensions[package_type]
            width = ref['width']
            height = ref['height']
            spacing = ref['pin_spacing']
        else:
            # Default values
            width = 80
            height = 200
            spacing = 8
        
        if package_type.startswith('DIP'):
            # DIP packages
            pins_per_side = pin_count // 2
            
            # Left side pins
            for i in range(pins_per_side):
                x = 0
                y = 20 + i * spacing
                positions.append((x, y))
            
            # Right side pins (reverse order)
            for i in range(pins_per_side):
                x = width
                y = 20 + (pins_per_side - 1 - i) * spacing
                positions.append((x, y))
        
        elif package_type.startswith(('QFP', 'PLCC')):
            # Quad packages
            pins_per_side = pin_count // 4
            
            # Top side
            for i in range(pins_per_side):
                x = (width - (pins_per_side - 1) * spacing) / 2 + i * spacing
                y = 0
                positions.append((x, y))
            
            # Right side
            for i in range(pins_per_side):
                x = width
                y = (height - (pins_per_side - 1) * spacing) / 2 + i * spacing
                positions.append((x, y))
            
            # Bottom side (reverse)
            for i in range(pins_per_side):
                x = width - ((width - (pins_per_side - 1) * spacing) / 2 + i * spacing)
                y = height
                positions.append((x, y))
            
            # Left side (reverse)
            for i in range(pins_per_side):
                x = 0
                y = height - ((height - (pins_per_side - 1) * spacing) / 2 + i * spacing)
                positions.append((x, y))
        
        return positions
    
    def _fix_pin_spacing(self, content, metadata):
        """Fix pin spacing"""
        # This would involve recalculating all pin positions with proper spacing
        return self._fix_pin_positions(content, metadata)
    
    def _add_missing_pins(self, content, metadata):
        """Add missing pins"""
        package_type = metadata.get('package_type', '')
        current_pin_count = metadata.get('pin_count', 0)
        
        if '-' in package_type:
            try:
                expected_pins = int(package_type.split('-')[1])
                if current_pin_count < expected_pins:
                    # Generate positions for missing pins
                    all_positions = self._generate_pin_positions(package_type, expected_pins)
                    
                    # Add missing pins at the end
                    pin_additions = []
                    for i in range(current_pin_count, expected_pins):
                        x, y = all_positions[i]
                        pin_name = f"Pin{i+1}"
                        pin_type = "unused"
                        pin_additions.append(f'    comp.add_pin("{pin_name}", "{pin_type}", {x}, {y})')
                    
                    # Find the last add_pin call and add new pins after it
                    last_pin_match = None
                    for match in re.finditer(r'comp\.add_pin\([^)]+\)', content):
                        last_pin_match = match
                    
                    if last_pin_match:
                        insert_pos = last_pin_match.end()
                        new_pins = '\n' + '\n'.join(pin_additions)
                        content = content[:insert_pos] + new_pins + content[insert_pos:]
            
            except (ValueError, IndexError):
                pass
        
        return content
    
    def _guess_pin_type(self, pin_name):
        """Guess pin type from name"""
        name_upper = pin_name.upper()
        
        if name_upper in ['VCC', 'VDD', '+5V']:
            return 'power'
        elif name_upper in ['GND', 'VSS']:
            return 'ground'
        elif name_upper.startswith('CLK'):
            return 'clock'
        elif name_upper.startswith('A') and name_upper[1:].isdigit():
            return 'address'
        elif name_upper.startswith('D') and name_upper[1:].isdigit():
            return 'data'
        elif name_upper in ['RESET', 'RST']:
            return 'reset'
        else:
            return 'control'


class PinAlignmentTool(QMainWindow):
    """Main window for the pin alignment tool"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pin Alignment Tool - Retro System Emulator")
        self.setMinimumSize(1000, 700)
        
        self.analyzer = ChipAnalyzer()
        self.fix_engine = ChipFixEngine()
        self.components_dir = Path("components")
        
        self._create_ui()
        self._create_menu_bar()
        self._create_status_bar()
        
        # Auto-scan for components
        QTimer.singleShot(1000, self._auto_scan_components)
    
    def _create_ui(self):
        """Create the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Create tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Analysis tab
        analysis_tab = self._create_analysis_tab()
        self.tabs.addTab(analysis_tab, "Analysis")
        
        # Fix options tab
        fix_tab = self._create_fix_tab()
        self.tabs.addTab(fix_tab, "Fix Options")
        
        # Batch operations tab
        batch_tab = self._create_batch_tab()
        self.tabs.addTab(batch_tab, "Batch Operations")
        
        # Preview tab
        preview_tab = self._create_preview_tab()
        self.tabs.addTab(preview_tab, "Preview")
    
    def _create_analysis_tab(self):
        """Create analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Scan controls
        scan_group = QGroupBox("Component Scanning")
        scan_layout = QHBoxLayout(scan_group)
        
        self.scan_btn = QPushButton("Scan Components Directory")
        self.scan_btn.clicked.connect(self._scan_components)
        scan_layout.addWidget(self.scan_btn)
        
        self.components_dir_label = QLabel(f"Directory: {self.components_dir}")
        scan_layout.addWidget(self.components_dir_label)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_components_dir)
        scan_layout.addWidget(browse_btn)
        
        layout.addWidget(scan_group)
        
        # Results
        results_group = QGroupBox("Analysis Results")
        results_layout = QVBoxLayout(results_group)
        
        # Statistics
        self.stats_label = QLabel("No analysis performed yet")
        results_layout.addWidget(self.stats_label)
        
        # Issues list
        self.issues_list = QListWidget()
        self.issues_list.itemDoubleClicked.connect(self._show_issue_details)
        results_layout.addWidget(self.issues_list)
        
        layout.addWidget(results_group)
        
        return widget
    
    def _create_fix_tab(self):
        """Create fix options tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Fix options
        options_group = QGroupBox("Fix Options")
        options_layout = QVBoxLayout(options_group)
        
        self.fix_dimensions_cb = QCheckBox("Fix chip dimensions")
        self.fix_dimensions_cb.setChecked(True)
        self.fix_dimensions_cb.setToolTip("Correct chip width and height to standard values")
        options_layout.addWidget(self.fix_dimensions_cb)
        
        self.fix_pin_positions_cb = QCheckBox("Fix pin positions")
        self.fix_pin_positions_cb.setChecked(True)
        self.fix_pin_positions_cb.setToolTip("Recalculate and fix pin X,Y coordinates")
        options_layout.addWidget(self.fix_pin_positions_cb)
        
        self.fix_pin_spacing_cb = QCheckBox("Fix pin spacing")
        self.fix_pin_spacing_cb.setChecked(True)
        self.fix_pin_spacing_cb.setToolTip("Ensure proper spacing between pins")
        options_layout.addWidget(self.fix_pin_spacing_cb)
        
        self.add_missing_pins_cb = QCheckBox("Add missing pins")
        self.add_missing_pins_cb.setChecked(False)
        self.add_missing_pins_cb.setToolTip("Add pins if count doesn't match package type")
        options_layout.addWidget(self.add_missing_pins_cb)
        
        self.create_backup_cb = QCheckBox("Create backup files")
        self.create_backup_cb.setChecked(True)
        self.create_backup_cb.setToolTip("Create .backup files before making changes")
        options_layout.addWidget(self.create_backup_cb)
        
        layout.addWidget(options_group)
        
        # Package-specific settings
        package_group = QGroupBox("Package-Specific Settings")
        package_layout = QGridLayout(package_group)
        
        package_layout.addWidget(QLabel("DIP Pin Spacing:"), 0, 0)
        self.dip_spacing_spin = QSpinBox()
        self.dip_spacing_spin.setRange(4, 20)
        self.dip_spacing_spin.setValue(8)
        package_layout.addWidget(self.dip_spacing_spin, 0, 1)
        
        package_layout.addWidget(QLabel("QFP Pin Spacing:"), 1, 0)
        self.qfp_spacing_spin = QSpinBox()
        self.qfp_spacing_spin.setRange(2, 10)
        self.qfp_spacing_spin.setValue(5)
        package_layout.addWidget(self.qfp_spacing_spin, 1, 1)
        
        package_layout.addWidget(QLabel("Scale Factor:"), 2, 0)
        self.scale_factor_spin = QDoubleSpinBox()
        self.scale_factor_spin.setRange(0.1, 5.0)
        self.scale_factor_spin.setValue(1.0)
        self.scale_factor_spin.setSingleStep(0.1)
        package_layout.addWidget(self.scale_factor_spin, 2, 1)
        
        layout.addWidget(package_group)
        
        # Selected file actions
        actions_group = QGroupBox("Actions")
        actions_layout = QHBoxLayout(actions_group)
        
        self.fix_selected_btn = QPushButton("Fix Selected File")
        self.fix_selected_btn.clicked.connect(self._fix_selected_file)
        self.fix_selected_btn.setEnabled(False)
        actions_layout.addWidget(self.fix_selected_btn)
        
        self.preview_fix_btn = QPushButton("Preview Fix")
        self.preview_fix_btn.clicked.connect(self._preview_fix)
        self.preview_fix_btn.setEnabled(False)
        actions_layout.addWidget(self.preview_fix_btn)
        
        layout.addWidget(actions_group)
        
        return widget
    
    def _create_batch_tab(self):
        """Create batch operations tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Batch selection
        selection_group = QGroupBox("Batch Selection")
        selection_layout = QVBoxLayout(selection_group)
        
        # Filters
        filter_layout = QHBoxLayout()
        
        self.filter_by_package_cb = QCheckBox("Filter by package:")
        filter_layout.addWidget(self.filter_by_package_cb)
        
        self.package_filter_combo = QComboBox()
        self.package_filter_combo.addItems([
            "All", "DIP-40", "DIP-48", "DIP-64", "PLCC-44", "PLCC-68", "QFP-44", "QFP-68"
        ])
        filter_layout.addWidget(self.package_filter_combo)
        
        selection_layout.addLayout(filter_layout)
        
        # File list with checkboxes
        self.batch_files_list = QListWidget()
        self.batch_files_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        selection_layout.addWidget(self.batch_files_list)
        
        # Selection buttons
        selection_buttons = QHBoxLayout()
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self._select_all_batch)
        selection_buttons.addWidget(select_all_btn)
        
        select_none_btn = QPushButton("Select None")
        select_none_btn.clicked.connect(self._select_none_batch)
        selection_buttons.addWidget(select_none_btn)
        
        select_issues_btn = QPushButton("Select Files with Issues")
        select_issues_btn.clicked.connect(self._select_issues_batch)
        selection_buttons.addWidget(select_issues_btn)
        
        selection_layout.addLayout(selection_buttons)
        
        layout.addWidget(selection_group)
        
        # Batch actions
        batch_actions_group = QGroupBox("Batch Actions")
        batch_actions_layout = QHBoxLayout(batch_actions_group)
        
        self.batch_fix_btn = QPushButton("Fix Selected Files")
        self.batch_fix_btn.clicked.connect(self._batch_fix_files)
        batch_actions_layout.addWidget(self.batch_fix_btn)
        
        self.batch_analyze_btn = QPushButton("Re-analyze Selected")
        self.batch_analyze_btn.clicked.connect(self._batch_analyze_files)
        batch_actions_layout.addWidget(self.batch_analyze_btn)
        
        layout.addWidget(batch_actions_group)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return widget
    
    def _create_preview_tab(self):
        """Create preview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # File selection
        file_group = QGroupBox("File Preview")
        file_layout = QHBoxLayout(file_group)
        
        self.preview_file_combo = QComboBox()
        self.preview_file_combo.currentTextChanged.connect(self._update_preview)
        file_layout.addWidget(self.preview_file_combo)
        
        refresh_preview_btn = QPushButton("Refresh")
        refresh_preview_btn.clicked.connect(self._update_preview)
        file_layout.addWidget(refresh_preview_btn)
        
        layout.addWidget(file_group)
        
        # Before/After comparison
        comparison_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Before
        before_group = QGroupBox("Before Fix")
        before_layout = QVBoxLayout(before_group)
        self.before_text = QTextEdit()
        self.before_text.setReadOnly(True)
        self.before_text.setFont(QFont("Courier", 9))
        before_layout.addWidget(self.before_text)
        comparison_splitter.addWidget(before_group)
        
        # After
        after_group = QGroupBox("After Fix (Preview)")
        after_layout = QVBoxLayout(after_group)
        self.after_text = QTextEdit()
        self.after_text.setReadOnly(True)
        self.after_text.setFont(QFont("Courier", 9))
        after_layout.addWidget(self.after_text)
        comparison_splitter.addWidget(after_group)
        
        layout.addWidget(comparison_splitter)
        
        return widget
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_dir_action = file_menu.addAction("Open Components Directory...")
        open_dir_action.triggered.connect(self._browse_components_dir)
        
        file_menu.addSeparator()
        
        export_report_action = file_menu.addAction("Export Analysis Report...")
        export_report_action.triggered.connect(self._export_analysis_report)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        validate_fixes_action = tools_menu.addAction("Validate All Fixes")
        validate_fixes_action.triggered.connect(self._validate_all_fixes)
        
        restore_backups_action = tools_menu.addAction("Restore from Backups...")
        restore_backups_action.triggered.connect(self._restore_from_backups)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self._show_about)
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_label = QLabel("Ready")
        self.statusBar().addWidget(self.status_label)
        
        self.files_label = QLabel("Files: 0")
        self.statusBar().addPermanentWidget(self.files_label)
        
        self.issues_label = QLabel("Issues: 0")
        self.statusBar().addPermanentWidget(self.issues_label)
    
    def _auto_scan_components(self):
        """Auto-scan components directory if it exists"""
        if self.components_dir.exists():
            self._scan_components()
    
    def _browse_components_dir(self):
        """Browse for components directory"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Components Directory", str(self.components_dir)
        )
        
        if directory:
            self.components_dir = Path(directory)
            self.components_dir_label.setText(f"Directory: {self.components_dir}")
            self._scan_components()
    
    def _scan_components(self):
        """Scan components directory for chip files"""
        if not self.components_dir.exists():
            QMessageBox.warning(self, "Directory Not Found", 
                              f"Components directory not found: {self.components_dir}")
            return
        
        self.status_label.setText("Scanning components...")
        self.analyzer.chips_analyzed.clear()
        self.analyzer.issues_found.clear()
        
        # Find all Python files in subdirectories
        chip_files = []
        for subdir in self.components_dir.iterdir():
            if subdir.is_dir():
                for py_file in subdir.glob("*.py"):
                    if py_file.name != "__init__.py":
                        chip_files.append(py_file)
        
        # Analyze each file
        total_files = len(chip_files)
        for i, chip_file in enumerate(chip_files):
            self.status_label.setText(f"Analyzing {chip_file.name}... ({i+1}/{total_files})")
            QApplication.processEvents()
            
            self.analyzer.analyze_chip_file(chip_file)
        
        # Update UI
        self._update_analysis_results()
        self._populate_batch_files()
        self._populate_preview_files()
        
        self.status_label.setText("Analysis complete")
    
    def _update_analysis_results(self):
        """Update the analysis results display"""
        total_files = len(self.analyzer.chips_analyzed)
        files_with_issues = len([chip for chip in self.analyzer.chips_analyzed if chip.get('issues')])
        total_issues = len(self.analyzer.issues_found)
        
        # Update statistics
        stats_text = f"Analyzed {total_files} files, {files_with_issues} files have issues, {total_issues} total issues found"
        self.stats_label.setText(stats_text)
        
        # Update status bar
        self.files_label.setText(f"Files: {total_files}")
        self.issues_label.setText(f"Issues: {total_issues}")
        
        # Populate issues list
        self.issues_list.clear()
        for issue in self.analyzer.issues_found:
            file_path = issue['file']
            issue_desc = issue['issue']
            item_text = f"{file_path.name}: {issue_desc}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, issue)
            self.issues_list.addItem(item)
        
        # Enable/disable buttons
        has_files = total_files > 0
        self.fix_selected_btn.setEnabled(has_files)
        self.preview_fix_btn.setEnabled(has_files)
    
    def _populate_batch_files(self):
        """Populate the batch files list"""
        self.batch_files_list.clear()
        
        for chip in self.analyzer.chips_analyzed:
            filepath = chip['filepath']
            filename = Path(filepath).name
            
            # Create display text with issues indicator
            issues = chip.get('issues', [])
            if issues:
                display_text = f"❌ {filename} ({len(issues)} issues)"
            else:
                display_text = f"✅ {filename}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, chip)
            self.batch_files_list.addItem(item)
    
    def _populate_preview_files(self):
        """Populate the preview files dropdown"""
        self.preview_file_combo.clear()
        
        for chip in self.analyzer.chips_analyzed:
            filepath = chip['filepath']
            filename = Path(filepath).name
            self.preview_file_combo.addItem(filename, filepath)
    
    def _show_issue_details(self, item):
        """Show detailed information about an issue"""
        issue_data = item.data(Qt.ItemDataRole.UserRole)
        if issue_data:
            file_path = issue_data['file']
            issue_desc = issue_data['issue']
            
            # Find the chip data
            chip_data = None
            for chip in self.analyzer.chips_analyzed:
                if chip['filepath'] == str(file_path):
                    chip_data = chip
                    break
            
            if chip_data:
                details = f"File: {file_path}\n"
                details += f"Issue: {issue_desc}\n\n"
                details += f"Current Properties:\n"
                details += f"  Package Type: {chip_data.get('package_type', 'Unknown')}\n"
                details += f"  Dimensions: {chip_data.get('width', 'Unknown')} x {chip_data.get('height', 'Unknown')}\n"
                details += f"  Pin Count: {chip_data.get('pin_count', 'Unknown')}\n"
                
                QMessageBox.information(self, "Issue Details", details)
    
    def _get_fix_options(self):
        """Get current fix options"""
        return {
            'fix_dimensions': self.fix_dimensions_cb.isChecked(),
            'fix_pin_positions': self.fix_pin_positions_cb.isChecked(),
            'fix_pin_spacing': self.fix_pin_spacing_cb.isChecked(),
            'add_missing_pins': self.add_missing_pins_cb.isChecked(),
            'create_backup': self.create_backup_cb.isChecked(),
            'dip_spacing': self.dip_spacing_spin.value(),
            'qfp_spacing': self.qfp_spacing_spin.value(),
            'scale_factor': self.scale_factor_spin.value()
        }
    
    def _fix_selected_file(self):
        """Fix the selected file"""
        current_item = self.issues_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a file to fix")
            return
        
        issue_data = current_item.data(Qt.ItemDataRole.UserRole)
        if not issue_data:
            return
        
        file_path = Path(issue_data['file'])
        fix_options = self._get_fix_options()
        
        # Confirm fix
        reply = QMessageBox.question(
            self, "Confirm Fix",
            f"Fix file: {file_path.name}?\n\nThis will modify the file. "
            f"{'A backup will be created.' if fix_options['create_backup'] else 'No backup will be created.'}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.fix_engine.fix_chip_file(file_path, fix_options)
            
            if success:
                QMessageBox.information(self, "Fix Complete", f"Successfully fixed {file_path.name}")
                # Re-analyze the file
                self.analyzer.analyze_chip_file(file_path)
                self._update_analysis_results()
            else:
                QMessageBox.critical(self, "Fix Failed", f"Failed to fix {file_path.name}:\n{message}")
    
    def _preview_fix(self):
        """Preview what the fix would do"""
        current_item = self.issues_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a file to preview")
            return
        
        issue_data = current_item.data(Qt.ItemDataRole.UserRole)
        if not issue_data:
            return
        
        file_path = Path(issue_data['file'])
        
        # Set the preview tab to this file and switch to it
        for i in range(self.preview_file_combo.count()):
            if self.preview_file_combo.itemData(i) == str(file_path):
                self.preview_file_combo.setCurrentIndex(i)
                break
        
        self.tabs.setCurrentIndex(3)  # Switch to preview tab
        self._update_preview()
    
    def _update_preview(self):
        """Update the preview display"""
        current_file = self.preview_file_combo.currentData()
        if not current_file:
            return
        
        file_path = Path(current_file)
        
        try:
            # Load original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            self.before_text.setPlainText(original_content)
            
            # Generate preview of fixed content
            fix_options = self._get_fix_options()
            
            # Create a copy and apply fixes
            preview_content = original_content
            metadata = self.analyzer._extract_metadata(original_content)
            
            if fix_options['fix_dimensions']:
                preview_content = self.fix_engine._fix_dimensions(preview_content, metadata)
            
            if fix_options['fix_pin_positions']:
                preview_content = self.fix_engine._fix_pin_positions(preview_content, metadata)
            
            self.after_text.setPlainText(preview_content)
            
        except Exception as e:
            self.before_text.setPlainText(f"Error loading file: {str(e)}")
            self.after_text.setPlainText("")
    
    def _select_all_batch(self):
        """Select all files in batch list"""
        for i in range(self.batch_files_list.count()):
            self.batch_files_list.item(i).setSelected(True)
    
    def _select_none_batch(self):
        """Select no files in batch list"""
        self.batch_files_list.clearSelection()
    
    def _select_issues_batch(self):
        """Select only files with issues"""
        for i in range(self.batch_files_list.count()):
            item = self.batch_files_list.item(i)
            chip_data = item.data(Qt.ItemDataRole.UserRole)
            has_issues = bool(chip_data.get('issues'))
            item.setSelected(has_issues)
    
    def _batch_fix_files(self):
        """Fix all selected files in batch"""
        selected_items = self.batch_files_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select files to fix")
            return
        
        fix_options = self._get_fix_options()
        
        # Confirm batch fix
        reply = QMessageBox.question(
            self, "Confirm Batch Fix",
            f"Fix {len(selected_items)} selected files?\n\n"
            f"{'Backups will be created.' if fix_options['create_backup'] else 'No backups will be created.'}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self._perform_batch_fix(selected_items, fix_options)
    
    def _perform_batch_fix(self, selected_items, fix_options):
        """Perform the actual batch fix operation"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(selected_items))
        self.progress_bar.setValue(0)
        
        successful_fixes = 0
        failed_fixes = 0
        
        for i, item in enumerate(selected_items):
            chip_data = item.data(Qt.ItemDataRole.UserRole)
            file_path = Path(chip_data['filepath'])
            
            self.status_label.setText(f"Fixing {file_path.name}...")
            QApplication.processEvents()
            
            success, message = self.fix_engine.fix_chip_file(file_path, fix_options)
            
            if success:
                successful_fixes += 1
            else:
                failed_fixes += 1
                print(f"Failed to fix {file_path}: {message}")
            
            self.progress_bar.setValue(i + 1)
            QApplication.processEvents()
        
        self.progress_bar.setVisible(False)
        
        # Show results
        result_msg = f"Batch fix complete!\n\n"
        result_msg += f"Successfully fixed: {successful_fixes} files\n"
        result_msg += f"Failed to fix: {failed_fixes} files"
        
        QMessageBox.information(self, "Batch Fix Complete", result_msg)
        
        # Re-scan to update results
        self._scan_components()
        self.status_label.setText("Batch fix complete")
    
    def _batch_analyze_files(self):
        """Re-analyze selected files"""
        selected_items = self.batch_files_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select files to analyze")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(selected_items))
        self.progress_bar.setValue(0)
        
        for i, item in enumerate(selected_items):
            chip_data = item.data(Qt.ItemDataRole.UserRole)
            file_path = Path(chip_data['filepath'])
            
            self.status_label.setText(f"Analyzing {file_path.name}...")
            QApplication.processEvents()
            
            self.analyzer.analyze_chip_file(file_path)
            
            self.progress_bar.setValue(i + 1)
            QApplication.processEvents()
        
        self.progress_bar.setVisible(False)
        self._update_analysis_results()
        self.status_label.setText("Re-analysis complete")
    
    def _export_analysis_report(self):
        """Export analysis report to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Analysis Report", "analysis_report.txt", 
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Pin Alignment Tool - Analysis Report\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # Summary
                    total_files = len(self.analyzer.chips_analyzed)
                    files_with_issues = len([chip for chip in self.analyzer.chips_analyzed if chip.get('issues')])
                    f.write(f"Total files analyzed: {total_files}\n")
                    f.write(f"Files with issues: {files_with_issues}\n")
                    f.write(f"Total issues found: {len(self.analyzer.issues_found)}\n\n")
                    
                    # Detailed results
                    f.write("Detailed Results:\n")
                    f.write("-" * 20 + "\n\n")
                    
                    for chip in self.analyzer.chips_analyzed:
                        f.write(f"File: {chip['filepath']}\n")
                        f.write(f"Package: {chip.get('package_type', 'Unknown')}\n")
                        f.write(f"Dimensions: {chip.get('width', 'Unknown')} x {chip.get('height', 'Unknown')}\n")
                        f.write(f"Pin Count: {chip.get('pin_count', 'Unknown')}\n")
                        
                        issues = chip.get('issues', [])
                        if issues:
                            f.write(f"Issues: {', '.join(issues)}\n")
                        else:
                            f.write("Issues: None\n")
                        
                        f.write("\n")
                
                QMessageBox.information(self, "Export Complete", f"Report exported to {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export report: {str(e)}")
    
    def _validate_all_fixes(self):
        """Validate that all fixes were applied correctly"""
        # Re-scan and check if issues were resolved
        original_issues = len(self.analyzer.issues_found)
        self._scan_components()
        new_issues = len(self.analyzer.issues_found)
        
        msg = f"Validation complete!\n\n"
        msg += f"Issues before: {original_issues}\n"
        msg += f"Issues after: {new_issues}\n"
        msg += f"Issues resolved: {max(0, original_issues - new_issues)}"
        
        QMessageBox.information(self, "Validation Complete", msg)
    
    def _restore_from_backups(self):
        """Restore files from backup files"""
        backup_files = []
        
        # Find all .backup files
        if self.components_dir.exists():
            for subdir in self.components_dir.iterdir():
                if subdir.is_dir():
                    for backup_file in subdir.glob("*.backup"):
                        backup_files.append(backup_file)
        
        if not backup_files:
            QMessageBox.information(self, "No Backups", "No backup files found")
            return
        
        # Show restore dialog
        reply = QMessageBox.question(
            self, "Restore from Backups",
            f"Found {len(backup_files)} backup files. Restore all?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            restored = 0
            for backup_file in backup_files:
                try:
                    original_file = backup_file.with_suffix('')
                    backup_file.replace(original_file)
                    restored += 1
                except Exception as e:
                    print(f"Failed to restore {backup_file}: {e}")
            
            QMessageBox.information(self, "Restore Complete", f"Restored {restored} files from backups")
            self._scan_components()
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """Pin Alignment Tool for Visual Retro System Emulator Builder

This tool helps fix common issues with IC chip definitions:
• Incorrect chip dimensions and scaling
• Misaligned pin positions
• Improper pin spacing
• Missing pins

Features:
• Automatic analysis of chip files
• Batch fixing operations
• Before/after preview
• Backup creation
• Package-specific optimizations

Use this tool to ensure your retro computer chips are properly scaled and positioned for accurate emulation."""
        
        QMessageBox.about(self, "About Pin Alignment Tool", about_text)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    app.setApplicationName("Pin Alignment Tool")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("RetroEmu")
    
    try:
        window = PinAlignmentTool()
        window.show()
        
        print("✓ Pin Alignment Tool started successfully")
        print("Features:")
        print("  • Automatic chip file analysis")
        print("  • Scaling and positioning issue detection") 
        print("  • Batch fixing operations")
        print("  • Before/after preview")
        print("  • Backup file management")
        print("  • Package-specific optimizations")
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"✗ Error starting Pin Alignment Tool: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()