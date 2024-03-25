import signal
import sys

from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID


# Create the USBMonitor instance
monitor = USBMonitor()

# Define the `on_connect` and `on_disconnect` callbacks
on_connect = lambda device_id, device_info: (
    print(f"Connected: {device_info_str(device_info=device_info)}"),
    # send_email('USB Connected', f"Connected: {device_info_str(device_info=device_info)}")
)
on_disconnect = lambda device_id, device_info: (
    print(f"Disconnected: {device_info_str(device_info=device_info)}"),
    # send_email('USB Disconnected', f"Disconnected: {device_info_str(device_info=device_info)}")
)

# Function to handle the signal
def signal_handler(sig, frame):
    print('Stopping the monitoring...')
    monitor.stop_monitoring()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Start the daemon
monitor.start_monitoring(on_connect=on_connect, on_disconnect=on_disconnect)

# Infinite loop to keep the script running
while True:
    pass