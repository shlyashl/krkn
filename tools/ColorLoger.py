import logging
import colorlog
"""
    Setup the logging environment
"""

log = logging.getLogger('pythonConfig')
log.setLevel(logging.DEBUG)
date_format = '%Y-%m-%d %H:%M:%S'
cformat = ' %(log_color)s %(asctime)s\t%(levelname)s\t%(funcName)30s%(lineno)4d\t%(message)s'
colors = {'DEBUG': 'green',
          'INFO': 'cyan',
          'WARNING': 'bold_yellow',
          'ERROR': 'bold_red',
          'CRITICAL': 'bold_purple'}
formatter = colorlog.ColoredFormatter(cformat, date_format,
                                      log_colors=colors)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)

# import logging
# from colorlog import ColoredFormatter
#
#
#
#
# # log_format = ' %(log_color)s %(asctime)s\t%(levelname)s\t%(name)s %(funcName)30s%(lineno)4d\t%(message)s'
# log_format = ' %(log_color)s %(asctime)s\t%(levelname)s\t%(funcName)30s%(lineno)4d\t%(message)s'
# log_level = logging.INFO
# logging.root.setLevel(log_level)
#
# formatter = ColoredFormatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
# stream = logging.StreamHandler()
# stream.setLevel(log_level)
# stream.setFormatter(formatter)
# log = logging.getLogger('pythonConfig')
# log.setLevel(log_level)
# log.addHandler(stream)
#
# def logger_config(name=None):
#
#

