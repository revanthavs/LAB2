import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

# PROXY SERVER ACCEPT REQUEST AND RERLY THEM TO OTHER SERVER AND SEND BACK THE RESULT TO THE INTIAL SERVER 

def send_request(host, port, request_data):
    # Client socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Sending data to google
        client_socket.connect((host, port))
        client_socket.send(request_data)
        # We are specifing the other server that we are done sending data
        client_socket.shutdown(socket.SHUT_WR)

        # Getting response from google
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0:
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        return result


def handle_connection(conn, addr):
    with conn:
        print(f"Connected by: {addr}")
        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            # We want to build out the request that we want to send the stream to google
            request += data

        response = send_request("www.google.com", 80, request)
        # Will return the responds from google
        conn.sendall(response)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Why 2? This parameter allows how many of queries are allowed to the server
        server_socket.listen(2)
        conn, addr = server_socket.accept()

        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Why 2? This parameter allows how many of queries are allowed to the server
        server_socket.listen(2)

        while True:
            conn, addr = server_socket.accept()
            # The movement we have another connection request we will create a new thread and process the request
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

    

start_threaded_server()
# start_server()