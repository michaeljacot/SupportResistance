

"""

main method


"""

from SupportResistanceMethod import *
from lineCalc import *
import matplotlib.pyplot as plt


######## main method ##########


symbol = "UBER"

data = getData(symbol,453)

#get lines s - 0 , r - 1
intervals = [23,45] 


sLines,rLines,aLines,intervals = getLines(data,True,intervals,False)


plt.plot(data)



for s in sLines:
    plotLine(s[0],s[1],len(data),"s",data)

for r in rLines:
    plotLine(r[0],r[1],len(data),"r",data)
    
for a in aLines:
    plotLine(a[0],a[1],len(data),"a",data)

plt.title("Closing Prices with Support and Resistance Lines\nSymbol:"+symbol)

plt.show()

"""
Crash cases:
    


Issues:
    
    
"""


