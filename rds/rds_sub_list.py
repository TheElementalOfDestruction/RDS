import copy
import pprint

from rds.rds_sub_base import RDSSubBase
from rds.type_conversion import convertType, registerRDSSubType


class RDSSubList(RDSSubBase):
    __list = None
    def __init__(self, master, _list):
        RDSSubBase.__init__(self, master)
        self.__list = []

        for x in _list:
            self.__list.append(convertType(master, x))

    def getData(self):
        ret = copy.copy(self.__list)
        for x, y in enumerate(ret):
            ret[x] = y.getData() if isinstance(y, RDSSubBase) else y
        return ret

    def _save(self):
        for x, y in enumerate(self.__list):
            self.__list[x] = convertType(self._master, y)
        self._master._save()

    # From here on we need to forward the functions to our list or intercept them.
    def __add__(self, *args, **kwargs):
        return self.__list.__add__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self.__list.__contains__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.__delitem__(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def __eq__(self, *args, **kwargs):
        return self.__list.__eq__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return self.__list.__ge__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self.__list.__getitem__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        return self.__list.__gt__(*args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.__iadd__(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def __imul__(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.__imul__(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def __le__(self, *args, **kwargs):
        return self.__list.__le__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self.__list.__len__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        return self.__list.__lt__(*args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self.__list.__mul__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self.__list.__ne__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self.__list.__repr__(*args, **kwargs)

    def __reversed__(self, *args, **kwargs):
        return self.__list.__reversed__(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return self.__list.__rmul__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.__setitem__(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def __sizeof__(self, *args, **kwargs):
        return self.__list.__sizeof__(*args, **kwargs)

    def append(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.append(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def clear(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.clear(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def copy(self, *args, **kwargs):
        return self.__list.copy(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self.__list.count(*args, **kwargs)

    def extend(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.extend(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def index(self, *args, **kwargs):
        return self.__list.index(*args, **kwargs)

    def insert(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.insert(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def pop(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.pop(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def remove(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.remove(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def reverse(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.reverse(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret

    def sort(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            ret = self.__list.sort(*args, **kwargs)
        except:
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            self._running.remove(id)
        return ret



registerRDSSubType(list, RDSSubList)
pprint.PrettyPrinter._dispatch[RDSSubList.__repr__] = pprint.PrettyPrinter._pprint_list
