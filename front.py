import streamlit as st
import requests as rq

URL = "http://127.0.0.1:5000"

def tela_login():
    st.title("Tela Login")
    if st.button('Entrar'):
        usuario_login()
    if st.button('Cadastrar'):
        novo_usuario()

def usuario_login():
    st.title("Login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button('Login'):
        r = rq.post(f'{URL}/login', json={"email": email, "senha": senha})
        if r.status_code == 200:
            st.success('Login efetuado com sucesso')
            st.session_state['token'] = r.json()['token']
            st.session_state['usuario'] = r.json()['usuario']
        else:
            st.error('Email ou senha inválidos')

        
def meus_usuarios():
    st.title("Meus Usuários")
    r = rq.get(f'{URL}/usuarios')
    status = r.status_code
    if status == 200:
        st.table(r.json()["usuarios"])

def novo_usuario():
    st.title("Novo Usuário")
    cpf = st.text_input("CPF")
    email = st.text_input("Email")
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    if st.button('Cadastrar'):
        r = rq.post(f'{URL}/usuarios', json={"cpf": cpf, "nome": nome, "email": email, "senha": senha})
        if r.status_code == 201:
            st.success('Usuário cadastrado com sucesso')
        
def dados_usuario():
    st.title("Dados Usuário")
    id = st.text_input('Id do usuario')
    if st.button('Buscar Usuario'):
        r = rq.get(f'{URL}/usuarios/{id}')
        st.table(r.json())
        st.session_state['Usuario'] = r.json()
    if 'Usuario' in st.session_state:
        cpf = st.text_input("CPF")
        email = st.text_input("Email")
        nome = st.text_input("Nome")
        senha = st.text_input("Senha", type="password")
        if st.button('Atualizar Usuario'):
            r = rq.put(f'{URL}/usuarios/{id}', json={"cpf": cpf, "nome": nome, "email": email, "senha": senha})
            if r.status_code == 200:
                st.success('Usuário atualizado com sucesso')
        if st.button('Apagar Usuario'):
            r = rq.delete(f'{URL}/usuarios/{id}')
            if r.status_code == 204:
                st.success('Usuário apagado com sucesso')



def home():

    r = rq.get(f'{URL}/noticias')  

    if r.status_code == 200:
        resposta_json = r.json()
        
        noticias = resposta_json["noticias"]

        for noticia in noticias:
            st.title(noticia['titulo'])
            st.write ("\n")
            st.write ("\n")
            st.write(noticia['tipo'])
            st.write ("\n")
            st.write(noticia['conteudo'])
            st.write ("\n")
            st.write(noticia['data'])
            st.write("-------------------------------------------------")



def atualiza_noticias():

    st.button('Atualizar Notícias')

    if st.button('Atualizar Notícias'):
        r = rq.post(f'{URL}/noticias')  

        if r.status_code == 200 or 201:
            st.success('Notícias atualizadas com sucesso')

        else:
            st.error('Erro ao atualizar notícias')



def edita_noticias():
    st.title("Editar Notícias")
    id = st.text_input('Titulo da notícia')
    if st.button('Buscar Notícia'):
        r = rq.get(f'{URL}/noticia/{id}')
        st.session_state['Noticia'] = r.json()

    if 'Noticia' in st.session_state:
        titulo = st.text_input("Titulo")
        conteudo = st.text_input("Conteudo")
        tipo = st.text_input("Tipo")

        if st.button('Atualizar Notícia'):
            r = rq.put(f'{URL}/noticias/{id}', json={"titulo": titulo, "conteudo": conteudo, "tipo": tipo})

            if r.status_code == 200 or 204:
                st.success('Notícia atualizada com sucesso')

            else:
                st.error('Erro ao atualizar notícia')
        if st.button('Apagar Notícia'):
            r = rq.delete(f'{URL}/noticias/{id}')
            if r.status_code == 200 or 204:
                st.success('Usuário apagado com sucesso')
            else:
                st.error('Erro ao apagar notícia')



if __name__ == "__main__":
    st.sidebar.subheader("Menu")
    opcao = st.sidebar.radio("", ["Home", "Meus Usuários", "Novo Usuário", "Dados Usuário", "Atualizar Notícias", "Editar Notícias"])

    if opcao == "Home":
        home()
    elif opcao == "Meus Usuários":
        meus_usuarios()
    elif opcao == "Novo Usuário":
        novo_usuario()
    elif opcao == "Dados Usuário":
        dados_usuario()
    elif opcao == "Atualizar Notícias":
        atualiza_noticias()
    elif opcao == "Editar Notícias":
        edita_noticias()