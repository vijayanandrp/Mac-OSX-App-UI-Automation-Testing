import os
import pprint
from logger import Logger
from config import crash_path, user_crash_path


class OsUtils(object):
	""" This class contains os based operations and functions """
	def __init__(self):
		self.logger = Logger.defaults(name="os_utils", output_stream=False)

	def check_if_file_exist(self, file_name=None):
		"""  Function verifies whether the file located in a given path or not """

		if not file_name:
			self.logger.warning("file_name is empty")
			return False

		if os.path.isfile(file_name):
			self.logger.info("file found - %s " % file_name)
			return True
		else:
			self.logger.info("file not found - %s " % file_name)
			return False

	def fetch_files_from_path(self, path=None):
		"""  Fetches the list of files available in current given path """
		if not path:
			self.logger.info('Path cannot be None')
			return False

		if not os.path.isdir(path):
			self.logger.info('Path is not valid')
			return False

		for path, dirs, files in os.walk(path):
			return files

	def check_crashes(self, app_name="crash"):
		""" Function that looks for crashes for specified app """
		crashes = []
		for path in [crash_path, user_crash_path]:
			files = self.fetch_files_from_path(path)
			crash = [fn for fn in files if ".crash" in fn.lower()]
			crashes += crash

		self.logger.debug("crash files - %s " % pprint.pformat(crashes, indent=1))
		crashes = [fn for fn in crashes if app_name.lower() in fn.lower()]
		self.logger.info("App crash files - %s " % pprint.pformat(crashes, indent=1))

		if not len(crashes):
			return None
		else:
			return crashes

