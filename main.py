import pygame
import sys

pygame.init()

print("LIVE BRAWL: Iniciando...")

LARGURA = 405
ALTURA = 720
FPS = 60

PRETO = (15, 17, 26)
BRANCO = (245, 245, 250)
AZUL = (45, 135, 255)
VERMELHO = (245, 65, 80)
CINZA = (45, 49, 65)
ROXO = (120, 70, 220)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("LIVE BRAWL")

relogio = pygame.time.Clock()

fonte_titulo = pygame.font.SysFont("arial", 36, bold=True)
fonte_texto = pygame.font.SysFont("arial", 16)


# ==========================================
# 6. LOOP PRINCIPAL
# ==========================================

executando = True

while executando:
    relogio.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    # Fundo
    tela.fill(PRETO)

    # Titulo
    titulo = fonte_titulo.render(
        "LIVE BRAWL", True, BRANCO
    )

    tela.blit(
        titulo,
        (
            LARGURA // 2 - titulo.get_width() // 2,
            60
        )
    )

    # Indicador de equipes
    equipe_azul = fonte_texto.render(
        "TIME AZUL", True, AZUL
    )

    equipe_vermelha = fonte_texto.render(
        "TIME VERMELHO", True, VERMELHO
    )

    tela.blit(equipe_azul, (40, 180))
    tela.blit(
        equipe_vermelha,
        (
            LARGURA - equipe_vermelha.get_width() - 40,
            180
        )
    )

    # Area principal da arena
    arena = pygame.Rect(20, 150, 365, 390)

    pygame.draw.rect(
        tela, (25, 28, 42), arena,
        border_radius=18
    )

    pygame.draw.rect(
        tela, ROXO, arena,
        width=3, border_radius=18
    )

    # Plataforma principal
    pygame.draw.rect(
        tela, CINZA,
        (45, 450, 315, 15),
        border_radius=8
    )

    pygame.draw.line(
        tela, ROXO,
        (45, 450), (360, 450), 3
    )

    # Lutadores provisórios
    pygame.draw.rect(
        tela, AZUL,
        (95, 385, 35, 60),
        border_radius=8
    )

    pygame.draw.rect(
        tela, VERMELHO,
        (275, 385, 35, 60),
        border_radius=8
    )

    # Indicador de presentes futuros
    presentes = fonte_texto.render(
        "PRESENTES = PODERES",
        True, BRANCO
    )

    tela.blit(
        presentes,
        (
            LARGURA // 2 - presentes.get_width() // 2,
            1030
        )
    )

    # Rodape da LIVE
    rodape = pygame.font.SysFont(
        "arial", 20, bold=True
    ).render(
        "LIVE BRAWL | BATALHA AO VIVO",
        True, (170, 170, 190)
    )

    tela.blit(
        rodape,
        (
            LARGURA // 2 - rodape.get_width() // 2,
            1190
        )
    )

    pygame.display.flip()

pygame.quit()
sys.exit()
