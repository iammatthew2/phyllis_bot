import subprocess
import os

# Define the absolute path to the stream executable
stream_path = os.path.expanduser("/home/holly/dev/whisper.cpp/stream")

def run_stream():
    """Start the stream subprocess."""
    try:
        if not os.path.isfile(stream_path):
            raise FileNotFoundError(f"Error: The file '{stream_path}' does not exist.")
        if not os.access(stream_path, os.X_OK):
            raise PermissionError(f"Error: The file '{stream_path}' is not executable.")

        process = subprocess.Popen(
            [
                stream_path, "-m", "/home/holly/dev/whisper.cpp/models/ggml-tiny.en.bin", 
                "--step", "4000", "--length", "4000", "-c", "0", "-t", "4", "-ac", "512", "-f", "magic.txt"
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            cwd=os.path.expanduser("~/dev/whisper.cpp")
        )

        return process

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except PermissionError as perm_error:
        print(perm_error)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
