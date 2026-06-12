# Pratica 7 - Projeto de Filtros FIR

Esta pasta reune os materiais da Aula Pratica 7 da disciplina **Processamento de Sinais I**.

## Autores
- Pedro Nicollas Pereira Azevedo Della Torre Bastos
- Gabriel Florencio da Fonseca
- Ricardo Alexandre Vieira da Silva

## Conteudo da pasta
- `Aula_Prática_7.pdf`: enunciado atual da pratica.
- `questao_1.ipynb`: projeto manual de filtros FIR por janelamento para passa-baixas, passa-altas, passa-faixas e rejeita-faixas.
- `questao_2.ipynb`: derivacao da resposta ao impulso ideal para as tres formas de modulo da figura e projeto FIR correspondente.
- `questao_3.ipynb`: filtragem do audio `handel.wav` com FIR, comparacao com a pratica 6 e quantizacao dos coeficientes.
- `fir_utils.py`: funcoes auxiliares compartilhadas pelos notebooks.

## Estrategia adotada
- A pratica inteira evita funcoes prontas de projeto de filtros.
- Os filtros FIR sao obtidos por truncamento da resposta ideal seguido de janelamento.
- A questao 3 usa um sistema FIR em cascata com passa-altas em `180 Hz`, rejeita-faixas em `1850-2150 Hz` e passa-baixas em `2400 Hz`.
- A comparacao com a pratica 6 reutiliza a referencia `PA 180 Hz + PB 1800 Hz` implementada no notebook `pratica_6/questao_5.ipynb`.

## Observacoes
- No item 2(b), o enunciado apresenta a resposta ideal em funcao de `omega_c`, sem valor numerico fixo. Para os graficos, foi adotado `omega_c = pi / 8`.
- As linhas `SYSTEM:` presentes no texto extraido do PDF foram tratadas como ruido do arquivo e nao como parte do enunciado.
- O arquivo `handel.wav` e lido de `../data/handel.wav`.
