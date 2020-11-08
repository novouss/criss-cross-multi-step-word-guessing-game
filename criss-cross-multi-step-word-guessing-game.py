import os
import random

word = ""  # A string representing the word being guessed by the player.
word_length = 0 # An integer representing the length of the word being guessed by the player. 
guess_no = 1 # An integer representing how many guesses the player has made.

board = []
scores = [] # Records score.

# The guess slices will depend on.

# First Index: Word length
# Second Index: Slices
# Third Index: Slice indexes

guess_index_tuple = (
	((0,1), (1,2), (0,2)), # Word lengths of 3
	((0,1), (2,3), (1,2), (0,3)), # Word lengths of 4
	((0,1), (1,3), (3,4), (2,4), (0,4)), # Word lengths of 5
	((0,1), (1,3), (4,5), (1,2), (2,5), (0,5)), #Word lenghts of 6
	((2,3), (0,2), (4,6), (5,6), (3,4), (3,6), (0,6)), # Word lenghts of 7
	((0,1), (1,3), (4,7), (3,5), (3,6), (5,7), (2,7), (0,7)) # Word lengths of 8
) 




def word_select(difficulty): 

	# A string representing a FIXED or ARBITRARY word selection. 

	global word
	global word_length
	global guess_index_tuple

	filename = 'FIXED' if difficulty == 'f' else 'ARBITRARY'

	with open(f'LEVELS/{filename}.txt', 'r') as file:
		content = file.readlines()
		word = random.choice(content)
	
	word = word[:-1]
	word_length = len(word)

def user_guess(substring, user, scores): 

	# Calculates user score

	# This is the stuipdest part of this code hahahhaha
	vowel = ['a', 'e', 'i', 'o', 'u'] 
	consonant = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

	score = 0 # Calculates score.


	# print(substring + " " + user)

	if len(substring) != len(user): # if user inputs a guess that's less than the substring
		return False

	for index, letter in enumerate(user):

		# Each letter guessed correctly but in the wrong position within the substring gets 5 points. 
		if (letter in substring) and (letter in vowel or letter in consonant):
			score += 5

		# Letter guessed is in the correct position.
		if user[index] == substring[index]:
			
			# Each vowel guessed in the correct position gets 14 points. 
			if letter in vowel:
				score += 14

			# Each consonant guessed in the correct position gets 12 points. 
			if letter in consonant:
				score += 12

	scores.append(score) # Saves score for totaling.
	return True

def create_display(board, word_length):
	
	# Creates the following display on the top portion of the board depending on word_length
	#        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | <------------- This
	# Guess 0| - | - | - | - | - | - | - | - | <---- create_guess_line() 

	display = "       "

	for i in range(1, word_length + 1):
		display += f'| {str(i)} '

	display += '|'
	board.append(display)

def create_guess_line(guess_no, guess_index_tuple, board, word, word_length):

	display = f'Guess {guess_no + 1}'

	min = guess_index_tuple[0]
	max = guess_index_tuple[1]

	for i in range(word_length):

		display += f'| * ' if min <= i <= max else f'| - ' 

	display += '|'
	board.append(display)

	# When user reaches his/her final guess
	if guess_no + 1 == word_length:
		final_answer(board, word)
		return

	while True:
		display_board(board)

		if user_guess(word[min:max + 1], input(f'Now enter Guess {guess_no + 1}: '), scores):
			break

	board[guess_no + 1] += F'   {scores[guess_no]} Points'



def display_board(board):

	for i in board:
		print(i + '\n' + ('-' * (len(board[0]) + 3)))



def final_answer(board, word):

	user = ""
	display_board(board)

	while len(user) != len(word):
		user = input(f'Now enter your final guess. i.e. guess the whole word: ')

	if user == word:
		print('You have guessed the word correctly. Congratulations!')
	else:
		print(f'Your guess was wrong. The correct word was {word}')



if __name__ == "__main__":
	# START OF PROGRAM
	print("DIFFICULTIES\nF - FIXED\nA - Arbitrary")
	word_select(input('Enter difficulty: ').upper())
	create_display(board, word_length)

	# print(word) # For troubleshooting scoring

	# Finds proper sequence of splices depending on word length
	for index in range(len(guess_index_tuple)):

		if len(word) == len(guess_index_tuple[index]):
			guess_index_tuple = guess_index_tuple[index]

	# Mind of game
	for guess_no in range(word_length):

		create_guess_line(guess_no, guess_index_tuple[guess_no], board, word, word_length)