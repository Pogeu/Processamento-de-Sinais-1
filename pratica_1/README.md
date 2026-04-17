# Prática 1 - Sinais e Sistemas

Esta pasta reúne os materiais da Aula Prática 1 da disciplina **Processamento de Sinais I**.

## Autores:
- Pedro Nicollas Pereira Azevedo Della Torre Bastos
- Gabriel Florencio da Fonseca
- Ricardo Alexandre Vieira da Silva

## Conteúdo da pasta
- `Processamento_de_Sinais_I___Aula_Prática_1.pdf`: enunciado da prática.
- notebooks Jupyter com a implementação e análise de cada item proposto.

## Tema da prática
A prática aborda geração, análise e reprodução de sinais, além do uso de resposta ao impulso para modelagem de sistemas.

## Atividades propostas
1. Para o sinal `x(t) = cos(2*pi*f*t)`, com duração de 5 s e frequência de amostragem `fs = 44,1 kHz`:
   - gerar gráficos no domínio do tempo para `f = 500 Hz`, `5000 Hz` e `10000 Hz`;
   - escrever código para tocar os sinais gerados;
   - comentar os resultados obtidos.

2. Para um `chirp` com frequência inicial `f0 = 500 Hz`, frequência final `f1 = 10000 Hz`, duração de 5 s e `fs = 44,1 kHz`:
   - gerar gráficos no domínio do tempo com varreduras lineares, quadráticas e logarítmicas;
   - escrever código para tocar os sinais gerados;
   - comentar os resultados obtidos.

3. Ler o arquivo `handel.wav` e:
   - gerar o gráfico do sinal de áudio no domínio do tempo;
   - escrever código para reproduzir o sinal original, com o dobro da frequência de amostragem e com o quádruplo da frequência de amostragem;
   - comentar os resultados e comparar o espectro do áudio com os espectros das questões anteriores.

4. Usar o arquivo `h_banheiro.wav`, que representa a resposta ao impulso de um banheiro:
   - descrever o procedimento para calcular a resposta ao impulso de uma sala qualquer;
   - explicar limitações e cuidados envolvidos no processo.

5. Ler os arquivos `h_banheiro.wav` e `sinal_taca.wav` e:
   - gerar gráficos dos sinais no domínio do tempo;
   - escrever código para tocar os sinais;
   - comentar os resultados.

6. Calcular a resposta de `h_banheiro[n]` para uma entrada igual ao sinal de áudio e ao sinal da taça:
   - avaliar as respostas no tempo;
   - ouvir as respostas;
   - comentar os resultados obtidos.

## Observação importante
Para convoluir dois sinais, eles precisam estar na mesma frequência de amostragem.

## Observação sobre arquivos
Os notebooks desta prática podem usar os arquivos de áudio centralizados em `../data` em vez das cópias locais da pasta.

## Resumo das respostas das questões
1. **Sinais senoidais**: conforme a frequência aumenta de `500 Hz` para `5000 Hz` e `10000 Hz`, cresce o número de oscilações no mesmo intervalo de tempo. Na reprodução, isso se traduz em sons progressivamente mais agudos.

2. **Sinais chirp**: os chirps linear, quadrático e logarítmico apresentam varredura contínua de frequência entre `500 Hz` e `10000 Hz`, mas com taxas de crescimento diferentes. Auditivamente, todos começam mais graves e terminam mais agudos.

3. **Áudio `handel.wav`**: no domínio do tempo, o sinal é mais complexo e não periódico como os anteriores, por representar um trecho musical com várias componentes simultâneas. Ao reproduzir com `2x` e `4x` a frequência de amostragem, o áudio fica mais rápido e mais agudo. No espectro, aparecem várias componentes de frequência, diferentemente dos sinais mais simples das questões 1 e 2.

4. **Resposta ao impulso de uma sala**: o procedimento consiste em emitir um sinal conhecido no ambiente, gravar a resposta com um microfone e aplicar deconvolução para estimar a resposta ao impulso. Os principais cuidados envolvem ruído ambiente, não linearidades da fonte, reflexões múltiplas e posicionamento do microfone.

5. **`h_banheiro.wav` e `sinal_taca.wav`**: a resposta ao impulso do banheiro apresenta um pico inicial seguido de reflexões decrescentes, enquanto o sinal da taça mostra uma oscilação ressonante com decaimento gradual. Na audição, a taça soa como uma ressonância definida, e o banheiro como um impulso curto com reverberação.

6. **Convolução com `h_banheiro.wav`**: ao convoluir os sinais de entrada com a resposta ao impulso do banheiro, o resultado passa a simular a propagação do som nesse ambiente. No tempo, os sinais ficam mais longos por causa das reflexões; na audição, surge uma reverberação perceptível, típica de um espaço fechado.

## Sugestão de organização
Uma forma prática de estruturar esta pasta é:
- um notebook para geração e análise dos sinais senoidais e chirps;
- um notebook para análise dos arquivos de áudio;
- um notebook para resposta ao impulso e convolução.
