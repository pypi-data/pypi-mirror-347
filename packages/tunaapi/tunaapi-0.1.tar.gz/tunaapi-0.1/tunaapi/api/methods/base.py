class TunaMethod:
    @property
    def params(self) -> str:
        prms = '&'.join(
            [f'{k}={v}' for k, v in self.__dict__.items()]
        )
        return '?' + prms if prms else ''
