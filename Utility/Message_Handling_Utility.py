
def handling(msg):
    return{
        'hello': lambda: hello(),
        'goodbye': lambda: goodbye(),


    }.get(msg, lambda: None)()


def hello():
    print("hello")


def goodbye():
    print("goodbye")


if __name__ == '__main__':  # If run as module, start game
    msg = input("Input:")
    handling(msg)
