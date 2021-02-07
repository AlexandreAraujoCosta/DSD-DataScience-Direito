import dsd

# Definição dos parâmetros de busca
Classe = "ADI"
NumeroInicial = 5500
NumeroFinal = 6000

# Definição do diretório para gravar os dados
path = 'STFADIhtml//'

# realiza a extração dos dados e a gravação    
for n in range(NumeroFinal-NumeroInicial):
    
    # define número do processo a ser buscado
    NumProcesso = str(NumeroFinal-n)
    print(NumProcesso)
    
    # busca dados do processo definido por classe e número, no banco do CC
    dados = dsd.solicitar_dados_CC (Classe, NumProcesso)
       
    # grava dados no arquivo definido
    dsd.gravar_dados_no_arquivo(Classe, NumProcesso, path, dados)