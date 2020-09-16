'''
Created on Sep 11, 2020

@author: ssmup
'''

import math
from gmpy2 import mpz
import gmpy2
from time import time
from Encoder import Encoder

def pi_chudnovsky_bs(digits):
    """
    Compute int(pi * 10**digits)

    This is done using Chudnovsky's series with binary splitting
    
    taken from https://www.craig-wood.com/nick/pub/pymath/pi_chudnovsky_bs_gmpy.py
    requires installation of https://pypi.python.org/pypi/gmpy2
    """
    C = 640320
    C3_OVER_24 = C**3 // 24
    def bs(a, b):
        """
        Computes the terms for binary splitting the Chudnovsky infinite series

        a(a) = +/- (13591409 + 545140134*a)
        p(a) = (6*a-5)*(2*a-1)*(6*a-1)
        b(a) = 1
        q(a) = a*a*a*C3_OVER_24

        returns P(a,b), Q(a,b) and T(a,b)
        """
        if b - a == 1:
            # Directly compute P(a,a+1), Q(a,a+1) and T(a,a+1)
            if a == 0:
                Pab = Qab = mpz(1)
            else:
                Pab = mpz((6*a-5)*(2*a-1)*(6*a-1))
                Qab = mpz(a*a*a*C3_OVER_24)
            Tab = Pab * (13591409 + 545140134*a) # a(a) * p(a)
            if a & 1:
                Tab = -Tab
        else:
            # Recursively compute P(a,b), Q(a,b) and T(a,b)
            # m is the midpoint of a and b
            m = (a + b) // 2
            # Recursively calculate P(a,m), Q(a,m) and T(a,m)
            Pam, Qam, Tam = bs(a, m)
            # Recursively calculate P(m,b), Q(m,b) and T(m,b)
            Pmb, Qmb, Tmb = bs(m, b)
            # Now combine
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
        return Pab, Qab, Tab
    # how many terms to compute
    DIGITS_PER_TERM = math.log10(C3_OVER_24/6/2/6)
    N = int(digits/DIGITS_PER_TERM + 1)
    # Calclate P(0,N) and Q(0,N)
    P, Q, T = bs(0, N)
    one_squared = mpz(10)**(2*digits)
    sqrtC = gmpy2.isqrt((10005*one_squared))
    return (Q*426880*sqrtC) // T

# The last 5 digits or pi for various numbers of digits
check_digits = {
        100 : 70679,
       1000 :  1989,
      10000 : 75678,
     100000 : 24646,
    1000000 : 58151,
   10000000 : 55897,
}

"""
OBSOLETE CODE
PLEASE IGNORE :)   
def piSlicer(sliceCount = 10, sliceSize = 14000, codonLength = 3, maxInt = 1000):
    '''
    prints values of Pi at which any less digits would not contain every single possible codon. (codon = 000, 001, .. 999)
    Then removes that section of the piString and searches again, from the index of the initial breakpoint + sliceSize (a value slightly larger than the index of the first breakpoint, so I'm assuming that all codons can fit in a 13000 digit space).
    So because 8555 is the first breakpoint, having 8554 digits would not contain every codon, but 8555 digits would contain every codon.
    That means pi_chudnovsky_bs(8555) would have every codon within the string, but pi_chudnovsky_bs(8554) would not.
    So basically it returns acceptable lengths for inputs into pi_chudnovsky_bs.
    ***ACtually not true. This fails around breakpoint 13 but it passes if I use the breakpoint+1.
    Can change default codon length from 3 to something else.
    Useful for determining slices of Pi which the encoder can pick to use as a cipher.
    Also prints the length of time taken to find the breakpoint.
    '''
    if(sliceCount < 0):
        sliceCount = 10
        print("Can't have negative sliceCount, defaulting to 10")
    print("Slicing pi {0} times, with an initial slice size of {1}".format(sliceCount, sliceSize))
    
    encoder = Encoder()
    pi = pi_chudnovsky_bs(sliceSize) #a low number greater than the first break point (which is 8555 for codonLength = 3)
    piString = str(pi)
    cap = encoder.expansiveCodonChecker(piString, 0, codonLength, maxInt) #this becomes 8555
    print("Breakpoint 0 found: {0}".format(cap))
    failurePoints = [0,cap]
    start = time()
    lastMoment = 0
    for i in range(0, sliceCount-1):
        digits = cap+sliceSize
        pi = pi_chudnovsky_bs(digits)
        piString = str(pi)
        cap = encoder.expansiveCodonChecker(piString, cap, codonLength)
        failurePoints.append(cap)
        timeTaken = time()-start
        print("Breakpoint {0} found: {1}    Time: {2}    TDelta: {3}".format(i+1, cap, '{:5.5}'.format(timeTaken), '{:5.5}'.format(timeTaken-lastMoment)))
        lastMoment = time()-start
    print("Done slicing!")
    return failurePoints
    
def getPiSlice(sliceNumber):
    '''
    Takes in a slice number and returns a size-2 array of the cap and floor indices of the slice.
    Slice number has to be greater than or equal to 0.
    '''
    if(sliceNumber < 0):
        sliceNumber = 0
        print("sliceNumber defaulted to 0")
    allIndices = piSlicer(sliceCount = sliceNumber+1)
    sliceIndices = []
    sliceIndices.append(allIndices[sliceNumber+1])
    sliceIndices.append(allIndices[sliceNumber])
    return sliceIndices
    
def sliceChecker(sliceCount = 10, sliceSize = 14000):
    '''
    Runs piSlicer to get some slices then double checks the validity of each slice.
    Because I'm insecure.
    '''
    breakpoints = piSlicer(sliceCount, sliceSize)
    encoder = Encoder()
    floor = 0
    for i in range(0,len(breakpoints)):
        test = encoder.codonChecker(getPi(breakpoints[i],floor))
        if(test):
            print("PASS! Check passed between breakpoints {0} ({1}) and {2} ({3})".format(i, breakpoints[i], i-1, floor))
        else:
            print("FAIL! Check failed between breakpoints {0} ({1}) and {2} ({3})".format(i, breakpoints[i], i-1, floor))
        floor = breakpoints[i]
        
def sliceAverager(sliceCount = 10):
    '''
    Calculates a number of slices then checks the average number of digits in each breakpoint.
    Useful for statistical purposes?
    '''
    fridge = piSlicer(sliceCount)
    total = 0
    floor = 0
    for piSlice in fridge:
        cap = int(piSlice)
        total += cap - floor
        floor = cap
    print("Average pi slice size: {0}".format(total/len(fridge)))
    
def encoderCheck(printStrings=False):
    '''
    Uses a bunch of functions from Encoder and an RNG generator to fully test translation of an int value into and out of pi codons.
    Doesn't always work. See comment at end of function. 80-90% success rate.
    '''
    from random import randint
    encoder = Encoder()
    randstring = str(randint(10000000,100000000000000))
    strings = encoder.numStringSlicer(randstring)
    formattedstrings = encoder.numStringSliceFormatter(strings)
    codonSubbed = encoder.codonSubstituter(formattedstrings, getPi())
    resubbed = encoder.codonTranslator(codonSubbed, getPi())
    reconstituted = encoder.numStringGluer(resubbed)
    if(printStrings):
        print(randstring)
        print(reconstituted)
    success = False
    if(randstring == reconstituted):
        if(printStrings):
            print("YAY! THIS MEANS TRANSLATION INTO AND OUT OF PI IS SUCCESSFUL!\n")
        success = True
    return success
    '''
    this is broken becomes sometimes it trims zeros that shouldnt be trimmed.
    can fix this by only trimming zeros on the last element in reconstituted.
    I fixed this ^ but now,
    this also is broken in that if the last term is "0" or "00" or something like that it just gets erased.
    a potential fix is adding zeros to the end of the initial numstring once it's detected to not be evenly divisible by 3.
    this ^ is not a potential fix because that will just shift the zero problem; how will it be clear that 0s should be trimmed off the end when retranslating it into the numString?
    
    potentially, i don't need to fix anything. because ascii goes from 0 - 127. if ascii 000 = ascii 0, then i can add zeros to the front of the extra codon and not worry about trimming
    '''

def encoderCheck2(stringLength = 100, printStrings = False, inputString = ""):
    '''
    Uses a bunch of functions from Encoder and an RNG generator to fully test translation of a character string into and out of pi codons.
    This works by taking the character string, turning it into an int string of ascii values, then doing the same process as encoderCheck for number string encoding.
    Always works. 100% of the time.
    '''
    import string
    import random
    encoder = Encoder()
    letters = string.ascii_letters
    if(inputString != ""):
        randstring= ''.join(random.choice(letters) for i in range(stringLength))
    else:
        randstring = inputString
    asciiString = encoder.stringToAscii(randstring)
    strings = encoder.numStringSlicer(asciiString)
    codonSubbed = encoder.codonSubstituter(strings, getPi())
    resubbed = encoder.codonTranslator(codonSubbed, getPi())
    reconstituted = encoder.asciiToString(resubbed)
    if(printStrings):
        print(randstring)
        print(reconstituted)
    success = False
    if(randstring == reconstituted):
        if(printStrings):
            print("YAY! THIS MEANS TRANSLATION INTO AND OUT OF PI IS SUCCESSFUL!\n")
        success = True
    return success
    
def measureEncoderSuccess(encoderType, measureCount = 10000, printStrings = False):
    '''
    Runs either encoderCheck or encoderCheck2 measureCount times and returns the percentage of successful encoding/decoding.
    encoderType = 1 --> encoderCheckV2, encoderType = 0 --> faulty encoderCheck
    '''
    successCount = 0
    print('Running encoderCheck {0} times..'.format(measureCount))
    if(encoderType == 1):
        print('Using string encoderCheck')
    else:
        encoderType = 0
        print('Using number encoderCheck')
    for i in range(measureCount):
        if(encoderType == 0):
            if(encoderCheck(printStrings)):
                successCount += 1
        else:
            if(encoderCheck2(printStrings)):
                successCount += 1
        if(i % 500 == 0):
            print('Ran {0} times..'.format(i))
    print('Calculating...')
    
    print('Success Percentage: {0}%'.format(successCount*100/measureCount))
    
def encode(inputToEncode,piSlice=1):
    '''
    Takes an input (int or string, whatever) and encodes it based on the given piSlice.
    Defaults to the first slice.
    Returns an array of codons that represent the indices of pi where the input data is found in the piSlice.
    ''' 
    sliceBounds = getPiSlice(piSlice)
    piString = getPi(sliceBounds[0], sliceBounds[1])
    encoder = Encoder()
    stringToEncode = str(inputToEncode)
    asciiString = encoder.stringToAscii(stringToEncode)
    asciiSlices = encoder.numStringSlicer(asciiString)
    codonSubbedSlices = encoder.codonSubstituter(asciiSlices, piString)
    return codonSubbedSlices

def decode(inputToDecode,piSlice=1):
    '''
    Takes an input (array of codons) and decodes it based on the given piSlice.
    Defaults to the first slice.
    Returns a string of concatenated characters based on the ascii code that the codons represented..
    '''
    sliceBounds = getPiSlice(piSlice)
    piString = getPi(sliceBounds[0], sliceBounds[1])
    encoder = Encoder()
    asciiSubbedSlices = encoder.codonTranslator(inputToDecode, piString)
    reconstitutedString = encoder.asciiToString(asciiSubbedSlices)
    return reconstitutedString
"""
def getPi(length = 8555, startLength = 0):
    '''
    A way for me to call pi_chudnovsky_bs that allows me to easily call it and request for substrings beyond a certain initial length.
    Useful for slicing pi based on breakpoints determined by piSlicer.
    getPi(breakpoint2, breakpoint1) where breakpoint2 > breakpoint 1 and they're both exact values determined from piSlicer
    Defaults to 8555 because that's the first breakpoint with codon length = 3 with codons going from 0 - 999.
    Actually returns a length of 2 more than the length parameter. Intentionally.
    '''
    pi = pi_chudnovsky_bs(length+1) #this is length+1 because breakpoint 13 fails without it. I have a hypothesis about this where the breakpoint works 99% of the time because of RNG but it's not really supposed to without the +1
    piString = str(pi)
    piString = piString[startLength:]
    return piString

def encodeByBounds(inputToEncode,sliceBounds=[0, 3853]):
    '''
    Takes an input (int or string, whatever) and encodes it based on the given sliceBounds.
    Defaults to the first slice for codons of length 3 ranging from 0 to 128.
    Assumes the slice contains all codons required to encode the input.
    Returns an array of codons that represent the indices of pi where the input data is found in the piSlice.
    ''' 
    piString = getPi(sliceBounds[1], sliceBounds[0])
    encoder = Encoder()
    stringToEncode = str(inputToEncode)
    asciiString = encoder.stringToAscii(stringToEncode)
    asciiSlices = encoder.numStringSlicer(asciiString)
    codonSubbedSlices = encoder.codonSubstituter(asciiSlices, piString)
    return codonSubbedSlices

def decodeByBounds(inputToDecode,sliceBounds=[0, 3853]):
    '''
    Takes an input (array of codons) and decodes it based on the given sliceBounds.
    Defaults to the first slice for codons of length 3 ranging from 0 to 128.
    Assumes the slice contains all codons required to decode the input.
    Returns a string of concatenated characters based on the ascii code that the codons represented..
    '''
    piString = getPi(sliceBounds[1], sliceBounds[0])
    encoder = Encoder()
    asciiSubbedSlices = encoder.codonTranslator(inputToDecode, piString)
    reconstitutedString = encoder.asciiToString(asciiSubbedSlices)
    return reconstitutedString
    
if __name__ == "__main__":
    string = "The color of animals is by no means a matter of chance; it depends on many considerations, but in the majority of cases tends to protect the animal from danger by rendering it less conspicuous. Perhaps it may be said that if coloring is mainly protective, there ought to be but few brightly colored animals. There are, however, not a few cases in which vivid colors are themselves protective. The kingfisher itself, though so brightly colored, is by no means easy to see. The blue harmonizes with the water, and the bird as it darts along the stream looks almost like a flash of sunlight."
    string2 = "He killed 100239 people."
    string = '"Are you insane?", he said.'
    #print(encoderCheck2(inputString = string))
    #print(encoderCheck2(inputString = string2))
    
    #piSlicer(sliceCount=5,maxInt=128)
    piString = getPi(10000)
    encoder = Encoder()
    slices = encoder.piSliceDefiner(piString)
    for indices in slices:
        print(indices)
    #sliceBounds = slices[3]
    
    '''
    encoded = encodeByBounds(string)
    print(string)
    decoded = decodeByBounds(encoded)
    print(decoded)
    
    print("test 2")
    
    encoded = encodeByBounds(string,sliceBounds)
    print(string)
    decoded = decodeByBounds(encoded,sliceBounds)
    print(decoded)
    '''
    
    '''
    maybe add an array of pre-generated pi values to use... waiting 20 seconds every time you encode something is a pain in the ass
    BUT EITHER WAY
    THE ENCODING IS WORKING PERFECTLY!
    IT"S AMAZING!
    to-do:
    add a function that works by generating increasing lengths of pi (digit by digit) and notes the length it takes to have all codons.
    kind of like expansiveCodonChecker but instead of slowly trimming pi it slowly builds on pi.
    this way it can just keep generating more and more and more and get precise data about breakpoints instead of failing sometimes because the gap is larger than 14k or whatever i set it to through piSlicer
    
    once this ^ function is made i can clear up some old functions
    '''
    #measureEncoderSuccess(100000000)
    #encoderCheck2(printStrings = True)
    #measureEncoderSuccess(1)
    #sliceChecker(500, 12000)
    #this fails at breakpoints 145, 372, 432, 449.
    #piSlicer(sliceCount=10,codonLength=3)
    #sliceChecker(10)
    
    #print(encoder.codonChecker(getPi(106872,100771)))
    #print(encoder.codonChecker(getPi(24775,16170)))
    '''
    TODO LIST:
    Maybe calculate the average size of each slice of pi? That could be interesting. done
    *****KEY: (not really important. i can develop the rest of the functionality for just the first slice of pi)
        Create a function to automatically re-check breakpoints as it finds them - 
        so it dynamically notices that after adding 10000 (or whatever) the breakpoint failed, and then have it re-add 10000 (or whatever)
            and have it wait until proper failure
            (where proper failure means expansiveCodonChecker goes through more than just 1 character down from the piString).
    Add the translation feature. So far this is just a PI Scanner
    Maybe figure out how to make the codonChecker a binary search or a tree search instead of a sequential search.
    Doesn't really make sense because the numbers need to be in order, but if there's a better way I should take it.
    '''
    
            
            