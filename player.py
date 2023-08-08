import requests
import re
base_url = 'https://pds-nerdle-b475e73d0e76.herokuapp.com'

def load_possible_equations():
	file=open('options/8.txt')
	options = [line.strip() for line in file]
	return options
#lo que tengo que hacer es verificar 
def remove_bads(options,info,play):
	dic = {'2':set(),'1':set(),'0':set()}
	new_options = []
	for i in range(len(info)):
				dic[info[i]].add((play[i],i))
	correct = [x[0] for x in dic['2']]
	in_correct = [x[0] for x in dic['0']]
	semi_correct = [x[0] for x in dic['1']]

	print(dic)
	# for e in options:
	# 	print(e)
	if len(correct)>1 and len(in_correct)>1:
		for eq in options:
			not_in_eq = True
			not_same_pos_1= True
			not_same_pos_2= True

			fixed_number = True
			for key in dic:
				if key=='0':

					#Si estan no las quiero
					for ch,pos in dic[key]:
						if ch in correct or ch in semi_correct:
							if eq[pos]==ch:
								not_same_pos_2= False

						elif ch in eq:
							not_in_eq = False
				elif key == '1':
					for ch,pos in dic[key]:
						if eq[pos] ==ch:
							not_same_pos_1 = False
				elif key=='2':
					for ch,pos in dic[key]:
						if eq[pos] != ch:
							fixed_number = False
			if not_in_eq and not_same_pos_1 and fixed_number and not_same_pos_2:
				new_options.append(eq)
			else:
				continue
	else:
		for eq in options:
			not_in_eq = True
			not_same_pos_1= True
			fixed_number = True
			for key in dic:
				if key=='0':

					#Si estan no las quiero
					for ch,pos in dic[key]:
						if ch in eq:
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


options = load_possible_equations()

player_key = 'MUNO206'
game = 15
#6 opener 10-4=6
#7 opener 34-29=5
#8 opener 12+36=48
equality = '12+36=48'
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
	options = remove_bads(options,r['result'][0],equality)
	print(f"posibles opciones: {len(options)}")

	print(f"Recomendamos probar con: {options[0]}")
	equality = options[0]
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