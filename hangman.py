#Hangman.py
#Author Christopher Benner
#Date Created 5 Jan 2023
#Create a basic game of hangman that allows one player to enter a word,
#and a second person to guess the word. Also added the possibility to play
#the computer from the list of words already submitted by a player

import os
import random

play_again = 'y'
score = 0
tries = 0
filled_hangman = [
				"|      |",
				"|      O",
				"|     /|\\",
				"|     / \\",
				]
empty_hangman = [
                "--------",
                "|",
                "|",
                "|",
                "|",
                "|",
                "________"]

def get_word():
    """
    Ask the user for a valid word. If the word contains anything other than letters,
    the word is invalid. If the word is valid, it will check to see if that word is
    already in the list of words that have been added. If it has not been added, it is
    added to the list of word and written to words.txt
	
    :return: user generated word
    """
    word = input("Enter a word to guess: ")
    if not word.isalpha():
    	print("Enter a valid word. (quit to exit)")
    	word = get_word()
    elif word.lower() == 'quit':
    	quit()
    word = word.lower()
    #Check to see if the new word is unique. If it is, add it to the list of words to choose from
    
    try:
    	with open('words.txt','r') as words:
    		list_of_words = words.read()
    except FileNotFoundError:
    	list_of_words = []
    with open('words.txt','a') as words:
    	if word not in list_of_words:
    		words.write("\n"+word)

    os.system('cls' if os.name == 'nt' else 'clear')
    return word

#add a computer player option. With each word played add to a file a pull a random one from that file to play
def get_computer_word():
	"""
	Returns a random word from words.txt
	:return: word selected from words.txt
	"""
	try:
	    with open('words.txt','r') as words:
		    list_of_words = words.readlines()
		    word = random.choice(list_of_words)
		    word = word.strip()
	    return word
	except FileNotFoundError:
		print("File not found. PLease add the necessary file or play against another player first.")
		quit()
def guess_word(word):
	"""
	Creates the logic of whether or not a letter guessed by the player is in the word.
	Also looks to see if the user has found the word or if the player has taken too many tries.
	Continues to ask for another letter until one of those two conditions is met
	"""
	global wrong, score
	display()
	player_guess = guess_letter()
	count = 0
	win = 0
	for i, letter in enumerate(word):
		if player_guess == letter:
			letters[i] = letter
			count += 1
	if count == 0:
		print('that letter is wrong')
		wrong_letters.append(player_guess)
		wrong += 1
	
	#Display the status of the hangman
	display()
	#The board is represented by __ for each missing letter. Check to see if all letters have been found
	if '__' not in letters:
		print('Congratulations, you found the word')
		score += 1
	#The player gets four wrong guesses before the game is over
	elif wrong == 4:
		print("You have lost")
		print(f"The correct answer is: {word}")
	else:
	    guess_word(word)
	


def guess_letter():
	"""
	Returns a user input letter if the letter is valid.
	Prompts the user for a letter, and checks to verify that the letter is a valid guess.
	Problems come from having non-alpha characters, having the wrong number of letters, or guessing a previously guessed letter
	:return: user guess
	"""
	guess = input('Enter a letter to guess: ')
	if not guess.isalpha() or len(guess) != 1:
		print("Enter a single letter to guess")
		return guess_letter()
	guess = guess.lower()
	if guess in guessed_letters:
		print("You have already guessed that letter")
		guess = guess_letter()
	else:
		guessed_letters.append(guess)
	return guess

def display():
	"""
	The game board of the hangman game. This is updated with the number of wrong guesses to draw the hangman.
	"""
	os.system('cls' if os.name == 'nt' else 'clear')
	wrong_remaining = wrong
	for index, line in enumerate(empty_hangman):
		if index < 1:
			print(line)
		elif index >= 1 and wrong_remaining > 0:
			print(filled_hangman[index-1])
			wrong_remaining -= 1
		else:
			print(line)
	board = " ".join(letters)
	print(f'\nHere is the current board: {board}')
	print(f'Wrong letters: {wrong_letters}')


while(play_again[0].lower()=='y' ):
	os.system('cls' if os.name == 'nt' else 'clear')
	game_choice = input("Do you want to play the computer? y/n ")
	if game_choice[0].lower() == 'y':
		word = get_computer_word()
	else:
		word = get_word()
	wrong_letters = []
	wrong = 0
	letters = []
	guessed_letters = []
	for letter in word:
		letters.append('__')
	guess_word(word)
	tries += 1
	print(f"You have won {score} time(s) of {tries} attempt(s)")
	play_again = input("Do you want to play again? y/n ")

print("Thank you for playing. Goodbye!")