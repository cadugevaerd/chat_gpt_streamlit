from openai import OpenAI
import openai
import streamlit as st

def conecta_gpt(mensagens):
    #print(st.session_state["key"])
    try:
        client = OpenAI(api_key=st.session_state["key"])
        respostas = client.chat.completions.create(
            messages=[
            {"role": m["role"], "content": m["content"]}
            for m in mensagens
        ],
            model=st.session_state["openai_model"],
            temperature=0,
            stream=True,
        )
        return respostas
    except openai.APIConnectionError as e:
        st.write("Erro de conexão. Verifique sua chave.")
        return None
