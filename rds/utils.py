from rds.type_conversion import convertType

def restoreRDS(master, dictionary):
    for x in dictionary:
        dictionary[x] = convertType(master, dictionary[x])
    return dictionary

def stop():
    """
    Stops all threads of the IDGenerator classes.
    """
    import rds.id_generator
    rds.id_generator.stop = True
