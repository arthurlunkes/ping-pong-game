"""Ponto de entrada do jogo Ping-Pong.

Este módulo inicializa o pygame, monta as dependências de cada camada
e inicia o loop principal do jogo.
"""

import sys

import pygame

import config
from game.ai import AIController
from game.core import Game
from game.entities import Ball, Paddle
from game.input_handler import InputHandler
from game.physics import PhysicsEngine
from ui.hud import HUD
from ui.menu import MenuScreen
from ui.renderer import Renderer


def _criar_jogo(screen: pygame.Surface) -> Game:
    """Instancia e conecta todas as dependências de uma partida."""
    player1 = Paddle(
        x=config.PADDLE_MARGIN,
        y=config.SCREEN_HEIGHT // 2 - config.PADDLE_HEIGHT // 2,
        width=config.PADDLE_WIDTH,
        height=config.PADDLE_HEIGHT,
        speed=config.PADDLE_SPEED,
    )
    player2 = Paddle(
        x=config.SCREEN_WIDTH - config.PADDLE_MARGIN - config.PADDLE_WIDTH,
        y=config.SCREEN_HEIGHT // 2 - config.PADDLE_HEIGHT // 2,
        width=config.PADDLE_WIDTH,
        height=config.PADDLE_HEIGHT,
        speed=config.PADDLE_SPEED,
    )
    ball = Ball(
        x=config.SCREEN_WIDTH // 2 - config.BALL_RADIUS // 2,
        y=config.SCREEN_HEIGHT // 2 - config.BALL_RADIUS // 2,
        radius=config.BALL_RADIUS,
        velocity_x=config.BALL_SPEED_X,
        velocity_y=config.BALL_SPEED_Y,
    )
    renderer = Renderer(
        screen=screen,
        draw_api=pygame.draw,
        display_api=pygame.display,
        background_color=config.BLACK,
        foreground_color=config.WHITE,
    )
    hud = HUD(
        screen=screen,
        font_factory=pygame.font.SysFont,
        text_color=config.WHITE,
        center_x=config.SCREEN_WIDTH // 2,
    )
    return Game(
        player1=player1,
        player2=player2,
        ball=ball,
        renderer=renderer,
        hud=hud,
        ai=AIController(difficulty="medium"),
        input_handler=InputHandler(
            up_key=pygame.K_UP,
            down_key=pygame.K_DOWN,
            quit_event_type=pygame.QUIT,
        ),
        physics=PhysicsEngine(),
        clock=pygame.time.Clock(),
        event_api=pygame.event,
        key_api=pygame.key,
        fps=config.FPS,
        screen_width=config.SCREEN_WIDTH,
        screen_height=config.SCREEN_HEIGHT,
        win_score_player1=config.WIN_SCORE_PLAYER_1,
        win_score_player2=config.WIN_SCORE_PLAYER_2,
    )


def _criar_menu(screen: pygame.Surface) -> MenuScreen:
    """Instancia o menu principal com as dependências do pygame."""
    return MenuScreen(
        screen=screen,
        event_api=pygame.event,
        display_api=pygame.display,
        time_api=pygame.time,
        font_factory=pygame.font.SysFont,
        title=config.WINDOW_TITLE,
        background_color=config.BLACK,
        foreground_color=config.WHITE,
        screen_width=config.SCREEN_WIDTH,
        screen_height=config.SCREEN_HEIGHT,
        quit_event_type=pygame.QUIT,
        keydown_event_type=pygame.KEYDOWN,
        start_key=pygame.K_SPACE,
    )


def main() -> None:
    """Inicializa o pygame e executa o ciclo menu → partida."""
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)

    menu = _criar_menu(screen)

    while True:
        if not menu.run():
            break
        if not _criar_jogo(screen).run():
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()