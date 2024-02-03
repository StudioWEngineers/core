class _Float:
    """
    """
    def __init__(self, value: float) -> None:
        """
        """
        if not isinstance(value, float):
            raise RuntimeError

        self._val = value
        self._type = float

    def get_item(self) -> float:
        """
        """
        return self._val

    def set_item(self, new_value: float) -> None:
        """
        """
        if isinstance(new_value, float):
            self._val = new_value

        raise RuntimeError
