#!/usr/bin/env python
import json
from six.moves.urllib.request import urlopen
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
from flask import session
import datetime

import paho.mqtt.client as mqttClient
import time


broker_address = "192.168.43.148"
port = 1883


client = mqttClient.Client("Python")               #create new instance
client.connect(broker_address, port=port)          #connect to broker
client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    print("waiting for connection")

dicc={'add':addPassword,'update':updatePassword,'delP':deletePassword,'delAll':deleteAllPasswords}

command=input("Ingrese la operacion que desea relizar con los argumentos necesarios")
parts=command.split(";")

if len(parts)>2:
    dicc[parts[0]](parts[1],parts[2])
elif len(parts)==2:
    dicc[parts[0]](parts[1])
else:
    dicc[parts[0]]()

AUTH0_DOMAIN = 'isis2503-jpotalora10.auth0.com'
API_AUDIENCE = 'uniandes.edu.co/blocksecurity'
ALGORITHMS = ["RS256"]

app=Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='3uxEZCqcYG-QyhES5770rxQ3wwOfdufn',
    client_secret='secretoooooooooo',
    api_base_url='https://isis2503-jpotalora10.auth0.com',
    access_token_url='https://isis2503-jpotalora10.auth0.com/oauth/token',
    authorize_url='https://isis2503-jpotalora10.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    resp = auth0.authorize_access_token()

    url = 'https://isis2503-jpotalora10.auth0.com/userinfo'
    headers = {'authorization': 'Bearer ' + resp['access_token']}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()

    # Store the tue user information in flask session.
    session['jwt_payload'] = userinfo

    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/dashboard')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='YOUR_CALLBACK_URL', audience='https://isis2503-jpotalora10.auth0.com/userinfo')

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': '3uxEZCqcYG-QyhES5770rxQ3wwOfdufn'}
    return redirect(auth0.base_url + '/v2/logout?' + urlencode(params))

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
        client.publish('security.sens.subs',"ADD_PASSWORD;"+str(val)+";"+str(index))

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
            client.publish('security.sens.subs',"UPDATE_PASSWORD;"+str(val)+";"+str(index))
    else:
        print('El usuario solo puede cambiar la clave entre 8AM y 6PM')
    if user=='adminYale':
        if int(val)<0 or int(val)>9999:
            print("La clave debe contener como maximo 4 digitos")
        elif int(index)<1 or int(index)>20:
            print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
        else:
            client.publish('security.sens.subs',"UPDATE_PASSWORD;"+str(val)+";"+str(index))

@app.route('/claves/del1', methods = ['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def deletePassword(index):
    now=datetime.datetime().now()
    if 18>now>8 and user=='propietario':
        if int(index)<1 or int(index)>20:
            print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
        else:
            client.publish('security.sens.subs',"DELETE_PASSWORD;"+str(index))
    else:
        print("El propietario no tiene permitido eliminar la clace en esta hora")


@app.route('/claves/del2')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def deleteAllPasswords():
    if user=='adminyale':
    else:
        print("No cuenta con los permisos necesarios apra realizar esta operacion")





