import sys

class handler:
    def custom_exception_handler(exc_type, exc_value):
        if "raised by my code" in str(exc_value):
            print("Exception:", exc_value)
        else:
            # Ignore other exceptions
            pass

    def __init__(self) -> None:
        sys.excepthook = self.custom_handler