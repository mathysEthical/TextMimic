import argparse
import re
import math
from Crypto.Util.number import bytes_to_long, long_to_bytes

parser = argparse.ArgumentParser(description='TextMimic is a tool to hide text using custom templates')

parser.add_argument('encodedFile', type=str, help='Encoded file path exemple encoded/cipher.txt')
parser.add_argument('template', type=str, help='Template to use, for exemple templates/event.txt')
parser.add_argument('mode', type=str, help='Mode: encode or decode')


args = parser.parse_args()

if args.mode not in ["encode","decode"]: parser.error("Mode must be 'encode' or 'decode'")

grammar=open(args.template,"r").read()

allRotors=re.findall("{(.*?)}", grammar,re.MULTILINE)
rotorsWords=[]
rotorsCount=[]

maxHiddable=1
for R in allRotors:
    words=R.split("|")
    rotorsWords.append(words)
    maxHiddable*=len(words)
    rotorsCount.append(len(words))

def encode(grammar):
    maxChar=math.floor(math.log(maxHiddable)/math.log(256))
    pt=bytes_to_long(input(f"Text to hide (Max {maxChar} chars ) : ").encode())
    assert maxHiddable>pt, "Text to hide is too long"
    rotorsIndex=intToArray(pt,rotorsCount)

    for i in range(len(rotorsWords)):
        begin=grammar.split("{")[0]
        grammar=grammar.replace(begin+"{"+allRotors[i]+"}",begin+rotorsWords[i][rotorsIndex[i]])

    open(args.encodedFile,"w").write(grammar)

def decode(grammar):
    encoded=open(args.encodedFile,"r").read()
    rotorsIndex=[]
    for i in range(len(rotorsWords)):
        rotorIndex=getRotorIndex(encoded,grammar,rotorsWords[i])
        rotorsIndex.append(rotorIndex)
        begin=grammar.split("{")[0]
        grammar=grammar.replace(begin+"{"+allRotors[i]+"}",begin+rotorsWords[i][rotorIndex])

    pt=arrayToInt(rotorsIndex,rotorsCount)
    print(long_to_bytes(pt).decode())

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
    longest=0
    toReturn=0
    for i in range(len(rotorWords)):
        word=rotorWords[i]
        if(encoded.startswith(re.sub(r"{.*?}", word, toTest,1,re.MULTILINE))):
            if(len(word)>longest):
                longest=len(word)
                toReturn=i
    return toReturn

def intToArray(pt, rotorsCount):
    rotorsCount=rotorsCount[::-1]
    rotorsIndex=[]
    for i in range(len(rotorsCount)):
        a=pt%(rotorsCount[i])
        pt-=a
        pt//=rotorsCount[i]
        rotorsIndex.append(a)
    return rotorsIndex[::-1]

if(args.mode=="encode"):
    encode(grammar)
if(args.mode=="decode"):
    decode(grammar)