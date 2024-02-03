class _Bool:
    """
    """
    def __init__(self, value: bool) -> None:
        """
        """
        if not isinstance(value, bool):
            raise RuntimeError

        self._val = value
        self._type = bool

    def get_item(self) -> bool:
        """
        """
        return self._val

    def set_item(self, new_value: bool) -> None:
        """
        """
        if isinstance(new_value, bool):
            self._val = new_value

        raise RuntimeError
