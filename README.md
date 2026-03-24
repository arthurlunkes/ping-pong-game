# Ping-Pong 2D (Pygame)

Jogo Pong 2D desenvolvido com Python e Pygame, aplicando princípios SOLID
e separação de responsabilidades.

## Descrição

Clone clássico do Pong com:

- Jogador humano (raquete esquerda) e oponente controlado por IA (raquete direita)
- Motor de física isolado para colisões
- IA extensível por nível de dificuldade
- Arquitetura orientada a objetos com módulos desacoplados

## Controles

| Tecla           | Ação                     |
| --------------- | ------------------------ |
| Seta para cima  | Mover raquete para cima  |
| Seta para baixo | Mover raquete para baixo |
| Espaço          | Iniciar partida no menu  |

## Arquitetura

```
ping-pong-game/
├── main.py               ← ponto de entrada, monta e inicia o jogo
├── config.py             ← todas as constantes configuráveis
├── game/
│   ├── core.py           ← classe Game (orquestrador do loop)
│   ├── entities.py       ← classes Ball e Paddle (domínio puro)
│   ├── physics.py        ← classe PhysicsEngine (colisões)
│   ├── ai.py             ← classe AIController (lógica da IA)
│   ├── input_handler.py  ← classe InputHandler (entrada do teclado)
│   └── protocols.py      ← contratos abstratos (Protocols/interfaces)
└── ui/
    ├── renderer.py       ← classe Renderer (desenho de entidades)
    ├── hud.py            ← classe HUD (placar)
    └── menu.py           ← classe MenuScreen (tela inicial)
```

### Princípios SOLID aplicados

| Princípio | Nome completo                   | Aplicação no projeto                                                                                                                        |
| --------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| SRP       | Single Responsibility Principle | Cada classe tem exatamente uma responsabilidade: `PhysicsEngine` só trata colisões, `HUD` só desenha o placar, etc.                         |
| OCP       | Open/Closed Principle           | `AIController` é estendido por novas dificuldades adicionando entradas no dicionário `_AJUSTE_VELOCIDADE`, sem tocar nos métodos existentes |
| LSP       | Liskov Substitution Principle   | Qualquer classe que implemente um Protocol (ex.: `IRenderizador`) pode substituir outra sem quebrar o comportamento de `Game`               |
| ISP       | Interface Segregation Principle | Cada Protocol expõe apenas os métodos que o consumidor precisa: `IHUD` só tem `draw_score`, `IMotorFisico` só tem os métodos de colisão     |
| DIP       | Dependency Inversion Principle  | `Game` depende dos contratos em `protocols.py` — nunca das classes concretas `Renderer`, `AIController`, `PhysicsEngine`, etc.              |

## Como Instalar

1. (Opcional) Crie e ative um ambiente virtual:

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r pip_freeze.txt
```

## Como Executar

```bash
python main.py
```

## Dependência Principal

- pygame 2.6.1
