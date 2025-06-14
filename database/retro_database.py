"""
X-Seti - June12 2025 - Updated Retro Component Database
Compatible with the new ComponentInfo system and reads from components folder
"""

#This goes in database/
import os
import sys
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the new component system
try:
    from component_library import ComponentInfo, ComponentLibrary, component_library
    print("✅ Successfully imported ComponentInfo from component_library")
except ImportError as e:
    print(f"⚠️ Could not import from component_library: {e}")
    # Create a fallback ComponentInfo
    class ComponentInfo:
        def __init__(self, name: str, category: str = "Custom", description: str = "", **kwargs):
            self.name = name
            self.category = category
            self.description = description
            self.pins = []
            self.properties = {}
            self.width = kwargs.get('width', 60)
            self.height = kwargs.get('height', 40)
            self.package_type = kwargs.get('package_type', 'DIP')
            self.pin_count = kwargs.get('pin_count', 40)
            self.manufacturer = kwargs.get('manufacturer', '')
            
        def add_pin(self, name: str, pin_type: str, x: float, y: float, direction: str = "input"):
            self.pins.append({
                'name': name, 'type': pin_type, 'x': x, 'y': y, 'direction': direction
            })

class RetroComponentDatabase:
    """Updated retro component database"""
    
    def __init__(self):
        self.components: Dict[str, ComponentInfo] = {}
        self.categories: Dict[str, List[str]] = {}
        
        # Create components directory if it doesn't exist
        self.components_dir = os.path.join(os.path.dirname(__file__), 'components')
        os.makedirs(self.components_dir, exist_ok=True)
        
        self._load_all_components()
        
    def _load_all_components(self):
        """Load all components from various sources"""
        print("Loading components...")
        
        # Try to load from components folder first
        self._load_from_components_folder()
        
        # Load from component_library if available
        self._load_from_component_library()
        
        # Create fallback components if we don't have any
        if not self.components:
            self._create_fallback_components()
            
        print(f"✅ Loaded {len(self.components)} components")
        
    def _load_from_components_folder(self):
        """Load components from the components folder structure"""
        base_components_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'components')
        
        if not os.path.exists(base_components_dir):
            print(f"⚠️ Components directory not found: {base_components_dir}")
            return
            
        # Load from subdirectories
        for subdir in ['commodore', 'amiga', 'custom']:
            subdir_path = os.path.join(base_components_dir, subdir)
            if os.path.exists(subdir_path):
                self._load_from_directory(subdir_path, subdir.title())
                
    def _load_from_directory(self, directory: str, category: str):
        """Load components from a specific directory"""
        try:
            for filename in os.listdir(directory):
                if filename.endswith('.py') and not filename.startswith('__'):
                    self._load_component_from_file(
                        os.path.join(directory, filename), 
                        filename[:-3],  # Remove .py
                        category
                    )
        except Exception as e:
            print(f"⚠️ Error loading from directory {directory}: {e}")
            
    def _load_component_from_file(self, filepath: str, module_name: str, category: str):
        """Load component from Python file"""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for component info in the module
                if hasattr(module, 'COMPONENT_INFO'):
                    info = module.COMPONENT_INFO
                    component = ComponentInfo(
                        name=info.get('name', module_name.replace('_', ' ').title()),
                        category=info.get('category', category),
                        description=info.get('description', ''),
                        package_type=info.get('package_type', 'DIP'),
                        pin_count=info.get('pin_count', 40),
                        manufacturer=info.get('manufacturer', ''),
                        width=info.get('width', 60),
                        height=info.get('height', 40)
                    )
                    
                    # Add pins if available
                    if 'pins' in info:
                        for pin_info in info['pins']:
                            component.add_pin(
                                pin_info.get('name', ''),
                                pin_info.get('type', 'general'),
                                pin_info.get('x', 0),
                                pin_info.get('y', 0),
                                pin_info.get('direction', 'input')
                            )
                            
                    # Add properties if available
                    if 'properties' in info:
                        component.properties.update(info['properties'])
                        
                    self.add_component(component)
                    print(f"✅ Loaded component: {component.name}")
                    
        except Exception as e:
            print(f"⚠️ Error loading component from {filepath}: {e}")
            
    def _load_from_component_library(self):
        """Load components from the component library"""
        try:
            if 'component_library' in globals() and component_library:
                for component_info in component_library.get_all_components():
                    self.add_component(component_info)
                    
        except Exception as e:
            print(f"⚠️ Error loading from component library: {e}")
            
    def _create_fallback_components(self):
        """Create fallback components if no others are available"""
        print("Creating fallback components...")
        
        # CPU Components
        z80 = ComponentInfo(
            name="Z80 CPU",
            category="Processors", 
            description="8-bit microprocessor",
            package_type="DIP",
            pin_count=40,
            manufacturer="Zilog",
            width=60,
            height=80
        )
        
        # Add Z80 pins (simplified)
        pin_spacing = 2.54  # Standard pin spacing in mm
        start_y = 5
        
        for i in range(20):  # Left side pins
            pin_name = f"Pin {i+1}"
            z80.add_pin(pin_name, "general", 0, start_y + i * pin_spacing, "input")
            
        for i in range(20):  # Right side pins  
            pin_name = f"Pin {i+21}"
            z80.add_pin(pin_name, "general", 60, start_y + i * pin_spacing, "output")
            
        # Add properties using the properties dict
        z80.properties.update({
            "Clock Speed": "4.0 MHz",
            "Architecture": "8-bit",
            "Instruction Set": "Z80",
            "Package": "DIP-40"
        })
        
        self.add_component(z80)
        
        # Memory Components
        ram_64k = ComponentInfo(
            name="RAM 64KB",
            category="Memory",
            description="64KB Dynamic RAM",
            package_type="DIP", 
            pin_count=16,
            width=40,
            height=30
        )
        
        ram_64k.properties.update({
            "Capacity": "64KB",
            "Type": "DRAM",
            "Access Time": "150ns"
        })
        
        self.add_component(ram_64k)
        
        # Graphics Components
        vic2 = ComponentInfo(
            name="VIC-II",
            category="Graphics",
            description="Video Interface Chip from Commodore 64",
            package_type="DIP",
            pin_count=40,
            manufacturer="MOS Technology",
            width=60,
            height=80
        )
        
        vic2.properties.update({
            "Resolution": "320x200", 
            "Colors": "16",
            "Sprites": "8"
        })
        
        self.add_component(vic2)
        
        # Audio Components
        sid = ComponentInfo(
            name="SID 6581",
            category="Audio",
            description="Sound Interface Device from Commodore 64",
            package_type="DIP",
            pin_count=28,
            manufacturer="MOS Technology",
            width=50,
            height=60
        )
        
        sid.properties.update({
            "Voices": "3",
            "Waveforms": "4", 
            "Filters": "Multi-mode"
        })
        
        self.add_component(sid)
        
        print(f"✅ Created {len(self.components)} fallback components")
        
    def add_component(self, component: ComponentInfo):
        """Add a component to the database"""
        self.components[component.name] = component
        
        # Add to category
        category = component.category
        if category not in self.categories:
            self.categories[category] = []
        if component.name not in self.categories[category]:
            self.categories[category].append(component.name)
            
    def get_component(self, name: str) -> Optional[ComponentInfo]:
        """Get component by name"""
        return self.components.get(name)
        
    def get_components_by_category(self, category: str) -> List[ComponentInfo]:
        """Get all components in a category"""
        if category in self.categories:
            return [self.components[name] for name in self.categories[category] 
                   if name in self.components]
        return []
        
    def get_all_components(self) -> List[ComponentInfo]:
        """Get all components"""
        return list(self.components.values())
        
    def get_categories(self) -> List[str]:
        """Get all categories"""
        return list(self.categories.keys())
        
    def search_components(self, query: str) -> List[ComponentInfo]:
        """Search components by name or description"""
        query = query.lower()
        results = []
        
        for component in self.components.values():
            if (query in component.name.lower() or 
                query in component.description.lower()):
                results.append(component)
                
        return results
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            'total_components': len(self.components),
            'categories': len(self.categories),
            'components_by_category': {
                cat: len(comps) for cat, comps in self.categories.items()
            }
        }

# Create global instances
retro_database = RetroComponentDatabase()

# Create alias for compatibility
global_component_library = retro_database

# Export for compatibility
__all__ = ['retro_database', 'global_component_library', 'RetroComponentDatabase']
