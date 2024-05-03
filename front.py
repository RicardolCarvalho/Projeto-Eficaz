import streamlit as st
import requests as rq
from urllib.parse import urlencode

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
                        st.query_params['page'] = 'home'  # Redirecionar para a tela home
                        print('CWFEB,ERKOJNVWOQSVNEOBSWRINBOWRNOBLMWESAOVNMWEONBOW4TEK NBOEQN B OQWRNEBOEQWNBOWE OQN O')
                        break
                    else:
                        st.error('Senha inválida')
                        break
            else:
                st.error('CPF não encontrado')
                

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
            st.query_params['page'] = 'home'  # Redirecionar para a tela home após o sucesso do cadastro
            print('CWFEB,ERKOJNVWOQSVNEOBSWRINBOWRNOBLMWESAOVNMWEONBOW4TEK NBOEQN B OQWRNEBOEQWNBOWE OQN O')


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

#______________________________________________________

def home():
    r = rq.get(f'{URL}/noticias')  

    if r.status_code == 200:
        resposta_json = r.json()
        
        noticias = resposta_json["noticias"]

        tipos = list(set(noticia['tipo'] for noticia in noticias)) 
        tipo_selecionado = st.selectbox('Filtrar por tipo de notícia:', ['Todos'] + tipos)

        for noticia in noticias:
            if tipo_selecionado == 'Todos' or noticia['tipo'] == tipo_selecionado:
                st.title(noticia['titulo'])
                st.write(noticia['tipo'])
                st.write(noticia['conteudo'])
                st.write(noticia['data'])
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

if __name__ == "__main__":
    st.query_params['page'] = 'login'
    if 'page' in st.query_params:
        if st.query_params['page'] == 'login':
            tela_login()
        elif st.query_params['page'] == 'home':
            home()
    else:   
        tela_login()
    if 'token' in st.session_state:
        meus_usuarios()
        novo_usuario()
        dados_usuario()
        atualiza_noticias()
        edita_noticias()
        home()
    elif 'page' in st.query_params:
        if st.query_params['page'] == 'home':
            home()
