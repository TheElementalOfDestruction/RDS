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
