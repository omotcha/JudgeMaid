
class MarkdownUtil:
    def __init__(self, target: str or None):
        """

        :param target: markdown string
        """
        if target:
            self._target = target
        else:
            self._target = ""

    def retarget(self, target: str or None):
        """

        :param target: markdown string
        :return:
        """
        if target:
            self._target = target
        else:
            self._target = ""

    def get(self) -> str:
        return self._target

    def add_header(self, header: str or None) -> str:
        """

        :param header: normal header string
        :return:
        """
        if not header:
            header = "基本信息"
        self._target = f"""## {header}

        """ + self._target
        return self._target
