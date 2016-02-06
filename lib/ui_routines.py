import time
import atomac
from atomac.AXKeyCodeConstants import *
from atomac import AXKeyCodeConstants

from logger import Logger
log = Logger.defaults(name='ui_routines',output_stream=False)


def double_click(ui_obj):
	""" mouse activity for double clicking  """
	position = ui_obj.AXPosition
	size = ui_obj.AXSize
	click_point = ((position[0] + size[0] / 2), (position[1] + size[1] / 2))
	try:
		log.debug('click point - %s ' % str(click_point))
		ui_obj.doubleClickMouse(click_point)
	except Exception as er:
		log.info('Error when clicking left - '+str(er))


def click_left(ui_obj):
	""" mouse activity for clicking left  """
	position = ui_obj.AXPosition
	size = ui_obj.AXSize
	click_point = ((position[0] + size[0] / 2), (position[1] + size[1] / 2))
	try:
		log.debug('click point - %s ' % str(click_point))
		ui_obj.clickMouseButtonLeft(click_point)
	except Exception as er:
		log.info('Error when clicking left - '+str(er))


def click_right(ui_obj):
	""" mouse activity for clicking right  """
	position = ui_obj.AXPosition
	size = ui_obj.AXSize
	click_point = ((position[0] + size[0] / 2), (position[1] + size[1] / 2))
	try:
		log.debug('click point - %s ' % str(click_point))
		ui_obj.clickMouseButtonRight(click_point)
	except Exception as er:
		log.info('Error when clicking right - '+str(er))


def open_app(bundle_id=None):
	""" to open the application using the bundle ids """
	if not bundle_id:
			log.debug('BundleId value is empty - %s' % bundle_id)
			return 0
	try:
		atomac.launchAppByBundleId(bundle_id)
		time.sleep(5)
		app_ref = atomac.getAppRefByBundleId(bundle_id)
		app_ref.activate()
		log.info('Bundle Id - %s is opened now' % bundle_id)
		return app_ref
	except Exception:
		log.error('Exception caught while opening app', exc_info=True)
		return 0


def close_app(bundle_id=None):
	""" to close the application using bundle id  """
	if not bundle_id:
			log.debug('BundleId value is empty - %s' % bundle_id)
			return 0
	try:
		atomac.terminateAppByBundleId(bundle_id)
		time.sleep(2)
		return 1
	except Exception:
		log.error('Exception caught while closing app', exc_info=True)
		return 0


def fetch_atomac_ui_object(bundle_id=None):
	""" fetches the ui objects and properties of the opened windows  """
	try:
		return atomac.getAppRefByBundleId(bundle_id)
	except Exception:
		log.warning('Exception caught while  fetching atomac object', exc_info=True)
		return None


def find_atomac_ui_object(app_obj=None):
	"""  Helps to search for the ui properties in the opened app """
	pass
