import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(process)d %(thread)d [line:%(lineno)d]  %(levelname)s  %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='D:\\python_SRC\\Stock_SRC\\tmpData\\log\\log.txt',
                    filemode='w')

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')