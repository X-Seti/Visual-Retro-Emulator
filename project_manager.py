"""
X-Seti - June07 2025 - Consolidated Project Manager
Handles project creation, loading, saving, and management
"""

import os
import json
import time
import shutil
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ProjectSettings:
    """Project settings configuration"""
    name: str = "Untitled Project"
    description: str = ""
    author: str = ""
    version: str = "1.0.0"
    created_date: str = ""
    modified_date: str = ""
    target_system: str = ""  # e.g., "C64", "Amiga", "Custom"
    
    # Visual settings
    grid_size: int = 20
    grid_visible: bool = True
    snap_to_grid: bool = True
    
    # Layer settings
    active_layer: str = "chip"
    layer_visibility: Dict[str, bool] = field(default_factory=lambda: {
        "chip": True,
        "pcb": False,
        "gerber": False
    })
    
    # Export settings
    export_format: str = "json"
    export_path: str = ""
    
    # Simulation settings
    simulation_speed: float = 1.0
    debug_mode: bool = False

@dataclass
class Project:
    """Project data structure"""
    settings: ProjectSettings = field(default_factory=ProjectSettings)
    components: Dict[str, Any] = field(default_factory=dict)
    connections: List[Dict[str, Any]] = field(default_factory=list)
    canvas_state: Dict[str, Any] = field(default_factory=dict)
    custom_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.settings.created_date:
            self.settings.created_date = time.strftime("%Y-%m-%d %H:%M:%S")
        self.settings.modified_date = time.strftime("%Y-%m-%d %H:%M:%S")

class ProjectManager:
    """Comprehensive project management system"""
    
    def __init__(self):
        self.current_project: Optional[Project] = None
        self.current_file_path: Optional[str] = None
        self.is_modified: bool = False
        self.recent_projects: List[str] = []
        self.auto_save_enabled: bool = True
        self.auto_save_interval: int = 300  # 5 minutes
        self.max_recent_projects: int = 10
        
        # Load settings
        self._load_manager_settings()
        
        print("✓ Project Manager initialized")
    
    def _load_manager_settings(self):
        """Load project manager settings"""
        settings_file = "project_manager_settings.json"
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.recent_projects = data.get('recent_projects', [])
                self.auto_save_enabled = data.get('auto_save_enabled', True)
                self.auto_save_interval = data.get('auto_save_interval', 300)
                self.max_recent_projects = data.get('max_recent_projects', 10)
                
                print("✓ Project manager settings loaded")
        except Exception as e:
            print(f"⚠️ Error loading project manager settings: {e}")
    
    def _save_manager_settings(self):
        """Save project manager settings"""
        settings_file = "project_manager_settings.json"
        try:
            data = {
                'recent_projects': self.recent_projects,
                'auto_save_enabled': self.auto_save_enabled,
                'auto_save_interval': self.auto_save_interval,
                'max_recent_projects': self.max_recent_projects
            }
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print("✓ Project manager settings saved")
        except Exception as e:
            print(f"⚠️ Error saving project manager settings: {e}")
    
    def new_project(self, name: str = "Untitled Project", 
                   description: str = "", author: str = "") -> bool:
        """Create a new project"""
        try:
            # Check if current project needs saving
            if self.is_modified and not self._prompt_save_current():
                return False
            
            # Create new project
            settings = ProjectSettings(
                name=name,
                description=description,
                author=author,
                created_date=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            
            self.current_project = Project(settings=settings)
            self.current_file_path = None
            self.is_modified = False
            
            print(f"✓ New project created: {name}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error creating new project: {e}")
            return False
    
    def open_project(self, file_path: str) -> bool:
        """Open an existing project"""
        try:
            # Check if current project needs saving
            if self.is_modified and not self._prompt_save_current():
                return False
            
            if not os.path.exists(file_path):
                print(f"⚠️ Project file not found: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load project data
            project = self._load_project_from_dict(data)
            if not project:
                return False
            
            self.current_project = project
            self.current_file_path = file_path
            self.is_modified = False
            
            # Add to recent projects
            self._add_to_recent_projects(file_path)
            
            print(f"✓ Project opened: {file_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error opening project: {e}")
            return False
    
    def save_project(self, file_path: str = None) -> bool:
        """Save the current project"""
        try:
            if not self.current_project:
                print("⚠️ No project to save")
                return False
            
            # Use current file path if not specified
            if file_path is None:
                file_path = self.current_file_path
            
            if not file_path:
                print("⚠️ No file path specified for save")
                return False
            
            # Update modified date
            self.current_project.settings.modified_date = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Convert project to dictionary
            project_data = self._save_project_to_dict(self.current_project)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            self.current_file_path = file_path
            self.is_modified = False
            
            # Add to recent projects
            self._add_to_recent_projects(file_path)
            
            print(f"✓ Project saved: {file_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error saving project: {e}")
            return False
    
    def save_project_as(self, file_path: str) -> bool:
        """Save project with a new file path"""
        return self.save_project(file_path)
    
    def close_project(self) -> bool:
        """Close the current project"""
        try:
            # Check if current project needs saving
            if self.is_modified and not self._prompt_save_current():
                return False
            
            self.current_project = None
            self.current_file_path = None
            self.is_modified = False
            
            print("✓ Project closed")
            return True
            
        except Exception as e:
            print(f"⚠️ Error closing project: {e}")
            return False
    
    def export_project(self, export_path: str, format: str = "json") -> bool:
        """Export project in various formats"""
        try:
            if not self.current_project:
                print("⚠️ No project to export")
                return False
            
            if format.lower() == "json":
                return self._export_as_json(export_path)
            elif format.lower() == "zip":
                return self._export_as_zip(export_path)
            elif format.lower() == "xml":
                return self._export_as_xml(export_path)
            else:
                print(f"⚠️ Unsupported export format: {format}")
                return False
                
        except Exception as e:
            print(f"⚠️ Error exporting project: {e}")
            return False
    
    def import_project(self, import_path: str) -> bool:
        """Import project from various formats"""
        try:
            if not os.path.exists(import_path):
                print(f"⚠️ Import file not found: {import_path}")
                return False
            
            file_ext = os.path.splitext(import_path)[1].lower()
            
            if file_ext == ".json":
                return self.open_project(import_path)
            elif file_ext == ".zip":
                return self._import_from_zip(import_path)
            else:
                print(f"⚠️ Unsupported import format: {file_ext}")
                return False
                
        except Exception as e:
            print(f"⚠️ Error importing project: {e}")
            return False
    
    def get_current_project(self) -> Optional[Project]:
        """Get the current project"""
        return self.current_project
    
    def get_current_file(self) -> Optional[str]:
        """Get current file path"""
        return self.current_file_path
    
    def is_project_modified(self) -> bool:
        """Check if project has unsaved changes"""
        return self.is_modified
    
    def mark_modified(self):
        """Mark project as modified"""
        self.is_modified = True
    
    def get_recent_projects(self) -> List[str]:
        """Get list of recent projects"""
        # Filter out non-existent files
        valid_projects = [p for p in self.recent_projects if os.path.exists(p)]
        if len(valid_projects) != len(self.recent_projects):
            self.recent_projects = valid_projects
            self._save_manager_settings()
        
        return self.recent_projects.copy()
    
    def clear_recent_projects(self):
        """Clear recent projects list"""
        self.recent_projects.clear()
        self._save_manager_settings()
    
    def get_project_info(self) -> Dict[str, Any]:
        """Get information about current project"""
        if not self.current_project:
            return {}
        
        return {
            'name': self.current_project.settings.name,
            'description': self.current_project.settings.description,
            'author': self.current_project.settings.author,
            'version': self.current_project.settings.version,
            'created_date': self.current_project.settings.created_date,
            'modified_date': self.current_project.settings.modified_date,
            'target_system': self.current_project.settings.target_system,
            'file_path': self.current_file_path,
            'is_modified': self.is_modified,
            'component_count': len(self.current_project.components),
            'connection_count': len(self.current_project.connections)
        }
    
    def update_project_settings(self, settings: Dict[str, Any]) -> bool:
        """Update project settings"""
        try:
            if not self.current_project:
                print("⚠️ No project to update")
                return False
            
            # Update settings
            for key, value in settings.items():
                if hasattr(self.current_project.settings, key):
                    setattr(self.current_project.settings, key, value)
            
            # Update modified date
            self.current_project.settings.modified_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.mark_modified()
            
            print("✓ Project settings updated")
            return True
            
        except Exception as e:
            print(f"⚠️ Error updating project settings: {e}")
            return False
    
    def add_component_data(self, component_id: str, component_data: Dict[str, Any]):
        """Add component data to project"""
        if self.current_project:
            self.current_project.components[component_id] = component_data
            self.mark_modified()
    
    def remove_component_data(self, component_id: str):
        """Remove component data from project"""
        if self.current_project and component_id in self.current_project.components:
            del self.current_project.components[component_id]
            self.mark_modified()
    
    def add_connection_data(self, connection_data: Dict[str, Any]):
        """Add connection data to project"""
        if self.current_project:
            self.current_project.connections.append(connection_data)
            self.mark_modified()
    
    def remove_connection_data(self, connection_data: Dict[str, Any]):
        """Remove connection data from project"""
        if self.current_project and connection_data in self.current_project.connections:
            self.current_project.connections.remove(connection_data)
            self.mark_modified()
    
    def update_canvas_state(self, canvas_data: Dict[str, Any]):
        """Update canvas state in project"""
        if self.current_project:
            self.current_project.canvas_state = canvas_data
            self.mark_modified()
    
    def get_canvas_state(self) -> Dict[str, Any]:
        """Get canvas state from project"""
        if self.current_project:
            return self.current_project.canvas_state
        return {}
    
    def set_custom_data(self, key: str, value: Any):
        """Set custom data in project"""
        if self.current_project:
            self.current_project.custom_data[key] = value
            self.mark_modified()
    
    def get_custom_data(self, key: str, default: Any = None) -> Any:
        """Get custom data from project"""
        if self.current_project:
            return self.current_project.custom_data.get(key, default)
        return default
    
    # ========== PRIVATE METHODS ==========
    
    def _prompt_save_current(self) -> bool:
        """Prompt to save current project - override in GUI"""
        # In a console application, always save
        if self.current_file_path:
            return self.save_project()
        else:
            print("⚠️ Current project has unsaved changes but no file path")
            return True  # Continue without saving
    
    def _add_to_recent_projects(self, file_path: str):
        """Add file to recent projects list"""
        # Remove if already exists
        if file_path in self.recent_projects:
            self.recent_projects.remove(file_path)
        
        # Add to beginning
        self.recent_projects.insert(0, file_path)
        
        # Limit list size
        if len(self.recent_projects) > self.max_recent_projects:
            self.recent_projects = self.recent_projects[:self.max_recent_projects]
        
        # Save settings
        self._save_manager_settings()
    
    def _load_project_from_dict(self, data: Dict[str, Any]) -> Optional[Project]:
        """Load project from dictionary data"""
        try:
            # Load settings
            settings_data = data.get('settings', {})
            settings = ProjectSettings(
                name=settings_data.get('name', 'Untitled Project'),
                description=settings_data.get('description', ''),
                author=settings_data.get('author', ''),
                version=settings_data.get('version', '1.0.0'),
                created_date=settings_data.get('created_date', ''),
                modified_date=settings_data.get('modified_date', ''),
                target_system=settings_data.get('target_system', ''),
                grid_size=settings_data.get('grid_size', 20),
                grid_visible=settings_data.get('grid_visible', True),
                snap_to_grid=settings_data.get('snap_to_grid', True),
                active_layer=settings_data.get('active_layer', 'chip'),
                layer_visibility=settings_data.get('layer_visibility', {
                    "chip": True, "pcb": False, "gerber": False
                }),
                export_format=settings_data.get('export_format', 'json'),
                export_path=settings_data.get('export_path', ''),
                simulation_speed=settings_data.get('simulation_speed', 1.0),
                debug_mode=settings_data.get('debug_mode', False)
            )
            
            # Create project
            project = Project(
                settings=settings,
                components=data.get('components', {}),
                connections=data.get('connections', []),
                canvas_state=data.get('canvas_state', {}),
                custom_data=data.get('custom_data', {})
            )
            
            return project
            
        except Exception as e:
            print(f"⚠️ Error loading project from data: {e}")
            return None
    
    def _save_project_to_dict(self, project: Project) -> Dict[str, Any]:
        """Save project to dictionary data"""
        return {
            'metadata': {
                'version': '1.0',
                'type': 'retro_emulator_project',
                'saved_date': time.strftime("%Y-%m-%d %H:%M:%S")
            },
            'settings': {
                'name': project.settings.name,
                'description': project.settings.description,
                'author': project.settings.author,
                'version': project.settings.version,
                'created_date': project.settings.created_date,
                'modified_date': project.settings.modified_date,
                'target_system': project.settings.target_system,
                'grid_size': project.settings.grid_size,
                'grid_visible': project.settings.grid_visible,
                'snap_to_grid': project.settings.snap_to_grid,
                'active_layer': project.settings.active_layer,
                'layer_visibility': project.settings.layer_visibility,
                'export_format': project.settings.export_format,
                'export_path': project.settings.export_path,
                'simulation_speed': project.settings.simulation_speed,
                'debug_mode': project.settings.debug_mode
            },
            'components': project.components,
            'connections': project.connections,
            'canvas_state': project.canvas_state,
            'custom_data': project.custom_data
        }
    
    def _export_as_json(self, export_path: str) -> bool:
        """Export project as JSON"""
        try:
            project_data = self._save_project_to_dict(self.current_project)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Project exported as JSON: {export_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error exporting as JSON: {e}")
            return False
    
    def _export_as_zip(self, export_path: str) -> bool:
        """Export project as ZIP archive"""
        try:
            import zipfile
            
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add main project file
                project_data = self._save_project_to_dict(self.current_project)
                project_json = json.dumps(project_data, indent=2, ensure_ascii=False)
                zipf.writestr('project.json', project_json)
                
                # Add component images if they exist
                images_dir = "images"
                if os.path.exists(images_dir):
                    for root, dirs, files in os.walk(images_dir):
                        for file in files:
                            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path)
                                zipf.write(file_path, arcname)
                
                # Add documentation
                docs = ['README.md', 'CHANGELOG.md', 'LICENSE']
                for doc in docs:
                    if os.path.exists(doc):
                        zipf.write(doc, doc)
            
            print(f"✓ Project exported as ZIP: {export_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error exporting as ZIP: {e}")
            return False
    
    def _export_as_xml(self, export_path: str) -> bool:
        """Export project as XML"""
        try:
            import xml.etree.ElementTree as ET
            
            root = ET.Element("RetroEmulatorProject")
            root.set("version", "1.0")
            
            # Settings
            settings_elem = ET.SubElement(root, "Settings")
            for key, value in self._save_project_to_dict(self.current_project)['settings'].items():
                setting = ET.SubElement(settings_elem, "Setting")
                setting.set("name", key)
                setting.text = str(value)
            
            # Components
            components_elem = ET.SubElement(root, "Components")
            for comp_id, comp_data in self.current_project.components.items():
                comp_elem = ET.SubElement(components_elem, "Component")
                comp_elem.set("id", comp_id)
                for key, value in comp_data.items():
                    if isinstance(value, (str, int, float, bool)):
                        comp_elem.set(key, str(value))
            
            # Connections
            connections_elem = ET.SubElement(root, "Connections")
            for conn_data in self.current_project.connections:
                conn_elem = ET.SubElement(connections_elem, "Connection")
                for key, value in conn_data.items():
                    conn_elem.set(key, str(value))
            
            # Write to file
            tree = ET.ElementTree(root)
            tree.write(export_path, encoding='utf-8', xml_declaration=True)
            
            print(f"✓ Project exported as XML: {export_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error exporting as XML: {e}")
            return False
    
    def _import_from_zip(self, import_path: str) -> bool:
        """Import project from ZIP archive"""
        try:
            import zipfile
            import tempfile
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract ZIP
                with zipfile.ZipFile(import_path, 'r') as zipf:
                    zipf.extractall(temp_dir)
                
                # Look for project.json
                project_file = os.path.join(temp_dir, 'project.json')
                if os.path.exists(project_file):
                    return self.open_project(project_file)
                else:
                    print("⚠️ No project.json found in ZIP archive")
                    return False
                    
        except Exception as e:
            print(f"⚠️ Error importing from ZIP: {e}")
            return False
    
    def auto_save(self) -> bool:
        """Perform auto-save if enabled"""
        if (self.auto_save_enabled and 
            self.is_modified and 
            self.current_file_path):
            
            try:
                # Create backup
                backup_path = self.current_file_path + ".backup"
                if os.path.exists(self.current_file_path):
                    shutil.copy2(self.current_file_path, backup_path)
                
                # Save
                success = self.save_project()
                
                if success:
                    print("✓ Auto-save completed")
                    # Remove backup on successful save
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                else:
                    # Restore backup on failure
                    if os.path.exists(backup_path):
                        shutil.move(backup_path, self.current_file_path)
                
                return success
                
            except Exception as e:
                print(f"⚠️ Auto-save failed: {e}")
                return False
        
        return True
    
    def validate_project(self) -> Tuple[bool, List[str]]:
        """Validate current project"""
        errors = []
        
        if not self.current_project:
            errors.append("No project loaded")
            return False, errors
        
        # Validate settings
        if not self.current_project.settings.name:
            errors.append("Project name is required")
        
        # Validate components
        for comp_id, comp_data in self.current_project.components.items():
            if not isinstance(comp_data, dict):
                errors.append(f"Invalid component data for {comp_id}")
            elif 'type' not in comp_data:
                errors.append(f"Component {comp_id} missing type")
        
        # Validate connections
        component_ids = set(self.current_project.components.keys())
        for i, conn in enumerate(self.current_project.connections):
            if not isinstance(conn, dict):
                errors.append(f"Invalid connection data at index {i}")
                continue
            
            # Check if referenced components exist
            start_comp = conn.get('start_component')
            end_comp = conn.get('end_component')
            
            if start_comp and start_comp not in component_ids:
                errors.append(f"Connection {i} references missing component: {start_comp}")
            
            if end_comp and end_comp not in component_ids:
                errors.append(f"Connection {i} references missing component: {end_comp}")
        
        return len(errors) == 0, errors
    
    def get_project_statistics(self) -> Dict[str, Any]:
        """Get project statistics"""
        if not self.current_project:
            return {}
        
        stats = {
            'total_components': len(self.current_project.components),
            'total_connections': len(self.current_project.connections),
            'components_by_type': {},
            'file_size': 0,
            'creation_date': self.current_project.settings.created_date,
            'last_modified': self.current_project.settings.modified_date
        }
        
        # Count components by type
        for comp_data in self.current_project.components.values():
            comp_type = comp_data.get('type', 'unknown')
            stats['components_by_type'][comp_type] = stats['components_by_type'].get(comp_type, 0) + 1
        
        # Get file size
        if self.current_file_path and os.path.exists(self.current_file_path):
            stats['file_size'] = os.path.getsize(self.current_file_path)
        
        return stats

# Create a global instance for backward compatibility
global_project_manager = ProjectManager()

# Export classes and instance
__all__ = ['Project', 'ProjectSettings', 'ProjectManager', 'global_project_manager']