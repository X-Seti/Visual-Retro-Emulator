#!/usr/bin/env python3
"""
X-Seti - June23 2025 - Project Manager - Managers Package Version
Provides project management within the managers package structure
"""
#this belongs in managers/project_manager.py

import sys
import os

# Add parent directory to path to import from root
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import from root project_manager and re-export
try:
    from project_manager import (
        ProjectManager as RootProjectManager, 
        Project as RootProject,
        ProjectSettings as RootProjectSettings
    )
    
    # Re-export with same names
    ProjectManager = RootProjectManager
    Project = RootProject
    ProjectSettings = RootProjectSettings
    
    print("✅ Successfully imported project manager components from root")
    
except ImportError as e:
    print(f"⚠️ Could not import from root project_manager: {e}")
    
    # Try importing from core as fallback
    try:
        from core.project_manager import (
            ProjectManager as CoreProjectManager, 
            Project as CoreProject
        )
        
        # Re-export with same names
        ProjectManager = CoreProjectManager
        Project = CoreProject
        
        # Create basic ProjectSettings if not available in core
        class ProjectSettings:
            """Basic project settings fallback"""
            def __init__(self):
                self.name = "Untitled Project"
                self.description = ""
                self.author = ""
                self.version = "1.0.0"
                self.created_date = ""
                self.modified_date = ""
        
        print("✅ Successfully imported project manager from core (with fallback ProjectSettings)")
        
    except ImportError as e2:
        print(f"⚠️ Could not import from core.project_manager: {e2}")
        
        # Create minimal fallback implementations
        class ProjectManager:
            """Fallback project manager"""
            def __init__(self):
                self.current_project = None
                print("⚠️ Using fallback ProjectManager")
                
            def new_project(self, name: str = ""):
                print(f"Creating new project: {name}")
                return None
                
            def open_project(self, path: str):
                print(f"Opening project: {path}")
                return None
                
            def save_project(self, path: str = None):
                print(f"Saving project: {path}")
                return True
                
            def save_current_project(self):
                print("Saving current project")
                return True
                
            def close_project(self):
                print("Closing project")
                self.current_project = None
                
        class Project:
            """Fallback project"""
            def __init__(self, name: str = ""):
                self.name = name
                self.path = ""
                self.components = {}
                self.connections = []
                print(f"⚠️ Using fallback Project: {name}")
        
        class ProjectSettings:
            """Fallback project settings"""
            def __init__(self):
                self.name = "Untitled Project"
                self.description = ""
                self.author = ""
                self.version = "1.0.0"
                self.created_date = ""
                self.modified_date = ""
                self.target_system = ""
                self.grid_size = 20
                self.grid_visible = True
                self.snap_to_grid = True
                print("⚠️ Using fallback ProjectSettings")

# Export all components
__all__ = ['ProjectManager', 'Project', 'ProjectSettings']