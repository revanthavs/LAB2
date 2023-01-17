import socket

BYTES_TO_READ = 4096

def get(host, port):

    # request = b"GET / HTTP/1.1\nHost:" + host.encode('utf-8') + b"\n\n"
    request = b"GET / HTTP/1.1\nHost: www.google.com\n\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((host,port))
        s.send(request)
        s.shutdown(socket.SHUT_WR)
        print("Wating for response!")
        chunk = s.recv(BYTES_TO_READ)
        result = b'' + chunk

        # As long as we recieve the data we print it to terminal
        while(len(chunk) > 0):
            print(result)
            chunk = s.recv(BYTES_TO_READ)
            result += chunk
            # result = s.recv(BYTES_TO_READ)

        return result
    # s.close()

# prot 80 is because it's accepted TCP protocol
get("127.0.0.1", 8080)