# Pratica 6 - Projeto de Filtros IIR

Esta pasta reune os materiais da Aula Pratica 6 da disciplina **Processamento de Sinais I**.

## Autores
- Pedro Nicollas Pereira Azevedo Della Torre Bastos
- Gabriel Florencio da Fonseca
- Ricardo Alexandre Vieira da Silva

## Conteudo da pasta
- `Aula_Prática_6.pdf`: enunciado atual da pratica.
- `questao_1.ipynb`: blocos IIR basicos de 2a ordem e variacao do parametro `r`.
- `questao_2.ipynb`: passa-faixas por cascata de passa-altas e passa-baixas.
- `questao_3.ipynb`: rejeita-faixas por paralelo de passa-baixas e passa-altas.
- `questao_4.ipynb`: quantizacao dos coeficientes dos filtros das questoes 2 e 3.
- `questao_5.ipynb`: filtragem do audio `handel.wav` contaminado.

## Restricao adotada
A resolucao usa apenas blocos basicos passa-baixas e passa-altas. Por isso:

- passa-faixas foi implementado como cascata de passa-altas com passa-baixas;
- rejeita-faixas foi implementado como paralelo de passa-baixas com passa-altas;
- o notch pedido no enunciado foi aproximado por uma rejeicao estreita usando passa-baixas e passa-altas.

## Parametro de seletividade
Todas as questoes variam o parametro `r`. Quanto maior `r`, mais proximos os polos ficam do circulo unitario. Isso aumenta a seletividade e estreita a transicao, mas tambem reduz a margem de estabilidade e aumenta a sensibilidade a quantizacao.

## Observacoes
- As linhas `SYSTEM:` que aparecem no texto extraido do PDF foram tratadas como ruído do arquivo e nao fazem parte da resolucao.
- O arquivo `handel.wav` e lido de `../data/handel.wav`.
- A questao 5 usa a taxa de amostragem nativa do arquivo de audio.
