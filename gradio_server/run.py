import subprocess
import signal
import sys
import time

# Function to handle Ctrl+C
def signal_handler(sig, frame):
    print('Ctrl+C pressed! Terminating subprocesses...')
    proc1.terminate()
    proc2.terminate()
    proc3.terminate()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Start the subprocesses
print('Starting subprocesses...')
proc2 = subprocess.Popen(['python', 'freshness.py'])
print('Freshness IP:')
time.sleep(5)
proc3 = subprocess.Popen(['python', 'ocr.py'])
print('OCR IP:')
time.sleep(5)
# proc1 = subprocess.Popen(['python', 'count_owl-vith.py'])
proc1 = subprocess.Popen(['python', 'count_dino.py'])
print('Count IP:')

# Wait for the subprocesses to complete
proc1.wait()
proc2.wait()
proc3.wait()