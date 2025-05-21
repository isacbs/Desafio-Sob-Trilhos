import pygame
import random
import sys
import os
import time

def fase_media(player_name=None, tempo_acumulado=0):
    if not pygame.font.get_init():
        pygame.font.init()

    # Inicializando
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.stop()

    # Configurando os diretórios
    BASE_DIR = os.path.dirname(__file__)
    IMG_DIR = os.path.join(BASE_DIR, "imgs")

    # Carregando o início da música de fundo
    pygame.mixer.music.load(os.path.join(BASE_DIR, "sons", "estacao.mp3"))
    pygame.mixer.music.play(-1)  # -1 significa loop infinito

    # Configuração inicial
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Desafio Sob Trilhos")

    # Fontes e relógio
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Arial", 40)
    fonte_vilao = pygame.font.SysFont("Arial", 25)

    BRANCO = (255, 255, 255)
    AMARELO = (253, 214, 3)

    # Carregamento das imagens
    prota_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_parada.png")), (100, 100))
    prota_andando = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_andando.png")), (100, 100))
    vilao_andando = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "vilao_andando.png")), (100, 100))
    vilao_parado = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "vilao_parado.png")), (100, 100))
    escada_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "escada.png")), (800, 600))
    escada_quebrada_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "escadaquebr.png")), (800, 600))
    escada_escolha_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "escada2.png")), (800, 600))

    # Configuração do protagonista
    prota = pygame.Rect(100, 500, 50, 50)
    vel = 5

    # Configuração do vilão
    vilao = pygame.Rect(400, 300, 50, 50)
    vilao_direita = True
    vel_vilao = 3
    VILAO_MIN_X = 170
    VILAO_MAX_X = 550
    vilao_img = vilao_parado

    tempo_limite = 60
    start_time = time.time()

    # Escolha aleatória de qual escada está quebrada
    escada_quebrada_lado = random.choice([1, 2])
    tentativa = 0
    acertou = False

    while not acertou and tentativa < 2:
        tela.blit(escada_escolha_img, (0, 0))
        texto = fonte.render("Qual escada você quer seguir? (1 ou 2)", True, AMARELO)
        tela.blit(texto, (180, 40))
        pygame.display.flip()

        esperando_escolha = True
        while esperando_escolha:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        escolha = 1
                        esperando_escolha = False
                    elif evento.key == pygame.K_2:
                        escolha = 2
                        esperando_escolha = False

        if escolha == escada_quebrada_lado:
            tela.blit(escada_quebrada_img, (0, 0))
            msg = fonte.render("Escada quebrada! Tente outra...", True, AMARELO)
            tela.blit(msg, (230, 40))
            pygame.display.flip()
            pygame.time.wait(2000)
            tentativa += 1
        else:
            tela.blit(escada_img, (0, 0))
            pygame.display.flip()
            pygame.time.wait(2000)
            acertou = True

    # Configuração das mensagens do jogo
    mensagem = ""
    fala_vilao = ""
    fala_timer = 0

    def desenhar_tela():
        tela.fill(BRANCO)
        tela.blit(escada_img, (0, 0))
        tela.blit(prota_img, prota)
        tela.blit(vilao_img, vilao)

        tempo_restante = max(0, int(tempo_limite - (time.time() - start_time)))
        timer_text = fonte.render(f"Tempo: {tempo_restante}s", True, AMARELO)
        tela.blit(timer_text, (20, 20))

        if player_name:
            name_text = fonte.render(f"Jogador: {player_name}", True, AMARELO)
            tela.blit(name_text, (20, 70))

        if mensagem:
            texto_msg = fonte.render(mensagem, True, AMARELO)
            tela.blit(texto_msg, (SCREEN_WIDTH // 2 - texto_msg.get_width() // 2, SCREEN_HEIGHT // 2))

        # Exibe a fala do vilão
        nonlocal fala_timer, fala_vilao
        if fala_vilao and time.time() < fala_timer:
            fala_text = fonte_vilao.render(fala_vilao, True, BRANCO)
            tela.blit(fala_text, (vilao.x, vilao.y - 30))
        else:
            fala_vilao = ""

    # Loop principal do jogo
    while True:
        tempo_restante = max(0, int(tempo_limite - (time.time() - start_time)))
        if tempo_restante <= 0:
            return fase_media(player_name, tempo_acumulado)

        desenhar_tela()
        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            prota.x -= vel
        if keys[pygame.K_RIGHT]:
            prota.x += vel
        if keys[pygame.K_UP]:
            prota.y -= vel
        if keys[pygame.K_DOWN]:
            prota.y += vel

        prota.x = max(0, min(prota.x, SCREEN_WIDTH - prota.width))
        prota.y = max(0, min(prota.y, SCREEN_HEIGHT - prota.height))

        # Movimento do vilão
        if vilao_direita:
            vilao.x += vel_vilao
            vilao_img = vilao_andando
            if vilao.x >= VILAO_MAX_X:
                vilao_direita = False
                fala_vilao = "O trem não vai chegar mais rápido se você correr"
                fala_timer = time.time() + 3
        else:
            vilao.x -= vel_vilao
            vilao_img = vilao_andando
            if vilao.x <= VILAO_MIN_X:
                vilao_direita = True
                fala_vilao = "Não precisa dessa ansiedade toda!"
                fala_timer = time.time() + 3

        # Verifica colisão entre protagonista e vilão
        if prota.colliderect(vilao):
            mensagem = "Você foi pego! Tente novamente."
            desenhar_tela()
            pygame.display.flip()
            pygame.time.wait(3000)
            return fase_media(player_name, tempo_acumulado)

        # Verifica se o jogador chegou ao topo da tela (completou a fase)
        if prota.y <= 10:
            desenhar_tela()
            pygame.display.flip()
            pygame.time.wait(2000)
            tempo_total = tempo_acumulado + (time.time() - start_time)
            from faseFinal import fase_final
            return fase_final(player_name, tempo_total)