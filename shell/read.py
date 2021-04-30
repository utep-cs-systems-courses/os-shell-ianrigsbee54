from os import read

index = 0
limit = 0
line = ""
def getChar():
    global index, limit
    if index == limit: #initially 0=0
        index = 0
        limit = read(0, 100)#fill buffer
        if limit == 0: #if nothing was inputted
            return "EOF"
    if index < len(limit)-1: #ensure we dont get index out of bounds error
        c = chr(limit[index])#convert encoded byte to char and return it
        index+=1
        return c
    else:
        return "EOF"#once we reach the end, return EOF
def readLine():
    global index, limit, line
    line = "" #for our return string
    char = getChar()
    while (char != '' and char != "EOF" and char != '\n'): #search for specific characters
        line += char #put char into line and continue
        char = getChar()
    index = 0#once we are done with a line then set initial values to 0
    limit = 0
    return line
