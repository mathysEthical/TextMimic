import re
from Crypto.Util.number import long_to_bytes

encoded=open("encoded.txt","r").read()
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

def arrayToInt(theArray, rotorsCount):
    total=0
    factor=1
    theArray=theArray[::-1]
    rotorsCount=rotorsCount[::-1]
    for i in range(len(rotorsCount)):
        total+=factor*theArray[i]
        factor*=rotorsCount[i]
    return total

def getRotorIndex(encoded,actualGrammar,rotorWords):
    toTest="{".join(actualGrammar.split("{")[:2])
    for i in range(len(rotorWords)):
        word=rotorWords[i]
        if(encoded.startswith(re.sub(r"{.*?}", word, toTest,1,re.MULTILINE))):
            return i

rotorsIndex=[]
for i in range(len(rotorsWords)):
    rotorIndex=getRotorIndex(encoded,grammar,rotorsWords[i])
    rotorsIndex.append(rotorIndex)
    begin=grammar.split("{")[0]
    grammar=grammar.replace(begin+"{"+allRotors[i]+"}",begin+rotorsWords[i][rotorIndex])

pt=arrayToInt(rotorsIndex,rotorsCount)
print(long_to_bytes(pt).decode())