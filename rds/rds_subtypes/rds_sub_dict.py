import copy
import pprint

from rds.rds_subtypes import RDSSubBase
from rds.type_conversion import convertType, registerRDSSubType


class RDSSubDict(RDSSubBase):
    __dict = None
    def __init__(self, master, dictionary):
        RDSSubBase.__init__(self, master)
        self.__dict = dictionary
        self._running = master._running

        for x in self.__dict:
            self.__dict[x] = convertType(master, self.__dict[x])

    def getData(self):
        ret = copy.copy(self.__dict)
        for x in ret:
            ret[x] = ret[x].getData() if isinstance(ret[x], RDSSubBase) else ret[x]
        return ret

    def _save(self):
        for x in self.__dict:
            self.__dict[x] = convertType(self.__dict[x])

        self._master._save()

    # From here on we need to forward the functions to our dict or intercept them.
    def __contains__(self, *args, **kwargs):
        return self.__dict.__contains__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__dict.__delitem__(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def __eq__(self, *args, **kwargs):
        return self.__dict.__eq__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return self.__dict.__ge__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self.__dict.__getitem__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        return self.__dict.__gt__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self.__dict.__iter__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        return self.__dict.__le__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self.__dict.__len__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        return self.__dict.__lt__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self.__dict.__ne__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self.__dict.__repr__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__dict.__setitem__(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def __sizeof__(self, *args, **kwargs):
        return self.__dict.__sizeof__(*args, **kwargs)

    def clear(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__dict.clear(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def copy(self, *args, **kwargs):
        return self.__dict.copy(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.__dict.get(*args, **kwargs)

    def items(self, *args, **kwargs):
        return self.__dict.items(*args, **kwargs)

    def keys(self, *args, **kwargs):
        return self.__dict.keys(*args, **kwargs)

    def pop(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__dict.pop(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def popitem(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__dict.popitem(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def setdefault(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__dict.setdefault(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def update(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__dict.update(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def values(self, *args, **kwargs):
        return self.__dict.values(*args, **kwargs)



# Register RDSSubDict as the handler for dict.
registerRDSSubType(dict, RDSSubDict)

# Add handling to the pprint module for RDSSubDict.
pprint.PrettyPrinter._dispatch[RDSSubDict.__repr__] = pprint.PrettyPrinter._pprint_dict
