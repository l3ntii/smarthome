import threading
from sensors import temp, safety, alarm, light

def main():
    print("Temperature and Safety sensors are running... (Press Ctrl+C to stop)")

    temp_thread = threading.Thread(target=temp.run, daemon=True)
    temp_thread.start()

    safety_thread = threading.Thread(target=safety.run, daemon=True)
    safety_thread.start()

    alarm_thread = threading.Thread(target=alarm.run, daemon=True)
    alarm_thread.start()

    light_thread = threading.Thread(target=light.run, daemon=True)
    light_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down program.")

if __name__ == "__main__":
    main()
