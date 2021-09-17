import dsd

# Definição dos parâmetros de busca
Classe = "ADI"
NumeroInicial = 1
NumeroFinal = 6596
dominio = 'http://portal.stf.jus.br/processos/'

#iterador para buscar os processos
for vezes in range (NumeroFinal-NumeroInicial+1):

    dsd.esperar(5,5,vezes)
    dsd.esperar(30,40,vezes)
    dsd.esperar(60,700,vezes)

    NumProcesso = str(NumeroFinal-vezes)
    print (Classe+NumProcesso)

    # Extração das informações
    html = dsd.solicitar_dados_AP(Classe, NumProcesso)

    # extrai campo incidente do html
    incidente = dsd.extrair(html,'id="incidente" value="', '">')

    # extrai dados dos URLs

    partes          = dsd.get_utf8(dominio +'abaPartes.asp?incidente='+ incidente)

    informacoes     = dsd.get_utf8(dominio +'abaPartes.asp?incidente='+ incidente)

    andamentos      = dsd.get_utf8(dominio + 'abaandamentos.asp?incidente='+incidente +'&imprimir=1')

    pauta           = dsd.get_utf8(dominio + 'abapautas.asp?incidente=' + incidente)

    sessao          = dsd.get_utf8(dominio + 'abasessao.asp?incidente=' + incidente)

    decisoes        = dsd.get_utf8(dominio + 'abadecisoes.asp?incidente=' + incidente)

    deslocamentos   = dsd.get_utf8(dominio + 'abadeslocamentos.asp?incidente=' + incidente)

    peticoes        = dsd.get_utf8(dominio + 'abapeticoes.asp?incidente=' + incidente)

    recursos         = dsd.get_utf8(dominio + 'abarecursos.asp?incidente=' + incidente)

    if (Classe == 'ADI'
        or Classe == 'ADPF'
        or Classe == 'ADO'
        or Classe == 'ADC'):
        cc = dsd.solicitar_dados_CC(Classe, NumProcesso)
    else:
        cc = 'NA'

    # define dados a serem gravados
    dados = ('incidente=' + incidente + 'fonte>>>>' +html +
             'partes>>>>' + partes + 'informacoes>>>>' + informacoes +
             'andamentos>>>>' + andamentos + 'pauta>>>>' + pauta +
             'sessao>>>>' + sessao + 'decisoes>>>>' + decisoes +
             'deslocamentos>>>>' + deslocamentos + 'peticoes>>>>' +
             peticoes + 'recursos>>>>' + recursos + 'cc>>>>' + cc)

    # função de gravação
    dsd.gravar_dados_no_arquivo (Classe, NumProcesso, 'ADItotal\\', dados)

    print (f'Gravado arquivo {Classe+NumProcesso}')
