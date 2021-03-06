
import os, sys, re
from read import readLine

prompt = '$ '
waitChild = True#always wait for child
Input = ""

def execute(inputArg):
    global Input
    Input = inputArg
    
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed. Try again.").encode())
        sys.exit(1)
    if rc == 0:
        if '/' in Input[0]: #for absolute paths
            prog = Input[0]
            try:
                os.execve(prog, Input, os.environ)
            except FileNotFoundError:
                pass
            os.write(2, ("%s : command not found\n" % (Input[0])).encode())
            sys.exit(1)
        if '<' in Input: #check for redirects
            redirect("in", Input)
        elif '>' in Input:
            redirect("out", Input)
        for dir in re.split(':', os.environ['PATH']):
            program = "%s/%s" % (dir, Input[0])
            try:
                os.execve(program, Input, os.environ)#have child execute program
            except FileNotFoundError:
                pass
        os.write(2, ("%s : command not found\n" % (Input[0])).encode())
        sys.exit(1)
    elif rc > 0:
        if waitChild:#by default always wait for child
            os.wait()
        os.write(2, ("child finished\n").encode())
        
        
def redirect(direction, inputArg):
    global Input
    Input = inputArg
    #check redirect if input or output
    if direction == "in":
        os.close(0)
        os.open(Input[Input.index('<')+1], os.O_RDONLY)#open file, open for reading only
        os.set_inheritable(0, True)
        Input.remove(Input[Input.index('<')+1])#remove associated characters
        Input.remove('<')
        
    if direction == "out":
        os.close(1)
        os.open(Input[Input.index('>')+1], os.O_CREAT | os.O_WRONLY)#create file if it doesnt exist
        os.set_inheritable(1, True)
        Input.remove(Input[Input.index('>')+1])
        Input.remove('>')
    
def pipeInput():
    global Input
    leftArg = Input[:Input.index('|')]#split just like regular string
    rightArg = Input[Input.index('|')+1:]
    pipeRead, pipeWrite = os.pipe()
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed\n").encode())
        sys.exit(1)
    elif rc == 0: #we will exec left arg here
        if '<' in leftArg:
            redirect("in", leftArg)         
        if '>' in leftArg:
            redirect("out", leftArg)
        os.close(1) #close fd1 for pipeWrite
        os.dup(pipeWrite)#dup pipeWrite
        os.set_inheritable(1, True)#allow child to use
        for fd in (pipeRead, pipeWrite):
            os.close(fd)#close associated file descriptors
        execute(leftArg)
        sys.exit(0)
    else: #then exec the right arg here
        if '<' in rightArg:
            redirect("in", rightArg)
        if '>' in rightArg:
            redirect("out", rightArg)
        os.close(0)#close 0 of fd which is connected to keyboard
        os.dup(pipeRead)#dup pipeRead
        os.set_inheritable(0, True)
        for fd in (pipeRead, pipeWrite):
            os.close(fd)#close associated file descriptors
        execute(rightArg)
        sys.exit(0)
        
def main():
    global waitChild
    global Input
    while True:
        
        if 'PS1' in os.environ:#if bash prompt present in environ then write it
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1,prompt.encode())
            
        Input = readLine()
        Input = Input.split()
        if '|' in Input: #check for pipe(), split in method, will probably fork in condition
            pipeInput()
            continue
        
        if "exit" in Input:
            os.write(1, ("Exiting shell\n").encode())
            sys.exit(0)
        if '&' in Input:
            waitChild = False
        if "cd" in Input:
            try:
                if len(Input) == 1:
                    os.chdir("..")#go back a directory
                    continue
                else:
                    os.chdir(Input[1])#change to arguement directory
                    continue
            except:#and if that directory doesnt exist throw an error
                os.write(2, ("director %s: no such directory" % Input[1]).encode())
                sys.exit(1)
        if "pwd" in Input:
            os.write(2, (os.getcwd() + "\n").encode())
            continue
        
        execute(Input)#exec program if it doesnt fit any of previous conditions
        
if __name__ == '__main__':
        main()
