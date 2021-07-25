import collections
import copy
import os
import pickle
import pprint
import threading

from .rds_subtypes import RDSSubBase
from .type_conversion import convertType
from .utils import restoreRDS


class RDSList(object):
    __list = None
    def __init__(self, location, name, redundancy = 2):
        """
        A Redundant Data Storage List.
        :param location:    The location on the disk where the folder containing
                            the RDS files will be located.
        :param name:        The unique name for this RDSList instance. This is
                            also used as the name of the folder that contains
                            the RDS files.
        :param redundancy:  The level of redundancy to be used. Currently this
                            has no noticable upsides for numbers greater than 3.
                            2 is believed to be the best at the moment, but 3
                            might be better.

        The actual location of the RDS files will be the location plus the name.
        For example, if your location is "/home/user/rds" and your name is
        "rds1", the rds files will be stored in "/home/user/rds/rds1/".
        """
        location = location.replace('\\', '/')
        location += '' if location.endswith('/') else '/'
        self.__location = location
        self.__name = name
        self.__redundancy = redundancy
        # The full path in which the files will be saved.
        self.__realLocation = self.__location + self.__name + '/'
        self.__formatString = self.__realLocation + '{}.pickle'
        self.__savingFile = self.__realLocation + 'SAVING_STARTED'
        self.__savingFiles = tuple(self.__realLocation + 'SAVING_{}'.format(x) for x in range(redundancy))
        self._lock = threading.Lock()

        self.loadData()

    def getData(self):
        """
        Returns a copy of the data in the list. Generally meant for internal use
        as modifying the returned list could end up being problematic.
        """
        ret = copy.copy(self.__list)
        for index, item in enumerate(ret):
            ret[index] = item.getData() if isinstance(item, RDSSubBase) else item
        return ret

    def loadData(self):
        """
        Load the list data, if it exists. Otherwise, load an empty list.
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
                    self.__list = restoreRDS(self, pickle.load(f))
                    if not isinstance(self.__list, list):
                        raise TypeError('Expected to load a list, got {}.'.format(self.__list.__class__.__name__))

                # Let's do what we can to finish the last save before we do anything.
                self._save(start = interruptId)
            else:
                with open(self.__formatString.format(0), 'rb') as f:
                    self.__list = restoreRDS(self, pickle.load(f))
                    if not isinstance(self.__list, list):
                        raise TypeError('Expected to load a list, got {}.'.format(self.__list.__class__.__name__))
        else:
            # We didn't find evidence of having a save, so create new data.
            self.__list = []

    def _awaitTurn(self):
        """
        Waits for it's turn before returning. Returns an exception if 20 seconds
        pass and it is not it's turn yet to prevent an infinite stop.
        """
        if not self._lock.acquire(timeout = 20):
            raise Exception('RDSList ({}) was waiting for 20 seconds without being able to aquire a lock.'.format(self))

    def _save(self, start = 0):
        """
        Save the data. :param start: specifies where we should start saving.
        This is used to finish a save when it was interrupted.
        """
        # Make sure if any dictionaries or lists were added that we change them to the correct type.
        for index, item in enumerate(self.__list):
            self.__list[index] = convertType(self, item)

        # Make the save directory if it doesn't exist.
        os.makedirs(self.__realLocation, exist_ok = True)

        # Make a file to show we are currently saving.
        with open(self.__savingFile, 'w') as sf:
            for id in range(start, self.__redundancy):
                # Make a file to show which level of redundancy we are on.
                with open(self.__savingFiles[id], 'w') as sfn:
                    # Open the current redundancy file and save to it.
                    with open(self.__formatString.format(id), 'wb') as f:
                        pickle.dump(self.getData(), f)
                # If we finished the current redundancy, delete the marker for it.
                os.remove(self.__savingFiles[id])
        # If we finished saving, then delete the saving marker.
        os.remove(self.__savingFile)

    # From here on we need to forward the functions to our dict or intercept them.
    def __add__(self, *args, **kwargs):
        return self.__list.__add__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self.__list.__contains__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        self._awaitTurn()
        try:
            ret = self.__list.__delitem__(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        finally:
            self._lock.release()
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
        self._awaitTurn()
        backup = copy.copy(self.__list)
        try:
            self.__list.__iadd__(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        except:
            self.__list = backup
            raise
        finally:
            self._lock.release()
        return self # Special instance where we need to return self.

    def __imul__(self, *args, **kwargs):
        self._awaitTurn()
        try:
            self.__list.__imul__(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        finally:
            self._lock.release()
        return self # Special instance where we need to return self.

    def __iter__(self, *args, **kwargs):
        return self.__list.__iter__(*args, **kwargs)

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
        self._awaitTurn()
        backup = copy.copy(self.__list)
        try:
            ret = self.__list.__setitem__(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        except:
            self.__list = backup
            raise
        finally:
            self._lock.release()
        return ret

    def __sizeof__(self, *args, **kwargs):
        return self.__list.__sizeof__(*args, **kwargs)

    def append(self, *args, **kwargs):
        self._awaitTurn()
        backup = copy.copy(self.__list)
        try:
            ret = self.__list.append(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        except:
            self.__list = backup
            raise
        finally:
            self._lock.release()
        return ret

    def clear(self, *args, **kwargs):
        self._awaitTurn()
        try:
            ret = self.__list.clear(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        finally:
            self._lock.release()
        return ret

    def copy(self, *args, **kwargs):
        return self.__list.copy(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self.__list.count(*args, **kwargs)

    def extend(self, *args, **kwargs):
        self._awaitTurn()
        backup = copy.copy(self.__list)
        try:
            ret = self.__list.extend(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        except:
            self.__list = backup
            raise
        finally:
            self._lock.release()
        return ret

    def index(self, *args, **kwargs):
        return self.__list.index(*args, **kwargs)

    def insert(self, *args, **kwargs):
        self._awaitTurn()
        backup = copy.copy(self.__list)
        try:
            ret = self.__list.insert(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        except:
            self.__list = backup
            raise
        finally:
            self._lock.release()
        return ret

    def pop(self, *args, **kwargs):
        self._awaitTurn()
        try:
            ret = self.__list.pop(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        finally:
            self._lock.release()
        return ret

    def remove(self, *args, **kwargs):
        self._awaitTurn()
        try:
            ret = self.__list.remove(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        finally:
            self._lock.release()
        return ret

    def reverse(self, *args, **kwargs):
        self._awaitTurn()
        try:
            ret = self.__list.reverse(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        finally:
            self._lock.release()
        return ret

    def sort(self, *args, **kwargs):
        self._awaitTurn()
        try:
            ret = self.__list.sort(*args, **kwargs)
        except:
            self._lock.release()
            raise
        try:
            self._save()
        finally:
            self._lock.release()
        return ret



# Add handling to the pprint module for RDSDict.
pprint.PrettyPrinter._dispatch[RDSList.__repr__] = pprint.PrettyPrinter._pprint_list
