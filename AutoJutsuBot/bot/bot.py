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
    "templates/bola_de_fogo.png": "ZVCB",
    "templates/confusao_mental.png": "VZBX",
    "templates/descarga_eletrica.png": "NVXVBN",
    "templates/desvanecimento_de_presenca.png": "VZVB",
    "templates/flecha_trovao.png": "NVCB",
    "templates/flor_de_fenix.png": "ZVXZ",
    "templates/investida_molhada.png": "XVCB",
    "templates/mascara_do_sofrimento.png": "ZVXCXZ",
    "templates/onda_de_vacuo.png": "BVNB",
    "templates/ondas_furiosas.png": "XVZXCX",
    "templates/parede_de_terra.png": "CVC",
    "templates/parede_do_vendaval.png": "BVNCXC",
    "templates/pistola_de_pedra.png": "CVBX",
    "templates/prisao_de_agua.png": "XVXCVZ",
    "templates/punho_de_rocha.png": "CVBC",
    "templates/rio_de_lama.png": "CVZX",
    "templates/senbon_relampago.png": "NVXZCN",
    "templates/tiros_de_agua.png": "XVBX",
    "templates/veu_da_letargia.png": "VZC",
    "templates/visao_distorcida.png": "VZV",
    "templates/pantano_do_submundo.png": "CVZCXB",
    "templates/fenda_terrestre.png": "CVBXVC",
    "templates/toujinbou.png": "CVBCXZCV",
    "templates/domo_de_terra.png": "CVCXZCXC",
    "templates/falsa_escuridao.png": "NVBNCVBN",
    "templates/suishoha.png": "XVBNXZVX",
    "templates/dragao_dagua.png": "XVZXVCXB",
    "templates/furacao_das_chamas.png": "ZVBXCXCZ",
    "templates/leque_das_chamas.png": "ZVBNXZ",
    "templates/aniquilacao_de_fogo.png": "ZVXCXZBZ",
    "templates/abismo_dos_sonhos.png": "VBNBXC",
    "templates/estrangulamento_das_plantas.png": "VBCX",
    "templates/colapso_dos_cinco_sentidos.png": "VZNX",
    "templates/revelar_ilusoes.png": "VBNV",
    "templates/mundo_ilusorio.png": "VBNVBC",
    "templates/arauto_das_trevas.png": "VZVXVZ",
    "templates/coroa_agonizante.png": "VBZXZV",
    "templates/inimigo_fantasma.png": "VZXCVZ",
    "templates/vendaval_divino.png": "BVNVCXVB",
    "templates/ruptura_do_vento.png": "BVCVBN",
    "templates/dano_de_pressao.png": "BVCXCVCX",
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