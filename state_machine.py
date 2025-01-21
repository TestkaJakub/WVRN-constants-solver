class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def add_transition(self, event, target_state):
        self.transitions[event] = target_state

    def get_next_state(self, event):
        return self.transitions.get(event, None)

class FiniteStateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state_name):
        state = State(state_name)
        self.states[state_name] = state
        if self.current_state is None:
            self.current_state = state  # Set the first state as the initial state

    def add_transition(self, from_state, event, to_state):
        if from_state in self.states and to_state in self.states:
            self.states[from_state].add_transition(event, self.states[to_state])
        else:
            raise ValueError("States must be added before creating transitions")

    def set_initial_state(self, state_name):
        if state_name in self.states:
            self.current_state = self.states[state_name]
        else:
            raise ValueError(f"State '{state_name}' not found in the FSM")

    def process_event(self, event):
        if self.current_state is None:
            raise ValueError("Initial state not set")
        
        next_state = self.current_state.get_next_state(event)
        if next_state:
            print(f"Transitioning from {self.current_state.name} to {next_state.name} on event '{event}'")
            self.current_state = next_state
        else:
            print(f"No transition found for event '{event}' in state '{self.current_state.name}'")

    def get_current_state(self):
        return self.current_state.name if self.current_state else None