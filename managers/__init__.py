"""
Managers Package
Central management systems for the retro emulator
"""

# Import from root level modules and core
try:
    from project_manager import ProjectManager, Project
    from core.project_manager import ProjectManager as CoreProjectManager, Project as CoreProject
except ImportError:
    # Fallback if imports fail
    print("Warning: Could not import project managers")
    ProjectManager = None
    Project = None
    CoreProjectManager = None
    CoreProject = None

try:
    from component_library import ComponentLibrary, component_library
except ImportError:
    print("Warning: Could not import component library")
    ComponentLibrary = None
    component_library = None

try:
    from core.components import ComponentManager
except ImportError:
    print("Warning: Could not import component manager")
    ComponentManager = None

try:
    from core.simulation import SimulationEngine
except ImportError:
    print("Warning: Could not import simulation engine")
    SimulationEngine = None

# Import layer manager
try:
    from .layer_manager import LayerManager, Layer, EnhancedLayerManager
except ImportError:
    print("Warning: Could not import layer manager")
    LayerManager = None
    Layer = None
    EnhancedLayerManager = None

__all__ = [
    'ProjectManager',
    'Project', 
    'CoreProjectManager',
    'CoreProject',
    'ComponentLibrary',
    'component_library',
    'ComponentManager',
    'SimulationEngine',
    'LayerManager',
    'Layer',
    'EnhancedLayerManager'
]

__version__ = '1.0.0'