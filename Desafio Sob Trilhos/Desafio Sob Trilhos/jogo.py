import pygame
import random
import time
import os

# Inicializa o Pygame
pygame.init()

# Caminho base seguro, usado para acessar recursos como imagens
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "imgs")

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Define a tela
pygame.display.set_caption("Desafio Sob Trilhos")  # Define o título da janela

# Fonte utilizada para texto
font = pygame.font.SysFont("Arial", 32)

# Carregamento e redimensionamento das imagens
menu_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "menu.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
historia_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "sobre.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
integrantes_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "integrantes.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
parte_inicial_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "parte_inicial.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "game_over.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Imagens do protagonista (personagem principal)
prota_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_parada.png")), (100, 100))
prota_andando_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_andando.png")), (100, 100))
prota_pensando_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_pensando.png")), (100, 100))

# Imagens de NPCs (personagens não jogáveis)
npc_images = [pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, f"npc{i}.png")), (100, 100)) for i in range(1, 7)]

# Define o relógio para controlar a taxa de atualização do jogo
clock = pygame.time.Clock()

# Classe NPC, que controla o comportamento dos personagens não jogáveis
class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(npc_images)  # Escolhe uma imagem aleatória para o NPC
        self.rect = self.image.get_rect()  # Define o retângulo de colisão da imagem
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)  # Posição inicial aleatória
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 40)
        self.speed = random.choice([2, 2.5, 3])  # Velocidade aleatória
        self.direction = random.choice(['up', 'down', 'left', 'right'])  # Direção aleatória

    def update(self):
        # Atualiza a posição do NPC baseado na direção
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        # Aleatoriamente muda a direção do NPC
        if random.randint(0, 100) < 2:
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        # Limita a posição do NPC para que ele não ultrapasse os limites da tela
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - 40))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - 40))

# Classe Protagonista, que controla o movimento do personagem principal
class Protagonista(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = prota_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))  # Posiciona o protagonista na parte inferior da tela
        self.speed = 3
        self.last_move_time = time.time()  # Armazena o tempo do último movimento
        self.base_speed = 3

    def update(self, keys_pressed, npc_group):
        moved = False

        # Atualiza a posição com base nas teclas pressionadas
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

        # Checa colisão com NPCs, reduzindo a velocidade se houver colisão
        for npc in npc_group:
            if self.rect.colliderect(npc.rect):
                self.speed = 0.5
                break
        else:
            self.speed = self.base_speed

        # Limita a posição do protagonista para que ele não ultrapasse os limites da tela
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - 50))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - 50))

        # Atualiza a imagem com base no movimento
        if moved:
            self.last_move_time = time.time()
            self.image = prota_andando_img
        else:
            if time.time() - self.last_move_time > 5:
                self.image = prota_pensando_img  # Muda para a imagem pensando após 5 segundos de inatividade
            else:
                self.image = prota_img

# Função da fase fácil, onde o jogador controla o protagonista
def fase_facil():
    prota = Protagonista()
    npc_group = pygame.sprite.Group([NPC() for _ in range(6)])  # Cria 6 NPCs
    all_sprites = pygame.sprite.Group([prota] + list(npc_group))  # Agrupa todos os sprites

    tempo_limite = 60
    start_time = time.time()  # Marca o início do tempo
    running = True

    while running:
        tempo_restante = max(0, int(tempo_limite - (time.time() - start_time)))

        screen.blit(parte_inicial_image, (0, 0))  # Desenha o fundo da fase

        # Cronômetro
        timer_text = font.render(f"Tempo: {tempo_restante}s", True, (255, 0, 0))
        screen.blit(timer_text, (20, 20))

        keys = pygame.key.get_pressed()  # Pega as teclas pressionadas
        prota.update(keys, npc_group)  # Atualiza o movimento do protagonista
        npc_group.update()  # Atualiza os NPCs

        all_sprites.draw(screen)  # Desenha todos os sprites
        pygame.display.flip()  # Atualiza a tela
        clock.tick(60)  # Controla a taxa de atualização (60 FPS)

        if prota.rect.y < 10:  # Verifica se o protagonista chegou ao topo da tela
            menu()  # Chama o menu
            return

        if tempo_restante <= 0:  # Se o tempo acabou, chama a tela de Game Over
            tela_game_over()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Tela de Game Over
def tela_game_over():
    running = True
    while running:
        screen.blit(game_over_image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
                menu()

# Tela Sobre
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
                if 30 <= x <= 80 and 520 <= y <= 570:  # Verifica clique em botão de voltar
                    menu()
                    return

# Tela de Integrantes
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
                if 30 <= x <= 80 and 520 <= y <= 570:  # Verifica clique em botão de voltar
                    menu()
                    return

# Função principal do menu
def menu():
    running = True
    button_width = 100
    button_height = 50
    button_spacing = 20
    total_width = (3 * button_width) + (2 * button_spacing)
    start_x = (SCREEN_WIDTH - total_width) // 2

    # Define as áreas dos botões
    button_about_rect = pygame.Rect(start_x, SCREEN_HEIGHT - 100, button_width, button_height)
    button_start_rect = pygame.Rect(start_x + button_width + button_spacing, SCREEN_HEIGHT - 100, button_width, button_height)
    button_group_rect = pygame.Rect(start_x + 2 * (button_width + button_spacing), SCREEN_HEIGHT - 100, button_width, button_height)

    while running:
        screen.blit(menu_image, (0, 0))  # Desenha a tela do menu
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Pega a posição do mouse
                if button_about_rect.collidepoint(mouse_pos):
                    sobre_nos()  # Chama a tela sobre
                    return
                elif button_start_rect.collidepoint(mouse_pos):
                    fase_facil()  # Inicia a fase fácil
                    return
                elif button_group_rect.collidepoint(mouse_pos):
                    integrantes()  # Chama a tela de integrantes
                    return

# Chama o menu inicial

def fase_media(tela, clock, personagem):
    fonte = pygame.font.SysFont(None, 36)
    largura_tela, altura_tela = tela.get_size()
    tempo_maximo = 180  # 3 minutos
    tempo_inicio = time.time()
    vilao_derrotado = False
    vilao_encontrado = False

    # Cria retângulos para as escadas (esquerda e direita)
    escada_esquerda = pygame.Rect(150, altura_tela - 200, 100, 150)
    escada_direita = pygame.Rect(largura_tela - 250, altura_tela - 200, 100, 150)

    # Escolher aleatoriamente qual escada é funcional
    funcional_esquerda = random.choice([True, False])

    # Comando que o jogador deve pressionar para vencer o vilão
    comandos_possiveis = ['e', 'left', 'shift']
    comando_esperado = random.choice(comandos_possiveis)
    comando_texto = {
        'e': 'Pressione E para distrair o vilão!',
        'left': 'Desvie com a seta esquerda!',
        'shift': 'Corra com SHIFT!'
    }

    personagem.x = largura_tela // 2
    personagem.y = altura_tela - 100
    velocidade = 5

    rodando = True
    while rodando:
        tela.fill((30, 30, 30))  # fundo escuro
        tempo_atual = time.time()
        tempo_restante = tempo_maximo - (tempo_atual - tempo_inicio)

        # Cronômetro
        if tempo_restante <= 0:
            print("Game Over - tempo esgotado")
            return "game_over"

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Movimento do personagem
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            personagem.x -= velocidade
        if teclas[pygame.K_RIGHT]:
            personagem.x += velocidade
        if teclas[pygame.K_UP]:
            personagem.y -= velocidade
        if teclas[pygame.K_DOWN]:
            personagem.y += velocidade

        # Escadas
        pygame.draw.rect(tela, (200, 200, 0), escada_esquerda)  # amarelo
        pygame.draw.rect(tela, (0, 150, 255), escada_direita)   # azul

        # Personagem
        pygame.draw.rect(tela, (255, 100, 100), personagem)

        # Verifica se personagem escolheu uma escada
        if not vilao_encontrado:
            if personagem.colliderect(escada_esquerda):
                if funcional_esquerda:
                    vilao_encontrado = True
                else:
                    print("Escada quebrada! Volte e tente a outra!")
                    personagem.x += 150  # empurra de volta
            elif personagem.colliderect(escada_direita):
                if not funcional_esquerda:
                    vilao_encontrado = True
                else:
                    print("Escada quebrada! Volte e tente a outra!")
                    personagem.x -= 150

        # Desafio com o vilão
        if vilao_encontrado and not vilao_derrotado:
            texto = fonte.render(comando_texto[comando_esperado], True, (255, 255, 255))
            tela.blit(texto, (largura_tela // 2 - 150, 50))

            if comando_esperado == 'e' and teclas[pygame.K_e]:
                vilao_derrotado = True
            elif comando_esperado == 'left' and teclas[pygame.K_LEFT]:
                vilao_derrotado = True
            elif comando_esperado == 'shift' and teclas[pygame.K_LSHIFT]:
                vilao_derrotado = True

        # Vitória
        if vilao_derrotado:
            texto = fonte.render("Você venceu o vilão! Indo para a Fase 3...", True, (0, 255, 0))
            tela.blit(texto, (largura_tela // 2 - 200, altura_tela // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            return "fase_dificil"  # próxima fase

        # Tempo na tela
        tempo_texto = fonte.render(f"Tempo restante: {int(tempo_restante)}s", True, (255, 255, 255))
        tela.blit(tempo_texto, (20, 20))

        pygame.display.update()
        clock.tick(60)

menu()
