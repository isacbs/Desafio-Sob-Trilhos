import pygame
import sys
import os

def ranking(player_name, tempo_total):
    pygame.init()
    pygame.mixer.init()
    BASE_DIR = os.path.dirname(__file__)
    IMG_DIR = os.path.join(BASE_DIR, "imgs")
    RANKING_FILE = os.path.join(BASE_DIR, "ranking.txt")

    pygame.mixer.music.load(os.path.join(BASE_DIR, "sons", "comeco-fim.mp3"))
    pygame.mixer.music.play(-1)  #-1 significa o loop infinito

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fase Final - Ranking")

    BRANCO = (255, 255, 255)
    AMARELO = (253, 214, 3)
    PRETO = (0, 0, 0)

    #Se as fontes não funcionarem
    try:
        fonte = pygame.font.SysFont("Pixelify Sans", 40)
        pequena = pygame.font.SysFont("Pixelify Sans", 30)
    except:
        fonte = pygame.font.SysFont(None, 40)
        pequena = pygame.font.SysFont(None, 30)

    try:
        ranking_img = pygame.transform.scale(
            pygame.image.load(os.path.join(IMG_DIR, "ranking.png")),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
    except pygame.error:
        tela.fill((0, 0, 128))  #Fundo azul se tiver erro
        ranking_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        ranking_img.fill((0, 0, 128))

    #Salvar nome e tempo no arquivo txt
    try:
        with open(RANKING_FILE, "a") as f:
            f.write(f"{player_name},{int(tempo_total)}\n")
    except:
        print("Erro ao salvar o ranking.")

    # Ler e ordenar o ranking
    jogadores = []
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "r") as f:
            for linha in f:
                try:
                    nome, tempo = linha.strip().split(",")
                    jogadores.append((nome, int(tempo)))
                except:
                    continue
    jogadores.sort(key=lambda x: x[1])  # Menor tempo primeiro

    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        tela.blit(ranking_img, (0, 0))

        for i, (nome, tempo) in enumerate(jogadores[:10]):
            linha_render = pequena.render(f"{i+1}º {nome} - {tempo} segundos", True, BRANCO)
            tela.blit(linha_render, (SCREEN_WIDTH // 2 - linha_render.get_width() // 2, 230  + i * 35))
        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                rodando = False

    #Depois de sair do loop, voltar ao menu principal
    from jogo import menu
    menu()
