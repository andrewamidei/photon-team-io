import socket
import queue

message_queue = queue.Queue()

def udp_server(stop_event, IP="127.0.0.1", receive_port=7501, send_port=7500):
    receive_address = (IP, receive_port)
    send_address = (IP, send_port)
    buffer_size = 1024

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(receive_address)

    print(f"Server listening on {IP}:{receive_port}")

    while not stop_event.is_set():
        udp_socket.settimeout(1)
        try:
            message, address = udp_socket.recvfrom(buffer_size)
            message = message.decode()
            print("Message from Client:", message)

            message_queue.put(message)

            # Send start signal after receiving "202"
            if message == "202":
                response = "202"
                udp_socket.sendto(response.encode(), send_address)
                print("Game start signal sent.")

            else:
                response = "Received your message"
                udp_socket.sendto(response.encode(), send_address)

        except socket.timeout:
            continue

    udp_socket.close()
    print("Server has been shut down.")


if __name__ == "__main__":
    from threading import Event
    stop_event = Event()
    udp_server(stop_event)
