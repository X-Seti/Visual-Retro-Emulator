"""
Component Library System
Manages and loads various retro computer components
"""

import os
import importlib.util
from typing import Dict, List, Any, Optional, Type
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ComponentInfo:
    """Information about a component"""
    name: str
    category: str
    description: str
    module_path: str = ""
    class_name: str = ""
    image_path: Optional[str] = None
    package_type: str = "DIP"
    pin_count: int = 40
    manufacturer: str = ""
    year: str = ""
    datasheet_url: str = ""
    # Additional fields for compatibility with existing database
    width: Optional[float] = None
    height: Optional[float] = None
    pins: Optional[List[Dict[str, Any]]] = None
    properties: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Handle additional initialization"""
        if self.pins is None:
            self.pins = []
        if self.properties is None:
            self.properties = {}
        # Auto-generate class_name if not provided
        if not self.class_name and self.name:
            # Convert name to class name format
            self.class_name = self.name.replace(' ', '').replace('-', '') + 'Component'
        # Auto-generate module_path if not provided
        if not self.module_path:
            self.module_path = "core.components"
    
    def add_pin(self, name: str, pin_type: str, x: float, y: float, direction: str = "input"):
        """Add a pin to the component - for database compatibility"""
        pin_info = {
            'name': name,
            'type': pin_type,
            'x': x,
            'y': y,
            'direction': direction
        }
        self.pins.append(pin_info)
        
    def set_property(self, key: str, value: Any):
        """Set a property - for database compatibility"""
        self.properties[key] = value
        
    def get_property(self, key: str, default: Any = None):
        """Get a property - for database compatibility"""
        return self.properties.get(key, default)
        
    def set_size(self, width: float, height: float):
        """Set component size - for database compatibility"""
        self.width = width
        self.height = height
        
    def get_pin_count(self) -> int:
        """Get number of pins"""
        return len(self.pins) if self.pins else self.pin_count
        
    def get_pins(self) -> List[Dict[str, Any]]:
        """Get all pins"""
        return self.pins or []
        
    def find_pin(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a pin by name"""
        for pin in self.pins:
            if pin.get('name') == name:
                return pin
        return None

# Alias for backward compatibility
ComponentDefinition = ComponentInfo

class ComponentLibrary:
    """Main component library manager"""
    
    def __init__(self):
        self.components: Dict[str, ComponentInfo] = {}
        self.categories: Dict[str, List[str]] = {}
        self.loaded_classes: Dict[str, Type] = {}
        
        # Initialize with built-in components
        self._initialize_builtin_components()
        self._scan_component_directories()
        
    def _initialize_builtin_components(self):
        """Initialize built-in component definitions"""
        
        # CPU Components
        self.register_component(ComponentInfo(
            name="6502 CPU",
            category="Processors",
            description="8-bit microprocessor used in Apple II, Commodore 64, NES",
            module_path="core.components",
            class_name="ProcessorComponent",
            pin_count=40,
            package_type="DIP",
            manufacturer="MOS Technology",
            year="1975"
        ))
        
        self.register_component(ComponentInfo(
            name="Z80 CPU",
            category="Processors", 
            description="8-bit microprocessor used in many computers and arcade games",
            module_path="core.components",
            class_name="ProcessorComponent",
            pin_count=40,
            package_type="DIP",
            manufacturer="Zilog",
            year="1976"
        ))
        
        self.register_component(ComponentInfo(
            name="68000 CPU",
            category="Processors",
            description="16/32-bit processor used in Amiga, Atari ST, Sega Genesis",
            module_path="core.components", 
            class_name="ProcessorComponent",
            pin_count=64,
            package_type="DIP",
            manufacturer="Motorola",
            year="1979"
        ))
        
        # Memory Components
        self.register_component(ComponentInfo(
            name="RAM 64KB",
            category="Memory",
            description="64KB Dynamic RAM",
            module_path="core.components",
            class_name="MemoryComponent",
            pin_count=16,
            package_type="DIP"
        ))
        
        self.register_component(ComponentInfo(
            name="ROM 32KB", 
            category="Memory",
            description="32KB Read-Only Memory",
            module_path="core.components",
            class_name="MemoryComponent", 
            pin_count=28,
            package_type="DIP"
        ))
        
        # Graphics Components
        self.register_component(ComponentInfo(
            name="VIC-II",
            category="Graphics",
            description="Video Interface Chip from Commodore 64",
            module_path="core.components",
            class_name="GraphicsComponent",
            pin_count=40,
            package_type="DIP",
            manufacturer="MOS Technology",
            year="1981"
        ))
        
        self.register_component(ComponentInfo(
            name="TMS9918A",
            category="Graphics", 
            description="Texas Instruments Video Display Processor",
            module_path="core.components",
            class_name="GraphicsComponent",
            pin_count=40,
            package_type="DIP",
            manufacturer="Texas Instruments",
            year="1979"
        ))
        
        # Audio Components
        self.register_component(ComponentInfo(
            name="SID 6581",
            category="Audio",
            description="Sound Interface Device from Commodore 64",
            module_path="core.components",
            class_name="AudioComponent", 
            pin_count=28,
            package_type="DIP",
            manufacturer="MOS Technology",
            year="1982"
        ))
        
        self.register_component(ComponentInfo(
            name="AY-3-8910",
            category="Audio",
            description="General Instrument Programmable Sound Generator",
            module_path="core.components",
            class_name="AudioComponent",
            pin_count=40,
            package_type="DIP",
            manufacturer="General Instrument",
            year="1978"
        ))
        
        # I/O Components
        self.register_component(ComponentInfo(
            name="6522 VIA",
            category="I/O",
            description="Versatile Interface Adapter",
            module_path="core.components",
            class_name="IOComponent",
            pin_count=40,
            package_type="DIP",
            manufacturer="MOS Technology",
            year="1977"
        ))
        
        self.register_component(ComponentInfo(
            name="8255 PPI", 
            category="I/O",
            description="Programmable Peripheral Interface",
            module_path="core.components",
            class_name="IOComponent",
            pin_count=40,
            package_type="DIP",
            manufacturer="Intel",
            year="1976"
        ))
        
    def _scan_component_directories(self):
        """Scan component directories for additional components"""
        component_dirs = [
            "components/commodore",
            "components/amiga", 
            "components/custom"
        ]
        
        for component_dir in component_dirs:
            if os.path.exists(component_dir):
                self._scan_directory(component_dir)
                
    def _scan_directory(self, directory: str):
        """Scan a directory for component modules"""
        try:
            for file in os.listdir(directory):
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = file[:-3]  # Remove .py extension
                    module_path = os.path.join(directory, file)
                    
                    # Try to load component info from module
                    self._load_component_from_file(module_path, module_name, directory)
                    
        except Exception as e:
            print(f"Error scanning directory {directory}: {e}")
            
    def _load_component_from_file(self, file_path: str, module_name: str, directory: str):
        """Load component information from a Python file"""
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for component metadata
                if hasattr(module, 'COMPONENT_INFO'):
                    info = module.COMPONENT_INFO
                    component_info = ComponentInfo(
                        name=info.get('name', module_name),
                        category=info.get('category', 'Custom'),
                        description=info.get('description', ''),
                        module_path=file_path,
                        class_name=info.get('class_name', module_name.title().replace('_', '')),
                        image_path=info.get('image_path'),
                        package_type=info.get('package_type', 'DIP'),
                        pin_count=info.get('pin_count', 40),
                        manufacturer=info.get('manufacturer', ''),
                        year=info.get('year', ''),
                        datasheet_url=info.get('datasheet_url', '')
                    )
                    self.register_component(component_info)
                    
        except Exception as e:
            print(f"Error loading component from {file_path}: {e}")
            
    def register_component(self, component_info: ComponentInfo):
        """Register a component in the library"""
        self.components[component_info.name] = component_info
        
        # Add to category
        category = component_info.category
        if category not in self.categories:
            self.categories[category] = []
        if component_info.name not in self.categories[category]:
            self.categories[category].append(component_info.name)
            
    def get_component_info(self, name: str) -> Optional[ComponentInfo]:
        """Get component information by name"""
        return self.components.get(name)
        
    def get_components_by_category(self, category: str) -> List[ComponentInfo]:
        """Get all components in a category"""
        if category in self.categories:
            return [self.components[name] for name in self.categories[category]]
        return []
        
    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        return list(self.categories.keys())
        
    def get_all_components(self) -> List[ComponentInfo]:
        """Get all available components"""
        return list(self.components.values())
        
    def search_components(self, query: str) -> List[ComponentInfo]:
        """Search components by name or description"""
        query = query.lower()
        results = []
        
        for component in self.components.values():
            if (query in component.name.lower() or 
                query in component.description.lower() or
                query in component.manufacturer.lower()):
                results.append(component)
                
        return results
        
    def load_component_class(self, component_name: str) -> Optional[Type]:
        """Load the actual component class"""
        if component_name in self.loaded_classes:
            return self.loaded_classes[component_name]
            
        component_info = self.get_component_info(component_name)
        if not component_info:
            return None
            
        try:
            # Load the module
            if component_info.module_path.endswith('.py'):
                # Load from file
                spec = importlib.util.spec_from_file_location(
                    component_name, component_info.module_path
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
            else:
                # Load from module name
                module = importlib.import_module(component_info.module_path)
                
            # Get the class
            if hasattr(module, component_info.class_name):
                component_class = getattr(module, component_info.class_name)
                self.loaded_classes[component_name] = component_class
                return component_class
                
        except Exception as e:
            print(f"Error loading component class {component_name}: {e}")
            
        return None
        
    def create_component_instance(self, component_name: str, **kwargs):
        """Create an instance of a component"""
        component_class = self.load_component_class(component_name)
        if component_class:
            try:
                return component_class(**kwargs)
            except Exception as e:
                print(f"Error creating component instance {component_name}: {e}")
        return None
        
    def get_component_image_path(self, component_name: str, package_type: str = None) -> Optional[str]:
        """Get the image path for a component"""
        component_info = self.get_component_info(component_name)
        if not component_info:
            return None
            
        # If specific image path is provided, use it
        if component_info.image_path and os.path.exists(component_info.image_path):
            return component_info.image_path
            
        # Try to find image based on naming convention
        package = package_type or component_info.package_type
        pin_count = component_info.pin_count
        
        # Look in images/components directory
        base_name = component_name.lower().replace(' ', '_').replace('-', '_')
        image_patterns = [
            f"images/components/{base_name}_{package.lower()}_{pin_count}.png",
            f"images/components/{base_name}_{package.lower()}.png",
            f"images/components/{base_name}.png",
            f"images/{base_name}_{package.lower()}_{pin_count}.png",
            f"images/{base_name}.png"
        ]
        
        for pattern in image_patterns:
            if os.path.exists(pattern):
                return pattern
                
        return None
        
    def export_library_info(self) -> Dict[str, Any]:
        """Export library information"""
        exported = {
            'categories': self.categories,
            'components': {}
        }
        
        for name, info in self.components.items():
            exported['components'][name] = {
                'name': info.name,
                'category': info.category,
                'description': info.description,
                'module_path': info.module_path,
                'class_name': info.class_name,
                'image_path': info.image_path,
                'package_type': info.package_type,
                'pin_count': info.pin_count,
                'manufacturer': info.manufacturer,
                'year': info.year,
                'datasheet_url': info.datasheet_url
            }
            
        return exported
        
    def get_library_statistics(self) -> Dict[str, Any]:
        """Get library statistics"""
        stats = {
            'total_components': len(self.components),
            'categories': len(self.categories),
            'components_by_category': {},
            'manufacturers': {},
            'package_types': {},
            'pin_counts': {}
        }
        
        for component in self.components.values():
            # Count by category
            category = component.category
            stats['components_by_category'][category] = stats['components_by_category'].get(category, 0) + 1
            
            # Count by manufacturer
            manufacturer = component.manufacturer or 'Unknown'
            stats['manufacturers'][manufacturer] = stats['manufacturers'].get(manufacturer, 0) + 1
            
            # Count by package type
            package = component.package_type
            stats['package_types'][package] = stats['package_types'].get(package, 0) + 1
            
            # Count by pin count
            pins = str(component.pin_count)
            stats['pin_counts'][pins] = stats['pin_counts'].get(pins, 0) + 1
            
        return stats

# Global component library instance
component_library = ComponentLibrary()
            