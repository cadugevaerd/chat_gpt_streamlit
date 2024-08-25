from Chat import tratar_nome

class TestClass:
    def test_quando_o_nome_precisa_ser_tratado(self):
        entrada = [{"role": "user", "content": "Carlos Eduardo"}] #given
        esperado = 'carlos_eduardo'
        resposta = tratar_nome(entrada) #when
        
        assert resposta == esperado