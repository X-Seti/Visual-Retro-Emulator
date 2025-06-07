"""
Project Manager
X-Seti - June07 2025 - Handles project operations for the visual retro emulator
This imports from core.project_manager and provides compatibility
"""

# Import everything from the core project manager
try:
    from core.project_manager import *
    from core.project_manager import ProjectManager as CoreProjectManager
    from core.project_manager import Project as CoreProject
    
    # Create aliases for backward compatibility
    ProjectManager = CoreProjectManager
    Project = CoreProject
    
except ImportError as e:
    # Fallback for when core module isn't available
    print(f"Warning: core.project_manager not found ({e}), using fallback implementation")
    
    import json
    import os
    from datetime import datetime
    from typing import Dict, List, Any, Optional
    
    class Project:
        """Simple fallback project implementation"""
        
        def __init__(self):
            self.name = ""
            self.path = ""
            self.components = {}
            self.connections = []
            self.metadata = {}
            
        def save(self, path: str) -> bool:
            """Save project to file"""
            try:
                project_data = {
                    'name': self.name,
                    'components': self.components,
                    'connections': self.connections,
                    'metadata': self.metadata,
                    'saved_at': datetime.now().isoformat()
                }
                
                with open(path, 'w') as f:
                    json.dump(project_data, f, indent=2)
                    
                self.path = path
                return True
            except Exception as e:
                print(f"Error saving project: {e}")
                return False
                
        def load(self, path: str) -> bool:
            """Load project from file"""
            try:
                with open(path, 'r') as f:
                    project_data = json.load(f)
                    
                self.name = project_data.get('name', '')
                self.components = project_data.get('components', {})
                self.connections = project_data.get('connections', [])
                self.metadata = project_data.get('metadata', {})
                self.path = path
                
                return True
            except Exception as e:
                print(f"Error loading project: {e}")
                return False
    
    class ProjectManager:
        """Simple fallback project manager"""
        
        def __init__(self):
            self.current_project = None
            self.recent_projects = []
            
        def new_project(self, name: str) -> Project:
            """Create a new project"""
            project = Project()
            project.name = name
            self.current_project = project
            return project
            
        def open_project(self, path: str) -> Optional[Project]:
            """Open an existing project"""
            project = Project()
            if project.load(path):
                self.current_project = project
                return project
            return None
            
        def save_project(self, path: str = None) -> bool:
            """Save current project"""
            if self.current_project:
                save_path = path or self.current_project.path
                return self.current_project.save(save_path)
            return False
            
        def close_project(self):
            """Close current project"""
            self.current_project = None
