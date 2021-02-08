import csv
import requests
import time
import os
from unicodedata import normalize

#biblioteca de funções
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8')

def extrair(fonte,MarcadorInicio, MarcadorFim):
    inicio = fonte.find(MarcadorInicio)
    if inicio == -1:
        return 'NA'
    else:
        inicio = inicio + len(MarcadorInicio)
        fim = fonte.find(MarcadorFim, inicio)
        if  MarcadorFim == '' or fim == -1:
            return fonte[inicio:]
        elif MarcadorInicio == '':
            return fonte[:fim]
        else:
            return fonte[inicio:fim]

def extrair_campo_lista (string, split, lista_inicio_fim):
    # define o número de elementos a serem extraídos
    n_elementos= string.count(split)

    # cria uma lista (dados) com os dados da string, segmentada no split
    elementos = string.split(split)
    elementos = elementos[1:]

    # imprime o número de elementos a serem extraídos
    # print (str(n_elementos) + ' elementos')

    #define a lista que será retornada como resultado
    campo_lista = []

    # iteração sobre cada um dos n elementos
    for item in range(n_elementos):

        # carrega na variável campo um elemento de cada vez
        campo = elementos[item]
        # print (campo)
        # redefine a lista elemento_lista
        elemento_lista = []

        # insere no elemento o número de ordem, iniciando em 1
        elemento_lista.append(['ORDEM', str(item+1)])

        # identifica os atributos de cada elemento
        for elemento in range(len(lista_inicio_fim)):
            # extrai os marcadores da lista
            marcadores = lista_inicio_fim[elemento]
            atributo = marcadores[0].upper()
            inicio = marcadores[1]
            fim = marcadores[2]

            # extrai o atributo a partir dos marcadores
            dado = ''
            dado = extrair(campo, inicio, fim)
            dado = limpar(dado)
            dado = limpar2(dado)
            dado = remover_acentos(dado)

            elemento_lista.append([atributo, dado.upper()])
        # acrescenta o elemento extraído na lista que compõe o campo
        campo_lista.append(elemento_lista)

    # retorna a lista de elementos como resultado função
    return campo_lista


def solicitar_dados_Juris (classe, numero):
    url = ('http://stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28'
           + classe
           +'%24%2ESCLA%2E+E+'
           + numero
           + '%2ENUME%2E%29+OU+%28'
           + classe +
           ' %2EACMS%2E+ADJ2+'
           + numero
           + '%2EACMS%2E%29&base=baseAcordaos')

    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('<a href="#" id="imprimir" onclick="sysImprimir(); return false;">Imprimir</a>')
    return (url + ">>>>> \n" + string[inicio:])

def solicitar_dados_CC (classe, numero):
    url = ('http://www.stf.jus.br/portal/peticaoInicial/verPeticaoInicial.asp?base='
           + classe
           + '&documento=&s1=1&numProcesso='
           + numero)
    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('processo/verProcessoAndamento.asp?')
    return (url + ">>>>> \n" + string[inicio:])

def solicitar_dados_mono (classe, numero):
    url = ('http://stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28'
           + classe
           +'%24%2ESCLA%2E+E+'
           + numero
           + '%2ENUME%2E%29+NAO+S%2EPRES%2E&base=baseMonocraticas')

    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('<a href="#" id="imprimir" onclick="sysImprimir(); return false;">Imprimir</a>')
    return (url + ">>>>> \n" + string[inicio:])

def solicitar_dados_AP (classe, numero):
    url = ('http://portal.stf.jus.br/processos/listarProcessos.asp?classe='
           + classe
           + '&numeroProcesso='
           + numero)
    string = requests.get(url)
    string.encoding = 'utf-8'
    htmlfonte = string.text
    htmlfonte = extrair(htmlfonte,
                        '<div class="processo-titulo m-b-8">',
                        '<div class="p-l-0" id="resumo-partes">')
    return (url + ">>>>> \n" + htmlfonte)

def solicitar_utf8 (dominio, path, query):
    html = requests.get(dominio+path+query)
    html.encoding = 'utf-8'
    html = html.text
    return html


def carregar_arquivo (classe, numero, path):
    nomedoarquivo = (path + classe + str(0)*(4-len(numero)) + numero + '.html')
    arquivoaberto = (classe +  str(0)*(4-len(numero)) + numero + '.html')
    print (nomedoarquivo)
    arquivo = open(nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return arquivoaberto, html

def carregar_arquivo_nome (nome, path):
    nomedoarquivo = (nome)
    arquivo = open(path + nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return html

def gravar_dados_no_arquivo (classe, numero, path, dados):
    nomedoarquivo = (path + classe + str(0)*(4-len(numero)) + numero + '.html')
    arquivo = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivo.write(dados)
    arquivo.close

def gravar_dados_no_arquivo_nome (nomedoarquivo, dados):
    arquivo = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivo.write(dados)
    arquivo.close

def extrair_da_lista (relacao_de_arquivos, path):
    nomedoarquivo = relacao_de_arquivos.pop()
    arquivo = open(path + nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return nomedoarquivo, html

#   funções de limpeza
def limpar(fonte): # útil para textos em LN. retira parágrafos iniciais e converte quebras de linha em '//'
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip('\n')
    fonte = fonte.lstrip('\n')
    fonte = fonte.lstrip('\n')
    fonte = fonte.lstrip('\n')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip('\n')
    fonte = fonte.lstrip('\n')
    fonte = fonte.lstrip('\n')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip('"')
    fonte = fonte.lstrip('>')
    fonte = fonte.replace('\n','//')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('\t', '')
    fonte = fonte.replace('/#','')
    return fonte

def limpar2(fonte): #útil para campos com início com espaços. exclui quebras de linha.
    fonte = fonte.replace('\n','')
    fonte = fonte.replace('/#','')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip('-')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip('\t')
    return fonte

def limpar_decisao (string):
    string = string.replace('\n','')
    string = string.replace('\t','')
    string = string.replace('     ','')
    string = string.replace('  ',' ')
    string = string.upper()
    string = remover_acentos(string)
    return string

def write_csv_header (nomedoarquivo,campos,variavel0):
    if variavel0 == 0:
        arquivoaberto = open(nomedoarquivo, mode='w',
                             encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
        arquivoaberto_csv.writerow(campos.split(','))
        arquivoaberto.close()


def esperar (segundos, ciclos, variavel0):
    if variavel0%ciclos == 0 and variavel0 != 0:
        print ('espera ' + str(variavel0))
        time.sleep(segundos)


def write_csv_line (nomedoarquivo,dados):
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+',
                             encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
        arquivoaberto_csv.writerow(dados)
        arquivoaberto.close()

def write_csv_lines (nomedoarquivo, dados):
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+',
                             encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
        for item in range(len(dados)):
            arquivoaberto_csv.writerow(dados.pop(0))
        arquivoaberto.close()

def extrai_acordaos_da_string (arquivo_a_extrair, path):  # usar duas contra-barras depois do nome

    if arquivo_a_extrair in os.listdir(path):

        acordaos = carregar_arquivo_nome (arquivo_a_extrair, path)
        # print (arquivo_a_extrair)

        n_acordaos = extrair(acordaos,'Documentos encontrados: ','</td>')
        acordaos_publicados = []

        adi_decisao = 'NA'
        acordaos_publicados = []
        acordaos_adi = []
        acordaos_agr = []
        acordaos_emb = []
        acordaos_qo = []
        acordaos_outros = []

        if "Nenhum registro encontrado" in acordaos:
            decisao_colegiada = []

        else:
            decisao_colegiada = []

            for decisoes in range (int(n_acordaos)):


                acordaos_adi    = []
                acordaos_emb    = []
                acordaos_agr    = []
                acordaos_qo     = []
                acordaos_outros = []
                lista_processos_citados = []
                lista_procesoss_citados_com_tema = []
                acordao_tipo = 'NA'
                processo_juris = 'NA'
                relator_juris = 'NA'
                data_acordao = 'NA'
                orgao_julgador_acordao = 'NA'
                publicacao_acordao = 'NA'
                ementa = 'NA'
                decisao_juris = 'NA'
                legislacao = 'NA'
                observacao = 'NA'
                doutrina = 'NA'

                acordaos = acordaos.replace ('/n/n','/n')
                acordaos = acordaos.replace ('/t','')


                processo_juris = extrair(acordaos,'''<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --''', '<br />').upper()
                processo_juris = processo_juris.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                processo_juris = processo_juris.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                if 'ADI' in arquivo_a_extrair:
                    processo_juris = processo_juris.replace('AÇÃO DECLARATÓRIA DE CONSTITUCIONALIDADE', 'ADI')
                processo_juris = processo_juris.replace('MEDIDA CAUTELAR', 'MC')
                processo_juris = processo_juris.replace('\n', '')
                processo_juris = processo_juris.replace('\t', '')
                processo_juris = processo_juris.replace('>', '')
                processo_juris = processo_juris.replace('REFERENDO NA MC','MC (REFERENDO)')
                processo_juris = processo_juris.replace('REFERENDO NOS EMB.DECL.','EMB.DECL. (REFERENDO)')
                processo_juris = processo_juris.replace('REFERENDO NO AG.REG.','AG.REG (REFERENDO)')
                processo_juris = processo_juris.replace('SEGUNDOS ','')
                processo_juris = processo_juris.replace('SEGUNDO','')
                processo_juris = processo_juris.replace('TERCEIROS','')

                acordao_tipo = 'NA'

                if processo_juris[0:3] == "MC ":
                    acordao_tipo = "MC"
                elif processo_juris[0:3] == "EMB":
                    acordao_tipo = 'EMBARGOS'
                elif processo_juris[0:2] == "AG":
                    acordao_tipo = 'AGRAVO'
                elif processo_juris[0:3] == "QUE":
                    acordao_tipo = 'QO'
                elif processo_juris[0:3] == "ADI":
                    acordao_tipo = 'PRINCIPAL'
                else:
                    acordao_tipo = 'OUTROS'


                relator_juris = extrair(acordaos, 'Relator(a):&nbsp ', '<br />').upper()
                relator_juris = relator_juris.lstrip(' ')
                relator_juris = relator_juris.lstrip('MIN.')
                relator_juris = relator_juris.lstrip(' ')
                relator_juris = remover_acentos(relator_juris)

                data_acordao = extrair(acordaos, 'Julgamento:&nbsp', '&nbsp')
                data_acordao = data_acordao.replace('\t','')

                orgao_julgador_acordao = extrair(acordaos, 'Órgão Julgador:&nbsp', '<br />')

                publicacao_acordao = extrair (acordaos, '''<PRE><span style='font-family:tahoma, verdana, arial, sans-serif;font-size:1.1 em;font-weight:bold'>''', '</PRE>')

                ementa = extrair (acordaos, '''<p><div style="line-height: 150%;text-align: justify;">''', '</div>')

                decisao_juris = extrair (acordaos, '''<p><div style="text-align:justify; color: #385260; font-weight: normal; font-size: 11px">''', '</div>')

                legislacao = extrair (acordaos, '''Legislação</strong></p>''', '</PRE>')
                legislacao = legislacao.replace('\t','')
                legislacao = legislacao.replace('\n','')

                observacao =  extrair (acordaos, '''<p><strong>Observação</strong></p>''', '</PRE>')
                if 'Acórdão(s) citado(s)' in acordaos and 'Nenhum registro encontrado' not in acordaos and 'AGUARDANDO INDEXAÇÃO' not in acordaos:
                    observacao = observacao.replace ('(s)','')
                    observacao = observacao.replace ('(2ªT)','')
                    observacao = observacao.replace ('(1ªT)','')
                    observacao = observacao.replace ('(TP)','')
                    n_cit = observacao.count('href')
                    for links in range (n_cit):
                        inicio = observacao.find ('href')
                        fim = observacao.find ('>',inicio)
                        retirar = observacao[inicio:fim]
                        observacao = observacao.replace(retirar,'')

                    observacao = observacao.replace('\n','')
                    observacao = observacao.replace('<a>','')
                    observacao = observacao.replace('<a >','')
                    observacao = observacao.replace('</a>','')
                    observacao = observacao.replace(' ,',',')
                    observacao = observacao.replace(' .','.')
                    observacao = observacao.replace('.','')


                    observacao = observacao.split('(')[1:]
                    if  observacao != [] and 'Número de páginas' in observacao[-1]:
                        observacao[-1] = extrair (observacao[-1],'','Número de páginas')
                    lista_processos_citados = []
                    lista_procesoss_citados_com_tema = []
                    for obs in range (len(observacao)):
                        elemento = observacao[obs]
                        elemento = elemento.split(')')
                        tema = [elemento.pop(0)]
                        elemento = str(elemento).split(',')
                        for item in range (len(elemento)):
                            processo_citado = elemento[item]
                            processo_citado = processo_citado.lstrip('[')
                            processo_citado = processo_citado.lstrip("]")
                            processo_citado = processo_citado.lstrip(' ')
                            processo_citado = processo_citado.lstrip("'")

                            processo_citado_e_tema = processo_citado + ',' + str(tema)
                            lista_processos_citados.append(processo_citado)
                            lista_procesoss_citados_com_tema.append(processo_citado_e_tema)


                doutrina = extrair(acordaos, '''<p><strong>Doutrina</strong></p>''', '</PRE>')



                decisao_colegiada = [arquivo_a_extrair, acordao_tipo, processo_juris, relator_juris, data_acordao, orgao_julgador_acordao, publicacao_acordao, ementa, decisao_juris, legislacao, observacao, lista_processos_citados, lista_procesoss_citados_com_tema, doutrina]
                # print (decisao_colegiada)

                acordaos_publicados.append(decisao_colegiada)
                if acordao_tipo == 'PRINCIPAL':
                    acordaos_adi.append(decisao_colegiada)
                    adi_decisao = decisao_juris
                if acordao_tipo == 'EMB':
                    acordaos_emb.append(decisao_colegiada)
                if acordao_tipo == 'AGR':
                    acordaos_agr.append(decisao_colegiada)
                if acordao_tipo == 'QO':
                    acordaos_qo.append(decisao_colegiada)
                if acordao_tipo == 'OUTROS':
                    acordaos_outros.append(decisao_colegiada)




            recortar = acordaos.find('<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --')
            acordaos = acordaos[recortar+len('<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --'):]
        return (arquivo_a_extrair,
                adi_decisao,
                acordaos_publicados,
                acordaos_adi,
                acordaos_agr,
                acordaos_emb,
                acordaos_qo,
                acordaos_outros)
    else:
        return ([], 'NA', [], [], [], [], [], [])


def extrai_mono_da_string (arquivo_a_extrair, path):  # usar duas contra-barras depois do nome

        if arquivo_a_extrair in os.listdir(path):

            monocraticas = carregar_arquivo_nome (arquivo_a_extrair , path)
            # print (arquivo_a_extrair)

            # n_monocraticas = extrair(monocraticas,'Documentos encontrados: ','</td>')


            n_monocraticas = monocraticas.count('img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;')

            adi_decisao_mono = 'NA'
            monocraticas_publicadas = []
            monocraticas_adi = []
            monocraticas_agr = []
            monocraticas_emb = []
            monocraticas_qo = []
            monocraticas_outros = []
            monocraticas_amicus = []
            monocraticas_mc = []
            monocraticas_publicadas = []
            processo_juris = 'NA'


            if "Nenhum registro encontrado" in monocraticas:
                decisao_monocratica = []

            else:
                decisao_monocratica = []

                for decisoes in range (int(n_monocraticas)):


                    monocraticas_adi    = []
                    monocraticas_emb    = []
                    monocraticas_agr    = []
                    monocraticas_qo     = []
                    monocraticas_outros = []

                    acordao_tipo = 'NA'
                    processo_juris = 'NA'
                    relator_juris = 'NA'
                    data_acordao = 'NA'
                    orgao_julgador_acordao = 'NA'
                    decisao_juris = 'NA'
                    legislacao = 'NA'
                    observacao = 'NA'


                    monocraticas = monocraticas.replace ('/n/n','/n')
                    monocraticas = monocraticas.replace ('/t','')


                    processo_juris = extrair(monocraticas,'''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />''', '<br />').upper()

                    processo_juris = processo_juris.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                    processo_juris = processo_juris.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                    processo_juris = processo_juris.replace('MEDIDA CAUTELAR', 'MC')
                    processo_juris = processo_juris.replace('\n', '')
                    processo_juris = processo_juris.replace('\t', '')
                    processo_juris = processo_juris.split('<STRONG>')[1]

                    acordao_tipo = 'na'

                    if "AMICUS" in processo_juris:
                        moocratica_tipo = "AMICUS"
                    elif 'MC' in processo_juris or 'CAUT' in processo_juris:
                        moocratica_tipo = "CAUT"
                    elif 'EMB.' in processo_juris:
                        moocratica_tipo = 'EMB'
                    elif 'AG.REG' in processo_juris:
                        moocratica_tipo = 'AGR'
                    elif 'ORDEM' in processo_juris or 'QO' in processo_juris:
                        moocratica_tipo = 'QO'
                    elif processo_juris[0:3] == "ADI":
                        moocratica_tipo = 'PRINCIPAL'
                    else:
                        moocratica_tipo = 'OUTROS'


                    relator_juris = extrair(monocraticas, 'Relator(a):&nbsp ', '<br />').upper()
                    relator_juris = relator_juris.lstrip(' ')
                    relator_juris = relator_juris.lstrip('MIN.')
                    relator_juris = relator_juris.lstrip(' ')
                    relator_juris = remover_acentos(relator_juris)

                    data_acordao = extrair(monocraticas, 'Julgamento:&nbsp', '&nbsp')
                    data_acordao = data_acordao.replace('\t','')

                    orgao_julgador_acordao = relator_juris

                    publicacao_monocratica = extrair (monocraticas, '''<pre><span style='font-family:tahoma, verdana, arial, sans-serif;font-size:1.1 em;font-weight:bold'>''', '</pre>')


                    decisao_juris = extrair (monocraticas, '''Decisão</strong></p>''', '</pre>')
                    if '<pre>' in decisao_juris:
                        decisao_juris = decisao_juris.split('<pre>')[1]
                    decisao_juris = limpar2(decisao_juris)
                    decisao_juris = decisao_juris.replace('\n\n','\n')



                    legislacao = extrair (monocraticas, '''Legislação</strong></p>''', '</pre>')
                    legislacao = legislacao.replace('\t','')
                    legislacao = legislacao.replace('\n','')

                    observacao =  extrair (monocraticas, '''<p><strong>observação</strong></p>''', '</pre>')



                    decisao_monocratica = [arquivo_a_extrair, acordao_tipo, processo_juris, relator_juris, data_acordao, orgao_julgador_acordao, publicacao_monocratica, decisao_juris, legislacao, observacao]
                    # print (decisao_monocratica)

                    monocraticas_publicadas.append(decisao_monocratica)
                    if moocratica_tipo == 'PRINCIPAL':
                        monocraticas_adi.append(decisao_monocratica)
                        adi_decisao_mono = decisao_juris
                    if moocratica_tipo == 'EMB':
                        monocraticas_emb.append(decisao_monocratica)
                    if moocratica_tipo == 'AGR':
                        monocraticas_agr.append(decisao_monocratica)
                    if moocratica_tipo == 'QO':
                        monocraticas_qo.append(decisao_monocratica)
                    if moocratica_tipo == 'OUTROS':
                        monocraticas_outros.append(decisao_monocratica)
                    if moocratica_tipo == 'AMICUS':
                        monocraticas_amicus.append(decisao_monocratica)
                    if moocratica_tipo == 'MC':
                        monocraticas_mc.append(decisao_monocratica)



                recortar = monocraticas.find('''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />''')
                monocraticas = monocraticas[recortar+len('''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />'''):]
            return (processo_juris,
                    arquivo_a_extrair,
                    adi_decisao_mono,
                    monocraticas_publicadas,
                    monocraticas_adi,
                    monocraticas_mc,
                    monocraticas_agr,
                    monocraticas_emb,
                    monocraticas_qo,
                    monocraticas_amicus,
                    monocraticas_outros)
        else:
            return ([], 'NA', [], [], [], [], [], [], [],[], [])