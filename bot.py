#!/usr/bin/env python3

import socket
import sys
import os
import re
from time import sleep

class IRClient:

    sock = socket.socket()

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, channel, message):
        self.sock.send(("PRIVMSG " + channel + " :" + message + "\n").encode())

    def connect(self, server, channel, nickname):
        self.sock.connect((server, 6667))
        self.sock.send(("USER " + nickname + " " + nickname + " " + nickname + " :Lets go on an Adventure!\n").encode())
        self.sock.send(("NICK " + nickname + "\n").encode())
        self.sock.send(("JOIN " + channel + "\n").encode())

    def quit(self):
        self.sock.send(("QUIT :Abentuerzeit! Schalten sie auch nächstes Mal wieder ein!\n").encode())

    def getText(self):
        text=self.sock.recv(4096).decode()

        if text.find("PING") != -1:
            self.sock.send(("PONG " + text.split()[1] + "\n").encode())

        return text

channel = "#adventuretime"
# channel = "#faui2k15"
# channel = "#katbot2"
server = "irc.fau.de"
nickname = "AdventureTime"

abenteuer = "Seht oh mächtige Mäuse! A KÄS! Doch OH JE! Der gefährliche katbot bewacht ihn! Was könnt Ihr nur tun um ihn zu bekommen?"

items = {
        "tot stellen" : "katbot durchschaut Euren Trick! Aber wie Katzen so sind, interessiert es nicht weiter und katbot verliert das interesse an Euch",
        "attacke" : "Ihr versucht katbot zu beißen, aber katbot beißt euch zuerst. Ihr seid tot!",
        "schlaflied singen" : "~sleepy\nkatbot ist eingeschlafen, Ihr könnt nun den KÄS Euch ergattern. Ehre gebühre Euch!"
        }

def getItems(items):
    head, *tail = items
    for item in tail:
        head += ", " + item
    return head

irc = IRClient()
irc.connect(server, channel, nickname)

irc.send(channel, "Zeit für ein Abenteur!")
irc.send(channel, "Heute: " + abenteuer)
i = getItems(items)
print(i)
irc.send(channel, "Ihr könnt folgendes tun: " + i )

while 1:
    t = irc.getText()
    print(t)
    if t.find("PRIVMSG " + channel + " :" + nickname) != -1:
        if t.find("raus!") != -1 and t.find(":Stef!") != -1:
            irc.send(channel, "ok..., Tschüssch")
            break
        elif t.find("auch") != -1:
            irc.send(channel, "Cool, du bist dabei! Derzeit: " + abenteuer)
        else:
            resp = items.get(re.findall(":"+ nickname + ": ([a-zA-Z\ ]*)", t)[0], "Lies doch oben was du tun kannst!").split("\n")
            for r in resp:
                irc.send(channel, r)
                sleep(1)
#            irc.send(channel, "under construction, aktuell geht nur: ich will auch mitmachen! oder irgendwas das auf \"auch\" matched")
irc.quit()
