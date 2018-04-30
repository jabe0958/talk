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
    
    res_num = len(responders)
    idx = random.randint(0, res_num - 1)
    
    return responders[idx]

