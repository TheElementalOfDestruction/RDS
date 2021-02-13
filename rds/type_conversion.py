# Dictionary that will contain all available RDS subtypes. Use `registerRDSSubType` to add to this list.
TYPE_CONVERSION_DICT = {}

def convertType(master, inp):
    """
    Converts the inputs to the correct type
    """
    return TYPE_CONVERSION_DICT.get(type(inp), noType)(master, inp)

def noType(master, inp):
    """
    Specifies that the type does not have a dedicated RDS conversion.
    """
    return inp

def registerRDSSubType(_type, rds_handler):
    """
    Adds a RDSSubType handler for the specified type. Generally, the handler should
    be a class.
    """
    TYPE_CONVERSION_DICT[_type] = rds_handler
