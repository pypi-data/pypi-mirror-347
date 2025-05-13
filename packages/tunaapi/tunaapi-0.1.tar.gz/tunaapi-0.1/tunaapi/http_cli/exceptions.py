class UnexpectedMethodError(Exception):

    def __init__(self, method: str):
        self.method = method

    def __str__(self) -> str:
        return f'Unexpected method value: {self.method}'
