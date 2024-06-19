import os
import signal
import subprocess
import time
import sys
import threading
from utils.voice_to_file import run_stream
from utils.file_reader import read_last_lines
from utils.generative_context import generate_response_from_conversation, generate_response_from_direct_instruction
import logging

logging.basicConfig(filename='logging/application.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class StreamRunner:
    def __init__(self):
        self.process = None
        self.stop_event = threading.Event()

    def signal_handler(self, signum, frame):
        print(f"Signal {signum} received, terminating subprocess and exiting.")
        self.stop_event.set()
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
                print("Subprocess terminated.")
            except subprocess.TimeoutExpired:
                print("Subprocess did not terminate in time. Killing...")
                self.process.kill()
        sys.exit(0)

    def background_task(self):
        self.process = run_stream()
        if self.process:
            try:
                while not self.stop_event.is_set() and self.process.poll() is None:
                    time.sleep(0.1)
                if self.process.poll() is None:
                    self.process.terminate()
                    self.process.wait(timeout=5)
            except Exception as e:
                print(f"An error occurred in background task: {e}")

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        self.thread = threading.Thread(target=self.background_task)
        self.thread.start()

    def wait_for_completion(self):
        self.thread.join()

def main_task():
    print("phyllis is starting up")
    with open('/home/holly/dev/whisper.cpp/magic.txt', 'w') as file:
        pass

    init_message1 = generate_response_from_direct_instruction("you have just now come online")

    subprocess.run(['sudo', 'python3', '/home/holly/dev/phyllis_bot/utils/render_matrix_text.py', init_message1])
    time.sleep(2)

    previous_lines = None
    wait_time = 5  # Initial wait time
    max_wait_time = 15  # Maximum wait time

    # Function to handle signals and clean up
    def signal_handler(signum, frame):
        print(f"Signal {signum} received, cleaning up and exiting.")
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    time.sleep(5)
    while True:
        current_lines = read_last_lines(num_lines=5)
        logger.debug('current lines: ' + current_lines)

        if current_lines != previous_lines:
            if "magic magic repeat" in current_lines:
                subprocess.run(['sudo', 'python3', '/home/holly/dev/phyllis_bot/utils/render_matrix_text.py', current_lines])
            elif "magic magic kill" in current_lines:
                print("Magic kill detected. Terminating the current process...")
                os.kill(os.getpid(), signal.SIGTERM)
            elif "magic magic shutdown" in current_lines or "magic magic shut down" in current_lines:
                print("Magic shutdown begin...")
                with open('file.txt', 'w') as file:
                    pass
                try:
                    subprocess.run(['sudo', 'shutdown', 'now'], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")
            elif "magic magic pause" in current_lines:
                print("Magic pause detected. Pausing the process for 30 seconds...")
                time.sleep(30)
            else:
                print("File content changed, processing...")
                ai_commentary = generate_response_from_conversation(current_lines)
                subprocess.run(['sudo', 'python3', '/home/holly/dev/phyllis_bot/utils/render_matrix_text.py', ai_commentary])
                previous_lines = current_lines
                wait_time = 5  # Reset wait time to initial value
        else:
            print(current_lines)
            logger.info('So should this')

            print(f"No change detected. Waiting for {wait_time} seconds.")

        time.sleep(wait_time)
        wait_time = min(wait_time * 2, max_wait_time)  # Exponential backoff

def main():
    logger.info('application started')
    logger.debug('this is here')
    runner = StreamRunner()
    runner.start()

    main_task()

    runner.wait_for_completion()

if __name__ == "__main__":
    main()
