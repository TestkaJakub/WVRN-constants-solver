import json
from WVRN import declaration
from state_machine import FiniteStateMachine
from bfs import *
from data_processing import *

# Load priorities from priorities.json
def load_priorities(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        return data.get("priorities", [])

fsm = FiniteStateMachine()
fsm = declaration(fsm)

# Load priority order from JSON
PRIORITY = load_priorities("priorities.json")

# Validate if PRIORITY is loaded correctly
if not PRIORITY:
    raise ValueError("The priorities list is empty. Please check priorities.json.")

shortest_paths_data = find_shortest_paths(fsm, "0", PRIORITY)  # Get shortest paths
format_and_save_as_json(shortest_paths_data, "shortest_paths.json")  # Save as JSON
