# 🌌 Space Defender

**Desenvolvedor:** Gabriel M Magalhaes  
**RA:** 1137910  
**Curso:** Ciência da Computação - 1º Semestre

**Testador do Jogo:** Gustavo Barbosa Portela | 1137640

---

## 🚀 Descrição do Jogo

Space Defender é um jogo de nave espacial no estilo arcade clássico, onde o jogador controla uma nave de combate contra hordas de inimigos. Inspirado nos grandes sucessos dos anos 80 e 90, o jogo apresenta:

- 🕹 Controles simples e intuitivos
- 👾 Inimigos aleatórios e em quantidade crescente
- ✨ Efeitos visuais retro
- 🎵 Trilha sonora épica (Megalovania)
- 🗣️ Entrada de nome por voz ou texto
- 📝 Registro automático das últimas partidas

**História:**  
No ano de 2147, a Terra está sob ataque das forças inimigas. Como piloto da elite espacial, sua missão é proteger o planeta destruindo o máximo de naves inimigas possível.

---

## 💻 Tecnologias Utilizadas

| Componente             | Tecnologia         |
|------------------------|-------------------|
| **Linguagem**          | Python            |
| **Biblioteca Principal** | PyGame          |
| **Interface de Menu**  | Tkinter           |
| **Reconhecimento de Voz** | SpeechRecognition |
| **Síntese de Voz**     | pyttsx3           |
| **Armazenamento de Dados** | JSON          |

---

## 🎮 Como Jogar

### Início
- Ao iniciar, escolha informar seu nome por voz (microfone) ou digitando.
- Uma tela de boas-vindas explica as mecânicas do jogo.

### Controles
- **Setas direcionais ou A/D:** Movimentação da nave
- **Clique esquerdo do mouse:** Atira
- **Barra de espaço:** Pausa o jogo

### Objetivo
- **Destrua naves inimigas** para ganhar pontos.
- **Desvie das naves inimigas** para não perder.
- A cada colisão, o jogo termina e mostra um log das últimas 5 partidas.

### Pontuação e Log
- Cada nave inimiga destruída soma pontos.
- Ao perder, um log das últimas 5 partidas é exibido, mostrando data e pontuação.
- O log é salvo automaticamente no arquivo `log.dat`.

---