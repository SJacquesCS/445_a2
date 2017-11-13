import socket
import threading
import argparse
import os


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
            req_splitter = request.split(" ")
            body_splitter = request.split("\r\n\r\n")
            vb_req_splitter = body_splitter[0].split("\r\n")

            verbose_answer = ""

            for line in vb_req_splitter:
                verbose_answer += str(line) + "<br>"

            if "GET" in req_splitter:
                get_index = req_splitter.index("GET")

                if req_splitter[get_index + 1] == "/" or req_splitter[get_index + 1] == "/favicon.ico":
                    temp_response = verbose_answer + "<br><br>Files Available:<br><br>"
                    files = os.listdir('./files')

                    for file in files:
                        temp_response += "/" + file + "<br>"

                    response = "HTTP/1.1 200 OK\r\n"\
                               + "Content-Type: text/html\r\n"\
                               + "Content-Length: "\
                               + str(len(temp_response))\
                               + "\r\n\r\n"\
                               + temp_response
                else:
                    try:
                        file = open("./files" + req_splitter[get_index + 1], "r")
                        temp_response = verbose_answer + "<br><br>" + file.read()

                        response = "HTTP/1.1 200 OK\r\n" \
                                   + "Content-Type: text/html\r\n" \
                                   + "Content-Length: " \
                                   + str(len(temp_response)) \
                                   + "\r\n\r\n" \
                                   + temp_response
                    except FileNotFoundError:
                        response = "HTTP/1.1 400 BAD REQUEST\r\n"\
                                   + "Content-Type: text/html\r\n"\
                                   + "Content-Length: 26\r\n\r\n"\
                                   + "HTTP ERROR 400 BAD REQUEST"
            elif "POST" in req_splitter:
                post_index = req_splitter.index("POST")
                path_to_data = "./files" + req_splitter[post_index + 1]

                if req_splitter[post_index + 1] == "/":
                    response = "HTTP/1.1 400 BAD REQUEST\r\n"\
                               + "Content-Type: text/html\r\n"\
                               + "Content-Length: 26\r\n\r\n"\
                               + "HTTP ERROR 400 BAD REQUEST"
                else:
                    path_splitter = path_to_data.split("/")

                    for x in range(0, len(path_splitter) - 1):
                        new_dir = path_splitter[x] + "/"

                    if not os.path.exists(new_dir):
                        os.makedirs("./files/" + new_dir)

                    if os.path.isfile(path_to_data):
                        temp_response = verbose_answer + "<br><br>File " + req_splitter[post_index + 1] + " overwritten"
                    else:
                        temp_response = verbose_answer + "<br><br>File " + req_splitter[post_index + 1] + " created"

                    file = open(path_to_data, "w")
                    file.write(body_splitter[1])
                    file.close()

                    response = "HTTP/1.1 200 OK\r\n" \
                               + "Content-Type: text/html\r\n" \
                               + "Content-Length: " \
                               + str(len(temp_response)) \
                               + "\r\n\r\n" \
                               + temp_response
            else:
                response = "HTTP/1.1 400 BAD REQUEST\r\n"\
                           + "Content-Type: text/html\r\n"\
                           + "Content-Length: 26\r\n\r\n"\
                           + "HTTP ERROR 400 BAD REQUEST"

            encoded_response = response.encode("utf-8")

            conn.sendall(encoded_response)
    finally:
        conn.close()


parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server('', args.port)
