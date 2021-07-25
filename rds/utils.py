from .type_conversion import convertType

def restoreRDS(master, data):
    """
    Function for restoring the main data instance for a main RDS type. The first
    argument is a
    """
    if isinstance(data, dict):
        for x in data:
            data[x] = convertType(master, data[x])
    elif isinstance(data, list):
        for index, item in enumerate(data):
            data[index] = convertType(master, item)
    else:
        raise TypeError('No matching main RDS type for "{}".'.format(type(data)))

    return data
