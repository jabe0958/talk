#!/usr/bin/env

from .abstract_responder import AbstractResponder
import random


class PptpResponder(AbstractResponder):
    def talk(self):
        return "pptp"

if __name__ == "__main__":
    pptp = PptpResponder() 
    for i in range(5):
        print("> " + pptp.talk())
