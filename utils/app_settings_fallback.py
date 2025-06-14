"""
X-Seti - App Settings System - Simple Fallback Implementation
Provides basic theme and settings management
"""
#this goes in utils/
import json
import os
from typing import Dict, Any, Optional

class AppSettingsSystem:
    """Simple app settings system with theme support"""
    
    def __init__(self, config_file: str = "app_settings.json"):
        self.config_file = config_file
        self.settings = {
            'theme': 'default',
            'window_geometry': {},
            'recent_files': [],
            'grid_visible': True,
            'snap_to_grid': True,
            'auto_save': True,
            'language': 'en'
        }
        
        # Available themes
        self.themes = {
            'default': {
                'name': 'Default',
                'colors': {
                    'background': '#f0f0f0',
                    'foreground': '#000000',
                    'accent': '#0078d4'
                }
            },
            'dark': {
                'name': 'Dark',
                'colors': {
                    'background': '#2d2d2d',
                    'foreground': '#ffffff',
                    'accent': '#0078d4'
                }
            },
            'retro': {
                'name': 'Retro Green',
                'colors': {
                    'background': '#001100',
                    'foreground': '#00ff00',
                    'accent': '#ffff00'
                }
            }
        }
        
        self.load_settings()
        print("✓ App Settings System initialized")
    
    def load_settings(self) -> bool:
        """Load settings from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
                print(f"✓ Settings loaded from {self.config_file}")
                return True
        except Exception as e:
            print(f"⚠️ Error loading settings: {e}")
        
        return False
    
    def save_settings(self) -> bool:
        """Save settings to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            print(f"✓ Settings saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"⚠️ Error saving settings: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value"""
        self.settings[key] = value
    
    def get_theme(self, theme_name: str = None) -> Dict[str, Any]:
        """Get theme configuration"""
        if theme_name is None:
            theme_name = self.settings.get('theme', 'default')
        
        return self.themes.get(theme_name, self.themes['default'])
    
    def get_available_themes(self) -> Dict[str, Dict[str, Any]]:
        """Get all available themes"""
        return self.themes.copy()
    
    def set_theme(self, theme_name: str) -> bool:
        """Set current theme"""
        if theme_name in self.themes:
            self.settings['theme'] = theme_name
            print(f"✓ Theme changed to: {theme_name}")
            return True
        else:
            print(f"⚠️ Unknown theme: {theme_name}")
            return False
    
    def get_current_theme_name(self) -> str:
        """Get current theme name"""
        return self.settings.get('theme', 'default')
    
    def add_recent_file(self, file_path: str, max_files: int = 10):
        """Add file to recent files list"""
        recent_files = self.settings.get('recent_files', [])
        
        # Remove if already exists
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Add to beginning
        recent_files.insert(0, file_path)
        
        # Limit list size
        recent_files = recent_files[:max_files]
        
        self.settings['recent_files'] = recent_files
    
    def get_recent_files(self) -> list:
        """Get recent files list"""
        return self.settings.get('recent_files', [])
    
    def clear_recent_files(self):
        """Clear recent files list"""
        self.settings['recent_files'] = []
    
    def export_settings(self, export_file: str) -> bool:
        """Export settings to file"""
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            print(f"✓ Settings exported to {export_file}")
            return True
        except Exception as e:
            print(f"⚠️ Error exporting settings: {e}")
            return False
    
    def import_settings(self, import_file: str) -> bool:
        """Import settings from file"""
        try:
            if os.path.exists(import_file):
                with open(import_file, 'r', encoding='utf-8') as f:
                    imported_settings = json.load(f)
                    self.settings.update(imported_settings)
                print(f"✓ Settings imported from {import_file}")
                return True
        except Exception as e:
            print(f"⚠️ Error importing settings: {e}")
        
        return False
    
    def reset_to_defaults(self):
        """Reset settings to defaults"""
        self.settings = {
            'theme': 'default',
            'window_geometry': {},
            'recent_files': [],
            'grid_visible': True,
            'snap_to_grid': True,
            'auto_save': True,
            'language': 'en'
        }
        print("✓ Settings reset to defaults")
    
    def get_window_geometry(self, window_name: str) -> Optional[Dict[str, int]]:
        """Get saved window geometry"""
        return self.settings.get('window_geometry', {}).get(window_name)
    
    def set_window_geometry(self, window_name: str, geometry: Dict[str, int]):
        """Save window geometry"""
        if 'window_geometry' not in self.settings:
            self.settings['window_geometry'] = {}
        
        self.settings['window_geometry'][window_name] = geometry
    
    def apply_theme_to_widget(self, widget, theme_name: str = None):
        """Apply theme colors to a widget (basic implementation)"""
        theme = self.get_theme(theme_name)
        colors = theme.get('colors', {})
        
        try:
            # Basic stylesheet application
            style = f"""
            QWidget {{
                background-color: {colors.get('background', '#f0f0f0')};
                color: {colors.get('foreground', '#000000')};
            }}
            QPushButton {{
                background-color: {colors.get('accent', '#0078d4')};
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {colors.get('accent', '#0078d4')}aa;
            }}
            """
            
            widget.setStyleSheet(style)
            print(f"✓ Theme applied to widget: {theme['name']}")
            
        except Exception as e:
            print(f"⚠️ Error applying theme: {e}")

# Create global instance for compatibility
app_settings = AppSettingsSystem()

# Export for import compatibility
__all__ = ['AppSettingsSystem', 'app_settings']
