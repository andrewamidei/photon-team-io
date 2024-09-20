import socket # Built in socket module


server_address = ('127.0.0.1', 500)
buffer_size = 1024 # buffer size is one kilobyte of data

UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDPSocket.bind(server_address)

print(f"Listening for clients at {(IP, PORT)}")

while True:
    data, address = UDPSocket.recvfrom(buffer_size)
    message = data.decode()

    print("Client :" + data)
