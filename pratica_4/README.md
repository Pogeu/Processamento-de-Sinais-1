# Prática 4 - DFT e DCT

Esta pasta reúne os materiais da Aula Prática 4 da disciplina **Processamento de Sinais I**.

## Autores:
- Pedro Nicollas Pereira Azevedo Della Torre Bastos
- Gabriel Florencio da Fonseca
- Ricardo Alexandre Vieira da Silva

## Conteúdo da pasta
- `Aula_Prática_4.pdf`: enunciado da prática.
- notebooks Jupyter com a implementação e análise de cada questão proposta.
- `relatorio_pratica_4.pdf`: relatório final resumido da prática.

## Tema da prática
A prática aborda propriedades da DFT e da DCT, incluindo amostragem espectral, efeito de zero-padding, compressão de áudio 1-D e compressão de imagens 2-D.

## Atividades propostas
1. Para o sinal discreto finito
   - `x[n] = δ[n] - δ[n-1] + δ[n-2] - δ[n-3]`
   - comparar a DTFT contínua com a DFT para `N` em `{4, 16, 64, 1024}`;
   - comentar os resultados.

2. Para o sinal
   - `x(t) = sin(2πt) + sin(2.02πt)`
   - amostrado com `fs = 10 Hz`;
   - estudar o efeito do tamanho da DFT e do zero-padding na visualização espectral;
   - comentar os resultados.

3. Para o áudio `handel.wav`
   - comparar compressão por DCT e por DFT/FFT;
   - preservar diferentes percentuais de energia;
   - comparar número de coeficientes mantidos e erro de reconstrução;
   - comentar os resultados.

4. Para a imagem `sosias.jpg`
   - calcular a DCT2;
   - analisar a concentração de energia no domínio transformado;
   - comentar os resultados.

5. Para a imagem `sosias.jpg`
   - realizar compressão por blocos com tamanhos `8x8` e `64x64`;
   - testar preservação de energia em `95%` e `50%`;
   - comparar erro e degradação visual;
   - comentar os resultados.

## Resumo das respostas das questões
1. **DTFT x DFT**: a DFT representa amostras da DTFT; aumentar `N` densifica a amostragem em frequência e melhora a visualização do espectro contínuo.

2. **Zero-padding e resolução**: zero-padding melhora a interpolação visual do espectro, mas a separação real entre componentes próximas depende do aumento do número de amostras observadas.

3. **Compressão de áudio**: a DCT concentrou energia em menos coeficientes do que a FFT para níveis equivalentes de erro, produzindo compressão mais eficiente para o áudio analisado.

4. **Energia da imagem na DCT2**: a maior parte da energia ficou concentrada nas baixas frequências espaciais, justificando o uso da DCT em compressão de imagens.

5. **Compressão por blocos**: blocos menores preservaram melhor os detalhes visuais, enquanto blocos maiores aumentaram a compactação ao custo de maior erro e mais degradação perceptual.

## Observações sobre implementação
- Os notebooks foram ajustados para localizar automaticamente a raiz do projeto, podendo ser executados tanto a partir da raiz quanto da própria pasta `pratica_4`.
- O arquivo de áudio utilizado nas análises é lido a partir de `../data/handel.wav` apenas na questão 3.
- A imagem utilizada nas análises é lida a partir de `../data/sosias.jpg` nas questões 4 e 5.
- As questões 1 e 2 não dependem de arquivos externos.
- Referências a `handel.wav` e `sosias.jpg` foram removidas dos exercícios que não utilizam esses arquivos.
