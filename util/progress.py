import datetime
from abc import ABC
from typing import Final, Optional


class StateError(Exception):
    pass


class ProgressState(ABC):
    _progress: 'Progress'

    def __init__(self, progress: 'Progress'):
        self._progress = progress

    def activate(self):
        raise StateError()

    def update(self):
        raise StateError()

    def finish(self, force: bool):
        if force:
            self._progress.set_state(TerminatedState(self._progress))
        else:
            raise StateError()


class InitialState(ProgressState):
    def activate(self):
        self._progress.set_state(ActivateState(self._progress))


class ActivateState(ProgressState):
    def update(self):
        return None

    def finish(self, force: bool):
        self._progress.set_state(TerminatedState(self._progress))


class TerminatedState(ProgressState):
    pass


class Progress:
    _state: ProgressState
    _target: Final[int]
    _value: int
    _start_time: Optional[datetime.datetime] = None

    def __init__(self, *, target: int):
        self._state = InitialState(self)
        self._target = target
        self._value = 0

    def activate(self):
        self._state.activate()
        self._start_time = datetime.datetime.now()

    def update(self, increment: int = 1):
        self._state.update()
        self._value += increment

    def finish(self, force: bool = False):
        self._state.finish(force=force)

    def set_state(self, new_state: ProgressState):
        self._state = new_state

    @property
    def elapsed(self):
        return datetime.datetime.now() - self._start_time
