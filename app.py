import database
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from os import environ

load_dotenv('.env')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def lol():
    return " powered by PAX with ❤ ", 200

@app.route('/register-license', methods=['POST'])
def registerLicense():
    license = request.args.get('license')
    username = request.args.get('username')
    admin = request.args.get('admin')
    if not license or not admin or not username:
        return jsonify({ "error": True, "message": "Unsuficient arguments" }), 400
    elif not admin == environ['ADMIN-KEY']:
        return jsonify({ "error": True, "message": "Invalid access key" }), 401
    else:
        r = database.addLicense(username, license)
        return jsonify(r)

@app.route('/revoke-license', methods=['DELETE'])
def revokeLicense():
    license = request.args.get('license')
    admin = request.args.get('admin')
    if not license or not admin:
        return jsonify({ "error": True, "message": "Unsuficient arguments" }), 400
    elif not admin == environ['ADMIN-KEY']:
        return jsonify({ "error": True, "message": "Invalid access key" }), 401
    else:
        l = database.checkLicense(license)
        if not 'error' in l:
            database.revokeLicense(license)
        return jsonify(l)

@app.route('/check-license', methods=['GET'])
def checkLicense():
    license = request.args.get('license')
    if not license:
        return jsonify({ "error": True, "message": "License not provided" }), 400
    else:
        l = database.checkLicense(license)
        return jsonify(l)

if __name__ == "__main__":
    try:
        _ = environ['ADMIN-KEY']
        _ = environ['DATABASE-URL']
    except:
        print('ERRO: não foi possível relacionar alguma variável de ambiente')
        exit(-1)
    app.run()