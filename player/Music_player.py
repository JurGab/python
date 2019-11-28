import os
from tkinter import *
from pygame import mixer 		#praacuje len s .wav subormy
from mutagen.mp3 import MP3 	#pracuje so zvukovymi subormy
from tkinter import filedialog
import tkinter.messagebox
import threading
import time

hlavne_okno = Tk()
# hlavne_okno.geometry('300x500')
hlavne_okno.title('Gabriel\'s player')
hlavne_okno.iconbitmap('gytara.ico')

#status bar, bd - border, sunken-vnorene, anchor - prilepene na danu stranu
statusbar = Label(hlavne_okno, text='Moj prehravac', bd=1, relief=SUNKEN, anchor=W)
#sticky w+e roztiahne v ramci gridu z lava do prava
statusbar.pack(side=BOTTOM, fill=X)

#vytvorime 2 frames ktore rozdelia okno na lavu a pravu stranu
#lava strana obsahuje playlist, prava vsetko ostatne
lavy_frame = Frame(hlavne_okno)
lavy_frame.pack(side=LEFT, padx=10)

pravy_frame = Frame(hlavne_okno)
pravy_frame.pack()

vrchny_frame = Frame(pravy_frame)
vrchny_frame.pack()

#zobrazenie detailov pesnicky v hlavnom okne
detaily = Label(hlavne_okno, text='...')
detaily.pack()

#zobrazenie celkovej dlzky pesnicky v hlavnom okne
dlzka_pesnicky = Label(vrchny_frame, text='Dlzka pesnicky --:--')
dlzka_pesnicky.pack()

#zobrazenie aktualnej dlzky pesnicky v hlavnom okne
dlzka_pesnicky_akt = Label(vrchny_frame, text='Aktualna dlzka pesnicky --:--')
dlzka_pesnicky_akt.pack()

#vytvorenie frame v ramci hlavneho okna. 
stredny_frame = Frame(pravy_frame)
stredny_frame.pack()

#novy frame pre hlasitost
spodny_frame = Frame(pravy_frame)
spodny_frame.pack()

def ukaz_detaily():
	#zobrazi nazov pesnicky
	detaily['text'] = 'Prehravam ' + '-' + os.path.basename(subor)
	#rozdeli nazov suboru na 2 casti v liste, nazov a pripona
	subor_data = os.path.splitext(subor)

	#pokial je subor s priponou mp3, zisti jej dlzku
	if subor_data[1] == '.mp3':
		pesnicka = MP3(subor)
		celk_dlzka = pesnicka.info.length
	else:
	#pre subory ak nie su mp3
	#nacita subor do 'd' a potom vrati dlzku pesnicky v sekundach do celk_dlzka
		d = mixer.Sound(subor)
		celk_dlzka = d.get_length()

	# #divmod vydeli celk_dlzka 60-timi a vysledok ulozi do mins, zostatok po 
	# deleni do secs
	mins, secs = divmod(celk_dlzka, 60)
	mins = round(mins)
	secs = round(secs)
	cas_format = '{:02d}:{:02d}'.format(mins, secs)
	dlzka_pesnicky['text'] = 'Dlzka pesnicky ' + cas_format
	#zavola funkciu na odpocitavanie celkoveho casu pesnicky po sekundach
	#odpocet_casu je while funkcia. Pokial je while aktivne, nie je mozne
	#robit nic ine v programe. Preto sa vytvori vlakno Thread, aby mohlo
	#subezne ist viacero cinnosti
	vlakno1 = threading.Thread(target=odpocet_casu, args=(celk_dlzka, ))
	vlakno1.start()

#funkcia na odpocitavanie zostavajuceho casu pesnicky
def odpocet_casu(cas):
	#aby sme vedeli nacitat hodnotu pauznute ktore je mimo odpocet_casu
	global pauznute
	#cas je na zaciatku rovny celk_dlzka
	#get_busy vrati false ak sa zastavi prehravanie a tym sa zastavi cas
	while cas and mixer.music.get_busy():
		#continue - pokial je pauznute tak sa ignoruje vsetko dalsie vo
		#funkcii 
		if pauznute:
			continue
		else:
			mins, secs = divmod(cas, 60)
			mins = round(mins)
			secs = round(secs)
			cas_format = '{:02d}:{:02d}'.format(mins, secs)
			dlzka_pesnicky_akt['text'] = 'Aktualna dlzka pesnicky ' + cas_format
			#urobi pauzu na 1 sekundu
			time.sleep(1)
			#znizi cas o 1 sekundu
			cas -= 1

pauznute = FALSE

#funkcia na nahranie a spustenie mp3 suboru
def prehraj():
	global pauznute
	#pri prvom spusteni programu pauznute je defaultne FALSE.
	if pauznute:
		mixer.music.unpause()
		pauznute = FALSE
	else:
		try:
			mixer.music.load(subor)
			mixer.music.play()
			#zmeni parameter text v statusbar
			statusbar['text'] = 'Prehravam pesnicku' + ' ' + os.path.basename(subor)
			ukaz_detaily()
		except:
			tkinter.messagebox.showwarning('Oznam', 'Ziaden subor nie je vybrany.')

#zobrazi detaily prehravanej pesnicky, tak ze prepise text v Label detaily

def ukonci():
	mixer.music.stop()
	statusbar['text'] = 'Prehravanie ukoncene'


def pauza():
	#ked sa da pauza tak po spusteni play sa znova zacne prehravat od
	#zaciatku skladby. Preto zadame parameter pauznute
	global pauznute
	pauznute = TRUE
	mixer.music.pause()
	statusbar['text'] = 'Prehravanie pozastavene'

def nastav_hlasitost(vyska):
	#set_volume je hodnota medzi 0 a 1, preto ho treba upravit na nami zobrazene rozpatie 0 az 100
	#vyska je string, je nutne zmenit na int
	vyska_hlasu = int(vyska) / 100
	mixer.music.set_volume(vyska_hlasu)

def o_nas():
	tkinter.messagebox.showinfo('O nas', 'Copyright EDGE CAPITAL')

#nacitanie suboru z pocitaca cez prehliadac
#subor je parameter IBA v ramci danej funkcie. Aby sa mohla volat aj mimo, musi sa dat global
def nacitat_subor():
	global subor
	subor = filedialog.askopenfilename()
	statusbar['text'] = 'Nacitavam subor' 

#muted defaultne na false
muted = FALSE

def mute():
	global muted
	#pokial je muted tak nech urobi unmute
	if muted:
		mixer.music.set_volume(0.7)
		hlasitost.set(70)
		hlasitost_btn.config(image=fotka_unmute)
		muted = FALSE
	#pokial je unmuted tak nech muted
	else:
		mixer.music.set_volume(0) #nastavi zobrazenie na 0
		hlasitost.set(0)	#nastavi hlasitost na 0
		hlasitost_btn.config(image=fotka_mute)
		muted = TRUE

#vytvorenie prazdnej lišty menu
menubar = Menu(hlavne_okno)
#tymto prizom je hlavne menu vzdy na vrchu okna a je pripravene na pripojenie submenu
hlavne_okno.config(menu=menubar)

#vytvorenie sub_menu tj polozky v hlavnom menu
#tearoff=0 znamena ze sa nevykresli prvy ciarkovany oddelovac v submenu
menu_soubor = Menu(menubar, tearoff=0)
#pridanie polozky do hlavneho menu
menubar.add_cascade(label='Soubor', menu=menu_soubor)
#pridanie polozky do submenu
menu_soubor.add_command(label='Otvorit', command=nacitat_subor)
menu_soubor.add_separator()
menu_soubor.add_command(label='Ukoncit', command=hlavne_okno.quit)

menu_help = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help',menu=menu_help)
menu_help.add_cascade(label='O nas', command=o_nas)


#spustenie mixeru
mixer.init()

#tlacitko play
fotka_play =PhotoImage(file='play_btn.png')
play_btn = Button(stredny_frame, image=fotka_play, command=prehraj)
play_btn.grid(row=0, column=0, padx=20)

#tlacitko stop
fotka_stop =PhotoImage(file='stop_btn.png')
stop_btn = Button(stredny_frame, image=fotka_stop, command=ukonci)
stop_btn.grid(row=0, column=1, padx=20, pady=20)

# #tlacitko pauza 
fotka_pause = PhotoImage(file='pause_btn.png')
pause_btn = Button(stredny_frame, image=fotka_pause, command=pauza)
pause_btn.grid(row=0, column=2, padx=20)


#zobrazenie kontroly hlasitosti
hlasitost = Scale(spodny_frame, from_=0, to=100, orient= HORIZONTAL, command=nastav_hlasitost)
#pri spusteni prehravaca sa nastavi defatultne zobrazenie na volume 70 
hlasitost.set(70)
#nastavenie hlasitosti na 0.7 defaultne
mixer.music.set_volume(0.7)
hlasitost.grid(row=0, column=1, columnspan=3, sticky=W+E, padx=20, pady=20)

#ikona pre mute/unmute

fotka_mute = PhotoImage(file='mute.png')
fotka_unmute = PhotoImage(file='unmute.png')
hlasitost_btn = Button(spodny_frame, image=fotka_unmute, command=mute)
hlasitost_btn.grid(row=0, column=0)


def pri_zatvoreni():
	ukonci()
	hlavne_okno.destroy()

#pri kliknuti na X zatvorenie okna sa zavola funkcia ukonci
#pokial hraje hudba a kliklo by sa na X bez zastavenia hudby, tak bude chyba
#main thread is not in main loop
#preto sa najprv musi ukoncit thread (zastavenim prehravania hudby) zavolanim
#funkcie ukonci()
hlavne_okno.protocol('WM_DELETE_WINDOW', pri_zatvoreni)

hlavne_okno.mainloop()

