'''
Created on Sep 11, 2020

@author: ssmup
'''

class Encoder(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #print("\nEncoder Constructed :D")
        
        '''
        To do list:
        1. Pi scanner (just use find()) done
        2. Pi 000-999 number checker. done
        3. Input string codon-splitter
        4. Codon translator/splicer
        5. Codon re-translator/splicer
        6. GUI?
        
        
        '''
    
    def codonChecker(self, piString, codonLength = 3, maxInt = 1000):
        '''
        Takes a length of pi and checks if all possible codons are found within it.
        A codon is a 3-digit long integer (by default), with values ranging from 000-maxInt.
        Can have more or less than 3-digits per codon. NOT WORTH TRYING WITH LENGTH = 4!!!!!! THE REQUIRED SLICE SIZE IS WAY TOO BIG
        Returns true if all codons are found, false if not.
        '''
        codonList = []
        for i in range(maxInt):
            codonStr = str(i).zfill(codonLength)
            #codonStr = '{:0<3}'.format(i) poor formatting strategy
            codonList.append(codonStr)
        success = True
        for i in range(0,maxInt):
            index = piString.find(codonList[i])
            if(index == -1):
                success = False
        return success
    
    """
    OBSOLETE CODE
    def expansiveCodonChecker(self, piString, frontLimit=0, codonLength=3, maxInt = 1000):
        #'''
        Takes a length of pi and checks if all possible codons are found within it. (via codonChecker)
        Trims the beginning of the string if necessary (trimming earlier slices so it doesn't find the same slice)
        If it passes, it removes a character from the end of the pi string and checks it again (also via codonChecker)
        Continues to do so until it fails, then returns the size of the pi string after all of those characters were removed.
        Useful for identifying slices of pi that contain all the codons and where those slices end.
        #'''
        size = len(piString)
        piString = piString[frontLimit:]
        while(self.codonChecker(piString,codonLength,maxInt)):
            piString = piString[:-1]
            size -= 1
        #print("Failed at: size = {0}, frontLimit = {1}".format(size, frontLimit)) #only useful when developing the method/ debugging pi slicing methods
        return size
    """
        
    def piSliceDefiner(self, piString, codonLength = 3, maxInt = 128, detailedConsoleOut = False):
        '''
        Takes a length of pi and parses it by adding one character at a time to a new string.
        When the new string contains every single codon (which range from 0 to maxInt, formatted to have a length of codonLength),
            it saves the start and end indices of the length of pi copied to the new string into an array.
        The new string is then reset, and the process repeats from that point in the piString.
        Returns the array of indices. Format: [[start,end],[start,end],...,[start,end]]
        WARNING: Very last slice will probably not be accurate if the end of the last entry is the same as the length of the entered parameter piString.
        Useful for determining slices of pi that contain all the codons and where those slices end for a pre-determined length of pi.
        '''
        piSlice = ""
        meltingPiString = piString
        floor = 0
        cap = 0
        sliceDefinitions = []
        print("Searching through {0} characters of pi for codons ranging from 0 to {1}...".format(len(piString),maxInt))
        while(len(meltingPiString) > 0):
            floorIndex = floor
            while(self.codonChecker(piSlice,codonLength,maxInt) == False):
                if(len(meltingPiString) > 0):
                    piSlice += meltingPiString[0] #adds the first character from the meltingPiString to piSlice
                    floor += 1
                    cap += 1
                    meltingPiString = meltingPiString[1:] #removes the character just added to piSlice from the meltingPiString so as to not add the same character twice
                else:
                    return sliceDefinitions #this will fix the issue with the last slice being inaccurate
                    break
            capIndex = cap
            piSlice = ""
            sliceDefinition = [floorIndex,capIndex]
            sliceDefinitions.append(sliceDefinition)
            if(detailedConsoleOut):
                print("Found {0} breakpoint(s)".format(len(sliceDefinitions)))
        return sliceDefinitions
        
    def numStringSlicer(self, numberString, sliceSize = 3):
        '''
        Takes a string of numbers and slices it. Can take a raw int number as well.
        Returns an array of X-digit strings and some leftover at the end if the string has extra digits.
        '''
        numberString = str(numberString)
        length = len(numberString)
        sliceCount = length//sliceSize  #this is floor(length/sliceSize)
        extraDigits = length%sliceSize
        cleanString = numberString
        if(extraDigits > 0):
            cleanString = numberString[:-extraDigits]
            extraString = numberString[length-extraDigits:]
        slices = []
        for i in range(0, sliceCount):
            index = i*3
            stringSlice = cleanString[index:index+3]
            slices.append(stringSlice)
        if(extraDigits > 0):
            slices.append(extraString)
        return slices
    
    def numStringSliceFormatter(self, strings, sliceSize = 3):
        '''
        Takes an array of numString slices (see numStringSlicer) and formats them to all be the same number of digits.
        '''
        formattedStrings = []
        for element in strings:
            formatted = element.zfill(sliceSize)
            formattedStrings.append(formatted)
        return formattedStrings
    
    def codonSubstituter(self, formattedSlicedNumStrings, piSlice):
        '''
        Takes an array of formatted numString slices (see numStringSliceFormatter) and returns an array of codon indices that report where the numString slice is found within the piSlice.
        '''
        subbedList = []
        for numStringSlice in formattedSlicedNumStrings:
            index = piSlice.find(numStringSlice)
            subbedList.append(index)
        return subbedList
    
    def codonTranslator(self,codonSubbedList, piSlice, codonLength = 3):
        '''
        Takes an array of codon indices (see codonSubstituter) and returns an array of formatted numString slices based on the codons found at those indices within the piSlice.
        '''
        numStrings = []
        for codon in codonSubbedList:
            index = int(codon)
            numString = piSlice[index:index+codonLength]
            numStrings.append(numString)
        return numStrings
    
    def numStringGluer(self,strings, strip = False):
        '''
        Takes an array of numString slices and trims leading zeros added by numStringSliceFormatter, glues them together, and returns a single string.
        Optionally strips extra zeros from the left of each codon, but this is off by default.
        '''
        wholeString = ""
        stringCount = len(strings)
        i = 0
        for element in strings:
            if(strip):
                if(i == stringCount-1):
                    wholeString = wholeString + element.lstrip("0")
                else:
                    wholeString = wholeString + element
            else:
                wholeString = wholeString + element
            i += 1
        return wholeString
    
    def stringToAscii(self, string):
        '''
        Takes a string and returns a string of ascii values, where each character in the original string is turned into an ascii value and concatenated onto the returned string.
        '''
        asciiString = ""
        string = str(string)
        for character in string:
            asciiValue = str(ord(character))
            asciiString += asciiValue.zfill(3)
        return asciiString
    
    def asciiToString(self, asciiSlices):
        '''
        Takes an array of ascii codons and turns them into characters before concatenating them. Returns the concatenated string.
        '''
        outString = ""
        for codon in asciiSlices:
            outString += chr(int(codon))
        return outString
            