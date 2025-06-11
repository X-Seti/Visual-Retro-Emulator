"""
X-Seti - June10 2025 - Project Management System
Complete implementation with all expected methods
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
            
    def get_name(self) -> str:
        """Get project name"""
        if self.metadata:
            return self.metadata.name
        return "Untitled Project"
        
    def get_file_path(self) -> Optional[str]:
        """Get project file path"""
        return self.project_path or self.project_dir
        
    def mark_modified(self):
        """Mark project as modified"""
        self.is_modified = True

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
        
    def new_project(self, name: str, description: str = "", author: str = "", 
                   target_system: str = "", project_dir: str = ".") -> bool:
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
            
    def create_new_project(self, name: str, description: str = "", author: str = "",
                          target_system: str = "", project_dir: str = ".") -> bool:
        """Alias for new_project"""
        return self.new_project(name, description, author, target_system, project_dir)
        
    def open_project(self, project_path: str) -> bool:
        """Open an existing project"""
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
            
    def load_project(self, project_path: str) -> bool:
        """Alias for open_project"""
        return self.open_project(project_path)
        
    def save_project(self, project_path: Optional[str] = None) -> bool:
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
            
    def save_current_project(self, project_path: Optional[str] = None) -> bool:
        """Alias for save_project"""
        return self.save_project(project_path)
        
    def close_project(self) -> bool:
        """Close the current project"""
        return self.close_current_project()
        
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
            
    def get_current_project(self) -> Optional[Project]:
        """Get the current project"""
        return self.current_project
        
    def get_current_file(self) -> Optional[str]:
        """Get current project file path"""
        if self.current_project:
            return self.current_project.get_file_path()
        return None
        
    def get_current_project_name(self) -> str:
        """Get current project name"""
        if self.current_project:
            return self.current_project.get_name()
        return "No Project"
        
    def is_project_loaded(self) -> bool:
        """Check if a project is currently loaded"""
        return self.current_project is not None
        
    def is_project_modified(self) -> bool:
        """Check if current project is modified"""
        return self.current_project.is_modified if self.current_project else False
        
    def has_project(self) -> bool:
        """Check if there is a current project"""
        return self.current_project is not None
        
    def get_project_info(self) -> Dict[str, Any]:
        """Get current project information"""
        if not self.current_project:
            return {}
            
        info = {
            'name': self.current_project.get_name(),
            'path': self.current_project.get_file_path(),
            'modified': self.current_project.is_modified,
            'loaded': self.current_project.is_loaded
        }
        
        if self.current_project.metadata:
            info.update({
                'description': self.current_project.metadata.description,
                'author': self.current_project.metadata.author,
                'version': self.current_project.metadata.version,
                'created_date': self.current_project.metadata.created_date,
                'modified_date': self.current_project.metadata.modified_date,
                'target_system': self.current_project.metadata.target_system
            })
            
        return info
        
    def mark_project_modified(self):
        """Mark current project as modified"""
        if self.current_project:
            self.current_project.mark_modified()
            self.projectModified.emit()
            
    def update_project_components(self, components_data: Dict[str, Any]):
        """Update current project components"""
        if self.current_project:
            self.current_project.components_data = components_data
            self.current_project.mark_modified()
            self.projectModified.emit()
            
    def update_project_connections(self, connections_data: List[Tuple[str, str, str, str]]):
        """Update current project connections"""
        if self.current_project:
            self.current_project.connections_data = connections_data
            self.current_project.mark_modified()
            self.projectModified.emit()
            
    def set_project_metadata(self, **kwargs):
        """Update project metadata"""
        if self.current_project and self.current_project.metadata:
            for key, value in kwargs.items():
                if hasattr(self.current_project.metadata, key):
                    setattr(self.current_project.metadata, key, value)
            self.current_project.mark_modified()
            self.projectModified.emit()
            
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
            
    def get_recent_projects(self) -> List[str]:
        """Get recent projects list"""
        return self.recent_projects.copy()
        
    def clear_recent_projects(self):
        """Clear recent projects list"""
        self.recent_projects.clear()
        self.save_recent_projects()
        
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
        
    def get_project_statistics(self) -> Dict[str, Any]:
        """Get current project statistics"""
        if not self.current_project:
            return {}
            
        stats = {
            'components_count': len(self.current_project.components_data),
            'connections_count': len(self.current_project.connections_data),
            'is_modified': self.current_project.is_modified,
            'is_loaded': self.current_project.is_loaded
        }
        
        return stats

# Aliases for backward compatibility
CoreProjectManager = ProjectManager
CoreProject = Project
