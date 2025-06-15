import os
import json
import datetime

def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("log.dat","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("log.dat","w")

    
def escreverDados(nome, pontos):
    # Gera data e hora no formato desejado
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    novo_registro = [pontos, data_hora]
    if os.path.exists("log.dat"):
        with open("log.dat", "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except Exception:
                dados = {}
    else:
        dados = {}
    dados[nome] = novo_registro
    with open("log.dat", "w", encoding="utf-8") as f:
        json.dump(dados, f)