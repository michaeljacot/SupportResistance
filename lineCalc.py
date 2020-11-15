# -*- coding: utf-8 -*-
"""
Created on Thu May  7 20:32:23 2020

@author: Michael
"""

import matplotlib.pyplot as plt
import numpy as np
from DerivativeAnalysis import turningPoints


#takes two points as tuples and returns the coeff for the linear equation (y = mx + b) 
def getLine(p1,p2):
    #point is in the form (x,y)
    
    #equation for slope
    m = (p2[0] - p1[0])/(p2[1] - p1[1])
    
    #rearange y = mx + b to solve for b
    b = p1[0] - p1[1]*m
    
    #return the coeffs as a tuple
    return [m,b]



#takes in the values for the slope and the y intercept and plots the line
#m : slope of the line , b: y intercept, domain: x range (from 0), sr: support or resistance (string "s" for support, "r" for resistance)
def plotLine(m,b,domain,sr,h):
        
    def line(x):
        return m*x +b
    
    x = np.arange(0,domain,1)
    
    if (sr == "s"):
        plt.plot(x,line(x),color = 'red',label = "Support Lines")
        plt.ylim(bottom = (min(h)-min(h)*0.2),top = (max(h)+max(h)*0.2)) 

    elif( sr == "r"):
        plt.plot(x,line(x),color = 'blue',label = "Resistance Lines")
        plt.ylim(bottom = (min(h)-min(h)*0.2),top = (max(h)+max(h)*0.2)) 
    elif (sr == "a"):
        plt.plot(x,line(x),color = 'green',label = "Average Lines")
        plt.ylim(bottom = (min(h)-min(h)*0.2),top = (max(h)+max(h)*0.2)) 
    else:
        print("Did not print line")
    


#this method takes in the paramaters of a line and returns how far above or below the line the point is
#point p is in form (x,y)
def compareToLine(m,b,p):
    
    x = p[0]
    y = p[1]
    
    compare = m*x+b
    return y-compare


#returns the point on the line y = mx + b corresponding to specific x position
def getPointOnLine(m,b,x):
    return m*x+b
    



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
    
#gets the minimum distance to a point from a line p- (x,y)
def distanceToLine(m,b,p):
    
    A = -m
    B = 1
    C = -b
    
    
    distance = abs(A*p[0] + B*p[1] + C)/np.sqrt(A**2+B**2)
    
    return distance



#gets the modifier to offset the y intercept of each new line. Modifies each new support or resistance line by offsetting the initial point 
def getBModifier(h,curB,mAvg,bAvg,vals,start,stop,sr,output):

    
    if (sr == "r"):
        if output:
            print()
            print("Finding bMod for range ", start,stop)
        
        averageDistance = 0
        
        
        pointCounter = 0
        largest = 0
        largestIndex = 1
        average = 0
        for i in range(start,stop):
            
            if i in vals:
                average += vals[i]
                pointCounter +=1
                
                
                
                thisDistance = distanceToLine(mAvg,bAvg,(i,vals[i]))
                
                averageDistance += thisDistance
                
                
                if thisDistance > largest:
                    largest = thisDistance
                    largestIndex = i
                    
        
        #catches the condition where zero points are found in range
        if pointCounter == 0:
            if output: print("Zero points found in the range ", start, stop , " Try increasing range to find more points")
            return 0
        
        
        averageDistance = averageDistance/pointCounter
        if output:print("The average distance to the line for points in this range is ", averageDistance)
            
        if output:print("Points in this range is ", pointCounter)
        #average = average / (pointCounter)      
        furthestPoint = (largestIndex,vals[largestIndex])
        
        #using this value as the bModifier would always return paralel lines
        distance = distanceToLine(mAvg,bAvg,furthestPoint)
        
        
        trueDistance = pythagoreanDisplacement(mAvg, bAvg, distance)
        if output:
            print("The distance to the furthest point from average line is ", distance)
            print("The displacement that the line will have to take to be parallel will be ", trueDistance)
            print()
        
        return trueDistance  + averageDistance
    
    else:
        if output:
            print()
            print("Finding bMod for range ", start,stop)
        
        
        
        averageDistance = 0
        pointCounter = 0
        maxDistance = 0
        maxDistanceIndex = 1
        average = 0
        for i in range(start,stop):
            
            if i in vals:
                average += vals[i]
                pointCounter +=1
                
                thisDistance = distanceToLine(mAvg,bAvg,(i,vals[i]))
                
                averageDistance += thisDistance
                
                
                if thisDistance > maxDistance:
                    maxDistance = thisDistance
                    maxDistanceIndex = i
                    
        #catches the condition where zero points are found in range
        if pointCounter == 0:
            if output: print("Zero points found in the range ", start, stop , " Try increasing range to find more points")
            return 0

          
        
        averageDistance = averageDistance/pointCounter
        if output: print("The average distance to the line for points in this range is ", averageDistance)
        
        
        if output:print("Points in this range is ", pointCounter)
        average = average / (pointCounter)      
        furthestPoint = (maxDistanceIndex,vals[maxDistanceIndex])
        
        distance = distanceToLine(mAvg,bAvg,furthestPoint)
        
        
        trueDistance = pythagoreanDisplacement(mAvg, bAvg, distance)
        
        if output:
            print("The distance to the furthest point from average line is ", distance)
            print("The displacement that the line will have to take to be parallel will be ", trueDistance)
            print()
        
        
        
        #return distance + modifier*mFactor + averageDistance
        return trueDistance + averageDistance
    
#returns the actual displacement that the line should have (ask me about this is you want it explained)
def pythagoreanDisplacement(m,b,displacement):
    #find angle that the line makes with horizontal (same as angle with vertical)
    vAngle = np.arctan(m)
    
    trueDisplacement = displacement/np.cos(vAngle)
    
    return trueDisplacement
    

