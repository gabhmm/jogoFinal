import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox
import pyttsx3

def reconhecerVoz():
    reconhecedor = sr.Recognizer()
    janelaOuvindo = tk.Toplevel()
    janelaOuvindo.title("Ouvindo...")
    janelaOuvindo.geometry("250x80")
    janelaOuvindo.resizable(False, False)
    label_ouvindo = tk.Label(janelaOuvindo, text="Ouvindo...", font=("Arial", 16))
    label_ouvindo.pack(expand=True, pady=20)
    janelaOuvindo.update()
    janelaOuvindo.lift()
    janelaOuvindo.attributes('-topmost', True)
    janelaOuvindo.after(100, lambda: janelaOuvindo.focus_force())
    nome = ""
    with sr.Microphone() as fonte:
        try:
            janelaOuvindo.update()
            audio = reconhecedor.listen(fonte, timeout=5)
            nome = reconhecedor.recognize_google(audio, language="pt-BR")
        except sr.WaitTimeoutError:
            messagebox.showerror("Erro", "Tempo esgotado. Tente novamente.")
        except sr.UnknownValueError:
            messagebox.showerror("Erro", "Não foi possível reconhecer o nome. Tente novamente.")
        except sr.RequestError:
            messagebox.showerror("Erro", "Erro ao acessar o serviço de reconhecimento.")
    janelaOuvindo.destroy()
    return nome

def falarBemVindo(nome):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.say(f"Bem vindo, {nome}!")
    engine.runAndWait()