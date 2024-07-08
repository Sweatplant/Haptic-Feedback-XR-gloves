import numpy as np
import time

index = 0

array = np.arange(0, 1001, 25)
matrix_with_data = np.matrix([array, array, array, array, array])


def datafilewrite():
    global index
    while True:
        # Extract the data from the current index column and flatten it
        data = np.array(matrix_with_data[:, index]).flatten()

        # Increment the index and reset if it reaches the limit
        index += 1
        if index >= matrix_with_data.shape[1]:
            index = 0

        # Write the data to the file
        with open("datafile.txt", 'w') as file:
            file.write(' '.join(map(str, data)))
        print(data)
        # Optional: add a sleep to avoid writing too quickly
        time.sleep(1)  # Uncomment this line if you want a delay between writes


# Example usage
datafilewrite()
