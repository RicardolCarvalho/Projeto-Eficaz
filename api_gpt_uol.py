from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import requests
from selenium.common.exceptions import TimeoutException
import time
import json
from api_gpt_g1 import post_noticias

lista_css = ['#app > div > div:nth-child(7) > section:nth-child(2) > div > div > div:nth-child(1) > div > div.col-24.col-lg-15 > article > a',
             '#app > div > div:nth-child(7) > section:nth-child(2) > div > div > div:nth-child(1) > div > div.col-24.col-lg-15 > div.section__grid__main__rows > div > div > div > div.col-24.col-lg-16 > div > div.col-24.col-lg-12.sectionGrid__grid__columnOne > article:nth-child(1) > a',
             '#app > div > div:nth-child(7) > section:nth-child(2) > div > div > div:nth-child(1) > div > div.col-24.col-lg-15 > div.section__grid__main__rows > div > div > div > div.col-24.col-lg-16 > div > div.col-24.col-lg-12.sectionGrid__grid__columnTwo > article:nth-child(1) > a',
             '#app > div > div:nth-child(7) > section:nth-child(2) > div > div > div:nth-child(1) > div > div.col-24.col-lg-15 > div.section__grid__main__rows > div > div > div > div.col-24.col-lg-8.sectionGrid__grid__columnThree > article:nth-child(1) > a',
             '#app > div > div:nth-child(7) > section:nth-child(2) > div > div > div:nth-child(1) > div > div.col-24.col-lg-15 > div.section__grid__main__rows > div > div > div > div.col-24.col-lg-16 > div > div.col-24.col-lg-12.sectionGrid__grid__columnOne > article:nth-child(2) > a',
             '#app > div > div:nth-child(7) > section:nth-child(2) > div > div > div:nth-child(1) > div > div.col-24.col-lg-15 > div.section__grid__main__rows > div > div > div > div.col-24.col-lg-16 > div > div.col-24.col-lg-12.sectionGrid__grid__columnTwo > article:nth-child(2) > a',
             '#app > div > div:nth-child(7) > section:nth-child(2) > div > div > div:nth-child(1) > div > div.col-24.col-lg-15 > div.section__grid__main__rows > div > div > div > div.col-24.col-lg-8.sectionGrid__grid__columnThree > article:nth-child(2) > a',
]

def busca_noticias(lista_css):
    # Configuração do Selenium para buscar notícias
    s = Service('chromedriver.exe')
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=s, options=options)
    wait = WebDriverWait(driver, 10)
    lista_textos = []
    
    try:
        for news in lista_css:
            try:  # Limitando para o primeiro seletor para teste
                driver.get('https://www.uol.com.br/')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                noticia_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'{news}')))
                noticia_url = noticia_link.get_attribute('href')

                if noticia_url:
                    driver.get('https://leiaisso.net/')
                    input_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#i')))
                    input_field.send_keys(noticia_url)
                    submit_button = driver.find_element(By.CSS_SELECTOR, '#read-this > input.bt.mb1')
                    submit_button.click()
                    processed_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#post')))
                    processed_text = processed_text.text
                    lista_textos.append(processed_text)
            except TimeoutException:
                print(f"Elemento não encontrado com o seletor: {news}. Ignorando e continuando...")
                continue
    finally:
        driver.quit()

    return lista_textos

def processar_textos(lista_textos):

    session = requests.Session()
    id_modelo = 'gpt-3.5-turbo'
    link = 'https://api.openai.com/v1/chat/completions'
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resultados_finais = []

    for idx, texto in enumerate(lista_textos):
        retry_attempts = 3
        while retry_attempts > 0:
            body_mensagem = {
                "model": id_modelo,
                "messages": [{
                    "role": "user",
                    "content": f"Vou te dar quatro comandos, o primeiro é dar um título para a notícia, "
                               f"o segundo é resumir a notícia em até 400 caracteres, o terceiro é encontrar a data "
                               f"e o quarto é me falar em qual gênero você acha que a notícia mais se identifica entre apenas "
                               f"(política, economia, esportes, entretenimento, mundo, saúde, cidade): {texto}"
                               "Quero que a resposta seja um json {'titulo':, 'resumo':, 'data':, 'genero':}"
                }]
            }
            resposta = session.post(link, json=body_mensagem, headers=headers)
            if resposta.status_code == 200:
                dados_resposta = resposta.json()
                resposta_texto = dados_resposta.get('choices', [{}])[0].get('message', {}).get('content', '').replace('\n', '')
                try:
                    resultado = json.loads(resposta_texto)
                    resultados_finais.append(resultado)  # Adiciona o resultado como um dicionário na lista
                except json.JSONDecodeError:
                    resultados_finais.append({'Erro': 'Falha ao decodificar a resposta JSON'})
                break
            elif resposta.status_code == 429:
                time.sleep(20)  # Espera recomendada pela mensagem de erro
                retry_attempts -= 1
            else:
                resultados_finais.append({'Erro': f"Erro ao processar o texto: {resposta.status_code} {resposta.text}"})
                break

    return resultados_finais


# print(processar_textos(busca_noticias(lista_css)))

def post_todas_noticias_2():
    resultados = processar_textos(busca_noticias(lista_css))
    for i in range(len(resultados)):
        post_noticias({
            "titulo":  resultados[i]["titulo"],
            "conteudo": resultados[i]["resumo"],
            "data": resultados[i]["data"],
            "tipo": resultados[i]["genero"],
            "portal" : "UOL"
        })

    return {"mensagem": "todas as notícias foram postadas"}, 201