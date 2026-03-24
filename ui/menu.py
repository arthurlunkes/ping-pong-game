"""Tela de menu principal do jogo Ping-Pong."""

from __future__ import annotations
from typing import Any


class MenuScreen:
    """Controla loop e renderização do menu inicial."""

    def __init__(
        self,
        screen: Any,
        event_api: Any,
        display_api: Any,
        time_api: Any,
        font_factory: Any,
        title: str,
        background_color: tuple[int, int, int],
        foreground_color: tuple[int, int, int],
        screen_width: int,
        screen_height: int,
        quit_event_type: int,
        keydown_event_type: int,
        start_key: int,
    ) -> None:
        """Inicializa dependências do menu e parâmetros visuais."""
        self.screen = screen
        self.event_api = event_api
        self.display_api = display_api
        self.time_api = time_api
        self.font_factory = font_factory
        self.title = title
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.quit_event_type = quit_event_type
        self.keydown_event_type = keydown_event_type
        self.start_key = start_key

        self.title_font = self.font_factory(None, 50)
        self.instruction_font = self.font_factory(None, 26)

    def run(self) -> bool:
        """Executa o loop do menu.

        Retorna:
        - True quando o usuário solicita iniciar a partida
        - False quando o usuário fecha a janela
        """
        while True:
            for event in self.event_api.get():
                if event.type == self.quit_event_type:
                    return False
                if event.type == self.keydown_event_type and getattr(event, "key", None) == self.start_key:
                    return True

            self.screen.fill(self.background_color)
            self._draw_title()
            self._draw_blinking_instruction()
            self.display_api.flip()

    def _draw_title(self) -> None:
        """Desenha o título centralizado na parte superior."""
        text = self.title_font.render(self.title, True, self.foreground_color)
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 4 + 50))
        self.screen.blit(text, text_rect)

    def _draw_blinking_instruction(self) -> None:
        """Desenha instrução piscando para iniciar o jogo."""
        tempo = self.time_api.get_ticks()
        if tempo % 2000 < 1000:
            instruction = self.instruction_font.render(
                "Pressione ESPACO para jogar", True, self.foreground_color
            )
            instruction_rect = instruction.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 + 60)
            )
            self.screen.blit(instruction, instruction_rect)
