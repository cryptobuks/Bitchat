import time
import socket
import threading
import peers as ps
import string
import random

history = []
alives = []

def StartListen():
    host = "" #your ip
    port = 19001
    while 1:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        data, addr = sock.recvfrom(1024)
        gData = data.decode()
        gAddr = addr[0]
        threading.Thread(target=gotData, args=(gData,gAddr)).start()
        #gotData(data.decode(), addr[0]) # in threading ^
        sock.close()

def gotData(rawdata, addr):
    global alives
    print("recv: "+rawdata)
    data = rawdata.split("|")
    
    if data[0] == "msg":
        canPost = True
        if len(data) >= 3:
            for c in history:
                if c == data[2]: # checks if has been posted
                    canPost = False
            if canPost == True:
                print(data[1])
                history.append(data[2])
                for a in alives:
                    if a != addr:
                        SendData(rawdata, a)
    
    if data[0] == "ping":
        SendData("alive", addr)
        #aliveAppend(addr)
    if data[0] == "alive":
        aliveAppend(addr)
    if data[0] == "peer":
        if len(data) >= 1:
            ps.addPeer(data[1])
    if data[0] == "updatepeers":
        if len(data) >= 1:
            localpeers = ps.getLocalPeers()
            for p in localpeers:
                SendData("peer|"+str(p), addr)
                time.sleep(.1)

                
def SendData(data, host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    print("sending: "+data+", to: "+host)
    sock.sendto(bytes(data, "utf-8"), (host, 19001))
    sock.close()


def id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def gatherAlives():
    peers = ps.getLocalPeers()
    global alives
    alives = []
    #print(peers[0])
    for addr in peers:
        #print("addr: "+addr)
        SendData("ping", addr)

def cleanup():
    clean = []
    wasCleaned = False
    global alives
    for i in alives:
        if i not in clean:
            clean.append(i)
            wasCleaned == True
    if wasCleaned == True:
        alives = clean
            
def updatePeers():
    global alives
    for addr in alives:
        SendData("updatepeers", addr)

def aliveAppend(x):
    alives.append(x)
def getAlives():
    return alives

