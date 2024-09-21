# import logging
# import os.path
# from datetime import datetime
#
# import colorlog
#
# log_colors_config = {
#     'DEBUG': 'white',  # cyan white
#     'INFO': 'green',
#     'WARNING': 'yellow',
#     'ERROR': 'red',
#     'CRITICAL': 'bold_red',
# }
#
# logger = logging.getLogger('ccft.logger')
#
#
# def config_log(debug, application_dir, file_name=None):
#     global logger
#
#     log_dir = os.path.join(application_dir, 'logs')
#
#     if not os.path.isdir(log_dir):
#         os.mkdir(log_dir)
#
#     time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
#     if file_name is None:
#         logfile = f'{log_dir}\\{time}.log'
#     else:
#         logfile = f'{log_dir}\\{time}-{file_name}.log'
#
#     # 输出到控制台
#     console_handler = logging.StreamHandler()
#     # 输出到文件
#     file_handler = logging.FileHandler(filename=logfile, mode='a', encoding='utf8')
#
#     if debug:
#         logger.setLevel(logging.DEBUG)
#         console_handler.setLevel(logging.DEBUG)
#         file_handler.setLevel(logging.DEBUG)
#
#         file_formatter = logging.Formatter(
#             fmt='[%(asctime)s.%(msecs)04d %(levelname)s] %(funcName)s -> line:%(lineno)d : %(message)s',
#             datefmt='%Y-%m-%d  %H:%M:%S'
#         )
#
#         console_formatter = colorlog.ColoredFormatter(
#             fmt='%(log_color)s[%(asctime)s.%(msecs)04d %(levelname)s] %(funcName)s -> line:%(lineno)d : %(message)s',
#             datefmt='%Y-%m-%d  %H:%M:%S',
#             log_colors=log_colors_config
#         )
#     else:
#         logger.setLevel(logging.INFO)
#         console_handler.setLevel(logging.INFO)
#         file_handler.setLevel(logging.INFO)
#
#         file_formatter = logging.Formatter(
#             fmt='[%(asctime)s.%(msecs)03d %(levelname)s] %(message)s',
#             datefmt='%Y-%m-%d  %H:%M:%S'
#         )
#
#         console_formatter = colorlog.ColoredFormatter(
#             fmt='%(log_color)s[%(asctime)s.%(msecs)03d %(levelname)s] %(message)s',
#             datefmt='%Y-%m-%d  %H:%M:%S',
#             log_colors=log_colors_config
#         )
#
#     console_handler.setFormatter(console_formatter)
#     file_handler.setFormatter(file_formatter)
#
#     if not logger.handlers:
#         logger.addHandler(console_handler)
#         logger.addHandler(file_handler)
#
#     console_handler.close()
#     file_handler.close()
#     pass
