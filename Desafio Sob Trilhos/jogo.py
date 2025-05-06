import pygame

# Inicialização do pygame
pygame.init()

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Desafio Sob Trilhos")

# Imagens
menu_image = pygame.image.load("imgs/menu.png")
historia_image = pygame.image.load("imgs/historia.png")
integrantes_image = pygame.image.load("imgs/integrantes.png")
npc_images = [pygame.image.load(f"imgs/npc{i}.jpg") for i in range(1, 7)]
parte_inicial_image = pygame.image.load("imgs/parte_inicial.png")
game_over_image = pygame.image.load("imgs/game_over.png")
prota_andando_image = pygame.image.load("imgs/prota_andando.png")
prota_parada_image = pygame.image.load("imgs/prota_parada.png")
prota_pensando_image = pygame.image.load("imgs/prota_pensando.png")

# Redimensionando as telas de fundo
menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
historia_image = pygame.transform.scale(historia_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
parte_inicial_image = pygame.transform.scale(parte_inicial_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)