"""Elementos de HUD (placar) para o jogo Ping-Pong."""

from __future__ import annotations
from typing import Any


class HUD:
    """Renderiza informações de interface, como pontuação."""

    def __init__(
        self,
        screen: Any,
        font_factory: Any,
        text_color: tuple[int, int, int],
        center_x: int,
        score_y: int = 30,
    ) -> None:
        """Inicializa o HUD com dependências e posicionamento padrão."""
        self.screen = screen
        self.font = font_factory(None, 36)
        self.text_color = text_color
        self.center_x = center_x
        self.score_y = score_y

    def draw_score(self, player_1_score: int, player_2_score: int) -> None:
        """Desenha o placar no topo da tela."""
        score_text = self.font.render(f"{player_1_score} - {player_2_score}", True, self.text_color)
        self.screen.blit(score_text, score_text.get_rect(center=(self.center_x, self.score_y)))
