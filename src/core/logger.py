import logging

class LoggerPreparationError(Exception):
    """ロガーが未初期化時のエラー"""

class LoggerHolder:

    _apl = logging.getLogger('applogger')
    _apl_inited: bool = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(LoggerHolder, cls).__new__(cls)
        return cls._instance

    def init_app_logger(self, filename: str):

        self._apl.setLevel(logging.DEBUG)
        _apl_format = logging.Formatter(fmt='%(asctime)s, %(filename)s:%(lineno)d, %(levelname)s, %(message)s')

        _stream_handler = logging.StreamHandler()
        _stream_handler.setFormatter(_apl_format)
        self._apl.addHandler(_stream_handler)

        _file_handler = logging.FileHandler(filename)
        _file_handler.setFormatter(_apl_format)
        self._apl.addHandler(_file_handler)

        self._apl_inited = True
        self.get_apl_logger().info('apl logger inited.')

    def get_apl_logger(self):
        return self._apl


def apllog():
    return LoggerHolder().get_apl_logger()

def init_apl_logger(filename: str):
    LoggerHolder().init_app_logger(filename)