"""Entidades principais do jogo Ping-Pong.

Este módulo define as entidades usadas pelo jogo de forma
independente das responsabilidades de renderização e entrada.
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Paddle:
    """Representa uma raquete controlada por jogador ou IA."""

    x: int
    y: int
    width: int
    height: int
    speed: int

    @property
    def rect(self) -> tuple[int, int, int, int]:
        """Retorna o retângulo atual da raquete como (x, y, largura, altura)."""
        return (self.x, self.y, self.width, self.height)

    def move(self, delta_y: int) -> None:
        """Move a raquete verticalmente em delta_y pixels."""
        self.y += delta_y

    def clamp_to_screen(self, screen_height: int) -> None:
        """Mantém a raquete totalmente dentro dos limites da tela."""
        if self.y < 0:
            self.y = 0
        elif self.y > screen_height - self.height:
            self.y = screen_height - self.height

    @property
    def center_y(self) -> int:
        """Retorna a coordenada y do centro da raquete."""
        return self.y + self.height // 2


@dataclass
class Ball:
    """Representa a bola, incluindo posição e velocidade."""

    x: int
    y: int
    radius: int
    velocity_x: int
    velocity_y: int

    @property
    def rect(self) -> tuple[int, int, int, int]:
        """Retorna um retângulo para verificações de colisão.

        O código original modela a bola como quadrado para colisão, enquanto
        a renderização usa um círculo. Esse comportamento é preservado.
        """
        size = self.radius
        return (self.x, self.y, size, size)

    def update(self) -> None:
        """Avança a posição da bola com base na velocidade atual."""
        self.x += self.velocity_x
        self.y += self.velocity_y

    def invert_x(self) -> None:
        """Inverte a direção horizontal do movimento."""
        self.velocity_x = -self.velocity_x

    def invert_y(self) -> None:
        """Inverte a direção vertical do movimento."""
        self.velocity_y = -self.velocity_y

    def reset(self, center_x: int, center_y: int) -> None:
        """Reposiciona a bola no centro preservando a direção atual."""
        self.x = center_x - self.radius // 2
        self.y = center_y - self.radius // 2
