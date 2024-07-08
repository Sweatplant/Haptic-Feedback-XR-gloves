import socket

received_data = [0, 0, 0, 0, 0]
previous_data = []  # To keep track of the previous data


def start_server():
    global received_data, previous_data

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set the socket options to reuse the address
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Get local machine name
    host = '127.0.0.1'
    port = 65433

    # Bind to the port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen(1)
    print("Server is listening...")

    def string_to_array(input_string):
        # Split the string by spaces
        string_elements = input_string.split()

        # Convert each element to an integer
        int_array = [int(element) for element in string_elements]

        return int_array

    def update_received_data(new_data):
        global received_data, previous_data

        for i in range(len(new_data)):
            if new_data[i] == 0:
                # If there is a zero in the new data, update the received data with zero
                received_data[i] = 0
            elif previous_data[i] == 0:
                # If the new data is different and not zero, retain the previous value
                received_data[i] = new_data[i]
            # elif new_data[i] > previous_data[i]:
            #     # If the new data is bigger, then use that value
            #     received_data[i] = new_data[i]

        # Update the previous_data to be the same as received_data
        previous_data = received_data.copy()
        return received_data

    while True:
        # Establish a connection
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")

        while True:
            try:
                # Receive data
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                data = string_to_array(data)
                #print(data)
                received_data = update_received_data(data)
               # print(received_data)

                # Send a response
                response = "\n"
                client_socket.send(response.encode('utf-8'))
            except ConnectionResetError:
                break

        # Close the connection
        client_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    start_server()
