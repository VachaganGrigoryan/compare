import json
from typing import Any


class Compare:
    DIFF = []

    def __init__(self, expected: Any, actual: Any, esc_fields: list = None, path: list = None):
        self.expected = expected
        self.actual = actual
        self.esc_fields = esc_fields
        self._path: list = path or ['$']

    @property
    def path(self):
        return '.'.join(self._path)

    def __process__diff(self):
        if not self.c_type():
            self.DIFF.append({
                    'path': self.path,
                    'message': f'Not Equal Type.',
                    'expected': self.expected,
                    'actual': self.actual
            })
        elif isinstance(self.expected, list):
            self.c_list()
        elif isinstance(self.expected, dict):
            self.c_dict()
        elif self.expected != self.actual:
            self.DIFF.append({
                    'path': self.path,
                    'message': f'Not Equal Value.',
                    'expected': self.expected,

                    'actual': self.actual
            })

    def compare(self) -> list:
        self.__process__diff()
        return self.DIFF

    def c_type(self) -> bool:
        return self.actual.__class__ == self.expected.__class__

    def c_len(self):
        return len(self.expected) == len(self.actual)

    def c_dict_key(self):
        return sorted(self.expected.keys()) == sorted(self.actual.keys())

    def c_list(self):
        if not self.c_len():
            self.DIFF.append({
                    'path': self.path,
                    'message': f'Not Equal length.',
                    'expected': self.expected,
                    'actual': self.actual
            })
        else:
            for i, (expected, actual) in enumerate(zip(self.expected, self.actual)):
                Compare(expected, actual, path=self._path+[f'[{i}]']).compare()

    def c_dict(self):
        if not self.c_dict_key():
            self.DIFF.append({
                    'path': self.path,
                    'message': f'Not Equal Dict Keys.',
                    'expected': tuple(self.expected.keys()),
                    'actual': tuple(self.actual.keys())
            })
        else:
            for key in self.expected.keys():
                Compare(self.expected.get(key), self.actual.get(key), path=self._path+[key]).compare()

    def __str__(self):
        return f'{self.DIFF}'


if __name__ == '__main__':
    exp = [65, {"foo": "bar", "john": "doe"}]
    act = [True, {"john": "doe", "foo": "bar", 'e': 54}]

    diff = Compare(exp, act)
    diff.compare()
    print(json.dumps(diff.DIFF, indent=4))
