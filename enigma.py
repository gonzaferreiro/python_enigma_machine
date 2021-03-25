import re
import functools
from abc import ABC
from abc import abstractmethod
from errorHandling import InputError
from errorHandling import PlugboardError
from errorHandling import inputValidator
from tools import printStatus
from tools import positionLooper

class PlugLead:
    """PlugLead object to be included within a Plugboard
    object. Responsible for encoding the letters it owns 
    at the begninning and at the end of the encoding process.
    """

    @inputValidator('inputElement','PlugLead')
    def __init__(self,letters):
        """
        Parameters
        ----------

        letters : str
            String with the two letters corresponding 
            to the PlugLead, e.g. 'AE'.
        """
        self.lettersList = [x.lower() for x in letters]
        
    @inputValidator('encodingElement','PlugLead')
    def encode(self,letterInput):
        """Function responsible for encoding the input coming
        into the plugboard after looking for the spceific PlugLead
        storing the letter to be encoded.

        Parameters
        ----------
        letterInput : str
            Input letter to be encoded.

        Returns
        -------
        str
            Returns encoded letter.
        """
            
        if letterInput not in self.lettersList:
            return letterInput.upper()
        
        else:
            return list(filter(lambda x: x!=letterInput,self.lettersList))[-1].upper()
class Plugboard:
    """Plugboad object to be included within an Enigma
    Machine object. Responsible for storing the set of PlugLeads and 
    enoding single letters by fnidng and using the right PlugLead.
    """
    def __init__(self,numPlugLeads=10):
        """
        Parameters
        ----------

        numPlugLeads : int
            Maximum number of PlugLeads to be stored by the
            Plugboard. 10 by default, but ca be up to 13.
        """
        self.plugLeadsLetters = []
        self.plugLeads = []

        if numPlugLeads > 13:
            raise ValueError("{} - > [Plugboad]".format(numPlugLeads) +
        " Number of PlugLeads cannot be greater than 13")

        else:
            self.numPlugLeads = numPlugLeads
        
    def add(self,PlugLead):
        """Add a PlugLead object to the list of PlugLeads up
        to the maximum number of PlugLeads allowed. Storing as well
        the individual letters of the PlugLead object into a list
        for easy retrieval.

        Parameters
        ----------
        PlugLead : PlugLead
            PlugLead object to be stored for decoding.

        Raises
        ------
        PlugboardError
            If the number of PlugLeads exceeds the maximum or any
            of the letters in the PlugLead object has been already
            assigned to another PlugLead object.
        """
        currentPlugLeads = []
        
        if len(self.plugLeads) == self.numPlugLeads:
            errorMessage = 'Cannot add. Max number of PlugLeads has been reached ({}).'.format(self.numPlugLeads)
            raise PlugboardError(''.join([x.upper() for x in PlugLead.lettersList]),errorMessage)
        
        for x in PlugLead.lettersList:
            
            if x in self.plugLeadsLetters:
                errorMessage = 'Already assigned to another PlugLead.'+\
                'Please restart your Enigma Machine for including it.'
                raise PlugboardError(x.upper(), errorMessage)
                
            else:
                
                currentPlugLeads.append(x)
                
        self.plugLeadsLetters += currentPlugLeads
        self.plugLeads.append(PlugLead)
    
    @inputValidator('encodingElement', 'Plugboard')
    def encode(self,letterInput):
        """Looks for the PlugLead object owner of the letter to be 
        encoded and calls its encode function.capitalize()

        Parameters
        ----------
        letterInput : str
            Input letter coming to be encoded.

        Returns
        -------
        str
            Returns encoded letter.
        """

        if letterInput in self.plugLeadsLetters:
            plugBoard = self.plugLeads[self.plugLeadsLetters.index(letterInput)//2]
            return plugBoard.encode(letterInput)
        
        else:
            return letterInput.upper()

class EnigmaMachine:
    """Enigma Machine object, responsible for storing and all the 
    underlying objects and orchestrating the entire cycle of encoding.
    """
    
    def __init__(self):
        """
        Parameters
        ----------

        None
        """
        self.rotorsList = []
        self.plugBoard = None
        self.reflector = None
    
    def addRotor(self, rotorObject, order):
        """Function for adding a Rotor object into the enigma machine.

        Parameters
        ----------
        rotorObject : Rotor
            Rotor object to be added.
        order : int
            Relative order from left to right of the rotor between rotors.

        Raises
        ------
        ValueError
            If position of the rotor to be added is invalid.
        """
        if type(order) != int or  order < 1:
            raise ValueError("Position {} is invalid for rotor {}".format(order,rotorObject.name))

        elif order-1 > len(self.rotorsList):
            raise ValueError("Rotor {} out of order or yet not enough rotors for position {}.".format(rotorObject.name,order))

        else:
            self.rotorsList.insert(order-1,rotorObject)
        
    def addPlugBoard(self, plugBoardObject):
        """Function for adding a Pugboard object into the enigma machine.

        Parameters
        ----------
        plugBoardObject : Plugboard
            Plugboard object to be added.
        """
        self.plugBoard = plugBoardObject
        
    def addReflector(self, reflectorObject):
        """Function for adding a Reflector object into the enigma machine.

        Parameters
        ----------
        reflectorObject : Reflector
            Reflector object to be added.
        """
        self.reflector = reflectorObject

    def serialEncode(self, inputString, printStatusFlag=False):
        """Function that receives a string of length greater than 1
        and iterates through each letter encoding/decoding them.

        Parameters
        ----------
        inputString : str
            String to be decoded/encoded.
        printStatusFlag : bool, optional
            Flag for using the printing feature, which prints at each
            step of the encoding/decodig process the behaviour of the elements
            of the enigma machine. Ideal for debugging or understanding the
            transformation along the way. By default False

        Returns
        -------
        str
            Returns the encoded/decoded string.
        """

        encodedString = ''

        for s in inputString:
            encoded_s = self.fullEncode(s, printStatusFlag)
            encodedString += encoded_s
            # Closing script encoding again through the plugboard
            finalEncodedInputPrint = 'Encoded input so far: {}\n'.format(encodedString)
            printStatus(finalEncodedInputPrint,printStatusFlag)

        return encodedString.upper()

    @inputValidator('encodingElement','Element to encode')
    def fullEncode(self, inputLetter, printStatusFlag=False):
        """Function for running one entire iteration (i.e. one letter)
        of encoding/decoding. Going through every object and every step of 
        the process and returning the encoded letter.

        Parameters
        ----------
        inputLetter : str
            Letter to be encoded/decoded.
        printStatusFlag : bool, optional
            Flag for using the printing feature, which prints at each
            step of the encoding/decodig process the behaviour of the elements
            of the enigma machine. Ideal for debugging or understanding the
            transformation along the way. By default False

        Returns
        -------
        str
            Returns de encoded/decoded letter.
        """
        
        # First, we encode using the plugboard settings
        encodedInput = self.plugBoard.encode(inputLetter)
        plugboardString = 'Plugboard transforms input in: {}\n'.format(encodedInput)
        printStatus(plugboardString,printStatusFlag)
        
        numRotors = len(self.rotorsList)
        # Obtaining initial positions before turning anything
        initialPositions = [x.currentPos for x in self.rotorsList]
        # List for checking that rotors only turn once
        hasTurned = [False]*numRotors
        # Checking whether rotors have a notchless rotor to their right
        notchlessToTheRight = [False if x==1 
                            else self.rotorsList[-x+1].rotorType=='notchless' 
                            for x in range(1,numRotors+1)]
        
        # Setting up notifications and printing if requested
        startPrint = 'Starting with rotors at: {}'.format([x.currentPos for x in self.rotorsList])
        lettersPrint = 'Corresponding letters: {}\n'.format([x.genericMapping[x.currentPos] for x in self.rotorsList])
        printStatus(startPrint,printStatusFlag)
        printStatus(lettersPrint,printStatusFlag)
        
        # Turning rotors if notch has been reached
        for r in range(1,numRotors+1):
            currentPos = initialPositions[-r]
            letterCurrentPos = self.rotorsList[-r].genericMapping[currentPos]
            notch = self.rotorsList[-r].notch
            
            # Updating positions if:
            # 1. Notch has been reached
            # 2. We are within the first three rotors
            # 3. The rotor to the right is not a notchless rotor
            # ---------------
            # IMPORTANT:
            # When a rotor, let's say A, reaches its notch, 
            # it can turn when the rotor to its left engages 
            # the notch with its pawl turning itself 
            # and A, i.e. its right neighbour
            if letterCurrentPos in notch and r in [1,2] and not notchlessToTheRight[-r]:
                
                # if it hasn't turned before, the rotor that's
                # at its notch will rotate now due to the rotor
                # to its left engaging with its rachet
                if not hasTurned[-r]:
                    updatedPos = positionLooper(self.rotorsList[-r].currentPos+1,25)
                    self.rotorsList[-r].currentPos = updatedPos
                    hasTurned[-r] = True

                # If it hasn't turned, then the rotor to the left
                # will turn now after engaging the ratchet
                # ---------------
                # IMPORTANT NOTE:
                # Rotors further to the left shouldn't rotate
                if r <= 2:
                    updatedPos = positionLooper(self.rotorsList[-r-1].currentPos+1,25)
                    self.rotorsList[-r-1].currentPos = updatedPos
                    hasTurned[-r-1] = True
        
        # If first rotor did not turn yet, then turn
        if not hasTurned[-1]:
            updatedPos = positionLooper(self.rotorsList[-1].currentPos+1,25)
            self.rotorsList[-1].currentPos = updatedPos
                
        # Encoding after turns have happened
        # Encoding from right to left
        for r in reversed(self.rotorsList):   
            encodedInput = r.encode(encodedInput,'right',printStatusFlag)
            name = r.name  
            
        # Refector encoding
        encodedInput = self.reflector.encode(encodedInput,'left',printStatusFlag)
        name=self.reflector.name
        relectorPrint = 'Reflector {} transforms input in: {}\n'.format(name,encodedInput)
        printStatus(relectorPrint,printStatusFlag)
                                                
        # Encoding from left to right
        for r in self.rotorsList:
            encodedInput = r.encode(encodedInput,'left',printStatusFlag)
            name = r.name

        encodedInput = self.plugBoard.encode(encodedInput)
                                                                    
        return encodedInput.upper()

    def setup(self, rotors, reflector, plugleads=None, numPlugLeads=10):
        """Function for setting up your brand new Enigma Machine
        in one simple line including the required objects.

        Parameters
        ----------
        rotors : list
            List with the rotors to be used, including the name,
            initial position, ring setting and position in the machine
            from left to right. For example, for setting up a
            Rotor Beta in the rightmost position in a machine with 
            four rotors you'd enter the follwing:
            * ['RotorBeta',1,'A',4].
            For setting up a Custom Rotor you'd need to necessarily 
            add the mapping. Additionaly you could add one or several 
            notches as well. Take the following example for setting up
            a Custom Rotor in the first position from left to right
            with two notches at the letter E and Z:
            * ['RotorCustom',1,'A',1, 'ABCEDGFHIJKLMNOPQRSTUVWXYZ','EZ']
            Take the following example for setting up a Custom Rotor
            without notches at the second position from left to right:
            * ['RotorCustom',1,'A',2, 'ABCEDGFHIJKLMNOPQRSTUVWXYZ']
        reflector : str
            Name of the reflector to be used. Can be a singular string
            or a list containing the name of the reflector and its
            mapping in case of being a Custom Reflector.
            Example of custom reflector:
            ['ReflectorCustom','ABCEDGFHIJKLMNOPQRSTUVWXYZ']
        plugleads : str, optional
            String with the combinations of letters to be set up in the
            PlugLead objects, by default None. For example, for setting up
            2 PlugLeads for the letters AB and CD you'd need the
            following str: "AB CD".
        numPlugLeads: str, optional
            Parameter for including more than the default number of Plug
            of PlugLeads (10) if wanted.
        """
        myPlugboard = Plugboard(numPlugLeads)
        self.addPlugBoard(myPlugboard)
        
        if plugleads is not None:
            plugleads = plugleads.split(' ')

            for i in plugleads:
                self.plugBoard.add(PlugLead(i))

        validRotors = ['RotorI','RotorII','RotorIII','RotorIV','RotorV','RotorBeta',\
            'RotorGamma','RotorVI','RotorVII','RotorVIII','RotorCustom']

        validReflectors = ['ReflectorA','ReflectorB',\
            'ReflectorC','ReflectorBThin','ReflectorCThin','ReflectorCustom']

        # Validating entry for rotors
        if len(rotors) < 3:
            raise ValueError('Minimum number of rotors is 3.')
        
        for i in rotors:
            if len(i) < 4:
                raise ValueError('Please enter a valid number of arguments for rotor {}'.format(i[0]))
            else:
                if i[0] in validRotors:
                    if i[0] == 'RotorCustom':
                        if len(i) == 5 and len(i[4])==26:
                            rotor = globals()[i[0]](i[1],i[2],i[4])
                            self.addRotor(rotor,i[3])
                        elif len(i) == 6 and len(i[4])==26:
                            rotor = globals()[i[0]](i[1],i[2],i[4],i[5])
                            self.addRotor(rotor,i[3])
                        else:
                            raise ValueError('Please enter valid arguments for rotor {}.'.format(i[0]) +\
                                ' Name, Ring Settings (1-26), Initial Position (A-X), relative' +\
                                ' position between rotors and mapping (26 different letters). ')
                    else:
                        if len(i) == 4:
                            rotor = globals()[i[0]](i[1],i[2])
                            self.addRotor(rotor,i[3])
                        else:
                            raise ValueError('Please enter a valid number of arguments for rotor {}'.format(i[0]))
                else:
                    raise ValueError('{} is not a valid rotor. Valid options are: {}'.format(i[0],validRotors))

        # Validating entry for reflector    
        if type(reflector) == list:
            if len(reflector) != 2:
                    raise ValueError('Please enter a valid number of arguments for Reflector')
            else:
                if reflector[0] in validReflectors and len(reflector[1]) == 26:
                    reflector = globals()[reflector[0]](reflector[1])
                else:
                    raise ValueError('Please enter valid arguments for reflector {}.'.format(reflector[0]) +\
                        ' Valid reflector and mappgin with 26 letters')
        else:
            if reflector in validReflectors:
                reflector = globals()[reflector]()
            else:
                raise ValueError('{} is not a valid rotor. Valid options are: {}'.format(reflector,validReflectors))

        self.addReflector(reflector)

class Rotor(ABC):
    """Rotor superclass. Stores generic attributes and owns the
    setup and encoding functions to be used by individual rotors.
    """
    
    @abstractmethod
    def __init__(self, ringSetting, initialPos, rotorType, name):
        """
        Parameters
        ----------

        ringSetting : int
            Number of the ring settings, from 1 to 26.
        intialPos: str
            Initial position of the rotor, from A to Z.
        """
        genericMapping = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                          'N','O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        self.genericMapping = genericMapping
        self.rotorType = rotorType
        self.name = name
        self.mapping = None
        
        if rotorType == 'reflector':
            self.ringSetting = ringSetting
            self.initialPos = initialPos
            self.currentPos = initialPos

        else:
            self.ringSetting = self.set_ring_setting(ringSetting)
            self.initialPos = self.set_initial_pos(initialPos)
            self.currentPos = self.set_initial_pos(initialPos)
        
    @inputValidator('ringSetting','Ring Settings')
    def set_ring_setting(self, ringSetting):
        """If input is valid returns ring settings.

        Parameters
        ----------
        ringSetting : int
            Number of the ring settings, from 1 to 26.

        Returns
        -------
        int
            Ring setting validated from 0 to 25 for internal use.
        """
        return ringSetting-1
        
    @inputValidator('encodingElement','Initial Position')
    def set_initial_pos(self, initialPos):
        """If input is valid returns intiial position.

        Parameters
        ----------
        initialPos : str
            Initial position of the rotor, from A to Z.

        Returns
        -------
        str
            Initial position validated.
        """
        return self.genericMapping.index(initialPos.upper())
    
    @inputValidator('encodingElement','')
    def encode(self, letterInput, direction, printFlag):
        """Function used by both rotors and reflectors
        for the encoding of single letters.

        Parameters
        ----------
        letterInput : str
            Letter to be encoded/decoded.
        direction : str
            Only "right" and "left" are valid.
        printFlag : boolean
            Flag for using the printing feature, which prints at each
            step of the encoding/decodig process the behaviour of the elements
            of the enigma machine. Ideal for debugging or understanding the
            transformation along the way. 

        Returns
        -------
        str
            Decoded/encoded letter.
        """
        if self.rotorType == 'reflector':
            return self.mapping[self.genericMapping.index(letterInput.upper())].lower()
        else:
            letterPos = self.genericMapping[self.currentPos]
            offset = self.currentPos-self.ringSetting
            startString1 = 'Coming into rotor {} at position {} ({}) '.format(self.name,letterPos,self.currentPos)
            startString2 = 'and ring settings {} | '.format(self.ringSetting)
            startString3 = 'Offset {}'.format(offset)
            printStatus(startString1+startString2+startString3,printFlag)
            inputIndex = self.genericMapping.index(letterInput.upper())
            inputIndexString1 = 'Input letter index is {}. '.format(inputIndex)
            inputIndexOffset = positionLooper(inputIndex+offset,25)
            inputIndexString2 = 'Adjusted index {} '.format(inputIndexOffset)
            letterInputOffset = self.genericMapping[inputIndexOffset]
            inputIndexString3 = 'tranforms input letter in {}'.format(letterInputOffset)
            printStatus(inputIndexString1+inputIndexString2+inputIndexString3,printFlag)
            if direction == 'right':
                index = self.genericMapping.index(letterInputOffset)
                indexString = 'Input letter {} holds genericMappingIndex {}'.format(letterInputOffset, index)
                printStatus(indexString,printFlag)
                letter = self.mapping[index]
                letterString = 'Corresponding to rotorLetter {}'.format(letter)
                printStatus(letterString,printFlag)
            else:
                index = self.mapping.index(letterInputOffset)
                indexString = 'Input letter {} holds rotorIndex {}'.format(letterInputOffset, index)
                printStatus(indexString,printFlag)
                letter = self.genericMapping[index]
                letterString = 'Corresponding to genericMappingLetter {}'.format(letter)
                printStatus(letterString,printFlag)
            outputIndexOffset = positionLooper(self.genericMapping.index(letter)-offset,25)
            returnLetter = self.genericMapping[outputIndexOffset]
            returnString = 'Applying offset returns letter {}\n'.format(returnLetter)
            printStatus(returnString,printFlag)
            return returnLetter.upper()     
        
class RotorI(Rotor):
    """Rotor's child class for Rotor I.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchrotor', name='I')
        self.notch = ['Q']
        self.mapping = ['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O',
                        'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R', 'C', 'J']
        
class RotorII(Rotor):
    """Rotor's child class for Rotor II.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchrotor', name='II')
        self.notch = ['E']
        self.mapping = ['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W',
                        'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V', 'O', 'E']
        
class RotorIII(Rotor):
    """Rotor's child class for Rotor III.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchrotor', name='III')
        self.notch = ['V']
        self.mapping = ['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z',
                        'N', 'Y', 'E', 'I', 'W', 'G', 'A', 'K', 'M', 'U', 'S', 'Q', 'O']
        
class RotorIV(Rotor):
    """Rotor's child class for Rotor IV.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchrotor', name='IV')
        self.notch = ['J']
        self.mapping = ['E', 'S', 'O', 'V', 'P', 'Z', 'J', 'A', 'Y', 'Q', 'U', 'I', 'R',
                        'H', 'X', 'L', 'N', 'F', 'T', 'G', 'K', 'D', 'C', 'M', 'W', 'B']
        
class RotorV(Rotor):
    """Rotor's child class for Rotor V.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchrotor', name='V')
        self.notch = ['Z']
        self.mapping = ['V', 'Z', 'B', 'R', 'G', 'I', 'T', 'Y', 'U', 'P', 'S', 'D', 'N',
                        'H', 'L', 'X', 'A', 'W', 'M', 'J', 'Q', 'O', 'F', 'E', 'C', 'K']
        
class RotorBeta(Rotor):
    """Rotor's child class for Rotor Beta.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchlessrotor', name='beta')
        self.notch = [False]
        self.mapping = ['L', 'E', 'Y', 'J', 'V', 'C', 'N', 'I', 'X', 'W', 'P', 'B', 'Q',
                        'M', 'D', 'R', 'T', 'A', 'K', 'Z', 'G', 'F', 'U', 'H', 'O', 'S']
        
class RotorGamma(Rotor):
    """Rotor's child class for Rotor Gamma.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchlessrotor', name='gamma')
        self.notch = [False]
        self.mapping = ['F', 'S', 'O', 'K', 'A', 'N', 'U', 'E', 'R', 'H', 'M', 'B', 'T',
                        'I', 'Y', 'C', 'W', 'L', 'Q', 'P', 'Z', 'X', 'V', 'G', 'J', 'D']

class RotorVI(Rotor):
    """Rotor's child class for Rotor VI.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchrotor', name='VI')
        self.notch = ['Z','M']
        self.mapping = [x for x in 'JPGVOUMFYQBENHZRDKASXLICTW']

class RotorVII(Rotor):
    """Rotor's child class for Rotor VII.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchrotor', name='VII')
        self.notch = ['Z','M']
        self.mapping = [x for x in 'NZJHGRCXMYSWBOUFAIVLPEKQDT']

class RotorVIII(Rotor):
    """Rotor's child class for Rotor VII.
    """
    def __init__(self, ringSetting, initialPos):
        super().__init__(ringSetting, initialPos, rotorType='notchrotor', name='VIII')
        self.notch = ['Z','M']
        self.mapping = [x for x in 'FKQHTLXOCBJSPDZRAMEWNIUYGV']

class RotorCustom(Rotor):
    """Rotor's child class for Custom Rotor.
    """
    def __init__(self, ringSetting, initialPos, mapping, notches=None):
        """
        Parameters
        ----------

        ringSetting : int
            Number of the ring settings, from 1 to 26.
        intialPos: str
            Initial position of the rotor, from A to Z.
        mapping: str
            String coontaining all the letters from the alphabet
            in the desired order for the rotor's custom mapping.
        notches : str, optional
            String letter or letters to be used as notches.
            For example "A" for one notch or "TZ" for two notches.
            None by default.
        """
        if notches is None:
            rotorType = 'notchlessrotor'
            itsNotch = [False]
        else:
            rotorType = 'notchrotor'
            itsNotch = [x for x in notches]
            elementsCount = dict.fromkeys(itsNotch, 0)
            for i in itsNotch:
                elementsCount[i] += 1
            if sorted(elementsCount.values())[-1] > 1:
                raise ValueError("Notches cannot repeat letters.")
            if len(itsNotch) > 26:
                raise ValueError('Amount of notches cannot be greater than 26.')
        super().__init__(ringSetting, initialPos, rotorType=rotorType, name='custom')
        self.notch = itsNotch
        self.mapping = [x for x in mapping]
        elementsCount = dict.fromkeys(mapping, 0)
        for i in mapping:
            elementsCount[i] += 1
        if sorted(elementsCount.values())[-1] > 1:
            raise ValueError("Mapping cannot repeat letters.")
        else:
            self.mapping = [x for x in mapping]
        
class ReflectorA(Rotor):
    """Rotor's child class for Reflector A.
    """
    def __init__(self):
        """
        Parameters
        ----------

        None
        """
        super().__init__(ringSetting=None, initialPos=None, rotorType='reflector', name='A')
        self.notch = [False]
        self.mapping = ['E', 'J', 'M', 'Z', 'A', 'L', 'Y', 'X', 'V', 'B', 'W', 'F', 'C',
                        'R', 'Q', 'U', 'O', 'N', 'T', 'S', 'P', 'I', 'K', 'H', 'G', 'D']
        
class ReflectorB(Rotor):
    """Rotor's child class for Reflector B.
    """
    def __init__(self):
        """
        Parameters
        ----------

        None
        """
        super().__init__(ringSetting=None, initialPos=None, rotorType='reflector', name='B')
        self.notch = [False]
        self.mapping = ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O',
                        'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T']
        
class ReflectorC(Rotor):
    """Rotor's child class for Reflector C.
    """
    def __init__(self):
        """
        Parameters
        ----------

        None
        """
        super().__init__(ringSetting=None, initialPos=None, rotorType='reflector', name='C')
        self.notch = [False]
        self.mapping = ['F', 'V', 'P', 'J', 'I', 'A', 'O', 'Y', 'E', 'D', 'R', 'Z', 'X',
                        'W', 'G', 'C', 'T', 'K', 'U', 'Q', 'S', 'B', 'N', 'M', 'H', 'L']
        
class ReflectorBThin(Rotor):
    """Rotor's child class for Reflector B Thin.
    """
    def __init__(self):
        """
        Parameters
        ----------

        None
        """
        super().__init__(ringSetting=None, initialPos=None, rotorType='reflector', name='BThin')
        self.notch = [False]
        self.mapping = [x for x in 'ENKQAUYWJICOPBLMDXZVFTHRGS']

class ReflectorCThin(Rotor):
    """Rotor's child class for Reflector C Thing.
    """
    def __init__(self):
        """
        Parameters
        ----------

        None
        """
        super().__init__(ringSetting=None, initialPos=None, rotorType='reflector', name='BThin')
        self.notch = [False]
        self.mapping = [x for x in 'ENKQAUYWJICOPBLMDXZVFTHRGS']

class ReflectorCustom(Rotor):
    """Rotor's child class for Custom Reflector.
    """
    def __init__(self,mapping):
        """
        Parameters
        ----------

        mapping: str
            String coontaining all the letters from the alphabet
            in the desired order for the rotor's custom mapping.
        """
        super().__init__(ringSetting=None, initialPos=None, rotorType='reflector', name='custom')
        self.notch = [False]
        elementsCount = dict.fromkeys(mapping, 0)
        for i in mapping:
            elementsCount[i] += 1
        if sorted(elementsCount.values())[-1] > 1:
            raise ValueError("Mapping cannot repeat letters.")
        else:
            self.mapping = [x for x in mapping]