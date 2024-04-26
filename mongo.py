from flask import Flask, request
from flask_pymongo import PyMongo
from get_g1 import get_g1_news

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://admin:admin@projeficaz.fsc9tus.mongodb.net/TGproj"
mongo = PyMongo(app)

@app.route('/usuarios', methods=['GET'])
def get_users():    
    filtro = {}
    projecao = {'_id': 0}
    dados_user = mongo.db.usuarios.find(filtro, projecao)
    lista_user = list(dados_user)
    return {'usuarios': lista_user}, 200

@app.route('/usuarios', methods=['POST'])
def post_users():
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
    
    id_users = mongo.db.ids.find_one('id_user')
    data['id'] = id_users['id_user']
    mongo.db.ids.update_one({'_id': 'id_user'}, {'$inc': {'id_user': 1}})
    
    dados_user = mongo.db.usuarios.find(filtro, projecao)
    lista_user = list(dados_user)
    for user in lista_user:
        if data['cpf'] == user['cpf']:
            return {"erro": "cpf já cadastrado"}, 400

    result = mongo.db.usuarios.insert_one(data)
    return {"id": str(result.inserted_id)}, 201

@app.route('/usuarios/<id>', methods=['GET'])
def get_user(id):
    filtro = {'id':id}
    projecao = {'_id': 0}
    dados_user = mongo.db.usuarios.find_one(filtro, projecao)
    return dados_user, 200

@app.route('/usuarios/<id>', methods=['PUT'])
def put_user(id):
    filtro = {"id":id}
    projecao = {"_id": 0}
    data = request.json
    usuario_existente = mongo.db.usuarios.find_one(filtro, projecao)
    if usuario_existente is None:
        return {"erro": "usuário não encontrado"}, 404
    mongo.db.usuarios.update_one(filtro, {"$set": data})
    return {"mensagem": "alteração realizada com sucesso"}, 200

@app.route('/usuarios/<id>', methods=['DELETE'])
def delete_user(id):
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
    data = request.json
    if data['titulo'] == " " or data['titulo'] == "":
        return {"erro": "título é obrigatório"}, 400
    if data['data'] == " " or data['data'] == "":
        return {"erro": "data é obrigatório"}, 400
    if data['conteudo'] == " " or data['conteudo'] == "":
        return {"erro": "conteúdo é obrigatório"}, 400
    if data['tipo'] == " " or data['tipo'] == "":
        return {"erro": "tipo é obrigatório"}, 400
    
    id_newss = mongo.db.ids.find_one('id_news')
    data['id'] = id_newss['id_news']
    mongo.db.ids.update_one({'_id': 'id_news'}, {'$inc': {'id_news': 1}})
    
    result = mongo.db.noticias.insert_one(data)
    return {"id": str(result.inserted_id)}, 201

@app.route('/noticias/<id>', methods=['GET'])
def get_new(id):
    filtro = {'id': id}
    projecao = {'_id': 0}
    dados_news = mongo.db.noticias.find_one(filtro, projecao)
    return dados_news, 200

@app.route('/noticias/<id>', methods=['DELETE'])
def delete_new(id):
    filtro ={"id": id}
    projecao = {'_id': 0}
    noticia_existente = mongo.db.noticias.find_one(filtro, projecao)
    if noticia_existente is None:
        return {"erro": "notícia não encontrada"}, 404
    else:
        mongo.db.noticias.delete_one(filtro)
    
    return {"mensagem": "notícia deletada com sucesso"}, 200

if __name__ == '__main__':
    app.run(debug=True)