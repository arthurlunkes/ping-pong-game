"""Protocolos (contratos abstratos) do jogo Ping-Pong.

Este módulo define as interfaces usadas por Game e demais módulos de alto nível.
Seguindo o Princípio da Inversão de Dependência (DIP), módulos de alto nível
devem depender dessas abstrações, não de implementações concretas.
"""

from __future__ import annotations
from collections.abc import Sequence
from typing import Protocol


class IControladorIA(Protocol):
    """Contrato para qualquer estratégia de controle da raquete adversária."""

    def compute_move(self, paddle: object, ball: object) -> int:
        """Calcula e retorna o deslocamento vertical da raquete para o frame atual."""
        ...


class IMotorFisico(Protocol):
    """Contrato para motor de física responsável por colisões."""

    def handle_paddle_collision(self, ball: object, paddle_left: object, paddle_right: object) -> bool:
        """Trata colisão da bola com as raquetes. Retorna True se houve colisão."""
        ...

    def handle_wall_collision(self, ball: object, screen_height: int) -> bool:
        """Trata colisão da bola com as paredes. Retorna True se houve colisão."""
        ...


class IEntradaJogador(Protocol):
    """Contrato para leitura de entrada do jogador."""

    def get_player_dy(self, paddle_speed: int, pressed_keys: Sequence[bool]) -> int:
        """Retorna deslocamento vertical do jogador com base nas teclas pressionadas."""
        ...

    def get_quit_event(self, events: Sequence[object]) -> bool:
        """Retorna True quando evento de encerramento da janela for detectado."""
        ...


class IRenderizador(Protocol):
    """Contrato para renderização dos elementos visuais do jogo."""

    def clear(self) -> None:
        """Limpa a tela."""
        ...

    def draw_paddle(self, paddle: object) -> None:
        """Desenha uma raquete na tela."""
        ...

    def draw_ball(self, ball: object) -> None:
        """Desenha a bola na tela."""
        ...

    def flip(self) -> None:
        """Apresenta o frame atual na janela."""
        ...


class IHUD(Protocol):
    """Contrato para exibição de informações de interface (placar)."""

    def draw_score(self, player_1_score: int, player_2_score: int) -> None:
        """Desenha o placar na tela."""
        ...
