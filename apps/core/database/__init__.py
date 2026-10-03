"""
X-Seti - June07 2025 - Database Package
Component and project database management
"""

#this belongs in databse/
# Try to import database modules with fallbacks
try:
    from .component_db import ComponentDatabase, ComponentRecord
except ImportError as e:
    print(f"⚠️ Could not import ComponentDatabase: {e}")
    ComponentDatabase = None
    ComponentRecord = None

try:
    from .project_db import ProjectDatabase, ProjectRecord
except ImportError as e:
    print(f"⚠️ Could not import ProjectDatabase: {e}")
    ProjectDatabase = None
    ProjectRecord = None

__all__ = [
    'ComponentDatabase',
    'ComponentRecord',
    'ProjectDatabase', 
    'ProjectRecord'
]

__version__ = '1.0.0'
