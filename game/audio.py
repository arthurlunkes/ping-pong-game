"""Gerenciamento de áudio do jogo Ping-Pong.

Carrega os efeitos sonoros da pasta sons/ localizada na raiz do projeto.
"""

from __future__ import annotations

import pathlib
import pygame.mixer

_SONS_DIR = pathlib.Path(__file__).resolve().parent.parent / "sons"


class AudioManager:
    """Gerencia efeitos sonoros do jogo."""

    def __init__(self) -> None:
        self._som_raquete     = pygame.mixer.Sound(str(_SONS_DIR / "ball_raquete_barulho.mp3"))
        self._som_parede      = pygame.mixer.Sound(str(_SONS_DIR / "barulho_ball_parede.mp3"))
        self._som_gol         = pygame.mixer.Sound(str(_SONS_DIR / "player_perdeabola.mp3"))
        self._som_player_win  = pygame.mixer.Sound(str(_SONS_DIR / "player1_win.mp3"))
        self._som_player_lose = pygame.mixer.Sound(str(_SONS_DIR / "player1_lose.mp3"))

    def tocar_colisao_raquete(self) -> None:
        """Toca som de colisão da bola com a raquete."""
        self._som_raquete.play()

    def tocar_colisao_parede(self) -> None:
        """Toca som de colisão da bola com a parede."""
        self._som_parede.play()

    def tocar_gol(self) -> None:
        """Toca alerta sonoro de marcação de ponto."""
        self._som_gol.play()

    def iniciar_musica(self) -> None:
        """Sem implementação — música de fundo removida."""
    
    def tocar_vitoria_jogador(self) -> None:
        """Toca som de vitória de um jogador."""
        self._som_player_win.play()

    def tocar_derrota_jogador(self) -> None:
        """Toca som de derrota de um jogador."""
        self._som_player_lose.play()

    def parar_musica(self) -> None:
        """Sem implementação — música de fundo removida."""
