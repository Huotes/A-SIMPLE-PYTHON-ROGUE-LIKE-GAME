# A Simple Python Rogue-like Game

Um jogo simples estilo rogue-like feito com Python e Pygame Zero, onde você controla um mago que enfrenta inimigos em um mapa.


## Sobre
Este projeto é um protótipo básico de jogo rogue-like com foco em mecânicas de movimento, combate mágico e inimigos simples.
Feito em Python 3.10 para aproveitar melhorias na tipagem, expressões estruturadas (match/case) e a estabilidade da linguagem nessa versão, garantindo compatibilidade com a lib (Pygame Zero).

## Estrutura do Projeto
```bash
A-SIMPLE-PYTHON-ROGUE-LIKE-GAME/
│
├── config.py           # Configurações globais (resolução, velocidade, etc)
├── enemy.py            # Classe e lógica dos inimigos
├── game_manager.py     # Lógica principal do jogo, controle de estados
├── main.py             # Arquivo principal para rodar o jogo
├── player.py           # Classe e lógica do jogador
├── spells.py           # Magias do jogador
├── requirements.txt    # Dependências do projeto (pgzero)
├── images/             # Sprites e imagens usadas no jogo
├── sounds/             # Sons e músicas do jogo
└── venv/               # Ambiente virtual Python
```
## Como rodar o jogo
Criar e ativar ambiente virtual (opcional, mas recomendado):

```bash

python3.10 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Instalar dependências:
```

```bash
pip install -r requirements.txt
```
## Executar o jogo:

```bash
pgzrun main.py
```
## Controles
- W/A/S/D — Movimentar o personagem (mago) pelo mapa.

- Clique esquerdo do mouse — Lança uma magia na direção do cursor.

- ENTER — Reiniciar o jogo após game over.

## Considerações Técnicas
Desenvolvido com Python 3.10 para compatibilidade.

Utiliza Pygame Zero para simplificar criação de jogos 2D em Python.

O jogo é desenhado para uma resolução fixa (480x320 px), facilitando o controle da viewport e performance.

Organização do código modularizada para fácil manutenção e futuras expansões.