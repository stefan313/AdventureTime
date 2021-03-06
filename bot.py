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

    def connect(self, server, nickname):
        self.sock.connect((server, 6667))
        self.sock.send(("USER " + nickname + " " + nickname + " " + nickname + " :Lets go on an Adventure!\n").encode())
        self.sock.send(("NICK " + nickname + "\n").encode())

    def join(self, channel):
        self.sock.send(("JOIN " + channel + "\n").encode())

    def quit(self):
        self.sock.send(("QUIT :Abenteuerzeit! Schalten sie auch nächstes Mal wieder ein!\n").encode())

    def getText(self):
        text=self.sock.recv(4096).decode()
        if text.find("PING") != -1:
            self.sock.send(("PONG " + text.split()[1] + "\n").encode())
        return text

#channel = "#adventuretime"
# channel = "#faui2k15"
channel = "#katbot"
# channel = "#mathe"
server = "irc.fau.de"
nickname = "AdventureTime"

#abenteuer = "Seht oh Ihr mächtigen Mäuse! A KÄS! Doch OH JE! Der gefährliche katbot bewacht ihn! Was könnt Ihr nur tun um ihn zu bekommen?"
abenteuer = "Helft dem flauschigen hrnz seine love Laura zu ergattern!"

'''
items = {
        "tot stellen" : "katbot durchschaut Euren Trick! Aber wie Katzen so sind, interessiert es einfach nicht weiter und katbot verliert das Interesse an Euch. Gerade noch mal davon gekommen!",
        "attacke" : "Ihr versucht katbot zu beißen, aber katbot beißt euch zuerst. Ihr seid tot!",
#        "schlaflied singen" : "Soft katbot, Warm katbot, Little ball of fur, happy katbot, sleepy katbot, purr purr purr.\nkatbot ist eingeschlafen, Ihr könnt nun den KÄS Euch ergattern. Ehre gebühre Euch!"
        "schlaflied singen" : "katbot: sleepy katbot\nkatbot ist eingeschlafen, Ihr könnt nun den KÄS Euch ergattern. Ehre gebühre Euch!"
        }
'''

items = {
        "schuechtern ansprechen" : "Laura friendzoned dich!",
        "ignorieren" : "Wie zur Hölle glaubst du funktioniert das mit den Damen????",
        "einen auf Macho machen" : "Leider verzählst du dich in den komplexen Zahlen in den komplexen Zahlen und Laura ist einfach besser in Mathe!\nZurück auf die Schulbank mit dir!",
        "knuddeln" : "Awwwwwwww <3\nNope...",
        "streicheln" : "Schelle!\nFrauen tascht man nicht einfach so an",
        "pi aufsagen" : "WOW\nUnd wie soll das jetzt helfen?",
        "knutschen" : "\n...\nEcht?\nTraust du dich eh nicht..."
        }

def getItems(items):
    head, *tail = items
    for item in tail:
        head += ", " + item
    return head

irc = IRClient()
irc.connect(server, nickname)
irc.join(channel)

irc.send(channel, "Zeit für ein Abenteuer!")
irc.send(channel, "Heute: " + abenteuer)
i = getItems(items)
irc.send(channel, "Ihr könnt folgendes tun: " + i )
irc.send(channel, "Useage: " + nickname + ": <aktion>")

while 1:
    t = irc.getText()
    print(t)
    if t.find("PRIVMSG " + channel + " :" + nickname) != -1:
        if t.find("raus!") != -1 and t.startswith(":Stef!308116@ircbox") != -1:
            irc.send(channel, "ok..., Tschüssch")
            break
        elif t.find("auch") != -1 or t.find("mitmachen") != -1:
            irc.send(channel, "Cool, du bist dabei! Derzeit: " + abenteuer)
            i = getItems(items)
            irc.send(channel, "Ihr könnt folgendes tun: " + i )
        else:
            resp = items.get(re.findall(":"+ nickname + ": ([a-zA-Z\ ]*)", t)[0], "Falls Ihr auch mitmachen möchtet: Schreibet es mir! Ansonsten: Lies doch oben was Ihr tun könnt!").split("\n")
            for r in resp:
                irc.send(channel, r)

irc.quit()
