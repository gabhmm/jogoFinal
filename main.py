import pygame, sys, random, json
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
from recursos.aplicacoes import reconhecerVoz, falarBemVindo  # Importa do aplicacoes.py
import datetime
import os

pygame.init()
inicializarBancoDeDados()

tamanhoTela = (1000,700)
branco = (255,255,255)
preto = (0, 0 ,0 )
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanhoTela ) 
pygame.display.set_caption("")
pygame.mixer.music.load("recursos/megalovania.mp3")
telaInicial = pygame.image.load("recursos/tela_inicial.png")
nave = pygame.image.load("recursos/nave_espacial.png")
estrelas = []

icone  = pygame.image.load("recursos/icone.png")
pygame.display.set_icon(icone)
fundoJogo = pygame.image.load("recursos/fundoJogo.png")
fundoDead = pygame.image.load("recursos/tela_inicial.png")
missel = pygame.image.load("recursos/missile.png")
missileSound = pygame.mixer.Sound("recursos/missile.wav")
explosaoSound = pygame.mixer.Sound("recursos/explosao.wav")
fonteMenu = pygame.font.SysFont("arial",35)
fonteMorte = pygame.font.SysFont("arial",120)

for i in range(100):
    estrela = {
        'x': random.randint(0, tamanhoTela[0]),
        'y': random.randint(0, tamanhoTela[1]),
        'speed': random.uniform(0.5, 3)
    }
    estrelas.append(estrela)

def adicionarEstrela():
    for estrela in estrelas:
        estrela['y'] += estrela['speed']
        if estrela['y'] > tamanhoTela[1]:
            estrela['y'] = 0
            estrela['x'] = random.randint(0, tamanhoTela[0])
        pygame.draw.circle(tela, branco, (int(estrela['x']), int(estrela['y'])), 1)

def pausarJogo():
    pausado = True
    fontePausa = pygame.font.SysFont("arial", 60)
    textoPausa = fontePausa.render("PAUSE", True, (255, 255, 255))
    pygame.mixer.music.pause()
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = False
                    pygame.mixer.music.unpause()
        tela.blit(textoPausa, (tela.get_width()//2 - textoPausa.get_width()//2, tela.get_height()//2 - textoPausa.get_height()//2))
        pygame.display.update()
        pygame.time.Clock().tick(15)

def obterNome():
    root = tk.Tk()
    root.title("Escolha como informar seu nome")
    root.geometry("350x120")
    root.resizable(False, False)
    nome_usuario = {"valor": ""}

    def fechar():
        root.destroy()

    def usar_voz():
        nome = reconhecerVoz()  # Chama do aplicacoes.py
        if nome:
            nome_usuario["valor"] = nome
            root.destroy()
            # Fala o nome após reconhecer
            falarBemVindo(nome)

    def usar_texto():
        def enviar_nome():
            nome = entry_nome.get()
            if nome:
                nome_usuario["valor"] = nome
                janela_nome.destroy()
                root.destroy()
                # Fala o nome após digitar
                falarBemVindo(nome)
            else:
                messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        janela_nome = tk.Toplevel(root)
        janela_nome.title("Digite seu nome")
        janela_nome.geometry("300x80")
        tk.Label(janela_nome, text="Digite seu nome:").pack(pady=5)
        entry_nome = tk.Entry(janela_nome)
        entry_nome.pack()
        tk.Button(janela_nome, text="Enviar", command=enviar_nome).pack(pady=5)
        janela_nome.transient(root)
        janela_nome.grab_set()
        janela_nome.wait_window()

    label = tk.Label(root, text="Como você deseja informar seu nome?", font=("Arial", 11))
    label.pack(pady=10)
    frame_botoes = tk.Frame(root)
    frame_botoes.pack()
    btn_voz = tk.Button(frame_botoes, text="Falar", width=12, command=usar_voz)
    btn_voz.grid(row=0, column=0, padx=10)
    btn_texto = tk.Button(frame_botoes, text="Digitar", width=12, command=usar_texto)
    btn_texto.grid(row=0, column=1, padx=10)
    root.protocol("WM_DELETE_WINDOW", fechar)
    root.mainloop()
    return nome_usuario["valor"]

def telaBoasVindas(nome):
    larguraButtonStart = 320
    alturaButtonStart = 70
    explicacao = [
        "Bem-vindo ao jogo, {}!".format(nome),
        "",
        "Mecânica:",
        "- Use as setas ou A/D para mover a nave.",
        "- Desvie dos mísseis que caem.",
        "- Ganhe pontos a cada míssil desviado.",
        "- Pressione SPACE para pausar o jogo.",
        "",
        "Boa sorte!"
    ]
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if 'startButton' in locals() and startButton.collidepoint(evento.pos):
                    return
        tela.fill(branco)
        tela.blit(telaInicial, (0,0))
        y = 120
        linhas_renderizadas = []
        largura_max = 0
        altura_total = 0
        for linha in explicacao:
            fonte = fonteMenu if linha.startswith("Bem-vindo") else pygame.font.SysFont("arial", 28)
            texto = fonte.render(linha.replace("{}".format(nome), nome), True, branco)
            linhas_renderizadas.append((texto, fonte))
            largura_max = max(largura_max, texto.get_width())
            altura_total += texto.get_height() + 10
        altura_total -= 10
        padding_x = 40
        padding_y = 40
        rect_x = (tamanhoTela[0] - largura_max) // 2 - padding_x
        rect_y = 120 - padding_y
        rect_w = largura_max + 2 * padding_x
        rect_h = altura_total + 2 * padding_y
        pygame.draw.rect(tela, preto, (rect_x, rect_y, rect_w, rect_h), border_radius=20)
        y_texto = 120
        for texto, fonte in linhas_renderizadas:
            tela.blit(texto, ((tamanhoTela[0] - texto.get_width()) // 2, y_texto))
            y_texto += texto.get_height() + 10
        startButton = pygame.draw.rect(
            tela, preto,
            ((tamanhoTela[0] - larguraButtonStart) // 2, y_texto + 40, larguraButtonStart, alturaButtonStart),
            border_radius=15
        )
        startTexto = fonteMenu.render("INICIAR PARTIDA", True, branco)
        tela.blit(
            startTexto,
            ((tamanhoTela[0] - startTexto.get_width()) // 2, y_texto + 40 + (alturaButtonStart - startTexto.get_height()) // 2)
        )
        pygame.display.update()
        relogio.tick(60)

def jogar():
    nome = obterNome()
    if not nome:
        return
    telaBoasVindas(nome)
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 10
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    larguraPersona = 250
    alturaPersona = 127
    larguaMissel  = 50
    alturaMissel  = 250
    dificuldade  = 30

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausarJogo()
        teclas = pygame.key.get_pressed()
        movimentoXPersona = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimentoXPersona = -5
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimentoXPersona = 5
        posicaoXPersona += movimentoXPersona      
        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > tamanhoTela[0] - larguraPersona:
            posicaoXPersona = tamanhoTela[0] - larguraPersona
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        tela.blit( nave, (posicaoXPersona, posicaoYPersona) )
        adicionarEstrela()
        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0,800)
            pygame.mixer.Sound.play(missileSound)
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        texto_placar = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(texto_placar, (20, 20))
        fonte_pausa_lateral = pygame.font.SysFont("arial", 18)
        texto_pausa = fonte_pausa_lateral.render("Press SPACE to pause", True, preto)
        tela.blit(texto_pausa, (texto_placar.get_width() + 40, 15))
        pixelsPersonaX = list(range(int(posicaoXPersona), int(posicaoXPersona+larguraPersona)))
        pixelsPersonaY = list(range(int(posicaoYPersona), int(posicaoYPersona+alturaPersona)))
        pixelsMisselX = list(range(int(posicaoXMissel), int(posicaoXMissel) + larguaMissel))
        pixelsMisselY = list(range(int(posicaoYMissel), int(posicaoYMissel) + alturaMissel))
        if  len( set(pixelsMisselY).intersection(pixelsPersonaY) ) > dificuldade:
            if len( set(pixelsMisselX).intersection(pixelsPersonaX) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
        pygame.display.update()
        relogio.tick(60)

def start():
    larguraButtonStart = 200
    alturaButtonStart  = 50
    larguraButtonQuit = 200
    alturaButtonQuit  = 50
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if 'startButton' in locals() and startButton.collidepoint(evento.pos):
                    larguraButtonStart = 200
                    alturaButtonStart  = 50
                if 'quitButton' in locals() and quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 200
                    alturaButtonQuit  = 50
            elif evento.type == pygame.MOUSEBUTTONUP:
                if 'startButton' in locals() and startButton.collidepoint(evento.pos):
                    larguraButtonStart = 180
                    alturaButtonStart  = 40
                    jogar()
                if 'quitButton' in locals() and quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 180
                    alturaButtonQuit  = 40
                    quit()
        tela.fill(branco)
        tela.blit(telaInicial, (0,0) )
        startButton = pygame.draw.rect(tela, branco, ((tamanhoTela[0]-larguraButtonStart)/2, (tamanhoTela[1]/2)-alturaButtonStart, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("INICIAR", True, preto)
        tela.blit(startTexto, ((tamanhoTela[0]-larguraButtonStart+65)/2, (tamanhoTela[1]/2)-alturaButtonStart+5))
        quitButton = pygame.draw.rect(tela, branco, ((tamanhoTela[0]-larguraButtonQuit)/2, (tamanhoTela[1]/2)+alturaButtonQuit/2, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("SAIR", True, preto)
        tela.blit(quitTexto, ((tamanhoTela[0]-larguraButtonQuit+110)/2, (tamanhoTela[1]/2)+alturaButtonQuit/2+5))
        pygame.display.update()
        relogio.tick(60)
      
def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 200
    alturaButtonStart  = 50
    larguraButtonQuit = 200
    alturaButtonQuit  = 50
    if not os.path.exists("log.dat"):
        with open("log.dat", "w", encoding="utf-8") as f:
            json.dump({}, f)
    try:
        with open("log.dat", "r", encoding="utf-8") as f:
            log_partidas = json.load(f)
        if log_partidas:
            ultimo_nome = list(log_partidas.keys())[-1]
            pontos = log_partidas[ultimo_nome][0]
        else:
            pontos = 0
    except Exception:
        pontos = 0
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open("log.dat", "r", encoding="utf-8") as f:
            log_json = json.load(f)
    except Exception:
        log_json = {}
    log_json[data_hora] = [pontos, data_hora]
    with open("log.dat", "w", encoding="utf-8") as f:
        json.dump(log_json, f, ensure_ascii=False, indent=2)
    try:
        with open("log.dat", "r", encoding="utf-8") as f:
            log_partidas = json.load(f)
        ultimos_registros = list(log_partidas.items())[-5:]
    except Exception:
        ultimos_registros = []
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()                
            elif evento.type == pygame.MOUSEBUTTONUP or evento.type == pygame.MOUSEBUTTONDOWN:
                if 'startButton' in locals() and startButton.collidepoint(evento.pos):
                    larguraButtonStart = 200
                    alturaButtonStart  = 50
                    jogar()
                if 'quitButton' in locals() and quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 200
                    alturaButtonQuit  = 50
                    quit()              
        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )
        fonteLog = pygame.font.SysFont("arial", 24)
        texto_titulo = fonteMenu.render("Log das Últimas 5 Partidas", True, branco)
        logs_renderizados = []
        largura_max = texto_titulo.get_width()
        altura_total = texto_titulo.get_height() + 20
        for data, (pontos_log, data_hora_log) in reversed(ultimos_registros):
            texto_log = fonteLog.render(f"Pontos: {pontos_log} | Data: {data_hora_log}", True, branco)
            logs_renderizados.append(texto_log)
            largura_max = max(largura_max, texto_log.get_width())
            altura_total += texto_log.get_height() + 10
        altura_total -= 10
        padding_x = 40
        padding_y = 30
        rect_x = (tamanhoTela[0] - largura_max) // 2 - padding_x
        rect_y = 180
        rect_w = largura_max + 2 * padding_x
        rect_h = altura_total + 2 * padding_y
        pygame.draw.rect(tela, preto, (rect_x, rect_y, rect_w, rect_h), border_radius=20)
        y_log = rect_y + padding_y
        tela.blit(texto_titulo, ((tamanhoTela[0] - texto_titulo.get_width()) // 2, y_log))
        y_log += texto_titulo.get_height() + 20
        for texto_log in logs_renderizados:
            tela.blit(texto_log, ((tamanhoTela[0] - texto_log.get_width()) // 2, y_log))
            y_log += texto_log.get_height() + 10
        espacamento_botoes = 40
        botoes_y = rect_y + rect_h + espacamento_botoes
        startButton = pygame.draw.rect(
            tela, branco,
            ((tamanhoTela[0] // 2) - larguraButtonStart - 20, botoes_y, larguraButtonStart, alturaButtonStart),
            border_radius=15
        )
        startTexto = fonteMenu.render("INICIAR", True, preto)
        tela.blit(
            startTexto,
            ((tamanhoTela[0] // 2) - larguraButtonStart - 20 + (larguraButtonStart - startTexto.get_width()) // 2,
             botoes_y + (alturaButtonStart - startTexto.get_height()) // 2)
        )
        quitButton = pygame.draw.rect(
            tela, branco,
            ((tamanhoTela[0] // 2) + 20, botoes_y, larguraButtonQuit, alturaButtonQuit),
            border_radius=15
        )
        quitTexto = fonteMenu.render("SAIR", True, preto)
        tela.blit(
            quitTexto,
            ((tamanhoTela[0] // 2) + 20 + (larguraButtonQuit - quitTexto.get_width()) // 2,
             botoes_y + (alturaButtonQuit - quitTexto.get_height()) // 2)
        )
        pygame.display.update()
        relogio.tick(60)

start()