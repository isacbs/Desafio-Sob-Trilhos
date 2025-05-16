def fase_media(): 
    import pygame
    import random
    import sys
    import os

    pygame.init()

    BASE_DIR = os.path.dirname(__file__)
    IMG_DIR = os.path.join(BASE_DIR, "imgs")

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Desafio Sob Trilhos")

    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Pixelify Sans", 40)
    fonte_vilao = pygame.font.SysFont("Pixelify Sans", 30)  # Fonte menor para o vilão

    BRANCO = (255, 255, 255)
    AMARELO = (253, 214, 3)
    PRETO = (0, 0, 0)

    # Imagens
    prota_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_parada.png")), (100, 100))
    prota_andando = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "prota_andando.png")), (100, 100))
    vilao_andando = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "vilao_andando.png")), (100, 100))
    vilao_parado = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "vilao_parado.png")), (100, 100))
    escada_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "escada.png")), (800, 600))  # escada correta
    escada_quebrada_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "escadaquebr.png")), (800, 600))  # escada quebrada
    escada_escolha_img = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "escada2.png")), (800, 600))  # imagem com as duas escadas e pergunta

    prota = pygame.Rect(100, 500, 50, 50)
    vel = 5
    em_escada = False

    vilao = pygame.Rect(400, 300, 50, 50)
    vilao_direita = True
    vel_vilao = 3
    vilao_img = vilao_parado

    # ===== FASE DE ESCOLHA DAS ESCADAS =====
    escada_quebrada_lado = random.choice([1, 2])
    tentativa = 0
    acertou = False

    while not acertou and tentativa < 2:
        tela.blit(escada_escolha_img, (0, 0))  # mostra a imagem com as duas escadas
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
            # Errou, escada quebrada
            tela.blit(escada_quebrada_img, (0, 0))
            msg = fonte.render("Escada quebrada! Tente outra...", True, AMARELO)
            tela.blit(msg, (230, 40))
            pygame.display.flip()
            pygame.time.wait(2000)
            tentativa += 1
        else:
            # Acertou!
            tela.blit(escada_img, (0, 0))  # escada correta preenche a tela
            pygame.display.flip()
            pygame.time.wait(2000)
            acertou = True

    # ===== COMEÇA A FASE NORMAL COM O VILÃO =====
    mensagem = ""

    def desenhar_tela():
        tela.fill(BRANCO)
        tela.blit(escada_img, (0, 0))  # fundo da escada correta
        tela.blit(prota_img, (prota.x, prota.y))
        tela.blit(vilao_img, (vilao.x, vilao.y))
        texto = fonte_vilao.render(mensagem, True, AMARELO)  # fala do vilão em amarelo e menor
        tela.blit(texto, (200, 50))
        pygame.display.flip()

    def verificar_colisao_escada():
        nonlocal em_escada
        if prota.colliderect(pygame.Rect(200, 400, 100, 200)) or prota.colliderect(pygame.Rect(500, 400, 100, 200)):
            em_escada = True
        else:
            em_escada = False

    # Lista de falas do vilão
    falas_vilao = [
        "Tá com pressa é?",
        "Não precisa dessa ansiedade toda",
        "O trem não vai chegar mais rápido se você correr"
    ]
    fala_index = 0
    tempo_ultima_fala = pygame.time.get_ticks()
    intervalo_falas = 2000  # 2 segundos

    rodando = True
    while rodando:
        clock.tick(60)
        prota_img = prota_img
        vilao_img = vilao_andando

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimento do protagonista
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            prota.x -= vel
            prota_img = prota_andando
        if teclas[pygame.K_RIGHT]:
            prota.x += vel
            prota_img = prota_andando
        if teclas[pygame.K_UP] and em_escada:
            prota.y -= vel
        if teclas[pygame.K_DOWN] and em_escada:
            prota.y += vel
        elif not em_escada:
            if teclas[pygame.K_UP]:
                prota.y -= vel
            if teclas[pygame.K_DOWN]:
                prota.y += vel

        # Movimento do vilão
        if vilao_direita:
            vilao.x += vel_vilao
            if vilao.x > 700:
                vilao_direita = False
        else:
            vilao.x -= vel_vilao
            if vilao.x < 100:
                vilao_direita = True

        # Verifica tempo para nova fala do vilão
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultima_fala > intervalo_falas:
            mensagem = falas_vilao[fala_index]
            fala_index = (fala_index + 1) % len(falas_vilao)
            tempo_ultima_fala = tempo_atual

        # Colisão com vilão
        if prota.colliderect(vilao):
            mensagem = "Você foi pego pelo vilão!"
            desenhar_tela()
            pygame.time.wait(2000)
            rodando = False  # encerra a fase
            continue

        verificar_colisao_escada()
        desenhar_tela()