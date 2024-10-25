import re
import math
from Crypto.Util.number import bytes_to_long
pt=bytes_to_long(b"DVC{Hello!}")

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

print("maxHiddable",math.floor(math.log(maxHiddable)/math.log(256)),"chars")
print("is hiddable", maxHiddable>pt)
# print("rotorsCount",rotorsCount)


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
# print("rotorsIndex",rotorsIndex)

for i in range(len(rotorsWords)):
    begin=grammar.split("{")[0]
    grammar=grammar.replace(begin+"{"+allRotors[i]+"}",begin+rotorsWords[i][rotorsIndex[i]])

open("encoded.txt","w").write(grammar)