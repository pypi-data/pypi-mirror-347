class Command4:
    def __init__(self, counter: int, a: int) -> None:
        a = 3
        b = 33
        self._counter = counter
        self._counter_2 = 0
        self._counter_4 = 0
        self._counter_5 = self._counter_4
        self._counter_3 = 0
        self._a = a

    async def execute(self) -> int:
        self._counter += 1
        self._counter_2 += 1
        return 3
