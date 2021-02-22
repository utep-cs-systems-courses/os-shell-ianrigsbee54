
import os, sys, re
from read import readLine

prompt = '$ '
Input = ""

def redirect(direction):
    #check redirect if input or output
    #return and pass in loop
    global Input
    
    if direction == "in":
        os.close(0)
        os.open(Input[Input.index('<')+1], os.O_RDONLY)
        os.set_inheritable(0, True)
        Input.remove(Input[Input.index('<')+1])
        Input.remove('<')
    if direction == "out":
        os.close(1)
        os.open(Input[Input.index('>')+1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        Input.remove(Input[Input.index('>')+1])
        Input.remove('>')

def pipeInput(Inputarg):
    global Input
    Input = Input.split('|')
    leftArg = Input[0].split()
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
            #FINISH LEFTARG
            
    else: #then exec the right arg here
        if '<' in rightArg:
            redirect("in")
        if '>' in rightArg:
            redirect("out")
            #FINISH RIGHTARG
        
        
def main():
    global Input
    
    while True:
        
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1,prompt.encode())
        
        Input = readLine()
        
        if '|' in Input: #check for pipe here so we can split in pipe()
            pipeInput(Input)
            continue
        
        Input = Input.split() #now below we can check the splitted string for certain keywords
        
        
        if "exit" in Input:
            os.write(1, ("Exiting shell\n").encode())
            sys.exit(0)
        if "cd" in Input:
            try:
                if len(Input) == 1:
                    os.chdir("..")#go back a directory
                else:
                    os.chdir(Input[1])#change to arguement directory
            except:#and if that directory doesnt exist throw an error
                os.write(2, ("director %s: no such directory" % Input[1]).encode())

        
        rc = os.fork()
        
        if rc < 0:
            os.write(2, ("fork failed\n").encode())
            sys.exit(1) 
            
        elif rc == 0:
            #CHANGE FOR PIPE USE
            if '>' in Input: #check for redirect
                redirect("out")
            if '<' in Input:
                redirect("in")
           
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, Input[0])
                try:
                    os.execve(program, Input, os.environ) #exec command with arguements
                except FileNotFoundError:
                    pass
                
            os.write(2, ("could not execute command %s\n" % Input[0].encode()))
            sys.exit(1) #exit with error
        else:
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n"%childPidCode).encode())
                
if __name__ == '__main__':
        main()

    

        

