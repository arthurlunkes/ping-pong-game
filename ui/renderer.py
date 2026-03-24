"""Renderização visual de entidades e elementos de tela.

Este módulo desacopla chamadas de desenho da lógica de jogo. As dependências
concretas (API de desenho e display) são injetadas externamente.
"""

from __future__ import annotations
from typing import Any
from game.entities import Ball, Paddle


class Renderer:
    """Responsável por desenhar elementos visuais do jogo."""

    def __init__(
        self,
        screen: Any,
        draw_api: Any,
        display_api: Any,
        background_color: tuple[int, int, int],
        foreground_color: tuple[int, int, int],
    ) -> None:
        """Inicializa o renderizador com as dependências visuais necessárias."""
        self.screen = screen
        self.draw_api = draw_api
        self.display_api = display_api
        self.background_color = background_color
        self.foreground_color = foreground_color

    def clear(self) -> None:
        """Limpa a tela com a cor de fundo."""
        self.screen.fill(self.background_color)

    def draw_paddle(self, paddle: Paddle) -> None:
        """Desenha uma raquete na tela."""
        self.draw_api.rect(self.screen, self.foreground_color, paddle.rect)

    def draw_ball(self, ball: Ball) -> None:
        """Desenha a bola na tela.

        O comportamento original é preservado: o centro do círculo usa as
        coordenadas x/y da própria entidade.
        """
        self.draw_api.circle(self.screen, self.foreground_color, (ball.x, ball.y), ball.radius)

    def flip(self) -> None:
        """Apresenta o frame atual na janela."""
        self.display_api.flip()
