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


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(f"Received token: {token}")  # Debugging output
        
        if not token:
            return jsonify({'message': 'Token não encontrado!'}), 403
        
        if token.startswith('Bearer '):
            token = token[7:]
        else:
            return jsonify({'message': 'Token mal formatado, prefixo Bearer ausente!'}), 403
        
        try:
            data = jwt_lib.decode(token, 'sprint', algorithms=["HS256"])
            g.user_cpf = data['cpf']
            g.user_role = data['role']
            print(f"Decoded data: {data}")  # Debugging output
        except jwt_lib.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 403
        except jwt_lib.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 403
        except Exception as e:
            return jsonify({'message': f'Token não pode ser verificado! {str(e)}'}), 403

        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    filtro = {'email': data['email'], 'senha': data['senha']}
    projecao = {'_id': 0}
    usuario = mongo.db.usuarios.find_one(filtro, projecao)
    if usuario is None:
        return {"erro": "usuário e/ou senha inválidos"}, 400
    token = jwt_lib.encode({'cpf': usuario['cpf'], 'role': usuario['role']}, 'sprint', algorithm='HS256')
    return {"token": token}, 200


@app.route('/usuarios', methods=['GET'])
def get_users():  
        filtro = {}
        projecao = {'_id': 0}
        dados_user = mongo.db.usuarios.find(filtro, projecao)
        lista_user = list(dados_user)
        return {'usuarios': lista_user}, 200


@app.route('/usuarios', methods=['POST'])
def post_users():
    data = request.json
    if data['nome'].strip() == "" or data['email'].strip() == "" or "@" not in data['email'] or data['senha'].strip() == "" or data['cpf'].strip() == "":
        return {"erro": "Todos os campos são obrigatórios e devem ser válidos"}, 400
    
    role = 'admin' if data['cpf'] == "000000000" else 'user'
    data.update({'role': role, 'id': mongo.db.ids.find_one()['id_user']})
    mongo.db.ids.update_one({}, {'$inc': {'id_user': 1}})
    
    if mongo.db.usuarios.find_one({'cpf': data['cpf']}):
        return {"erro": "CPF já cadastrado"}, 400
    
    token = jwt_lib.encode({'cpf': data['cpf'], 'role': role}, 'sprint', algorithm='HS256')
    user_data = data.copy()
    user_data.update({'token': token})
    mongo.db.usuarios.insert_one(user_data)
    return {"token": token, "id": user_data['id']}, 201

@app.route('/usuarios/<id>', methods=['GET'])
def get_user(id):
    filtro = {'id':id}
    projecao = {'_id': 0}
    dados_user = mongo.db.usuarios.find_one(filtro, projecao)
    return dados_user, 200

@app.route('/usuarios/<id>', methods=['PUT'])
@token_required
def put_user(id):
    data = request.json
    if not mongo.db.usuarios.find_one({"id": id}):
        return {"erro": "Usuário não encontrado"}, 404
    mongo.db.usuarios.update_one({"id": id}, {"$set": data})
    return {"mensagem": "Alteração realizada com sucesso"}, 200

@app.route('/usuarios/<id>', methods=['DELETE'])
@token_required
def delete_user(id):
    if not mongo.db.usuarios.find_one({"id": id}):
        return {"erro": "Usuário não encontrado"}, 404
    mongo.db.usuarios.delete_one({"id": id})
    return {"mensagem": "Usuário deletado com sucesso"}, 200

#-------------------------------------------------------------------------------
@app.route('/usuarios/a/<cpf>', methods=['GET'])
def get_user_cpf(cpf):
    filtro = {'cpf': cpf}
    projecao = {'_id': 0}
    dados_user = mongo.db.usuarios.find_one(filtro, projecao)
    return dados_user, 200

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

@app.route('/noticias/<titulo>', methods=['DELETE'])
@token_required
def delete_new(titulo): 
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