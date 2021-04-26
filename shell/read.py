from os import read

index = 0
limit = 0
def getChar():
    global index, limit
    if index == limit:
        index = 0
        limit = read(0, 100)
        if limit == 0:
            return "EOF"
    if index < len(limit)-1:
        c = chr(limit[index])
        index+=1
        return c
    else:
        return "EOF"
def readLine():
    global index, limit
    line = ""
    char = getChar()
    while (char != '' and char != "EOF"):
        line += char
        char = getChar()
    index = 0
    limit = 0
    return line
