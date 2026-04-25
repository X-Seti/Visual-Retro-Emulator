# X-Seti - June23 2025 - CAD Tools Debug Guide
# Debug checklist for CAD tools icons and functionality

# ISSUE 1: Multiple CAD Implementations Detected
# ==============================================
# Found these conflicting files:
# - ui/cad_tools_panel.py (Complete implementation with emoji icons)
# - ui/cad_tools.py (Different implementation)  
# - ui/main_window.py (Built-in CAD tools in _create_cad_tools_dock)

# ISSUE 2: Missing Icons Problem
# ============================
# The emoji icons (🔍📏🔘⚫🟢) aren't showing because:
# 1. Font doesn't support emoji
# 2. System doesn't have emoji fonts
# 3. PyQt6 emoji rendering issues

# ISSUE 3: Import Conflicts
# ========================
# Multiple CAD tool classes with same names causing import conflicts

# DEBUG STEPS:
# ============

# Step 1: Check which CAD tools panel is actually being used
def debug_cad_tools_imports():
    """Add this to main_window.py to see what's imported"""
    print("🔍 CAD Tools Import Debug:")
    
    try:
        from ui.cad_tools_panel import CADToolsPanel
        print(f"✅ CADToolsPanel imported from ui.cad_tools_panel")
        print(f"   Type: {type(CADToolsPanel)}")
        print(f"   Module: {CADToolsPanel.__module__}")
    except ImportError as e:
        print(f"❌ Failed to import from ui.cad_tools_panel: {e}")
    
    try:
        from ui.cad_tools import CADToolsWidget
        print(f"✅ CADToolsWidget imported from ui.cad_tools")
        print(f"   Type: {type(CADToolsWidget)}")
        print(f"   Module: {CADToolsWidget.__module__}")
    except ImportError as e:
        print(f"❌ Failed to import from ui.cad_tools: {e}")

# Step 2: Check if CAD tools dock is created
def debug_cad_tools_dock_creation():
    """Add this to main_window._create_docks()"""
    print("🔍 CAD Tools Dock Creation Debug:")
    
    if hasattr(self, 'cad_tools_dock'):
        print(f"✅ cad_tools_dock exists: {type(self.cad_tools_dock)}")
        widget = self.cad_tools_dock.widget()
        print(f"   Widget: {type(widget)}")
        print(f"   Visible: {self.cad_tools_dock.isVisible()}")
        print(f"   Children: {len(widget.children()) if widget else 0}")
    else:
        print("❌ cad_tools_dock not found")

# Step 3: Check if tool buttons are created
def debug_tool_buttons():
    """Add this to CAD tools panel __init__"""
    print("🔍 Tool Buttons Debug:")
    
    if hasattr(self, 'tool_button_map'):
        print(f"✅ tool_button_map exists with {len(self.tool_button_map)} buttons")
        for tool, button in self.tool_button_map.items():
            print(f"   {tool.value}: {button.text()}")
    else:
        print("❌ tool_button_map not found")
    
    if hasattr(self, 'tool_buttons'):
        buttons = self.tool_buttons.buttons()
        print(f"✅ tool_buttons group has {len(buttons)} buttons")
        for i, btn in enumerate(buttons):
            print(f"   Button {i}: '{btn.text()}' - Visible: {btn.isVisible()}")
    else:
        print("❌ tool_buttons group not found")

# Step 4: Font and Emoji Debug
def debug_emoji_fonts():
    """Check if emoji fonts are working"""
    from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
    from PyQt6.QtGui import QFont
    
    print("🔍 Emoji Font Debug:")
    
    # Test different fonts
    test_fonts = [
        "Segoe UI Emoji",
        "Noto Color Emoji", 
        "Apple Color Emoji",
        "Symbola",
        "Arial",
        "Segoe UI"
    ]
    
    test_emoji = "🔍📏🔘⚫🟢⛔🖨️🔩"
    
    for font_name in test_fonts:
        font = QFont(font_name)
        print(f"   Font '{font_name}': Available = {font.exactMatch()}")

# QUICK FIXES:
# ===========

# Fix 1: Replace emoji with text labels
def create_text_only_cad_tools():
    """Use text-only CAD tool buttons"""
    tools = [
        (CADTool.SELECT, "Select", "SEL"),
        (CADTool.TRACE, "Trace", "TRC"), 
        (CADTool.PAD, "Pad", "PAD"),
        (CADTool.VIA, "Via", "VIA"),
        (CADTool.COPPER_FILL, "Fill", "FIL"),
        (CADTool.KEEPOUT, "Keep", "KEP"),
        (CADTool.SILKSCREEN, "Silk", "SLK"),
        (CADTool.DRILL, "Drill", "DRL"),
        (CADTool.RECTANGLE, "Rect", "RCT"),
        (CADTool.CIRCLE, "Circle", "CRC"),
        (CADTool.POLYGON, "Poly", "PLY"),
        (CADTool.TEXT, "Text", "TXT"),
        (CADTool.DIMENSION, "Dim", "DIM"),
        (CADTool.RULER, "Rule", "RUL")
    ]
    
    for tool, name, short in tools:
        btn = QPushButton(f"{short}\n{name}")
        # Rest of button setup...

# Fix 2: Simple ASCII symbols instead of emoji
def create_ascii_symbol_cad_tools():
    """Use ASCII symbols for CAD tools"""
    tools = [
        (CADTool.SELECT, "Select", "->"),
        (CADTool.TRACE, "Trace", "~~"),
        (CADTool.PAD, "Pad", "[]"),
        (CADTool.VIA, "Via", "()"),
        (CADTool.COPPER_FILL, "Fill", "##"),
        (CADTool.KEEPOUT, "Keep", "XX"),
        (CADTool.SILKSCREEN, "Silk", "Ab"),
        (CADTool.DRILL, "Drill", "**"),
        (CADTool.RECTANGLE, "Rect", "[]"),
        (CADTool.CIRCLE, "Circle", "()"),
        (CADTool.POLYGON, "Poly", "<>"),
        (CADTool.TEXT, "Text", "T"),
        (CADTool.DIMENSION, "Dim", "|-|"),
        (CADTool.RULER, "Rule", "---")
    ]

# Fix 3: Remove conflicting CAD implementations
def remove_duplicate_cad_tools():
    """Steps to clean up conflicting CAD tools"""
    # 1. Remove built-in CAD tools from main_window.py _create_cad_tools_dock()
    # 2. Use only ui/cad_tools_panel.py
    # 3. Remove ui/cad_tools.py if not needed
    # 4. Update imports to use single source
    pass

# IMPLEMENTATION PRIORITY:
# ======================
# 1. First: Get basic CAD tools showing (text-only buttons)
# 2. Second: Get tool selection working 
# 3. Third: Get tools actually doing something on canvas
# 4. Fourth: Add icons/symbols back when basics work

# RECOMMENDED ACTION:
# ==================
# 1. Add debug functions to main_window.py
# 2. Run debug to see what's actually loaded
# 3. Choose ONE CAD implementation (ui/cad_tools_panel.py)
# 4. Remove others to eliminate conflicts
# 5. Replace emoji with text/ASCII symbols
# 6. Test tool selection
# 7. Connect tools to canvas operations
