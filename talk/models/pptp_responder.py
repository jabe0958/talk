#!/usr/bin/env

from .abstract_responder import AbstractResponder
import os, random

PPTP_FILE = "../../resources/pptp.txt"

class PptpResponder(AbstractResponder):
    def talk(self):
        messages = []
        base_dir = os.path.dirname(__file__)
        with open(os.path.join(base_dir, PPTP_FILE), "r") as f:
            message = f.readline()
            while message:
                message = message.strip()
                if len(message) > 0:
                    messages.append(message)
                message = f.readline()

        if len(messages) == 0:
            return "pptp error."

        idx = random.randint(0, len(messages) - 1)
        return messages[idx]

if __name__ == "__main__":
    pptp = PptpResponder() 
    for i in range(5):
        print("> " + pptp.talk())
