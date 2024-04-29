import streamlit as st
import requests as rq

URL = ""

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
        st.table(r.json())

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



if __name__ == "__main__":
    st.sidebar.subheader("Menu")
    opcao = st.sidebar.radio("", ["Tela inicial", "Meus Usuários", "Novo Usuário", "Dados Usuário"])

    if opcao == "Tela inicial":
        tela_inicial()
    elif opcao == "Meus Usuários":
        meus_usuarios()
    elif opcao == "Novo Usuário":
        novo_usuario()
    elif opcao == "Dados Usuário":
        dados_usuario()