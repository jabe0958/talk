#!/usr/bin/env python

from flask import Flask

from talk.views.talk import talk

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

app.register_blueprint(talk, url_prefix='/talk')


@app.after_request
def set_json_charset(response):
    content_type = response.headers.get('Content-Type')
    if content_type.lower().find('application/json') > -1:
        response.headers.add('Content-Type', 'application/json; charset=UTF-8')
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
