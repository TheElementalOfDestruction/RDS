**v1.3.0**
* No longer uses the `IDGenerator`. Waiting for turns now purely uses the `threading.Lock` class and should (hopefully) be faster and a smoother experience.
* Added new class `RDSList`. Works like `RDSDict` in that it can directly replace an existing list object.
* Made RDS objects more resilient. Now if they end up being unable to save they will revert back to the previous version before a change was attempted. Unfortunately this means they will be slightly slower. I did this in a smart way, so only functions where this is a possible problem should be affected. Functions that do not add to the objects cannot prevent a new pickle from being formed, so they will not be checked.
* Fixed the timeout exception not having the data formatted into it when I moved it directly into RDSDict (and RDSList).
* Fixed some issues with in-place operators returning the data the represented instead of the RDS instance.
* Fixed `RDSSubList` missing the `__iter__` function.

**v1.2.2**
* Changed public name for PyPI (why is RDS refused?).
* Fixed README to use new name in links.

**v1.2.1**
* Prepared for upload to PyPI.
* Changed to use relative imports.

**v1.2.0**
* Updated `IDGenerator` to use a lock system as opposed to a socket system. The sockets would occasionally fail for some reason and were not as efficient as they could have been. This should make everything a lot smoother.

**v1.1.5**
* Updated `setup.py`.
* Fixed README.

**v1.1.4**
* Fixed major bug that prevented a lot of list modification functions.

**v1.1.3**
* Fixed major bug that prevented subtypes from working. The parameter `inp` was used, but in the most important place I accidentally put `input` which made it so that no types were being converted.
* Fixed issue in `RDSSubDict` where `convertType` was being called incorrectly.

**v1.1.2**
* Fixed bug in `setup.py` that caused the `rds_subtypes` submodule to not be installed.

**v1.1.1**
* Updated the README to have at least *some* useful information.
* Added docstrings and comments in many places where they were desperately needed.
* Modified the thread used for the `IDGenerator` class so that it would automatically exit when the main thread does.

**v1.1.0**
* Reorganized file structure to place all the RDS subtypes into their own submodule for better organization and ease of access.

**v1.0.1**
* Fixed critical bugs that snuck past testing.
* Added code that will add compatibility between existing RDS objects and the `pprint` module.

**v1.0.0**
* Initial release.
