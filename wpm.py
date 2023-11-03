import time
import random
import curses
from curses import wrapper


def inicio_tela(stdscr):
	stdscr.clear()
	stdscr.addstr("Bem vindo ao teste de digitação!")
	stdscr.addstr("\nPressione qualquer tecla para continuar...")
	stdscr.refresh()
	stdscr.getkey()


def exibir_texto(stdscr, alvo, atual, wpm=0):
	stdscr.addstr(alvo)
	stdscr.addstr(1, 0, f"WPM: {wpm}")

	for i, char in enumerate(atual):
		char_correto = alvo[i]
		color = curses.color_pair(1)
		if char != char_correto:
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)


def carregar_texto():
	with open("texto.txt", "r") as f:
		linhas = f.readlines()
		return random.choice(linhas).strip()


def teste_wpm(stdscr):
	texto_alvo = carregar_texto()
	texto_atual = []
	wpm = 0
	inicio_tempo = time.time()
	stdscr.nodelay(True)

	while True:
		tempo_decorrido = max(time.time() - inicio_tempo, 1)
		wpm = round((len(texto_atual) / (tempo_decorrido / 60)) / 5)

		stdscr.clear()
		exibir_texto(stdscr, texto_alvo, texto_atual, wpm)
		stdscr.refresh()

		if "".join(texto_atual) == texto_alvo:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

# ord(key) == representação numérica no teclado em ASCII | 27 ≡ esc
		if ord(key) == 27:
			break

# curses obriga-nos a lidar com a exclusão de caractéres manualmente; do contrário o cursor só volta a posição anterior.
		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(texto_atual) > 0:
				texto_atual.pop()
		elif len(texto_atual) < len(texto_alvo):
			texto_atual.append(key)


def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	inicio_tela(stdscr)

	while True:
		teste_wpm(stdscr)
		stdscr.addstr(2, 0, "Você finalizou o teste, meus parabéns! Pressione 'esc' para sair ou qualquer tecla para continuar...")
		key = stdscr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)