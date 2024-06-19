import os

# Define a constant for the file path
OUTPUT_FILE_PATH = os.path.expanduser("~/dev/whisper.cpp/magic.txt")

def read_last_lines(num_lines=5):
    """Reads the last `num_lines` lines from the specified file."""
    try:
        with open(OUTPUT_FILE_PATH, 'r') as file:
            # Read all lines and strip new lines
            lines = [line.strip() for line in file.readlines()]
            # Get the last `num_lines` lines
            last_lines = lines[-num_lines:]
            # Combine into a single string
            combined_string = ' '.join(last_lines)
            return combined_string
    except FileNotFoundError:
        return f"Error: The file '{OUTPUT_FILE_PATH}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"

def read_all_lines():
    """Reads all lines from the specified file."""
    try:
        with open(OUTPUT_FILE_PATH, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            return lines
    except FileNotFoundError:
        return f"Error: The file '{OUTPUT_FILE_PATH}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"

def read_first_lines(num_lines=5):
    """Reads the first `num_lines` lines from the specified file."""
    try:
        with open(OUTPUT_FILE_PATH, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            first_lines = lines[:num_lines]
            combined_string = ' '.join(first_lines)
            return combined_string
    except FileNotFoundError:
        return f"Error: The file '{OUTPUT_FILE_PATH}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"
