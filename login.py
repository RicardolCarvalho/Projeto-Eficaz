from flask import request, Response
from functools import wraps 
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_auth(username, password, mongo):
    hashed_password = hash_password(password)
    filtro = {'email': username, 'senha': hashed_password}
    usuario = mongo.db.usuarios.find_one(filtro)
    return bool(usuario)

def authenticate():
    return Response(
    'Acesso negado.\n'
    'Faça login com usuário e senha válidos.', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password, kwargs('mongo')):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
