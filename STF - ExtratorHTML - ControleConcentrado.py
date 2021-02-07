import dsd
import requests

def solicitar_dados_Juris (classe, numero):
    url = ('http://www.stf.jus.br/portal/peticaoInicial/verPeticaoInicial.asp?base=' 
           + classe 
           + '&documento=&s1=1&numProcesso=' 
           + numero)
    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('processo/verProcessoAndamento.asp?')
    return (url + ">>>>> \n" + string[inicio:])

# Definição dos parâmetros de busca
Classe = "ADI"
NumeroInicial = 5000
NumeroFinal = 5050

# realiza a extração dos dados e a gravação    
for n in range (NumeroFinal-NumeroInicial+1):
    
    dsd.esperar(2,5,n)
    
    # define número do processo a ser buscado
    NumProcesso = str(NumeroFinal-n)
    
    # busca dados do processo definido por classe e número, no banco do CC
    dados = solicitar_dados_Juris (Classe, NumProcesso)
       
    # grava dados no arquivo definido
    dsd.gravar_dados_no_arquivo(Classe, NumProcesso,'ADIhtml//', dados)

