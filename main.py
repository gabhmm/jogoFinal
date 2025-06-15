import pygame, sys, random, json
import tkinter as tk
import sys
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
from recursos.aplicacoes import reconhecerVoz, falarBemVindo
import datetime

pygame.init()
inicializarBancoDeDados()

tamanhoTela = (1000, 700)
corBranca = (255, 255, 255)
corPreta = (0, 0, 0)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanhoTela)
pygame.display.set_caption("")
pygame.mixer.music.load("recursos/megalovania.mp3")
telaInicial = pygame.image.load("recursos/tela_inicial.png")
naveJogador = pygame.image.load("recursos/nave_espacial.png")
imagemLua = pygame.image.load("recursos/lua_objeto.png")
fundoMorte = pygame.image.load("recursos/tela_inicial.png")
somNave = pygame.mixer.Sound("recursos/nave_tiro.mp3")
somExplosao = pygame.mixer.Sound("recursos/explosao.wav")
fundoJogo = pygame.image.load("recursos/fundoJogo.jpg")
naveInimiga = pygame.image.load("recursos/nave_inimiga.png")
icone = pygame.image.load("recursos/icone.png")
pygame.display.set_icon(icone)
fonteMenu = pygame.font.SysFont("arial", 35)
fonteMorte = pygame.font.SysFont("arial", 120)

def jogar():
    listaEstrelas = []
    for i in range(100):
        estrela = {
            'x': random.randint(0, tamanhoTela[0]),
            'y': random.randint(0, tamanhoTela[1]),
            'velocidade': random.uniform(0.5, 3)
        }
        listaEstrelas.append(estrela)

    def adicionarEstrela():
        for estrela in listaEstrelas:
            estrela['y'] += estrela['velocidade']
            if estrela['y'] > tamanhoTela[1]:
                estrela['y'] = 0
                estrela['x'] = random.randint(0, tamanhoTela[0])
            pygame.draw.circle(tela, corBranca, (int(estrela['x']), int(estrela['y'])), 1)

    def pausarJogo():
        pausado = True
        fontePausa = pygame.font.SysFont("arial", 60)
        textoPausa = fontePausa.render("PAUSE", True, corBranca)
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
            tela.blit(textoPausa, (tela.get_width() // 2 - textoPausa.get_width() // 2, tela.get_height() // 2 - textoPausa.get_height() // 2))
            pygame.display.update()
            pygame.time.Clock().tick(15)

    def obterNome():
        root = tk.Tk()
        root.title("Escolha como informar seu nome")
        root.geometry("350x120")
        root.resizable(False, False)
        nomeUsuario = {"valor": ""}

        def fechar():
            root.destroy()

        def usarVoz():
            nome = reconhecerVoz()
            if nome:
                nomeUsuario["valor"] = nome
                root.destroy()
                falarBemVindo(nome)

        def usarTexto():
            def enviarNome():
                nome = entryNome.get()
                if nome:
                    nomeUsuario["valor"] = nome
                    janelaNome.destroy()
                    root.destroy()
                    falarBemVindo(nome)
                else:
                    messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
            janelaNome = tk.Toplevel(root)
            janelaNome.title("Digite seu nome")
            janelaNome.geometry("300x80")
            tk.Label(janelaNome, text="Digite seu nome:").pack(pady=5)
            entryNome = tk.Entry(janelaNome)
            entryNome.pack()
            tk.Button(janelaNome, text="Enviar", command=enviarNome).pack(pady=5)
            janelaNome.transient(root)
            janelaNome.grab_set()
            janelaNome.wait_window()

        label = tk.Label(root, text="Como você deseja informar seu nome?", font=("Arial", 11))
        label.pack(pady=10)
        frameBotoes = tk.Frame(root)
        frameBotoes.pack()
        btnVoz = tk.Button(frameBotoes, text="Falar", width=12, command=usarVoz)
        btnVoz.grid(row=0, column=0, padx=10)
        btnTexto = tk.Button(frameBotoes, text="Digitar", width=12, command=usarTexto)
        btnTexto.grid(row=0, column=1, padx=10)
        root.protocol("WM_DELETE_WINDOW", fechar)
        root.mainloop()
        return nomeUsuario["valor"]

    def telaBoasVindas(nome):
        larguraBotaoIniciar = 320
        alturaBotaoIniciar = 70
        explicacao = [
            "Bem-vindo ao jogo, {}!".format(nome),
            "",
            "Mecânica:",
            "- Use as setas ou A/D para mover a nave.",
            "- Clique com o botão esquerdo do mouse para atirar.",
            "- Destrua naves inimigas para ganhar pontos.",
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
                    if 'botaoIniciar' in locals() and botaoIniciar.collidepoint(evento.pos):
                        return
            tela.fill(corBranca)
            tela.blit(telaInicial, (0, 0))
            y = 120
            linhasRenderizadas = []
            larguraMaxima = 0
            alturaTotal = 0
            for linha in explicacao:
                fonte = fonteMenu if linha.startswith("Bem-vindo") else pygame.font.SysFont("arial", 28)
                texto = fonte.render(linha.replace("{}".format(nome), nome), True, corBranca)
                linhasRenderizadas.append((texto, fonte))
                larguraMaxima = max(larguraMaxima, texto.get_width())
                alturaTotal += texto.get_height() + 10
            alturaTotal -= 10
            margemX = 40
            margemY = 40
            posicaoXRetangulo = (tamanhoTela[0] - larguraMaxima) // 2 - margemX
            posicaoYRetangulo = 120 - margemY
            larguraRetangulo = larguraMaxima + 2 * margemX
            alturaRetangulo = alturaTotal + 2 * margemY
            pygame.draw.rect(tela, corPreta, (posicaoXRetangulo, posicaoYRetangulo, larguraRetangulo, alturaRetangulo), border_radius=20)
            yTexto = 120
            for texto, fonte in linhasRenderizadas:
                tela.blit(texto, ((tamanhoTela[0] - texto.get_width()) // 2, yTexto))
                yTexto += texto.get_height() + 10
            botaoIniciar = pygame.draw.rect(
                tela, corPreta,
                ((tamanhoTela[0] - larguraBotaoIniciar) // 2, yTexto + 40, larguraBotaoIniciar, alturaBotaoIniciar),
                border_radius=15
            )
            textoIniciar = fonteMenu.render("INICIAR PARTIDA", True, corBranca)
            tela.blit(
                textoIniciar,
                ((tamanhoTela[0] - textoIniciar.get_width()) // 2, yTexto + 40 + (alturaBotaoIniciar - textoIniciar.get_height()) // 2)
            )
            pygame.display.update()
            relogio.tick(60)

    nome = obterNome()
    if not nome:
        return
    telaBoasVindas(nome)
    posicaoXNave = 400
    posicaoYNave = 450
    pontos = 0
    larguraNave = 200
    alturaNave = 120
    naveRedimensionada = pygame.transform.smoothscale(naveJogador, (larguraNave, alturaNave))
    larguraNaveInimiga = int(larguraNave * 0.7)
    alturaNaveInimiga = int(alturaNave * 0.7)
    naveInimigaRedimensionada = pygame.transform.smoothscale(naveInimiga, (larguraNaveInimiga, alturaNaveInimiga))
    listaNavesInimigas = []
    quantidadeInicialNaves = 2
    velocidadeNaveInimiga = 4
    velocidadeMaxima = 15
    tempoUltimaNave = pygame.time.get_ticks()
    intervaloNovaNave = 2000
    for _ in range(quantidadeInicialNaves):
        x = random.randint(0, tamanhoTela[0] - larguraNaveInimiga)
        y = random.randint(-600, -alturaNaveInimiga)
        listaNavesInimigas.append({'x': x, 'y': y, 'vel': velocidadeNaveInimiga})
    listaTiros = []
    larguraTiro = 8
    alturaTiro = 30
    corTiro = (255, 50, 50)
    velocidadeTiro = 13
    escalaLua = 0.25
    mudancaEscala = 0.01
    escalaMin = 0.20
    escalaMax = 0.30
    pygame.mixer.Sound.play(somNave)
    pygame.mixer.music.play(-1)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausarJogo()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    xTiro = posicaoXNave + larguraNave // 2 - larguraTiro // 2
                    yTiro = posicaoYNave
                    listaTiros.append({'x': xTiro, 'y': yTiro})
        teclas = pygame.key.get_pressed()
        movimentoXNave = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimentoXNave = -9
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimentoXNave = 9
        posicaoXNave += movimentoXNave
        if posicaoXNave < 0:
            posicaoXNave = 0
        elif posicaoXNave > tamanhoTela[0] - larguraNave:
            posicaoXNave = tamanhoTela[0] - larguraNave
        escalaLua += mudancaEscala
        if escalaLua >= escalaMax or escalaLua <= escalaMin:
            mudancaEscala *= -1
        larguraLua = int(imagemLua.get_width() * escalaLua)
        alturaLua = int(imagemLua.get_height() * escalaLua)
        luaRedimensionada = pygame.transform.smoothscale(imagemLua, (larguraLua, alturaLua))
        tela.fill(corBranca)
        tela.blit(fundoJogo, (0, 0))
        posicaoXLua = tamanhoTela[0] - larguraLua - 20
        posicaoYLua = 20
        tela.blit(luaRedimensionada, (posicaoXLua, posicaoYLua))
        tela.blit(naveRedimensionada, (posicaoXNave, posicaoYNave))
        adicionarEstrela()
        for naveInimigaObj in listaNavesInimigas:
            naveInimigaObj['y'] += naveInimigaObj['vel']
            tela.blit(naveInimigaRedimensionada, (naveInimigaObj['x'], naveInimigaObj['y']))
        for naveInimigaObj in listaNavesInimigas[:]:
            if naveInimigaObj['y'] > tamanhoTela[1]:
                listaNavesInimigas.remove(naveInimigaObj)
                pontos += 1
                novaVel = min(naveInimigaObj['vel'] + 0.3, velocidadeMaxima)
                x = random.randint(0, tamanhoTela[0] - larguraNaveInimiga)
                y = random.randint(-600, -alturaNaveInimiga)
                listaNavesInimigas.append({'x': x, 'y': y, 'vel': novaVel})
        tempoAtual = pygame.time.get_ticks()
        if tempoAtual - tempoUltimaNave > intervaloNovaNave and len(listaNavesInimigas) < 8:
            x = random.randint(0, tamanhoTela[0] - larguraNaveInimiga)
            y = random.randint(-600, -alturaNaveInimiga)
            vel = min(velocidadeNaveInimiga + pontos * 0.1, velocidadeMaxima)
            listaNavesInimigas.append({'x': x, 'y': y, 'vel': vel})
            tempoUltimaNave = tempoAtual
            if intervaloNovaNave > 700:
                intervaloNovaNave -= 30
        for tiro in listaTiros[:]:
            tiro['y'] -= velocidadeTiro
            pygame.draw.rect(tela, corTiro, (tiro['x'], tiro['y'], larguraTiro, alturaTiro))
            if tiro['y'] < -alturaTiro:
                listaTiros.remove(tiro)
        for tiro in listaTiros[:]:
            retTiro = pygame.Rect(tiro['x'], tiro['y'], larguraTiro, alturaTiro)
            for naveInimigaObj in listaNavesInimigas[:]:
                retInimiga = pygame.Rect(naveInimigaObj['x'], naveInimigaObj['y'], larguraNaveInimiga, alturaNaveInimiga)
                if retTiro.colliderect(retInimiga):
                    listaTiros.remove(tiro)
                    listaNavesInimigas.remove(naveInimigaObj)
                    pontos += 1
                    break
        textoPlacar = fonteMenu.render(f"Pontos: {pontos}", True, corBranca)
        tela.blit(textoPlacar, (20, 20))
        fontePausaLateral = pygame.font.SysFont("arial", 18)
        textoPausa = fontePausaLateral.render("Press SPACE to pause", True, corPreta)
        tela.blit(textoPausa, (textoPlacar.get_width() + 40, 15))
        retJogador = pygame.Rect(posicaoXNave, posicaoYNave, larguraNave, alturaNave)
        for naveInimigaObj in listaNavesInimigas:
            retInimiga = pygame.Rect(naveInimigaObj['x'], naveInimigaObj['y'], larguraNaveInimiga, alturaNaveInimiga)
            if retJogador.colliderect(retInimiga):
                escreverDados(nome, pontos)
                dead(pontos)
        pygame.display.update()
        relogio.tick(60)

def dead(pontosFinais):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(somExplosao)
    larguraBotaoIniciar = 200
    alturaBotaoIniciar = 50
    larguraBotaoSair = 200
    alturaBotaoSair = 50
    try:
        with open("log.dat", "r", encoding="utf-8") as f:
            logPartidas = json.load(f)
        ultimosRegistros = list(logPartidas.items())[-5:]
    except Exception:
        ultimosRegistros = []
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP or evento.type == pygame.MOUSEBUTTONDOWN:
                if 'botaoIniciar' in locals() and botaoIniciar.collidepoint(evento.pos):
                    larguraBotaoIniciar = 200
                    alturaBotaoIniciar = 50
                    jogar()
                if 'botaoSair' in locals() and botaoSair.collidepoint(evento.pos):
                    larguraBotaoSair = 200
                    alturaBotaoSair = 50
                    sys.exit()
        tela.fill(corBranca)
        tela.blit(fundoMorte, (0, 0))
        fonteLog = pygame.font.SysFont("arial", 24)
        textoTitulo = fonteMenu.render("Log das Últimas 5 Partidas", True, corBranca)
        logsRenderizados = []
        larguraMaxima = textoTitulo.get_width()
        alturaTotal = textoTitulo.get_height() + 20
        for data, (pontosLog, dataHoraLog) in reversed(ultimosRegistros):
            textoLog = fonteLog.render(f"Pontos: {pontosLog} | Data: {dataHoraLog}", True, corBranca)
            logsRenderizados.append(textoLog)
            larguraMaxima = max(larguraMaxima, textoLog.get_width())
            alturaTotal += textoLog.get_height() + 10
        alturaTotal -= 10
        margemX = 40
        margemY = 30
        posicaoXRetangulo = (tamanhoTela[0] - larguraMaxima) // 2 - margemX
        posicaoYRetangulo = 180
        larguraRetangulo = larguraMaxima + 2 * margemX
        alturaRetangulo = alturaTotal + 2 * margemY
        pygame.draw.rect(tela, corPreta, (posicaoXRetangulo, posicaoYRetangulo, larguraRetangulo, alturaRetangulo), border_radius=20)
        yLog = posicaoYRetangulo + margemY
        tela.blit(textoTitulo, ((tamanhoTela[0] - textoTitulo.get_width()) // 2, yLog))
        yLog += textoTitulo.get_height() + 20
        for textoLog in logsRenderizados:
            tela.blit(textoLog, ((tamanhoTela[0] - textoLog.get_width()) // 2, yLog))
            yLog += textoLog.get_height() + 10
        espacamentoBotoes = 40
        botoesY = posicaoYRetangulo + alturaRetangulo + espacamentoBotoes
        botaoIniciar = pygame.draw.rect(
            tela, corBranca,
            ((tamanhoTela[0] // 2) - larguraBotaoIniciar - 20, botoesY, larguraBotaoIniciar, alturaBotaoIniciar),
            border_radius=15
        )
        textoIniciar = fonteMenu.render("INICIAR", True, corPreta)
        tela.blit(
            textoIniciar,
            ((tamanhoTela[0] // 2) - larguraBotaoIniciar - 20 + (larguraBotaoIniciar - textoIniciar.get_width()) // 2,
             botoesY + (alturaBotaoIniciar - textoIniciar.get_height()) // 2)
        )
        botaoSair = pygame.draw.rect(
            tela, corBranca,
            ((tamanhoTela[0] // 2) + 20, botoesY, larguraBotaoSair, alturaBotaoSair),
            border_radius=15
        )
        textoSair = fonteMenu.render("SAIR", True, corPreta)
        tela.blit(
            textoSair,
            ((tamanhoTela[0] // 2) + 20 + (larguraBotaoSair - textoSair.get_width()) // 2,
             botoesY + (alturaBotaoSair - textoSair.get_height()) // 2)
        )
        pygame.display.update()
        relogio.tick(60)

def start():
    larguraBotaoIniciar = 200
    alturaBotaoIniciar = 50
    larguraBotaoSair = 200
    alturaBotaoSair = 50
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if 'botaoIniciar' in locals() and botaoIniciar.collidepoint(evento.pos):
                    larguraBotaoIniciar = 200
                    alturaBotaoIniciar = 50
                if 'botaoSair' in locals() and botaoSair.collidepoint(evento.pos):
                    larguraBotaoSair = 200
                    alturaBotaoSair = 50
            elif evento.type == pygame.MOUSEBUTTONUP:
                if 'botaoIniciar' in locals() and botaoIniciar.collidepoint(evento.pos):
                    larguraBotaoIniciar = 180
                    alturaBotaoIniciar = 40
                    jogar()
                if 'botaoSair' in locals() and botaoSair.collidepoint(evento.pos):
                    larguraBotaoSair = 180
                    alturaBotaoSair = 40
                    sys.exit()
        tela.fill(corBranca)
        tela.blit(telaInicial, (0, 0))
        botaoIniciar = pygame.draw.rect(tela, corBranca, ((tamanhoTela[0] - larguraBotaoIniciar) / 2, (tamanhoTela[1] / 2) - alturaBotaoIniciar, larguraBotaoIniciar, alturaBotaoIniciar), border_radius=15)
        textoIniciar = fonteMenu.render("INICIAR", True, corPreta)
        tela.blit(textoIniciar, ((tamanhoTela[0] - larguraBotaoIniciar + 65) / 2, (tamanhoTela[1] / 2) - alturaBotaoIniciar + 5))
        botaoSair = pygame.draw.rect(tela, corBranca, ((tamanhoTela[0] - larguraBotaoSair) / 2, (tamanhoTela[1] / 2) + alturaBotaoSair / 2, larguraBotaoSair, alturaBotaoSair), border_radius=15)
        textoSair = fonteMenu.render("SAIR", True, corPreta)
        tela.blit(textoSair, ((tamanhoTela[0] - larguraBotaoSair + 110) / 2, (tamanhoTela[1] / 2) + alturaBotaoSair / 2 + 5))
        pygame.display.update()
        relogio.tick(60)

start()