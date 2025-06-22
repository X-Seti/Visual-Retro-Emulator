
"""
Enhanced Component Image Viewer Widget
Shows realistic chip images in the component information dialog
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from pathlib import Path

class ComponentImageViewer(QWidget):
    """Widget for displaying realistic component images"""
    
    def __init__(self, component_def, parent=None):
        super().__init__(parent)
        self.component_def = component_def
        self._setup_ui()
        self._load_images()
    
    def _setup_ui(self):
        """Set up the image viewer UI"""
        layout = QVBoxLayout(self)
        
        # Package selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Package:"))
        
        self.package_combo = QComboBox()
        self.package_combo.currentTextChanged.connect(self._on_package_changed)
        selector_layout.addWidget(self.package_combo)
        
        layout.addLayout(selector_layout)
        
        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(200, 200)
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        layout.addWidget(self.image_label)
        
        # No image message
        self.no_image_label = QLabel("No image available")
        self.no_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_image_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.no_image_label)
    
    def _load_images(self):
        """Load available images for this component"""
        images_dir = Path("images/components")
        
        if not images_dir.exists():
            self._show_no_images()
            return
        
        # Look for images matching this component
        component_id = self.component_def.component_id.replace('_', '-')
        image_files = list(images_dir.glob(f"{component_id}_*.png"))
        
        if not image_files:
            self._show_no_images()
            return
        
        # Extract package types from filenames
        packages = []
        for image_file in image_files:
            parts = image_file.stem.split('_')
            if len(parts) >= 2:
                package_part = '_'.join(parts[1:])  # Everything after component name
                package = package_part.replace('_', '-').upper()
                packages.append((package, str(image_file)))
        
        if packages:
            self.package_combo.clear()
            for package, filepath in packages:
                self.package_combo.addItem(package, filepath)
            
            self.no_image_label.hide()
            self.image_label.show()
            self.package_combo.show()
            
            # Load first image
            self._on_package_changed(packages[0][0])
        else:
            self._show_no_images()
    
    def _show_no_images(self):
        """Show no images available state"""
        self.package_combo.hide()
        self.image_label.hide()
        self.no_image_label.show()
    
    def _on_package_changed(self, package_name):
        """Handle package selection change"""
        filepath = self.package_combo.currentData()
        if filepath and Path(filepath).exists():
            pixmap = QPixmap(filepath)
            if not pixmap.isNull():
                # Scale image to fit
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
            else:
                self.image_label.setText("Could not load image")
        else:
            self.image_label.setText("Image file not found")
