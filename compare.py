from typing import Any


class Compare:
    DIFF = []

    def __init__(self, expected: Any, actual: Any, esc_fields: list = None):
        self.expected = expected
        self.actual = actual
        self.esc_fields = esc_fields

    def __process__diff(self):
        if not self.check_type():
            pass

    def check(self) -> list:
        self.__process__diff()
        return self.DIFF

    def check_type(self) -> bool:
        return isinstance(self.actual, self.expected.__class__)

    def __str__(self):
        return f'{self.DIFF}'


if __name__ == '__main__':
    exp = None
    act = None

    diff = Compare(exp, act)
    print(diff.check_type())
