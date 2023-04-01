import sys


def show_error(message: str) -> None:
    """
    show Error message to User.
    :param message: error message to show
    """
    print(message)
    print('Failed to Create output swagger file.')
    sys.exit(1)
