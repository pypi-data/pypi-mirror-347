import json
import os

def load_report_type_map():
    """
    Loads the reportTypeMap.json from the metadata directory relative to this file.
    Returns the parsed JSON data or None if there's an error.
    """
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'metadata', 'reportTypeMap.json'))
        if not os.path.exists(path):
            print(f"Error: The file {path} does not exist.")
            return None
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading reportTypeMap.json: {e}")
        return None
