# ****
# Imports
# ****


from random_word import RandomWords
from Utility import Message_Tags as TAG
import re
import sys


class HangMan:
    def __init__(self):
        global word
        global hidden_word
        global player_attempts
        global max_attempts
        global game_finished
        global game_completion_state

        game_completion_state = ''
        word = ''
        hidden_word = ''
        player_attempts = 0
        max_attempts = 5

        self.word = word
        self.hidden_word = hidden_word
        self.player_attempts = player_attempts
        self.max_attempts = max_attempts
        self.game_completion_state = game_completion_state

        generate_word()  # Generate a word
        hide_word(word)  # Hide the generated word using *


# Generate a random word
def generate_word():
    global word
    r = RandomWords()
    word = r.get_random_word()


# "Hide" the word
def hide_word(word):
    global hidden_word
    hidden_word = re.sub('[a-z A-Z]', '*', word)  # regex change each letter to *


# Called if the game is finished
def finished_game():
    global game_finished
    game_finished = True
    print('[SYSTEM] Game Finished')
    print(f'finished game in game = {game_finished}')


def check_guess(user_guess):
    global word
    global hidden_word
    for guess in re.finditer(user_guess, word):  # For each occurrence of the user_guess in the word
        replacement_letter = word[guess.start()]  # Get the letter at the location in word
        hidden_word = hidden_word[:guess.start()] + replacement_letter + hidden_word[guess.start() + 1:]  # Enter the letter into the hidden_word
        # print(f'[LETTER FOUND] {user_guess} is in the word')


# Use a find() in an if followed by a replacement in the hidden_word
def make_guess(user_guess):
    global word
    global hidden_word
    global max_attempts
    global player_attempts
    global game_completion_state

    print(f'The maximum number of attempts is {max_attempts}')

    guess_location = word.find(user_guess)  # Guess location is if the guess is in the word as location

    if player_attempts == max_attempts:  # If the user takes more then the max number of attempts
        print(f'[LOSE] You have taken to may attempts. The word was - {word}')
        game_completion_state = TAG.GAME_LOSE_MSG

    elif '*' not in hidden_word:  # If * is not in hidden word all letters have been found
        print(f'[WIN] You have found all the letters in the word - {word}')
        game_completion_state = TAG.GAME_WIN_MSG
        # sys.exit("Game finished")

    elif guess_location == -1:  # If the letter is not in the word
        player_attempts += 1
        print(f'{user_guess} not in the word. Number of attempts = {player_attempts}/{max_attempts}')

    else:
        check_guess(user_guess)


if __name__ == '__main__':  # If run as module, start game
    HangMan()



