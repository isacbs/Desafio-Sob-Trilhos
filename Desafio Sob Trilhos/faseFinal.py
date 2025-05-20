import pygame
import random
import time
import os
from ranking import ranking

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.image = random.choice(images)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.inflate_ip(-80, 0)
        self.speed = random.choice([-2, 2])
        self.original_speed = self.speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > 800:
            self.speed *= -1

def show_quiz_screen():
    screen = pygame.display.set_mode((800, 600))
    try:
        background = pygame.image.load(os.path.join("imgs", "quizcerto.png")).convert()
        background = pygame.transform.scale(background, (800, 600))
    except:
        background = pygame.Surface((800, 600))
        background.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

        screen.blit(background, (0, 0))
        pygame.display.flip()

def fase_final(player_name=None, tempo_acumulado=0):
    pygame.init()
    pygame.mixer.init()

    BASE_DIR = os.path.dirname(__file__)
    IMG_DIR = os.path.join(BASE_DIR, "imgs")

    # Imagens
    prota_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_parada.png")), (100, 100))
    prota_andando = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_andando.png")), (100, 100))
    parte_final_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "parte_final.png")), (800, 600))

    npc_images = [
        pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, f"npc{i}.png")), (100, 100))
        for i in range(1, 7)
    ]

    pygame.mixer.music.load(os.path.join(BASE_DIR, "sons", "estacao.mp3"))
    pygame.mixer.music.play(-1)

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fase Final - Desafio Sob Trilhos")

    prota = pygame.Rect(400, 500, 100, 100)
    speed = 5
    current_prota_img = prota_img
    prota_previous_pos = prota.copy()

    obstaculos = [
        pygame.Rect(35, 345, 60, 90),
        pygame.Rect(185, 345, 40, 100),
        pygame.Rect(240, 345, 110, 100),
        pygame.Rect(400, 420, 20, 60),
        pygame.Rect(480, 465, 20, 10),
        pygame.Rect(640, 315, 100, 100),
        pygame.Rect(540, 360, 1, 1),
        pygame.Rect(580, 200, 200, 100),
        pygame.Rect(10, 200, 200, 100),
        pygame.Rect(350, 180, 200, 100),
    ]

    #Área de vitória
    ganhar_area = pygame.Rect(350, 300, 1, 1)

    tempo_limite = 180
    start_time = time.time()

    font = pygame.font.SysFont("Arial", 30)
    AMARELO = (253, 214, 3)

    npcs = pygame.sprite.Group()
    for i in range(5):
        x = random.randint(50, 700)
        y = random.randint(420, 540)
        npc = NPC(x, y, npc_images)
        npcs.add(npc)

    running = True
    clock = pygame.time.Clock()

    while running:
        tempo_restante = max(0, int(tempo_limite - (time.time() - start_time)))

        if tempo_restante <= 0:
            pygame.display.flip()
            pygame.time.wait(3000)
            
            return fase_final(player_name, tempo_acumulado)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        prota_previous_pos.x = prota.x
        prota_previous_pos.y = prota.y

        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_LEFT]:
            prota.x -= speed
            moving = True
        if keys[pygame.K_RIGHT]:
            prota.x += speed
            moving = True
        if keys[pygame.K_UP]:
            prota.y -= speed
            moving = True
        if keys[pygame.K_DOWN]:
            prota.y += speed
            moving = True

        current_prota_img = prota_andando if moving else prota_img

        #Colisão com NPCs
        for npc in npcs:
            if prota.colliderect(npc.rect):
                prota.x = prota_previous_pos.x
                prota.y = prota_previous_pos.y
                break

        #Colisão com obstáculos
        for obstaculo in obstaculos:
            if prota.colliderect(obstaculo):
                prota.x = prota_previous_pos.x
                prota.y = prota_previous_pos.y
                break

        prota.x = max(0, min(prota.x, SCREEN_WIDTH - prota.width))
        prota.y = max(0, min(prota.y, SCREEN_HEIGHT - prota.height))

        npcs.update()

        screen.blit(parte_final_img, (0, 0))
        screen.blit(current_prota_img, prota)
        npcs.draw(screen)

        tempo_text = font.render(f"Tempo: {tempo_restante}s", True, AMARELO)
        screen.blit(tempo_text, (20, 20))
        if player_name:
            name_text = font.render(f"Jogador: {player_name}", True, AMARELO)
            screen.blit(name_text, (20, 60))

        pygame.display.flip()

        #Verificação de vitória
        if prota.colliderect(ganhar_area):
            tempo_total = tempo_acumulado + (time.time() - start_time)
            venceu_text = font.render("Você venceu!", True, AMARELO)
            screen.blit(venceu_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)

            # Mostra a tela do quiz e espera ENTER
            if show_quiz_screen():
                from quiz import run_quiz
                run_quiz(player_name, tempo_total)
                return ranking(player_name, tempo_total)

        clock.tick(60)

if __name__ == "__main__":
    fase_final()
