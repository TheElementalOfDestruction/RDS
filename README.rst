|License: GPL v3| |PyPI3| |PyPI1|

RDS
===
Python Redundant Data Storage Module. Store changes made to a dictionary onto the disk in a redundant manor that will prevent it from getting corrupted if the saving is interrupted.

An ``RDSDict`` allows you to make asynchronous and multithreaded modifications to a dictionary safely, and also allows you to have those modifications saved in a way that is redundant. Should the object get interrupted during the saving process, it can restore from the most recently completed entry. An ``RDSList`` is the equivalent class for a list.

To create a new instance, each main RDS type takes two required arguments: ``location`` and ``name``. ``location`` refers to folder where the RDS data will be saved and ``name`` refers to the name of the folder where the individual RDS data will be saved for this instance. While ``location`` can be shared. ``name`` *must* be unique.

.. code:: python

    from rds import RDSDict

    myDict = RDSDict('C:/RDS/', 'myDict')

Once you have a new main instance, it can be used identically to the type that it is replacing. For example, ``RDSDict`` can directly replace a dict in any code, as long as the code does not specifically check if the instance is dict.

Creating a New RDS Type
-----------------------
This module will not be able to detect changes made to an object unless it has a corresponding RDS subtype. As such, if you want to use a custom type in an RDS structure and have changes to it registered, you will need to create your own RDS subtype. Doing so is a relatively simple process. The first thing you must do is create a new class that is a subclass of ``RDSSubBase``.

.. code:: python

    from rds.rds_subtypes import RDSSubBase

    class MyRDSSubType(RDSSubBase):
        def __init__(self, master, instance):
            RDSSubBase.__init__(self, master)
            # Your code here...

You can make the mapping work however you would like, but you should make it so your custom RDS subtype is able to be used identically to the type it will be replacing. Any functions that will be modifying the object should be replaced by one that looks like this:

.. code:: python

    def myFunction(self, *args, **kwargs):
        id = self._awaitTurn()
        try:
            # This is an example of how you could be calling your functions.
            ret = self.__object.myFunction(*args, **kwargs)
        except:
            # Ensure that you remove the current id from the run list is an error has occured.
            self._running.remove(id)
            raise
        try:
            self._save()
        finally:
            # Ensure that you remove the current id from the run list.
            self._running.remove(id)
        return ret

If you need to do some custom procedure every time you save, you can implement your own save function that does that code before calling ``self._master._save()``. Simply replace any calls to ``self._master._save()`` with that function instead.

You must also ensure that your subtype has a ``getData`` method that will either return the actual object being used or a copy of it. It is recommended to return a copy in some way so that you can use ``getData`` to get a copy of the object that is safe to modify. ``getData`` is a method that only takes the ``self`` argument.

Once you have done all of that, you will finally need to register your subtype with the module. So for a RDS subtype called ``MyRDSSubType`` that will be replacing objects of the class ``MyClass``, you would register that like so:

.. code:: python

    registerRDSSubType(MyType, MyRDSSubType)

After that line has been executed, the module will be aware of your subtype and automatically replace any instances of the class you specified with the RDS subtype class.

.. |License: GPL v3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: LICENSE.txt

.. |PyPI3| image:: https://img.shields.io/badge/pypi-1.3.0-blue.svg
   :target: https://pypi.org/project/py-rds/1.3.0/

.. |PyPI1| image:: https://img.shields.io/badge/python-3.6+-brightgreen.svg
   :target: https://www.python.org/downloads/release/python-367/
