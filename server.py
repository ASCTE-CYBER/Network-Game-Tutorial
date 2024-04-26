import socket
from _thread import *
import sys
from var import NUMBER_PLAYERS, SERVER_HOST, SERVER_PORT, BUFFER_SIZE

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER_HOST, SERVER_PORT))
except socket.error as e:
    print(str(e))

s.listen(NUMBER_PLAYERS)
print("Waiting for a connection")

def get_ids(id):
    player_ids = []
    for i in range(0, NUMBER_PLAYERS):
        if i != id:
            player_ids.append(i)
    return player_ids

currentId = "0"
pos = ["0:50,50", "1:100,100", "2:150,150"]
def threaded_client(conn):
    global currentId, pos, NUMBER_PLAYERS
    global pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        #try:
        data = conn.recv(BUFFER_SIZE)
        reply = data.decode('utf-8')
        if not data:
            conn.send(str.encode("Goodbye"))
            break
        else:
            print("Received: " + reply)
            arr = reply.split(":")
            id = int(arr[0])
            pos[id] = reply

            other_player_ids = get_ids(id)
            for i in other_player_ids:
                reply = pos[i][:] + ';'
                print("Sending: " + reply)
                conn.sendall(str.encode(reply))
        #except:
            #break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))
