import socket

def udp_server(stop_event, IP="127.0.0.1", port=5000):
    server_address = (IP, port)  # the host and the port, respectively
    buffer_size = 1024

    # Creating the UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(server_address)

    print(f"Server listening on {IP}:{port}")

    while not stop_event.is_set():
        udp_socket.settimeout(1)  # Set a timeout to periodically check the stop_event
        try:
            # Receive message from the client
            message, address = udp_socket.recvfrom(buffer_size)
            message = message.decode()

            print("Message from Client:", message)
            print("Client IP Address:", address)

            # Optionally, send a response back to the client
            response = f"Received your message: {message}"
            udp_socket.sendto(response.encode(), address)
        except socket.timeout:
            continue

    udp_socket.close()
    print("Server has been shut down.")

if __name__ == "__main__":
    from threading import Event
    stop_event = Event()
    udp_server(stop_event)