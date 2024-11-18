import socket
import queue

message_queue = queue.Queue()

def udp_server(stop_event, IP="127.0.0.1", receive_port=7501, send_port=7500): # function to create a UDP server
    receive_address = (IP, receive_port) # IP address and port number to receive
    send_address = (IP, send_port) 
    buffer_size = 1024
 
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create a socket for the server
    udp_socket.bind(receive_address) # bind the socket to the IP address and port number
 
    print(f"Server listening on {IP}:{receive_port}") # print that the server is listening

    while not stop_event.is_set():
        udp_socket.settimeout(1) # set timeout for the socket
        try:
            message, address = udp_socket.recvfrom(buffer_size) # receive message from the client
            message = message.decode() # decode the message
            print("Message from Client:", message) # print the message received from the client

            message_queue.put(message)

            # Send start signal after receiving "202"
            if message == "202":
                response = "202"
                udp_socket.sendto(response.encode(), send_address) # send response to the client
                print("Game start signal sent.") # print that the game has started signal has been sent

            else:
                response = "Received your message"
                udp_socket.sendto(response.encode(), send_address) # send response to the client

        except socket.timeout:
            continue

    udp_socket.close() # close the socket
    print("Server has been shut down.")


if __name__ == "__main__":
    from threading import Event # import Event class from threading module
    stop_event = Event() # create an event to stop the server
    udp_server(stop_event) # start the UDP server
