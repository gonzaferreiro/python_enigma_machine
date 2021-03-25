import re
import functools

class InputError(Exception):
    """Exception to be raised for invalid inputs.
    """

    def __init__(self, char, message="Input is invalid."):
        """
        Parameters
        ----------

        char : str
            Invalidad character raising this exception.
        message: str
            Message to be shown when this exception is raised.
        """
        self.char = char
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "{0} - > {1}".format(self.char,self.message)

class PlugboardError(Exception):
    """Exception to be raised when there's an error with the PlugBoard.
    """

    def __init__(self, char, message):
        """
        Parameters
        ----------

        char : str
            Invalidad character raising this exception.
        message: str
            Message to be shown when this exception is raised.
        """
        self.char = char
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "{0} - > {1}".format(self.char,self.message)

def inputValidator(component, element):
    """Decorator for validating the input for several
    functions across the programme.

    Parameters
    ----------
    component : Str
        Part of the enigma machine or action to be performed.
        For example: 'encodingElement' or 'ringSettting'.
    element : Str
        String to be included within the error message.
        Makes reference to the type of component.add()
        For example: 'Ring Settings' or 'Initial Position'.
    """
    def function_decorator(function):
        def cleaning_function(selfObject, currentInput, *args, **kwargs):
            
            if component in ['inputElement','encodingElement']:
            
                lettersClean = "".join(re.findall("[a-zA-Z]+", currentInput))
                amountLettersInput = len(currentInput)
                amountLettersClean = len(lettersClean)

                if amountLettersInput > amountLettersClean:
                    raise InputError(currentInput, message="[{0}] Input can only take letters [a-zA-Z].".format(element))

                if component in 'inputElement':

                    if amountLettersClean != 2:
                        raise InputError(currentInput, message="[{0}] Input must cointain TWO letters.".format(element))

                    elif lettersClean[0] == lettersClean[1]:
                        raise InputError(currentInput, message="[{0}] Input letters must be different.".format(element))

                elif component == 'encodingElement':

                    if amountLettersClean != 1:
                        raise InputError(currentInput, message="[{0}] Input must cointain ONE letter.".format(element))

                return function(selfObject,lettersClean.lower(), *args, **kwargs)
            
            elif component in ['ringSetting']:
                inputClean = int("0"+"".join(re.findall("[0-9]+", str(currentInput))))
                amountCharsInput = len(str(currentInput))
                amountCharsClean = len(str(inputClean))

                if inputClean < 1 or inputClean > 26 or amountCharsInput > amountCharsClean:
                    raise InputError(currentInput, message="[{0}] Input can only take numbers between 1-26.".format(element))

                return function(selfObject,inputClean, *args, **kwargs)
            
            else:
                
                print('tu vieja')

        r = functools.update_wrapper(cleaning_function, function)
        return r

    return function_decorator

