#CS360_Robot, Server.py
#By: Lucas Cook

import socket
import threading
import array
import pickle
import select
import time
import sys

globalChecklist = [0,0,0]
clients = set()
clients_lock = threading.Lock()

class ThreadedServer:
    def __init__(self, host, port, master):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    #Continuously listening for incoming connection requests from Client.py
    #Accepts connection and adds the client to the set of all current clients
    #Calls listenToClient()
    def listen(self):
        def clientSetUpdater():
            size = -1
            while True:
                time.sleep(1)
                with clients_lock:
                    for c in clients.copy():
                        try:
                            c.send("HB")                         
                        except:
                            print "\nDISCONNECTED SOCKET:"
                            print c
                            clients.remove(c)
                if (len(clients) != size):
                    print "-\n--CURRENT CLIENTS---"
                    print list(clients)
                    size = len(clients)
                
        print globalChecklist
        self.sock.listen(5)
        clientSetUpdater = threading.Thread(name='clientSetUpdater',target=clientSetUpdater)
        clientSetUpdater.setDaemon(True)
        clientSetUpdater.start()
        
        while True:
            if globalChecklist == [1,1,1]:
                break
            client, address = self.sock.accept()
            with clients_lock:
                clients.add(client)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    #Sends the current checklist to the newly connected client
    #Listens for a message from the client , int (1,2,3,4,5)
    #Checks the number recieved off of the globalChecklist
    #Sends the updated checklist to every client 
    def listenToClient(self, client, address):
        size = 1024
        currentChecklist = pickle.dumps(globalChecklist)
        client.send(currentChecklist)
        while not globalChecklist == [1,1,1]:
            try:
                data = client.recv(size)
                if data:
                    response = data
                    if data == 'yellow':
                        globalChecklist[0] = 1
                    elif data == 'pink':
                        globalChecklist[1] = 1
                    elif data == 'blue':
                        globalChecklist[2] = 1
                    else:
                        print "INVALID INPUT"
                    print "\nFound "+response+" ball"
                    print globalChecklist

                    if globalChecklist == [1,1,1]:
                        client.send("-1")
                        
                    else:
                        sendableChecklist = pickle.dumps(globalChecklist)
                        with clients_lock:
                            for c in clients:
                                c.sendall(sendableChecklist)
                                
                else:
                    raise error('Client disconnected')

            except:
                client.close()
                return False

        print "---DISCONNECTING ALL CURRENT CLIENTS---"
        time.sleep(2)
        print "---SEARCH COMPLETE---"
        
if __name__ == "__main__":
    port_num = 8080;
    ThreadedServer('',port_num,'').listen().setDaemon(True)
