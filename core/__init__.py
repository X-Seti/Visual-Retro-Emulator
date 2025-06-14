"""
X-Seti - June07 2025 - Core Package
Visual Retro System Emulator Builder - Core System Components
"""
#this belongs in core/
# Import components with fallbacks
try:
    from .components import (
        BaseComponent, ProcessorComponent, MemoryComponent, 
        GraphicsComponent, AudioComponent, IOComponent,
        ComponentPort, ComponentFactory, ComponentManager
    )
except ImportError as e:
    print(f"⚠️ Some core components not available: {e}")
    # Import what we can
    try:
        from .components import BaseComponent, ComponentManager
        print("✓ Basic components imported")
    except ImportError as e2:
        print(f"❌ Critical component import failed: {e2}")
        BaseComponent = None
        ComponentManager = None
    
    # Set missing components to None
    ProcessorComponent = None
    MemoryComponent = None  
    GraphicsComponent = None
    AudioComponent = None
    IOComponent = None
    ComponentPort = None
    ComponentFactory = None

# Import project management with fallbacks
try:
    from .project_manager import Project, ProjectManager
except ImportError as e:
    print(f"⚠️ Project management not available in core: {e}")
    Project = None
    ProjectManager = None
    ProjectMetadata = None

# Import simulation with fallbacks
try:
    from .simulation import SimulationEngine, SimulationConfig, Signal, SimulationBus, DebugInterface
except ImportError as e:
    print(f"⚠️ Simulation engine not available: {e}")
    SimulationEngine = None
    SimulationConfig = None
    Signal = None
    SimulationBus = None
    DebugInterface = None

__all__ = [
    # Component system
    'BaseComponent',
    'ProcessorComponent', 
    'MemoryComponent',
    'GraphicsComponent',
    'AudioComponent',
    'IOComponent',
    'ComponentPort',
    'ComponentFactory',
    'ComponentManager',
    
    # Project management
    'Project',
    'ProjectManager', 
    'ProjectMetadata',
    
    # Simulation system
    'SimulationEngine',
    'SimulationConfig',
    'Signal',
    'SimulationBus',
    'DebugInterface'
]

__version__ = '1.0.0'
__author__ = 'Visual Retro System Emulator Builder Team'

# Note: ProjectMetadata is available in the root project_manager.py
# Import it directly from there if needed: from project_manager import ProjectMetadata
