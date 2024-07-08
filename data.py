import time
import numpy as np
import threading
import serial
import Python_server as server

# Global variable to hold received data
received_data_glove = None
data = []
hololens_glove_data = []

def read_data_file(mode):
    """
    Reads array from file, and then deletes it from the file.
    """
    filename = "datafile.txt"
    if mode == "calibrate":
        filename = "calibrate.txt"

    with open(filename, 'r') as file:
        lines = file.readlines()
        array = []
        for line in lines:
            # Split the line into numbers, convert them to integers, and add to the array
            numbers = list(map(int, line.split()))
            array.extend(numbers)
        # Delete the contents of the file by opening it in write mode and doing nothing
    with open(filename, 'w'):
        pass
    return array


def receive_data_hololens(mode):
    """
    Receives data from hololens
    """
    # Start the server in a separate thread
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()

    global data
    while True:
        time.sleep(0.1)
        if mode == "normal":
            if server.received_data:  # Check if there's new data from the server
                data = server.received_data
            if data:
                print(data)
        elif mode == "calibrate":
            data = read_data_file(mode)
            hololens_glove_data = server.received_data


def command_generator(A,B,C,D,E):
    """
    Generates command for gloves from 0-1000 values of fingers
    A=thumb B=index C=middle D=ring E=pink
    """
    # Ensure the values are within the range 0 to 1000
    values = [A, B, C, D, E]
    for value in values:
        if not (0 <= value <= 1000):
            value = 1000
            return value
            #raise ValueError("Values must be between 0 and 1000")

    # Create the string in the desired format
    command_string = f"A{A}B{B}C{C}D{D}E{E}F0G0H0\n"
    return command_string


def check_command():
    global data
    # print(data)
    if len(data) == 5:
        command = command_generator(*data)
    else:
        command = []

    return command


def send_data(bt_serial_glove):
    """
    Send data to the connected Bluetooth device.
    """
    while True:
        command = check_command() #check command
        if command: #check if command is not empty
            bt_serial_glove.write(command.encode('utf-8')) #send command
            #print(command)
        else:
            bt_serial_glove.write("\n".encode('utf-8')) #send \n
        return


def data_glove(bt_serial_glove):
    """
    Receive data from the connected Bluetooth device.
    """
    global received_data_glove
    while True:
        data = bt_serial_glove.readline().decode('utf-8')
        # print(data)
        if data:  # Check if data is not empty
            received_data_glove = data
            #print(received_data_glove)
            send_data(bt_serial_glove)
