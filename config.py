"""Constantes centralizadas de configuração do jogo Ping-Pong.

Este módulo agrupa todos os valores configuráveis em um único lugar para
evitar vars espalhadas pelo código.
"""

# Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Ping-Pong"

# Cores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Raquete
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_MARGIN = 15
PADDLE_SPEED = 5

# Bola
BALL_RADIUS = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Pontuação de vitória equilibrada para dar chance ao jogador
WIN_SCORE_PLAYER_1 = 5
WIN_SCORE_PLAYER_2 = 5
