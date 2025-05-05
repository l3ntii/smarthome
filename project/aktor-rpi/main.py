import threading
from mqtt import subscriber
from logic import control
from logic import actions

def main():
    print("System starting...")

    subscriber.start()

    control_thread = threading.Thread(target=control.run, daemon=True)
    control_thread.start()

    print("Aktor-RPi is running. Press Ctrl+C to exit.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down...")
        actions.set_fan(False)
        actions.set_heat(False)
        actions.set_light(False)
        actions.buzzer_off
        actions.cleanup()

if __name__ == "__main__":
    main()