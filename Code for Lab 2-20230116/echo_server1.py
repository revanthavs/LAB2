import socket

BYTES_TO_READ = 4096
# 0.0.0.1 will look for all addresss
# Local host 
HOST = "127.0.0.1"
PORT = 8080

def handle_connection(conn, addr):
    # with 'with" we don't have to worry about closing it
    # socket documentation and look for address
    with conn:
        # Prints out the address that has connected to us
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            # This is a echo server everything that is send to it will send us back
            conn.sendall(data)

    return

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen()

        conn, addr = s.accept()
        handle_connection(conn, addr)

    return

start_server()