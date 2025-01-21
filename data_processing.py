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