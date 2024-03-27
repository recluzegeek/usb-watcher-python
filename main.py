import signal
import smtplib
import sys

from usbmonitor import USBMonitor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create the USBMonitor instance
monitor = USBMonitor()

device_info_str = lambda device_info: ', '.join(f"{key}: {value}" for key, value in device_info.items())

# Email settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587
# username = ''
app_secret = ''
from_email = ''
to_email = ''


def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, app_secret)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


def get_device_type(device_info):
    devtype = device_info.get('DEVTYPE', '')
    return devtype


# Define the `on_connect` and `on_disconnect` callbacks
on_connect = lambda device_id, device_info: (
    print(
        f"Connected: {device_id} ({get_device_type(device_info=device_info)})\n{device_info_str(device_info=device_info)}"),
    send_email('🚨🔔 USB Connected', f"Connected: {device_info_str(device_info=device_info)}")
)
on_disconnect = lambda device_id, device_info: (
    print(
        f"Disconnected: {device_id} ({get_device_type(device_info=device_info)})\n{device_info_str(device_info=device_info)}"),
    send_email('🚨🔔 USB Disconnected', f"Disconnected: {device_info_str(device_info=device_info)}")
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
