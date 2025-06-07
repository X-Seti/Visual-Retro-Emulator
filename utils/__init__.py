"""
Utils Package
Utility modules and tools for the retro emulator
"""

# Import chip editor safely
try:
    from .chip_editor import *
    # Only create aliases if the classes exist
    if 'ChipEditor' in globals():
        ChipDesigner = ChipEditor
        ChipCreator = ChipEditor
    else:
        ChipDesigner = None
        ChipCreator = None
except ImportError as e:
    print(f"Warning: Could not import from chip_editor: {e}")
    ChipEditor = None
    ChipDesigner = None  
    ChipCreator = None

# Import other utils safely
try:
    from .App_settings_system import *
except ImportError:
    print("Warning: Could not import App_settings_system")

# Safe exports - only include what actually exists
__all__ = []

# Add exports only if they exist
for name in ['ChipEditor', 'ChipDesigner', 'ChipCreator', 'AppSettingsSystem']:
    if name in globals() and globals()[name] is not None:
        __all__.append(name)

__version__ = '1.0.0'