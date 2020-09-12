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
    
    def codonChecker(self, piString):
        '''
        Takes a length of pi and checks if all possible codons are found within it.
        A codon is a 3-digit long integer, with values ranging from 000-999.
        Returns true if all codons are found, false if not.
        '''
        codonList = []
        for i in range(1000):
            codonStr = '{:0>3}'.format(i)
            codonList.append(codonStr)
        success = True
        for i in range(0,1000):
            index = piString.find(codonList[i])
            if(index == -1):
                success = False
        return success
    
    def expansiveCodonChecker(self, piString, frontLimit=0):
        '''
        Takes a length of pi and checks if all possible codons are found within it. (via codonChecker)
        Trims the beginning of the string if necessary (trimming earlier slices so it doesn't find the same slice)
        If it passes, it removes a character from the end of the pi string and checks it again (also via codonChecker)
        Continues to do so until it fails, then returns the size of the pi string after all of those characters were removed.
        Useful for identifying slices of pi that contain all the codons and where those slices end.
        '''
        size = len(piString)
        piString = piString[frontLimit:]
        while(self.codonChecker(piString)):
            piString = piString[:-1]
            size -= 1
        #print("Failed at: size = {0}, frontLimit = {1}".format(size, frontLimit)) #only useful when developing the method/ debugging pi slicing methods
        return size
            
        
        