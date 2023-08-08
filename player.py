import requests
import re
base_url = 'https://pds-nerdle-b475e73d0e76.herokuapp.com'

def load_possible_equations():
	file=open('options/5.txt')
	options = [line.strip() for line in file]
	return options
#lo que tengo que hacer es verificar 
def remove_bads(options,info,play):
	dic = {'2':set(),'1':set(),'0':set()}
	new_options = []
	for i in range(len(info)):
			if info[i] == '0':
				dic[info[i]].add(play[i])
			else:
				dic[info[i]].add((play[i],i))
	
	if len(dic['2'])>0:
		accepted = [x[0] for x in dic['2']]
		for e in accepted:
			if e in dic['0']:
				options.pop(options.index(play))
				dic['0'].remove(e)
				
	for eq in options:
		not_in_eq = True
		not_same_pos_1= True
		fixed_number = True
		for key in dic:
			if key=='0':

				#Si estan no las quiero
				for e in dic[key]:
					if e in eq:
						not_in_eq = False
			elif key == '1':
				for ch,pos in dic[key]:
					if eq[pos] ==ch:
						not_same_pos_1 = False
			elif key=='2':
				for ch,pos in dic[key]:
					if eq[pos] != ch:
						fixed_number = False
		if not_in_eq and not_same_pos_1 and fixed_number:
			new_options.append(eq)
		else:
			continue

	return new_options








# # Obtener juegos activos
# response = requests.get(f'{base_url}/api/games/')
# games = response.json()['games']
# games_len_5 = []

# for dic in games:
# 	if dic['eq_length'] == 5:
# 		games_len_5.append(dic['id'])

# for g in games_len_5: #lista con los dics de cada juego
#   print(g)

options = load_possible_equations()

player_key = 'MUNO206'
game = 1
equality = '1+2=3'
data = {
    'game': game,
    'key': player_key,
    'equality': equality
}
r = requests.post(f'{base_url}/api/play/', data=data)
r = r.json()
#{'result': ['00200'], 'equalities_state': [False], 'finished': False}
i=1

while(not r['finished']):
	print(r)
	options = remove_bads(options,r['result'][0],equality)
	print(f"posibles opciones: {len(options)}")
	for x in options:
		print(x)
	print(f"Recomendamos probar con: {options[0]}")
	equality = input('>>> ')
	data = {
    'game': game,
    'key': player_key,
    'equality': equality
	}
	r = requests.post(f'{base_url}/api/play/', data=data)
	r = r.json()
	i+=1

print(f"Respuesta: {equality}")
print(f"intentos: {i}")

data = {
    'game': game,
    'key': player_key
}
r = requests.post(f'{base_url}/api/reset/', data=data)
print("borrado")



 # my key:MUNO206
# for finding where is the equal >>> re.search("is", String).start()