'''
Created on Sep 11, 2020

@author: ssmup
'''

import math #for pi_chudnovsky_bs math
from gmpy2 import mpz   #for pi_chudnovsky_bs math
import gmpy2    #for pi_chudnovsky_bs math
from Encoder import Encoder #for Encoder
import tkinter as tk    #for the gui
from functools import partial   #for putting commands in Buttons
from tkinter import StringVar   #for textboxes in the UI
from tkinter import filedialog  #for loading/saving files (if it says its unused, dont believe it)

class GUIRunner(object):
    '''
    classdocs
    '''
    if __name__ == "__main__":
        from GUIRunner import GUIRunner
        window = GUIRunner()
        
    def __init__(self, sizeRatio=1/3, circleSize = 500, circleRatio = 1/2):
        '''
        Creates a GUI with a Window that's sized based on sizeRatio, with a circle on a canvas based on circleSize and circleRatio.
        Works fine if called without any parameters.
        '''
        self.top = tk.Tk()
        ratio = sizeRatio
        moddedWidth = int(1920*ratio)
        moddedHeight = int(1080*ratio)
        self.top.title("Pi-based Data Encoder/Decoder")
        
        #generates a frame to show the data in the encoder
        self.dataFrame = tk.LabelFrame(self.top, text="Data: Type Here! or Load a File (This can scroll)")  # height=moddedHeight, width=moddedWidth
        self.dataScroll = tk.Scrollbar(self.dataFrame)
        self.dataScroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.dataFrameTArea = tk.Text(self.dataFrame,relief=tk.RAISED,width=70,yscrollcommand=self.dataScroll.set)
        self.dataToInsert = ""
        self.dataFrameTArea.pack(fill=tk.BOTH)
        self.dataScroll.config(command=self.dataFrameTArea.yview)
        self.errorLabelVar = StringVar(value="Errors will appear here")
        self.errorLabel = tk.Label(self.dataFrame,textvariable=self.errorLabelVar)
        self.errorLabel.pack()
        self.dataFrame.pack(side=tk.RIGHT)
        
        
        #supposed to center the window
        winWidth = self.top.winfo_reqwidth()
        winHeight = self.top.winfo_reqheight()
        xPos = int((self.top.winfo_screenwidth() - winWidth)/4)
        yPos = int((self.top.winfo_screenheight() - winHeight)/4)
        
        #generates a frame to hold the canvas (for the pi chart)
        self.piFrame = tk.LabelFrame(self.top, text="Pi Display")
        self.piFrame.pack(side=tk.TOP)
        
        #finds the bounding box for the Circles on the canvas, then draws the base circle and generates the ID for the arcs
        self.piDisplay = tk.Canvas(self.piFrame,bg="gray",height=moddedHeight,width=moddedWidth)
        circleSize = circleSize
        circleRatio = circleRatio
        moddedCircle = int(circleSize*circleRatio)
        canvWidth = self.piDisplay.winfo_reqwidth()
        canvHeight = self.piDisplay.winfo_reqheight()
        self.piBoundingBox = (canvWidth-moddedCircle)/2, (canvHeight-moddedCircle)/2, (canvWidth+moddedCircle)/2, (canvHeight+moddedCircle)/2
        self.piDisplay.create_oval(self.piBoundingBox, fill="black")
        self.startValue = 0
        self.endValue = 10000
        self.startDegree = 0
        self.endDegree = 0
        self.arcID = self.piDisplay.create_arc(self.piBoundingBox,start=self.startDegree, extent=self.endDegree, fill="red")
        self.piDisplay.pack()
        
        #generates a frame to hold UI widgets.
        self.UIFrame = tk.LabelFrame(self.top, bg="white", text="Play with me!")
        self.UIFrame.pack()
        
        #generates an info frame to go below the canvas, for labels and text entries
        self.infoFrame = tk.Frame(self.UIFrame)
        self.piStringLengthVar = StringVar()
        self.piStringLengthVar.set("Pi String Size Goes Here")
        self.piStringLabel = tk.Label(self.infoFrame,textvariable=self.piStringLengthVar)
        self.piStringLabel.pack()
        self.startValueLabel = tk.Label(self.infoFrame,text="Pi String Lower Bound:")
        self.startValueLabel.pack()
        self.startValueVar = StringVar()
        self.startValueTArea = tk.Entry(self.infoFrame,textvariable=self.startValueVar,exportselection=0)
        self.startValueTArea.pack()
        self.endValueLabel = tk.Label(self.infoFrame,text="Pi String Upper Bound:")
        self.endValueLabel.pack()
        self.endValueVar = StringVar()
        self.endValueTArea = tk.Entry(self.infoFrame,textvariable=self.endValueVar,exportselection=0)
        self.endValueTArea.pack()
        self.infoFrame.pack()
        
        #generates another frame to go below the canvas, this one holds buttons
        self.buttonFrame = tk.Frame(self.UIFrame)
        self.updateArcButton = tk.Button(self.buttonFrame, text="Update Arc", fg="black",command=partial(self.updateArc))
        self.resetArcButton = tk.Button(self.buttonFrame, text="Reset Arc", fg="black",command=partial(self.resetArc))
        self.loadFileButton = tk.Button(self.buttonFrame, text="Load a File", fg="black",command=partial(self.loadFromFile))
        self.saveFileButton = tk.Button(self.buttonFrame, text="Save to File", fg="black",command=partial(self.saveToFile))
        #self.button5 = tk.Button(self.buttonFrame, text="Update Data", fg="black",command=partial(self.updateDataFrame)) #kind of useless ngl
        self.clearDataButton = tk.Button(self.buttonFrame, text="Clear Data", fg="black",command=partial(self.clearDataFrame))
        self.encodeButton = tk.Button(self.buttonFrame, text="Encode Data", fg="black",command=partial(self.encode))
        self.decodeButton = tk.Button(self.buttonFrame, text="Decode Data", fg="black",command=partial(self.decode))
        self.updateArcButton.pack(side=tk.LEFT)
        self.resetArcButton.pack(side=tk.LEFT)
        #self.button5.pack(side=tk.LEFT)
        self.loadFileButton.pack(side=tk.RIGHT)
        self.saveFileButton.pack(side=tk.RIGHT)
        self.clearDataButton.pack(side=tk.LEFT)
        self.encodeButton.pack(side=tk.LEFT)
        self.decodeButton.pack(side=tk.LEFT)
        self.buttonFrame.pack()
        
        #spawns window, sets some variables to default values
        self.top.geometry("+{0}+{1}".format(xPos,yPos))
        self.resetArc()
        self.startValueVar.set("0")
        self.endValueVar.set("10000")
        self.dataToInsert = "How To Use This:\nClick Encode Data to turn any text/numbers written here into a string of numbers.\nThis string is based on the numbers you enter for the Pi String bounds. You can also just use the default values.\nOnce you have that encoded string, click Decode Data to return it to readable text. This is also based on the Pi String bound values, so make sure to encode and decode data using the same bounds both times.\n Otherwise you can enter whatever values for pi you want, and if the program has a problem with it (see below for the error bar), it will let you know.\nIf it doesn't work, try increasing the distance between the two bounds. Also, you can try encoding something multiple times (like 3 times), then decoding it that many times to return to the original input. But remember, the bounds have to be the same when you're encoding and decoding the same data. \nUse Update Arc to update the circle display (which represents a slice of pi that you've selected) without Encoding/Decoding anything. Use Reset Arc to reset the bounds and the pi display. I don't really know a reason for it, because you can just change both bounds and click Update, but you can do it.\nLoad a File reads data from a text file and loads it in the Data frame. Save to File takes the data in the frame and saves it to a text file. This is so you can save long encoded strings or something.\nThanks for looking at this!\n-Samihan"
        self.updateDataFrame()
        self.top.mainloop()
        
    #GUI functions
    def resetArc(self):
        '''
        Resets arc drawing.
        '''
        self.piDisplay.delete(self.arcID)
        self.startValueVar.set("")
        self.endValueVar.set("")
        
    def redrawPiSlice(self):
        '''
        Redraws an arc on top of the main circle on the canvas.
        Uses the class variables startDegree and endDegree.
        Deletes the old arc based on the arcID parameter.
        Sets the paramater arcID to the arc that gets drawn.
        '''
        self.piDisplay.delete(self.arcID)   #put this in a try if it throws an error if theres nothing to delete, so far it looks fine
        arc = self.piDisplay.create_arc(self.piBoundingBox,start=self.startDegree, extent=self.endDegree-self.startDegree, fill="red")
        self.arcID = arc
        
    def updateArc(self):
        '''
        Calls updateDegrees and redrawPiSlice.
        '''
        validDegrees = self.updateDegrees()
        if(validDegrees):
            self.redrawPiSlice()
        
    def updateDegrees(self):
        '''
        Calls both readStartValue and readEndValue. Sets the piStringLength to the endValue rounded up to the nearest 10000.
        Determines the degree to pi character ratio, then calculates the startDegree and endDegree values based on that.
        Returns true if no errors occur.
        '''
        success = False
        self.updateErrorLabel("")   #clearing the error frame
        validStart = self.readStartValue()
        validEnd = self.readEndValue()
        if(validStart and validEnd):
            self.piStringLength = self.endValue + (10000 - self.endValue%10000)
            self.piStringLengthVar.set("Max Pi Length: " + str(self.piStringLength))
            self.degreeToCharRatio = self.piStringLength/360
            self.startDegree = self.startValue/self.degreeToCharRatio
            self.endDegree = self.endValue/self.degreeToCharRatio
            success = True
        return success
    
    def readStartValue(self):
        '''
        Reads the value in the startValueTArea
        If there's nothing to read, show the error in the error label.
        Returns true if no error occurs.
        '''
        success = False
        try:
            rawValue = int(self.startValueVar.get())
            self.startValue = rawValue
            success = True
        except:
            self.updateErrorLabel("Pi String Bound Error")
        return success
        
    def readEndValue(self):
        '''
        Reads the value in the endValueTArea
        If there's nothing to read, show the error in the error label.
        Returns true if no error occurs.
        '''
        success = False
        try:
            rawValue = int(self.endValueVar.get())
            self.endValue = rawValue
            success = True
        except:
            self.updateErrorLabel("Pi String Bound Error")
        return success
    
    def loadFromFile(self):
        '''
        Opens a browse for file window, then reads it for data. Stores to dataToInsert, then calls updateDataFrame
        If the file type isn't readable, show the error in the error label.
        Returns true if no error occurs.
        '''
        success = False
        file = tk.filedialog.askopenfile(initialdir="/",mode="r",filetypes= (("Text File","*.txt"),("All Files","*.*")))
        if file is None:    #exit if dialog is cancelled
            return success
        fileData = ""
        try:
            for line in file:
                fileData += str(line)
            self.dataToInsert = fileData
            self.updateDataFrame()
            success = True
        except:
            self.updateErrorLabel("The selected file wasn't readable")
        return success
        
    def saveToFile(self):
        '''
        Opens a save as window, then saves the data currently in the dataFrameTArea.
        Returns true if no error occurs.
        '''
        success = False
        file = tk.filedialog.asksaveasfile(initialdir="/",defaultextension=".txt",filetypes= (("Text File","*.txt"),("All Files","*.*")))
        if file == "" or file is None:    #exit if dialog is cancelled
            return success
        file.write(self.dataFrameTArea.get(1.0, tk.END))
        success = True
        return success
        
    def clearDataFrame(self):
        '''
        Clears the text in the data frame.
        '''
        self.dataFrameTArea.delete(1.0, tk.END)
        
    def insertIntoDataFrame(self):
        '''
        Inserts the string in dataToInsert into the data frame.
        '''
        self.dataFrameTArea.insert(1.0, self.dataToInsert)
        
    def updateDataFrame(self):
        '''
        Calls clearDataFrame then insertIntoDataFrame
        '''
        self.clearDataFrame()
        self.insertIntoDataFrame()
        
    def updateErrorLabel(self, errorString=""):
        '''
        Replaces the errorLabel with what's in errorLabel Value.
        '''
        self.errorLabelVar.set(errorString)
        
    def encode(self):
        '''
        Refreshes the entered degree values and the arc.
        Then generates a length of pi based on the entered pi limits.
        It tries to encode the entered data. If it fails, it cancels the whole thing and prints an error message to the error label.
        Otherwise it prints the encoded data in the data frame.
        '''
        validDegrees = self.updateDegrees()
        self.updateArc()
        if(validDegrees):
            heldData = self.dataFrameTArea.get(1.0,tk.END)
            heldData = heldData[:-1]    #removing the newline character at the end of the dataframe
            try:
                sliceBounds = [self.startValue,self.endValue]
                encodedData = self.encodeByBounds(heldData,sliceBounds)
                encodedDataString = ""
                for index in encodedData:
                    if(index == -1):    #this triggers if any codon is not found in the pi string. it terminates the encode process.
                        raise
                    encodedDataString += str(index)
                    encodedDataString += "."
                encodedDataString = encodedDataString[:-1]
                self.dataToInsert = encodedDataString
                self.updateDataFrame()
            except:
                self.updateErrorLabel("ENCODE FAILED - Increase the bounds or load different data.")
    
    def decode(self):
        '''
        Refreshes the entered degree values and the arc.
        Then generates a length of pi based on the entered pi limits.
        It tries to decode the entered data. If it fails, it cancels the whole thing and prints an error message to the error label.
        Otherwise it prints the decoded data in the data frame.
        '''
        validDegrees = self.updateDegrees()
        self.updateArc()
        if(validDegrees):
            heldData = self.dataFrameTArea.get(1.0,tk.END)
            heldData = heldData[:-1]    #removing the newline character at the end of the dataframe
            heldData = str(heldData)
            indexList = heldData.split('.')
            try:
                sliceBounds = [self.startValue,self.endValue]
                decodedData = self.decodeByBounds(indexList, sliceBounds)
                self.dataToInsert = decodedData
                self.updateDataFrame()
            except:
                self.updateErrorLabel("DECODE FAILED - Increase the bounds or load different data")
            
    #basic runner/encoder functions
    def pi_chudnovsky_bs(self,digits):
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
    
    def getPi(self,length = 8555, startLength = 0):
        '''
        A way for me to call pi_chudnovsky_bs that allows me to easily call it and request for substrings beyond a certain initial length.
        Useful for slicing pi based on breakpoints determined by piSlicer.
        getPi(breakpoint2, breakpoint1) where breakpoint2 > breakpoint 1 and they're both exact values determined from piSlicer
        Defaults to 8555 because that's the first breakpoint with codon length = 3 with codons going from 0 - 999.
        Actually returns a length of 2 more than the length parameter. Intentionally.
        '''
        pi = self.pi_chudnovsky_bs(length+1) #this is length+1 because breakpoint 13 fails without it. I have a hypothesis about this where the breakpoint works 99% of the time because of RNG but it's not really supposed to without the +1
        piString = str(pi)
        piString = piString[startLength:]
        return piString
    
    def encodeByBounds(self,inputToEncode,sliceBounds=[0, 3853]):
        '''
        Takes an input (int or string, whatever) and encodes it based on the given sliceBounds.
        Defaults to the first slice for codons of length 3 ranging from 0 to 128.
        Assumes the slice contains all codons required to encode the input.
        Returns an array of codons that represent the indices of pi where the input data is found in the piSlice.
        ''' 
        piString = self.getPi(sliceBounds[1], sliceBounds[0])
        encoder = Encoder()
        stringToEncode = str(inputToEncode)
        asciiString = encoder.stringToAscii(stringToEncode)
        asciiSlices = encoder.numStringSlicer(asciiString)
        codonSubbedSlices = encoder.codonSubstituter(asciiSlices, piString)
        return codonSubbedSlices
    
    def decodeByBounds(self,inputToDecode,sliceBounds=[0, 3853]):
        '''
        Takes an input (array of codons) and decodes it based on the given sliceBounds.
        Defaults to the first slice for codons of length 3 ranging from 0 to 128.
        Assumes the slice contains all codons required to decode the input.
        Returns a string of concatenated characters based on the ascii code that the codons represented..
        '''
        piString = self.getPi(sliceBounds[1], sliceBounds[0])
        encoder = Encoder()
        asciiSubbedSlices = encoder.codonTranslator(inputToDecode, piString)
        reconstitutedString = encoder.asciiToString(asciiSubbedSlices)
        return reconstitutedString      
            