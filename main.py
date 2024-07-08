import time
import threading
from connection import find_bluetooth_device, connect_to_bluetooth_serial_port
from data import receive_data_hololens, data_glove
from calibrate import calibrate

def main():
    device_name_glove = "lucidgloves-right"  # Replace with your device's Bluetooth name
    bt_address_glove = find_bluetooth_device(device_name_glove)

    if bt_address_glove is None:
        print("Could not find Bluetooth device.")
        return

    bt_serial_glove = connect_to_bluetooth_serial_port(bt_address_glove)
    bt_serial_holo = None  # Placeholder for future Hololens Bluetooth connection

    mode = input("Press Enter for normal mode or 'c' for calibrate mode: ")
    if mode == "":
        mode = "normal"
    elif mode == "c":
        mode = "calibrate"
        calibration_thread = threading.Thread(target=calibrate, daemon=True)
        calibration_thread.start()
    else:
        mode = "normal"
    print(f"Mode is set to: {mode}")

    holo_thread = threading.Thread(target=receive_data_hololens, args=(mode,), daemon=True)
    holo_thread.start()

    glove_thread = threading.Thread(target=data_glove, args=(bt_serial_glove,), daemon=True)
    glove_thread.start()

    try:
        while True:
            time.sleep(0)
    except KeyboardInterrupt:
        print("Disconnecting...")
    finally:
        bt_serial_glove.close()


if __name__ == "__main__":
    main()
