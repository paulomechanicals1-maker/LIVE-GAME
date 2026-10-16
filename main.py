
import pygame
import sys
import math

pygame.init()

# CONFIGURACOES DA JANELA
LARGURA = 405
ALTURA = 720
FPS = 60

# CONFIGURACOES DO JOGO
GRAVIDADE = 0.65
FORCA_PULO = -12
VELOCIDADE = 4

# CONFIGURACOES DO COMBATE
DANO_ATAQUE = 10
ALCANCE_ATAQUE = 55
TEMPO_RECARGA = 500  # milissegundos
DURACAO_GOLPE = 150  # milissegundos

#MOVIMENTACAO AVANCADA
ACELERACAO = 0.75
VELOCIDADE_MAXIMA = 5.2
ATRITO = 0.78
FORCA_PULO = -12
FORCA_PULO_EXTRA = -10
FORCA_RECUO = 7
TEMPO_ATORDOADO = 180
TEMPO_DASH = 160
RECARGA_DASH = 9000

# CORES
PRETO = (15, 15, 20)
BRANCO = (245, 245, 245)
AZUL = (40, 130, 255)
VERMELHO = (245, 55, 65)
VERDE = (50, 210, 100)
CINZA = (65, 65, 75)
AMARELO = (255, 210, 60)

# JANELA
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("LIVE BRAWL")

relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 22, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 16, bold=True)

# ARENA
CHAO_Y = 610
chao = pygame.Rect(0, CHAO_Y, LARGURA, ALTURA - CHAO_Y)

# PLATAFORMAS
plataformas = [
    chao,
    pygame.Rect(45, 490, 110, 16),
    pygame.Rect(250, 490, 110, 16),
]

# JOGADORES
largura_jogador = 38
altura_jogador = 58

jogador_azul = {
    "rect": pygame.Rect(65, CHAO_Y - altura_jogador,
                        largura_jogador, altura_jogador),
    "cor": AZUL,
    "vida": 100,
    "direcao": 1,
    "vel_y": 0,
    "no_chao": True,
    "ultimo_ataque": 0,
    "fim_golpe": 0,
    "nome": "AZUL",
    "vx": 0.0,
    "atordoado_ate": 0,
    "dash_ate": 0,
    "ultimo_dash": -10000,
    "pulos": 0,
}

jogador_vermelho = {
    "rect": pygame.Rect(302, CHAO_Y - altura_jogador,
                        largura_jogador, altura_jogador),
    "cor": VERMELHO,
    "vida": 100,
    "direcao": -1,
    "vel_y": 0,
    "no_chao": True,
    "ultimo_ataque": 0,
    "fim_golpe": 0,
    "nome": "VERMELHO",
    "vx": 0.0,
    "atordoado_ate": 0,
    "dash_ate": 0,
    "ultimo_dash": -10000,
    "pulos": 0,
}

vencedor = None


def aplicar_fisica(jogador):
    jogador["vel_y"] += GRAVIDADE
    jogador["rect"].y += int(jogador["vel_y"])
    jogador["no_chao"] = False

    for plataforma in plataformas:
        if jogador["rect"].colliderect(plataforma):
            # Caindo sobre a plataforma
            if jogador["vel_y"] >= 0:
                jogador["rect"].bottom = plataforma.top
                jogador["vel_y"] = 0
                jogador["no_chao"] = True

            # Batendo por baixo da plataforma
            elif jogador["vel_y"] < 0:
                jogador["rect"].top = plataforma.bottom
                jogador["vel_y"] = 0


def atacar(atacante, defensor, agora):
    if agora - atacante["ultimo_ataque"] < TEMPO_RECARGA:
        return

    atacante["ultimo_ataque"] = agora
    atacante["fim_golpe"] = agora + DURACAO_GOLPE

    corpo = atacante["rect"]
    alvo = defensor["rect"]

    # Area de alcance do golpe
    if atacante["direcao"] == 1:
        area_ataque = pygame.Rect(
            corpo.right,
            corpo.top + 8,
            ALCANCE_ATAQUE,
            corpo.height - 16,
        )
    else:
        area_ataque = pygame.Rect(
            corpo.left - ALCANCE_ATAQUE,
            corpo.top + 8,
            ALCANCE_ATAQUE,
            corpo.height - 16,
        )

    # O golpe acerta somente se houver contato com a area

    if area_ataque.colliderect(alvo):
        defensor["vida"] = max(0, defensor["vida"] - DANO_ATAQUE)

        # Empurra o adversario para tras
        defensor["vx"] = atacante["direcao"] * FORCA_RECUO
        defensor["atordoado_ate"] = agora + TEMPO_ATORDOADO

        # Pequeno impulso vertical para dar sensacao de impacto
        defensor["vel_y"] = -3.5
        defensor["no_chao"] = False

def desenhar_barra_vida(x, y, nome, vida, cor):
    largura = 145
    altura = 18

    texto = fonte_pequena.render(nome, True, BRANCO)
    tela.blit(texto, (x, y - 22))

    pygame.draw.rect(tela, CINZA, (x, y, largura, altura))

    largura_vida = int(largura * vida / 100)

    if largura_vida > 0:
        pygame.draw.rect(
            tela,
            cor,
            (x, y, largura_vida, altura),
        )

    pygame.draw.rect(tela, BRANCO, (x, y, largura, altura), 2)

    numero = fonte_pequena.render(str(vida), True, BRANCO)
    tela.blit(numero, (x + largura + 5, y))



def desenhar_jogador(jogador, agora):
    corpo = jogador["rect"]
    cx = corpo.centerx

    if abs(jogador["vx"]) > 0.5 and jogador["no_chao"]:
        cy = corpo.top + int(math.sin(agora * 0.025) * 2)
    else:
        cy = corpo.top
    direcao = jogador["direcao"]
    cor = jogador["cor"]

    contorno = (12, 12, 22)
    branco = (245, 245, 255)
    pele = (255, 202, 160)
    calca = (32, 35, 49)
    tenis = (235, 235, 245)

    if cor == AZUL:
        cabelo = (20, 100, 255)
        cabelo_luz = (80, 190, 255)
        roupa = (20, 100, 235)
        roupa_luz = (80, 180, 255)
    else:
        cabelo = (230, 35, 55)
        cabelo_luz = (255, 100, 75)
        roupa = (205, 30, 50)
        roupa_luz = (255, 85, 80)

    # Espelha os desenhos conforme a direcao do lutador
    def ponto(x, y):
        return (int(cx + x * direcao), int(cy + y))

    def poligono(pontos, cor_preenchimento, cor_borda=contorno, largura=3):
        pts = [ponto(x, y) for x, y in pontos]
        pygame.draw.polygon(tela, cor_preenchimento, pts)
        if cor_borda:
            pygame.draw.polygon(tela, cor_borda, pts, largura)

    def circulo(x, y, raio, cor_circulo, borda=contorno):
        pos = ponto(x, y)
        pygame.draw.circle(tela, cor_circulo, pos, raio)
        if borda:
            pygame.draw.circle(tela, borda, pos, raio, 2)

    def linha(p1, p2, cor_linha, largura):
        pygame.draw.line(
            tela, cor_linha, ponto(*p1), ponto(*p2), largura
        )

    # Sombra no chao
    pygame.draw.ellipse(
        tela, (5, 5, 15),
        (corpo.x - 8, corpo.bottom - 4, corpo.width + 16, 12)
    )

    # Pernas
    poligono([
        (-12, 35), (-2, 36), (-5, 48),
        (-15, 54), (-22, 50), (-16, 43)
    ], calca)

    poligono([
        (2, 35), (12, 34), (16, 44),
        (23, 49), (18, 55), (7, 51), (0, 43)
    ], calca)

    # Detalhes das calcas
    linha((-10, 40), (-14, 48), (100, 105, 130), 2)
    linha((8, 39), (13, 46), (100, 105, 130), 2)

    # Tenis
    poligono([
        (-20, 48), (-12, 49), (-10, 53),
        (-2, 55), (-2, 59), (-24, 59), (-26, 56)
    ], tenis)

    poligono([
        (12, 48), (18, 47), (21, 52),
        (27, 55), (27, 59), (7, 59), (7, 55)
    ], tenis)

    linha((-22, 56), (-5, 56), cor, 3)
    linha((10, 56), (25, 56), cor, 3)

    # Tronco e jaqueta
    poligono([
        (-13, 17), (0, 14), (12, 18),
        (15, 36), (8, 42), (-10, 40), (-16, 31)
    ], roupa)

    # Camiseta
    poligono([
        (-4, 18), (3, 18), (7, 36),
        (0, 39), (-5, 35)
    ], branco, contorno, 2)

    # Faixas da jaqueta
    linha((-12, 23), (-9, 35), roupa_luz, 3)
    linha((10, 22), (12, 32), roupa_luz, 3)

    # Bracos em posicao de luta
    poligono([
        (-12, 20), (-20, 23), (-25, 30),
        (-19, 34), (-11, 29), (-5, 25)
    ], roupa)

    poligono([
        (10, 20), (18, 21), (25, 27),
        (22, 33), (15, 30), (8, 27)
    ], roupa)

    # Luvas
    circulo(-22, 31, 7, cor)
    circulo(23, 29, 7, cor)
    linha((-26, 31), (-19, 31), branco, 2)
    linha((19, 29), (26, 29), branco, 2)

    # Pescoco
    pygame.draw.rect(
        tela, pele,
        (int(cx - 5), int(cy + 12), 10, 9)
    )

    # Rosto
    circulo(0, 10, 12, pele)

    # Faixa na testa
    poligono([
        (-11, 5), (-6, 0), (5, 1),
        (12, 5), (10, 8), (-5, 6)
    ], cor)

    # Cabelo espetado
    poligono([
        (-12, 7), (-15, 0), (-10, 1),
        (-13, -7), (-5, -3), (-2, -13),
        (3, -5), (10, -9), (8, -2),
        (14, 0), (10, 8), (5, 4),
        (-3, 3)
    ], cabelo)

    # Brilhos no cabelo
    linha((-9, 0), (-4, -5), cabelo_luz, 3)
    linha((0, -3), (4, -6), cabelo_luz, 2)

    # Olho e sobrancelha
    linha((2, 7), (8, 6), contorno, 3)
    pygame.draw.circle(tela, contorno, ponto(5, 9), 2)

    # Efeito de ataque
    if agora < jogador["fim_golpe"]:
        x = corpo.right if direcao == 1 else corpo.left - ALCANCE_ATAQUE
        efeito = pygame.Rect(
            x, corpo.top + 10,
            ALCANCE_ATAQUE, corpo.height - 20
        )
        pygame.draw.rect(
            tela, AMARELO, efeito, 4, border_radius=12
        )


def desenhar_arena():
    # Fundo escuro
    tela.fill((8, 10, 30))

    # Ceu com estrelas
    for x, y, raio in [
        (30, 230, 2), (90, 280, 2), (160, 220, 1),
        (280, 240, 2), (360, 300, 2), (220, 190, 1),
        (55, 350, 1), (335, 205, 1)
    ]:
        pygame.draw.circle(tela, (100, 140, 255), (x, y), raio)

    # Predios ao fundo
    predios = [
        (0, 300, 42, 310), (48, 260, 45, 350),
        (100, 325, 40, 285), (145, 285, 48, 325),
        (200, 340, 42, 270), (250, 275, 48, 335),
        (303, 315, 45, 295), (352, 265, 53, 345)
    ]

    for x, y, largura, altura in predios:
        pygame.draw.rect(
            tela, (17, 24, 58),
            (x, y, largura, altura)
        )

        # Janelas iluminadas
        for wy in range(y + 12, min(y + altura, CHAO_Y - 10), 24):
            for wx in range(x + 7, x + largura - 5, 15):
                luz = (40, 130, 255) if (wx + wy) % 3 else (255, 45, 130)
                pygame.draw.rect(
                    tela, luz, (wx, wy, 5, 9)
                )

    # Letreiro central
    pygame.draw.rect(
        tela, (20, 20, 48), (55, 350, 295, 105)
    )
    pygame.draw.rect(
        tela, (35, 100, 255), (55, 350, 295, 105), 3
    )
    pygame.draw.rect(
        tela, (255, 35, 105), (60, 355, 285, 95), 1
    )

    logo = fonte.render("LIVE BRAWL", True, BRANCO)
    tela.blit(
        logo,
        (LARGURA // 2 - logo.get_width() // 2, 385)
    )

    # Plataformas laterais
    for plataforma in plataformas[1:]:
        pygame.draw.rect(
            tela, (28, 35, 65), plataforma,
            border_radius=4
        )
        pygame.draw.line(
            tela, (40, 160, 255),
            plataforma.topleft, plataforma.topright, 3
        )

    # Chao da arena
    pygame.draw.rect(tela, (23, 25, 43), chao)
    pygame.draw.line(
        tela, (60, 140, 255),
        (0, CHAO_Y), (LARGURA, CHAO_Y), 4
    )

    for x in range(0, LARGURA, 45):
        pygame.draw.line(
            tela, (42, 45, 67),
            (x, CHAO_Y + 15), (x + 20, ALTURA), 1
        )

    # Titulo superior
    titulo = fonte.render("LIVE BRAWL", True, BRANCO)
    tela.blit(
        titulo,
        (LARGURA // 2 - titulo.get_width() // 2, 28)
    )

    # Barras de vida
    desenhar_barra_vida(
        12, 90, "JOGADOR AZUL",
        jogador_azul["vida"], AZUL
    )

    desenhar_barra_vida(
        12, 145, "JOGADOR VERMELHO",
        jogador_vermelho["vida"], VERMELHO
    )

def reiniciar_jogo():
    global vencedor

    jogador_azul.update({
        "rect": pygame.Rect(
            65, CHAO_Y - altura_jogador,
            largura_jogador, altura_jogador
        ),
        "vida": 100,
        "direcao": 1,
        "vel_y": 0,
        "no_chao": True,
        "ultimo_ataque": 0,
        "fim_golpe": 0,
        "vx": 0.0,
        "atordoado_ate": 0,
        "dash_ate": 0,
        "ultimo_dash": -10000,
        "pulos": 0,
    })

    jogador_vermelho.update({
        "rect": pygame.Rect(
            302, CHAO_Y - altura_jogador,
            largura_jogador, altura_jogador
        ),
        "vida": 100,
        "direcao": -1,
        "vel_y": 0,
        "no_chao": True,
        "ultimo_ataque": 0,
        "fim_golpe": 0,
        "vx": 0.0,
        "atordoado_ate": 0,
        "dash_ate": 0,
        "ultimo_dash": -10000,
        "pulos": 0,
    })

    vencedor = None


# LOOP PRINCIPAL
rodando = True

while rodando:
    relogio.tick(FPS)
    agora = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False

            if vencedor is not None and evento.key == pygame.K_r:
                reiniciar_jogo()

            if vencedor is None:
                # Ataque do jogador azul
                if evento.key == pygame.K_f:
                    atacar(jogador_azul, jogador_vermelho, agora)

                # Ataque do jogador vermelho
                if evento.key == pygame.K_RETURN:
                    atacar(jogador_vermelho, jogador_azul, agora)

    teclas = pygame.key.get_pressed()

    if vencedor is None:
        # MOVIMENTACAO DOS DOIS LUTADORES
        for jogador, teclas_esquerda, teclas_direita, tecla_pulo, tecla_dash in [
            (
                jogador_azul,
                pygame.K_a,
                pygame.K_d,
                pygame.K_w,
                pygame.K_LSHIFT,
            ),
            (
                jogador_vermelho,
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_UP,
                pygame.K_RSHIFT,
            ),
        ]:
            # Nao permite controlar o lutador durante a reacao ao golpe
            atordoado = agora < jogador["atordoado_ate"]

            if not atordoado:
                # Aceleracao horizontal
                if teclas[teclas_esquerda]:
                    jogador["vx"] -= ACELERACAO
                    jogador["direcao"] = -1

                if teclas[teclas_direita]:
                    jogador["vx"] += ACELERACAO
                    jogador["direcao"] = 1

                # Limita a velocidade
                jogador["vx"] = max(
                    -VELOCIDADE_MAXIMA,
                    min(VELOCIDADE_MAXIMA, jogador["vx"]),
                )

                # Atrito: desacelera quando solta as teclas
                if not teclas[teclas_esquerda] and not teclas[teclas_direita]:
                    jogador["vx"] *= ATRITO

                    if abs(jogador["vx"]) < 0.15:
                        jogador["vx"] = 0

                # Pulo duplo
                if teclas[tecla_pulo] and jogador["no_chao"]:
                    jogador["vel_y"] = FORCA_PULO
                    jogador["no_chao"] = False
                    jogador["pulos"] = 1

                # Dash: Shift + direcao atual
                if (
                    teclas[tecla_dash]
                    and agora - jogador["ultimo_dash"] >= RECARGA_DASH
                ):
                    jogador["ultimo_dash"] = agora
                    jogador["dash_ate"] = agora + TEMPO_DASH
                    jogador["vx"] = jogador["direcao"] * 11

            # Move o personagem pela velocidade horizontal
            jogador["rect"].x += int(jogador["vx"])

            # Limites da arena
            if jogador["rect"].left < 0:
                jogador["rect"].left = 0
                jogador["vx"] = 0

            if jogador["rect"].right > LARGURA:
                jogador["rect"].right = LARGURA
                jogador["vx"] = 0


        # FISICA
        aplicar_fisica(jogador_azul)
        aplicar_fisica(jogador_vermelho)

        # VERIFICAR VITORIA
        if jogador_azul["vida"] <= 0:
            vencedor = "VERMELHO"

        elif jogador_vermelho["vida"] <= 0:
            vencedor = "AZUL"

    # DESENHAR TUDO
    desenhar_arena()

    desenhar_jogador(jogador_azul, agora)
    desenhar_jogador(jogador_vermelho, agora)

    if vencedor is not None:
        texto_vitoria = fonte.render(
            f"{vencedor} VENCEU!",
            True,
            AMARELO,
        )

        tela.blit(
            texto_vitoria,
            (
                LARGURA // 2 - texto_vitoria.get_width() // 2,
                330,
            ),
        )

        texto_reiniciar = fonte_pequena.render(
            "Pressione R para jogar novamente",
            True,
            BRANCO,
        )

        tela.blit(
            texto_reiniciar,
            (
                LARGURA // 2 - texto_reiniciar.get_width() // 2,
                365,
            ),
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
