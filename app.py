from flask import Flask, render_template, request
import selenium
import openai

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resumo', methods=['POST'])
def resumo():
    url_noticia = request.form['url_noticia']
    texto_noticia = coletar_texto_noticia(url_noticia)  
    texto_resumido = resumir_noticia(texto_noticia)   
    return render_template('home.html', texto_resumido=texto_resumido)

def coletar_texto_noticia(url):
    # Implementação do Selenium para extrair texto de notícia
    pass

def resumir_noticia(texto):
    # Implementação da API do ChatGPT para resumir texto
    pass

if __name__ == '__main__':
    app.run(debug=True)
