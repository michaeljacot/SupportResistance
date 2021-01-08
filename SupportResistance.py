

"""

main method


"""

from SupportResistanceMethod import *
from lineCalc import *
import matplotlib.pyplot as plt
import pandas as pd


######## main method ##########


# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max


symbol = "BTC-USD"


#number is in days, if the number is greater than the number of days the stock has been on the market, the plot will display all available data
#getData(symbol,period, window)
period = "6mo"
window = "1d"

closes,data = getData(symbol,period,window)
date = data.iloc[0]
date = str(date.name)


#get lines s - 0 , r - 1
intervals = [23,45] 


sLines,rLines,aLines,intervals = getLines(closes,True,intervals,False)


plt.plot(closes)



for s in sLines:
    plotLine(s[0],s[1],len(closes),"s",closes)

for r in rLines:
    plotLine(r[0],r[1],len(closes),"r",closes)
    
for a in aLines:
    plotLine(a[0],a[1],len(closes),"a",closes)

plt.title("Closing Prices with Support and Resistance Lines\nSymbol:"+symbol+" Since " + date + "\n With closes every " +window )

plt.show()

"""
Crash cases:
    


Issues:
    
    
"""


