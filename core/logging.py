from django.conf import settings
from django.utils.timezone import now
from pythonjsonlogger import jsonlogger


class ELKJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(ELKJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['log_time'] = now()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {'json': {'()': 'core.logging.ELKJsonFormatter'}},
    "handlers": {
        "console": {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json',
        },
    },
    "root": {
        "handlers": ["console"],
        "level": 'DEBUG' if settings.DEBUG else 'INFO',
    },
}
