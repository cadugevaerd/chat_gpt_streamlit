import streamlit as st
import os
import json

database = "database/config.json"
def coleta_keys():
    if os.path.exists(database):
        with open(database, "r") as f:
            data = json.load(f)
        if "key" in data:
            key = data["key"]
            st.session_state["key"] = key
            st.text_input("",value=key,type="password")
    else:
        key = st.text_input("",type="password")
    return key

def gpt_model():
    st.markdown("## Escolha o modelo GPT:")
    response = st.selectbox("",["GPT-3.5","GPT-4o","GPT-4"],index=0)
    if response == "GPT-3.5":
        st.session_state["openai_model"] = "gpt-3.5-turbo-0125"
    elif response == "GPT-4o":
        st.session_state["openai_model"] = "gpt-4o"
    else:
        st.session_state["openai_model"] = "gpt-4-turbo"

if __name__ == "__main__":
    st.title("⚙️ Configurações GPT")
    st.divider()
    st.markdown("## Chave chat GPT:")
    key = coleta_keys()
    gpt_model()
    if st.button("Salvar"):
        st.session_state["key"] = key
        data = {
            "key" : key,
            "model" : st.session_state["openai_model"]
        }
        with open(database, "w+") as f:
            f.write(json.dumps(data))
        st.success("dados salvos com sucesso!")
    
    