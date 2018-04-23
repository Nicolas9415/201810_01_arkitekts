#!/usr/bin/env python
from kafka import KafkaConsumer, KafkaProducer
import json
from six.moves.urllib.request import urlopen
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt
from flask import session
import datetime

import paho.mqtt.client as mqtt

AUTH0_DOMAIN = 'isis2503-jpotalora10.auth0.com'
API_AUDIENCE = 'uniandes.edu.co/blocksecurity'
ALGORITHMS = ["RS256"]

app=Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:8090')


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must start with"
                             " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                     "incorrect claims,"
                                     "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                     "Unable to parse authentication"
                                     " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)
    return decorated



 user=session['jwt_payload']['http://blockscurity/roles'][0]


@app.route('/claves/add', methods = ['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def addPassword(val,index):
    if val<0 or val>9999:
        print("La clave debe contener como maximo 4 digitos")
    elif index<1 or index>20:
        print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
    else:
        producer.send('claves',"ADD_PASSWORD;"+str(val)+";"+str(index))

@app.route('/claves/update', methods = ['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def updatePassword(val,index):
    now=datetime.datetime().now()
    if 18>now>8 and user=='propietario':
        if int(val)<0 or int(val)>9999:
            print("La clave debe contener como maximo 4 digitos")
        elif int(index)<1 or int(index)>20:
            print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
        else:
            producer.send('claves',"UPDATE_PASSWORD;"+str(val)+";"+str(index))
    else:
        print('El usuario solo puede cambiar la clave entre 8AM y 6PM')
    if: user=='adminYale'
        if int(val)<0 or int(val)>9999:
            print("La clave debe contener como maximo 4 digitos")
        elif int(index)<1 or int(index)>20:
            print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
        else:
            producer.send('claves',"UPDATE_PASSWORD;"+str(val)+";"+str(index))
@app.route('/claves/del1', methods = ['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def deletePassword(index):
    now=datetime.datetime().now()
    if 18>now>8 and user=='propietario':
        if int(index)<1 or int(index)>20:
            print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
        else:
            producer.send('claves',"DELETE_PASSWORD;"+str(index))
    else:
        print("El propietario no tiene permitido eliminar la clace en esta hora")


@app.route('/claves/del2')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def deleteAllPasswords():
    if user=='adminyale':
        producer.send('claves',"DELETE_ALL")
    else:
        print("No cuenta con los permisos necesarios apra realizar esta operacion")

dicc={'add':addPassword,'update':updatePassword,'delP':deletePassword,'delAll':deleteAllPasswords}

command=input("Ingrese la operacion que desea relizar con los argumentos necesarios")
parts=command.split(";")

if len(parts)>2:
    dicc[parts[0]](parts[1],parts[2])
elif len(parts)==2:
    dicc[parts[0]](parts[1])
else:
    dicc[parts[0]]()



