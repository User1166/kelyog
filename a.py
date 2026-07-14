import pynput

def on_press(key):
    try:
        print(f"Key pressed: {key}")
    except Exception as e:
        print(f"Failed to process key press: {e}")

def on_release(key):
    if key == pynput.keyboard.Key.esc:
        return False

with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
