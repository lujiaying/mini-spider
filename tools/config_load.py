import ConfigParser


class ConfigLoader:
    """
    Attributes:

    Methods: read(): read conf file
    """
    def __init__(self):
        self._config = ConfigParser.ConfigParser()

    def read(self, file_path):
        """
        Args:
            file_path: string
        Returns:
            ret: int, 0 success, else fail
        """
        ret = self._config.read(file_path)
        if file_path in ret:
            return 0
        else:
            return -1

    def get(self, section, option):
        """
        Args:
            section: string
            option: string
        Returns:
            value: string
        """
        return self._config.get(section, option)

    def get_int(self, section, option):
        """
        Args:
            section: string
            option: string
        Returns:
            value: string
        """
        return self._config.get(section, option)

    def items(self, section):
        """
        Return a list of (name, value) pairs for each option 
        in the given section.
        
        Args:
            section: string
        Returns:
            items: list of (name, value)
        """
        return self._config.items(section)
