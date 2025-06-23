#!/usr/bin/env python3
"""
X-Seti - June22 2025 - Canvas functionality
"""
#this belongs in ui/ canvas.py

import sys
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import json
import os

try:
    from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem, 
                               QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem,
                               QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsPathItem,
                               QApplication, QMenu, QMessageBox, QGraphicsProxyWidget,
                               QWidget, QVBoxLayout, QLabel, QPushButton)
    from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF, pyqtSignal, QTimer
    from PyQt6.QtGui import (QPen, QBrush, QColor, QPainter, QPolygonF, QFont, 
                           QCursor, QPainterPath, QPixmap, QDrag, QTransform)
    PYQT6_AVAILABLE = True
except ImportError as e:
    print(f"❌ PyQt6 import failed: {e}")
    PYQT6_AVAILABLE = False


        
    def __init__(self, position: QPointF, width: float, height: float, layer_name: str = "pcb"):
            super().__init__(layer_name)

    def _setup_canvas(self):
        """Setup canvas properties"""
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
    def _initialize_pin_numbers_support(self):
        """Initialize pin numbers support - call from Canvas __init__"""
    try:
        from .pin_numbers import add_pin_numbers_to_canvas

        # Add pin numbers manager to this canvas
        self.pin_numbers_manager = add_pin_numbers_to_canvas(self)

        print("✓ Pin numbers support added to canvas")

    except ImportError as e:
        print(f"⚠️ Pin numbers module not available: {e}")

        # Fallback methods
        self.pin_numbers_visible = True

    def fallback_set_pin_numbers_visible(visible):
        self.pin_numbers_visible = visible
        print(f"🔢 Pin numbers {visible} (fallback mode)")

    def fallback_get_pin_numbers_visible():
        return self.pin_numbers_visible

        self.set_pin_numbers_visible = fallback_set_pin_numbers_visible
        self.get_pin_numbers_visible = fallback_get_pin_numbers_visible


        # === GRID AND VIEW METHODS ===
        
    def set_grid_visible(self, visible: bool):
        """Set grid visibility"""
        self.grid_visible = visible
        self.scene.update()
        
    def set_grid_spacing(self, spacing: int):
        """Set grid spacing"""
        self.grid_spacing = spacing
        self.scene.update()
        
    def set_snap_to_grid(self, snap: bool):
        """Set snap to grid"""
        self.snap_to_grid = snap
        
    def zoom_in(self):
        """Zoom in"""
        self.scale(1.25, 1.25)
        self.zoom_factor *= 1.25
        self.zoom_changed.emit(self.zoom_factor)
        
    def zoom_out(self):
        """Zoom out"""
        self.scale(0.8, 0.8)
        self.zoom_factor *= 0.8
        self.zoom_changed.emit(self.zoom_factor)
        
    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.resetTransform()
        self.zoom_factor = 1.0
        self.zoom_changed.emit(self.zoom_factor)
        
    def fit_to_window(self):
        """Fit all items to window"""
        self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
        # Calculate zoom factor from transform
        transform = self.transform()
        self.zoom_factor = transform.m11()  # Get scale factor
        self.zoom_changed.emit(self.zoom_factor)
        

if __name__ == "__main__":
    # Test the canvas
    if PYQT6_AVAILABLE:
        app = QApplication(sys.argv)
        canvas.show()
        app.exec()
        print("✅ Canvas test completed")
    else:
        print("⚠️ Cannot test - PyQt6 not available")
