import blinker as _
import requests

from flask import Flask, Response
from flask import jsonify
from flask import request as flask_request


app = Flask('API')

@app.route('/think/')
def think_handler():
    
    thoughts = requests.get('http://thinker:8000/', params={
        'subject': flask_request.args.getlist('subject', str),
    }).content

    return Response(thoughts, mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
