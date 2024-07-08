import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend
import matplotlib.pyplot as plt
import time
import data
import re
import Python_server

def data_decode(encoded_finger_locations):
    """
    Decode the data returned from the glove 0-4095
    In the glove these values are automatically assigned to the reach of the fingers max = 4095, min = 0
    """
    # Regular expression to find the values after A, B, C, D, and E
    matches = re.findall(r'[ABCDE](\d+)', encoded_finger_locations)
    # Convert the matches to integers
    location_fingers = [int(match) for match in matches]
    return location_fingers


def average_fingers(times=5, delay=0.2):
    """
    Compute the average of each finger's location from the collected data sets.
    """
    all_readings = []
    for _ in range(times):
        # location_fingers = data_decode(data.received_data_glove)
        location_fingers = Python_server.received_data
        all_readings.append(location_fingers)
        time.sleep(delay)

    # Compute the average
    num_fingers = len(all_readings[0])
    averaged_fingers = [
        sum(location_fingers[i] for location_fingers in all_readings) / times
        for i in range(num_fingers)
    ]

    return averaged_fingers

def calibrate():
    """
    Calibrates the glove device by sending incremental data and recording the responses.
    """
    received_data = []
    with open("calibrate.txt", 'w') as file:
        file.write(' '.join(map(str, [0, 0, 0, 0, 0])))
    print("Glove set to [0, 0, 0, 0, 0]")

    for i in range(0, 1100, 100):
        values = [i, i, i, i, i]
        input(f"Press Enter to send {values} for calibration step: ")
        with open("calibrate.txt", 'w') as file:
            file.write(' '.join(map(str, values)))
        time.sleep(1)
        input("Put your fingers to the maximum distance and press ENTER")
        if data.hololens_glove_data:
            # Collect and average data
            location_fingers = average_fingers()
            received_data.append(location_fingers)
            print(f"Received: {location_fingers}")
            print(received_data)
    # Plotting
    num_steps = len(received_data)
    num_fingers = len(received_data[0])
    step_values = range(0, 1100, 100)

    plt.figure(figsize=(10, 6))

    for finger_index in range(num_fingers):
        finger_data = [data[finger_index] for data in received_data]
        plt.plot(step_values, finger_data, marker='o', linestyle='-', label=f'Finger {finger_index + 1}')

    plt.xlabel('Glove Value')
    plt.ylabel('Finger Position')
    plt.title('Finger Calibration')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('calibration_plot.png')  # Save plot to a file
    plt.close()  # Close the plot to prevent it from being displayed
    return received_data
