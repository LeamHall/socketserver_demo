#!/usr/bin/env python

# name    :  socketserver_client.py
# version :  0.0.1
# date    :  20240712
# author  :
# desc    :

import argparse
import socket
import sys


def parse_arguments(args = []):
    """ Returns the parsed arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H", "--host",
        help    = "Host IP to listen on",
        default = "",
    )
    parser.add_argument(
        "-P", "--port",
        help    = "Port to listen on",
        default = 8080,
    )
    parser.add_argument(
        "-s", "--search",
        help    = "Search term(s)",
        default = "",
    )

    return vars(parser.parse_args(args))


if __name__ == "__main__":
    _args = parse_arguments(sys.argv[1:])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_args["host"], _args["port"]))
        sock.sendall(bytes(_args["search"] + "\n", "utf-8"))

        received = str(sock.recv(1024), "utf-8")

    print("Sent:     {}".format(_args["search"]))
    print("Received: {}".format(received))

