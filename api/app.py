from flask import Flask, jsonify

DEBUG = True

app = Flask

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong')
