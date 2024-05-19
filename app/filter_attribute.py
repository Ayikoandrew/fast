import logging

class BcryptWarningFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "module 'bcrypt' has n attribute __about__" not in record.msg
    