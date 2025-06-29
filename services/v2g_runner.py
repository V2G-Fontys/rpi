import subprocess
import os
import time
import signal

PYPLC_BRIDGE = os.path.expanduser("~/V2G/pyplc_bridge.py")
MODBUS_CONTROLLER = os.path.expanduser("~/V2G/modbus_controller.py")

processes = []

def start_process(path, name):
    print(f"Launching {name}...")
    return subprocess.Popen(["python3", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    try:
        processes.append(start_process(PYPLC_BRIDGE, "PyPLC Bridge"))
        processes.append(start_process(MODBUS_CONTROLLER, "Modbus Controller"))

        print("All processes running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping processes...")
        for proc in processes:
            try:
                os.kill(proc.pid, signal.SIGTERM)
            except Exception as e:
                print(f"Failed to terminate process: {e}")
    finally:
        print("Shutdown complete.")

if __name__ == "__main__":
    main()