#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

numChildren = 0
pidAddr = {}

if paramMap['usage']:
    params.usage()

servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket will unbind immediately on close
servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# accept will timeout in 5s
servSock.settimeout(5)          

servSock.bind((listenAddr, listenPort))
servSock.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

# run by child
def chatWithClient(connAddr):  
    sock, addr = connAddr
    print(f'Child: pid={os.getpid()} connected to client at {addr}')
    sock.send(b"hello")
    time.sleep(0.25);       # delay 1/4s
    sock.send(b"world")
    sock.shutdown(socket.SHUT_WR)
    sys.exit(0)                 # terminate child

while True:
    # reap zombie children (if any)
    while pidAddr.keys():
        if (waitResult := os.waitid(os.P_ALL, 0, os.WNOHANG | os.WEXITED)): 
            zPid, zStatus = waitResult.si_pid, waitResult.si_status
            print(f"""zombie reaped:
            \tpid={zPid}, status={zStatus}
            \twas connected to {pidAddr[zPid]}""")
            del pidAddr[zPid]
            numChildren -= 1
        else:
            break               # no zombies; break from loop
    print(f"Currently {len(pidAddr.keys())} clients")

    try:
        connSockAddr = servSock.accept() # accept connection from a new client
    except TimeoutError:
        connSockAddr = None 

    if connSockAddr is None:
        continue
        
    forkResult = os.fork()     # fork child for this client 
    if (forkResult == 0):        # child
        servSock.close()         # child doesn't need servSock
        chatWithClient(connSockAddr)
    # parent
    numChildren += 1
    sock, addr = connSockAddr
    sock.close()   # parent closes its connection to client
    pidAddr[forkResult] = addr
    print(f"spawned off child with pid = {forkResult} at addr {addr}")
    

