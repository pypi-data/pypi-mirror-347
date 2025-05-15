from .library import Server

if __name__ == "__main__":
    server = Server(host='0.0.0.0', port=1414)
    server.start()

