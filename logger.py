import logging

class Logger:
	def __init__(self, log_file, logging_level=logging.INFO):
		logging.basicConfig(filename=log_file, level=eval(logging_level))

	def debug(self, message):
		logging.debug(message)

	def info(self, message):
		logging.info(message)

	def warning(self, message):
		logging.warning(message)

	def error(self, message):
		logging.error(message)

