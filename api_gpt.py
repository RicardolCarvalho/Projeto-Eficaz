import openai
from get_g1 import get_g1_news
from pymongo import MongoClient
import time
import random 

client = MongoClient("mongodb+srv://admin:admin@projeficaz.fsc9tus.mongodb.net/TGproj", tlsAllowInvalidCertificates=True, tls=True)
db = client.TGproj

def post_noticias(data):
    if data['titulo'] == " " or data['titulo'] == "":
        return {"erro": "título é obrigatório"}, 400
    if data['conteudo'] == " " or data['conteudo'] == "":
        return {"erro": "conteúdo é obrigatório"}, 400
    if data['data'] == " " or data['data'] == "":
        return {"erro": "data é obrigatória"}, 400
    
    id_noticias = db.ids.find_one()
    data['id'] = id_noticias['id_news']
    db.ids.update_one({}, {'$inc': {'id_news': 1}})
    
    result = db.noticias.insert_one(data)
    return {"id": str(result.inserted_id)}, 201


def safe_api_call(call_function, *args, **kwargs):
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        try:
            return call_function(*args, **kwargs)
        except openai.error.RateLimitError as e:
            sleep_time = min(60, (2 ** attempt) + random.uniform(0, 1))  
            print(f"Rate limit reached, retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
            attempt += 1
    raise Exception("API call failed after maximum number of retries")





def resume_noticias(noticia):
    openai.api_key = ''
    noticias_resumidas = []
    for i in range(len(noticia)):
        messages = [
            {"role": "system", "content": "Você é um assistente que resume notícias."},
            {"role": "user", "content": noticia[i]["conteudo"] + " Resuma esta notícia em aproximadamente 300 caracteres."}
        ]
        response = safe_api_call(openai.ChatCompletion.create, model="gpt-3.5-turbo", messages=messages, max_tokens=150)
        noticias_resumidas.append(response['choices'][0]['message']['content'].strip())
    return noticias_resumidas




def categoriza_noticia(noticia):
    openai.api_key = ''
    tipo_noticia = []
    for i in range(len(noticia)):
        messages = [
            {"role": "system", "content": "Você é um assistente que categoriza notícias."},
            {"role": "user", "content": noticia[i]["conteudo"] + " Categorize esta notícia em uma das seguintes categorias: Política, Economia, Esportes, Entretenimento, Mundo"}
        ]
        response = safe_api_call(openai.ChatCompletion.create, model="gpt-3.5-turbo", messages=messages, max_tokens=50)
        tipo_noticia.append(response['choices'][0]['message']['content'].strip())
    return tipo_noticia




def post_todas_noticias():
    noticias = get_g1_news()
    noticias_resumidas = resume_noticias(noticias)
    tipos_noticia = categoriza_noticia(noticias)

    for i in range(len(noticias)):
        post_noticias({
            "titulo": noticias[i]["titulo"],
            "conteudo": noticias_resumidas[i],
            "data": noticias[i]["data"],
            "tipo": tipos_noticia[i]
        })

    return {"mensagem": "todas as notícias foram postadas"}, 201