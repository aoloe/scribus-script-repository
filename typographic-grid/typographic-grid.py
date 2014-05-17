import sys
try:
   import scribus
except ImportError:
   print "This script only works from within Scribus"
   sys.exit(1)

unit_current=scribus.getUnit() #get unit and change it to mm
scribus.setUnit(scribus.UNIT_MILLIMETERS)

page = scribus.getPageSize()
margin = scribus.getPageMargins()






scribus.setUnit(unit_current)
