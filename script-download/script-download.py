# -*- coding: utf-8 -*-
# © 2014, MIT license, Ale Rimoldi <a.l.e@graphicslab.org>
"""
USAGE
 
You must have a document open, and at least one text frame selected.
 
"""
import sys

import urllib.request
import urllib.error
import json

class Controller :
    window = 0
    def setWindow(self, window) :
        self.window = window
        
    def printMessage(self, message) :
        print(message)

    def showMessage(self) :
        window.setProperty("msg", "show") # you cannot return a value from a signal, you have to set a qml property and, then read its value from the qml event

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)
# engine = QQmlApplicationEngine("ui/main.qml")
engine = QQmlApplicationEngine()
colors = [
    { "color": "red", "text": "Zeile 1" },
    { "color": "green", "text": "Zeile 2" },
    { "color": "blue", "text": "Zeile 3" }
]
context = engine.rootContext()
context.setContextProperty("pythonListModel", colors) # the model has to be defined before the qml file is loaded
engine.load("ui/main.qml")
# import pdb; pdb.set_trace()

window = engine.rootObjects()[0]
window.show()

controller = Controller()
controller.setWindow(window)

window.printMessage.connect(controller.printMessage) # i think it should be after window.show(); and signal must be defined in the root element
window.showMessage.connect(controller.showMessage)


# import pdb; pdb.set_trace()

#msg = "efgh"
# window.setContextProperty("msg", msg)
#window.setProperty("msg", msg)
# window.msg = msg

engine.quit.connect(app.quit)
sys.exit(app.exec_())

# button = window.findChild(QObject, "printButton")
# button.printMessage.connect(printMessage)
# button.clicked.connect(printMessage) # better to directly connect he click?

print(test)


sys.exit()


# TODO: manage url not found
 
# gh_url = 'https://raw.github.com/aoloe/scribus-script-repository/master/'
gh_url = 'https://api.github.com/repos/aoloe/scribus-script-repository/git/trees/master?recursive=1'
req = urllib.request.Request(gh_url)
 
# password_manager = urllib.HTTPPasswordMgrWithDefaultRealm()
# password_manager.add_password(None, gh_url, 'user', 'pass')
 
# auth_manager = urllib.HTTPBasicAuthHandler(password_manager)
# opener = urllib.build_opener(auth_manager)
 
# urllib.install_opener(opener)
 
try:
    handler = urllib.request.urlopen(req) # returns http.client.HTTPResponse
    # import pdb; pdb.set_trace()
    response_code = handler.getcode()
except urllib.error.URLError as e:
    if not hasattr(e, "code"):
        raise
    response_code = e.code
 
if response_code == 200 :
    print(handler.getheader('content-type'))
    print(handler.getheader('X-RateLimit-Limit'))
    response = handler.readall().decode('utf-8')
    # print(response)
    file_list = json.loads(response)
    # print(file_list)
    # {u'url': u'https://api.github.com/repos/aoloe/scribus-script-repository/git/trees/caf72ddee55ae345862879bcf2559cf32ccd4a93', u'path': u'CopyPaste', u'type': u'tree', u'mode': u'040000', u'sha': u'caf72ddee55ae345862879bcf2559cf32ccd4a93'}
    # print(file_list['tree'])
    for file in file_list['tree'] :
        print(file['type'])
        print(file['path'])
        # print(file['url'])
elif response_code :
    print('repository URL is not valid ' + gh_url)


def on_qml_mouse_clicked():
    print('mouse clicked')

qml_rectangle = view.rootObject()
qml_rectangle.clicked.connect(on_qml_mouse_clicked)

sys.exit(app.exec_())
