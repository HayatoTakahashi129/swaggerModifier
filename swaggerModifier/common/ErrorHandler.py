import sys


def show_error(message: str):
    print(message)
    print('Failed to Create output swagger file.')
    sys.exit(1)
