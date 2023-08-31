from flask import Flask, request
import threading

app = Flask(__name__)

clients = {}

@app.route('/receive', methods=['POST'])
def receive_message():
    data = request.data.decode('utf-8')
    print("Received from client:", data)
    
    response = input("Enter a response to send back to the client: ")
    
    # Send the response to the client
    if data in clients:
        client_socket = clients[data]
        client_socket.send(response.encode('utf-8'))
    
    return "Response sent to client: " + response

def client_handler(client_socket, client_address):
    try:
        clients[client_address] = client_socket
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print("Received from client:", message)
            
            response = input("Enter a response to send back to the client: ")
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print("Client disconnected:", e)
    finally:
        client_socket.close()
        if client_address in clients:
            del clients[client_address]

if __name__ == "__main__":
    import socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12345))
    server.listen(5)
    print("Server is running...")

    while True:
        client_socket, client_address = server.accept()
        print("Connected to:", client_address)
        threading.Thread(target=client_handler, args=(client_socket, client_address)).start()
