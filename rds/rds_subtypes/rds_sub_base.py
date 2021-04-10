class RDSSubBase(object):
    """
    Base class for all RDS subtypes. Used mainly for detecting when an object is
    an RDS subtype.
    """
    def __init__(self, master):
        self._master = master
        self._running = master._running

    def _awaitTurn(self):
        return self._master._awaitTurn()
