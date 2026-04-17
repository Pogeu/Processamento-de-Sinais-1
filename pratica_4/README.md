# Prática 4 - DFT e DCT

Esta pasta reúne os materiais da prática 4 da disciplina **Processamento de Sinais I**.

## Autores:
- Pedro Nicollas Pereira Azevedo Della Torre Bastos
- Gabriel Florencio da Fonseca
- Ricardo Alexandre Vieira da Silva

## Conteúdo da pasta
- `Processamento_de_Sinais_I___Aula_Prática_3.pdf`: enunciado fornecido para a prática.
- `aula_pratica_3.mlx` e `exemplo_aula_pratica_3.mlx`: materiais originais em MATLAB.
- `sosias.jpg`: imagem utilizada nas questões de compressão bidimensional.
- notebooks Jupyter com a implementação e análise de cada questão proposta.

## Tema da prática
A prática explora compressão de sinais e imagens com transformadas ortogonais, comparando o desempenho da DCT e da DFT na concentração de energia e na reconstrução com perda controlada.

## Atividades propostas
1. Comprimir o áudio `handel` usando DCT para diferentes níveis de preservação de energia.
2. Repetir a compressão do áudio usando DFT/FFT e comparar com a DCT.
3. Calcular a DCT2 da imagem `sosias.jpg` e analisar a distribuição de energia.
4. Comprimir a imagem preservando diferentes percentuais de energia e comparar os resultados.
5. Repetir a compressão da imagem por blocos `8x8` e `16x16`, comentando as diferenças.

## Resumo das respostas das questões
1. **Compressão por DCT no áudio**: a DCT concentrou a energia de `handel.wav` em poucos coeficientes, permitindo boa reconstrução mesmo com forte redução da quantidade de dados.

2. **Compressão por DFT no áudio**: a FFT também reconstrói o sinal, mas em geral exige mais coeficientes para atingir qualidade semelhante, o que a torna menos eficiente para compressão do que a DCT.

3. **Energia da DCT2 da imagem**: a maior parte da energia da imagem ficou concentrada nas baixas frequências espaciais, mostrando que a DCT2 é adequada para compressão com perdas moderadas.

4. **Compressão global da imagem**: níveis altos de preservação de energia mantêm a aparência visual próxima da original, enquanto níveis mais baixos aumentam o borramento e reduzem os detalhes finos.

5. **Compressão por blocos**: blocos `8x8` e `16x16` permitem processamento local da imagem; `8x8` tende a ficar mais próximo do comportamento de codecs práticos, enquanto blocos maiores podem introduzir artefatos mais visíveis.

## Observações sobre implementação
- O enunciado original cita `handel.mat`, mas esse arquivo não está disponível no repositório.
- Nesta implementação, as questões de áudio usam `../data/handel.wav`, que fornece um equivalente prático para as análises em Python.
- As transformadas foram implementadas com `scipy.fft`, usando `dct`, `idct`, `dctn`, `idctn`, `fft` e `ifft`.
- A imagem foi convertida para tons de cinza antes da análise por DCT2 para simplificar a interpretação da energia.
