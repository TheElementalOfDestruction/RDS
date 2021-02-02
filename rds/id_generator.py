import json
import socket
import threading


class IDGenerator(object):
    def __init__(self, maxId = 9999999):
        """
        A class for generating a random id over the socket.
        :param maxId: the number of possible unique IDs that this instance can generate.
        """
        self.__maxID = maxId
        self.__stop = False
        self.__start()

    def __delete__(self, instance):
        """
        Function that *should* be called if the instance is ever deleted. Will
        cleanup the thread and the socket.
        """
        self.__stop = True

    def __start(self):
        """
        Starts the id generator. Returns the port it was opened on.
        """
        self.__socket = socket.socket()
        # Bind to our local address on a random port. If we try to reserve a defined
        # port then we would not be able to have multiple ID generators, and might
        # end up having problems if something else binds to that port.
        self.__socket.bind(('localhost', 0))
        # Set the timeout to 1 second. This is so we can check to see if we need to
        # stop the IDGenerator.
        self.__socket.settimeout(1)
        # Retrieve the port we bound to so we can connect to it.
        self.__port = self.__socket.getsockname()[1]
        # Create the thread that will provide the unique IDs.
        self.__thread = threading.Thread(target = self.__threadRunner, daemon = True)
        # Start the generator.
        self.__thread.start()

    def __threadRunner(self):
        """
        Function that will run in a thread. This is a socket that will generate
        the id.
        """
        id = 0
        while True:
            self.__socket.listen(100)
            # Check to see if self.__stop  has been set. If it has, we need to stop running.
            if self.__stop:
                self.__socket.close()
                return
            try:
                client, details = self.__socket.accept()
                message = json.dumps({'id': id}).encode('utf-8')
                # Loop until we have sent the entire message.
                while len(message) > 0:
                    sent = client.send(message)
                    message = message[sent:]
                client.close()
                # Increment the ID and loop back to 0 if we have hit the max ID.
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
