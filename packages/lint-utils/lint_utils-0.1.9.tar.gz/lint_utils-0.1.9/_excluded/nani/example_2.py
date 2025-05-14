class CumCommand:
    def __init__(self, db_context: str) -> None:
        self._db_context = db_context

    async def execute(self) -> int:
        raise NotImplementedError


class ChildCommand(CumCommand):
    async def execute(self) -> int:
        return 2


class ChildCommand2(CumCommand):
    async def execute(self) -> int:
        return 3


class Command2:
    def __init__(self, db_context: str) -> None:
        self._nani_ctx = db_context

    async def execute(self) -> int:
        return 3


class Command3(Command2):
    async def execute(self) -> int:
        return 3
