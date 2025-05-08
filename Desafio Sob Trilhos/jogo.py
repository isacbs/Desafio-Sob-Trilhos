import pygame
import random
import time

pygame.init()

# Dimensões
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Desafio Sob Trilhos")

# Imagens
menu_image = pygame.transform.scale(pygame.image.load("imgs/menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
historia_image = pygame.transform.scale(pygame.image.load("imgs/historia.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
integrantes_image = pygame.transform.scale(pygame.image.load("imgs/integrantes.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
parte_inicial_image = pygame.transform.scale(pygame.image.load("imgs/parte_inicial.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_image = pygame.transform.scale(pygame.image.load("imgs/game_over.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Protagonista
prota_img = pygame.transform.scale(pygame.image.load("imgs/prota_parada.png"), (50, 50))
prota_andando_img = pygame.transform.scale(pygame.image.load("imgs/prota_parada.png"), (50, 50))
prota_pensando_img = pygame.transform.scale(pygame.image.load("imgs/prota_pensando.png"), (50, 50))

# NPCs
npc_images = [pygame.transform.scale(pygame.image.load(f"imgs/npc{i}.png"), (40, 40)) for i in range(1, 7)]

clock = pygame.time.Clock()

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(npc_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 40)
        self.speed = random.choice([0.5, 1, 1.5])
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        if random.randint(0, 100) < 2:
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - 40))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - 40))

class Protagonista(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = prota_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.speed = 3
        self.last_move_time = time.time()

    def update(self, keys_pressed, npc_group):
        old_pos = self.rect.topleft
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed

        for npc in npc_group:
            if self.rect.colliderect(npc.rect):
                self.speed = 1
                break
        else:
            self.speed = 3

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - 50))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - 50))

        if self.rect.topleft != old_pos:
            self.last_move_time = time.time()

def fase_facil():
    prota = Protagonista()
    npc_group = pygame.sprite.Group()
    for _ in range(6):
        npc_group.add(NPC())

    all_sprites = pygame.sprite.Group()
    all_sprites.add(prota)
    all_sprites.add(npc_group)

    running = True
    start_time = time.time()

    while running:
        screen.blit(parte_inicial_image, (0, 0))
        keys = pygame.key.get_pressed()
        prota.update(keys, npc_group)
        npc_group.update()

        if time.time() - prota.last_move_time > 3:
            screen.blit(prota_pensando_img, (prota.rect.x, prota.rect.y - 60))

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if prota.rect.y < 10:
            menu()
            return

        if time.time() - start_time > 60:
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
                    print("Botão Sobre Nós pressionado")
                    sobre_nos()
                    return

                elif button_start_rect.collidepoint(mouse_pos):
                    print("Botão Iniciar Aqui pressionado")
                    fase_facil()
                    return

                elif button_group_rect.collidepoint(mouse_pos):
                    print("Botão Grupo pressionado")
                    integrantes()
                    return


menu()
