import socket # Built in socket module

def udp_client():
    server_address = ('127.0.0.1', 5000)
    buffer_size = 1024
    message = "Hello UDP Server"

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout for receiving response
    client_socket.settimeout(5)  

    try:
        # Send data to the server
        client_socket.sendto(message.encode(), server_address)
        print("Sent message to server:", message)

        # Receive response from the server
        data, _ = client_socket.recvfrom(buffer_size)
        response = data.decode()
        print("Received response from server:", response)

    except socket.timeout:
        print("No response from server, request timed out.")

    finally:
        client_socket.close()


if __name__ == "__main__":
    udp_client()