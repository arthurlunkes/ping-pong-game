"""Motor de física do jogo Ping-Pong.

Este módulo concentra as regras de colisão e limites do campo,
separando a lógica física do restante da aplicação.
"""

from __future__ import annotations

import random

from game.entities import Ball, Paddle


class PhysicsEngine:
    """Encapsula regras de colisão entre bola, raquetes e paredes."""

    @staticmethod
    def _intersect(rect_a: tuple[int, int, int, int], rect_b: tuple[int, int, int, int]) -> bool:
        """Retorna True quando dois retângulos (x, y, largura, altura) se interceptam."""
        ax, ay, aw, ah = rect_a
        bx, by, bw, bh = rect_b

        return (
            ax < bx + bw
            and ax + aw > bx
            and ay < by + bh
            and ay + ah > by
        )

    def check_paddle_collision(self, ball: Ball, paddle: Paddle) -> bool:
        """Verifica se a bola colidiu com uma raquete."""
        return self._intersect(ball.rect, paddle.rect)

    @staticmethod
    def _apply_angle_variation(ball: Ball, variation_range: float = 0.4) -> None:
        """Aplica variação aleatória no ângulo de saída da bola.

        A variação é aplicada ao velocity_y, criando rebotes impredizíveis.
        O parâmetro variation_range (padrão 0.4 = ±40%) controla a amplitude.
        Garante que velocity_y nunca fique zero ou muito pequeno.
        """
        factor = random.uniform(1.0 - variation_range, 1.0 + variation_range)
        new_velocity = int(ball.velocity_y * factor)
        # Garante mínimo de ±1 para evitar que velocity_y fique zero
        if new_velocity == 0:
            new_velocity = 1 if ball.velocity_y > 0 else -1
        ball.velocity_y = new_velocity

    def handle_paddle_collision(self, ball: Ball, paddle_left: Paddle, paddle_right: Paddle) -> bool:
        """Inverte eixo X da bola quando houver colisão com qualquer raquete.

        Após a colisão, reposiciona a bola para fora da raquete para evitar travamento.
        Aplica variação aleatória ao ângulo de saída para imprevisibilidade.
        Retorna True quando a colisão foi detectada e tratada.
        """
        if self.check_paddle_collision(ball, paddle_left):
            ball.invert_x()
            self._apply_angle_variation(ball, variation_range=0.6)
            # Reposiciona a bola para fora da raquete esquerda
            ball.x = paddle_left.x + paddle_left.width + 1
            return True
        elif self.check_paddle_collision(ball, paddle_right):
            ball.invert_x()
            self._apply_angle_variation(ball, variation_range=0.6)
            # Reposiciona a bola para fora da raquete direita
            ball.x = paddle_right.x - ball.radius - 1
            return True
        return False

    def handle_wall_collision(self, ball: Ball, screen_height: int) -> bool:
        """Inverte eixo Y da bola quando houver colisão nas bordas superior/inferior.

        Aplica variação aleatória ao ângulo de saída para imprevisibilidade.
        A lógica preserva o comportamento original, que considera o tamanho da bola
        com base em seu atributo de raio.
        """
        top_limit = 0
        bottom_limit = screen_height - ball.radius

        if ball.y <= top_limit:
            # Reposiciona para dentro da tela e força movimento para baixo.
            ball.y = top_limit
            ball.velocity_y = abs(ball.velocity_y)
            self._apply_angle_variation(ball, variation_range=0.6)
            return True

        if ball.y >= bottom_limit:
            # Reposiciona para dentro da tela e força movimento para cima.
            ball.y = bottom_limit
            ball.velocity_y = -abs(ball.velocity_y)
            self._apply_angle_variation(ball, variation_range=0.6)
            return True

        return False
