# ****
# Mathematical functions
# ****



def subtraction(value_a, value_b):
    sub_a = int(value_a)
    sub_b = int(value_b)
    value_s = str(sub_a - sub_b)  # Convert to str to keep the type in the holder list the same
    # print(value_s)
    return value_s


def addition(value_a, value_b):
    add_a = int(value_a)
    add_b = int(value_b)
    value_a = str(add_a + add_b)
    # print(value_a)
    return value_a


def multiplication(value_a, value_b):
    mult_a = int(value_a)
    mult_b = int(value_b)
    value_m = str(mult_a * mult_b)
    # print(value_m)
    return value_m


def division(value_a, value_b):
    div_a = int(value_a)
    div_b = int(value_b)
    value_d = str(div_a / div_b)
    # print(value_d)
    return value_d