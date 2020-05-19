from Utility.Polish_Notation import Polish_Notation_Calculator as Polish_Notation
from Utility.Hang_Man import Hang_Man_Game as Hang_Man


# Run the Suffix Calculator
def run_suffix_calculator(msg):
    msg = msg.replace('[SUFFIX_CALCULATOR]', '')

    user_input = msg  # Name change for consistency in computation module

    calculator_obj = Polish_Notation.start_computation(user_input)  # Make a new computation object and pass the user_input

    result = str(calculator_obj.global_result)  # result pulled from a global var in the computation object and converted to string to allow for encoding

    return result


# Create the hang man game object and pass the initial info to the user
def create_hang_man_object():
    hang_man_obj = Hang_Man
    hang_man_obj.HangMan()

    return hang_man_obj


def initial_hang_man_details(hang_man_obj):
    hidden_word = hang_man_obj.hidden_word
    max_attempts = hang_man_obj.max_attempts
    word = hang_man_obj.word

    return hidden_word + "//" + str(max_attempts) + "//" + word


def run_hang_man(msg, hang_man_obj):
    msg = msg.replace('[HANG_MAN]', '')
    word = hang_man_obj.word
    hidden_word = hang_man_obj.hidden_word
    max_attempts = hang_man_obj.max_attempts

    print(f'[RUN_GAME] The word is: {word}  The hidden word is: {hidden_word}  \nMax guesses is {max_attempts}')

    user_guess = msg

    hang_man_obj.make_guess(user_guess)

    word = hang_man_obj.word
    hidden_word = hang_man_obj.hidden_word
    player_attempts = hang_man_obj.player_attempts
    game_completion_state = hang_man_obj.game_completion_state


    return hidden_word + "//" + str(player_attempts) + "//" + game_completion_state




