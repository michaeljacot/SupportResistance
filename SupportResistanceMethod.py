# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:31:17 2020

@author: Michael
"""



import numpy as np
import yfinance as yf 
import matplotlib.pyplot as plt
from lineCalc import getLine,plotLine, compareToLine,getPointOnLine,lineOffset,checkLine,getBModifier
from DerivativeAnalysis import turningPoints

def getData(stock,domain):
    
    tick = yf.Ticker(stock)
    hist = tick.history(period="max", rounding=True)
    hist = hist[-domain:]
    h = hist.Close.tolist()
    
    return h
    


def findNextPoint(checkPoint,Vals):
    
    #loop through every value in the list of points
    for v in Vals:
        try:
            if v[1] > checkPoint:
                
                return v
        except:
            return -1
    
    




#gets first derivative
def derivative(h):
    dx = np.gradient(h)
    return dx


def getPoints(dx,h,output):
     
    #list that holds the index of the turning point in the data
    supportP = []
    resistanceP = []
    
    """
        Checking for zeros:
            We need to figure out wether or not this point is a 
            maximum or minimum after this, so use either the value of the second derivative (which might get messy with noise)
            or check to see what type of sign change occurs at the turning point (- to + implies minimum)/ (+ to - implies maximum)
    """
    
    
    #bounds adjusted to prevent index out of bounds error
    for i in range(1,len(dx)-1):
        
        if dx[i-1]<0 and dx[i+1]>0:
            supportP.append(i)
        elif dx[i-1]>0 and dx[i+1]<0:
            resistanceP.append(i)
        
    
    if output:
        
        plt.plot(h)
        #plots the support points
        for s in supportP:
            plt.plot(s,h[s],marker = 'o',markersize = 5 , color = 'red')
            
        #plots the resistance points
        for r in resistanceP:
            plt.plot(r,h[r],marker = 'o',markersize = 5 , color = 'blue')
        plt.title("Detected Turning Points")
        plt.show()
    
    #puts the values of the index and closing price in a list to be sorted
    supportVals = []
    for p in supportP:
        supportVals.append((h[p],p))
    
    
    #same thing but for resistance 
    resistanceVals = []
    for r in resistanceP:
        resistanceVals.append((h[r],r))
    
    return supportVals,resistanceVals


def supportLines(supportVals,h,dx,automatic,intervals,output):

    #####SUPPORT######
    lineIndex = 0
    
    supDict = dict(supportVals)
    supDict = dict((v,k) for k,v in supDict.items()) #reverses items in tuple
    
    
    
    
    newLineVals = intervals
    
    
    
            
   
    
    
    if output:
        print()
        print("The has new line points at ", newLineVals)
        print()
        print()
        print("*****Calculating Support Lines*****")
        print()
        print("***Generating Support Line #1***")
        
        
        
        
        
    supportLines = []
    averageLines = []
    
    #creates x set for the finding the average line
    x = np.arange(0,newLineVals[lineIndex],1)
    #creates the average line and uses numpys sick return format to get the m and b for y=mx+b
    mAvg,bAvg = np.polyfit(x,h[0:newLineVals[lineIndex]],1)
    #adds this first average line to the list of average lines to be returned
    averageLines.append((mAvg,bAvg))
    
    
    
    #gets the first modifier value for the first set of lines
    MODIFIER = getBModifier(h, bAvg, mAvg, bAvg, supDict, 0, newLineVals[lineIndex], "s",output)
    
    #(y,x)
    #uses the first point for each new line as the y intercept of the average line MODIFIED by the modifier factor 
    #see bModifier method in lineCalc
    thisSP1 = (bAvg-MODIFIER,0) 

    #uses the second point for the first line as the first of the support values
    thisSP2 = supportVals[0]
    if output : print("First support line is drawn between points " , thisSP1,thisSP2)
        
    #list to hold support lines
    
    
    #calls the getLine method on the first two points
    thisSupportLine = getLine(thisSP1,thisSP2)

    
    #loops through the index of all the closing prices (smoothed)
    for i in range(1,len(h)):
        
        lowest = 1
        
        thisSupportLine = getLine(thisSP1,thisSP2) #recalculate the line
        
        #check to see if this closing price is in the support dictionary
        if i in supDict:
            
            #if we have just updated the line, both points will be the same, so update the second point to be the next found support point
            
            p = (i,supDict[i])
            
            thisDiff = 0
            thisDiff = compareToLine(thisSupportLine[0], thisSupportLine[1], p)
        
            #print("The difference is " , diff)
            
            #check to see if we are below the support line, and update this line
            if thisDiff < 0:
                
                if thisDiff < lowest:
                    
                    thisSP2 = (supDict[i],i) #update the second point
                
                
                    lowest = thisDiff
                    #print("Updated p2 from " , thisSP2 , " to ", p)
                
    
                
                
        #checks to see if the closing price has moved far enough away from the moving average (determened by the tollerance measure) and appends the final support line to the list of accepted support lines to start a new line
        
        
        #if we are at the end of the list, just add the current line to the list of lines and break out of the loop, no need for more calculation
        if i == len(h)-1:
            
            supportLines.append(thisSupportLine)
            
            if output : print("Final Support Line Created using point ", thisSP1,  thisSP2)

            break
        
        
        
        if i in newLineVals :
            
            
            
            
            lineIndex +=1
            
            
            supportLines.append(thisSupportLine)
            
            if output : 
                print("New Support Added Created using point ", thisSP1,  thisSP2)
                print()
            
            if output : print("***Generating Line #", lineIndex+1,"***")
            
            
            #the first point when a new line is created in a data set should be a point far away on the average fit line (i choose the y intercept of the average line)
            x = np.arange(i,newLineVals[lineIndex],1)
            mAvg,bAvg = np.polyfit(x,h[i:newLineVals[lineIndex]],1)
            averageLines.append((mAvg,bAvg))
            
            
            
           
            
            MODIFIER = getBModifier(h, bAvg, mAvg, bAvg, supDict, newLineVals[lineIndex-1], newLineVals[lineIndex], "s",output)
            
            if output : print("The y intercept for the next average line is " , bAvg)
            
            thisSP1 = (bAvg-MODIFIER,0) 
            
            
            
            
            #gets the next point in line after the new line is created
            checkPoint = i
            nextPoint = findNextPoint(checkPoint,supportVals)
            thisSP2 = nextPoint
            
            if thisSP2 == None:
                break
            
            if output:
                print("Next two points are " , thisSP1,thisSP2)
                print()
            thisSupportLine = getLine(thisSP1,thisSP2)
            i+=1
            
    return supportLines,averageLines
        
            
        
    
########RESISTANCE#########
    
def resistanceLines(resistanceVals,h,dx,automatic,intervals,output):
    
    
    #get the initial support and resistance line by using the first two min/max

    lineIndex = 0
    
    
    
    
    
    resDict = dict(resistanceVals)
    resDict = dict((v,k) for k,v in resDict.items())
    
    newLineVals = intervals
    
    if output:
        print()
        print("*****Calculating Resistance Lines*****")
        print()
        print("***Generating Resistance Line #1***")
    
    
    
    x = np.arange(0,newLineVals[0],1)
    mAvg,bAvg = np.polyfit(x,h[0:newLineVals[0]],1)
    
    
    #(y,x)
    
    MODIFIER = getBModifier(h, bAvg, mAvg, bAvg, resDict, 0, newLineVals[lineIndex], "r",output)
    
    #MODIFIER = 3
    
    
    thisRP1 = (bAvg+MODIFIER,0) 
    
    
    
    
    

    #variables to hold the points that are used to calculate the CURRENT lines

    

    


    thisRP2 = resistanceVals[0]
    if output: print("First resistance line " , thisRP1,thisRP2)
        
    thisResistanceLine = getLine(thisRP1,thisRP2)
    
    resistanceLines = []    
    
    #loops through the index of all the closing prices (smoothed)
    for i in range(1,len(h)):
        
        highest = 0
              
    
        thisResistanceLine = getLine(thisRP1,thisRP2) #recalculate the line
        
        #check to see if this closing price is in the support dictionary
        if i in resDict:
            
            #if we have just updated the line, both points will be the same, so update the second point to be the next found support point
            
            p = (i,resDict[i])
            
            thisDiff = compareToLine(thisResistanceLine[0], thisResistanceLine[1], p)
        
            
            
            #check to see if we above the resistance line and update this line
            if thisDiff > 0:
                
                if thisDiff > highest:
                    
                    
                
                
                    highest = thisDiff
                    #print("Updated p2 from " , thisRP2 , " to ", p)
                
                    thisRP2 = (resDict[i],i) #update the second point
                
                
        #checks to see if the closing price has moved far enough away from the moving average (determened by the tollerance measure) and appends the final support line to the list of accepted support lines to start a new line
        
        
        
        if i == len(h)-1:
            resistanceLines.append(thisResistanceLine)
        
            if output: print("Final Resistance Line Created using point ", thisRP1,  thisRP2)
            break
    
        
        
        if i in newLineVals:
            
            
            
            
            lineIndex +=1
            
            
            resistanceLines.append(thisResistanceLine)
            
            
            
            if output : 
                print("New Resistance Added Created using point ", thisRP1,  thisRP2)
                print()
            
            if output : print("***Generating Line #", lineIndex+1,"***")
            
            
            #update the first and second point to the next ones in the dictionary
            
            #the first point when a new line is created in a data set should be a point far away on the average fit line (i choose the y intercept of the average line)
            x = np.arange(i,newLineVals[lineIndex],1)
            mAvg,bAvg = np.polyfit(x,h[i:newLineVals[lineIndex]],1)
            
            
            MODIFIER = getBModifier(h, bAvg, mAvg, bAvg, resDict, newLineVals[lineIndex-1], newLineVals[lineIndex], "r",output)

            if output: print("The y intercept for the next average line is " , bAvg)
            
            thisRP1 = (bAvg+ MODIFIER,0) 
        
            
            #gets the next point in line after the new line is created
            checkPoint = i
            nextPoint = findNextPoint(checkPoint,resistanceVals)
            thisRP2 = nextPoint
            
            if thisRP2 == None:
                break
            
            if output:
                print("Next points returned are " , thisRP1,thisRP2)
                print()
            thisResistanceLine = getLine(thisRP1,thisRP2)
            i+=1
            
              
    return resistanceLines


#wrapper method for lines
def getLines(h,automatic,intervals,output):
    
    
    #get first derivative
    dx = derivative(h)
    
    #get the min/max
    points = getPoints(dx,h,output)
    supportVals , resistanceVals = points[0], points[1]
    
    
    
    if automatic == True:
        
        if output:
            print("*****Starting Line generation*****")
            print("Automatic Line Generation")
            print("Finding line intervals...")
            
            points = turningPoints(dx,output)
            points  = np.sort(points)
            
            #have the supportLines return the automatic intervals so that you dont have to call it in resistanceLines again
            sLines,aLines = supportLines(supportVals,h,dx,False,points,output)
            rLines = resistanceLines(resistanceVals,h,dx,False,points,output)
            intervals = points
            
        else:
            points = turningPoints(dx,False)
            points  = np.sort(points)
            
            #have the supportLines return the automatic intervals so that you dont have to call it in resistanceLines again
            sLines,aLines = supportLines(supportVals,h,dx,False,points,output)
            rLines = resistanceLines(resistanceVals,h,dx,False,points,output)
            
            intervals = points
            
    else:
        
        if output:
            intervals.append(len(h)-1)
            print("*****Starting Line generation*****")
            print("Manual Line Generation")
            print("Manual Line Intervals at Points ", intervals)
    
            #only calls this to output the derivative plots
            dontUse = turningPoints(dx,output)
            
            #have the supportLines return the automatic intervals so that you dont have to call it in resistanceLines again
            sLines,aLines = supportLines(supportVals,h,dx,automatic,intervals,output)
            rLines = resistanceLines(resistanceVals,h,dx,automatic,intervals,output)
            
        else:
            intervals.append(len(h)-1)
            
            #have the supportLines return the automatic intervals so that you dont have to call it in resistanceLines again
            sLines,aLines = supportLines(supportVals,h,dx,automatic,intervals,output)
            rLines = resistanceLines(resistanceVals,h,dx,automatic,intervals,output)
            
    
    
    
    
    
    
    
    return sLines,rLines,aLines,intervals


"""
lineCheck algo 

method 1 : calculate the amount of space above/below the closing prices to a line given and return as a float 

method 2 : (this is the one you call) give in the line you want to test (m,b) , give "s" for support/ "r" for resistance. returns the relative fit of the line (0 being no fit, 1 being perfect fit)
           calculates the average line between all the closing prices, use method 1 to calculate the amount of space above/below the line (above for res/below for support or other way around) use that as "best fit paramater"
           call method 1 on the given line, compare to the line of best fit and return a ratio or something


"""


#returns the amount of space between a line segment and a data set 
def lineOffset(h,m,b,start,end):
    
    above = 0
    below = 0
    
    #loop through every point
    for i in range(start,end):
        
        #calculate the difference between the point and the data set        
        difference = getPointOnLine(m, b, i) - h[i]
        
        #if the difference is +ve, the line is above
        if difference >=0 :
            above += difference
        else:
            below += difference
        
    return above,below


#uses the lineOffset method do determine how good of a fit each line is using the interpolated line of best from np.polyfit 
def checkLine(h,m,b,sr,start,end):
    
    
    x = np.arange(start,end,1)
    
    #returns the m and b for the line of best fit
    mAvg,bAvg = np.polyfit(x,h[start:end],1)
    plotLine(mAvg,bAvg,len(h),"a",h)
    
    
    aboveAVG,belowAVG = lineOffset(h,mAvg,bAvg,start,end)
    aboveThis, belowThis = lineOffset(h,m,b,start,end)
    
    
    if (sr == "s"):
        #return aboveAVG/aboveThis
        return aboveThis/aboveAVG
    else:
        #return belowAVG/belowThis
        return belowThis/belowAVG
    
