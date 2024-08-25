from unidecode import unidecode
import re

class Tratamentos:
    def __init__(self) -> None:
        pass
    def tratar_nome(self,mensagem):
        nome = self.get_nome_mensagens(mensagem)
        nome = nome.replace(" ", "_")
        nome = unidecode(nome)
        nome = re.sub(r'\W+','', nome).lower()
        return nome

    def get_nome_mensagens(self,mensagens):
        nova_mensagem = ""
        for mensagem in mensagens:
            if mensagem['role'] == 'user':
                nova_mensagem = mensagem['content'][:30]
                break
        return nova_mensagem