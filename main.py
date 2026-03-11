import random
import sys

import pygame

# Basic game settings
WIDTH, HEIGHT = 900, 500
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 14, 100
PADDLE_SPEED = 7
AI_PADDLE_SPEED = 6
BALL_SIZE = 16
BALL_SPEED_X = 5
BALL_SPEED_Y = 4
WIN_SCORE = 7


def reset_ball():
	"""Center the ball and launch it in a random direction."""
	ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
	vx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
	vy = random.choice([-BALL_SPEED_Y, -BALL_SPEED_Y + 1, BALL_SPEED_Y - 1, BALL_SPEED_Y])
	return ball, vx, vy


def clamp_paddle(paddle):
	if paddle.top < 0:
		paddle.top = 0
	if paddle.bottom > HEIGHT:
		paddle.bottom = HEIGHT


def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Pong 2D")
	clock = pygame.time.Clock()

	score_font = pygame.font.SysFont("consolas", 44)
	info_font = pygame.font.SysFont("consolas", 24)

	left_paddle = pygame.Rect(40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
	right_paddle = pygame.Rect(WIDTH - 40 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
	ball, ball_vx, ball_vy = reset_ball()

	left_score = 0
	right_score = 0
	running = True

	while running:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		keys = pygame.key.get_pressed()

		# Player controls: Up/Down arrows
		if keys[pygame.K_UP]:
			left_paddle.y -= PADDLE_SPEED
		if keys[pygame.K_DOWN]:
			left_paddle.y += PADDLE_SPEED

		# Computer paddle AI: follows the ball with a small dead zone.
		ai_center = right_paddle.centery
		if ai_center < ball.centery - 12:
			right_paddle.y += AI_PADDLE_SPEED
		elif ai_center > ball.centery + 12:
			right_paddle.y -= AI_PADDLE_SPEED

		clamp_paddle(left_paddle)
		clamp_paddle(right_paddle)

		# Ball movement
		ball.x += ball_vx
		ball.y += ball_vy

		# Bounce on top/bottom walls
		if ball.top <= 0 or ball.bottom >= HEIGHT:
			ball_vy *= -1

		# Bounce on paddles
		if ball.colliderect(left_paddle) and ball_vx < 0:
			ball.left = left_paddle.right
			ball_vx *= -1
		elif ball.colliderect(right_paddle) and ball_vx > 0:
			ball.right = right_paddle.left
			ball_vx *= -1

		# Scoring
		if ball.left <= 0:
			right_score += 1
			ball, ball_vx, ball_vy = reset_ball()
		elif ball.right >= WIDTH:
			left_score += 1
			ball, ball_vx, ball_vy = reset_ball()

		# Draw
		screen.fill((0, 0, 0))
		pygame.draw.rect(screen, (255, 255, 255), left_paddle)
		pygame.draw.rect(screen, (255, 255, 255), right_paddle)
		pygame.draw.ellipse(screen, (255, 255, 255), ball)
		pygame.draw.aaline(screen, (140, 140, 140), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

		score_text = score_font.render(f"{left_score}   {right_score}", True, (255, 255, 255))
		screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

		# End game and restart hints
		if left_score >= WIN_SCORE or right_score >= WIN_SCORE:
			winner = "Jogador" if left_score > right_score else "Computador"
			win_text = info_font.render(f"{winner} venceu! Pressione R para reiniciar", True, (255, 255, 255))
			screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT - 40))

			if keys[pygame.K_r]:
				left_score = 0
				right_score = 0
				ball, ball_vx, ball_vy = reset_ball()

		pygame.display.flip()

	pygame.quit()
	sys.exit()


if __name__ == "__main__":
	main()
