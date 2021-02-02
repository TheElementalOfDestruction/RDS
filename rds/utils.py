from rds.type_conversion import convertType

def restoreRDS(master, dictionary):
    for x in dictionary:
        dictionary[x] = convertType(master, dictionary[x])
    return dictionary
