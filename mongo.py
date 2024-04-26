from flask import Flask, request
from flask_pymongo import PyMongo
from api_gpt import post_todas_noticias

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
    
    idss = mongo.db.ids.find_one()
    data['id'] = idss['id_user']
    mongo.db.ids.update_one({}, {'$inc': {'id_user': 1}})
    
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
    post_todas_noticias()
    

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