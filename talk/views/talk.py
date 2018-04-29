from flask import Blueprint
from flask import jsonify

from talk.models.marimite_responder import MarimiteResponder

talk = Blueprint('talk', __name__)


@talk.route("/")
def hello():
    return "Hello world."


@talk.route("/talk")
def hello2():
    return talk.talk()


@talk.route("/talk2")
def hello3():
    responder = MarimiteResponder()
    message = responder.talk()
    result = {'message': message}
    return jsonify(result)


