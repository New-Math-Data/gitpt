import threading
import itertools
import time #this can go away once we have a function we can wait for.

def spinner():
    """Display a rotating spinner while waiting for a response."""
    
    spinner_cycle = itertools.cycle(['|', '/', '-', '\\'])
    stop_spinner = threading.Event()

    def spin():
        while not stop_spinner.is_set():
            print(f"Generating commit message: {next(spinner_cycle)}", flush=True, end='\r')
            time.sleep(0.1)

    # Start the spinner in a new thread
    spinner_thread = threading.Thread(target=spin)
    spinner_thread.start()

    return stop_spinner