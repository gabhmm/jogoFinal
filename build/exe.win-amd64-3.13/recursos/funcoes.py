import os
import json
import datetime

def inicializarBancoDeDados():
    try:
        banco = open("log.dat", "r")
        banco.close()
    except:
        with open("log.dat", "w", encoding="utf-8") as banco:
            json.dump({}, banco)

def escreverDados(nome, pontos):
    dataHora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    novoRegistro = [pontos, dataHora]
    if os.path.exists("log.dat"):
        with open("log.dat", "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except Exception:
                dados = {}
    else:
        dados = {}
    chave = f"{nome} - {dataHora}"
    dados[chave] = novoRegistro
    with open("log.dat", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)