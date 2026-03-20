# Prática 3 - Transformada z

Esta pasta reúne os materiais da Aula Prática 3 da disciplina **Processamento de Sinais I**.

## Autores:
- Pedro Nicollas Pereira Azevedo Della Torre Bastos
- Gabriel Florencio da Fonseca
- Ricardo Alexandre Vieira da Silva

## Conteúdo da pasta
- `Aula_Prática_3.pdf`: enunciado da prática.
- notebooks Jupyter com a implementação e análise de cada questão proposta.

## Tema da prática
A prática aborda resposta em frequência, diagramas de polos e zeros, aplicação de sistemas lineares a sinais de áudio e recuperação aproximada de sinais por filtragem inversa.

## Atividades propostas
1. Para o sistema
   - `H(z) = 1 + 0.49z^-2 + 0.2401z^-6 - 0.0576z^-8 - 0.0282z^-10 - 0.0138z^-12`
   - calcular a resposta em frequência;
   - obter o diagrama de polos e zeros;
   - comentar os resultados.

2. Calcular a resposta de `H(z)` para uma entrada igual ao sinal de áudio do arquivo `handel.wav`:
   - calcular o espectro da saída;
   - comentar os resultados.

3. Projetar um filtro para recuperar o sinal de áudio original:
   - mostrar sua resposta em frequência;
   - mostrar seu diagrama de polos e zeros;
   - avaliar o quão próximo o sinal recuperado fica do sinal original;
   - comentar os resultados.

4. Para os sistemas
   - `H(z) = (1 - z^-L) / (1 - a z^-L)`
   - com `a` em `{0.7, 0.9}` e `L` em `{1, 4, 10}`
   - calcular a resposta em frequência;
   - obter o diagrama de polos e zeros;
   - comentar os resultados.

5. Repetir a lógica da questão 2 com os sistemas da questão 4.

6. Para os sistemas da questão 4, projetar filtros para recuperar o sinal de áudio original:
   - mostrar a resposta em frequência;
   - mostrar o diagrama de polos e zeros;
   - avaliar o quão próximo o sinal recuperado fica do original;
   - comentar os resultados.

7. Considerando os filtros utilizados nas questões 3 e 6:
   - projetar aproximações FIR desses filtros;
   - comentar a relação entre ordem do filtro e qualidade do sinal recuperado.

## Resumo das respostas das questões
1. **Sistema FIR da questão 1**: a resposta em frequência é moldada pelos zeros do numerador, produzindo atenuações seletivas em determinadas bandas.

2. **Aplicação em `handel.wav`**: o áudio de saída sofre coloração espectral conforme as bandas enfatizadas ou atenuadas por `H(z)`.

3. **Recuperação do sinal**: um equalizador inverso FIR regularizado permite recuperar o áudio de forma aproximada, reduzindo parte das distorções impostas pelo sistema.

4. **Sistemas parametrizados por `a` e `L`**: o valor de `a` controla o quão próximos os polos ficam do círculo unitário, enquanto `L` altera a periodicidade angular de polos e zeros.

5. **Resposta em áudio dos sistemas da questão 4**: diferentes pares `(a, L)` geram diferentes colorações sonoras e diferentes assinaturas espectrais sobre `handel.wav`.

6. **Filtros recuperadores da questão 6**: a recuperação é possível de forma aproximada com inversão regularizada, mas a qualidade varia com a seletividade do sistema original.

7. **Aproximações FIR**: ordens maiores tendem a melhorar a qualidade da recuperação, ao custo de maior complexidade computacional.

## Observações sobre implementação
- A função `calculate_spectrum()` é carregada a partir de `../tools/calculate_spectrum.ipynb`.
- O arquivo de áudio utilizado nas análises é lido a partir de `../data/handel.wav`.
- A recuperação do sinal foi modelada por filtros inversos FIR regularizados para evitar instabilidades numéricas.
