# -*- coding: utf-8 -*-
"""
Created on Sat May  2 17:40:36 2020

@author: Michael
"""

"""
    Analyze the values of the analytic first derivative to determine how to segment the plot
    
"""
import scipy.fftpack as ft
import numpy as np
import matplotlib.pyplot as plt 



"""
    Idea for fourier smoothing:
        Take the fourier transform of the raw closing prices.
        Set all but the first 10% of the fourier coefficients to 0. (smoothing)
        Preform inverse fourier transform. (Might need to scale data)
        Call np.gradient for first derivative of discrete data.
        Check for when its 0, save those indicies.
"""

#preforms smoothing with fourier coefficients
def fourier(h,fSmooth):
    #fourier stuff

    #preform cosine transform
    coeffs = ft.dct(h)

    #set all but the first 10% to 0
    #NOTE for a smoother plot, lower the value of fSmooth (its read as a percent i.e. 0 == 0% , 1 == 100%)
    
    coeffs[int(len(coeffs)*fSmooth)+1:] = 0

    #preform inverse cosine transform on the new coefficients
    invcoef = ft.idct(coeffs)/200 # for some reason the inverse fourier transform gets scaled by a factor of 200, this doesnt actually matter since we are looking at the rate of change, but I adjusted it anyways

    return invcoef

#returns the "behavior" of the trend 
def trend(dx,i):
    
    
    winSize = 5
    
    window = int(len(dx)/winSize)
    

    if i > len(dx)-window:
        #print("End case")
        return sum(dx[len(dx)-window:len(dx)])/window
    
    #print("Getting trend for range ", i, window+i)
    return sum(dx[i:window+i])/window
    
   
     
def turningPoints(dx,output):
    
    trends = []
    
    if output:
        plt.plot(dx)
        plt.title("Plot 1 : \nFirst Derivative from np.gradient")
        plt.show()
    
    #apply the fourier transform and smooth the plot
    
    """
        What is happening here?
            We apply a discrete cosine fourier transform (scipy method) to the set of data points. This essentially turns the set of
            numbers that we gave it into a function (like f(x) = x^2) whos terms consist of an infinite series of cosine functions. 
            In front of all of these functions is a fourier coefficient (thats actually what the scipy method returns, just a list of
            these coefficients), of which we can set a significant portion to 0 (thats what line 37 does in this file). What this does is
            it eleminates the effect of that cosine term from the overall function, which essentially removes a portion of the noise from the
            initial function. You can then take the points again (which have been modified so some are 0) and use an inverse cosine transform
            to put the function back into a form that you can look at again. That is what is happening between plots 1 and 2.
    """
    fSmooth = 0.2
    
    #apply the fourier transform and smooth the plot
    dx = fourier(dx,fSmooth)
    
    for i in range(len(dx)-1):
        trends.append(trend(dx,i))
        
    if output:   
        plt.plot(dx)
        plt.title("Plot 2 : \nFirst Derivative Smoothed using a Discrete Cosine Transform")
        plt.show()
        
    minimum = trends.index(min(trends))
    maximum = trends.index(max(trends))
    
    
    
    minThreshold = 0.05 # do not accept any turning points within the first 5% of the data set
    
    #the index at which if any turning point gets generated before it, the system will not accept it 
    minimumIndex = int((len(dx)-1)*minThreshold)
    
    
    #catches the case where both generated values are before the first 5% of the data set, returns the minimumIndex and the last value of the data set in this case
    if minimum < minimumIndex and maximum < minimumIndex: 
        return [minimumIndex,len(dx)-1]
    
    #same condition as above, but checks the other boundary condition (end of the list)
    if minimum > (len(dx)-1)-minimumIndex and maximum > (len(dx)-1)-minimumIndex:
        return [(len(dx)-1)-minimumIndex, (len(dx)-1)]
        
    #catches the condition where both values are generated at the indexes right beside eachother
    if abs(minimum-maximum)<2:
        return [minimum,len(dx)-1]
            
    #final check case, checks for one of the values being out of range
    if minimum < minimumIndex: return [maximum,len(dx)-1]
    if maximum < minimumIndex: return [minimum,len(dx)-1]
    
    if minimum > (len(dx)-1)-minimumIndex: return [maximum,len(dx)-1]
    if maximum > (len(dx)-1)-minimumIndex: return [minimum,len(dx)-1]
    
    
        
    """
        
        check for one turning point basically, you could just have it that both points have to
        cross a threshold and then only return the points that make it over the threshold
        
        make a method for all of the tests at the end ( lines 93-110)  
    """

    
        
    
    return [minimum,maximum,len(dx)-1]


