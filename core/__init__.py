"""
X-Seti - June07 2025 - Core Package
Visual Retro System Emulator Builder - Core System Components
"""

from .components import (
    BaseComponent, ProcessorComponent, MemoryComponent, 
    GraphicsComponent, AudioComponent, IOComponent,
    ComponentPort, ComponentFactory, ComponentManager
)
from .project_manager import Project, ProjectManager, ProjectMetadata
from .simulation import SimulationEngine, SimulationConfig, Signal, SimulationBus, DebugInterface

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
