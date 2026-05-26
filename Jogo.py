# Importa as bibliotecas usadas no jogo
# pygame: cria a janela, desenha imagens, detecta teclado e toca música
# sys: permite fechar o programa corretamente
# random: gera números aleatórios, usado em itens, barris e efeitos
# math: usado para animações com seno/cosseno, como fumaça, lava e brilho
import pygame
import sys
import random
import math

# Inicializa o pygame e o sistema de som
pygame.init()
pygame.mixer.init()

# Carrega e toca a música de fundo em loop infinito
pygame.mixer.music.load(r"C:\Users\rezen\Downloads\hard_boss_battle_1_bpm200.ogg")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Define o tamanho da tela e a altura total do mundo
# A tela mostra só uma parte do mundo; a câmera acompanha o jogador
LARGURA, ALTURA = 900, 800
MUNDO_ALTURA = 1400

# Cria a janela do jogo
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dino Barrel")

# Controla a velocidade do jogo
CLOCK = pygame.time.Clock()
FPS = 60

# Carrega as imagens de fundo das fases e ajusta ao tamanho da tela
fundo_img = pygame.image.load(r"C:\Users\rezen\Downloads\fundogame.jpg").convert()
fundo_img = pygame.transform.scale(fundo_img, (LARGURA, ALTURA))

fundo_fase2 = pygame.image.load(r"C:\Users\rezen\Downloads\fase final.webp").convert()
fundo_fase2 = pygame.transform.scale(fundo_fase2, (LARGURA, ALTURA))

# Cores usadas no jogo em formato RGB
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_ESC = (30, 30, 30)
AMARELO = (255, 220, 0)
VERMELHO = (220, 50, 50)
AZUL_CLARO = (80, 180, 255)
LARANJA = (255, 120, 30)
LARANJA_ESC = (200, 80, 10)
CINZA_PEDRA = (90, 85, 80)
CINZA_PEDRA2 = (120, 110, 100)
VERMELHO_LAVA = (255, 60, 0)
AMARELO_LAVA = (255, 200, 0)

def desenhar_vulcao(surface, t):
    # Desenha a tela inicial animada com vulcão, estrelas, lava, fumaça e faíscas.
    # O parâmetro "surface" é onde será desenhado.
    # O parâmetro "t" funciona como contador de tempo para animar os efeitos.

    surface.fill((15, 10, 30))

    # Desenha estrelas no céu com brilho variando
    random.seed(42)
    for _ in range(120):
        sx = random.randint(0, LARGURA)
        sy = random.randint(0, int(ALTURA * 0.55))
        brilho = 100 + int(60 * abs(math.sin(t * 0.03 + sx)))
        pygame.draw.circle(surface, (brilho, brilho, brilho), (sx, sy), 1)

    random.seed()

    # Desenha montanhas ao fundo
    montanha = [(0, ALTURA), (0, 500), (150, 320), (280, 420), (400, 200),
                (520, 380), (650, 290), (800, 430), (900, 380), (900, ALTURA)]
    pygame.draw.polygon(surface, (25, 20, 40), montanha)

    # Desenha o corpo principal do vulcão
    vx, vy_base, vy_topo = 450, ALTURA, 260
    largura_base, largura_topo = 380, 90
    vulcao = [(vx - largura_base // 2, vy_base), (vx - largura_topo // 2, vy_topo),
              (vx + largura_topo // 2, vy_topo), (vx + largura_base // 2, vy_base)]
    pygame.draw.polygon(surface, CINZA_PEDRA, vulcao)

    # Lado mais claro do vulcão para dar profundidade
    lado_claro = [(vx - largura_base // 2, vy_base), (vx - largura_topo // 2, vy_topo),
                  (vx - largura_topo // 2 + 30, vy_topo + 30), (vx - largura_base // 2 + 60, vy_base)]
    pygame.draw.polygon(surface, CINZA_PEDRA2, lado_claro)

    # Cratera
    cratera_y = vy_topo + 10
    pygame.draw.ellipse(surface, (50, 20, 10), (vx - largura_topo // 2 - 10, cratera_y - 18, largura_topo + 20, 36))

    # Lava escorrendo pelas laterais
    for lado in (-1, 1):
        for i in range(3):
            lx = vx + lado * (largura_topo // 2 - 10 + i * 12)
            for seg in range(8):
                seg_y = vy_topo + 20 + seg * 35
                cor = VERMELHO_LAVA if seg % 2 == 0 else AMARELO_LAVA
                pts = [
                    (lx + lado * seg * 3, seg_y),
                    (lx + lado * (seg * 3 + 8), seg_y + 18),
                    (lx + lado * (seg * 3 + 4), seg_y + 35),
                ]
                pygame.draw.lines(surface, cor, False, pts, 4)

    # Bolhas de lava saindo da cratera
    for i in range(14):
        angulo = -math.pi / 2 + math.sin(t * 0.05 + i * 0.8) * 0.6
        velocidade = 3 + (i % 5) * 0.8
        px = int(vx + math.cos(angulo) * velocidade * ((t % 40) + i * 5) % 120)
        py = int(cratera_y - 10 - (t * 2 + i * 18) % 180)
        if py <= cratera_y:
            cor = AMARELO_LAVA if i % 2 == 0 else VERMELHO_LAVA
            pygame.draw.circle(surface, cor, (px, py), max(1, 4 - (i % 3)))

    # Fumaça da cratera
    for i in range(5):
        sx = vx + int(math.sin(t * 0.04 + i * 1.2) * 20)
        sy = cratera_y - 30 - (t * 1.5 + i * 22) % 100
        if sy >= cratera_y - 130:
            raio = 12 + i * 4
            fuma = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
            alfa = max(0, 180 - int((cratera_y - 30 - sy) * 1.5))
            pygame.draw.circle(fuma, (80, 70, 70, alfa), (raio, raio), raio)
            surface.blit(fuma, (sx - raio, int(sy) - raio))

    # Rochas na parte inferior
    for i in range(6):
        rx = vx - 180 + i * 70 + int(math.sin(t * 0.03 + i) * 10)
        ry = ALTURA - 20 - (i % 3) * 8
        pygame.draw.ellipse(surface, (180 + i * 10, 40 + i * 5, 0), (rx, ry, 50 - i * 4, 12))

def desenhar_texto_arcade(surface, fonte, texto, cor, contorno, x, y, espaco_extra=6):
    # Desenha um texto com estilo arcade.
    # Cada letra é desenhada separadamente para permitir espaçamento customizado.
    # Primeiro desenha o contorno e depois a letra colorida por cima.

    chars = list(texto)

    # Calcula a largura total do texto para centralizar corretamente
    largura_total = sum(fonte.size(c)[0] + espaco_extra for c in chars) - espaco_extra
    cx = x - largura_total // 2

    for c in chars:
        w = fonte.size(c)[0]

        # Desenha o contorno da letra em volta
        letra_contorno = fonte.render(c, True, contorno)
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2):
                if dx != 0 or dy != 0:
                    surface.blit(letra_contorno, (cx + dx, y + dy))

        # Desenha a letra principal
        surface.blit(fonte.render(c, True, cor), (cx, y))
        cx += w + espaco_extra

def tela_inicio():
    # Mostra a tela inicial do jogo.
    # Ela fica em loop até o jogador apertar ENTER.
    # Também verifica se o jogador fechou a janela.

    fontes = ["Courier New", "Consolas", "Lucida Console", "monospace"]
    nomes = [f.lower() for f in pygame.font.get_fonts()]

    # Escolhe uma fonte estilo arcade disponível no computador
    fonte_nome = next((f for f in fontes if f.lower() in nomes), "monospace")

    # Cria fontes com tamanhos diferentes
    fonte_titulo = pygame.font.SysFont(fonte_nome, 88, bold=True)
    fonte_sub = pygame.font.SysFont(fonte_nome, 30, bold=True)
    fonte_cred = pygame.font.SysFont("arial", 20)
    fonte_press = pygame.font.SysFont(fonte_nome, 26, bold=True)

    t = 0

    while True:
        CLOCK.tick(FPS)
        t += 1

        # Trata eventos da tela inicial
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Ao apertar ENTER, sai da tela inicial e começa o jogo
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        # Desenha fundo animado, título, botão de ENTER e créditos
        desenhar_vulcao(TELA, t)

        painel = pygame.Surface((700, 320), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 160))
        TELA.blit(painel, (100, 100))

        desenhar_texto_arcade(TELA, fonte_titulo, "DINO BARREL", AMARELO, (160, 60, 0), LARGURA // 2, 118, 8)
        desenhar_texto_arcade(TELA, fonte_sub, "- HARD MODE -", VERMELHO, (80, 10, 10), LARGURA // 2, 228, 4)

        for bx in (LARGURA // 2 - 130, LARGURA // 2 + 100):
            pygame.draw.rect(TELA, LARANJA, (bx, 280, 30, 30), border_radius=6)
            pygame.draw.rect(TELA, CINZA_PEDRA, (bx, 280, 30, 30), 2, border_radius=6)

        pygame.draw.line(TELA, LARANJA_ESC, (200, 325), (700, 325), 2)

        cor_enter = BRANCO if (t // 30) % 2 == 0 else AMARELO
        contorno = (40, 40, 40) if cor_enter == BRANCO else (100, 60, 0)
        desenhar_texto_arcade(TELA, fonte_press, "[ ENTER ] PARA JOGAR", cor_enter, contorno, LARGURA // 2, 358, 3)

        y = ALTURA - 70
        for linha in ["Criado por:", "Luiz Coutinho  •  Felipe Mastandrea  •  João Tristão"]:
            txt = fonte_cred.render(linha, True, (180, 170, 160))
            TELA.blit(txt, (LARGURA // 2 - txt.get_width() // 2, y))
            y += 28

        pygame.display.flip()

def tela_transicao(numero_fase):
    # Mostra uma tela entre as fases.
    # O jogo só continua quando o jogador aperta ENTER.

    fontes = ["Courier New", "Consolas", "Lucida Console", "monospace"]
    nomes = [f.lower() for f in pygame.font.get_fonts()]
    fonte_nome = next((f for f in fontes if f.lower() in nomes), "monospace")
    fonte_grande = pygame.font.SysFont(fonte_nome, 72, bold=True)
    fonte_media = pygame.font.SysFont(fonte_nome, 32, bold=True)
    fonte_press = pygame.font.SysFont(fonte_nome, 24, bold=True)

    t = 0

    while True:
        CLOCK.tick(FPS)
        t += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        TELA.fill((10, 10, 20))
        painel = pygame.Surface((700, 300), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 180))
        TELA.blit(painel, (100, 220))

        desenhar_texto_arcade(TELA, fonte_grande, f"FASE {numero_fase}", AMARELO, (120, 60, 0), LARGURA // 2, 250, 6)
        desenhar_texto_arcade(TELA, fonte_media, "PREPARE-SE!", BRANCO, (40, 40, 40), LARGURA // 2, 360, 4)

        cor_enter = BRANCO if (t // 30) % 2 == 0 else AMARELO
        desenhar_texto_arcade(TELA, fonte_press, "[ ENTER ] PARA CONTINUAR", cor_enter, (40, 40, 40), LARGURA // 2, 430, 3)

        pygame.display.flip()

def tela_game_over():
    fontes = ["Courier New", "Consolas", "Lucida Console", "monospace"]
    nomes = [f.lower() for f in pygame.font.get_fonts()]
    fonte_nome = next((f for f in fontes if f.lower() in nomes), "monospace")
    fonte_grande = pygame.font.SysFont(fonte_nome, 80, bold=True)
    fonte_media = pygame.font.SysFont(fonte_nome, 30, bold=True)
    fonte_press = pygame.font.SysFont(fonte_nome, 24, bold=True)
    t = 0

    while True:
        CLOCK.tick(FPS)
        t += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

        TELA.fill((20, 0, 0))
        painel = pygame.Surface((700, 320), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 180))
        TELA.blit(painel, (100, 200))

        desenhar_texto_arcade(TELA, fonte_grande, "GAME OVER", VERMELHO, (80, 0, 0), LARGURA // 2, 230, 6)
        desenhar_texto_arcade(TELA, fonte_media, f"Pontuacao Final: {pontuacao}", BRANCO, (40, 40, 40), LARGURA // 2, 360, 4)

        cor_enter = BRANCO if (t // 30) % 2 == 0 else VERMELHO
        desenhar_texto_arcade(TELA, fonte_press, "[ ENTER ] PARA SAIR", cor_enter, (40, 40, 40), LARGURA // 2, 430, 3)

        pygame.display.flip()

def tela_vitoria():
    fontes = ["Courier New", "Consolas", "Lucida Console", "monospace"]
    nomes = [f.lower() for f in pygame.font.get_fonts()]
    fonte_nome = next((f for f in fontes if f.lower() in nomes), "monospace")
    fonte_grande = pygame.font.SysFont(fonte_nome, 80, bold=True)
    fonte_media = pygame.font.SysFont(fonte_nome, 30, bold=True)
    t = 0

    while True:
        CLOCK.tick(FPS)
        t += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

        TELA.fill((10, 10, 20))
        desenhar_texto_arcade(TELA, fonte_grande, "VOCE VENCEU!", AMARELO, (120, 60, 0), LARGURA // 2, 280, 6)
        desenhar_texto_arcade(TELA, fonte_media, f"Pontuacao Final: {pontuacao}", BRANCO, (40, 40, 40), LARGURA // 2, 400, 4)
        pygame.display.flip()

# Mostra a tela inicial antes de carregar o restante do jogo
tela_inicio()