import socket
import threading

def receive_from_server():
    while True:
        response = client_socket.recv(1024)
        if not response:
            break
        print("Server response:", response.decode('utf-8'))

server_address = ('127.0.0.1', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

receive_thread = threading.Thread(target=receive_from_server)
receive_thread.start()

try:
    while True:
        message = input("Enter a message to send to the server (or type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("Client is closing...")
finally:
    client_socket.close()
