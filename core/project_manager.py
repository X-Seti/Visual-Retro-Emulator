"""
X-Seti - June07 2025 - Project Management System
Handles project creation, saving, loading, and management
"""

import json
import os
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from PyQt6.QtCore import QObject, pyqtSignal

@dataclass
class ProjectMetadata:
    """Project metadata information"""
    name: str
    description: str
    version: str
    author: str
    created_date: str
    modified_date: str
    tags: List[str]
    target_system: str
    notes: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectMetadata':
        return cls(**data)

class ProjectSignals(QObject):
    """Signals for project events"""
    projectLoaded = pyqtSignal(str)  # project_path
    projectSaved = pyqtSignal(str)   # project_path
    projectClosed = pyqtSignal()
    projectModified = pyqtSignal()
    errorOccurred = pyqtSignal(str)  # error_message

class Project:
    """Represents a single project"""
    
    PROJECT_EXTENSION = '.vrse'  # Visual Retro System Emulator
    METADATA_FILE = 'project.json'
    COMPONENTS_FILE = 'components.json'
    CONNECTIONS_FILE = 'connections.json'
    ASSETS_DIR = 'assets'
    EXPORTS_DIR = 'exports'
    
    def __init__(self, project_path: Optional[str] = None):
        self.project_path = project_path
        self.project_dir = None
        self.metadata: Optional[ProjectMetadata] = None
        self.components_data: Dict[str, Any] = {}
        self.connections_data: List[Tuple[str, str, str, str]] = []
        self.custom_data: Dict[str, Any] = {}
        self.is_modified = False
        self.is_loaded = False
        
        if project_path:
            self.project_dir = self._get_project_dir(project_path)
            
    def _get_project_dir(self, project_path: str) -> str:
        """Get project directory from project path"""
        if project_path.endswith(self.PROJECT_EXTENSION):
            return project_path[:-len(self.PROJECT_EXTENSION)]
        return project_path
        
    def create_new(self, name: str, description: str, author: str, 
                   target_system: str, project_dir: str) -> bool:
        """Create a new project"""
        try:
            # Create project directory
            self.project_dir = os.path.join(project_dir, name)
            os.makedirs(self.project_dir, exist_ok=True)
            
            # Create subdirectories
            os.makedirs(os.path.join(self.project_dir, self.ASSETS_DIR), exist_ok=True)
            os.makedirs(os.path.join(self.project_dir, self.EXPORTS_DIR), exist_ok=True)
            
            # Create metadata
            current_time = datetime.now(timezone.utc).isoformat()
            self.metadata = ProjectMetadata(
                name=name,
                description=description,
                version="1.0.0",
                author=author,
                created_date=current_time,
                modified_date=current_time,
                tags=[],
                target_system=target_system,
                notes=""
            )
            
            # Initialize empty data
            self.components_data = {}
            self.connections_data = []
            self.custom_data = {}
            
            # Save initial project
            self.save()
            self.is_loaded = True
            self.is_modified = False
            
            return True
            
        except Exception as e:
            print(f"Error creating project: {e}")
            return False
            
    def load(self, project_path: str) -> bool:
        """Load an existing project"""
        try:
            self.project_path = project_path
            self.project_dir = self._get_project_dir(project_path)
            
            if not os.path.exists(self.project_dir):
                raise FileNotFoundError(f"Project directory not found: {self.project_dir}")
                
            # Load metadata
            metadata_path = os.path.join(self.project_dir, self.METADATA_FILE)
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata_dict = json.load(f)
                    self.metadata = ProjectMetadata.from_dict(metadata_dict)
            else:
                raise FileNotFoundError("Project metadata file not found")
                
            # Load components
            components_path = os.path.join(self.project_dir, self.COMPONENTS_FILE)
            if os.path.exists(components_path):
                with open(components_path, 'r', encoding='utf-8') as f:
                    self.components_data = json.load(f)
            else:
                self.components_data = {}
                
            # Load connections
            connections_path = os.path.join(self.project_dir, self.CONNECTIONS_FILE)
            if os.path.exists(connections_path):
                with open(connections_path, 'r', encoding='utf-8') as f:
                    connections_list = json.load(f)
                    self.connections_data = [tuple(conn) for conn in connections_list]
            else:
                self.connections_data = []
                
            # Load custom data
            custom_data_path = os.path.join(self.project_dir, 'custom.json')
            if os.path.exists(custom_data_path):
                with open(custom_data_path, 'r', encoding='utf-8') as f:
                    self.custom_data = json.load(f)
            else:
                self.custom_data = {}
                
            self.is_loaded = True
            self.is_modified = False
            
            return True
            
        except Exception as e:
            print(f"Error loading project: {e}")
            return False
            
    def save(self, project_path: Optional[str] = None) -> bool:
        """Save the project"""
        try:
            if project_path:
                self.project_path = project_path
                self.project_dir = self._get_project_dir(project_path)
                
            if not self.project_dir:
                raise ValueError("No project directory specified")
                
            # Ensure directory exists
            os.makedirs(self.project_dir, exist_ok=True)
            
            # Update modification time
            if self.metadata:
                self.metadata.modified_date = datetime.now(timezone.utc).isoformat()
                
                # Save metadata
                metadata_path = os.path.join(self.project_dir, self.METADATA_FILE)
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(self.metadata.to_dict(), f, indent=2)
                    
            # Save components
            components_path = os.path.join(self.project_dir, self.COMPONENTS_FILE)
            with open(components_path, 'w', encoding='utf-8') as f:
                json.dump(self.components_data, f, indent=2)
                
            # Save connections
            connections_path = os.path.join(self.project_dir, self.CONNECTIONS_FILE)
            with open(connections_path, 'w', encoding='utf-8') as f:
                json.dump(self.connections_data, f, indent=2)
                
            # Save custom data
            if self.custom_data:
                custom_data_path = os.path.join(self.project_dir, 'custom.json')
                with open(custom_data_path, 'w', encoding='utf-8') as f:
                    json.dump(self.custom_data, f, indent=2)
                    
            self.is_modified = False
            return True
            
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
            
    def export_to_archive(self, archive_path: str) -> bool:
        """Export project to a compressed archive"""
        try:
            if not self.project_dir or not os.path.exists(self.project_dir):
                return False
                
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.project_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.project_dir)
                        zipf.write(file_path, arcname)
                        
            return True
            
        except Exception as e:
            print(f"Error exporting project: {e}")
            return False
            
    def import_from_archive(self, archive_path: str, extract_dir: str) -> bool:
        """Import project from a compressed archive"""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(extract_dir)
                
            # Find the project directory in the extracted files
            project_name = self.metadata.name if self.metadata else "imported_project"
            self.project_dir = os.path.join(extract_dir, project_name)
            
            # Load the imported project
            return self.load(self.project_dir)
            
        except Exception as e:
            print(f"Error importing project: {e}")
            return False
            
    def add_asset(self, asset_path: str, asset_name: Optional[str] = None) -> bool:
        """Add an asset file to the project"""
        try:
            if not self.project_dir:
                return False
                
            assets_dir = os.path.join(self.project_dir, self.ASSETS_DIR)
            os.makedirs(assets_dir, exist_ok=True)
            
            if not asset_name:
                asset_name = os.path.basename(asset_path)
                
            dest_path = os.path.join(assets_dir, asset_name)
            shutil.copy2(asset_path, dest_path)
            
            self.mark_modified()
            return True
            
        except Exception as e:
            print(f"Error adding asset: {e}")
            return False
            
    def remove_asset(self, asset_name: str) -> bool:
        """Remove an asset from the project"""
        try:
            if not self.project_dir:
                return False
                
            asset_path = os.path.join(self.project_dir, self.ASSETS_DIR, asset_name)
            if os.path.exists(asset_path):
                os.remove(asset_path)
                self.mark_modified()
                return True
            return False
            
        except Exception as e:
            print(f"Error removing asset: {e}")
            return False
            
    def get_assets(self) -> List[str]:
        """Get list of all assets in the project"""
        try:
            if not self.project_dir:
                return []
                
            assets_dir = os.path.join(self.project_dir, self.ASSETS_DIR)
            if os.path.exists(assets_dir):
                return [f for f in os.listdir(assets_dir) 
                       if os.path.isfile(os.path.join(assets_dir, f))]
            return []
            
        except Exception as e:
            print(f"Error getting assets: {e}")
            return []
            
    def get_asset_path(self, asset_name: str) -> Optional[str]:
        """Get full path to an asset"""
        if not self.project_dir:
            return None
            
        asset_path = os.path.join(self.project_dir, self.ASSETS_DIR, asset_name)
        return asset_path if os.path.exists(asset_path) else None
        
    def update_components_data(self, components_data: Dict[str, Any]):
        """Update components data"""
        self.components_data = components_data
        self.mark_modified()
        
    def update_connections_data(self, connections_data: List[Tuple[str, str, str, str]]):
        """Update connections data"""
        self.connections_data = connections_data
        self.mark_modified()
        
    def set_custom_data(self, key: str, value: Any):
        """Set custom data"""
        self.custom_data[key] = value
        self.mark_modified()
        
    def get_custom_data(self, key: str, default: Any = None) -> Any:
        """Get custom data"""
        return self.custom_data.get(key, default)
        
    def mark_modified(self):
        """Mark project as modified"""
        self.is_modified = True
        
    def get_project_info(self) -> Dict[str, Any]:
        """Get project information summary"""
        info = {
            'path': self.project_path,
            'directory': self.project_dir,
            'loaded': self.is_loaded,
            'modified': self.is_modified,
            'components_count': len(self.components_data),
            'connections_count': len(self.connections_data),
            'assets_count': len(self.get_assets())
        }
        
        if self.metadata:
            info.update({
                'name': self.metadata.name,
                'description': self.metadata.description,
                'version': self.metadata.version,
                'author': self.metadata.author,
                'created_date': self.metadata.created_date,
                'modified_date': self.metadata.modified_date,
                'target_system': self.metadata.target_system
            })
            
        return info

class ProjectManager(QObject):
    """Manages multiple projects and project operations"""
    
    # Signals
    projectLoaded = pyqtSignal(str)
    projectSaved = pyqtSignal(str)
    projectClosed = pyqtSignal()
    projectModified = pyqtSignal()
    errorOccurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_project: Optional[Project] = None
        self.recent_projects: List[str] = []
        self.settings_dir = os.path.expanduser("~/.vrse")
        self.recent_projects_file = os.path.join(self.settings_dir, "recent_projects.json")
        self.load_recent_projects()
        
    def create_new_project(self, name: str, description: str, author: str,
                          target_system: str, project_dir: str) -> bool:
        """Create a new project"""
        try:
            # Close current project
            self.close_current_project()
            
            # Create new project
            project = Project()
            if project.create_new(name, description, author, target_system, project_dir):
                self.current_project = project
                self.add_to_recent_projects(project.project_dir)
                self.projectLoaded.emit(project.project_dir)
                return True
            return False
            
        except Exception as e:
            self.errorOccurred.emit(f"Error creating project: {e}")
            return False
            
    def load_project(self, project_path: str) -> bool:
        """Load an existing project"""
        try:
            # Close current project
            self.close_current_project()
            
            # Load project
            project = Project()
            if project.load(project_path):
                self.current_project = project
                self.add_to_recent_projects(project_path)
                self.projectLoaded.emit(project_path)
                return True
            return False
            
        except Exception as e:
            self.errorOccurred.emit(f"Error loading project: {e}")
            return False
            
    def save_current_project(self, project_path: Optional[str] = None) -> bool:
        """Save the current project"""
        try:
            if not self.current_project:
                self.errorOccurred.emit("No project to save")
                return False
                
            if self.current_project.save(project_path):
                save_path = project_path or self.current_project.project_path or self.current_project.project_dir
                self.projectSaved.emit(save_path)
                return True
            return False
            
        except Exception as e:
            self.errorOccurred.emit(f"Error saving project: {e}")
            return False
            
    def close_current_project(self) -> bool:
        """Close the current project"""
        try:
            if self.current_project and self.current_project.is_modified:
                # In a real application, you'd show a dialog asking to save
                # For now, we'll just save automatically
                self.save_current_project()
                
            self.current_project = None
            self.projectClosed.emit()
            return True
            
        except Exception as e:
            self.errorOccurred.emit(f"Error closing project: {e}")
            return False
            
    def export_project(self, archive_path: str) -> bool:
        """Export current project to archive"""
        try:
            if not self.current_project:
                self.errorOccurred.emit("No project to export")
                return False
                
            return self.current_project.export_to_archive(archive_path)
            
        except Exception as e:
            self.errorOccurred.emit(f"Error exporting project: {e}")
            return False
            
    def import_project(self, archive_path: str, extract_dir: str) -> bool:
        """Import project from archive"""
        try:
            # Close current project
            self.close_current_project()
            
            # Import project
            project = Project()
            if project.import_from_archive(archive_path, extract_dir):
                self.current_project = project
                self.add_to_recent_projects(project.project_dir)
                self.projectLoaded.emit(project.project_dir)
                return True
            return False
            
        except Exception as e:
            self.errorOccurred.emit(f"Error importing project: {e}")
            return False
            
    def duplicate_project(self, new_name: str, new_dir: str) -> bool:
        """Duplicate the current project"""
        try:
            if not self.current_project:
                self.errorOccurred.emit("No project to duplicate")
                return False
                
            # Export current project to temporary archive
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
                temp_archive = temp_file.name
                
            if not self.current_project.export_to_archive(temp_archive):
                return False
                
            try:
                # Create new project from archive
                new_project = Project()
                if new_project.import_from_archive(temp_archive, new_dir):
                    # Update metadata
                    if new_project.metadata:
                        new_project.metadata.name = new_name
                        current_time = datetime.now(timezone.utc).isoformat()
                        new_project.metadata.created_date = current_time
                        new_project.metadata.modified_date = current_time
                        
                    # Rename project directory
                    old_dir = new_project.project_dir
                    new_project.project_dir = os.path.join(new_dir, new_name)
                    if os.path.exists(old_dir):
                        shutil.move(old_dir, new_project.project_dir)
                        
                    # Save with new settings
                    new_project.save()
                    return True
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_archive):
                    os.unlink(temp_archive)
                    
            return False
            
        except Exception as e:
            self.errorOccurred.emit(f"Error duplicating project: {e}")
            return False
            
    def add_to_recent_projects(self, project_path: str):
        """Add project to recent projects list"""
        try:
            # Remove if already in list
            if project_path in self.recent_projects:
                self.recent_projects.remove(project_path)
                
            # Add to beginning
            self.recent_projects.insert(0, project_path)
            
            # Keep only last 10
            self.recent_projects = self.recent_projects[:10]
            
            # Save to file
            self.save_recent_projects()
            
        except Exception as e:
            print(f"Error updating recent projects: {e}")
            
    def remove_from_recent_projects(self, project_path: str):
        """Remove project from recent projects list"""
        try:
            if project_path in self.recent_projects:
                self.recent_projects.remove(project_path)
                self.save_recent_projects()
                
        except Exception as e:
            print(f"Error removing from recent projects: {e}")
            
    def save_recent_projects(self):
        """Save recent projects list to file"""
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
            with open(self.recent_projects_file, 'w', encoding='utf-8') as f:
                json.dump(self.recent_projects, f, indent=2)
                
        except Exception as e:
            print(f"Error saving recent projects: {e}")
            
    def load_recent_projects(self):
        """Load recent projects list from file"""
        try:
            if os.path.exists(self.recent_projects_file):
                with open(self.recent_projects_file, 'r', encoding='utf-8') as f:
                    self.recent_projects = json.load(f)
                    
                # Filter out non-existent projects
                self.recent_projects = [
                    path for path in self.recent_projects
                    if os.path.exists(path)
                ]
            else:
                self.recent_projects = []
                
        except Exception as e:
            print(f"Error loading recent projects: {e}")
            self.recent_projects = []
            
    def get_recent_projects(self) -> List[Dict[str, Any]]:
        """Get recent projects with metadata"""
        projects_info = []
        
        for project_path in self.recent_projects:
            try:
                # Try to load project metadata
                project = Project()
                if project.load(project_path):
                    info = project.get_project_info()
                    projects_info.append(info)
                else:
                    # Project couldn't be loaded, remove from recent
                    self.remove_from_recent_projects(project_path)
                    
            except Exception as e:
                print(f"Error loading project info for {project_path}: {e}")
                
        return projects_info
        
    def get_current_project(self) -> Optional[Project]:
        """Get the current project"""
        return self.current_project
        
    def is_project_loaded(self) -> bool:
        """Check if a project is currently loaded"""
        return self.current_project is not None
        
    def is_project_modified(self) -> bool:
        """Check if current project is modified"""
        return self.current_project.is_modified if self.current_project else False
        
    def update_project_components(self, components_data: Dict[str, Any]):
        """Update current project components"""
        if self.current_project:
            self.current_project.update_components_data(components_data)
            self.projectModified.emit()
            
    def update_project_connections(self, connections_data: List[Tuple[str, str, str, str]]):
        """Update current project connections"""
        if self.current_project:
            self.current_project.update_connections_data(connections_data)
            self.projectModified.emit()
            
    def set_project_metadata(self, **kwargs):
        """Update project metadata"""
        if self.current_project and self.current_project.metadata:
            for key, value in kwargs.items():
                if hasattr(self.current_project.metadata, key):
                    setattr(self.current_project.metadata, key, value)
            self.current_project.mark_modified()
            self.projectModified.emit()
            
    def add_project_asset(self, asset_path: str, asset_name: Optional[str] = None) -> bool:
        """Add asset to current project"""
        if self.current_project:
            if self.current_project.add_asset(asset_path, asset_name):
                self.projectModified.emit()
                return True
        return False
        
    def remove_project_asset(self, asset_name: str) -> bool:
        """Remove asset from current project"""
        if self.current_project:
            if self.current_project.remove_asset(asset_name):
                self.projectModified.emit()
                return True
        return False
        
    def get_project_assets(self) -> List[str]:
        """Get list of project assets"""
        if self.current_project:
            return self.current_project.get_assets()
        return []
        
    def get_project_statistics(self) -> Dict[str, Any]:
        """Get current project statistics"""
        if not self.current_project:
            return {}
            
        stats = self.current_project.get_project_info()
        
        # Add additional statistics
        if self.current_project.components_data:
            component_types = {}
            for comp_data in self.current_project.components_data.values():
                comp_type = comp_data.get('type', 'Unknown')
                component_types[comp_type] = component_types.get(comp_type, 0) + 1
            stats['component_types'] = component_types
            
        return stats
        
    def validate_current_project(self) -> Tuple[bool, List[str]]:
        """Validate current project"""
        if not self.current_project:
            return False, ["No project loaded"]
            
        errors = []
        
        # Check project structure
        if not os.path.exists(self.current_project.project_dir):
            errors.append("Project directory does not exist")
            
        # Check required files
        required_files = [Project.METADATA_FILE]
        for req_file in required_files:
            file_path = os.path.join(self.current_project.project_dir, req_file)
            if not os.path.exists(file_path):
                errors.append(f"Required file missing: {req_file}")
                
        # Validate metadata
        if not self.current_project.metadata:
            errors.append("Project metadata is missing")
        elif not self.current_project.metadata.name:
            errors.append("Project name is required")
            
        return len(errors) == 0, errors
        
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            # This would clean up any temporary files created during operations
            pass
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")
            
    def get_project_templates(self) -> List[Dict[str, Any]]:
        """Get available project templates"""
        # This would return predefined project templates
        templates = [
            {
                'name': '8-bit Computer',
                'description': 'Basic 8-bit computer with CPU, RAM, and I/O',
                'target_system': '8-bit',
                'components': ['6502 CPU', 'RAM 64KB', '6522 VIA'],
                'template_file': 'templates/8bit_computer.json'
            },
            {
                'name': 'Game Console',
                'description': 'Retro game console with graphics and audio',
                'target_system': 'Console',
                'components': ['Z80 CPU', 'VIC-II', 'SID 6581', 'Joystick'],
                'template_file': 'templates/game_console.json'
            },
            {
                'name': 'Microcontroller',
                'description': 'Simple microcontroller system',
                'target_system': 'Microcontroller',
                'components': ['68000 CPU', 'ROM 32KB', '8255 PPI'],
                'template_file': 'templates/microcontroller.json'
            }
        ]
        return templates
        
    def create_from_template(self, template_name: str, project_name: str,
                           project_dir: str, author: str) -> bool:
        """Create new project from template"""
        try:
            templates = self.get_project_templates()
            template = next((t for t in templates if t['name'] == template_name), None)
            
            if not template:
                self.errorOccurred.emit(f"Template not found: {template_name}")
                return False
                
            # Create basic project
            if self.create_new_project(
                project_name,
                template['description'],
                author,
                template['target_system'],
                project_dir
            ):
                # Load template data if file exists
                template_file = template.get('template_file')
                if template_file and os.path.exists(template_file):
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        
                    # Apply template data to current project
                    if 'components' in template_data:
                        self.update_project_components(template_data['components'])
                    if 'connections' in template_data:
                        self.update_project_connections(template_data['connections'])
                        
                self.save_current_project()
                return True
                
            return False
            
        except Exception as e:
            self.errorOccurred.emit(f"Error creating from template: {e}")
            return False
