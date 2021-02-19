import os, sys, re
from read import readLine

prompt = '$ '
def redirect(Input):
    return False

def main():
    
    while True:
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1,prompt.encode())
        
        Input = readLine()
        Input = Input.split()
        
        if len(Input) == 0:#if no input 
            sys.exit(0)
            
        if "exit" in Input:
            os.write(1, ("Exiting shell\n").encode())
            sys.exit(0)
        if "cd" in Input:
            try:
                if ".." in Input:
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
            #CHANGE REST OF THIS FOR REDIRECT AND PIPE USE
            if ">" or "<" in Input: #check for redirect
                redirect(Input)
           
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, Input[0])
                try:
                    os.execve(program, Input, os.environ) #exec command with arguements
                except FileNotFoundError:
                    pass
                
            os.write(2, ("could not execute command %s\n" % input[0]).encode())
            sys.exit(1) #exit with error
            
        else:
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n"%childPidCode).encode())
                
if __name__ == '__main__':
        main()

    

        

