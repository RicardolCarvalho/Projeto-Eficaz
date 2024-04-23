from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import openai
from api_gpt import resumir_noticia
from get_g1 import get_g1_news

get_g1_news()
texto_noticia = "Texto completo da notícia"  
resumo = resumir_noticia(texto_noticia)
print("Resumo:", resumo)
