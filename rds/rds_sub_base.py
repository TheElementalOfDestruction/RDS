class RDSSubBase(object):
    """
    Used for detection of RDS subclasses. All RDS subclasses will inherit from this.
    """
    def __init__(self, master):
        self._master = master

    def _awaitTurn(self):
        return self._master._awaitTurn()
