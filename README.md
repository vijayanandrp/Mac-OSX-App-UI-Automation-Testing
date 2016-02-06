# Automation---Mac-OS-X---Applications
Simple python framework for automating client apps in Mac OS X using atomac and accessibility controls

http://vijay-anand-pandian.blogspot.in/2015/03/simple-automation-using-python-atomac.html
----------------------------------------------------------------------------------------------
This framework is written to automate the mac os x client side applications.
Especially for UI testing and validation.

I have used the atomac python library for automating this stuff.

TO-DO
=====
1. First try to run cli_automation.py
2. Install the dependencies in your machine like atomac and openpyxl
3. Make sure you have give the accessibility permissions to run the application (/data/snaps)


Configurations
==============
/data/configurations/

{
  "test_cases" : "app_store.py",
  "test_case_xl" : "app_store_ui_test.xlsx"
}

"test_cases" denotes the python file where you written your testcases for automation
"test_case_xl" denotes the excel file where you have the testcaes id and description
	Note: Make sure you have used only column A and B alone. Kindly refer my xlsx file.


Testcases
==========
/test_cases

this folder is maintained for writing the testcases


Logs
======
/data/logs/

Logging for the execution of the testc cases are stored and maintained in automation.log

Results
=======

/data/results/

{
  "test_cases" : "app_store.py",
  "test_case_xl" : "app_store_ui_test.xlsx"
}

Result file will be same as "test_case_xl" : "app_store_ui_test.xlsx"

i.     Passed testcases are denoted in DARK GREEN
ii.    Failed testcases are denoted in RED
iii.   Warning/Exception testcases are denoted in THICK BLUE

Library
=======
/lib/

This folder is maintained for the common functions and reusable codes for reducing the code repetition.

