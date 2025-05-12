# v2版本添加了企业微信机器人和飞书机器人
from .v2 import setup_logging as log

def setup_logging(name=None, is_logfile=True, console_level="DEBUG", file_level="DEBUG", log_max_days=7, log_max_size=50):
    return log(name=None, is_logfile=True, console_level="DEBUG", file_level="DEBUG", log_max_days=7, log_max_size=50)
