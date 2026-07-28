import pyautogui
import pydirectinput
import cv2
import numpy as np
import time
import keyboard


# ==============================
# CONFIGURAÇÃO
# ==============================

pydirectinput.PAUSE = 0


# Área do jutsu
AREA = (400, 100, 1100, 150)


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
# FUNÇÕES
# ==============================

def capturar():

    screenshot = pyautogui.screenshot(region=AREA)

    return cv2.cvtColor(
        np.array(screenshot),
        cv2.COLOR_RGB2GRAY
    )



def comparar(tela, imagem):

    template = cv2.imread(imagem, 0)

    if template is None:
        return 0


    resultado = cv2.matchTemplate(
        tela,
        template,
        cv2.TM_CCOEFF_NORMED
    )


    _, maior, _, _ = cv2.minMaxLoc(resultado)

    return maior



def enviar_jutsu(comando):

    for tecla in comando:

        pydirectinput.keyDown(tecla.lower())

        time.sleep(0.08)

        pydirectinput.keyUp(tecla.lower())

        time.sleep(0.06)


    time.sleep(0.05)

    pydirectinput.click()



# ==============================
# LOOP
# ==============================

print("Iniciando em 2 segundos...")
time.sleep(2)


while True:


    if keyboard.is_pressed("esc"):

        print("Bot parado!")

        break



    tela = capturar()


    melhor_valor = 0
    melhor_jutsu = None



    for imagem, comando in jutsus.items():

        valor = comparar(tela, imagem)


        if valor > melhor_valor:

            melhor_valor = valor
            melhor_jutsu = comando



    if melhor_valor > 0.8:


        print(
            "Detectado:",
            melhor_jutsu,
            "| confiança:",
            round(melhor_valor, 3),
            flush=True
        )


        enviar_jutsu(melhor_jutsu)


        # espera o jogo terminar o jutsu
        time.sleep(2)