import json
import socket
import threading


stop = False

class IDGenerator(object):
    def __init__(self, maxId = 9999999):
        """
        A class for generating a random id over the socket
        """
        self.__maxID = maxId
        self.__start()

    def __start(self):
        """
        Starts the id generator. Returns the port it was opened on.
        """
        self.__socket = socket.socket()
        self.__socket.bind(('localhost', 0))
        self.__socket.settimeout(1)
        self.__port = self.__socket.getsockname()[1]
        self.__thread = threading.Thread(target = self.__threadRunner)
        self.__thread.start()

    def __threadRunner(self):
        """
        Function that will run in a thread. This is a socket that will generate
        the id.
        """
        id = 0
        while True:
            self.__socket.listen(100)
            if stop:
                self.__socket.close()
                return
            try:
                client, details = self.__socket.accept()
                message = json.dumps({'id': id}).encode('utf-8')
                while len(message) > 0:
                    sent = client.send(message)
                    message = message[sent:]
                client.close()
                id += 1
                id %= self.__maxID
            except socket.timeout:
                pass

    def generateId(self):
        """
        Get a new ID from the generator.
        """
        sock = socket.socket()
        sock.connect(('localhost', self.__port))
        message = b''
        while True:
            get = sock.recv(1024)
            if get == b'':
                break
            message += get
        sock.close()
        return json.loads(message.decode('utf-8'))['id']
