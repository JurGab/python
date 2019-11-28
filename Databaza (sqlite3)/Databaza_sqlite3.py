#pre databazy knihovna sqlite3. vhodne pre male projekty
import sqlite3
from tkinter import *

hlavne_okno = Tk()
hlavne_okno.geometry('400x400')

def vymazanie_formulara():
	#funkcia vymaze text zadany v bunkach meno, priezvisko a vek
	meno.delete(0, END)
	priezvisko.delete(0, END)
	vek.delete(0, END)

def odoslanie_formulara():
	#musi sa znova nadviazat spojenie
	spojenie = sqlite3.connect('zoznam.db')
	#musi sa znova vytvorit kurzor
	kurzor = spojenie.cursor()

	#zapis do tabulky databazy
	kurzor.execute('INSERT INTO zoznam VALUES (:meno, :priezvisko, :vek)',
		#vytvori sa slovnik s KEYS a VALUES
		{
		'meno' : meno.get(),
		'priezvisko' : priezvisko.get(),
		'vek' : vek.get()
		})
	#po odoslani zmaze obsah vstupnych poli
	meno.delete(0, END)
	priezvisko.delete(0, END)
	vek.delete(0, END)

	#musi sa znova potvrdit commit
	spojenie.commit()
	spojenie.close()


#funkcia na vypis zoznamu z databazy
def vypis_databazy():
	#musi sa znova nadviazat spojenie
	spojenie = sqlite3.connect('zoznam.db')
	#musi sa znova vytvorit kurzor
	kurzor = spojenie.cursor()

	#select * zobrazi vsetky polozky v db
	#oid asi original id. Kazdy zaznam ma svoj originalne ID a
	#preto je mozne ho napr lahko zmazat na zaklade tohoto ID
	kurzor.execute('SELECT *, oid FROM zoznam')
	obsah = kurzor.fetchall() #vrati vsetky zaznamy
	print(obsah)
	# kurzor.fetchone() vrati 1 zaznam
	# kurzor.fetchmany(50) vrati 50 zaznamov



	#musi sa znova potvrdit commit
	spojenie.commit()
	spojenie.close()


#vytvorenie databazy alebo sa pripojit k nejakej. Pokial
#dbaza neexistuje tak ju vytvori
spojenie = sqlite3.connect('zoznam.db')

#cursor sa pouziva na komunikaciu s databazou
#vytvorenie kurzoru
kurzor = spojenie.cursor()

# databaza funguje ako excel tabulka, riadky a stlpce
# vytvorenie tabulky. Davaju sa 6 uvodzoviek, aby sa nemusel vypisovat
#TATO CAST SA SPUSTA IBA RAZ, ABY SA VYTVORILA DATABAZA. POTOM UZ SA PRI KAZDOM SPUSTENI PRACUJE S VYTVORENOU DATABAZOU
# dlhy riadok a tabulka bola prehladnejsia
# datove typy text, integer, real, null, "blob" video, image files
'''
kurzor.execute("""CREATE TABLE zoznam(
	meno text,
	priezvisko text,
	vek integer
	)
	""")
'''
# vytvorenie vstupu pre zadavanie novych udajov
meno = Entry(hlavne_okno, width=30)
meno.grid(row=0, column=1, padx=20)
priezvisko = Entry(hlavne_okno, width=30)
priezvisko.grid(row=1, column=1, padx=20)
vek = Entry(hlavne_okno, width=30)
vek.grid(row=2, column=1, padx=20)
#vytvorenie nazvov pre vstupy
meno_popis = Label(hlavne_okno, text='Meno')
meno_popis.grid(row=0, column=0, sticky=W)
priezvisko_popis = Label(hlavne_okno, text='Priezvisko')
priezvisko_popis.grid(row=1, column=0, sticky=W)
vek_popis = Label(hlavne_okno, text='Vek')
vek_popis.grid(row=2, column=0, sticky=W)

#vytvorenie tlacitka s funkciou na odoslanie/zmazanie vytvoreneho zaznamu
#padx, pady posunie o danu velkost v smere x, y
#ipadx, ipady roztiahne dany widget o zadanu velkost
vymazat = Button(hlavne_okno, text='Zmazat zaznam', command=vymazanie_formulara)
vymazat.grid(row=3, column=1, pady=50, ipadx=40)
odoslat = Button(hlavne_okno, text='Odoslat zaznam', command=odoslanie_formulara)
odoslat.grid(row=4, column=1, pady=50, ipadx=20)

#vytvorenie tlacitka na vypis zoznamu z databazy
dotaz = Button(hlavne_okno, text='Vypis databazu', command=vypis_databazy)
dotaz.grid(row=5, column=1)




#na vykonanie zmien v dbaze sa pouziva prikaz commit
spojenie.commit()




#ukoncenie spojenia s databazou. Pri ukonceni programu sa automaticky
#ukonci aj spojenie
spojenie.close()

hlavne_okno.mainloop()

