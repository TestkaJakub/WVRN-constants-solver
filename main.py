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

# Example Usage
fsm = FiniteStateMachine()
for i in range(256):
    fsm.add_state(str(i))

for i in range(256):
    for j in range(-8, 8):
        target = (i + j) % 256
        fsm.add_transition(str(i), f"addi {j}", str(target))

    target = (i * 2) % 256
    fsm.add_transition(str(i), "add acc", str(target))

    flipped = ~i & 0xFF  # Flip bits and ensure 8-bit range
    fsm.add_transition(str(i), "nand acc", str(flipped))

fsm.set_initial_state("0")

# Define your priority order
priority_order = ["addi 1", "addi 2", "addi 3", "addi 4", "addi 5", "addi 6", "addi 7", "addi -1", "addi -2", "addi -3", "addi -4", "addi -5", "addi -6", "addi -7", "addi -8", "add acc", "nand acc"]  # Adjust based on your preference

from collections import deque

def find_shortest_paths(fsm, start_state, priority_order):
    # Dictionary to store details for each state
    paths_data = {
        state: {
            "path": None,  # Sequence of operations to reach this state
            "operation_count": None  # Number of operations required
        }
        for state in fsm.states.keys()
    }
    paths_data[start_state]["path"] = []  # Start state has an empty path
    paths_data[start_state]["operation_count"] = 1  # Includes itself

    # BFS queue: store (current state, path of events to current state, count of operations)
    queue = deque([(start_state, [], 1)])

    while queue:
        current_state, events_path, operation_count = queue.popleft()

        # Get all transitions and sort by priority
        transitions = sorted(
            fsm.states[current_state].transitions.items(),
            key=lambda x: priority_order.index(x[0].split()[0]) if x[0].split()[0] in priority_order else len(priority_order)
        )

        # Explore transitions
        for event, target_state in transitions:
            if paths_data[target_state.name]["path"] is None:  # Not visited yet
                # Update the path and operation count for this state
                paths_data[target_state.name]["path"] = events_path + [event]
                paths_data[target_state.name]["operation_count"] = operation_count + 1
                queue.append((target_state.name, events_path + [event], operation_count + 1))

    return paths_data

import json

def format_as_json(paths_data):
    return json.dumps(paths_data, indent=4)

def format_as_text(paths_data):
    lines = []
    for state, data in sorted(paths_data.items(), key=lambda x: int(x[0])):
        path = data["path"] or []
        count = data["operation_count"] or 0
        lines.append(f"State {state}: Path = {path}, Operations = {count}")
    return "\n".join(lines)

def filter_states(paths_data, state_list):
    return {state: paths_data[state] for state in state_list if state in paths_data}

# Define your priority order
priority_order = ["addi", "add acc", "nand"]

# Find shortest paths
shortest_paths_data = find_shortest_paths(fsm, "0", priority_order)

# Format as JSON
print("JSON Output:")
print(format_as_json(shortest_paths_data))

# Format as plain text
print("\nPlain Text Output:")
print(format_as_text(shortest_paths_data))

# Filter for specific states
filtered_data = filter_states(shortest_paths_data, ["0", "7", "248"])
print("\nFiltered States:")
print(format_as_json(filtered_data))

import json

def format_and_save_as_json(paths_data, file_name):
    # Transform the data into the desired format
    formatted_data = {
        state: ["lda 0"] + (data["path"] or [])  # Start with "lda 0" and append operations
        for state, data in paths_data.items()
        if data["path"] is not None  # Exclude unreachable states
    }

    # Save to a JSON file
    with open(file_name, "w") as json_file:
        json.dump(formatted_data, json_file, indent=4)

    print(f"JSON file saved as '{file_name}'")

# Example Usage:
priority_order = ["addi", "add acc", "nand"]  # Define your operation priority
shortest_paths_data = find_shortest_paths(fsm, "0", priority_order)  # Get shortest paths
format_and_save_as_json(shortest_paths_data, "shortest_paths.json")  # Save as JSON
