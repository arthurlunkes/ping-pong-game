"""Orquestrador principal do jogo Ping-Pong.

Este módulo define a classe Game, que coordena as interações entre todas
as camadas: física, IA, entrada, renderização e regras de pontuação.
"""

from __future__ import annotations
from typing import Any
from game.entities import Ball, Paddle
from game.protocols import IAudioManager, IControladorIA, IEntradaJogador, IHUD, IMotorFisico, IRenderizador


class Game:
    """Coordena o loop de jogo e as interações entre entidades e responsabilidades."""

    def __init__(
        self,
        player1: Paddle,
        player2: Paddle,
        ball: Ball,
        renderer: IRenderizador,
        hud: IHUD,
        ai: IControladorIA,
        input_handler: IEntradaJogador,
        physics: IMotorFisico,
        clock: Any,
        event_api: Any,
        key_api: Any,
        fps: int,
        screen_width: int,
        screen_height: int,
        win_score_player1: int,
        win_score_player2: int,
        audio: IAudioManager | None = None,
    ) -> None:
        """Inicializa o jogo com todas as dependências injetadas via abstrações (DIP)."""
        self.player1 = player1
        self.player2 = player2
        self.ball = ball
        self.renderer = renderer
        self.hud = hud
        self.ai = ai
        self.input_handler = input_handler
        self.physics = physics
        self.clock = clock
        self.event_api = event_api
        self.key_api = key_api
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.win_score_player1 = win_score_player1
        self.win_score_player2 = win_score_player2
        self.audio = audio

        self.score_player1 = 0
        self.score_player2 = 0
        
        # Guarda velocidades iniciais para restaurar após cada gol
        self.initial_velocity_x = ball.velocity_x
        self.initial_velocity_y = ball.velocity_y

    def run(self) -> bool:
        """Executa o loop principal da partida.

        Retorna:
            True quando a partida termina por pontuação (permite voltar ao menu).
            False quando o usuário fecha a janela.
        """
        if self.audio:
            self.audio.iniciar_musica()
        try:
            while True:
                events = list(self.event_api.get())

                if self.input_handler.get_quit_event(events):
                    return False

                self._update()

                resultado = self._verificar_pontuacao()
                if resultado is not None:
                    return resultado

                self._renderizar()
                self.clock.tick(self.fps)
        finally:
            if self.audio:
                self.audio.parar_musica()

    def _update(self) -> None:
        """Atualiza posições e estado do jogo para o frame atual."""
        # Movimento do jogador controlado pelo teclado
        pressed_keys = self.key_api.get_pressed()
        dy_player = self.input_handler.get_player_dy(self.player1.speed, pressed_keys)
        self.player1.move(dy_player)
        self.player1.clamp_to_screen(self.screen_height)

        # Movimento da raquete controlada pela IA
        dy_ia = self.ai.compute_move(self.player2, self.ball)
        self.player2.move(dy_ia)
        self.player2.clamp_to_screen(self.screen_height)

        # Física da bola: movimento, colisão com raquetes e paredes
        self.ball.update()
        if self.physics.handle_paddle_collision(self.ball, self.player1, self.player2):
            if self.audio:
                self.audio.tocar_colisao_raquete()
        if self.physics.handle_wall_collision(self.ball, self.screen_height):
            if self.audio:
                self.audio.tocar_colisao_parede()

    def _verificar_pontuacao(self) -> bool | None:
        """Verifica se algum jogador marcou ponto e atualiza o placar.

        Retorna:
            True se a partida terminou por critério de vitória.
            None se o jogo deve continuar no próximo frame.
        """
        # Bola saiu pela esquerda: ponto para o jogador 2
        if self.ball.x <= 0:
            self.score_player2 += 1
            if self.audio:
                self.audio.tocar_gol()
            self._resetar_bola()
            if self.score_player2 >= self.win_score_player2:
                if self.audio:
                    self.audio.tocar_derrota_jogador()
                return True

        # Bola saiu pela direita: ponto para o jogador 1
        elif self.ball.x >= self.screen_width - self.ball.radius:
            self.score_player1 += 1
            if self.audio:
                self.audio.tocar_gol()
            self._resetar_bola()
            if self.score_player1 >= self.win_score_player1:
                if self.audio:
                    self.audio.tocar_vitoria_jogador()
                return True

        return None

    def _resetar_bola(self) -> None:
        """Reposiciona a bola no centro e restaura velocidades iniciais.
        
        Inverte a direção horizontal, mantendo a degradação da velocidade
        causada por variações aleatórias nas colisões. As velocidades iniciais
        são restauradas cada vez que a bola é resetada após um gol.
        """
        self.ball.reset(
            self.screen_width // 2, 
            self.screen_height // 2,
            velocity_x=self.initial_velocity_x,
            velocity_y=self.initial_velocity_y
        )
        self.ball.invert_x()

    def _renderizar(self) -> None:
        """Renderiza todos os elementos visuais do frame atual."""
        self.renderer.clear()
        self.renderer.draw_paddle(self.player1)
        self.renderer.draw_paddle(self.player2)
        self.renderer.draw_ball(self.ball)
        self.hud.draw_score(self.score_player1, self.score_player2)
        self.renderer.flip()
