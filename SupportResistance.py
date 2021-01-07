

"""

main method


"""

from SupportResistanceMethod import *
from lineCalc import *
import matplotlib.pyplot as plt
import pandas as pd


######## main method ##########





symbol = "BTC-USD"


#number is in days, if the number is greater than the number of days the stock has been on the market, the plot will display all available data
data,hist,bean = getData(symbol,1000)
date = bean.iloc[0]
date = str(date.name)


#get lines s - 0 , r - 1
intervals = [23,45] 


sLines,rLines,aLines,intervals = getLines(data,True,intervals,True)


plt.plot(data)



for s in sLines:
    plotLine(s[0],s[1],len(data),"s",data)

for r in rLines:
    plotLine(r[0],r[1],len(data),"r",data)
    
for a in aLines:
    plotLine(a[0],a[1],len(data),"a",data)

plt.title("Closing Prices with Support and Resistance Lines\nSymbol:"+symbol+" Since " + date)

plt.show()

"""
Crash cases:
    


Issues:
    
    
"""


