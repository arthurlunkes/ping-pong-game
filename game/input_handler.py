"""Camada de leitura de entrada para o jogo Ping-Pong.

Este módulo isola o acesso ao teclado e aos eventos de saída.
"""

from __future__ import annotations
from collections.abc import Sequence
from typing import Protocol


class EventLike(Protocol):
    """Protocolo mínimo para eventos com atributo de tipo."""

    type: int


class InputHandler:
    """Centraliza leitura de entrada do jogador local."""

    def __init__(self, up_key: int, down_key: int, quit_event_type: int) -> None:
        """Configura teclas de movimentação e tipo de evento de saída."""
        self.up_key = up_key
        self.down_key = down_key
        self.quit_event_type = quit_event_type

    def get_player_dy(self, paddle_speed: int, pressed_keys: Sequence[bool]) -> int:
        """Retorna deslocamento vertical do jogador com base no estado das teclas."""

        delta_y = 0
        if pressed_keys[self.up_key]:
            delta_y -= paddle_speed
        if pressed_keys[self.down_key]:
            delta_y += paddle_speed
        return delta_y

    def get_quit_event(self, events: Sequence[EventLike]) -> bool:
        """Retorna True quando houver evento de encerramento da janela."""
        return any(event.type == self.quit_event_type for event in events)
