"""Motor de física do jogo Ping-Pong.

Este módulo concentra as regras de colisão e limites do campo,
separando a lógica física do restante da aplicação.
"""

from __future__ import annotations

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

    def handle_paddle_collision(self, ball: Ball, paddle_left: Paddle, paddle_right: Paddle) -> bool:
        """Inverte eixo X da bola quando houver colisão com qualquer raquete.

        Retorna True quando a colisão foi detectada e tratada.
        """
        collided = self.check_paddle_collision(ball, paddle_left) or self.check_paddle_collision(
            ball, paddle_right
        )
        if collided:
            ball.invert_x()
        return collided

    def handle_wall_collision(self, ball: Ball, screen_height: int) -> bool:
        """Inverte eixo Y da bola quando houver colisão nas bordas superior/inferior.

        A lógica preserva o comportamento original, que considera o tamanho da bola
        com base em seu atributo de raio.
        """
        hit_wall = ball.y <= 0 or ball.y >= screen_height - ball.radius
        if hit_wall:
            ball.invert_y()
        return hit_wall
