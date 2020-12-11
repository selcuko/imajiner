class AbsentMasterException(Exception):
    def __init__(self, narrative=None):
        self.narrative = narrative
        if self.narrative:
            self.message = f'{self.narrative!r} had no master when save method called.'
        else:
            self.message = f'This instance had no master when save method called.'
        super().__init__(self.message)


class ReadonlyException(Exception):
    def __init__(self, narrative=None):
        self.narrative = narrative
        if self.narrative:
            self.message = f'{self.narrative!r} was read-only when save method called.'
        else:
            self.message = f'This instance was read-only when save method called.'
        super().__init__(self.message)