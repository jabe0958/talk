import random

from flask import Blueprint
from flask import jsonify
from flask import g

from talk.models.marimite_responder import MarimiteResponder
from talk.models.pptp_responder import PptpResponder

talk = Blueprint('talk', __name__)

@talk.route("/")
def hello():
    return "Hello world."


@talk.route("/talk")
def hello2():
    return talk.talk()


@talk.route("/talk2")
def hello3():
    responder = getResponder()
    message = responder.talk()
    result = {'message': message}
    return jsonify(result)

def getResponder():
    responders = getattr(g, "_responders", None)
    if responders is None:
        responders = []
        responders.append(MarimiteResponder())
        responders.append(PptpResponder())
    
    borders = getattr(g, "_responder_borders", None)
    if borders is None:
        borders = []
        borders.append(80)
        borders.append(20 + sum(borders))

    borders_sum = getattr(g, "_responder_borders_sum", None)
    if borders_sum is None:
        borders_sum = borders[len(borders) - 1]

    pos = random.randint(0, borders_sum -1)
    idx = 0
    pre_border = 0
    print("[pos] %s" % (pos))
    for i, border in enumerate(borders):
        print("[i] %s, [border] %s" % (i, border))
        idx = i
        if pre_border <= pos and pos < border:
            break
    print("[idx] %s" % (idx)) 
    return responders[idx]

