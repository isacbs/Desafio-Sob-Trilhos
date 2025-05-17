import pygame
import random
import time
import os
from faseMedia import fase_media
from ranking import ranking

pygame.init()

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "imgs")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Desafio Sob Trilhos")

font = pygame.font.SysFont("Arial", 32)
font_input = pygame.font.SysFont("Arial", 40)

# Carregamento de imagens
menu_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "menu.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
historia_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "sobre.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
integrantes_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "integrantes.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
parte_inicial_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "parte_inicial.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "game_over.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Nova imagem para a tela do nome
nome_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "nome.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))

prota_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_parada.png")), (100, 100))
prota_andando_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_andando.png")), (100, 100))
prota_pensando_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_pensando.png")), (100, 100))
npc_images = [pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, f"npc{i}.png")), (100, 100)) for i in range(1, 7)]

clock = pygame.time.Clock()

# Áreas de colisão (totalmente transparentes)
COLLISION_AREA_LEFT = pygame.Rect(0, 300, 400, 100)
COLLISION_AREA_RIGHT = pygame.Rect(500, 300, 300, 100)
PASSAGEM_VERDE = pygame.Rect(400, 300, 100, 100)

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(npc_images)
        self.rect = self.image.get_rect()
        # Spawn em qualquer lugar da tela
        self.rect.x = random.randint(0, SCREEN_WIDTH - 100)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 100)
        self.speed = random.choice([2, 2.5, 3])
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.change_direction_time = time.time()

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - 100))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - 100))

        if time.time() - self.change_direction_time > random.uniform(2, 5):
            self.direction = random.choice(['up', 'down', 'left', 'right'])
            self.change_direction_time = time.time()

        if self.rect.x <= 0:
            self.direction = 'right'
        elif self.rect.x >= SCREEN_WIDTH - 100:
            self.direction = 'left'
        if self.rect.y <= 0:
            self.direction = 'down'
        elif self.rect.y >= SCREEN_HEIGHT - 100:
            self.direction = 'up'

class Protagonista(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = prota_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.speed = 3
        self.base_speed = 3
        self.last_move_time = time.time()
        self.last_position = self.rect.copy()

    def update(self, keys_pressed, npc_group):
        moved = False
        self.last_position = self.rect.copy()

        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
            moved = True
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            moved = True
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            moved = True
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            moved = True

        for npc in npc_group:
            if self.rect.colliderect(npc.rect):
                self.speed = 0.5
                break
        else:
            self.speed = self.base_speed

        if (self.rect.colliderect(COLLISION_AREA_LEFT) or
            self.rect.colliderect(COLLISION_AREA_RIGHT)) and \
            not self.rect.colliderect(PASSAGEM_VERDE):
            self.rect = self.last_position

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - 50))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - 50))

        if moved:
            self.last_move_time = time.time()
            self.image = prota_andando_img
        else:
            if time.time() - self.last_move_time > 5:
                self.image = prota_pensando_img
            else:
                self.image = prota_img

def tela_nome():
    """
    
    Tela para digitar o nome do jogador.
    Exibe imagem 'nome.png' em tela cheia com quadrante azul para digitação.
    O jogador digita seu nome e pressiona S para iniciar o jogo.
    """
    input_text = ""
    running = True

    input_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 40, 400, 80)
    color_active = (0, 0, 255)   # Azul
    color = color_active

    while running:
        screen.blit(nome_image, (0, 0))

        # Renderiza o texto digitado um pouco mais para cima
        txt_surface = font_input.render(input_text, True, (255, 255, 255))
        # Posiciona o texto cerca de 20 pixels acima do centro vertical do quadrante azul
        text_pos = txt_surface.get_rect(center=(input_rect.centerx, input_rect.centery - 20))
        screen.blit(txt_surface, text_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_s:
                    if len(input_text.strip()) > 0:
                        fase_facil(player_name=input_text.strip())
                        return
                else:
                    if len(input_text) < 20 and event.unicode.isprintable():
                        input_text += event.unicode

        clock.tick(60)


def fase_facil(player_name=None):
    AMARELO = (253, 214, 3)
    prota = Protagonista()
    npc_group = pygame.sprite.Group([NPC() for _ in range(6)])
    all_sprites = pygame.sprite.Group([prota] + list(npc_group))

    tempo_limite = 60
    start_time = time.time()
    running = True

    while running:
        tempo_restante = max(0, int(tempo_limite - (time.time() - start_time)))
        screen.blit(parte_inicial_image, (0, 0))

        timer_text = font.render(f"Tempo: {tempo_restante}s", True, AMARELO)
        screen.blit(timer_text, (20, 20))

        if player_name:
            name_text = font.render(f"Jogador: {player_name}", True, AMARELO)
            screen.blit(name_text, (20, 60))

        keys = pygame.key.get_pressed()
        prota.update(keys, npc_group)
        npc_group.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if prota.rect.y < 10:
            total_tempo = time.time() - start_time
            fase_media(player_name=player_name, tempo_acumulado=total_tempo)
            return

        if tempo_restante <= 0:
            tela_game_over()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
def tela_game_over():
    running = True
    while running:
        screen.blit(game_over_image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
                menu()

def sobre_nos():
    running = True
    while running:
        screen.blit(historia_image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 30 <= x <= 80 and 520 <= y <= 570:
                    menu()
                    return

def integrantes():
    running = True
    while running:
        screen.blit(integrantes_image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 30 <= x <= 80 and 520 <= y <= 570:
                    menu()
                    return

def menu():
    running = True
    button_width = 100
    button_height = 50
    button_spacing = 20
    total_width = (3 * button_width) + (2 * button_spacing)
    start_x = (SCREEN_WIDTH - total_width) // 2

    button_about_rect = pygame.Rect(start_x, SCREEN_HEIGHT - 100, button_width, button_height)
    button_start_rect = pygame.Rect(start_x + button_width + button_spacing, SCREEN_HEIGHT - 100, button_width, button_height)
    button_group_rect = pygame.Rect(start_x + 2 * (button_width + button_spacing), SCREEN_HEIGHT - 100, button_width, button_height)

    while running:
        screen.blit(menu_image, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_about_rect.collidepoint(mouse_pos):
                    sobre_nos()
                    return
                elif button_start_rect.collidepoint(mouse_pos):
                    # Ao invés de ir direto para fase_facil, chama tela_nome
                    tela_nome()
                    return
                elif button_group_rect.collidepoint(mouse_pos):
                    integrantes()
                    return

        clock.tick(60)

menu()