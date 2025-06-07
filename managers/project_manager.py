"""
Project Manager - Managers Package Version
Provides project management within the managers package structure
"""

import sys
import os

# Add parent directory to path to import from root
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import from root project_manager
try:
    from project_manager import ProjectManager as RootProjectManager, Project as RootProject
    
    # Re-export with same names
    ProjectManager = RootProjectManager
    Project = RootProject
    
    print("✅ Successfully imported project manager from root")
    
except ImportError as e:
    print(f"⚠️ Could not import from root project_manager: {e}")
    
    # Try importing from core
    try:
        from core.project_manager import ProjectManager as CoreProjectManager, Project as CoreProject
        
        # Re-export with same names
        ProjectManager = CoreProjectManager
        Project = CoreProject
        
        print("✅ Successfully imported project manager from core")
        
    except ImportError as e2:
        print(f"⚠️ Could not import from core.project_manager: {e2}")
        
        # Create minimal fallback
        class ProjectManager:
            """Fallback project manager"""
            def __init__(self):
                self.current_project = None
                print("⚠️ Using fallback ProjectManager")
                
            def new_project(self, name: str):
                print(f"Creating new project: {name}")
                return None
                
            def open_project(self, path: str):
                print(f"Opening project: {path}")
                return None
                
            def save_project(self, path: str = None):
                print(f"Saving project: {path}")
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

# Make available for import
__all__ = ['ProjectManager', 'Project']