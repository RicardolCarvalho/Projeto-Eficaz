from flask import Flask, request, Response, jsonify, g
from flask_pymongo import PyMongo
from api_gpt_g1 import post_todas_noticias
from api_gpt_uol import post_todas_noticias_2
from urllib.parse import unquote
from functools import wraps
import jwt as jwt_lib 


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@projeficaz.fsc9tus.mongodb.net/TGproj"
mongo = PyMongo(app, tlsAllowInvalidCertificates=True, tls=True)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    filtro = {'email': data['email'], 'senha': data['senha']}
    projecao = {'_id': 0}
    usuario = mongo.db.usuarios.find_one(filtro, projecao)
    if usuario is None:
        return {"erro": "usuário e/ou senha inválidos"}, 400
    return {"id": usuario['id']}, 200

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token não encontrado!'}), 403
        
        if token.startswith('Bearer '):
            token = token[7:]
        try:
            data = jwt_lib.decode(token, 'sprint', algorithms=["HS256"])
            g.user_cpf = data['cpf']
        except jwt_lib.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 403
        except jwt_lib.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 403
        except Exception as e:
            return jsonify({'message': 'Token não pode ser verificado!'}), 403

        return f(*args, **kwargs)
    return decorated_function

@token_required
@app.route('/usuarios', methods=['GET'])
def get_users(): 
    cpf = g.user_cpf
    if cpf == "000000000":    
        filtro = {}
        projecao = {'_id': 0}
        dados_user = mongo.db.usuarios.find(filtro, projecao)
        lista_user = list(dados_user)
        return {'usuarios': lista_user}, 200

@token_required
@app.route('/usuarios', methods=['POST'])
def post_users():
    cpf = g.user_cpf
    if cpf == "000000000": 
        filtro = {}
        projecao = {'_id': 0}
        data = request.json
        if data['nome'] == " " or data['nome'] == "":
            return {"erro": "nome é obrigatório"}, 400
        if data['email'] == " " or data['email'] == "" or "@" not in data['email']:
            return {"erro": "email é obrigatório"}, 400
        if data['senha'] == " " or data['senha'] == "":
            return {"erro": "senha é obrigatório"}, 400
        if data['cpf'] == " " or data['cpf'] == "":
            return {"erro": "cpf é obrigatório"}, 400
        
        idss = mongo.db.ids.find_one()
        data['id'] = idss['id_user']
        mongo.db.ids.update_one({}, {'$inc': {'id_user': 1}})
        
        dados_user = mongo.db.usuarios.find(filtro, projecao)
        lista_user = list(dados_user)
        for user in lista_user:
            if data['cpf'] == user['cpf']:
                return {"erro": "cpf já cadastrado"}, 400
            
        token = jwt_lib.encode({'cpf:': data['cpf']}, 'sprint', algorithm='HS256')
        user_data = {'id': data['id'], 'nome': data['nome'], 'email': data['email'], 'senha': data['senha'], 
                    'cpf': data['cpf'], 'token': token}

        result = mongo.db.usuarios.insert_one(user_data)
        return {"token": token, "id": str(result.inserted_id)}, 201

@token_required
@app.route('/usuarios/<id>', methods=['GET'])
def get_user(id):
    filtro = {'id':id}
    projecao = {'_id': 0}
    dados_user = mongo.db.usuarios.find_one(filtro, projecao)
    return dados_user, 200

@token_required
@app.route('/usuarios/<id>', methods=['PUT'])
def put_user(id):
    cpf = g.user_cpf
    if cpf == "000000000": 
        filtro = {"id":id}
        projecao = {"_id": 0} 
        data = request.json
        usuario_existente = mongo.db.usuarios.find_one(filtro, projecao)
        if usuario_existente is None:
            return {"erro": "usuário não encontrado"}, 404
        mongo.db.usuarios.update_one(filtro, {"$set": data})
        return {"mensagem": "alteração realizada com sucesso"}, 200

@token_required
@app.route('/usuarios/<id>', methods=['DELETE'])
def delete_user(id):
    cpf = g.user_cpf
    if cpf == "000000000":
        filtro ={"id": id}
        projecao = {'_id': 0}
        usuario_existente = mongo.db.usuarios.find_one(filtro, projecao)
        if usuario_existente is None:
            return {"erro": "usuário não encontrado"}, 404
        else:
            mongo.db.usuarios.delete_one(filtro)
        
        return {"mensagem": "usuário deletado com sucesso"}, 200

#-------------------------------------------------------------------------------
@app.route('/noticias', methods=['GET'])
def get_news():
    filtro = {}
    projecao = {'_id': 0}
    dados_news = mongo.db.noticias.find(filtro, projecao)
    lista_news = list(dados_news)
    return {'noticias': lista_news}, 200

@app.route('/noticias', methods=['POST'])
def post_news():
    post_todas_noticias()
    post_todas_noticias_2()
  
@app.route('/noticias/<titulo>', methods=['GET'])
def get_new(titulo):
    titulo = unquote(titulo)
    filtro = {'titulo': titulo}
    projecao = {'_id': 0}
    dados_news = mongo.db.noticias.find_one(filtro, projecao)
    return dados_news, 200

@token_required
@app.route('/noticias/<titulo>', methods=['DELETE'])
def delete_new(titulo):
    cpf = g.user_cpf
    if cpf == "000000000": 
        titulo = unquote(titulo)
        filtro ={"titulo": titulo}
        projecao = {'_id': 0}
        noticia_existente = mongo.db.noticias.find_one(filtro, projecao)
        if noticia_existente is None:
            return {"erro": "notícia não encontrada"}, 404
        else:
            mongo.db.noticias.delete_one(filtro)
        
        return {"mensagem": "notícia deletada com sucesso"}, 200

@token_required
@app.route('/noticias/<titulo>', methods=['PUT'])
def put_new(titulo):
    cpf = g.user_cpf
    if cpf == "000000000": 
        titulo = unquote(titulo)
        filtro = {"titulo": titulo}    
        projecao = {"_id": 0} 
        data = request.json
        noticia_existente = mongo.db.noticias.find_one(filtro, projecao)

        if noticia_existente is None:
            return {"erro": "notícia não encontrada"}, 404
        
        mongo.db.noticias.update_one(filtro, {"$set": data})
        return {"mensagem": "alteração realizada com sucesso"}, 200

if __name__ == '__main__':
    app.run(debug=True)