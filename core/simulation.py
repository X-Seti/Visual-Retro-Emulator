"""
X-Seti - June07 2025 - Simulation Engine
Handles real-time simulation of the hardware system
"""

import time
import threading
from typing import Dict, List, Any, Optional, Callable, Tuple
from enum import Enum
from dataclasses import dataclass
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from core.components import BaseComponent, ComponentManager

class SimulationState(Enum):
    """Simulation states"""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    STEP = "step"
    ERROR = "error"

@dataclass
class SimulationConfig:
    """Simulation configuration"""
    clock_frequency: float = 1.0  # MHz
    max_cycles: int = -1  # -1 for unlimited
    real_time: bool = True
    step_mode: bool = False
    debug_mode: bool = False
    log_level: str = "INFO"
    
class Signal:
    """Represents a digital signal"""
    
    def __init__(self, name: str, bit_width: int = 1):
        self.name = name
        self.bit_width = bit_width
        self.value = 0
        self.previous_value = 0
        self.timestamp = 0.0
        self.history: List[tuple] = []  # (timestamp, value)
        
    def set_value(self, value: int, timestamp: float):
        """Set signal value with timestamp"""
        self.previous_value = self.value
        self.value = value & ((1 << self.bit_width) - 1)  # Mask to bit width
        self.timestamp = timestamp
        
        # Add to history
        self.history.append((timestamp, self.value))
        
        # Keep limited history
        if len(self.history) > 1000:
            self.history = self.history[-500:]
            
    def get_bit(self, bit_index: int) -> int:
        """Get specific bit value"""
        if 0 <= bit_index < self.bit_width:
            return (self.value >> bit_index) & 1
        return 0
        
    def set_bit(self, bit_index: int, value: int, timestamp: float):
        """Set specific bit value"""
        if 0 <= bit_index < self.bit_width:
            if value:
                new_value = self.value | (1 << bit_index)
            else:
                new_value = self.value & ~(1 << bit_index)
            self.set_value(new_value, timestamp)
            
    def is_rising_edge(self) -> bool:
        """Check if signal has rising edge"""
        return self.previous_value == 0 and self.value != 0
        
    def is_falling_edge(self) -> bool:
        """Check if signal has falling edge"""
        return self.previous_value != 0 and self.value == 0
        
    def has_changed(self) -> bool:
        """Check if signal value changed"""
        return self.value != self.previous_value

class SimulationBus:
    """Represents a bus connecting multiple components"""
    
    def __init__(self, name: str, bit_width: int):
        self.name = name
        self.bit_width = bit_width
        self.signals: Dict[str, Signal] = {}
        self.connected_components: List[BaseComponent] = []
        self.drivers: List[str] = []  # Components that can drive the bus
        
    def add_signal(self, signal_name: str) -> Signal:
        """Add a signal to the bus"""
        signal = Signal(f"{self.name}.{signal_name}", self.bit_width)
        self.signals[signal_name] = signal
        return signal
        
    def connect_component(self, component: BaseComponent, port_name: str, is_driver: bool = False):
        """Connect a component to the bus"""
        if component not in self.connected_components:
            self.connected_components.append(component)
            
        if is_driver:
            comp_id = f"{component.id}.{port_name}"
            if comp_id not in self.drivers:
                self.drivers.append(comp_id)
                
    def drive_bus(self, driver_id: str, value: int, timestamp: float):
        """Drive the bus with a value from a specific driver"""
        if driver_id in self.drivers:
            for signal in self.signals.values():
                signal.set_value(value, timestamp)
                
    def read_bus(self) -> int:
        """Read current bus value"""
        # For simplicity, return the value of the first signal
        if self.signals:
            return list(self.signals.values())[0].value
        return 0

class SimulationEngine(QObject):
    """Main simulation engine"""
    
    # Signals
    stateChanged = pyqtSignal(str)  # SimulationState
    cycleCompleted = pyqtSignal(int)  # cycle_number
    componentStateChanged = pyqtSignal(str, dict)  # component_id, state
    errorOccurred = pyqtSignal(str)  # error_message
    statisticsUpdated = pyqtSignal(dict)  # statistics
    
    def __init__(self, component_manager: ComponentManager):
        super().__init__()
        self.component_manager = component_manager
        self.config = SimulationConfig()
        self.state = SimulationState.STOPPED
        
        # Simulation state
        self.current_cycle = 0
        self.simulation_time = 0.0  # in seconds
        self.start_time = 0.0
        self.last_update_time = 0.0
        
        # Simulation data
        self.buses: Dict[str, SimulationBus] = {}
        self.signals: Dict[str, Signal] = {}
        self.event_queue: List[tuple] = []  # (timestamp, event_type, data)
        
        # Performance tracking
        self.cycles_per_second = 0.0
        self.actual_frequency = 0.0
        self.simulation_ratio = 1.0  # actual_freq / target_freq
        
        # Threading
        self.simulation_thread: Optional[threading.Thread] = None
        self.stop_requested = False
        self.pause_requested = False
        
        # Timer for real-time simulation
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulation_step)
        
        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = {}
        
    def configure(self, config: SimulationConfig):
        """Configure simulation parameters"""
        self.config = config
        
        # Update timer interval for real-time mode
        if self.config.real_time and self.config.clock_frequency > 0:
            # Calculate timer interval in milliseconds
            interval = int(1000.0 / (self.config.clock_frequency * 1000000))  # Convert MHz to Hz
            interval = max(1, interval)  # Minimum 1ms
            self.timer.setInterval(interval)
            
    def add_event_handler(self, event_type: str, handler: Callable):
        """Add event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        
    def remove_event_handler(self, event_type: str, handler: Callable):
        """Remove event handler"""
        if event_type in self.event_handlers:
            if handler in self.event_handlers[event_type]:
                self.event_handlers[event_type].remove(handler)
                
    def emit_event(self, event_type: str, data: Any = None):
        """Emit simulation event"""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Error in event handler: {e}")
                    
    def create_bus(self, name: str, bit_width: int) -> SimulationBus:
        """Create a new bus"""
        bus = SimulationBus(name, bit_width)
        self.buses[name] = bus
        return bus
        
    def create_signal(self, name: str, bit_width: int = 1) -> Signal:
        """Create a new signal"""
        signal = Signal(name, bit_width)
        self.signals[name] = signal
        return signal
        
    def connect_components(self):
        """Connect components to simulation buses and signals"""
        self.buses.clear()
        self.signals.clear()
        
        # Create standard buses
        data_bus = self.create_bus("data", 8)
        address_bus = self.create_bus("address", 16)
        
        # Create control signals
        clock_signal = self.create_signal("clock")
        reset_signal = self.create_signal("reset")
        read_write_signal = self.create_signal("rw")
        
        # Connect components to buses
        for component in self.component_manager.components.values():
            self._connect_component_to_simulation(component)
            
    def _connect_component_to_simulation(self, component: BaseComponent):
        """Connect a single component to simulation"""
        # Connect data ports to data bus
        for port in component.getPortsOfType('data'):
            if 'data' in self.buses:
                self.buses['data'].connect_component(
                    component, port.name, 
                    port.direction in ['output', 'bidirectional']
                )
                
        # Connect address ports to address bus
        for port in component.getPortsOfType('address'):
            if 'address' in self.buses:
                self.buses['address'].connect_component(
                    component, port.name,
                    port.direction == 'output'
                )
                
        # Connect control signals
        for port in component.getPortsOfType('control'):
            signal_name = f"{component.id}_{port.name}"
            signal = self.create_signal(signal_name)
            
        # Connect clock signals
        for port in component.getPortsOfType('clock'):
            if 'clock' in self.signals:
                # Component is connected to main clock
                pass
                
    def start_simulation(self):
        """Start the simulation"""
        if self.state in [SimulationState.RUNNING, SimulationState.STEP]:
            return
            
        try:
            # Initialize simulation
            self.current_cycle = 0
            self.simulation_time = 0.0
            self.start_time = time.time()
            self.last_update_time = self.start_time
            
            # Connect components
            self.connect_components()
            
            # Initialize all components
            for component in self.component_manager.components.values():
                component.simulation_active = True
                component.reset()
                
            # Set state and start
            self.state = SimulationState.RUNNING
            self.stateChanged.emit(self.state.value)
            
            if self.config.real_time:
                # Use timer for real-time simulation
                self.timer.start()
            else:
                # Use separate thread for fast simulation
                self.stop_requested = False
                self.simulation_thread = threading.Thread(target=self._simulation_loop)
                self.simulation_thread.daemon = True
                self.simulation_thread.start()
                
        except Exception as e:
            self.state = SimulationState.ERROR
            self.stateChanged.emit(self.state.value)
            self.errorOccurred.emit(f"Error starting simulation: {e}")
            
    def stop_simulation(self):
        """Stop the simulation"""
        if self.state == SimulationState.STOPPED:
            return
            
        self.stop_requested = True
        self.timer.stop()
        
        # Wait for simulation thread to finish
        if self.simulation_thread and self.simulation_thread.is_alive():
            self.simulation_thread.join(timeout=1.0)
            
        # Reset components
        for component in self.component_manager.components.values():
            component.simulation_active = False
            component.reset()
            
        self.state = SimulationState.STOPPED
        self.stateChanged.emit(self.state.value)
        
    def pause_simulation(self):
        """Pause the simulation"""
        if self.state == SimulationState.RUNNING:
            self.pause_requested = True
            self.timer.stop()
            self.state = SimulationState.PAUSED
            self.stateChanged.emit(self.state.value)
            
    def resume_simulation(self):
        """Resume the simulation"""
        if self.state == SimulationState.PAUSED:
            self.pause_requested = False
            self.state = SimulationState.RUNNING
            self.stateChanged.emit(self.state.value)
            
            if self.config.real_time:
                self.timer.start()
                
    def step_simulation(self):
        """Execute one simulation step"""
        if self.state in [SimulationState.STOPPED, SimulationState.PAUSED]:
            self.state = SimulationState.STEP
            self.stateChanged.emit(self.state.value)
            self.simulation_step()
            self.state = SimulationState.PAUSED
            self.stateChanged.emit(self.state.value)
            
    def simulation_step(self):
        """Execute one simulation cycle"""
        try:
            # Update simulation time
            current_time = time.time()
            if self.config.real_time:
                delta_time = current_time - self.last_update_time
                self.simulation_time += delta_time
            else:
                # In non-real-time mode, advance by one clock cycle
                self.simulation_time += 1.0 / (self.config.clock_frequency * 1000000)
                
            self.last_update_time = current_time
            
            # Generate clock signal
            if 'clock' in self.signals:
                clock_value = 1 if (self.current_cycle % 2) == 0 else 0
                self.signals['clock'].set_value(clock_value, self.simulation_time)
                
            # Update all components
            for component in self.component_manager.components.values():
                if component.simulation_active:
                    try:
                        component.simulate_step(self.current_cycle)
                        
                        # Emit component state if changed
                        if hasattr(component, 'state') and component.state:
                            self.componentStateChanged.emit(component.id, component.state)
                            
                    except Exception as e:
                        print(f"Error simulating component {component.name}: {e}")
                        
            # Process event queue
            self._process_event_queue()
            
            # Update cycle counter
            self.current_cycle += 1
            self.cycleCompleted.emit(self.current_cycle)
            
            # Update performance statistics
            self._update_performance_stats()
            
            # Check for simulation limits
            if self.config.max_cycles > 0 and self.current_cycle >= self.config.max_cycles:
                self.stop_simulation()
                
        except Exception as e:
            self.state = SimulationState.ERROR
            self.stateChanged.emit(self.state.value)
            self.errorOccurred.emit(f"Simulation error: {e}")
            
    def _simulation_loop(self):
        """Main simulation loop for non-real-time mode"""
        while not self.stop_requested and self.state == SimulationState.RUNNING:
            if not self.pause_requested:
                self.simulation_step()
                
                # Small delay to prevent 100% CPU usage
                if self.config.clock_frequency > 1000:  # If very high frequency
                    time.sleep(0.001)  # 1ms delay
            else:
                time.sleep(0.01)  # 10ms delay when paused
                
    def _process_event_queue(self):
        """Process scheduled events"""
        current_time = self.simulation_time
        events_to_process = []
        
        # Find events that should be processed
        for event in self.event_queue:
            timestamp, event_type, data = event
            if timestamp <= current_time:
                events_to_process.append(event)
                
        # Remove processed events from queue
        for event in events_to_process:
            self.event_queue.remove(event)
            
        # Process events
        for timestamp, event_type, data in events_to_process:
            self.emit_event(event_type, data)
            
    def schedule_event(self, delay: float, event_type: str, data: Any = None):
        """Schedule an event to occur after a delay"""
        timestamp = self.simulation_time + delay
        self.event_queue.append((timestamp, event_type, data))
        
        # Keep queue sorted by timestamp
        self.event_queue.sort(key=lambda x: x[0])
        
    def _update_performance_stats(self):
        """Update performance statistics"""
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        if elapsed_time > 0:
            self.cycles_per_second = self.current_cycle / elapsed_time
            target_frequency = self.config.clock_frequency * 1000000  # Convert MHz to Hz
            self.actual_frequency = self.cycles_per_second
            
            if target_frequency > 0:
                self.simulation_ratio = self.actual_frequency / target_frequency
            else:
                self.simulation_ratio = 1.0
                
        # Emit statistics every 100 cycles
        if self.current_cycle % 100 == 0:
            stats = self.get_simulation_statistics()
            self.statisticsUpdated.emit(stats)
            
    def get_simulation_statistics(self) -> Dict[str, Any]:
        """Get current simulation statistics"""
        return {
            'state': self.state.value,
            'current_cycle': self.current_cycle,
            'simulation_time': self.simulation_time,
            'cycles_per_second': self.cycles_per_second,
            'actual_frequency': self.actual_frequency,
            'target_frequency': self.config.clock_frequency * 1000000,
            'simulation_ratio': self.simulation_ratio,
            'component_count': len(self.component_manager.components),
            'bus_count': len(self.buses),
            'signal_count': len(self.signals),
            'event_queue_size': len(self.event_queue)
        }
        
    def get_signal_value(self, signal_name: str) -> Optional[int]:
        """Get current value of a signal"""
        if signal_name in self.signals:
            return self.signals[signal_name].value
        return None
        
    def set_signal_value(self, signal_name: str, value: int):
        """Set value of a signal"""
        if signal_name in self.signals:
            self.signals[signal_name].set_value(value, self.simulation_time)
            
    def get_bus_value(self, bus_name: str) -> Optional[int]:
        """Get current value of a bus"""
        if bus_name in self.buses:
            return self.buses[bus_name].read_bus()
        return None
        
    def set_bus_value(self, bus_name: str, value: int, driver_id: str):
        """Set value of a bus from a specific driver"""
        if bus_name in self.buses:
            self.buses[bus_name].drive_bus(driver_id, value, self.simulation_time)
            
    def get_component_state(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get state of a specific component"""
        component = self.component_manager.get_component(component_id)
        if component:
            return component.state.copy()
        return None
        
    def set_component_state(self, component_id: str, state_key: str, value: Any):
        """Set state of a specific component"""
        component = self.component_manager.get_component(component_id)
        if component:
            component.setState(state_key, value)
            
    def reset_simulation(self):
        """Reset simulation to initial state"""
        # Stop if running
        if self.state != SimulationState.STOPPED:
            self.stop_simulation()
            
        # Reset counters
        self.current_cycle = 0
        self.simulation_time = 0.0
        
        # Reset all signals and buses
        for signal in self.signals.values():
            signal.set_value(0, 0.0)
            signal.history.clear()
            
        for bus in self.buses.values():
            for signal in bus.signals.values():
                signal.set_value(0, 0.0)
                signal.history.clear()
                
        # Clear event queue
        self.event_queue.clear()
        
        # Reset all components
        for component in self.component_manager.components.values():
            component.reset()
            
    def export_simulation_data(self) -> Dict[str, Any]:
        """Export simulation data for analysis"""
        data = {
            'statistics': self.get_simulation_statistics(),
            'signals': {},
            'buses': {},
            'components': {}
        }
        
        # Export signal histories
        for name, signal in self.signals.items():
            data['signals'][name] = {
                'bit_width': signal.bit_width,
                'current_value': signal.value,
                'history': signal.history[-100:]  # Last 100 values
            }
            
        # Export bus data
        for name, bus in self.buses.items():
            data['buses'][name] = {
                'bit_width': bus.bit_width,
                'current_value': bus.read_bus(),
                'connected_components': [comp.id for comp in bus.connected_components],
                'drivers': bus.drivers
            }
            
        # Export component states
        for comp_id, component in self.component_manager.components.items():
            data['components'][comp_id] = {
                'name': component.name,
                'type': component.component_type,
                'state': component.state.copy(),
                'properties': component.properties.copy()
            }
            
        return data
        
    def import_simulation_data(self, data: Dict[str, Any]):
        """Import simulation data"""
        try:
            # Stop simulation if running
            if self.state != SimulationState.STOPPED:
                self.stop_simulation()
                
            # Import signal values
            if 'signals' in data:
                for name, signal_data in data['signals'].items():
                    if name in self.signals:
                        value = signal_data.get('current_value', 0)
                        self.signals[name].set_value(value, self.simulation_time)
                        
            # Import component states
            if 'components' in data:
                for comp_id, comp_data in data['components'].items():
                    component = self.component_manager.get_component(comp_id)
                    if component and 'state' in comp_data:
                        component.state.update(comp_data['state'])
                        
        except Exception as e:
            self.errorOccurred.emit(f"Error importing simulation data: {e}")
            
    def get_signal_history(self, signal_name: str, max_points: int = 1000) -> List[Tuple[float, int]]:
        """Get signal history for plotting"""
        if signal_name in self.signals:
            history = self.signals[signal_name].history
            if len(history) <= max_points:
                return history
            else:
                # Downsample history
                step = len(history) // max_points
                return history[::step]
        return []
        
    def add_breakpoint(self, condition: Callable[[], bool], description: str = ""):
        """Add a simulation breakpoint"""
        def breakpoint_handler(data):
            if condition():
                self.pause_simulation()
                self.emit_event('breakpoint_hit', {'description': description})
                
        self.add_event_handler('cycle_completed', breakpoint_handler)
        
    def add_watchpoint(self, signal_name: str, trigger_value: int, description: str = ""):
        """Add a signal watchpoint"""
        def watchpoint_handler(data):
            if signal_name in self.signals:
                signal = self.signals[signal_name]
                if signal.value == trigger_value and signal.has_changed():
                    self.emit_event('watchpoint_hit', {
                        'signal': signal_name,
                        'value': trigger_value,
                        'description': description
                    })
                    
        self.add_event_handler('cycle_completed', watchpoint_handler)
        
    def validate_simulation_setup(self) -> Tuple[bool, List[str]]:
        """Validate simulation setup"""
        errors = []
        warnings = []
        
        # Check if any components are present
        if not self.component_manager.components:
            errors.append("No components in system")
            
        # Check for unconnected power pins
        for component in self.component_manager.components.values():
            power_ports = component.getPortsOfType('power')
            for port in power_ports:
                if not port.connected_to:
                    warnings.append(f"Component {component.name} has unconnected power port: {port.name}")
                    
        # Check for floating buses
        for bus_name, bus in self.buses.items():
            if not bus.drivers:
                warnings.append(f"Bus {bus_name} has no drivers")
            elif len(bus.drivers) > 1:
                warnings.append(f"Bus {bus_name} has multiple drivers (potential conflict)")
                
        # Check clock distribution
        clock_components = []
        for component in self.component_manager.components.values():
            clock_ports = component.getPortsOfType('clock')
            if clock_ports:
                clock_components.append(component.name)
                
        if not clock_components:
            warnings.append("No components connected to clock")
            
        return len(errors) == 0, errors + warnings

class DebugInterface:
    """Debug interface for simulation"""
    
    def __init__(self, simulation_engine: SimulationEngine):
        self.engine = simulation_engine
        self.breakpoints: List[Dict[str, Any]] = []
        self.watchpoints: List[Dict[str, Any]] = []
        self.step_count = 0
        
    def add_breakpoint(self, condition: str, description: str = ""):
        """Add breakpoint with string condition"""
        breakpoint = {
            'id': len(self.breakpoints),
            'condition': condition,
            'description': description,
            'enabled': True,
            'hit_count': 0
        }
        self.breakpoints.append(breakpoint)
        
        # Compile condition and add to engine
        try:
            compiled_condition = compile(condition, '<breakpoint>', 'eval')
            
            def check_condition():
                try:
                    # Create context with simulation data
                    context = {
                        'cycle': self.engine.current_cycle,
                        'time': self.engine.simulation_time,
                        'signals': {name: signal.value for name, signal in self.engine.signals.items()},
                        'buses': {name: bus.read_bus() for name, bus in self.engine.buses.items()}
                    }
                    return eval(compiled_condition, {"__builtins__": {}}, context)
                except:
                    return False
                    
            self.engine.add_breakpoint(check_condition, description)
            
        except SyntaxError as e:
            raise ValueError(f"Invalid breakpoint condition: {e}")
            
        return breakpoint['id']
        
    def remove_breakpoint(self, breakpoint_id: int):
        """Remove breakpoint"""
        self.breakpoints = [bp for bp in self.breakpoints if bp['id'] != breakpoint_id]
        
    def add_watchpoint(self, signal_name: str, condition: str, description: str = ""):
        """Add watchpoint on signal"""
        watchpoint = {
            'id': len(self.watchpoints),
            'signal': signal_name,
            'condition': condition,
            'description': description,
            'enabled': True,
            'hit_count': 0
        }
        self.watchpoints.append(watchpoint)
        return watchpoint['id']
        
    def get_breakpoints(self) -> List[Dict[str, Any]]:
        """Get all breakpoints"""
        return self.breakpoints.copy()
        
    def get_watchpoints(self) -> List[Dict[str, Any]]:
        """Get all watchpoints"""
        return self.watchpoints.copy()
        
    def step_into(self, steps: int = 1):
        """Step into simulation"""
        self.step_count = steps
        for _ in range(steps):
            if self.engine.state in [SimulationState.STOPPED, SimulationState.PAUSED]:
                self.engine.step_simulation()
            else:
                break
                
    def run_until_breakpoint(self):
        """Run simulation until breakpoint is hit"""
        if self.engine.state == SimulationState.PAUSED:
            self.engine.resume_simulation()
        elif self.engine.state == SimulationState.STOPPED:
            self.engine.start_simulation()
            
    def examine_memory(self, component_id: str, address: int, length: int = 1) -> List[int]:
        """Examine memory contents"""
        # This would need to be implemented based on specific component types
        component = self.engine.component_manager.get_component(component_id)
        if component and hasattr(component, 'memory'):
            # Hypothetical memory access
            return [0] * length  # Placeholder
        return []
        
    def set_memory(self, component_id: str, address: int, data: List[int]):
        """Set memory contents"""
        # This would need to be implemented based on specific component types
        component = self.engine.component_manager.get_component(component_id)
        if component and hasattr(component, 'memory'):
            # Hypothetical memory write
            pass
            
    def get_register_values(self, component_id: str) -> Dict[str, int]:
        """Get register values for a component"""
        component = self.engine.component_manager.get_component(component_id)
        if component and hasattr(component, 'registers'):
            return component.registers.copy()  # Hypothetical
        return {}
        
    def set_register_value(self, component_id: str, register_name: str, value: int):
        """Set register value"""
        component = self.engine.component_manager.get_component(component_id)
        if component and hasattr(component, 'registers'):
            if register_name in component.registers:
                component.registers[register_name] = value
                
    def trace_execution(self, component_id: str, enable: bool = True):
        """Enable/disable execution tracing for a component"""
        component = self.engine.component_manager.get_component(component_id)
        if component:
            component.trace_enabled = enable
