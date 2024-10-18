import socket

def udp_server(IP="127.0.0.1", port=5000):
    server_address = (IP, port)  # the host and the port, respectively
    buffer_size = 1024

    # Creating the UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(server_address)

    print(f"Server listening on {IP}:{port}")

    while True:
        # receive message from the client
        message, address = udp_socket.recvfrom(buffer_size)
        message = message.decode()

        print("Message from Client:", message)
        print("Client IP Address:", address)

        # send response back to the client
        response = f"Received your message: {message}"
        udp_socket.sendto(response.encode(), address)

if __name__ == "__main__":
    udp_server()