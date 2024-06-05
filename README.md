Para buildar o projeto, iremos garantir que todos os pacotes necessários estão instalados.

`pip3 install -r requirements.txt`

Uma vez as dependências instaladas, rodemos o programa.

`python3 runner.py`

As variáveis do modelo de algoritmo genético podem ser alteradas no arquivo config.ini.
Tem como gerar os pontos e obstáculos de forma aleatória, mas também há elementos predefinidos que podem ser alterados, só basta definir a variável:

`generate_randomly = false`

O algoritmo, a cada nova geração, move um dos obstáculos aleatoriamente até 4 posições no mapa.