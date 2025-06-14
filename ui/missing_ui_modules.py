"""
X-Seti - June07 2025 - Missing UI Modules
Fallback implementations for missing UI components
"""

#this gpes in ui/
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                           QPushButton, QLabel, QStatusBar, QMenuBar, QMenu,
                           QTreeWidget, QTreeWidgetItem, QGraphicsView, 
                           QGraphicsScene, QGraphicsItem, QFrame, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush

class StatusBarManager:
    """Fallback status bar manager"""
    
    def __init__(self, status_bar: QStatusBar):
        self.status_bar = status_bar
        self.permanent_widgets = {}
        
    def show_message(self, message: str, timeout: int = 5000):
        """Show temporary message"""
        self.status_bar.showMessage(message, timeout)
        
    def set_permanent_message(self, key: str, message: str):
        """Set permanent status message"""
        if key not in self.permanent_widgets:
            label = QLabel()
            self.permanent_widgets[key] = label
            self.status_bar.addPermanentWidget(label)
        
        self.permanent_widgets[key].setText(message)
        
    def update_component_count(self, count: int):
        """Update component count display"""
        self.set_permanent_message('components', f'Components: {count}')
        
    def update_connection_count(self, count: int):
        """Update connection count display"""
        self.set_permanent_message('connections', f'Connections: {count}')

class MenuBarManager:
    """Fallback menu bar manager"""
    
    def __init__(self, menu_bar: QMenuBar, main_window):
        self.menu_bar = menu_bar
        self.main_window = main_window
        self.menus = {}
        self._create_menus()
        
    def _create_menus(self):
        """Create basic menu structure"""
        # File menu
        file_menu = self.menu_bar.addMenu('&File')
        self.menus['file'] = file_menu
        
        file_menu.addAction('&New Project', self._on_new_project)
        file_menu.addAction('&Open Project...', self._on_open_project)
        file_menu.addAction('&Save Project', self._on_save_project)
        file_menu.addSeparator()
        file_menu.addAction('E&xit', self.main_window.close)
        
        # Edit menu
        edit_menu = self.menu_bar.addMenu('&Edit')
        self.menus['edit'] = edit_menu
        
        edit_menu.addAction('&Undo', self._on_undo)
        edit_menu.addAction('&Redo', self._on_redo)
        edit_menu.addSeparator()
        edit_menu.addAction('&Copy', self._on_copy)
        edit_menu.addAction('&Paste', self._on_paste)
        
        # View menu
        view_menu = self.menu_bar.addMenu('&View')
        self.menus['view'] = view_menu
        
        view_menu.addAction('&Zoom In', self._on_zoom_in)
        view_menu.addAction('&Zoom Out', self._on_zoom_out)
        view_menu.addAction('&Fit to Window', self._on_fit_window)
        
        # Tools menu
        tools_menu = self.menu_bar.addMenu('&Tools')
        self.menus['tools'] = tools_menu
        
        tools_menu.addAction('&Preferences...', self._on_preferences)
        
        # Help menu
        help_menu = self.menu_bar.addMenu('&Help')
        self.menus['help'] = help_menu
        
        help_menu.addAction('&About', self._on_about)
        
    def _on_new_project(self):
        """New project handler"""
        if hasattr(self.main_window, 'project_manager'):
            self.main_window.project_manager.new_project()
            
    def _on_open_project(self):
        """Open project handler"""
        if hasattr(self.main_window, 'project_manager'):
            self.main_window.project_manager.open_project_dialog()
            
    def _on_save_project(self):
        """Save project handler"""
        if hasattr(self.main_window, 'project_manager'):
            self.main_window.project_manager.save_current_project()
            
    def _on_undo(self):
        """Undo handler"""
        print("Undo requested")
        
    def _on_redo(self):
        """Redo handler"""
        print("Redo requested")
        
    def _on_copy(self):
        """Copy handler"""
        print("Copy requested")
        
    def _on_paste(self):
        """Paste handler"""
        print("Paste requested")
        
    def _on_zoom_in(self):
        """Zoom in handler"""
        if hasattr(self.main_window, 'canvas'):
            self.main_window.canvas.zoom_in()
            
    def _on_zoom_out(self):
        """Zoom out handler"""
        if hasattr(self.main_window, 'canvas'):
            self.main_window.canvas.zoom_out()
            
    def _on_fit_window(self):
        """Fit to window handler"""
        if hasattr(self.main_window, 'canvas'):
            self.main_window.canvas.fit_in_view()
            
    def _on_preferences(self):
        """Preferences handler"""
        print("Preferences requested")
        
    def _on_about(self):
        """About dialog handler"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(self.main_window, "About", 
                         "Visual Retro System Emulator Builder\nVersion 1.0.0")

class PCBCanvas(QGraphicsView):
    """Basic PCB canvas implementation"""
    
    component_selected = pyqtSignal(object)
    component_moved = pyqtSignal(object, QPointF)
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Configure view
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Grid settings
        self.grid_size = 20
        self.show_grid = True
        
        # Component tracking
        self.components = {}
        self.connections = []
        
    def drawBackground(self, painter: QPainter, rect: QRectF):
        """Draw grid background"""
        super().drawBackground(painter, rect)
        
        if not self.show_grid:
            return
            
        # Draw grid
        painter.setPen(QPen(QColor(100, 100, 100), 0.5))
        
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        # Vertical lines
        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self.grid_size
            
        # Horizontal lines
        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self.grid_size
    
    def add_component(self, component_id: str, component_type: str, position: QPointF):
        """Add component to canvas"""
        # Create simple rectangle for component
        from PyQt6.QtWidgets import QGraphicsRectItem
        item = QGraphicsRectItem(0, 0, 60, 40)
        item.setBrush(QBrush(QColor(200, 200, 255)))
        item.setPen(QPen(QColor(0, 0, 0), 2))
        item.setPos(position)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        
        # Add text label
        from PyQt6.QtWidgets import QGraphicsTextItem
        text = QGraphicsTextItem(component_type, item)
        text.setPos(5, 10)
        
        self.scene.addItem(item)
        self.components[component_id] = item
        
        return item
    
    def remove_component(self, component_id: str):
        """Remove component from canvas"""
        if component_id in self.components:
            item = self.components[component_id]
            self.scene.removeItem(item)
            del self.components[component_id]
    
    def zoom_in(self):
        """Zoom in"""
        self.scale(1.25, 1.25)
        
    def zoom_out(self):
        """Zoom out"""
        self.scale(0.8, 0.8)
        
    def fit_in_view(self):
        """Fit scene in view"""
        self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

# Alias for backward compatibility
EnhancedPCBCanvas = PCBCanvas

class EnhancedComponentPalette(QWidget):
    """Component palette widget"""
    
    component_selected = pyqtSignal(str, str)  # component_type, component_name
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_components()
        
    def setup_ui(self):
        """Setup UI layout"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Component Palette")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Tree widget for components
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Components")
        self.tree.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.tree)
        
    def load_components(self):
        """Load component categories"""
        categories = {
            "CPUs": ["6502", "Z80", "68000", "8080"],
            "Memory": ["ROM", "RAM", "EEPROM"],
            "Graphics": ["TMS9918", "VIC-II", "PPU"],
            "Audio": ["SID", "AY-3-8910", "YM2612"],
            "I/O": ["PIA", "VIA", "UART"]
        }
        
        for category, components in categories.items():
            cat_item = QTreeWidgetItem(self.tree, [category])
            cat_item.setExpanded(True)
            
            for component in components:
                comp_item = QTreeWidgetItem(cat_item, [component])
                comp_item.setData(0, Qt.ItemDataRole.UserRole, (category, component))
    
    def _on_item_clicked(self, item, column):
        """Handle item click"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            category, component = data
            self.component_selected.emit(category, component)

class LayerControls(QWidget):
    """Layer controls widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        
        title = QLabel("Layers")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Layer buttons
        layers = ["Component", "PCB", "Gerber"]
        for layer in layers:
            btn = QPushButton(layer)
            btn.setCheckable(True)
            if layer == "Component":
                btn.setChecked(True)
            layout.addWidget(btn)
        
        layout.addStretch()

class PropertyEditor(QWidget):
    """Property editor widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        
        title = QLabel("Properties")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Placeholder for properties
        placeholder = QLabel("Select a component to view properties")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(placeholder)
        
        layout.addStretch()
