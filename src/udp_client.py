import socket 

def send_udp_message(message, server_address=('127.0.0.1', 7500), buffer_size=1024, timeout=10):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)

    try:
        client_socket.sendto(message.encode(), server_address)
        print("Sent message to server:", message)

        # Receive response from the server
        data, _ = client_socket.recvfrom(buffer_size)
        response = data.decode()
        print("Received response from server:", response)
        return response

    except socket.timeout:
        print("No response from server, request timed out.")
        return None

    finally:
        client_socket.close()


if __name__ == "__main__":
    message = "Hello UDP Server"
    send_udp_message(message)