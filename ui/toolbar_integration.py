#this belongs in ui/ toolbar_integration.py

"""
Simple Integration for Horizontal Component Toolbar
Adds horizontal toolbar to existing Visual Retro System Emulator Builder
WITHOUT modifying existing main window structure
"""

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

def add_horizontal_toolbar_to_existing_window(main_window):
    """
    Add horizontal component toolbar to existing main window
    Preserves all existing functionality and layout
    """
    try:
        # Import the horizontal toolbar
        from ui.horizontal_component_toolbar import HorizontalComponentToolbar
        
        # Get the current central widget
        current_central = main_window.centralWidget()
        
        if current_central is None:
            print("⚠️ No central widget found - cannot add toolbar")
            return None
        
        # Create new central widget with vertical layout
        new_central = QWidget()
        new_layout = QVBoxLayout(new_central)
        new_layout.setContentsMargins(2, 2, 2, 2)
        new_layout.setSpacing(2)
        
        # Create and add horizontal toolbar
        toolbar = HorizontalComponentToolbar()
        new_layout.addWidget(toolbar)
        
        # Add existing central widget below toolbar
        new_layout.addWidget(current_central)
        
        # Set the new central widget
        main_window.setCentralWidget(new_central)
        
        # Connect toolbar signals to existing handlers if available
        if hasattr(main_window, '_on_component_selected_from_toolbar'):
            toolbar.component_selected.connect(main_window._on_component_selected_from_toolbar)
        elif hasattr(main_window, 'on_component_selected'):
            toolbar.component_selected.connect(main_window.on_component_selected)
        else:
            # Create default handler
            toolbar.component_selected.connect(
                lambda cat, comp: print(f"Component selected: {comp} from {cat}")
            )
        
        print("✅ Horizontal toolbar successfully added to existing window")
        return toolbar
        
    except ImportError as e:
        print(f"⚠️ Failed to add horizontal toolbar: {e}")
        return None

def create_enhanced_main_window_class(existing_main_window_class):
    """
    Create enhanced version of existing main window class
    Adds horizontal toolbar while preserving all existing functionality
    """
    
    class EnhancedMainWindow(existing_main_window_class):
        """Enhanced main window with horizontal component toolbar"""
        
        def __init__(self):
            # Initialize parent class first
            super().__init__()
            
            # Add horizontal toolbar after parent initialization
            self.horizontal_toolbar = add_horizontal_toolbar_to_existing_window(self)
            
            print("✅ Enhanced main window with horizontal toolbar created")
        
        def _on_component_selected_from_toolbar(self, category, component_name):
            """Handle component selection from horizontal toolbar"""
            print(f"Toolbar component selected: {component_name} (Category: {category})")
            
            # Try to add to canvas if available
            if hasattr(self, 'canvas') and self.canvas:
                if hasattr(self.canvas, 'add_component'):
                    # Add to center of canvas view
                    view_center = self.canvas.mapToScene(self.canvas.viewport().rect().center())
                    self.canvas.add_component(component_name, category, view_center)
                    print(f"✅ Added {component_name} to canvas")
            
            # Try to update component palette if available
            if hasattr(self, 'component_palette') and self.component_palette:
                if hasattr(self.component_palette, 'select_component'):
                    self.component_palette.select_component(category, component_name)
        
        def get_horizontal_toolbar(self):
            """Get reference to horizontal toolbar"""
            return getattr(self, 'horizontal_toolbar', None)
    
    return EnhancedMainWindow

# Convenience function for easy integration
def integrate_horizontal_toolbar(main_window_class=None):
    """
    Integrate horizontal toolbar with existing or new main window
    
    Usage:
        # Option 1: Add to existing window instance
        toolbar = add_horizontal_toolbar_to_existing_window(my_window)
        
        # Option 2: Create enhanced class
        EnhancedMainWindow = integrate_horizontal_toolbar(MyMainWindowClass)
        window = EnhancedMainWindow()
    """
    if main_window_class is None:
        # Return the integration function for existing instances
        return add_horizontal_toolbar_to_existing_window
    else:
        # Return enhanced class
        return create_enhanced_main_window_class(main_window_class)

# Example usage for your project
def integrate_with_visual_retro_emulator():
    """
    Specific integration for Visual Retro System Emulator Builder
    """
    try:
        # Try to import your existing main window
        from ui.main_window import MainWindow
        
        # Create enhanced version
        EnhancedMainWindow = create_enhanced_main_window_class(MainWindow)
        
        print("✅ Visual Retro Emulator integration ready")
        print("   Use EnhancedMainWindow instead of MainWindow")
        
        return EnhancedMainWindow
        
    except ImportError as e:
        print(f"⚠️ Could not integrate with existing main window: {e}")
        print("   Use add_horizontal_toolbar_to_existing_window() manually")
        return None

if __name__ == "__main__":
    # Test integration
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Test with Visual Retro Emulator
    EnhancedMainWindow = integrate_with_visual_retro_emulator()
    
    if EnhancedMainWindow:
        window = EnhancedMainWindow()
        window.show()
        
        print("🚀 Enhanced Visual Retro Emulator with horizontal toolbar running!")
        sys.exit(app.exec())
    else:
        print("❌ Integration failed")
