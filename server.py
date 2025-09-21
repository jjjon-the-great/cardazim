import argparse
import sys
import socket
import struct
import threading

def get_message_from_socket(connected_socket: socket.socket):
    '''
    Takes in socket object, gets it's message and processes it.
    '''
    (length, ) = struct.unpack("<I", connected_socket.recv(4))
    (text, ) = struct.unpack(f"<{length}s", connected_socket.recv(length))
    print(text.decode('utf-8'))
    connected_socket.close()

def run_server(server_ip, server_port):
    '''
    Starts listening on ip, port
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((server_ip, server_port))
    while True:
        s.listen()
        (conn, addr) = s.accept()
        current_thread = threading.Thread(target = get_message_from_socket, args=(conn, ))
        current_thread.start()

def get_args():
    parser = argparse.ArgumentParser(description='initialize server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())