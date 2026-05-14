# Prática 5 - Transformadas de Wavelets

Esta pasta reúne os materiais da Aula Prática 5 da disciplina **Processamento de Sinais I**.

## Autores:
- Pedro Nicollas Pereira Azevedo Della Torre Bastos
- Gabriel Florencio da Fonseca
- Ricardo Alexandre Vieira da Silva

## Conteúdo da pasta
- `Aula_Prática_5.pdf`: enunciado atual da prática.
- notebooks Jupyter com a implementação e análise de cada questão.

## Tema da prática
A prática aborda códigos de Hadamard em CDMA, conceitos fundamentais de wavelets, análise multirresolução de sinais não estacionários e remoção de ruído com wavelets e DFT.

## Atividades propostas
1. Simular um sistema CDMA com códigos de Hadamard e analisar o efeito de ruído e distorção no código do receptor.
2. Elaborar um resumo sobre transformadas de wavelets e aplicações.
3. Analisar um sinal não estacionário com a wavelet `bior4.4` em cinco níveis.
4. Analisar e denoiser o sinal `leleccum.mat` com `db4`, comparando com uma estratégia baseada em DFT.

## Resumo das respostas das questões
1. **CDMA com Hadamard**: a ortogonalidade dos códigos facilita a separação dos usuários, mas o desempenho cai com o aumento do ruído ou com distorção nos códigos disponíveis no receptor.

2. **Resumo teórico**: wavelets fornecem análise tempo-frequência multiescala e são especialmente úteis para sinais não estacionários, compressão e remoção de ruído.

3. **Sinal não estacionário**: a decomposição por `bior4.4` separa adequadamente componentes lentas, transitórios e oscilações localizadas em diferentes escalas.

4. **Denoising em `leleccum.mat`**: a limiarização por wavelets preserva melhor estruturas locais do sinal, enquanto a DFT atua de forma mais global e pode ser menos seletiva em alguns cenários.

## Observações sobre implementação
- O enunciado cita um `script` externo `non_stationary_signal.ipynb`, mas ele não está presente no repositório local.
- Para manter a prática executável sem downloads adicionais, a questão 3 usa um sinal não estacionário equivalente gerado localmente.
- O arquivo `leleccum.mat` é lido de `../data/leleccum.mat`.
- Os notebooks usam `PyWavelets` (`pywt`) para a decomposição e reconstrução multiescala.
