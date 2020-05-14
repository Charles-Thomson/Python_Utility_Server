# ****
# Imports
# ****


from random_word import RandomWords
import re


class HangMan:
    def __init__(self):
        global word
        global hidden_word
        word = ''
        hidden_word = ''

        generate_word()  # Generate a word
        hide_word(word)  # Hide the generated word using *

        print(f'[SYSTEM]word :  {word} , Hidden_word : {hidden_word}')

        start_guessing()


# Generate a random word
def generate_word():
    global word
    r = RandomWords()
    word = r.get_random_word()


# "Hide" the word
def hide_word(word):
    global hidden_word
    hidden_word = re.sub('[a-z A-Z]', '*', word)  # regex change each letter to *


# Use a find() in an if followed by a replacement in the hidden_word
def start_guessing():
    global word
    global hidden_word
    word_found = False
    max_attempts = 5
    number_of_attempts = 0
    print(f'The maximum number of attempts is {max_attempts}')
    user_guess = input('Start Guessing:   ')

    while not word_found:
        guess_location = word.find(user_guess)  # Guess location is if the guess is in the word as location

        if number_of_attempts == max_attempts:  # If the user takes more then the max number of attempts
            print(f'[LOSE] You have taken to may attempts. The word was - {word}')
            break

        elif '*' not in hidden_word:  # If * is not in hidden word all letters have been found
            print(f'[WIN] You have found all the letters in the word - {word}')
            break

        elif guess_location == -1:  # If the letter is not in the word
            number_of_attempts += 1
            print(f'{user_guess} not in the word. Number of attempts = {number_of_attempts}/{max_attempts}')


        else:
            for guess in re.finditer(user_guess, word):   # For each occurrence of the user_guess in the word
                # print(f'{user_guess} found at location {guess.start()}')  # user_guess found at location - debug
                replacement_letter = word[guess.start()]  # Get the letter at the location in word
                hidden_word = hidden_word[:guess.start()] + replacement_letter + hidden_word[guess.start()+1:]  # Enter the letter into the hidden_word
                print(f'[LETTER FOUND] {user_guess} is in the word')
                # print(replacement_letter)  # - debug

        print(f'Word - {hidden_word}')  # Return the updated hidden word
        user_guess = input("Take a guess :  ")  # The user given guess

    print('[SYSTEM] Game Finished')

    play_again = input('\nPlay again ? (y/n) :  ')  # Offer to play again

    if play_again == "y":
        HangMan()

    elif play_again == "n":
        print('Sore loser')


if __name__ == '__main__':  # If run as module, start game
    HangMan()



