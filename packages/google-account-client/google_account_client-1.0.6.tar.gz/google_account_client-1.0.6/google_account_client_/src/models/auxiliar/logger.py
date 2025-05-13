import logging

class Logger:
    def setup_logger(self, name: str, enable_logs: bool) -> None:
        self.enable_logs = enable_logs
        self._name = name

        # Setup do logger
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)  # <-- Essencial pra exibir logs de todos os níveis

        # Evita múltiplos handlers se setup_logger for chamado mais de uma vez
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def log(self, msg: str, level: str = "info"):
        if not self.enable_logs:
            return

        if level != 'debug':
            msg = f"({self._name}) {msg}"

        level = level.lower()

        if level == "info":
            self._logger.info(msg)
        elif level == "debug":
            self._logger.debug(msg)
        elif level == "warning":
            self._logger.warning(msg)
        elif level == "error":
            self._logger.error(msg)
        else:
            self._logger.info(msg)