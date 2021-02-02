RDS
===
Python Redundant Data Storage Module. Store changes made to a dictionary onto the disk in a redundant manor that will prevent it from getting corrupted if the saving is interrupted.

An `RDSDict` allows you to make asynchronous and multithreaded modifications to a dictionary safely, and also allows you to have those modifications saved in a way that is redundant. Should the object get interrupted during the saving process, it can restore from the most recently completed entry.

Each `RDSDict` object will have it's own `IDGenerator` object with generates a (reasonably) unique id for each modification. This number will eventually loop back down, but is customizable for your use case.
