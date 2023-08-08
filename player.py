import requests
import re
base_url = 'https://pds-nerdle-b475e73d0e76.herokuapp.com'
player_key = 'MUNO206'

def send_data(game,key,equality):
	data = {
    'game': game,
    'key': key,
    'equality': equality
   	}
	r = requests.post(f'{base_url}/api/play/', data=data)
	return r.json()

def load_possible_equations(largo):
	if largo==5:
		file=open('options/5.txt')
		options = [line.strip() for line in file]
		return options,"1+2=3","9-5=4"
	
	elif largo==6:
		file=open('options/6.txt')
		options = [line.strip() for line in file]
		return options,"10-4=6","9+8=17"
	elif largo==7:
		file=open('options/7.txt')
		options = [line.strip() for line in file]
		return options,"34-29=5","56-7=49"
	elif largo==8:
		file=open('options/8.txt')
		options = [line.strip() for line in file]
		return options,"12+36=48","11+5-9=7"

def get_games():
	response = requests.get(f'{base_url}/api/games/')
	games = response.json()['games']
	game_len=[x['eq_length'] for x in games if x['eq_count']==1]
	game_id=[x['id'] for x in games if x['eq_count']==1]
	return game_len,game_id

#lo que tengo que hacer es verificar 

def remove_bads(options,info,play,dic):
	new_options = []
	for i in range(len(info)):
				dic[info[i]].add((play[i],i))
	correct = [x[0] for x in dic['2']]
	in_correct = [x[0] for x in dic['0']]
	semi_correct = [x[0] for x in dic['1']]

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
			if not_in_eq and not_same_pos_1 and fixed_number:

				new_options.append(eq)
			else:
				continue

	return new_options


g_lenghts,g_ids=get_games()



for j in range(len(g_lenghts)):
	dic = {'2':set(),'1':set(),'0':set()}

	game = g_ids[j]

	options,equality1,equality2= load_possible_equations(g_lenghts[j])
	r = send_data(game,player_key,equality1)
	print("sended 1")
	options = remove_bads(options,r['result'][0],equality1,dic)
	r = send_data(game,player_key,equality2)
	print("sended 2")

	equality=equality2
	i=2
	print(f"resolviendo: {game}")
	while(not r['finished']):
		options = remove_bads(options,r['result'][0],equality,dic)
		equality = options[0]
		r = send_data(game,player_key,equality)
		i+=1

	print(f"-->Juego: {j+1} resuelto en {i} intentos")
	print(f"Solucion: {equality}")
	data = {
	    'game': game,
	    'key': player_key
	}
	r = requests.post(f'{base_url}/api/reset/', data=data)


print("fin")



 # my key:MUNO206
# for finding where is the equal >>> re.search("is", String).start()