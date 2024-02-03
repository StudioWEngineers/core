class _Int:
    """
    """
    def __init__(self, value: int) -> None:
        """
        """
        if not isinstance(value, int):
            raise RuntimeError

        self._val = value
        self._type = int

    def get_item(self) -> int:
        """
        """
        return self._val

    def set_item(self, new_value: int) -> None:
        """
        """
        if isinstance(new_value, int):
            self._val = new_value

        raise RuntimeError
