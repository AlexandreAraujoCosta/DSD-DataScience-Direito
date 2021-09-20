# Data Science e direito
O projeto DSD (Data Sciece e Direito) contém uma série de programas em python voltados a extrair e organizar dados do site do Supremo Tribunal Federal (STF).
Esses programas foram desenvolvidos na disciplina Data Science e Direito, oferecida na graduação e na pós-graduação em Direito da UnB, pelo prof. Dr. Alexandre Araújo Costa.
A disciplina é acessível no seguinte endereço: www.dsd.arcos.org.br.

O projeto envolve alguns programas diferentes que estão contidos nesta página.

## 1. Módulo de funções: dsd.py
Este módulo contém uma série de funções dimensionadas para auxiliar no data mining de informações processuais do STF. Aconselhamos que você copie este módulo para o seu diretório de trabalho, ou para o diretório no qual você pretende armazenar os demais programas deste projeto. Esse passo é importante porque os demais programas dependem deste módulo para que possam operar adequadamente.

## 2. Programa extrator de dados da base de acompanhamento processual: STF_Extrator.py
Este programa se utiliza das funções contidas no módulo dsd.py, para extrair os dados de processos do STF e gravá-los em arquivos independentes.
Os processos a serem extraídos devem ser definidos por meio da edição do programa (sugerimos o uso do Spyder para essa finalidade), bastando para isso alterar a classe a ser buscada (ADI, ADPF, MS, etc.) e um intervalo de números (definido por um número inicial e um número final).
Também é simples adaptar o programa para buscar os dados relativos a uma lista de processos.
A operação consiste em requisitar os dados do STF (na base de Acompanhamento Processual e na base específica de Controle Concentrado) e gravar os dados em arquivos específicos, em um diretório determinado no programa (para alterá-lo, modifique o path).
Como o gargalo na extração de dados do STF se dá na capacidade de interação do seu computador com o servidor do Tribunal, que tende a cortar a comunicação após algumas centenas de consultas, a estratégia adotada é gravar todos os dados relevantes nos arquivos, para depois organizar esses dados, em um progrma que roda sobre os dados gravados.

## 3. Resultados da aplicação do extrator
Os arquivos .rar contém os dados extraídos por meio do STF_Extrator.py, em extração realizada entre 18 e 19 de setembro de 2021.
O conjunto dos dados extraídos somaria um arquivo .rar de 93K, o que levou a repartir o conteúdo em 4 arquivos para as ADIs e 1 para as ADPFs.
Para que funcione perfeitamente com o extrator, indica-se que esses arquivos sejam extraídos para um subdiretório do seu diretório de trabalho, que deve ter o nome de "ADItotal". Se você preferir outro nome, basta alterar no programa STF_Organizador.py o path usado para identificar a fonte dos dados.
Como o organizador incorpora todas as informações contidas nesse diretório, ele precisa ter somente os arquivos com os dados, sem contar com outros arquivos (como os tipo RAR ou outras informações, que acarretarão problemas na execução do organizador de dados.

## 4. Programa organizador dos dados: STF_Organizador.py
Este programa parte dos dados gerados pelo STF_Extrator.py e organiza essas informações em tabelas no formato CSV. De fato, os arquivos são gravados como TXT, pois isso facilita a sua incorporação posterior ao Excel, que é o programa tipicamente usado para explorar inicialmente esses dados.

