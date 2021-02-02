import collections
import copy
import os
import pickle
import pprint

from rds.id_generator import IDGenerator
from rds.rds_sub_base import RDSSubBase
from rds.type_conversion import convertType
from rds.utils import restoreRDS


class RDSDict(object):
    __dict = None
    def __init__(self, location, name, redundancy = 2, maxId = 999999):
        location = location.replace('\\', '/')
        location += '' if location.endswith('/') else '/'
        self.__location = location
        self.__name = name
        self.__redundancy = redundancy
        self.__realLocation = self.__location + self.__name + '/'
        self.__formatString = self.__realLocation + '{}.pickle'
        self.__savingFile = self.__realLocation + 'SAVING_STARTED'
        self.__savingFiles = tuple(self.__realLocation + 'SAVING_{}'.format(x) for x in range(redundancy))
        self.__idGen = IDGenerator(maxId)
        self._running = collections.deque()

        self.loadData()

    def getData(self):
        ret = copy.copy(self.__dict)
        for x in ret:
            ret[x] = ret[x].getData() if isinstance(ret[x], RDSSubBase) else ret[x]
        return ret

    def loadData(self):
        """
        Load the dictionary data, if it exists. Otherwise, load an empty dictionary.
        """
        if os.path.exists(self.__formatString.format(0)):
            # We have found evidence that we have saved before, so let's figure out how to load it.
            if os.path.exists(self.__savingFile):
                # The saving file was found, meaning that we were interrupted during saving. This makes everything more complicated...
                interruptId = None
                for name in self.__savingFiles: # Let's try to see if we can find where we were interruppted.
                    if os.path.exists(name):
                        interruptId = int(name.split('_')[-1])
                        break
                if interruptId is None:
                    # We have yet to find the interrupt point, so we need to try something different.
                    lastModifiedTime = -1
                    lastModifiedId = -1
                    for id in range(self.__redundancy):
                        name = self.__formatString.format(id)
                        if os.path.exists(name):
                            mtime = os.stat(name).st_mtime
                            if mtime > lastModifiedTime:
                                lastModifiedTime = mtime
                                lastModifiedId = id
                    interruptId = lastModifiedId + 1

                # By this point we should know exactly where we got interrupted, so let's handle that now.
                idToReadFrom = (self.__redundancy - 1) if interruptId == 0 else interruptId - 1
                with open(self.__formatString.format(idToReadFrom), 'rb') as f:
                    self.__dict = restoreRDS(self, pickle.load(f))

                # Let's do what we can to finish the last save before we do anything.
                self._save(start = interruptId)
            else:
                with open(self.__formatString.format(0), 'rb') as f:
                    self.__dict = restoreRDS(self, pickle.load(f))
        else:
            # We didn't find evidence of having a save, so create new data.
            self.__dict = {}

    def _awaitTurn(self):
        """
        Waits for it's turn before returning. Returns an int.
        """
        id = self.__idGen.generateId()
        self._running.append(id)
        while self._running[0] != id:
            pass # I would prefer to use a sleep function here, but that can be problematic if done with async
        return id

    def _save(self, start = 0):
        """
        Save the data. :param start: specified where we should start saving. This
        is used to finish a save when it was interrupted.
        """
        # Make sure if any dictionaries or lists were added that we change them to the correct type
        for x in self.__dict:
            self.__dict[x] = convertType(self, self.__dict[x])

        os.makedirs(self.__realLocation, exist_ok = True)
        with open(self.__savingFile, 'w') as sf:
            for id in range(start, self.__redundancy):
                with open(self.__savingFiles[id], 'w') as sfn:
                    with open(self.__formatString.format(id), 'wb') as f:
                        pickle.dump(self.getData(), f)
                os.remove(self.__savingFiles[id])
        os.remove(self.__savingFile)

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

pprint.PrettyPrinter._dispatch[RDSDict.__repr__] = pprint.PrettyPrinter._pprint_dict
