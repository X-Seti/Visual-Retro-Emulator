"""
X-Seti - June07 2025 - Core Simulation Engine
Retro computer simulation and emulation engine
"""

#this goes in core/
import threading
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

class SimulationState(Enum):
    """Simulation states"""
    STOPPED = "stopped"
    RUNNING = "running" 
    PAUSED = "paused"
    ERROR = "error"

@dataclass
class Signal:
    """Represents an electrical signal"""
    name: str
    value: int = 0
    width: int = 1  # bit width
    timestamp: float = 0.0
    
    def set_value(self, value: int):
        """Set signal value with timestamp"""
        self.value = value
        self.timestamp = time.time()

@dataclass
class SimulationConfig:
    """Simulation configuration"""
    clock_speed: int = 1000000  # 1MHz default
    time_step: float = 0.000001  # 1 microsecond
    max_iterations: int = 10000
    debug_mode: bool = False
    trace_signals: bool = False

class SimulationBus:
    """Communication bus for components"""
    
    def __init__(self, name: str, width: int = 8):
        self.name = name
        self.width = width
        self.signals: Dict[str, Signal] = {}
        self.listeners: List[Callable] = []
        self._lock = threading.Lock()
    
    def add_signal(self, name: str, width: int = 1) -> Signal:
        """Add a signal to the bus"""
        with self._lock:
            signal = Signal(name, width=width)
            self.signals[name] = signal
            return signal
    
    def set_signal(self, name: str, value: int):
        """Set signal value"""
        with self._lock:
            if name in self.signals:
                self.signals[name].set_value(value)
                self._notify_listeners(name, value)
    
    def get_signal(self, name: str) -> Optional[Signal]:
        """Get signal by name"""
        return self.signals.get(name)
    
    def add_listener(self, callback: Callable):
        """Add signal change listener"""
        self.listeners.append(callback)
    
    def _notify_listeners(self, signal_name: str, value: int):
        """Notify all listeners of signal change"""
        for listener in self.listeners:
            try:
                listener(signal_name, value)
            except Exception as e:
                print(f"Bus listener error: {e}")

class DebugInterface:
    """Debug interface for simulation"""
    
    def __init__(self):
        self.breakpoints: List[int] = []
        self.watch_signals: List[str] = []
        self.trace_log: List[Dict[str, Any]] = []
        self.max_trace_entries = 1000
    
    def add_breakpoint(self, address: int):
        """Add breakpoint at address"""
        if address not in self.breakpoints:
            self.breakpoints.append(address)
    
    def remove_breakpoint(self, address: int):
        """Remove breakpoint"""
        if address in self.breakpoints:
            self.breakpoints.remove(address)
    
    def add_watch_signal(self, signal_name: str):
        """Add signal to watch list"""
        if signal_name not in self.watch_signals:
            self.watch_signals.append(signal_name)
    
    def log_trace(self, component: str, action: str, data: Any):
        """Log trace entry"""
        entry = {
            'timestamp': time.time(),
            'component': component,
            'action': action,
            'data': data
        }
        self.trace_log.append(entry)
        
        # Limit trace log size
        if len(self.trace_log) > self.max_trace_entries:
            self.trace_log.pop(0)
    
    def get_recent_traces(self, count: int = 100) -> List[Dict[str, Any]]:
        """Get recent trace entries"""
        return self.trace_log[-count:]

class SimulationEngine:
    """Main simulation engine"""
    
    def __init__(self, component_manager=None):
        self.component_manager = component_manager
        self.config = SimulationConfig()
        self.state = SimulationState.STOPPED
        self.buses: Dict[str, SimulationBus] = {}
        self.debug = DebugInterface()
        self.components: List[Any] = []
        
        # Threading
        self._simulation_thread = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        
        # Timing
        self.simulation_time = 0.0
        self.cycle_count = 0
        
        # Create default buses
        self._create_default_buses()
        
        print("✓ SimulationEngine initialized")
    
    def _create_default_buses(self):
        """Create standard buses"""
        self.buses['address'] = SimulationBus('address', 16)
        self.buses['data'] = SimulationBus('data', 8)
        self.buses['control'] = SimulationBus('control', 8)
        
        # Add common control signals
        self.buses['control'].add_signal('clock')
        self.buses['control'].add_signal('reset')
        self.buses['control'].add_signal('read')
        self.buses['control'].add_signal('write')
    
    def add_component(self, component):
        """Add component to simulation"""
        if component not in self.components:
            self.components.append(component)
            
            # Connect component to buses if it has the interface
            if hasattr(component, 'connect_to_bus'):
                for bus_name, bus in self.buses.items():
                    component.connect_to_bus(bus_name, bus)
    
    def remove_component(self, component):
        """Remove component from simulation"""
        if component in self.components:
            self.components.remove(component)
    
    def start_simulation(self):
        """Start the simulation"""
        if self.state != SimulationState.STOPPED:
            return False
        
        self.state = SimulationState.RUNNING
        self._stop_event.clear()
        self._pause_event.clear()
        
        self._simulation_thread = threading.Thread(target=self._simulation_loop)
        self._simulation_thread.daemon = True
        self._simulation_thread.start()
        
        print("✓ Simulation started")
        return True
    
    def stop_simulation(self):
        """Stop the simulation"""
        if self.state == SimulationState.STOPPED:
            return
        
        self._stop_event.set()
        self.state = SimulationState.STOPPED
        
        if self._simulation_thread:
            self._simulation_thread.join(timeout=1.0)
        
        print("✓ Simulation stopped")
    
    def pause_simulation(self):
        """Pause the simulation"""
        if self.state == SimulationState.RUNNING:
            self._pause_event.set()
            self.state = SimulationState.PAUSED
    
    def resume_simulation(self):
        """Resume paused simulation"""
        if self.state == SimulationState.PAUSED:
            self._pause_event.clear()
            self.state = SimulationState.RUNNING
    
    def _simulation_loop(self):
        """Main simulation loop"""
        try:
            while not self._stop_event.is_set():
                # Check for pause
                while self._pause_event.is_set() and not self._stop_event.is_set():
                    time.sleep(0.01)
                
                if self._stop_event.is_set():
                    break
                
                # Execute one simulation step
                self._simulation_step()
                
                # Timing control
                time.sleep(self.config.time_step)
                
                # Check iteration limit
                if self.cycle_count >= self.config.max_iterations:
                    print("⚠️ Simulation reached maximum iterations")
                    break
                    
        except Exception as e:
            print(f"❌ Simulation error: {e}")
            self.state = SimulationState.ERROR
        finally:
            self.state = SimulationState.STOPPED
    
    def _simulation_step(self):
        """Execute one simulation step"""
        self.cycle_count += 1
        self.simulation_time += self.config.time_step
        
        # Generate clock signal
        clock_state = 1 if (self.cycle_count % 2) == 0 else 0
        self.buses['control'].set_signal('clock', clock_state)
        
        # Update all components
        for component in self.components:
            if hasattr(component, 'simulation_step'):
                try:
                    component.simulation_step(self.simulation_time)
                except Exception as e:
                    if self.config.debug_mode:
                        print(f"Component {component} error: {e}")
        
        # Debug tracing
        if self.config.trace_signals:
            self._trace_signals()
    
    def _trace_signals(self):
        """Trace signal states for debugging"""
        trace_data = {}
        for bus_name, bus in self.buses.items():
            bus_data = {}
            for signal_name, signal in bus.signals.items():
                bus_data[signal_name] = signal.value
            trace_data[bus_name] = bus_data
        
        self.debug.log_trace('system', 'signal_trace', trace_data)
    
    def reset_simulation(self):
        """Reset simulation state"""
        was_running = self.state == SimulationState.RUNNING
        
        if was_running:
            self.stop_simulation()
        
        # Reset state
        self.simulation_time = 0.0
        self.cycle_count = 0
        self.debug.trace_log.clear()
        
        # Reset buses
        for bus in self.buses.values():
            for signal in bus.signals.values():
                signal.set_value(0)
        
        # Reset components
        for component in self.components:
            if hasattr(component, 'reset'):
                component.reset()
        
        # Generate reset pulse
        self.buses['control'].set_signal('reset', 1)
        time.sleep(0.001)  # Brief reset pulse
        self.buses['control'].set_signal('reset', 0)
        
        if was_running:
            self.start_simulation()
        
        print("✓ Simulation reset")
    
    def get_bus_state(self, bus_name: str) -> Dict[str, Any]:
        """Get current state of a bus"""
        if bus_name not in self.buses:
            return {}
        
        bus = self.buses[bus_name]
        state = {}
        for signal_name, signal in bus.signals.items():
            state[signal_name] = {
                'value': signal.value,
                'timestamp': signal.timestamp,
                'width': signal.width
            }
        return state
    
    def get_simulation_stats(self) -> Dict[str, Any]:
        """Get simulation statistics"""
        return {
            'state': self.state.value,
            'simulation_time': self.simulation_time,
            'cycle_count': self.cycle_count,
            'components_count': len(self.components),
            'buses_count': len(self.buses),
            'clock_speed': self.config.clock_speed,
            'debug_mode': self.config.debug_mode
        }
