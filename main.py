import pygame
import sys

pygame.init()

PRETO=(0,0,0)
BRANCO=(255,255,255)

largura=800
altura=600

tela=pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Pong")


def menu_principal():
    while not False:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
               
        tela.fill(PRETO)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Pong", True, BRANCO)
        text_rect = text.get_rect(center=(largura//2, altura//4+50))
        tela.blit(text, text_rect)

        font_blynk = pygame.font.SysFont(None, 26)
        tempo = pygame.time.get_ticks()
        if tempo %2000<1000:
            text_blynk = font_blynk.render("Pressione ESPAÇO para jogar",
                                           True,
                                           BRANCO)
            text_blynk_rect = text_blynk.get_rect(center=(largura//2,
                                                           altura//2+60))
            tela.blit(text_blynk, text_blynk_rect)

        pygame.display.flip()


def game():
    clock=pygame.time.Clock()
    raquete_largura=10
    raquete_altura=60
    tamanho_bola=7

    player1_x =15
    player1_y = altura//2- raquete_altura//2

    player_2 = largura -15- raquete_largura
    player_2_y = altura//2- raquete_altura//2

    bola_x = largura//2- tamanho_bola//2
    bola_y = altura//2- tamanho_bola//2


    velocidade_bola_x =5
    velocidade_bola_y =5

    score_player1 =0
    score_player2 =0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return True

        tela.fill(PRETO)
   
        bola_x += velocidade_bola_x
        bola_y += velocidade_bola_y

        bola_rect = pygame.Rect(bola_x, bola_y, tamanho_bola, tamanho_bola)
        player1_rect = pygame.Rect(player1_x,
                                    player1_y,
                                    raquete_largura,
                                    raquete_altura)
   
        player_2_rect = pygame.Rect(player_2,
                                    player_2_y,
                                    raquete_largura,
                                    raquete_altura)
   
        if bola_rect.colliderect(player1_rect) or bola_rect.colliderect(player_2_rect):
            velocidade_bola_x =-velocidade_bola_x

        if bola_y <=0or bola_y >= altura - tamanho_bola:
            velocidade_bola_y =-velocidade_bola_y

        if bola_x <=0:
            score_player2 +=1
            bola_x = largura//2- tamanho_bola//2
            bola_y = altura//2- tamanho_bola//2
            velocidade_bola_x =-velocidade_bola_x
            print(f"Player 2: {score_player2}")
            if score_player2 >=2:
                print("Player 2 venceu!")
                return True
   
        if bola_x >= largura - tamanho_bola:
            score_player1 +=1
            bola_x = largura//2- tamanho_bola//2
            bola_y = altura//2- tamanho_bola//2
            velocidade_bola_x =-velocidade_bola_x
            print(f"Player 1: {score_player1}")
            if score_player1 >=10:
                print("Player 1 venceu!")
                return True

        if player_2_y + raquete_altura//2< bola_y:
            player_2_y +=5
        elif player_2_y + raquete_altura//2> bola_y:
            player_2_y -=5

        if player_2_y <0:
            player_2_y =0
        elif player_2_y > altura - raquete_altura:
            player_2_y = altura - raquete_altura

        pygame.draw.rect(tela, BRANCO, (player1_x,
                                        player1_y,
                                        raquete_largura,
                                        raquete_altura))
        pygame.draw.rect(tela, BRANCO, (player_2,
                                        player_2_y,
                                        raquete_largura,
                                        raquete_altura))
        pygame.draw.circle(tela, BRANCO, (bola_x, bola_y), tamanho_bola)

        font_score = pygame.font.SysFont(None, 36)
        score_text = font_score.render(f"{score_player1} - {score_player2}",
                                    True,
                                    BRANCO)
        tela.blit(score_text, score_text.get_rect(center=(largura//2, 30)))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player1_y >0:
            player1_y -=5
        if keys[pygame.K_DOWN] and player1_y < altura - raquete_altura:
            player1_y +=5

        pygame.display.flip()
        clock.tick(60)

def main():
    while True:
        if not menu_principal():
            break

        if not game():
            break

    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()