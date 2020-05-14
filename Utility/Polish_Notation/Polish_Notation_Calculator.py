# ****
# Imports
# ****

from string import digits
from Utility.Polish_Notation import Polish_Notation_Maths_Functions as myMath

# ****
# Const
# ****
VALID_OPERATORS = " x-/+"
INPUT_ERROR_MSG = '[INPUT_ERROR]'


class start_computation:
    def __init__(self, user_input):
        # Globals
        global STACK
        global USER_INPUT
        global global_result

        STACK = []
        USER_INPUT = []
        global_result = ''

        # need to use 'self.' to create for each object as apposed to one for all objects
        self.STACK = STACK
        self.USER_INPUT = USER_INPUT

        convert_to_list(user_input)
        check_input_validity(user_input)
        if global_result == '':
            computation()

        # At the end, i'm not sure why but it works here
        self.global_result = global_result


# convert the user input to a list/stack
def convert_to_list(user_input):
    global USER_INPUT  # Global var is declared in each method where it is used
    USER_INPUT = user_input.split()  # Creating the list/stack
    # print("Stack length : ")
    # print(len(USER_INPUT))  # Print for debug


# Being handled in this class as the check is being based on the USER_INPUT list
# Check the input in valid - only digits and valid operators
def check_input_validity(user_input):

    global global_result

    validSet = set(digits).union(VALID_OPERATORS)  # set = all ints and valid operators
    digit_set = set(digits)  # All digits

    # Check to see if any items contain int and operator
    if all(c in digit_set and VALID_OPERATORS for c in USER_INPUT):
        global_result = INPUT_ERROR_MSG
        # print(f'{global_result} : is the returned error ')

    elif all(c in validSet for c in user_input) and (len(USER_INPUT) > 2) and (len(USER_INPUT) % 2 != 0):
        user_input_values = sum(c.isdigit() for c in USER_INPUT)  # Number of ints in the list
        user_input_operators = len(USER_INPUT) - user_input_values  # Number of operators in the list
        # print(f'values = {user_input_values}  operators = {user_input_operators}')

        if user_input_values == user_input_operators + 1:
            print("Input elements are valid and length is valid")
            pass
        else:
            global_result = INPUT_ERROR_MSG

    else:
        global_result = INPUT_ERROR_MSG  # If the input is invalid set the global_result to error
        print(f'{global_result} : is the returned error')


# Carry out computation on the stack
def computation():
    # print(len(USER_INPUT))
    while len(USER_INPUT) > 0:  # While there are more elements in HOLDER
        pop_a = USER_INPUT.pop()
        # print(f'First pop :   {pop_a}')

        if pop_a.isdigit():  # If the element is an int add it to the stack
            STACK.append(pop_a)

        if pop_a in VALID_OPERATORS:  # If the elements is an operator, pop the last two elements from the stack and carry out computation
            operator = pop_a
            value_a = STACK.pop()
            value_b = STACK.pop()

            switch(operator, value_a, value_b)

    return_result()  # Print the result when the loop breaks


def return_result():
    global global_result
    global_result = ''.join(STACK)  # Convert the stack to string when the loop breaks
    print(f'The in object result is: {global_result}')  # Print the final result
    # global_result_return()


# Call the operation based upon given operator
def switch(operator, value_a, value_b):
    if operator == "x":
        result = myMath.multiplication(value_a, value_b)
        STACK.append(result)

    if operator == "-":
        result = myMath.subtraction(value_a, value_b)
        STACK.append(result)

    if operator == "/":
        result = myMath.division(value_a, value_b)
        STACK.append(result)

    if operator == "+":
        result = myMath.addition(value_a, value_b)
        STACK.append(result)


if __name__ == '__main__':   # If the module is run on it's own, ask for input

    user_input = input('Enter polish notation equation:  ')
    start_computation(user_input)


# Comment to show git change

