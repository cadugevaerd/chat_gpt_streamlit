import streamlit as st
import openai_chat as conecta_gpt
import json
import os
import os
import pickle
from cachetools import cached
from cachetools.keys import hashkey
from app.models.tratamentos import Tratamentos


PATH_CONFIGS = os.getcwd() + 'app/database/'
if not os.path.exists(PATH_CONFIGS):
    os.mkdir(PATH_CONFIGS)
def custom_key(*args, **kwargs):
    def convert_to_tuple(x):
        if isinstance(x, list):
            return tuple(convert_to_tuple(i) for i in x)
        if isinstance(x, dict):
            return {k: convert_to_tuple(v) for k, v in x.items()}
        return x

    args = tuple(convert_to_tuple(arg) for arg in args)
    kwargs = {k: convert_to_tuple(v) for k, v in kwargs.items()}
    return hashkey(args, frozenset(kwargs.items()))

@cached(cache={}, key=custom_key)
def carregar_confs():
    if os.path.exists(os.path.join('database', 'config.json')):
        with open(os.path.join('database', 'config.json'), 'r') as f:
            data = json.load(f)
        return data
    else:
        return None

def gera_resp_gpt(response):
    with st.chat_message("ai"):
        response = gpt.conecta_gpt(response)
        resposta = st.write_stream(response)
        resposta = {"role": "assistant", "content": resposta}
        #st.write(resposta)
    return resposta

def salvar_mensagens(mensagens):
        if len(mensagens) == 0:
            return []
        tratamentos = Tratamentos()
        nome = tratamentos.tratar_nome(mensagens)
        arquivo = {
            'nome': nome,
            'conversa': mensagens
        }
        with open(os.path.join(PATH_CONFIGS, f'{nome}.pkl'), "wb") as f:
            pickle.dump(arquivo, f)

def ler_mensagens(mensagens):
    
    if len(mensagens) == 1:
        return mensagens
    tratamentos = Tratamentos()
    nome = tratamentos.tratar_nome(mensagens)
    with open(os.path.join(PATH_CONFIGS, f'{nome}.pkl'), "rb") as f:
        mensagens = pickle.load(f)
    return mensagens

def inicia_chat():
    prompt = "Contexto: O seu Nome é Oriom. você foi desenvolvido para ser um chat bot inteligente. e ajudar as pessoas naquilo que elas gostariam de saber. \
            Objetivo: Ajudar as pessoas a pssuir respostas de forma inteligente. Responda 'Não tenho certeza sobre a resposta' se não tiver certeza da resposta."

    st.session_state['chat'] = [{'role': 'system', 'content': prompt}]
    messages = st.session_state['chat']
    return messages

def pagina_principal():
    st.title("🤖 ChatBot GPT - Orion")
    st.divider()
    config = carregar_confs()
    if config is not None:
        st.session_state['key'] = config['key']
        st.session_state['openai_model'] = config['model']
    if 'key' not in st.session_state:
        chat = st.chat_message("assistant")
        chat.markdown("Olá, meu nome é Orion, antes de iniciarmos uma conversa insira uma API Key Válida!")
        return False
    if 'chat' not in st.session_state:
        messages = inicia_chat()
    else:
        messages = ler_mensagens(st.session_state['chat'])
        if 'conversa' in messages:
            messages = messages['conversa']
    for message in messages:
        if message['role'] != 'system':
            chat = st.chat_message(message['role'])
            chat.markdown(message['content'])
    prompt = st.chat_input("Prompt:")
    if prompt:
        messages.append({'role': 'user', 'content': prompt})
        chat = st.chat_message('user')
        chat.markdown(prompt)
        chat_resp = gera_resp_gpt(messages)
        messages.append(chat_resp)
        st.session_state['chat'] = messages
        return True
    #st.write(config)
    #if response == "GPT-3.5":

@cached(cache={}, key=custom_key)
def seleciona_conversa(nome_conversa):
    if nome_conversa == '':
        st.session_state['chat'] = inicia_chat()
    else:
        arquivos = coleta_arquivos()['arquivos']
        
        for arquivo in arquivos:
            if arquivo.split('.')[0].lower() == nome_conversa:
                with open(os.path.join(PATH_CONFIGS, arquivo), "rb") as f:
                    mensagens = pickle.load(f)
                st.session_state['chat'] = mensagens['conversa']
                st.session_state['conversa_atual'] = nome_conversa
                
@cached(cache={}, key=custom_key)
def coleta_arquivos():
    arquivos = []
    for file in os.listdir(PATH_CONFIGS):
        if file.split('.')[1] == 'pkl':
            arquivos.append(file)
    arquivos = sorted(arquivos, key=lambda x: os.path.getmtime(os.path.join(PATH_CONFIGS, x)), reverse=True)
    return {'arquivos': arquivos} #retorna apenas os arquivos

@cached(cache={}, key=custom_key)
def listar_conversas():
    arquivos = coleta_arquivos()['arquivos']
    arquivos_retorno = []
    for file in arquivos:
        with open (os.path.join(PATH_CONFIGS, file),'rb') as f:
            conversa = pickle.load(f)
        arquivos_retorno.append(conversa['nome'])
        
    return {'conversas': arquivos_retorno}
    
def conversas():
    st.sidebar.button("➕ Nova conversa",
                      on_click=seleciona_conversa,
                      args=('',),
                      use_container_width=True)
    st.sidebar.markdown('')
    conversas_list = listar_conversas()['conversas']
    for conversa in conversas_list:
        conversa_temp = conversa.replace('_', ' ')
        if len(conversa_temp) >= 30:
            conversa_temp += '...'
        conversa_temp = conversa_temp.capitalize()
        st.sidebar.button(conversa_temp, on_click=seleciona_conversa, args=(conversa,), use_container_width=True,disabled=conversa == st.session_state['conversa_atual'])

def inicializar():
    if 'conversa_atual' not in st.session_state:
        st.session_state['conversa_atual'] = ''

if __name__ == "__main__":
    inicializar()
    
    retorno = pagina_principal()
    conversas()
    if retorno:
        salvar_mensagens(st.session_state['chat'])
