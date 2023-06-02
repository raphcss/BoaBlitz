import socket
import sys
from _thread import *

server = "172.18.194.8"  # Mettez ici l'adresse IP de votre serveur
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(25)  # Permet 25 connexions simultanées
print("En attente d'une connexion")

def threaded_client(conn):
    conn.send(str.encode("Connecté"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("Déconnecté")
                break
            else:
                print("Reçu : ", reply)
                print("Envoi : ", reply)
            conn.sendall(str.encode(reply))
        except:
            break

while True:
    conn, addr = s.accept()
    print("Connecté à :", addr)
    start_new_thread(threaded_client, (conn,))