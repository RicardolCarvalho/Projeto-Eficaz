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

    st.title('Atualizar Notícias')


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
                    st.session_state['noticia'] = r.json()["noticias"]

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
                    update_response = rq.put(f'{URL}/noticia/{titulo_noticia}', json={
                        'titulo': novo_titulo,
                        'tipo': novo_tipo,
                        'conteudo': novo_conteudo
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