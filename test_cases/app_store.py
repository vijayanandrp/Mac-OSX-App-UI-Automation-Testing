import time
import atomac
from atomac.AXKeyCodeConstants import *
from atomac import AXKeyCodeConstants
from ui_routines import open_app, close_app, double_click, click_left
from utils import OsUtils
from config import app_store_id
from logger import Logger

log = Logger.defaults("app_store", output_stream=False)

os_util = OsUtils()

# ##########################################
# ############# FUNCTIONS ##################


def click_appstore_icon(identifier=None):
	""" This function clicks the featured icon in the App Store """
	# open the product
	app_store = atomac.getAppRefByBundleId(app_store_id)
	app_store.activate()
	time.sleep(1)
	# search for the UI object
	app_store_obj = app_store.windows()[0].findAllR(AXRole='AXRadioButton', AXTitle='', AXIdentifier=identifier)
	if not len(app_store_obj):
		log.info('No clicking object found')
		return None
	# double click the ui obj
	double_click(app_store_obj[0])
	time.sleep(5)
	return 1


def search_in_appstore(search_value='Linux'):
	""" this function helps to search the apps in search filed  """
	try:
		app_store = atomac.getAppRefByBundleId(app_store_id)
		app_store.activate()
	except ValueError:
		return -1
	time.sleep(1)
	app_store_obj = app_store.windows()[0].findAllR(AXRole='AXTextField', AXRoleDescription='search text field')[0]
	click_left(app_store_obj)
	# select all
	app_store_obj.sendKeyWithModifiers('a', [COMMAND])
	# delete the previous entry
	app_store_obj.sendKey(DELETE)
	# enter the search value
	app_store_obj.sendKeys(search_value)
	# enter key to search
	app_store_obj.sendKey(RETURN)
	time.sleep(10)

# ##########################################
# ############# TEST CASES #################


def tc_662249():
	if not open_app(app_store_id):
		return 0

	time.sleep(30)
	log.info('looking for crash after opening apps')
	os_util.check_crashes('AppStore')
	time.sleep(10)

	if not close_app(app_store_id):
		return 0

	return 1


def tc_662250():
	if not open_app(app_store_id):
		return 0

	time.sleep(5)
	log.info('Clicking Featured icon in the app store')
	click_appstore_icon(identifier='updates')
	time.sleep(10)

	if not close_app(app_store_id):
		return 0

	return 1


def tc_662251():
	if not open_app(app_store_id):
		return 0

	time.sleep(5)
	log.info('Clicking Featured icon in the app store')
	click_appstore_icon(identifier='top-charts')
	time.sleep(10)

	if not close_app(app_store_id):
		return 0

	return 0


def tc_662252():
	if not open_app(app_store_id):
		return 0

	time.sleep(5)
	log.info('Clicking Featured icon in the app store')
	click_appstore_icon(identifier='genres')
	time.sleep(10)

	if not close_app(app_store_id):
		return 0

	return 1


def tc_662253():
	if not open_app(app_store_id):
		return 0

	time.sleep(5)
	log.info('Clicking Featured icon in the app store')
	click_appstore_icon(identifier='purchased')
	time.sleep(10)

	if not close_app(app_store_id):
		return 0

	return -1


def tc_662254():
	if not open_app(app_store_id):
		return 0

	time.sleep(5)
	log.info('search in app store')
	search_in_appstore(search_value='Angry Birds')
	time.sleep(30)

	if not close_app(app_store_id):
		return 0

	return 1

