import socket


server_address = ("127.0.0.1", 5000) # the host and the port, respectively
buffer_size = 1024

#going to specify who the client is in future sprint

# creating the UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    
    message, address = udp_socket.recvfrom(buffer_size)
    message = message.decode()

    print("Message from Client: " + message)
    print("Client IP Address: " + address)
    # udp_message = input("Enter message: ")
    # udp_socket.sendto(udp_message.encode(), serverAddressPort)
