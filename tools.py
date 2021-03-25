from errorHandling import inputValidator

def printStatus(string,boolean):
    """Function for printing updates along the coding/encoding process.

    Parameters
    ----------
    string : str
        String to be shown.
    boolean : bool
        Whether should the string be printed or not.
    """
    if boolean:
        print(string)

def positionLooper(inputNumber,base):
    """Helper function for when either the ring settings
    or the position of the rotors go above their max value.
    For example, if input number is 28 and base is 26
    the function will return 2.

    Parameters
    ----------
    inputNumber : int
        Input coming in the function for being evaluated.
    base : int
        Maxixmum number allowed to be reached.

    Returns
    -------
    int
        Returns corrected number within the allowed range.
    """
    if inputNumber>=0 and inputNumber <= base:
        return inputNumber
    elif inputNumber < 0:
        return (inputNumber%base)+1
    else:
        return (inputNumber%base)-1