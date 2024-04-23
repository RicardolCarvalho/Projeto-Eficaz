from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuração do driver do Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Acessando o site G1
driver.get("https://g1.globo.com/")

# Espera para garantir que a página seja carregada
time.sleep(5)

# Encontrando os elementos que contêm as notícias
noticias = driver.find_elements(By.CSS_SELECTOR, "a.feed-post-link")

# Lista para armazenar as notícias
lista_de_noticias = []

# Coletando as notícias
for noticia in noticias:
    titulo = noticia.text
    link = noticia.get_attribute('href')
    lista_de_noticias.append((titulo, link))

# Imprimindo as notícias
for titulo, link in lista_de_noticias:
    print(f"Título: {titulo}\nLink: {link}\n")

# Fechando o navegador
driver.quit()