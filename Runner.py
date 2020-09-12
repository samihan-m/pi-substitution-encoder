'''
Created on Sep 11, 2020

@author: ssmup
'''

#taken from https://www.craig-wood.com/nick/pub/pymath/pi_chudnovsky_bs_gmpy.py
#requires installation of https://pypi.python.org/pypi/gmpy2
import math
from gmpy2 import mpz
import gmpy2
from time import time
from Encoder import Encoder

fridge = []

def pi_chudnovsky_bs(digits):
    """
    Compute int(pi * 10**digits)

    This is done using Chudnovsky's series with binary splitting
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
   
def piSlicer(sliceCount = 10):
    '''
    prints values of Pi at which any less digits would not contain every single possible codon. (codon = 000, 001, .. 999)
    Then removes that section of the piString and searches again, from the index of the initial breakpoint + 9000 (slightly larger than the index of the first breakpoint, so I'm assuming that all codons can fit in a 9000 digit space)t.
    So because 8555 is the first breakpoint, having 8554 digits would not contain every codon, but 8555 digits would contain every codon.
    That means pi_chudnovsky_bs(8555) would have every codon within the string, but pi_chudnovsky_bs(8554) would not.
    So basically it returns acceptable lengths for inputs into pi_chudnovsky_bs.
    Useful for determining slices of Pi which the encoder can pick to use as a cipher.
    Not really designed for efficiency so it takes increasingly longer intervals of time to find breakpoints.
    Gets painfully long at around sliceCount >= 12.
    '''
    if(sliceCount <= 0):
        sliceCount = 10
        print("Can't have non-positive sliceCount, defaulting to 10")
    print("Slicing pi {0} times...".format(sliceCount))
    
    encoder = Encoder()
    pi = pi_chudnovsky_bs(10000) #a low number greater than the first break point (which is 8555)
    piString = str(pi)
    cap = encoder.expansiveCodonChecker(piString) #this becomes 8555
    print("Breakpoint 0 found: {0}".format(cap))
    failurePoints = [cap]
    for i in range(0, sliceCount-1):
        digits = cap+9000
        pi = pi_chudnovsky_bs(digits)
        piString = str(pi)
        cap = encoder.expansiveCodonChecker(piString,cap)
        failurePoints.append(cap)
        print("Breakpoint {0} found: {1}".format(i+1, cap))
    print("Done slicing!")
    return failurePoints

def getPi(length, startLength = 0):
    '''
    A way for me to call pi_chudnovsky_bs that allows me to easily call it and request for substrings beyond a certain initial length.
    Useful for slicing pi based on breakpoints determined by piSlicer.
    getPi(breakpoint2, breakpoint1) where breakpoint2 > breakpoint 1 and they're both exact values determined from piSlicer
    '''
    pi = pi_chudnovsky_bs(length)
    piString = str(pi)
    piString = piString[startLength:]
    return piString

def storeSlices(sliceCount = 10):
    '''
    saves the array holding sliceCount slices to a static variable for future reference by getSliceRange.
    Defaults to 10, just like piSlicer does. Anything above 10 takes quite a while.
    This might be useless because I don't know how to make the method variable fridge save to the "class" variable fridge.
    '''
    fridge = piSlicer(sliceCount)
    
def sliceChecker(sliceCount = 10):
    '''
    Runs piSlicer to get some slices then double checks the validity of each slice.
    Because I'm insecure.
    '''
    breakpoints = piSlicer(sliceCount)
    encoder = Encoder()
    floor = 0
    for i in range(0,len(breakpoints)):
        test = encoder.codonChecker(getPi(breakpoints[i],floor))
        if(test):
            print("PASS! Check passed between breakpoints {0} ({1}) and {2} ({3})".format(i, breakpoints[i], i-1, floor))
        else:
            print("FAIL! Check failed between breakpoints {0} ({1}) and {2} ({3})".format(i, breakpoints[i], i-1, floor))
        floor = breakpoints[i]
        
if __name__ == "__main__":
    sliceChecker(100)
    '''
    TODO LIST:
    Maybe calculate the average size of each slice of pi? That could be interesting.
    Add the translation feature. So far this is just a PI Scanner
    Maybe figure out how to make the codonChecker a binary search or a tree search instead of a sequential search.
    Doesn't really make sense because the numbers need to be in order, but if there's a better way I should take it.
    '''
    
            
            