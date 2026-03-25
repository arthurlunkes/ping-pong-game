"""Orquestrador principal do jogo Ping-Pong.

Este módulo define a classe Game, que coordena as interações entre todas
as camadas: física, IA, entrada, renderização e regras de pontuação.
"""

from __future__ import annotations
import random
from typing import Any

import config
from game.entities import Ball, DecoyBall, Paddle
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

        # Estado do power-up temporal de fragmentação
        self.elapsed_ms = 0
        self.last_fragment_ms = 0
        self.decoy_balls: list[DecoyBall] = []
        self.true_ball_color = (255, 255, 255)

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
                self.elapsed_ms += self.clock.get_time()

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

        # Física da bola verdadeira: movimento, colisão com raquetes e paredes
        self.ball.update()
        paddle_collision = self.physics.handle_paddle_collision(self.ball, self.player1, self.player2)
        if paddle_collision:
            if self.audio:
                self.audio.tocar_colisao_raquete()
            self._try_fragment_on_paddle_collision()

        if self.physics.handle_wall_collision(self.ball, self.screen_height):
            if self.audio:
                self.audio.tocar_colisao_parede()

        # Física das bolas distrativas (não pontuam)
        self._update_decoy_balls()

    def _try_fragment_on_paddle_collision(self) -> None:
        """Fragmenta em 4 bolas quando houver colisão e o intervalo de tempo for atingido."""
        if self.elapsed_ms - self.last_fragment_ms < config.BALL_FRAGMENT_INTERVAL_MS:
            return

        self.last_fragment_ms = self.elapsed_ms
        fragment_total = max(2, config.BALL_FRAGMENT_TOTAL)
        colors = self._generate_unique_colors(fragment_total)
        true_index = random.randrange(fragment_total)

        new_true_ball: Ball | None = None
        new_decoys: list[DecoyBall] = []

        base_x = self.ball.x
        base_y = self.ball.y
        base_radius = self.ball.radius
        base_vx = self.ball.velocity_x
        base_vy = self.ball.velocity_y

        for idx in range(fragment_total):
            vel_x = self._randomized_velocity(base_vx, min_abs=2, variation=2)
            vel_y = self._randomized_velocity(base_vy, min_abs=1, variation=3)
            frag_ball = Ball(base_x, base_y, base_radius, vel_x, vel_y)

            if idx == true_index:
                new_true_ball = frag_ball
                self.true_ball_color = colors[idx]
            else:
                new_decoys.append(
                    DecoyBall(
                        x=frag_ball.x,
                        y=frag_ball.y,
                        radius=frag_ball.radius,
                        velocity_x=frag_ball.velocity_x,
                        velocity_y=frag_ball.velocity_y,
                        color=colors[idx],
                    )
                )

        if new_true_ball is not None:
            self.ball = new_true_ball
            self.decoy_balls = new_decoys

    def _update_decoy_balls(self) -> None:
        """Atualiza as bolas distrativas para manter pressão visual no jogador."""
        for decoy in self.decoy_balls:
            decoy.update()
            self.physics.handle_paddle_collision(decoy, self.player1, self.player2)
            self.physics.handle_wall_collision(decoy, self.screen_height)

            if decoy.x <= 0 or decoy.x >= self.screen_width - decoy.radius:
                decoy.reset(
                    self.screen_width // 2,
                    self.screen_height // 2,
                    velocity_x=self._randomized_velocity(self.initial_velocity_x, min_abs=2, variation=2),
                    velocity_y=self._randomized_velocity(self.initial_velocity_y, min_abs=1, variation=3),
                )

    @staticmethod
    def _randomized_velocity(base_velocity: int, min_abs: int, variation: int) -> int:
        """Retorna velocidade com variação aleatória preservando direção de base."""
        base_abs = max(min_abs, abs(base_velocity))
        varied_abs = max(min_abs, base_abs + random.randint(-variation, variation))
        sign = -1 if base_velocity < 0 else 1

        if random.random() < 0.35:
            sign *= -1

        return sign * varied_abs

    @staticmethod
    def _generate_unique_colors(total: int) -> list[tuple[int, int, int]]:
        """Gera uma lista de cores RGB únicas e aleatórias."""
        colors: set[tuple[int, int, int]] = set()
        while len(colors) < total:
            colors.add(
                (
                    random.randint(40, 255),
                    random.randint(40, 255),
                    random.randint(40, 255),
                )
            )
        return list(colors)

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
        """Reposiciona a bola verdadeira no centro e limpa distrações ativas."""
        self.decoy_balls.clear()
        self.true_ball_color = (255, 255, 255)
        self.ball.reset(
            self.screen_width // 2,
            self.screen_height // 2,
            velocity_x=self.initial_velocity_x,
            velocity_y=self.initial_velocity_y,
        )
        self.ball.invert_x()

    def _renderizar(self) -> None:
        """Renderiza todos os elementos visuais do frame atual."""
        self.renderer.clear()
        self.renderer.draw_paddle(self.player1)
        self.renderer.draw_paddle(self.player2)
        self.renderer.draw_ball(self.ball, self.true_ball_color)
        for decoy in self.decoy_balls:
            self.renderer.draw_ball(decoy, decoy.color)
        self.hud.draw_score(self.score_player1, self.score_player2)
        self.renderer.flip()
