import streamlit as st
import requests as rq
from urllib.parse import urlencode

URL = "http://127.0.0.1:5000"  

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
            usuario_encontrado = False
            for usuario in response_json['usuarios']:
                if usuario['cpf'] == cpf and usuario['senha'] == senha:
                    st.success('Login efetuado com sucesso')
                    st.session_state['cpf'] = cpf
                    st.session_state['role'] = usuario.get('role')
                    usuario_encontrado = True
                    break
            if usuario_encontrado:
                st.experimental_rerun()
            if not usuario_encontrado:
                st.error('CPF ou senha inválidos')

                

def meus_usuarios():
    st.title("Usuários")
    r = rq.get(f'{URL}/usuarios')
    status = r.status_code
    if status == 200:
        st.table(r.json()["usuarios"])

def novo_usuario():
    st.title("Cadastrar")
    cpf = st.text_input("CPF")
    email = st.text_input("Email")
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    if st.button('Criar Usuário'):
        r = rq.post(f'{URL}/usuarios', json={"cpf": cpf, "nome": nome, "email": email, "senha": senha})

        print (r)

        if r.status_code == 201 or 200:
            st.success('Usuário criado com sucesso')

def perfil():
    st.title("Perfil")
    cpf = st.session_state['cpf']
    r = rq.get(f'{URL}/usuarios/a/{cpf}')
    if r.status_code == 200:
        try:
            response_json = r.json()
        except ValueError:
            st.error('Erro ao decodificar resposta JSON.')
    else:
        st.error(f'Erro na requisição: {r.status_code}')
    if r.status_code == 200:
        st.session_state['Usuario'] = response_json
    if 'Usuario' in st.session_state:
        usuario = st.session_state['Usuario']
        cpf = st.text_input("CPF", value=usuario['cpf'])
        email = st.text_input("Email", value=usuario['email'])
        nome = st.text_input("Nome", value=usuario['nome'])
        senha = st.text_input("Senha", type="password", value=usuario['senha'])

        st.table(usuario)
        if st.button('Atualizar Usuário'):
            r = rq.put(f'{URL}/usuarios/{cpf}', json={"cpf": cpf, "nome": nome, "email": email, "senha": senha})
            if r.status_code == 200:
                st.success('Usuário atualizado com sucesso')
#______________________________________________________ 

def dados_usuario():
    st.title("Dados Usuário")
    id = st.text_input('ID do usuário')
    if st.button('Buscar Usuário'):
        r = rq.get(f'{URL}/usuarios/{id}')
        response_json = None
        if r.status_code == 200:
            try:
                response_json = r.json()
            except ValueError:
                st.error('Erro ao decodificar resposta JSON.')
        else:
            st.error(f'Erro na requisição: {r.status_code}')
        if r.status_code == 200:
            for usuario in response_json['usuarios']:
                if usuario['id'] == id:
                    st.session_state['Usuario'] = usuario
                    break
    if 'Usuario' in st.session_state:
        usuario = st.session_state['Usuario']
        cpf = st.text_input("CPF", value=usuario['cpf'])
        email = st.text_input("Email", value=usuario['email'])
        nome = st.text_input("Nome", value=usuario['nome'])
        senha = st.text_input("Senha", type="password", value=usuario['senha'])

        st.table(usuario)
        if st.button('Atualizar Usuário'):
            r = rq.put(f'{URL}/usuarios/{id}', json={"cpf": cpf, "nome": nome, "email": email, "senha": senha})
            if r.status_code == 200:
                st.success('Usuário atualizado com sucesso')
        if st.button('Apagar Usuário'):
            r = rq.delete(f'{URL}/usuarios/{id}')
            if r.status_code == 204:
                st.success('Usuário apagado com sucesso')

#______________________________________________________

def home():
    r = rq.get(f'{URL}/noticias')  

    if r.status_code == 200:
        resposta_json = r.json()
        
        noticias = resposta_json["noticias"]

        tipos = list(set(noticia['tipo'] for noticia in noticias)) 
        tipo_selecionado = st.selectbox('Filtrar por tipo de notícia:', ['Todos'] + tipos)

        portais = list(set(noticia['portal'] for noticia in noticias))
        portal_selecionado = st.selectbox('Filtrar por portal:', ['Todos'] + portais)

        for noticia in noticias:
            if tipo_selecionado == 'Todos' or noticia['tipo'] == tipo_selecionado:
                if portal_selecionado == 'Todos' or noticia['portal'] == portal_selecionado:
                    
                    st.title(noticia['titulo'])
                    st.write(noticia['tipo'])
                    st.write(noticia['conteudo'])
                    st.write(noticia['data'])
                    st.write(noticia["portal"])
                    st.write("-------------------------------------------------")

def atualiza_noticias():
    st.title('Atualizar Notícias Diárias')

    if st.button('Atualizar'):
        r = rq.post(f'{URL}/noticias')  

        if r.status_code == 200 or 201:
            st.success('Notícias atualizadas com sucesso')
        else:
            st.error('Erro ao atualizar notícias')

def edita_noticias():
    st.title('Editar Notícias')
    
    if 'noticia' not in st.session_state:
        st.session_state['noticia'] = None
    
    titulo_noticia = st.text_input('Título da notícia', key='titulo_noticia')

    if st.button('Buscar'):
        if titulo_noticia:
            try:
                r = rq.get(f'{URL}/noticias/{titulo_noticia}')
                if r.status_code == 200:
                    st.session_state['noticia'] = r.json()

                else:
                    st.error('Notícia não encontrada.')
                    st.session_state['noticia'] = None
            except Exception as e:
                st.error(f'Erro ao buscar notícia: {e}')
                st.session_state['noticia'] = None

    if st.session_state['noticia']:
        with st.form("form_atualizar_noticia"):
       
            novo_titulo = st.text_input('Título', value=st.session_state['noticia']['titulo'])
            novo_tipo = st.text_input('Tipo', value=st.session_state['noticia']['tipo'])
            novo_conteudo = st.text_area('Conteúdo', value=st.session_state['noticia']['conteudo'])

            atualizar_button = st.form_submit_button('Atualizar Notícia')
            
            if atualizar_button:
                try:
                    update_response = rq.put(f'{URL}/noticias/{titulo_noticia}', json={
                        'titulo': novo_titulo,
                        'tipo': novo_tipo,
                        'conteudo': novo_conteudo, 
                    })

                    if update_response.status_code in [200, 204]:
                        st.success('Notícia atualizada com sucesso!')
        
                        st.session_state['noticia']['titulo'] = novo_titulo
                        st.session_state['noticia']['conteudo'] = novo_conteudo
                        st.session_state['noticia']['tipo'] = novo_tipo
                    else:
                        st.error('Falha ao atualizar notícia.')
                except Exception as e:
                    st.error(f'Erro ao atualizar notícia: {e}')

        if st.button('Remover Notícia'):
            try:
                
                delete_response = rq.delete(f'{URL}/noticias/{titulo_noticia}')

                if delete_response.status_code in [200, 204]:
                    st.success('Notícia removida com sucesso!')
                    st.session_state['noticia'] = None
                
                else:
                    st.error('Falha ao remover notícia.')

            except Exception as e:
                st.error(f'Erro ao remover notícia: {e}')



st.sidebar.title("Menu")

if 'role' not in st.session_state:
    page = st.sidebar.radio("", ('Home', "Login"))
else:
    if st.session_state['role'] == 'admin':
        page = st.sidebar.radio("", ('Home', "Usuários", "Dados Usuários","Editar Notícias", "Atualizar Notícias", "Perfil"))

    elif st.session_state['role'] == 'user':
        page = st.sidebar.radio("", ('Home', "Perfil"))
    else:
        page = st.sidebar.radio("", ('Home', "Login"))

if page == 'Home':
    home()
elif page == 'Login':
    if 'role' not in st.session_state:
        tela_login()
elif page == 'Usuários':
    if st.session_state['role'] == 'admin':
        meus_usuarios()
elif page == 'Editar Notícias':
    if st.session_state['role'] == 'admin':
        edita_noticias()
elif page == 'Atualizar Notícias':
    if st.session_state['role'] == 'admin':
        atualiza_noticias()
elif page == 'Dados Usuários':
    if st.session_state['role'] == 'admin':
        dados_usuario()
elif page == 'Perfil':
    if st.session_state['role'] == 'user' or 'admin':
        perfil()