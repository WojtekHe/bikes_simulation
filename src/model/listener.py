import abc


class OnTimeChangeListener(abc.ABC):

    @abc.abstractmethod
    def on_time_change(self, time: int) -> bool:
        raise NotImplemented()
