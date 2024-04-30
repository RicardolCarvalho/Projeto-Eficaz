import streamlit as st
import requests as rq

URL = "http://127.0.0.1:5000"  # Corrigi o formato da URL para incluir o protocolo HTTP

def tela_login():
    st.title("Login")
    opcao = st.radio("", ['Entrar', 'Cadastrar'])
    if opcao == 'Entrar':
        usuario_login()
    elif opcao == 'Cadastrar':
        novo_usuario()

def usuario_login():
    st.title("Entrar")
    cpf = st.text_input("CPF")
    senha = st.text_input("Senha", type="password")
    if st.button('Login'):
        r = rq.get(f'{URL}/usuarios')
        response_json = r.json()
        if r.status_code == 200:
            for usuario in response_json['usuarios']:
                if usuario['cpf'] == cpf:
                    if usuario['senha'] == senha:
                        st.success('Redirecionar para tela home')
                        break
                    else:
                        st.error('Senha inválida')
                        break
                else:
                    st.error('CPF não encontrado')
                    break
        
def meus_usuarios():
    st.title("Meus Usuários")
    r = rq.get(f'{URL}/usuarios')
    status = r.status_code
    if status == 200:
        st.table(r.json())

def novo_usuario():
    st.title("Cadastrar")
    cpf = st.text_input("CPF")
    email = st.text_input("Email")
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    if st.button('Criar Usuário'):
        r = rq.post(f'{URL}/usuarios', json={"cpf": cpf, "nome": nome, "email": email, "senha": senha})
        if r.status_code == 201:
            st.success('Redirecionar para tela home')
        
def dados_usuario():
    st.title("Dados Usuário")
    id = st.text_input('Id do usuário')
    if st.button('Buscar Usuário'):
        r = rq.get(f'{URL}/usuarios/{id}')
        st.table(r.json())
        st.session_state['Usuario'] = r.json()
    if 'Usuario' in st.session_state:
        cpf = st.text_input("CPF")
        email = st.text_input("Email")
        nome = st.text_input("Nome")
        senha = st.text_input("Senha", type="password")
        if st.button('Atualizar Usuário'):
            r = rq.put(f'{URL}/usuarios/{id}', json={"cpf": cpf, "nome": nome, "email": email, "senha": senha})
            if r.status_code == 200:
                st.success('Usuário atualizado com sucesso')
        if st.button('Apagar Usuário'):
            r = rq.delete(f'{URL}/usuarios/{id}')
            if r.status_code == 204:
                st.success('Usuário apagado com sucesso')

if __name__ == "__main__":
    tela_login()
    if 'token' in st.session_state:
        meus_usuarios()
        novo_usuario()
        dados_usuario()
