"""
X-Seti - June07 2025 - Hardware Module
Basic hardware components for the retro emulator
"""

# This is a fallback hardware module
# Re-export components from core.components

try:
    from core.components import (
        BaseComponent, ProcessorComponent, MemoryComponent,
        HardwareComponent, ComponentManager, ComponentFactory
    )
    
    # Try to import graphics components
    try:
        from core.components import GraphicsComponent, AudioComponent, IOComponent
    except ImportError:
        # If they don't exist yet, create simple placeholders
        GraphicsComponent = HardwareComponent
        AudioComponent = HardwareComponent  
        IOComponent = HardwareComponent
        
except ImportError as e:
    print(f"⚠️ Could not import from core.components: {e}")
    
    # Create minimal fallback classes
    class BaseComponent:
        def __init__(self, component_type="unknown", name=None, parent=None):
            self.component_type = component_type
            self.name = name or f"{component_type}_component"
            self.parent = parent
    
    HardwareComponent = BaseComponent
    ProcessorComponent = BaseComponent
    MemoryComponent = BaseComponent
    GraphicsComponent = BaseComponent
    AudioComponent = BaseComponent
    IOComponent = BaseComponent
    ComponentManager = None
    ComponentFactory = None

__all__ = [
    'BaseComponent', 'HardwareComponent', 'ProcessorComponent', 
    'MemoryComponent', 'GraphicsComponent', 'AudioComponent', 
    'IOComponent', 'ComponentManager', 'ComponentFactory'
]
