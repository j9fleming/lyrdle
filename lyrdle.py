import requests
import unidecode
import re
import getpass
import random
import sys
import time
from player import Player


root = "https://api.musixmatch.com/ws/1.1/"
api_key = "5c1a408fed27fd96854811499be84b73"
DEEZ_URL = "https://api.deezer.com/"

#game_settings
players = list()

#getting name and number of players
def set_up_players():
	#getting number of players
	while True:
		try:
			numplayers = int(input("How many players? (1 - 5): "))
		except:
			print("Please input a valid number between 1 and 5.")
			pass
		else:
			if numplayers > 0 and numplayers < 6:
				break
			else:
				print("Please input a valid number between 1 and 5.")

	#getting player names
	for i in range(1,numplayers+1):
		while(True):
			username = input(f"Player {i}, enter your name: ")
			if len(username) <= 0:
				print("Please enter at least one character.")
			else:
				break
		
		if i == 1:
			p1 = Player(username)
			players.append(p1)
		elif i == 2:
			p2 = Player(username)
			players.append(p2)
		elif i == 3:
			p3 = Player(username)
			players.append(p3)
		elif i == 4:
			p4 = Player(username)
			players.append(p4)
		elif i == 5:
			p5 = Player(username)
			players.append(p5)
		else:
			break

def create_song_list(artist_id):
	url = f"{DEEZ_URL}artist/{artist_id}/albums"
	r = requests.get(url).json()
	album_ids = []
	song_titles = set()
	for album in r['data']:
		album_ids.append(album['id'])
	for a_id in album_ids:
		url = f"{DEEZ_URL}album/{a_id}/tracks"
		r = requests.get(url).json()
		for track in r['data']:
			title_parts = track['title'].split("(")
			title = title_parts[0]
			song_titles.add(title)
	return song_titles

def get_lyrics(artist,track):
	url = f"{root}matcher.lyrics.get?apikey={api_key}&q_track={track}&q_artist={artist}"
	r = requests.get(url).json()
	lyrics_body = r['message']['body']['lyrics']['lyrics_body']
	lyrics = re.split('\n+',lyrics_body)
	i = lyrics.index("...")
	if i == -1:
		i = lyrics.index("******* This Lyrics is NOT for Commercial use *******")
	return lyrics[0:i]

#checks to see if user inputted artist name is valid/exists
def get_artist():
	artist_id = -1
	user_artist = input("Next, type in an artist with a space in between first and last names,\n"
 					   +"or press enter to quit. : ")
	while(True):
		if(user_artist == ""):
			sys.exit()

		url = f"{DEEZ_URL}search/artist?q={user_artist}"
		r = requests.get(url).json()
		if not r['data']:
			user_artist = input("Artist not found. Please input a valid artist name: ")
		else:			
			for i in r['data']:
				artist = unidecode.unidecode(i['name'].lower())
				if artist == unidecode.unidecode(user_artist.lower()):
					print(f"Artist found: {user_artist}")
					return i['id'], user_artist
			user_artist = input("Artist not found. Please input a valid artist name: ")

def play_game(lyrics, track):
	counter = 0
	num_lines = len(lyrics)
	for i in range(num_lines):
		line = lyrics[i]
		print()
		print("[" + str(counter + 1) + "]" + " " + line)
		print()
		counter += 1
		#asking for guesses
		for p in players:
			p.start()
			#guess = input(f'OK {p.name}, can you guess the song??? ')
			guess = getpass.getpass(f'OK {p.name}, can you guess the song??? ')
			p.stop()
			p.change_answer(guess)
		#checking if anyone got it right
		guessed_right = []
		for p in players:
			right_answer = re.sub(r'[\W_]+', '', track.lower())
			player_guess = re.sub(r'[\W_]+', '', p.answer.lower())
			if (player_guess == right_answer):
				guessed_right.append(p)


		if (len(guessed_right) == 1):
			print()
			print(f"The song was \"{track}\"")
			print(f'Player {guessed_right[0].name} guessed it in {counter} line(s)!!!')
			print(guessed_right[0])
			return True

		elif (len(guessed_right) > 1):
			winner = None
			for i in range(len(guessed_right)):
				if i == 0:
					winner = guessed_right[i]
				else:
					result = winner.compare_times(guessed_right[i])
					if(not result):
						winner = guessed_right[i]
			print()
			print(f"The song was \"{track}\"")
			print(f'Player {winner.name} guessed it in {counter} line(s) with the fastest time!!!')
			print(winner)
			print("Here are all the players that guessed correctly: ")
			for p in guessed_right:
				print(p)
			return True
		else:
			for p in players:
				p.reset()

	print()
	print(f"Oooof, no one guessed it :( The song was \"{track}\"")
	print()
	return False

def main():
	#Welcome message
	print("Welcome to Lyrdle! It's like Wordle, but with lyrics!")
	print("Compete with up to 4 of your friends to guess the song using only the lyrics.")

	#Configure settings
	print("First, let's configure the game settings.")
	set_up_players()
	print()

	#getting the lyrics for a song
	artist_id, input_artist = get_artist()
	song_list = create_song_list(artist_id)
	random_idx = random.randint(0,len(song_list) - 1)
	print("Searching for a song...")
	time.sleep(3)
	counter = 0
	lyrics = None
	track = None
	while(True):
		try:
			lyrics = get_lyrics(input_artist, list(song_list)[random_idx])
			track = list(song_list)[random_idx]
			#print(lyrics)
			#print(list(song_list)[random_idx])
			break
		except:
			print("...")
			random_idx = random.randint(0,len(song_list) - 1)
			time.sleep(1)
			counter += 1
			if counter > 5:
				print("Sorry, we were unable to find any lyrics.\n"
					+ "Would you like to try a different artist?")
				user_input = input("Enter 'y' or 'yes' to continue, or any other key to quit: ")
				user_input = user_input.lower()
				if user_input != 'y' and user_input != 'yes':
					sys.exit()
				else:
					artist_id, input_artist = get_artist()
					song_list = create_song_list(artist_id)
					random_idx = random.randint(0,len(song_list) - 1)
					print("Searching for a song...")
					time.sleep(3)
					counter = 0

	#playing a game
	print("Loaded lyrics. Lyrics will be shown starting from the beginning of the song.")
	time.sleep(3)
	print("Ready?")
	time.sleep(2)
	print("3")
	time.sleep(1)
	print("2")
	time.sleep(1)
	print("1")
	time.sleep(1)
	print("GO!")
	time.sleep(1)
	print()
	play = play_game(lyrics,track)

if __name__ == '__main__':
	main();
