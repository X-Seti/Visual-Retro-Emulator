"""
X-Seti - June07 2025 - Integration Component Loader
Loads and integrates components from various sources and formats
"""

import os
import json
import importlib
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from dataclasses import asdict

from component_library import ComponentLibrary, ComponentInfo
from core.components import BaseComponent, ComponentFactory

class ComponentLoader:
    """Loads components from various sources"""
    
    def __init__(self, component_library: ComponentLibrary):
        self.library = component_library
        self.loaded_modules = {}
        self.component_cache = {}
        
    def load_from_directory(self, directory: str) -> List[ComponentInfo]:
        """Load all components from a directory"""
        loaded_components = []
        
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return loaded_components
            
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                
                if os.path.isfile(item_path):
                    if item.endswith('.py'):
                        # Python module
                        component = self.load_from_python_file(item_path)
                        if component:
                            loaded_components.append(component)
                    elif item.endswith('.json'):
                        # JSON component definition
                        components = self.load_from_json_file(item_path)
                        loaded_components.extend(components)
                        
                elif os.path.isdir(item_path):
                    # Recursively load from subdirectory
                    sub_components = self.load_from_directory(item_path)
                    loaded_components.extend(sub_components)
                    
        except Exception as e:
            print(f"Error loading from directory {directory}: {e}")
            
        return loaded_components
        
    def load_from_python_file(self, file_path: str) -> Optional[ComponentInfo]:
        """Load component from Python file"""
        try:
            # Get module name from file
            module_name = Path(file_path).stem
            
            # Load module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if not spec or not spec.loader:
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check for component info
            if hasattr(module, 'COMPONENT_INFO'):
                info_dict = module.COMPONENT_INFO
                
                # Create ComponentInfo from dictionary
                component_info = ComponentInfo(
                    name=info_dict.get('name', module_name),
                    category=info_dict.get('category', 'Custom'),
                    description=info_dict.get('description', ''),
                    module_path=file_path,
                    class_name=info_dict.get('class_name', f"{module_name.title()}Component"),
                    image_path=info_dict.get('image_path'),
                    package_type=info_dict.get('package_type', 'DIP'),
                    pin_count=info_dict.get('pin_count', 40),
                    manufacturer=info_dict.get('manufacturer', ''),
                    year=info_dict.get('year', ''),
                    datasheet_url=info_dict.get('datasheet_url', '')
                )
                
                # Register with library
                self.library.register_component(component_info)
                return component_info
                
        except Exception as e:
            print(f"Error loading Python component from {file_path}: {e}")
            
        return None
        
    def load_from_json_file(self, file_path: str) -> List[ComponentInfo]:
        """Load components from JSON file"""
        loaded_components = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle different JSON formats
            if isinstance(data, dict):
                if 'components' in data:
                    # Multiple components in file
                    for comp_data in data['components']:
                        component = self._create_component_from_dict(comp_data, file_path)
                        if component:
                            loaded_components.append(component)
                else:
                    # Single component
                    component = self._create_component_from_dict(data, file_path)
                    if component:
                        loaded_components.append(component)
                        
            elif isinstance(data, list):
                # Array of components
                for comp_data in data:
                    component = self._create_component_from_dict(comp_data, file_path)
                    if component:
                        loaded_components.append(component)
                        
        except Exception as e:
            print(f"Error loading JSON components from {file_path}: {e}")
            
        return loaded_components
        
    def _create_component_from_dict(self, data: dict, source_file: str) -> Optional[ComponentInfo]:
        """Create ComponentInfo from dictionary"""
        try:
            component_info = ComponentInfo(
                name=data.get('name', 'Unknown'),
                category=data.get('category', 'Custom'),
                description=data.get('description', ''),
                module_path=data.get('module_path', 'core.components'),
                class_name=data.get('class_name', 'BaseComponent'),
                image_path=data.get('image_path'),
                package_type=data.get('package_type', 'DIP'),
                pin_count=data.get('pin_count', 40),
                manufacturer=data.get('manufacturer', ''),
                year=data.get('year', ''),
                datasheet_url=data.get('datasheet_url', '')
            )
            
            # Register with library
            self.library.register_component(component_info)
            return component_info
            
        except Exception as e:
            print(f"Error creating component from data in {source_file}: {e}")
            
        return None
        
    def create_component_instance(self, component_name: str, **kwargs) -> Optional[BaseComponent]:
        """Create an instance of a component"""
        # Check cache first
        cache_key = f"{component_name}_{hash(str(sorted(kwargs.items())))}"
        if cache_key in self.component_cache:
            # Return a copy of cached component
            cached = self.component_cache[cache_key]
            return self._clone_component(cached)
            
        # Get component info
        component_info = self.library.get_component_info(component_name)
        if not component_info:
            print(f"Component not found: {component_name}")
            return None
            
        try:
            # Try to create using ComponentFactory first
            component = ComponentFactory.create_component(
                component_info.category, 
                component_name, 
                **kwargs
            )
            
            if component:
                # Cache the component
                self.component_cache[cache_key] = component
                return self._clone_component(component)
                
            # If factory creation failed, try direct class loading
            component_class = self.library.load_component_class(component_name)
            if component_class:
                component = component_class(component_info.category, component_name, **kwargs)
                self.component_cache[cache_key] = component
                return self._clone_component(component)
                
        except Exception as e:
            print(f"Error creating component instance {component_name}: {e}")
            
        return None
        
    def _clone_component(self, component: BaseComponent) -> BaseComponent:
        """Create a copy of a component"""
        # This is a simplified clone - in practice you'd want a proper deep copy
        try:
            component_data = component.to_dict()
            cloned = ComponentFactory.create_from_dict(component_data)
            return cloned
        except:
            # Fallback: create new instance
            return ComponentFactory.create_component(
                component.component_type,
                component.name
            )
            
    def refresh_library(self):
        """Refresh the component library"""
        # Clear caches
        self.component_cache.clear()
        self.loaded_modules.clear()
        
        # Reload components from known directories
        component_dirs = [
            "components",
            "components/commodore", 
            "components/amiga",
            "components/custom"
        ]
        
        for directory in component_dirs:
            if os.path.exists(directory):
                self.load_from_directory(directory)
                
    def validate_component(self, component_name: str) -> tuple[bool, List[str]]:
        """Validate a component definition"""
        errors = []
        
        component_info = self.library.get_component_info(component_name)
        if not component_info:
            return False, ["Component not found"]
            
        # Check if module exists
        if component_info.module_path and not os.path.exists(component_info.module_path):
            if not self._is_builtin_module(component_info.module_path):
                errors.append(f"Module not found: {component_info.module_path}")
                
        # Check if image exists
        if component_info.image_path and not os.path.exists(component_info.image_path):
            errors.append(f"Image not found: {component_info.image_path}")
            
        # Try to load the component class
        try:
            component_class = self.library.load_component_class(component_name)
            if not component_class:
                errors.append("Failed to load component class")
        except Exception as e:
            errors.append(f"Error loading component class: {e}")
            
        return len(errors) == 0, errors
        
    def _is_builtin_module(self, module_path: str) -> bool:
        """Check if module path is a built-in module"""
        builtin_modules = [
            "core.components",
            "components",
            "__builtin__"
        ]
        return any(module_path.startswith(builtin) for builtin in builtin_modules)
        
    def export_component_definitions(self, output_file: str, format: str = 'json'):
        """Export all component definitions to file"""
        try:
            if format.lower() == 'json':
                self._export_to_json(output_file)
            else:
                print(f"Unsupported export format: {format}")
                
        except Exception as e:
            print(f"Error exporting component definitions: {e}")
            
    def _export_to_json(self, output_file: str):
        """Export to JSON format"""
        exported_data = {
            'metadata': {
                'version': '1.0',
                'exported_by': 'Integration Component Loader',
                'total_components': len(self.library.components)
            },
            'components': []
        }
        
        for component_info in self.library.get_all_components():
            component_dict = asdict(component_info)
            exported_data['components'].append(component_dict)
            
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(exported_data, f, indent=2, ensure_ascii=False)
            
    def import_component_definitions(self, input_file: str):
        """Import component definitions from file"""
        try:
            if input_file.endswith('.json'):
                self._import_from_json(input_file)
            else:
                print(f"Unsupported import format for file: {input_file}")
                
        except Exception as e:
            print(f"Error importing component definitions: {e}")
            
    def _import_from_json(self, input_file: str):
        """Import from JSON format"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if 'components' in data:
            for comp_data in data['components']:
                self._create_component_from_dict(comp_data, input_file)
                
    def get_loading_statistics(self) -> Dict[str, Any]:
        """Get loading statistics"""
        return {
            'cached_components': len(self.component_cache),
            'loaded_modules': len(self.loaded_modules),
            'total_components': len(self.library.components),
            'cache_hit_rate': self._calculate_cache_hit_rate()
        }
        
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        # This would need proper tracking in a real implementation
        return 0.0
        
    def clear_cache(self):
        """Clear all caches"""
        self.component_cache.clear()
        self.loaded_modules.clear()

# Integration functions for backward compatibility
def load_retro_components():
    """Load all retro components"""
    from component_library import component_library
    loader = ComponentLoader(component_library)
    
    # Load from standard directories
    directories = [
        "components/commodore",
        "components/amiga", 
        "components/custom"
    ]
    
    for directory in directories:
        loader.load_from_directory(directory)
        
    return loader

def get_component_by_name(name: str):
    """Get component information by name"""
    from component_library import component_library
    return component_library.get_component_info(name)

def create_component(name: str, **kwargs):
    """Create a component instance"""
    from component_library import component_library
    loader = ComponentLoader(component_library)
    return loader.create_component_instance(name, **kwargs)

# Global loader instance
_global_loader = None

def get_global_loader():
    """Get the global component loader"""
    global _global_loader
    if _global_loader is None:
        from component_library import component_library
        _global_loader = ComponentLoader(component_library)
    return _global_loader
