
texty = ['''
Situated about 10 miles west of Kemmerer, 
Fossil Butte is a ruggedly impressive 
topographic feature that rises sharply 
some 1000 feet above Twin Creek Valley 
to an elevation of more than 7500 feet 
above sea level. The butte is located just 
north of US 30N and the Union Pacific Railroad, 
which traverse the valley. ''',

'''At the base of Fossil Butte are the bright 
red, purple, yellow and gray beds of the Wasatch 
Formation. Eroded portions of these horizontal 
beds slope gradually upward from the valley floor 
and steepen abruptly. Overlying them and extending 
to the top of the butte are the much steeper 
buff-to-white beds of the Green River Formation, 
which are about 300 feet thick.''',

'''The monument contains 8198 acres and protects 
a portion of the largest deposit of freshwater fish 
fossils in the world. The richest fossil fish deposits 
are found in multiple limestone layers, which lie some 
100 feet below the top of the butte. The fossils 
represent several varieties of perch, as well as 
other freshwater genera and herring similar to those 
in modern oceans. Other fish such as paddlefish, 
garpike and stingray are also present.'''
]

oddelovac = 50 * '='

#prihlasovacie mena a hesla uzivatelov
uzivatel = {'bob': '123',
			'ann': 'pass123',
			'mike': 'password123',
			'liz': 'pass123'
			}

print(oddelovac)
print('\nVitaj v programe Text Analyzator.\nAby si mohol program pouzit, musis sa prihlasit.')
print(oddelovac)

meno = input('\nPrihlasovacie meno: ')
heslo = input('Heslo: ')

print(oddelovac)

#kontrola, ci zadane meno a heslo patri platnemu uzivatelovi
#ak je neplatna meno alebo heslo, tak sa ukonci program
prihlaseny = True

while prihlaseny:

	if meno in uzivatel and heslo == uzivatel[meno]:
		volba = input('\nSi prihlaseny. Mas na vyber z 3 textov. Zvol 1, 2 alebo 3: ')
		while volba not in ('1', '2', '3'):
			volba = input('\nMusis zvolit 1, 2 alebo 3: ')
	else:
		print('Chybne prihlasovacie udaje! Program sa ukonci.')
		break
	print(oddelovac, '\n')

	#vytiskne zvoleny originalny text
	print('Zvolil si text: \n')
	print(texty[int(volba)-1])
	print(oddelovac, '\n')

	#vybrany cely text rozdeli do listu rozd_podla_medzery na zaklade 
	#medzier v originalnom texte
	rozd_podla_medzery = texty[int(volba)-1].split()

	#v liste rozd_podla_medzery skontroluje polozky spojene '-' napr. ('to-be'),
	#rozdeli ich na slova ('to', 'be') a vsetky slova vlozi do rozd_podla_poml
	rozd_podla_poml = []

	while rozd_podla_medzery:
		slovo = rozd_podla_medzery.pop()
		
		if '-' in slovo:
			nove_slova = slovo.split('-')
			while nove_slova:
				rozd_podla_poml.append(nove_slova.pop())
		else:
			rozd_podla_poml.append(slovo)

	#kontrola a odstranenie ciarky a bodky, ak je sucastnou nejakeho slova
	finalny_text = []

	while rozd_podla_poml:
		slovo = rozd_podla_poml.pop()
		if '.' in slovo or ',' in slovo:
			finalny_text.append(slovo.strip(',.'))
		else:
			finalny_text.append(slovo)

	#celkovy pocet slov v texte
	pocet_slov = len(finalny_text)

	#kontrola poctu slov s velkymi pismenami, prvym velkym pismenom, malymi 
	#pismenami, pocet cisiel a cetnost dlzky slov
	poc_velkymi = 0
	poc_malymi = 0
	poc_zac_velkym = 0
	poc_cisiel = 0
	soucet_cisel = 0
	cetnost_slov = {}

	while finalny_text:

		slovo = finalny_text.pop()

		if slovo.isupper() and slovo.isalpha():
			poc_velkymi = poc_velkymi + 1
		elif slovo.islower() and slovo.isalpha():
			poc_malymi = poc_malymi + 1
		elif slovo.isnumeric():
			poc_cisiel = poc_cisiel +1
			soucet_cisel = soucet_cisel + int(slovo)
		elif slovo.isalpha() and slovo[0].isupper() and slovo[1].islower():
			poc_zac_velkym = poc_zac_velkym + 1

		#kontrola cetnosti dlzky slov
		dlzka = len(slovo)

		if dlzka in cetnost_slov:
			cetnost_slov[dlzka] = cetnost_slov[dlzka] + 1
		else:
			cetnost_slov[dlzka] = 1

	print(f'V texte je {pocet_slov} slov.')
	print(f'Pocet slov velkymi pismenami je {poc_velkymi}.')
	print(f'Pocet slov malymi pismenami je {poc_malymi}.')
	print(f'Pocet cisel je {poc_cisiel}.')
	print(f'Pocet slov zacinajucich velkym pismenom je {poc_zac_velkym}.')

	print(oddelovac, '\n')
	print(f'Soucet cisel je {soucet_cisel}.')
	print(oddelovac, '\n')

	#do listu poradie sa zoradia vzostupne vsekty hodnoty zo slovnika cetnost_slov
	#podla poctu pismen v slove (keys)
	poradie = sorted(cetnost_slov.keys())

	#vypise na obrazovku, kolkokrat sa v texte nachadza slovo s danym poctom znakov
	i = 0

	while i < len(cetnost_slov):
		print(poradie[i], cetnost_slov[poradie[i]]*'*', cetnost_slov[poradie[i]])
		i = i +1

	#ukoncenie programu, ak sa podarilo prihlasit na zaciatku
	prihlaseny = False

input()
