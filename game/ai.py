"""Controlador de IA para a raquete adversária.

Este módulo abstrai a tomada de decisão da raquete controlada pelo
computador e permite evoluir regras por dificuldade sem alterar o núcleo.
"""

from __future__ import annotations

from game.entities import Ball, Paddle


class AIController:
    """Controla o movimento vertical da raquete da IA."""

    def __init__(self, difficulty: str = "medium") -> None:
        """Inicializa a IA com um nível de dificuldade.

        Dificuldades suportadas nesta fase:
        - easy
        - medium
        - hard
        """
        self.difficulty = difficulty

    def _step_by_difficulty(self, default_speed: int) -> int:
        """Retorna passo de movimento conforme dificuldade configurada."""
        if self.difficulty == "easy":
            return max(1, default_speed - 2)
        if self.difficulty == "hard":
            return default_speed + 2
        return default_speed

    def compute_move(self, paddle: Paddle, ball: Ball) -> int:
        """Calcula deslocamento vertical da IA para o frame atual.

        Retorna:
        - valor positivo para descer
        - valor negativo para subir
        - zero para manter posição
        """
        step = self._step_by_difficulty(paddle.speed)

        if paddle.center_y < ball.y:
            return step
        if paddle.center_y > ball.y:
            return -step
        return 0
