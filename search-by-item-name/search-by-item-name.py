import scribus
item = scribus.valueDialog("Select items by ID", "id")
scribus.deselectAll()
try:
  scribus.selectObject(item)
except Exception:
  scribus.messageBox("Error", f"Item {item} not found")
