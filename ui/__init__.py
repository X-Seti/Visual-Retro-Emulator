#!/usr/bin/env python3
"""
X-Seti - June16 2025 - UI Package Init - Clean Components
Contains all clean user interface components with bubble tooltips and floating menus
"""

#this belongs in ui/__init__.py

import sys
import os

# ============================================================================
# CLEAN UI COMPONENTS - Primary imports
# ============================================================================

# Main Window - Clean version with floating menus
CleanMainWindow = None
try:
    from .main_window import CleanMainWindow, MainWindow, FixedMainWindow, EnhancedMainWindow
    print("✅ CleanMainWindow imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import CleanMainWindow: {e}")
    CleanMainWindow = None

# Component Palette - Clean version with bubble tooltips
CleanComponentPalette = None
ComponentBubble = None
ComponentEncyclopedia = None
try:
    from .component_palette import CleanComponentPalette, ComponentBubble, ComponentEncyclopedia
    print("✅ Clean Component Palette with bubbles imported")
except ImportError as e:
    print(f"⚠️ Could not import Clean Component Palette: {e}")
    CleanComponentPalette = None

# Enhanced Canvas - With floating toolbar and grid controls
EnhancedPCBCanvas = None
FloatingToolbar = None
GridSettingsDialog = None
try:
    from .enhanced_canvas import EnhancedPCBCanvas, FloatingToolbar, GridSettingsDialog
    print("✅ Enhanced Canvas with floating menus imported")
except ImportError as e:
    print(f"⚠️ Could not import Enhanced Canvas: {e}")
    EnhancedPCBCanvas = None

# ============================================================================
# FALLBACK IMPORTS - Legacy components if available
# ============================================================================

# Legacy canvas
PCBCanvas = None
try:
    if EnhancedPCBCanvas:
        PCBCanvas = EnhancedPCBCanvas  # Use enhanced version as primary
    else:
        from .canvas import PCBCanvas
        print("✅ Fallback PCBCanvas imported")
except ImportError as e:
    print(f"⚠️ Could not import fallback Canvas: {e}")
    PCBCanvas = None

# Legacy component palette
ComponentPalette = None
try:
    if CleanComponentPalette:
        ComponentPalette = CleanComponentPalette  # Use clean version as primary
    else:
        from .component_palette import ComponentPalette
        print("✅ Fallback ComponentPalette imported")
except ImportError as e:
    print(f"⚠️ Could not import fallback ComponentPalette: {e}")
    ComponentPalette = None

# ============================================================================
# SUPPORTING UI COMPONENTS
# ============================================================================

# Status Bar Manager
StatusBarManager = None
try:
    from .status_bar import StatusBarManager
    print("✅ StatusBarManager imported")
except ImportError as e:
    print(f"⚠️ Could not import StatusBarManager: {e}")
    StatusBarManager = None

# Menu Bar Manager
MenuBarManager = None
try:
    from .menu_bar import MenuBarManager
    print("✅ MenuBarManager imported")
except ImportError as e:
    print(f"⚠️ Could not import MenuBarManager: {e}")
    MenuBarManager = None

# Properties Panel
PropertiesPanel = None
try:
    from .properties_panel import PropertiesPanel
    print("✅ PropertiesPanel imported")
except ImportError as e:
    print(f"⚠️ Could not import PropertiesPanel: {e}")
    PropertiesPanel = None

# Layer Controls
LayerControls = None
try:
    from .layer_controls import LayerControls
    print("✅ LayerControls imported")
except ImportError as e:
    print(f"⚠️ Could not import LayerControls: {e}")
    LayerControls = None

# Property Editor
PropertyEditor = None
try:
    from .property_editor import PropertyEditor
    print("✅ PropertyEditor imported")
except ImportError as e:
    print(f"⚠️ Could not import PropertyEditor: {e}")
    PropertyEditor = None

# ============================================================================
# EXPORT CONFIGURATION
# ============================================================================

# Primary clean components for new installations
__all__ = []

# Main Window exports (prioritize clean version)
if CleanMainWindow is not None:
    __all__.extend(['CleanMainWindow', 'MainWindow', 'FixedMainWindow', 'EnhancedMainWindow'])
    # Set MainWindow to the clean version
    MainWindow = CleanMainWindow
    FixedMainWindow = CleanMainWindow
    EnhancedMainWindow = CleanMainWindow

# Canvas exports (prioritize enhanced version)
if EnhancedPCBCanvas is not None:
    __all__.extend(['EnhancedPCBCanvas', 'PCBCanvas', 'FloatingToolbar', 'GridSettingsDialog'])
elif PCBCanvas is not None:
    __all__.append('PCBCanvas')

# Component Palette exports (prioritize clean version)
if CleanComponentPalette is not None:
    __all__.extend(['CleanComponentPalette', 'ComponentPalette', 'ComponentBubble', 'ComponentEncyclopedia'])
elif ComponentPalette is not None:
    __all__.append('ComponentPalette')

# Supporting components
if StatusBarManager is not None:
    __all__.append('StatusBarManager')

if MenuBarManager is not None:
    __all__.append('MenuBarManager')

if PropertiesPanel is not None:
    __all__.append('PropertiesPanel')

if LayerControls is not None:
    __all__.append('LayerControls')

if PropertyEditor is not None:
    __all__.append('PropertyEditor')

# ============================================================================
# COMPONENT AVAILABILITY REPORT
# ============================================================================

def get_ui_component_status():
    """Get status of all UI components"""
    status = {
        'clean_main_window': CleanMainWindow is not None,
        'clean_component_palette': CleanComponentPalette is not None,
        'enhanced_canvas': EnhancedPCBCanvas is not None,
        'floating_toolbar': FloatingToolbar is not None,
        'component_bubble': ComponentBubble is not None,
        'component_encyclopedia': ComponentEncyclopedia is not None,
        'grid_settings_dialog': GridSettingsDialog is not None,
        'legacy_canvas': PCBCanvas is not None,
        'legacy_palette': ComponentPalette is not None,
        'status_bar': StatusBarManager is not None,
        'menu_bar': MenuBarManager is not None,
        'properties_panel': PropertiesPanel is not None,
        'layer_controls': LayerControls is not None,
        'property_editor': PropertyEditor is not None
    }
    return status

def print_ui_status():
    """Print UI component availability status"""
    status = get_ui_component_status()
    
    print("\n🎨 UI Component Status Report:")
    print("=" * 50)
    
    # Clean UI components
    print("\n✨ Clean UI Components:")
    clean_components = [
        ('Clean Main Window', status['clean_main_window']),
        ('Clean Component Palette', status['clean_component_palette']),
        ('Enhanced Canvas', status['enhanced_canvas']),
        ('Floating Toolbar', status['floating_toolbar']),
        ('Component Bubble', status['component_bubble']),
        ('Component Encyclopedia', status['component_encyclopedia']),
        ('Grid Settings Dialog', status['grid_settings_dialog'])
    ]
    
    for name, available in clean_components:
        icon = "✅" if available else "❌"
        print(f"  {icon} {name}")
    
    # Legacy components
    print("\n🔧 Legacy/Supporting Components:")
    legacy_components = [
        ('Legacy Canvas', status['legacy_canvas']),
        ('Legacy Palette', status['legacy_palette']),
        ('Status Bar Manager', status['status_bar']),
        ('Menu Bar Manager', status['menu_bar']),
        ('Properties Panel', status['properties_panel']),
        ('Layer Controls', status['layer_controls']),
        ('Property Editor', status['property_editor'])
    ]
    
    for name, available in legacy_components:
        icon = "✅" if available else "❌"
        print(f"  {icon} {name}")
    
    # Summary
    clean_count = sum([status['clean_main_window'], status['clean_component_palette'], 
                      status['enhanced_canvas'], status['floating_toolbar'],
                      status['component_bubble'], status['component_encyclopedia']])
    total_clean = 6
    
    print(f"\n📊 Clean UI Coverage: {clean_count}/{total_clean} ({int(clean_count/total_clean*100)}%)")
    print(f"📦 Total Available Components: {sum(status.values())}/{len(status)}")
    print("=" * 50)

# ============================================================================
# INITIALIZATION
# ============================================================================

# Print status on import
print(f"✅ UI package initialized with clean components")
print(f"📦 Available components: {__all__}")

# Print detailed status if requested
if os.getenv('XSETI_UI_DEBUG') == '1':
    print_ui_status()

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_main_window_class():
    """Get the best available main window class"""
    if CleanMainWindow is not None:
        return CleanMainWindow
    else:
        raise ImportError("No main window class available")

def get_canvas_class():
    """Get the best available canvas class"""
    if EnhancedPCBCanvas is not None:
        return EnhancedPCBCanvas
    elif PCBCanvas is not None:
        return PCBCanvas
    else:
        raise ImportError("No canvas class available")

def get_component_palette_class():
    """Get the best available component palette class"""
    if CleanComponentPalette is not None:
        return CleanComponentPalette
    elif ComponentPalette is not None:
        return ComponentPalette
    else:
        raise ImportError("No component palette class available")

# ============================================================================
# BACKWARDS COMPATIBILITY ALIASES
# ============================================================================

# Ensure these aliases exist for backwards compatibility
try:
    if 'MainWindow' not in locals() and CleanMainWindow is not None:
        MainWindow = CleanMainWindow
    
    if 'PCBCanvas' not in locals() and EnhancedPCBCanvas is not None:
        PCBCanvas = EnhancedPCBCanvas
    
    if 'ComponentPalette' not in locals() and CleanComponentPalette is not None:
        ComponentPalette = CleanComponentPalette
        
except NameError:
    pass  # Components not available

print("🎯 Clean UI package ready for use!")