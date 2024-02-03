class _List:
    """
    """
    def __init__(self, value: list) -> None:
        """
        """
        if not isinstance(value, list):
            raise RuntimeError

        self._val = value
        self._type = list

    def get_item(self) -> list:
        """
        """
        return self._val

    def set_item(self, new_value: list) -> None:
        """
        """
        if isinstance(new_value, list):
            self._val = new_value

        raise RuntimeError
