import re
import math
from Crypto.Util.number import bytes_to_long

grammar=open("grammar.txt","r").read()

allRotors=re.findall("{(.*?)}", grammar,re.MULTILINE)
rotorsWords=[]
rotorsCount=[]

maxHiddable=1
for R in allRotors:
    words=R.split("|")
    rotorsWords.append(words)
    maxHiddable*=len(words)
    rotorsCount.append(len(words))

maxChar=math.floor(math.log(maxHiddable)/math.log(256))
pt=bytes_to_long(input(f"Text to hide (Max {maxChar} chars ) : ").encode())
assert maxHiddable>pt, "Text to hide is too long"

def intToArray(pt, rotorsCount):
    rotorsCount=rotorsCount[::-1]
    rotorsIndex=[]
    for i in range(len(rotorsCount)):
        a=pt%(rotorsCount[i])
        pt-=a
        pt//=rotorsCount[i]
        rotorsIndex.append(a)
    return rotorsIndex[::-1]

rotorsIndex=intToArray(pt,rotorsCount)

for i in range(len(rotorsWords)):
    begin=grammar.split("{")[0]
    grammar=grammar.replace(begin+"{"+allRotors[i]+"}",begin+rotorsWords[i][rotorsIndex[i]])

open("encoded.txt","w").write(grammar)