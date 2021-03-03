import os

Buff = None #we want to remember where we are in Buff if newline in middle

def readChars():
    global Buff
    
    Buff = os.read(0, 500) #read up to 500 bytes
    
    return Buff

def readLine():
    global Buff
    string = ""#start with empty string
    i = 0
    
    if Buff == None:#read chars by default
        Buff = readChars()
    
    while len(Buff):
        string += chr(Buff[i])
        if "\n" in string:
            Buff = Buff[i+1:]#cut string to next character 
            return string
        i += 1
        
    if i == len(Buff):#if we reach end of Buff we reset
        i = 0
        Buff = readChars()
    return string
