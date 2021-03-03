
import os, sys, re
from read import readLine

prompt = '$ '
Input = ""
waitChild = True

def execute(inputArg):
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed. Try again.").encode())
        sys.exit(1)
    if rc == 0:
        if '/' in inputArg[0]: #for absolute paths
            prog = inputArg[0]
            try:
                os.execve(prog, inputArg, os.environ)
            except FileNotFoundError:
                pass
            os.write(2, ("%s : command not found\n" % (inputArg[0])).encode())
            sys.exit(1)
        if '<' in inputArg: #check for redirects
            redirect("in")
        elif '>' in inputArg:
            redirect("out")
        
        for dir in re.split(':', os.environ['PATH']):
            program = "%s/%s" % (dir, inputArg[0])
            try:
                os.execve(program, inputArg, os.environ)#have child execute program
            except FileNotFoundError:
                pass
        
        os.write(2, ("%s : command not found\n" % (inputArg[0])).encode())
        sys.exit(1)
    elif rc > 0:
        if waitChild:#by default always wait for child
            os.wait()
        os.write(2, ("child finished\n").encode())

def redirect(direction):
    #check redirect if input or output
    global Input
    
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

def pipeInput(Inputarg):
    global Input
    Input = Input.split('|')#split into two separate commands
    leftArg = Input[0].split()#split just like regular string
    rightArg = Input[1].split()
    pipeRead, pipeWrite = os.pipe()
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed\n").encode())
        sys.exit(1)
    elif rc == 0: #we will exec left arg here
        if '<' in leftArg:
            redirect("in")         
        if '>' in leftArg:
            redirect("out")
        os.close(1) #close 1 of fd which is connected to screen
        os.dup(pipeWrite)#dup pipeWrite
        os.set_inheritable(1, True)#allow child to use
        for fd in (pipeRead, pipeWrite):
            os.close(fd)#close associated file descriptors
        execute(leftArg)
        
    else: #then exec the right arg here
        if '<' in rightArg:
            redirect("in")
        if '>' in rightArg:
            redirect("out")
        os.close(0)#close 0 of fd which is connected to keyboard
        os.dup(pipeRead)#dup pipeRead
        os.set_inheritable(0, True)
        for fd in (pipeWrite, pipeRead):
            os.close(fd)#close associated file descriptors
        execute(rightArg)
        
def main():
    global Input, waitChild
    
    while True:
        
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1,prompt.encode())
            
        Input = readLine()
        if '|' in Input: #check for pipe(), split in method, will probably fork in condition
            pipeInput(Input)
            continue
        
        Input = Input.split() #now below we can check the splitted string for certain keywords
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
        execute(Input)#exec program if it doesnt fit any of previous conditions
        """
        """        
if __name__ == '__main__':
        main()

    

        

