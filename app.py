from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
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
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(5)
    texto = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()
    return texto

def resumir_noticia(texto):
    openai.api_key = 'sua_chave_de_api_aqui'
    response = openai.Completion.create(
        engine="davinci",
        prompt=texto + "\nResuma a notícia em aproximadamente 800 caracteres:",
        max_tokens=100
    )
    return response.choices[0].text

if __name__ == '__main__':
    app.run(debug=True)