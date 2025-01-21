from collections import deque

def find_shortest_paths(fsm, start_state, priority_order):
    paths_data = {
        state: {
            "path": None,
            "operation_count": None
        }
        for state in fsm.states.keys()
    }
    paths_data[start_state]["path"] = []
    paths_data[start_state]["operation_count"] = 1

    # BFS queue: (current state, path of events to current state, operation count)
    queue = deque([(start_state, [], 1)])

    while queue:
        current_state, events_path, operation_count = queue.popleft()

        # Get transitions and sort by priority within the current state's transitions
        transitions = sorted(
            fsm.states[current_state].transitions.items(),
            key=lambda x: priority_order.index(x[0]) if x[0] in priority_order else len(priority_order)
        )

        for event, target_state in transitions:
            # Strictly prefer shorter paths
            if paths_data[target_state.name]["path"] is None or operation_count + 1 < paths_data[target_state.name]["operation_count"]:
                paths_data[target_state.name]["path"] = events_path + [event]
                paths_data[target_state.name]["operation_count"] = operation_count + 1
                queue.append((target_state.name, events_path + [event], operation_count + 1))
            elif operation_count + 1 == paths_data[target_state.name]["operation_count"]:
                # If path length is the same, break ties by priority of operations
                existing_path = paths_data[target_state.name]["path"]
                new_path = events_path + [event]
                if compare_paths(new_path, existing_path, priority_order):
                    paths_data[target_state.name]["path"] = new_path

    return paths_data


def compare_paths(path1, path2, priority_order):
    """
    Compare two paths based on the priority order.
    Returns True if path1 is preferred over path2.
    """
    for op1, op2 in zip(path1, path2):
        if op1 != op2:
            return priority_order.index(op1) < priority_order.index(op2)
    return len(path1) < len(path2)


def filter_states(paths_data, state_list):
    return {state: paths_data[state] for state in state_list if state in paths_data}