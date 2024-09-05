# Flappy Bird Distribuido usando RPC

Este é um jogo Flappy Bird implementado em Python usando Pygame e RPyC para comunicação cliente-servidor.

## Descrição

O jogo consiste em um servidor que gerencia a lógica do jogo e um cliente que se conecta ao servidor para jogar. O objetivo é controlar um pássaro e fazê-lo voar entre canos sem colidir.

## Requisitos

- Python 3.x
- Pygame
- RPyC

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/juliobossigia/Flappy-Bird-com-RPC.git
   ```

2. Instale as dependências:
   ```
   pip install pygame rpyc
   ```

## Como jogar

1. Inicie o servidor:
   ```
   python game-serv.py
   ```

2. Inicie o cliente:
   ```
   python game-client.py
   ```

3. Use a barra de espaço para fazer o pássaro pular.

## Características

- Jogo Flappy Bird clássico
- Servidor suporta um cliente por vez
- Sistema de pontuação e recorde
- Dificuldade progressiva (velocidade aumenta com a pontuação)

## Estrutura do projeto

- `game-serv.py`: Arquivo do servidor
- `game-client.py`: Arquivo do cliente
- `bird.png`: Imagem do pássaro
- `pipe.png`: Imagem do cano

## Configuração

Por padrão, o servidor está configurado para rodar no IP 172.30.30.18 e na porta 9090. Você pode alterar essas configurações nos arquivos `game-serv.py` e `game-client.py` se necessário.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.
