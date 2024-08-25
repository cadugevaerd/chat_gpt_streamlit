from app.models.tratamentos import Tratamentos

class TestClass:
    def test_quando_o_nome_precisa_ser_tratado(self):
        entrada = [{"role": "user", "content": "Carlos Eduardo"}] #given
        esperado = 'carlos_eduardo'
        item = Tratamentos()
        resposta = item.tratar_nome(entrada) #when
        
        assert resposta == esperado