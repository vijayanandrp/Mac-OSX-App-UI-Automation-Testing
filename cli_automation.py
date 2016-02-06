#!/usr/bin/env python

import os
import sys
import getopt
import json
import importlib
import pprint

# current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# inserting the path in the system path
for path, dirs, files in os.walk(current_dir):
	sys.path.insert(0, path)

from logger import Logger
from utils import OsUtils as os_util
from config import config_path, test_case_xl_path, result_path

log = Logger.defaults("start_automation")

try:
	import openpyxl
	from openpyxl.styles import Font, Style, Color
except ImportError:
	log.error("sudo pip install openpyxl is missing", exc_info=True)
	sys.exit(55)


def __help():
	""" To define the usage of the program """
	log.info("calling help")
	sys.stderr.write("""
			Usage:
			python cli_automation.py -h
			python cli_automation.py --help
			python cli_automation.py -c app_store_ui_test.json
			python cli_automation.py --config app_store_ui_test.json

			Note:
			ui_test_json file should be configured early in the path /data/configurations/
			""")
	sys.exit(77)


def __json_to_dict(config_file):
	""" converts the json file into dictionary object """
	try:
		with open(config_file) as data_file:
			config_data = json.load(data_file)
	except ValueError:
		log.error("decode error", exc_info=True)
		sys.exit()

	log.debug("config_data \n %s" % pprint.pformat(config_data, indent=4))
	return config_data


def __get_config(config_file=None):
	""" module checks for the config file and converts the json to dict """
	config_file = os.path.join(config_path, config_file)

	if not os_util().check_if_file_exist(config_file):
		sys.exit()
	return __json_to_dict(config_file)


def __excel_to_dict(test_xl_file=None):
	""" reads the test_case excel files and store it in dictionary """
	test_xl_file = os.path.join(test_case_xl_path, test_xl_file)

	if not os_util().check_if_file_exist(test_xl_file):
		sys.exit()

	wb = openpyxl.load_workbook(test_xl_file, read_only=True)
	sheet = wb.get_sheet_by_name('Sheet1')
	tc_dict = {}
	total_sheet_row = sheet.get_highest_row()

	for row in range(2, total_sheet_row+1):
		try:
			tc_id = sheet['A' + str(row)].value
			tc_desc = sheet['B' + str(row)].value
			tc_values = dict(tc_desc=str(tc_desc), result='')
		except Exception:
			log.error("decode error", exc_info=True)
			sys.exit()
		try:
			tc_dict[int(tc_id)]=tc_values
		except KeyError:
			log.info("key error, %s, %s" %(tc_id, tc_desc))
			pass

	if len(tc_dict) == 0:
		log.error("testcase file is empty")
		sys.exit()
	else:
		log.debug("Test cases = \n %s" % pprint.pformat(tc_dict, indent=4))

	log.info('copying the test cases excel file to result path ')
	os.system('cp %s %s' % (test_xl_file, result_path))
	return tc_dict


def __dict_to_excel(test_xl_file, tc_dict=None):
	""" write the result in the excel sheet """
	test_xl_file = os.path.join(result_path, test_xl_file)

	if not os_util().check_if_file_exist(test_xl_file):
		sys.exit()

	wb = openpyxl.load_workbook(test_xl_file)
	sheet = wb.get_sheet_by_name('Sheet1')
	total_sheet_row = sheet.get_highest_row()
	arial_font = Font(name='Arial', size=10, italic=False, bold=True, shadow=False)
	style_obj = Style(font=arial_font)
	sheet['C1'].style = style_obj
	sheet['C1'] = "Result"

	def _color_for_result(result):
		if result == 1:
			result_font = Font(name='Arial', size=10, bold=True, shadow=False, color='00003300')
			return Style(font=result_font), 'PASSED'
		elif result == 0:
			result_font = Font(name='Arial', size=10, bold=True, shadow=False, color='00FF0000')
			return Style(font=result_font), 'FAILED'
		else:
			result_font = Font(name='Arial', size=10, bold=True, shadow=False, color='000000FF')
			return Style(font=result_font), 'EXCEPTION'

	for row in range(2, total_sheet_row+1):
		try:
			tc_id = int(sheet['A' + str(row)].value)
			tc_result = _color_for_result(tc_dict[tc_id]['result'])
			sheet['C%s' % str(row)].style = tc_result[0]
			sheet['C%s' % str(row)] = tc_result[1]
		except Exception:
			log.error("decode error", exc_info=True)

	wb.save(test_xl_file)


def __execute_test_cases(config_data, tc_dict):
	""" executes the test case functions in the test case python file """
	tc_py_file = config_data['test_cases']
	if ".py" in tc_py_file:
		tc_py_file = str(tc_py_file).replace(".py", "")

	test_module = importlib.import_module(tc_py_file)
	for tc_id in tc_dict.keys():
		tc_func = 'tc_%s' % str(tc_id)
		tc_func = getattr(test_module, tc_func)
		tc_result = tc_func()

		if tc_result not in [1, 0]:
			tc_result = -1

		tc_dict[tc_id]['result'] = tc_result

	log.debug('Result after execution - \n %s ' % pprint.pformat(tc_dict, indent=4))
	__dict_to_excel(config_data['test_case_xl'], tc_dict)


def __automate_app(config_data=None):
	""" module to execute the test case and save the app"""
	tc_xl_file = config_data['test_case_xl']
	tc_dict = __excel_to_dict(tc_xl_file)
	__execute_test_cases(config_data, tc_dict)


def main(argv):
	log.info('\n'+'*'*80+'\n')
	log.info("Starting main automation script")
	options = None
	try:
		options, args = getopt.getopt(argv, "hc:", ["help", "config="])
	except getopt.GetoptError:
		log.error("options error", exc_info=True)
		__help()

	if not len(options):
		log.error("no input parameter passed")
		__help()

	config_data = None
	for option, arg in options:
		if option in ('-h', '--help'):
			__help()
		elif option in ('-c', '--config'):
			config_data = __get_config(arg)

	if not config_data:
		log.info("config_data is \n %s " % pprint.pformat(config_data, indent=4))

	__automate_app(config_data)


if __name__ == '__main__':
	main(sys.argv[1:])

