import bluetooth
import serial

def find_bluetooth_device(device_name_glove):
    """
    Scan for available Bluetooth devices and return the address_glove of the device with the given name.
    """
    print("Searching for Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=6, lookup_names=True, flush_cache=True, lookup_class=False)

    for addr_glove, name_glove in nearby_devices:
        if name_glove == device_name_glove:
            print(f"Found Bluetooth device {device_name_glove} with address_glove {addr_glove}")
            return addr_glove
    return None

def connect_to_bluetooth_serial_port(address_glove):
    """
    Connect to the Bluetooth device with the specified address_glove using a serial port.
    """
    port = 7  # Standard port for Bluetooth SPP
    bt_serial_glove = serial.Serial(f'COM{port}', baudrate=115200, timeout=1)
    print(f"Connected to {address_glove} on port {port}")
    return bt_serial_glove
