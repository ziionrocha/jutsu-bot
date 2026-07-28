import tkinter as tk
from tkinter import ttk
import pyautogui
import pydirectinput
import cv2
import numpy as np
import time
import keyboard
import threading
import queue
import os
import sys
from datetime import datetime

pydirectinput.PAUSE = 0


def resource_path(relative_path):
    """Resolve o caminho de um recurso tanto rodando como script quanto
    empacotado como .exe (PyInstaller extrai os dados pra uma pasta temporária)."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ==============================
# CONFIGURAÇÃO
# ==============================

AREA = (400, 100, 1100, 150)

# Pasta onde ficam os prints dos jutsus
TEMPLATES_DIR = resource_path("templates")

jutsus = {
    "bola_de_fogo.png": "ZVCB",
    "confusao_mental.png": "VZBX",
    "descarga_eletrica.png": "NVXVBN",
    "desvanecimento_de_presenca.png": "VZVB",
    "flecha_trovao.png": "NVCB",
    "flor_de_fenix.png": "ZVXZ",
    "investida_molhada.png": "XVCB",
    "mascara_do_sofrimento.png": "ZVXCXZ",
    "onda_de_vacuo.png": "BVNB",
    "ondas_furiosas.png": "XVZXCX",
    "parede_de_terra.png": "CVC",
    "parede_do_vendaval.png": "BVNCXC",
    "pistola_de_pedra.png": "CVBX",
    "prisao_de_agua.png": "XVXCVZ",
    "punho_de_rocha.png": "CVBC",
    "rio_de_lama.png": "CVZX",
    "senbon_relampago.png": "NVXZCN",
    "tiros_de_agua.png": "XVBX",
    "veu_da_letargia.png": "VZC",
    "visao_distorcida.png": "VZV",
    "pantano_do_submundo.png": "CVZCXB",
    "fenda_terrestre.png": "CVBXVC",
    "toujinbou.png": "CVBCXZCV",
    "domo_de_terra.png": "CVCXZCXC",
    "falsa_escuridao.png": "NVBNCVBN",
    "suishoha.png": "XVBNXZVX",
    "dragao_dagua.png": "XVZXVCXB",
    "furacao_das_chamas.png": "ZVBXCXCZ",
    "leque_das_chamas.png": "ZVBNXZ",
    "aniquilacao_de_fogo.png": "ZVXCXZBZ",
    "abismo_dos_sonhos.png": "VBNBXC",
    "estrangulamento_das_plantas.png": "VBCX",
    "colapso_dos_cinco_sentidos.png": "VZNX",
    "revelar_ilusoes.png": "VBNV",
    "mundo_ilusorio.png": "VBNVBC",
    "arauto_das_trevas.png": "VZVXVZ",
    "coroa_agonizante.png": "VBZXZV",
    "inimigo_fantasma.png": "VZXCVZ",
    "vendaval_divino.png": "BVNVCXVB",
    "ruptura_do_vento.png": "BVCVBN",
    "dano_de_pressao.png": "BVCXCVCX",
}


# ==============================
# LÓGICA DO BOT (roda em thread separada)
# ==============================

class JutsuBot:
    def __init__(self, log_queue):
        self.running = False
        self.thread = None
        self.log_queue = log_queue

    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {msg}")

    def _checar_templates(self):
        if not os.path.isdir(TEMPLATES_DIR):
            self.log(f"AVISO: pasta '{TEMPLATES_DIR}/' não encontrada")
            return
        faltando = [
            nome for nome in jutsus
            if not os.path.isfile(os.path.join(TEMPLATES_DIR, nome))
        ]
        if faltando:
            self.log(f"AVISO: {len(faltando)} imagem(ns) não encontrada(s) em '{TEMPLATES_DIR}/'")

    def start(self):
        if self.running:
            return
        self._checar_templates()
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        self.log("Bot ativado")

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.log("Bot desativado")

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def capturar(self):
        screenshot = pyautogui.screenshot(region=AREA)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    def comparar(self, tela, imagem):
        caminho = os.path.join(TEMPLATES_DIR, imagem)
        template = cv2.imread(caminho, 0)
        if template is None:
            return 0
        resultado = cv2.matchTemplate(tela, template, cv2.TM_CCOEFF_NORMED)
        _, maior, _, _ = cv2.minMaxLoc(resultado)
        return maior

    def enviar_jutsu(self, comando):
        for tecla in comando:
            pydirectinput.keyDown(tecla.lower())
            time.sleep(0.08)
            pydirectinput.keyUp(tecla.lower())
            time.sleep(0.06)
        time.sleep(0.05)
        pydirectinput.click()

    def _loop(self):
        while self.running:
            try:
                tela = self.capturar()

                melhor_valor = 0
                melhor_jutsu = None

                for imagem, comando in jutsus.items():
                    valor = self.comparar(tela, imagem)
                    if valor > melhor_valor:
                        melhor_valor = valor
                        melhor_jutsu = comando

                if melhor_valor > 0.8:
                    self.log(f"Detectado: {melhor_jutsu} | confiança: {round(melhor_valor, 3)}")
                    self.enviar_jutsu(melhor_jutsu)
                    time.sleep(2)
                else:
                    time.sleep(0.05)
            except Exception as e:
                self.log(f"Erro: {e}")
                time.sleep(0.5)


# ==============================
# INTERFACE GRÁFICA
# ==============================

BG_DARK = "#1e1e2e"
BG_CARD = "#282838"
ACCENT_ON = "#4ade80"
ACCENT_OFF = "#f87171"
TEXT_MAIN = "#e5e5f0"
TEXT_DIM = "#9494a8"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Jutsu Bot")
        self.root.geometry("480x420")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.log_queue = queue.Queue()
        self.bot = JutsuBot(self.log_queue)

        self._build_ui()
        self._poll_log()

        # Hotkey global F6 para ligar/desligar
        keyboard.add_hotkey("F6", self.toggle_bot)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        # Cabeçalho
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(
            header, text="Jutsu Bot", font=("Segoe UI", 20, "bold"),
            bg=BG_DARK, fg=TEXT_MAIN
        ).pack(anchor="w")

        tk.Label(
            header, text="Reconhecimento automático de jutsus",
            font=("Segoe UI", 10), bg=BG_DARK, fg=TEXT_DIM
        ).pack(anchor="w")

        # Card de status
        card = tk.Frame(self.root, bg=BG_CARD)
        card.pack(fill="x", padx=20, pady=10)

        status_row = tk.Frame(card, bg=BG_CARD)
        status_row.pack(fill="x", padx=16, pady=16)

        self.status_dot = tk.Canvas(status_row, width=14, height=14, bg=BG_CARD, highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 10))
        self.dot_id = self.status_dot.create_oval(2, 2, 12, 12, fill=ACCENT_OFF, outline="")

        self.status_label = tk.Label(
            status_row, text="Desativado", font=("Segoe UI", 13, "bold"),
            bg=BG_CARD, fg=TEXT_MAIN
        )
        self.status_label.pack(side="left")

        tk.Label(
            status_row, text="  (F6 para alternar)", font=("Segoe UI", 9),
            bg=BG_CARD, fg=TEXT_DIM
        ).pack(side="left")

        # Botão principal
        self.toggle_btn = tk.Button(
            self.root, text="▶  ATIVAR BOT", font=("Segoe UI", 12, "bold"),
            bg=ACCENT_ON, fg="#0f0f16", activebackground="#22c55e",
            bd=0, relief="flat", height=2, cursor="hand2",
            command=self.toggle_bot
        )
        self.toggle_btn.pack(fill="x", padx=20, pady=(0, 10))

        # Log
        log_label = tk.Label(
            self.root, text="Atividade", font=("Segoe UI", 10, "bold"),
            bg=BG_DARK, fg=TEXT_DIM
        )
        log_label.pack(anchor="w", padx=20)

        log_frame = tk.Frame(self.root, bg=BG_CARD)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(4, 20))

        self.log_text = tk.Text(
            log_frame, bg=BG_CARD, fg=TEXT_MAIN, font=("Consolas", 9),
            bd=0, highlightthickness=0, wrap="word", state="disabled"
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_bot(self):
        self.bot.toggle()
        self._update_status()

    def _update_status(self):
        if self.bot.running:
            self.status_dot.itemconfig(self.dot_id, fill=ACCENT_ON)
            self.status_label.config(text="Ativado")
            self.toggle_btn.config(
                text="⏸  DESATIVAR BOT", bg=ACCENT_OFF, activebackground="#ef4444"
            )
        else:
            self.status_dot.itemconfig(self.dot_id, fill=ACCENT_OFF)
            self.status_label.config(text="Desativado")
            self.toggle_btn.config(
                text="▶  ATIVAR BOT", bg=ACCENT_ON, activebackground="#22c55e"
            )

    def _poll_log(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.config(state="normal")
                self.log_text.insert("end", msg + "\n")
                self.log_text.see("end")
                self.log_text.config(state="disabled")
        except queue.Empty:
            pass
        self.root.after(150, self._poll_log)

    def _on_close(self):
        self.bot.stop()
        keyboard.unhook_all_hotkeys()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
