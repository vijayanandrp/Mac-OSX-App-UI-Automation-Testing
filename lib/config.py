import os
import commands

current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# directory configurations
data_path = os.path.join(current_dir, 'data')
logs_path = os.path.join(data_path, 'logs')
config_path = os.path.join(data_path, 'configurations')
test_case_xl_path = os.path.join(data_path, 'test_case_xl')
result_path = os.path.join(data_path, 'result')

# logger configurations
log_file = os.path.join(logs_path, 'automation.log')

# Application BundleId
app_store_id = "com.apple.appstore"


# Crash file location
home = commands.getstatusoutput('echo $HOME')
crash_path = '/Library/Logs/DiagnosticReports'
user_crash_path = os.path.join(home[1], 'Library/Logs/DiagnosticReports' )
