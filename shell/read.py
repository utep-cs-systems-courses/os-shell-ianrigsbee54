import os

Buff = None

def readChar():
    global Buff
    
    Buff = os.read(0, 500)
    
    return Buff

def readLine():
    global Buff
    string = ""
    i = 0
    
    if Buff == None:
        Buff = readChar()
    
    while len(Buff):
        string += chr(Buff[i])
        if "\n" in string:
            Buff = Buff[i+1:]
            return string
        i += 1
        
    if i == len(Buff):
        i = 0
        Buff = readChar()
    return string
