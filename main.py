from WVRN import declaration
from state_machine import FiniteStateMachine
from bfs import *
from data_processing import *

fsm = FiniteStateMachine()
fsm = declaration(fsm)

# Define your priority order
PRIORITY = [
            "addi 7",
            "addi 6",
            "addi 5",
            "addi 4",
            "addi 3",
            "addi 2",
            "addi 1",
            "addi -8",
            "addi -7",
            "addi -6",
            "addi -5",
            "addi -4",
            "addi -3",
            "addi -2",
            "addi -1",
            "add acc",
            "nand acc",
            ]

shortest_paths_data = find_shortest_paths(fsm, "0", PRIORITY)  # Get shortest paths
format_and_save_as_json(shortest_paths_data, "shortest_paths.json")  # Save as JSON
