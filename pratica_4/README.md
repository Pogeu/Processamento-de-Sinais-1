# Pratica 4 - DFT e DCT

Esta pasta reune a implementacao e os resultados da Pratica 4 da disciplina **Processamento de Sinais I**.

## Autores
- Pedro Nicollas Pereira Azevedo Della Torre Bastos
- Gabriel Florencio da Fonseca
- Ricardo Alexandre Vieira da Silva

## Arquivos da pasta
- `Aula_Prática_4.pdf`: enunciado da pratica.
- `questao_1.ipynb`: comparacao entre DTFT e DFT para diferentes valores de `N`.
- `questao_2.ipynb`: efeito do tamanho da DFT e do zero-padding na visualizacao espectral.
- `questao_3.ipynb`: compressao do audio `handel.wav` por DCT e por FFT.
- `questao_4.ipynb`: analise da concentracao de energia da imagem `sosias.jpg` na DCT2.
- `questao_5.ipynb`: compressao da imagem `sosias.jpg` por blocos.
- `relatorio_pratica_4.pdf`: relatorio final resumido da pratica.

## Dados utilizados
Os notebooks usam arquivos da pasta `data/` na raiz do repositorio:
- `data/handel.wav`: usado apenas na questao 3.
- `data/sosias.jpg`: usado apenas nas questoes 4 e 5.

As questoes 1 e 2 nao dependem de arquivos externos.

## Estado atual dos notebooks
- Os notebooks foram ajustados para localizar automaticamente a raiz do projeto, entao podem ser executados tanto a partir da raiz quanto a partir da propria pasta `pratica_4`.
- As referencias a `handel.wav` e `sosias.jpg` foram removidas dos exercicios que nao usam esses arquivos.
- Cada notebook ficou com apenas as importacoes e funcoes auxiliares necessarias para sua propria questao.

## Resumo dos resultados
1. **Questao 1:** a DFT amostra a DTFT; aumentar `N` densifica a amostragem em frequencia sem alterar o conteudo do sinal.
2. **Questao 2:** zero-padding melhora a interpolacao visual do espectro, mas a separacao real entre componentes depende do numero de amostras reais.
3. **Questao 3:** a DCT concentrou energia em menos coeficientes que a FFT para niveis equivalentes de erro, tornando a compressao mais eficiente.
4. **Questao 4:** a maior parte da energia da imagem ficou concentrada nas baixas frequencias da DCT2.
5. **Questao 5:** blocos menores preservaram melhor a qualidade visual; blocos maiores comprimiram mais, com aumento do erro.

## Como executar
1. Abra o notebook desejado.
2. Execute a primeira celula para configurar caminhos e importacoes.
3. Rode as demais celulas em sequencia.

## Observacao
Se `data/handel.wav` ou `data/sosias.jpg` nao estiverem disponiveis, os notebooks que dependem deles nao poderao reproduzir os resultados correspondentes.
