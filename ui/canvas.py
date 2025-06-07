"""
X-Seti - June07 2025 - Enhanced Canvas Implementation
Handles the main drawing area with component placement and interaction
"""

from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                            QMessageBox, QMenu, QGraphicsItem, QApplication)
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QPointF, QMimeData
from PyQt6.QtGui import (QPainter, QBrush, QColor, QPen, QDrag, QPixmap,
                        QTransform, QFont, QPolygonF)
import math
import json
from typing import List, Optional, Dict, Any

# Import our connection system
from connection_system import Connection, EnhancedConnection, connection_manager
from core.components import BaseComponent

# Check if we have a rendering module, otherwise create placeholder classes
try:
    from core.rendering import EnhancedHardwareComponent, LayerManager
except ImportError:
    # Create placeholder classes if rendering module doesn't exist
    class EnhancedHardwareComponent(BaseComponent):
        """Placeholder for enhanced hardware component"""
        def __init__(self, component_type: str, name: str = None, parent=None):
            super().__init__(component_type, name, parent)

        def setupComponent(self):
            """Setup component-specific properties and ports"""
            self.setRect(0, 0, 60, 40)

    class LayerManager:
        """Placeholder for layer manager"""
        def __init__(self):
            self.layers = {}

        def add_layer(self, name: str, visible: bool = True):
            self.layers[name] = visible

        def get_layer_visibility(self, name: str) -> bool:
            return self.layers.get(name, True)


class SelectionRectangle(QGraphicsRectItem):
    """Visual selection rectangle for multi-select operations"""
    
    def __init__(self):
        super().__init__()
        self.setPen(QPen(QColor(0, 120, 255, 150), 2, Qt.PenStyle.DashLine))
        self.setBrush(QBrush(QColor(0, 120, 255, 30)))
        self.setZValue(1000)  # Always on top


class EnhancedPCBCanvas(QGraphicsView):
    """Enhanced canvas with hotkey support and improved selection"""
    
    # Signals for communicating with main window
    selectionChanged = pyqtSignal()
    componentsDeleted = pyqtSignal(int)
    
    def __init__(self):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        
        # Set up scene
        self.scene.setSceneRect(0, 0, 2000, 2000)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
        # Layer management
        self.layer_manager = LayerManager()
        self.current_layer = "chip"
        
        # Selection management
        self.selected_components = []
        self.selection_rectangle = None
        self.selection_start = None
        self.is_selecting = False
        
        # Clipboard for copy/paste
        self.clipboard_components = []
        
        # Setup appearance and interactions
        self._update_layer_appearance("chip")
        self.setAcceptDrops(True)
        self.setRenderHint(self.RenderHint.Antialiasing)
        self.setMouseTracking(True)
        
        # Setup hotkeys
        self._setup_hotkeys()
        
        # Connect scene selection changes
        self.scene.selectionChanged.connect(self._on_selection_changed)
    
    def _setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        # Delete selected components
        self.delete_shortcut = QShortcut(QKeySequence.StandardKey.Delete, self)
        self.delete_shortcut.activated.connect(self._delete_selected)
        
        # Alternative delete key
        self.delete_shortcut2 = QShortcut(QKeySequence("Backspace"), self)
        self.delete_shortcut2.activated.connect(self._delete_selected)
        
        # Copy/paste operations
        self.copy_shortcut = QShortcut(QKeySequence.StandardKey.Copy, self)
        self.copy_shortcut.activated.connect(self._copy_selected)
        
        self.paste_shortcut = QShortcut(QKeySequence.StandardKey.Paste, self)
        self.paste_shortcut.activated.connect(self._paste_components)
        
        self.cut_shortcut = QShortcut(QKeySequence.StandardKey.Cut, self)
        self.cut_shortcut.activated.connect(self._cut_selected)
        
        # Selection operations
        self.select_all_shortcut = QShortcut(QKeySequence.StandardKey.SelectAll, self)
        self.select_all_shortcut.activated.connect(self._select_all)
        
        self.duplicate_shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        self.duplicate_shortcut.activated.connect(self._duplicate_selected)
        
        # Clear selection
        self.escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        self.escape_shortcut.activated.connect(self._clear_selection)
    
    def _on_selection_changed(self):
        """Handle scene selection changes"""
        # Update our internal selection list
        self.selected_components = [
            item for item in self.scene.selectedItems() 
            if isinstance(item, EnhancedHardwareComponent)
        ]
        
        # Emit signal for main window
        self.selectionChanged.emit()
        
        # Update status message
        count = len(self.selected_components)
        if hasattr(self, 'parent') and hasattr(self.parent(), 'status_manager'):
            if count == 0:
                self.parent().status_manager.set_message("No components selected")
            elif count == 1:
                comp_name = self.selected_components[0].name
                self.parent().status_manager.set_message(f"Selected: {comp_name}")
            else:
                self.parent().status_manager.set_message(f"Selected: {count} components")
    
    # ========== SELECTION OPERATIONS ==========
    
    def _delete_selected(self):
        """Delete selected components (Delete/Backspace key)"""
        if not self.selected_components:
            return
        
        # Confirm deletion if multiple components
        if len(self.selected_components) > 1:
            reply = QMessageBox.question(
                self, 
                "Delete Components",
                f"Delete {len(self.selected_components)} selected components?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Delete components
        deleted_count = 0
        for component in self.selected_components.copy():
            self._delete_component(component, confirm=False)
            deleted_count += 1
        
        # Clear selection
        self.selected_components.clear()
        
        # Emit signal
        self.componentsDeleted.emit(deleted_count)
        
        print(f"✓ Deleted {deleted_count} component(s)")
    
    def _copy_selected(self):
        """Copy selected components to clipboard (Ctrl+C)"""
        if not self.selected_components:
            return
        
        self.clipboard_components = []
        
        for component in self.selected_components:
            # Store component data for copying
            comp_data = {
                'component_def': component.component_def,
                'package_type': component.package_type,
                'position': component.pos(),
                'properties': getattr(component, 'properties', {}),
                'layer': component.layer if hasattr(component, 'layer') else self.current_layer
            }
            self.clipboard_components.append(comp_data)
        
        print(f"✓ Copied {len(self.clipboard_components)} component(s) to clipboard")
    
    def _paste_components(self):
        """Paste components from clipboard (Ctrl+V)"""
        if not self.clipboard_components:
            return
        
        # Clear current selection
        self.scene.clearSelection()
        self.selected_components.clear()
        
        # Paste components with slight offset
        offset_x, offset_y = 20, 20
        pasted_components = []
        
        for comp_data in self.clipboard_components:
            try:
                # Create new component
                component = EnhancedHardwareComponent(
                    comp_data['component_def'],
                    comp_data['package_type'],
                    comp_data['layer']
                )
                
                # Set position with offset
                new_pos = comp_data['position'] + QPointF(offset_x, offset_y)
                component.setPos(new_pos)
                
                # Restore properties
                if 'properties' in comp_data:
                    if hasattr(component, 'properties'):
                        component.properties.update(comp_data['properties'])
                
                # Add to scene
                self.scene.addItem(component)
                self.layer_manager.add_component(component)
                
                # Select the new component
                component.setSelected(True)
                pasted_components.append(component)
                
            except Exception as e:
                print(f"Error pasting component: {e}")
        
        # Update selection list
        self.selected_components = pasted_components
        
        print(f"✓ Pasted {len(pasted_components)} component(s)")
    
    def _cut_selected(self):
        """Cut selected components (Ctrl+X)"""
        if not self.selected_components:
            return
        
        # Copy first, then delete
        self._copy_selected()
        self._delete_selected()
        
        print(f"✓ Cut {len(self.clipboard_components)} component(s)")
    
    def _select_all(self):
        """Select all components (Ctrl+A)"""
        components = [
            item for item in self.scene.items() 
            if isinstance(item, EnhancedHardwareComponent)
        ]
        
        # Clear current selection
        self.scene.clearSelection()
        
        # Select all components
        for component in components:
            component.setSelected(True)
        
        print(f"✓ Selected all {len(components)} components")
    
    def _duplicate_selected(self):
        """Duplicate selected components (Ctrl+D)"""
        if not self.selected_components:
            return
        
        # Copy and immediately paste
        self._copy_selected()
        self._paste_components()
        
        print(f"✓ Duplicated {len(self.selected_components)} component(s)")
    
    def _clear_selection(self):
        """Clear selection (Escape key)"""
        self.scene.clearSelection()
        self.selected_components.clear()
        print("✓ Selection cleared")
    
    # ========== MOUSE INTERACTION ==========
    
    def mousePressEvent(self, event):
        """Enhanced mouse press with selection support"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if clicking on a component
            item = self.itemAt(event.position().toPoint())
            
            if isinstance(item, EnhancedHardwareComponent):
                # Component clicked
                if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                    # Clear selection unless Ctrl is held
                    if not item.isSelected():
                        self.scene.clearSelection()
                
                # Select/deselect the item
                item.setSelected(not item.isSelected() if event.modifiers() & Qt.KeyboardModifier.ControlModifier else True)
                
            else:
                # Empty space clicked - start selection rectangle
                if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                    self.scene.clearSelection()
                
                # Start selection rectangle
                self.selection_start = self.mapToScene(event.position().toPoint())
                self.is_selecting = True
        
        elif event.button() == Qt.MouseButton.RightButton:
            # Right click - context menu
            item = self.itemAt(event.position().toPoint())
            if isinstance(item, EnhancedHardwareComponent):
                # Select the item if not already selected
                if not item.isSelected():
                    self.scene.clearSelection()
                    item.setSelected(True)
                
                self._show_context_menu(item, event.globalPosition().toPoint())
                return
            else:
                # Right click on empty space
                self._show_canvas_context_menu(event.globalPosition().toPoint())
                return
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for selection rectangle"""
        if self.is_selecting and self.selection_start:
            current_pos = self.mapToScene(event.position().toPoint())
            
            # Create or update selection rectangle
            if not self.selection_rectangle:
                self.selection_rectangle = SelectionRectangle()
                self.scene.addItem(self.selection_rectangle)
            
            # Update rectangle
            rect = QRectF(self.selection_start, current_pos).normalized()
            self.selection_rectangle.setRect(rect)
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release for selection"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            if self.selection_rectangle:
                # Select items within rectangle
                rect = self.selection_rectangle.rect()
                items_in_rect = [
                    item for item in self.scene.items(rect)
                    if isinstance(item, EnhancedHardwareComponent)
                ]
                
                # Select items
                for item in items_in_rect:
                    item.setSelected(True)
                
                # Remove selection rectangle
                self.scene.removeItem(self.selection_rectangle)
                self.selection_rectangle = None
            
            self.is_selecting = False
            self.selection_start = None
        
        super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event):
        """Handle additional key presses"""
        # Arrow keys for fine movement
        if self.selected_components and event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right]:
            step = 10 if event.modifiers() & Qt.KeyboardModifier.ShiftModifier else 1
            
            for component in self.selected_components:
                pos = component.pos()
                if event.key() == Qt.Key.Key_Up:
                    pos.setY(pos.y() - step)
                elif event.key() == Qt.Key.Key_Down:
                    pos.setY(pos.y() + step)
                elif event.key() == Qt.Key.Key_Left:
                    pos.setX(pos.x() - step)
                elif event.key() == Qt.Key.Key_Right:
                    pos.setX(pos.x() + step)
                
                component.setPos(pos)
            
            return
        
        super().keyPressEvent(event)
    
    # ========== CONTEXT MENUS ==========
    
    def _show_context_menu(self, component, global_pos):
        """Show enhanced context menu for component"""
        menu = QMenu()
        
        # Properties action
        props_action = menu.addAction("🔧 Properties...")
        props_action.triggered.connect(lambda: show_component_properties(component, self))
        
        # CHIP EDITOR ACTION
        edit_action = menu.addAction("✏️ Edit Chip...")
        edit_action.triggered.connect(lambda: self._edit_component_chip(component))
        
        menu.addSeparator()
        
        # Copy action
        copy_action = menu.addAction("📋 Copy")
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self._copy_selected)
        
        # Cut action
        cut_action = menu.addAction("✂️ Cut")
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self._cut_selected)
        
        # Duplicate action
        duplicate_action = menu.addAction("📑 Duplicate")
        duplicate_action.setShortcut(QKeySequence("Ctrl+D"))
        duplicate_action.triggered.connect(self._duplicate_selected)
        
        menu.addSeparator()
        
        # Rotate actions
        rotate_cw_action = menu.addAction("↻ Rotate 90° CW")
        rotate_cw_action.triggered.connect(lambda: self._rotate_selected(90))
        
        rotate_ccw_action = menu.addAction("↺ Rotate 90° CCW")
        rotate_ccw_action.triggered.connect(lambda: self._rotate_selected(-90))
        
        menu.addSeparator()
        
        # Delete action
        delete_action = menu.addAction("🗑️ Delete")
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self._delete_selected)
        
        menu.exec(global_pos)
    
    def _edit_component_chip(self, component):
        """Edit the component's chip definition"""
        if hasattr(component, 'component_def'):
            # Get parent main window
            main_window = self.window()
            if hasattr(main_window, '_edit_selected_chip'):
                main_window._edit_selected_chip()
    
    def _show_canvas_context_menu(self, global_pos):
        """Show context menu for empty canvas area"""
        menu = QMenu()
        
        # NEW CHIP ACTION
        new_chip_action = menu.addAction("🆕 New Chip...")
        new_chip_action.triggered.connect(self._create_new_chip)
        
        menu.addSeparator()
        
        # Paste action
        paste_action = menu.addAction("📋 Paste")
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.setEnabled(len(self.clipboard_components) > 0)
        paste_action.triggered.connect(self._paste_components)
        
        menu.addSeparator()
        
        # Select all action
        select_all_action = menu.addAction("🔘 Select All")
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self._select_all)
        
        menu.addSeparator()
        
        # Layer switching
        layer_menu = menu.addMenu("📋 Switch Layer")
        
        chip_action = layer_menu.addAction("🔌 Chip Placement")
        chip_action.triggered.connect(lambda: self._switch_layer("chip"))
        
        pcb_action = layer_menu.addAction("🖨️ PCB Layout")
        pcb_action.triggered.connect(lambda: self._switch_layer("pcb"))
        
        gerber_action = layer_menu.addAction("🏭 Gerber/Manufacturing")
        gerber_action.triggered.connect(lambda: self._switch_layer("gerber"))
        
        menu.exec(global_pos)
    
    def _create_new_chip(self):
        """Create a new chip component"""
        main_window = self.window()
        if hasattr(main_window, '_open_chip_editor'):
            main_window._open_chip_editor()
    
    # ========== COMPONENT OPERATIONS ==========
    
    def _rotate_selected(self, angle):
        """Rotate selected components"""
        for component in self.selected_components:
            current_rotation = component.rotation()
            component.setRotation(current_rotation + angle)
        
        print(f"✓ Rotated {len(self.selected_components)} component(s) by {angle}°")
    
    def _switch_layer(self, layer_name):
        """Switch to different layer"""
        main_window = self.window()
        if hasattr(main_window, 'layer_controls'):
            if layer_name == "chip":
                main_window.layer_controls.chip_radio.setChecked(True)
            elif layer_name == "pcb":
                main_window.layer_controls.pcb_radio.setChecked(True)
            elif layer_name == "gerber":
                main_window.layer_controls.gerber_radio.setChecked(True)
            
            main_window.layer_controls._switch_layer(layer_name)
    
    def _delete_component(self, component, confirm=True):
        """Delete a single component"""
        if confirm:
            reply = QMessageBox.question(
                self, 
                "Delete Component",
                f"Delete {component.name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return False
        
        # Remove from layer manager
        self.layer_manager.remove_component(component)
        
        # Remove from scene
        self.scene.removeItem(component)
        
        # Remove from selection if present
        if component in self.selected_components:
            self.selected_components.remove(component)
        
        return True
    
    # ========== DRAG AND DROP ==========
    
    def dropEvent(self, event):
        """Enhanced drop event handling"""
        if event.mimeData().hasFormat("application/x-component"):
            try:
                data = event.mimeData().data("application/x-component").data().decode()
                component_id = data
                
                # Get component from retro database
                component_def = retro_database.get_component(component_id)
                
                if component_def:
                    # Create enhanced hardware component
                    pos = self.mapToScene(event.position().toPoint())
                    
                    # Determine package type
                    package_type = getattr(component_def, 'package_type', 'DIP-40')
                    
                    component = EnhancedHardwareComponent(
                        component_def, package_type, self.current_layer
                    )
                    component.setPos(pos.x(), pos.y())
                    
                    self.scene.addItem(component)
                    self.layer_manager.add_component(component)
                    
                    # Clear selection and select new component
                    self.scene.clearSelection()
                    component.setSelected(True)
                    
                    event.acceptProposedAction()
                    print(f"✓ Dropped component: {component_def.name}")
                else:
                    print(f"✗ Component not found: {component_id}")
            except Exception as e:
                print(f"Error dropping component: {e}")
    
    def dragEnterEvent(self, event):
        """Handle drag enter"""
        if event.mimeData().hasFormat("application/x-component"):
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        """Handle drag move"""
        if event.mimeData().hasFormat("application/x-component"):
            event.acceptProposedAction()
    
    # ========== LAYER MANAGEMENT ==========
    
    def _update_layer_appearance(self, layer_name):
        """Update canvas appearance for different layers"""
        self.current_layer = layer_name
        
        if layer_name == "chip":
            # Chip placement - neutral background with grid
            self.setStyleSheet("background-color: #f0f0f0;")
            self._draw_grid(QColor(200, 200, 200))
            
        elif layer_name == "pcb":
            # PCB layout - green background
            self.setStyleSheet("background-color: #2d5016;")
            self._draw_grid(QColor(100, 150, 50))
            
        else:  # gerber
            # Manufacturing - dark background
            self.setStyleSheet("background-color: #1a1a1a;")
            self._draw_grid(QColor(64, 64, 64))
    
    def _draw_grid(self, color):
        """Draw grid with specified color"""
        # Clear existing grid
        for item in self.scene.items():
            if hasattr(item, '_is_grid_line'):
                self.scene.removeItem(item)
        
        # Draw new grid
        grid_size = 20
        pen = QPen(color, 1)
        
        # Vertical lines
        for x in range(0, int(self.scene.width()), grid_size):
            line = self.scene.addLine(x, 0, x, self.scene.height(), pen)
            line._is_grid_line = True
        
        # Horizontal lines
        for y in range(0, int(self.scene.height()), grid_size):
            line = self.scene.addLine(0, y, self.scene.width(), y, pen)
            line._is_grid_line = True

# Add missing alias for compatibility
if 'EnhancedCanvas' not in globals():
    # Create alias to whatever your main canvas class is called
    # Look for something like: class PCBCanvas, class MainCanvas, etc.
    EnhancedCanvas = YourMainCanvasClass  # Replace with actual class name
