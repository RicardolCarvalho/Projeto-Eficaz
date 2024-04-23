import openai


def resumir_noticia(texto):
    openai.api_key = 'sua_chave_de_api_aqui'
    response = openai.Completion.create(
        engine="davinci",
        prompt=texto + "\nResuma a notícia em aproximadamente 800 caracteres:",
        max_tokens=100
    )
    return response.choices[0].text