import streamlit as st
import requests

st.session_state['page'] = st.session_state.get('page', 'Cadastro_usuario')
page = st.sidebar.selectbox("Menu", ["Cadastro_usuario", "Busca_usuario", "Meus_usuarios", "Cadastra_livro", "Busca_livro", "Meus_livros"])
if page != st.session_state['page']:
    st.session_state['page'] = page

if st.session_state['page'] == "Cadastro_usuario":
    st.title("Cadastro")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    cpf = st.text_input("CPF")
    if st.button("Cadastrar"):
        if '@' in email and '.com' in email:
            response = requests.post("http://asp3-gabarito-720a4403f44a.herokuapp.com/usuarios", json={"Usuario":{"cpf": cpf,"email": email,"nome": nome}})
            if response.status_code == 201:
                st.success("Cadastro efetuado com sucesso")
            else:
                st.error("Erro ao cadastrar")
        else:
            st.error("Email inválido")

elif st.session_state['page'] == "Busca_usuario":
    st.title("Busca")
    id = st.text_input("ID")
    if st.button("Buscar"):
        response = requests.get(f"http://asp3-gabarito-720a4403f44a.herokuapp.com/usuarios/{id}")
        if response.status_code == 200:
            st.session_state['data_u'] = response.json()
            st.table(response.json())            
        else:
            st.error("Erro ao buscar")

elif st.session_state['page'] == "Meus_usuarios":
    st.title("Meus usuários")
    response = requests.get("http://asp3-gabarito-720a4403f44a.herokuapp.com/usuarios")
    if response.status_code == 200:
        st.table(response.json())
    else:
        st.error("Erro ao buscar")

elif st.session_state['page'] == "Cadastra_livro":
    st.title("Cadastro de livro")
    titulo = st.text_input("Título")
    autor = st.text_input("Autor")
    ano = st.text_input("Ano")
    genero = st.text_input("Genero")
    if st.button("Cadastrar"):
        response = requests.post("http://asp3-gabarito-720a4403f44a.herokuapp.com/livros", json={"Livro":{"titulo": titulo,
        "autor": autor,"anopublicacao": ano,"genero": genero}})
        if response.status_code == 201:
            st.success("Cadastro efetuado com sucesso")
        else:
            st.error("Erro ao cadastrar")

elif st.session_state['page'] == "Busca_livro":
    st.title("Busca de livro")
    id = st.text_input("ID")
    if st.button("Buscar"):
        response = requests.get(f"http://asp3-gabarito-720a4403f44a.herokuapp.com/livros/{id}")
        if response.status_code == 200:
            st.session_state['data_l'] = response.json()
            st.table(response.json())
        else:
            st.error("Erro ao buscar")

elif st.session_state['page'] == "Meus_livros":
    st.title("Meus livros")
    response = requests.get("http://asp3-gabarito-720a4403f44a.herokuapp.com/livros")
    if response.status_code == 200:
        st.table(response.json())
    else:
        st.error("Erro ao buscar")

if 'data_l' in st.session_state and st.session_state['page'] == "Busca_livro":
    titulo = st.text_input("Título", value=st.session_state['data_l']['titulo'])
    autor = st.text_input("Autor", value=st.session_state['data_l']['autor'])
    ano = st.text_input("Ano", value=st.session_state['data_l']['anopublicacao'])
    genero = st.text_input("Gênero", value=st.session_state['data_l']['genero'])
    if st.button("Atualizar"):
        response = requests.put(f"http://asp3-gabarito-720a4403f44a.herokuapp.com/livros/{st.session_state['data_l']['id']}", json={"Livro":{"titulo": titulo,
        "autor": autor,"anopublicacao": ano,"genero": genero}})
        if response.status_code == 200:
            st.success("Livro atualizado com sucesso")
        else:
            st.error("Erro ao atualizar")
    if st.button("Deletar"):
        response = requests.delete(f"http://asp3-gabarito-720a4403f44a.herokuapp.com/livros/{st.session_state['data_l']['id']}")
        if response.status_code == 200:
            st.success("Livro deletado com sucesso")
        else:
            st.error("Erro ao deletar")

if 'data_u' in st.session_state and st.session_state['page'] == "Busca_usuario":
    nome = st.text_input("Nome", value=st.session_state['data_u']['nome'])
    email = st.text_input("Email", value=st.session_state['data_u']['email'])
    cpf = st.text_input("CPF", value=st.session_state['data_u']['cpf'])
    if st.button("Atualizar"):
        response = requests.put(f"http://asp3-gabarito-720a4403f44a.herokuapp.com/usuarios/{st.session_state['data_u']['id']}", json={"Usuario":{"cpf": cpf,"email": email,"nome": nome}})
        if response.status_code == 200:
            st.success("Usuário atualizado com sucesso")
        else:
            st.error("Erro ao atualizar")
    if st.button("Deletar"):
        response = requests.delete(f"http://asp3-gabarito-720a4403f44a.herokuapp.com/usuarios/{st.session_state['data_u']['id']}")
        if response.status_code == 200:
            st.success("Usuário deletado com sucesso")
        else:
            st.error("Erro ao deletar")