import socket
import threading
import argparse
from os import listdir


def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    print('New client from', addr)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            request = data.decode("utf-8")

            print(request)

            response = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html \r\n" + "\r\n"

            if "GET" in request or "get" in request:
                files = listdir('./files')
                for file in files:
                    response += "/" + file + "\n"

            print(response)

            encoded_response = response.encode("utf-8")

            conn.send(encoded_response)
    finally:
        conn.close()

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server('', args.port)
