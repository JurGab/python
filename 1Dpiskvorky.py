
print('Hra 1D piskvorky')
pole = '--------------------'
print(pole)

while True:
	
	print('Hrac1, zadaj poziciu: ')
	Hrac1 = int(input())
	pole = pole[:Hrac1-1] + 'x' + pole[Hrac1:]
	print(pole)
	if 'xxx' in pole:
		print('Vyhral hrac 1.')
		break

	print('Hrac2, zadaj poziciu: ')
	Hrac2 = int(input())
	pole = pole[:Hrac2-1] + 'o' + pole[Hrac2:]
	print(pole)
	if 'ooo' in pole:
		print('Vyhral hrac 2.')
		break
	

konec = input()