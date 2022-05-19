# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2022/5/17 11:31
# # @Author  : martin.peng
# # @Site    :
# # @File    : handel_logger.py
# import datetime
# import logging
# import os
#
# from Config.global_dict import get_logging_config
# from Model.api import LoggingConfig
# from Runner.test_runner import load_system_yaml
#
#
# class HandelLogger(logging.FileHandler):
#
#     def __init__(self, handler_name, logging_config: LoggingConfig) -> None:
#         # logging.Handler.setLevel(self, logging_config.log_level)
#         # logging.Handler.setFormatter(self, logging_config.log_level)
#         self._name = handler_name
#         self.level = logging_config.log_level
#         self.formatter = logging_config.log_format
#         self.file_path = logging_config.log_file_path + logging_config.log_file_name
#         self.logging_config = logging_config
#         self.encoding = 'UTF-8'
#         logging.FileHandler.__init__(self, filename=self.file_path, encoding='UTF-8')
#         logging.FileHandler.setFormatter(self, fmt=logging_config.log_format)
#
#     def emit(self, record):
#         """
#         emit函数为自定义handler类时必重写的函数，这里可以根据需要对日志消息做一些处理，比如发送日志到服务器
#
#         发出记录(Emit a record)
#         """
#         msg = self.format(record)
#         _filePath = datetime.datetime.now().strftime(self.file_path)
#         _dir = os.path.dirname(_filePath)
#         try:
#             if os.path.exists(_dir) is False:
#                 os.makedirs(_dir)
#         except Exception:
#             print("can not make dirs")
#             print("filepath is " + _filePath)
#             pass
#         try:
#             _fobj = open(_filePath, 'a')
#             _fobj.write(msg)
#             _fobj.write("\n")
#             _fobj.flush()
#             _fobj.close()
#         except Exception:
#             print("can not write to file")
#             print("filepath is " + _filePath)
#             pass
#
#
# if __name__ == '__main__':
#     load_system_yaml()
#     logging.basicConfig()
#     logger = logging.getLogger("logger")
#     logger.setLevel(level=logging.INFO)
#     filehandler = HandelLogger('LoggerHandler', get_logging_config())
#     filehandler.setFormatter(get_logging_config().log_format)
#     logger.addHandler(filehandler)
#     logger.info('log...')
