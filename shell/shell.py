import os, sys, re
from read import readLine

prompt = '$ '

def main():
    
    while True:
        
        os.write(1,prompt.encode())
        
        Input = readLine()
        Input = Input.split()
        
        if len(Input) == 0:
            sys.exit(0)
            
        if "exit" in Input:
            os.write(1, ("Exiting shell\n").encode())
            sys.exit(0)
            
        rc = os.fork()
        
        if rc < 0:
            os.write(2, ("fork failed\n").encode())
            sys.exit(1)
            
        elif rc == 0:
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, Input[0])
                try:
                    os.execve(program, Input, os.environ)
                except FileNotFoundError:
                    pass
                
            os.write(2, ("could not execute command %s\n" % input[0]).encode())
            sys.exit(1)
            
        else:
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n"%childPidCode).encode())              
if __name__ == '__main__':
        main()



        

