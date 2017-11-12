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
            splitter = request.split(" ")
            vb_splitter = request.split("\r\n")
            verbose_answer = ""

            for line in vb_splitter:
                verbose_answer += str(line) + "<br>"

            if "GET" in splitter:
                get_index = splitter.index("GET")

                if splitter[get_index + 1] == "/":

                    response = "HTTP/1.1 200 OK\r\n"\
                               + "Content-Type: text/html\r\n\r\n"\
                               + verbose_answer + "\r\n"\
                               + "Files Available:<br><br>"

                    files = listdir('./files')
                    for file in files:
                        response += "/" + file + "<br>"
                else:
                    try:
                        file = open("./files" + splitter[get_index + 1])
                        response = "HTTP/1.1 200 OK\r\n"\
                                   + "Content-Type: text/html\r\n\r\n"\
                                   + file.read()
                    except FileNotFoundError:
                        response = "HTTP/1.1 404 NOT FOUND\r\n"\
                                   + "Content-Type: text/html\r\n\r\n"\
                                   + "HTTP ERROR 404 NOT FOUND"
            elif "POST" in splitter:
                response = "HTTP/1.1 200 OK\r\n"\
                           + "Content-Type: text/html"\
                           + "Content-Length: 16\r\n\r\n"\
                           + "<html><body><p>File Overwritten</p></body></html>"

            else:
                response = "HTTP/1.1 400 BAD REQUEST\r\n"\
                           + "Content-Type: text/html\r\n\r\n"\
                           + "HTTP ERROR 400 BAD REQUEST"

            print(response)

            encoded_response = response.encode("utf-8")

            conn.send(encoded_response)
    finally:
        conn.close()


parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server('', args.port)
