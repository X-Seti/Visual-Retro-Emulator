"""
X-Seti - June07 2025 - Managers Package
Project and Layer Management System
"""
#this belongs in managers/
# Import only what actually exists and works
try:
    from .project_manager import ProjectManager, Project, ProjectSettings
    print("✓ Successfully imported from managers.project_manager")
except ImportError as e:
    print(f"⚠️ Could not import from managers.project_manager: {e}")
    ProjectManager = None
    Project = None
    ProjectSettings = None

try:
    from .layer_manager import LayerManager
    print("✓ Successfully imported LayerManager")
except ImportError as e:
    print(f"⚠️ Could not import LayerManager: {e}")
    LayerManager = None

# Don't try to import ProjectMetadata from here - it's in the root project_manager.py
# Let other modules import it directly from where it actually exists

__all__ = [
    'ProjectManager',
    'Project', 
    'ProjectSettings',
    'LayerManager'
]

__version__ = '1.0.0'
