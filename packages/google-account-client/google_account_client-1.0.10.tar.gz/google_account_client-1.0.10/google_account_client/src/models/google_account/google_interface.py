class GoogleInterface():
    def __init__(self):
        raise TypeError(f'Class {self.__class__.__name__} cannot be instantiated directly')
    
    def log(self, msg: str, level: str = 'debug', show_name: bool = False):
        if show_name:
            msg = f'({self.name}) {msg}'

        level = level.lower()

        if level == 'info':
            self._logger.info(msg)
        elif level == 'warning':
            self._logger.warning(msg)
        elif level == 'error':
            self._logger.error(msg)
        else:
            self._logger.debug(msg)
            
    def log_newline(self, num_lines: int = 1):
        self._logger.newline(num_lines)