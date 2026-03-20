# Prática 2 - Amostragem

Esta pasta reúne os materiais da Aula Prática 2 da disciplina **Processamento de Sinais I**.

## Conteúdo da pasta
- `Aula_Prática_2.pdf`: enunciado da prática.
- notebooks Jupyter com a implementação e análise de cada questão proposta.

## Tema da prática
A prática aborda análise espectral, subamostragem, sobreamostragem, frequência de Nyquist, reconstrução de sinais e convolução com resposta ao impulso.

## Atividades propostas
1. Para o sinal `x(t) = cos(2*pi*f*t)`, amostrado com `fs = 44,1 kHz`:
   - calcular o espectro para `f = 500 Hz`, `5000 Hz`, `10000 Hz` e `50000 Hz`;
   - comentar os resultados obtidos.

2. Para um `chirp` com frequência inicial `f0 = 500 Hz`, frequência final `f1 = 10000 Hz` e `fs = 44,1 kHz`:
   - calcular o espectro para varreduras lineares, quadráticas e logarítmicas;
   - comentar os resultados obtidos.

3. Ler o arquivo `handel.wav` e:
   - calcular o espectro do sinal de áudio;
   - comentar os resultados obtidos.

4. Para a subamostragem de um sinal discreto `y[n] = x[nM]`, usando `handel.wav`:
   - criar uma função para realizar a subamostragem;
   - aplicar a subamostragem para `M = 2`, `4` e `8`;
   - calcular o espectro dos sinais subamostrados;
   - ouvir os sinais subamostrados;
   - comentar os resultados.

5. Repetir a questão anterior com `scipy.signal.resample()` e comparar com a função própria.

6. Para a sobreamostragem de um sinal discreto por inserção de zeros, usando `handel.wav`:
   - criar uma função para realizar a sobreamostragem;
   - aplicar a sobreamostragem para `L = 2`, `4` e `8`;
   - calcular o espectro dos sinais sobreamostrados;
   - ouvir os sinais sobreamostrados;
   - comentar os resultados.

7. Repetir a questão anterior com `scipy.signal.resample()` e comparar com a função própria.

8. Para o sinal `x(t) = cos(2000*pi*t) + sin(5000*pi*t)`, considerando uma aproximação contínua amostrada com `fs = 10 MHz`:
   - gerar o gráfico de `x(t)` no tempo com duração de `10 ms`;
   - calcular o espectro de `x(t)`;
   - amostrar o sinal na frequência de Nyquist;
   - calcular o espectro de `x[n]`;
   - reconstruir `x(t)` a partir de `x[n]` com interpolação sinc e pulso retangular;
   - comentar os resultados.

9. Ler os arquivos `h_banheiro.wav` e `sinal_taca.wav` e:
   - calcular o espectro dos sinais;
   - comentar os resultados obtidos.

10. Calcular a resposta de `h_banheiro[n]` para entradas iguais a `handel.wav` e `sinal_taca.wav`:
   - calcular o espectro das respostas;
   - comentar os resultados obtidos.

## Observação importante
Para convoluir dois sinais, eles precisam estar na mesma frequência de amostragem.

## Resumo das respostas das questões
1. **Cossenoides amostradas**: para frequências abaixo de Nyquist, o espectro mostra picos nas próprias frequências do sinal. Para `50000 Hz`, ocorre aliasing, e o pico aparece refletido dentro da faixa amostrada.

2. **Chirps**: os sinais linear, quadrático e logarítmico distribuem energia entre `500 Hz` e `10000 Hz`, mas com perfis espectrais diferentes conforme a lei de varredura.

3. **Áudio `handel.wav`**: o espectro do trecho musical possui várias componentes harmônicas, sendo muito mais complexo do que os sinais simples das primeiras questões.

4. **Subamostragem própria**: ao reduzir a taxa de amostragem sem filtragem anti-aliasing, surgem sobreposições espectrais e distorções mais visíveis para fatores maiores.

5. **Subamostragem com `resample()`**: a rotina da SciPy tende a gerar um resultado mais suave e com menos degradação do que a simples retirada de amostras.

6. **Sobreamostragem própria**: a inserção de zeros aumenta a taxa de amostragem, mas cria imagens espectrais sem adicionar informação nova ao sinal.

7. **Sobreamostragem com `resample()`**: a interpolação da SciPy reduz as imagens espectrais e produz uma versão mais suave do sinal sobreamostrado.

8. **Nyquist e reconstrução**: a amostragem em `5000 Hz` é suficiente para representar o sinal sem aliasing ideal, e a reconstrução por sinc recupera melhor o formato original do que o pulso retangular.

9. **`h_banheiro.wav` e `sinal_taca.wav`**: a resposta ao impulso do banheiro possui energia espalhada por ampla faixa, enquanto o sinal da taça apresenta picos mais ressonantes e concentrados.

10. **Convolução com `h_banheiro.wav`**: as respostas passam a incorporar a reverberação do ambiente, ficando mais longas no tempo e com espectros moldados pela resposta ao impulso.

## Observações sobre implementação
- A função `calculate_spectrum()` é carregada a partir de `calculate_spectrum.py`.
- Os arquivos de áudio são lidos a partir de `../data`.
- Na questão 10, `handel.wav` é reamostrado para a mesma frequência de amostragem de `h_banheiro.wav` antes da convolução.
