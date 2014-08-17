# -*- coding: utf-8 -*-
# © 2014, MIT license, Ale Rimoldi <a.l.e@graphicslab.org>
"""
USAGE
 
You must have a document open, and at least one text frame selected.
 
"""
import sys
import warnings

import urllib.request
import urllib.error
import json

class GitHub :

    username = ''
    repository = ''
    branch = 'master'

    manifest = {}

    def __init__(self, username, repository, branch = None) :
        self.username = username
        self.repository = repository
        if branch != None :
            self.branch = branch
    def readManifest(self) :
        self.manifest = self.getRepositoryManifest()
        print("manifest: "+str(self.manifest))

    def getContentFromUrl(self, url) :
        result = ''

        # TODO: manage url not found

        # gh_url = 'https://api.github.com/repos/aoloe/scribus-script-repository/git/trees/master'
        # password_manager = urllib.HTTPPasswordMgrWithDefaultRealm()
        # password_manager.add_password(None, gh_url, 'user', 'pass')

        # auth_manager = urllib.HTTPBasicAuthHandler(password_manager)
        # opener = urllib.build_opener(auth_manager)

        # urllib.install_opener(opener)
        
        request = urllib.request.Request(url)

        try:
            handler = urllib.request.urlopen(request) # returns http.client.HTTPResponse
            # import pdb; pdb.set_trace()
            response_code = handler.getcode()
        except urllib.error.URLError as e:
            if not hasattr(e, "code"):
                raise
            response_code = e.code

        if response_code == 200 :
            # print(handler.getheader('content-type'))
            # print(handler.getheader('X-RateLimit-Limit'))
            result = handler.readall().decode('utf-8')
        else :
            warnings.warn(message = "url is not valid: "+url, stacklevel = 2)

        return result

    def getJsonFromUrl(self, url) :
        result = {}
        response = self.getContentFromUrl(url)
        # print("response: "+response)
        if response :
            result = json.loads(response)
        return result

    def getRepositoryManifest(self) :
        result = {}
        url = 'https://raw.githubusercontent.com/%s/%s/%s/manifest.json' % (self.username, self.repository, self.branch)
        # print('url :'+url)
        result = self.getJsonFromUrl(url)
        return result

    def getScriptList(self) :
        result = []
        # gh_url = 'https://api.github.com/repos/aoloe/scribus-script-repository/git/trees/master?recursive=1'
        url = 'https://api.github.com/repos/%s/%s/git/trees/%s' % (self.username, self.repository, self.branch)
        file_list = self.getJsonFromUrl(url)
        # print(file_list)
        # {u'url': u'https://api.github.com/repos/aoloe/scribus-script-repository/git/trees/caf72ddee55ae345862879bcf2559cf32ccd4a93', u'path': u'CopyPaste', u'type': u'tree', u'mode': u'040000', u'sha': u'caf72ddee55ae345862879bcf2559cf32ccd4a93'}
        if file_list :
            for file in file_list['tree'] :
                if file['type'] == 'tree' :
                    if (self.isScriptPublished(file['path'])) :
                        result.append({"scriptName": file['path'], "installed": False});
        else :
            print('repository URL is not valid: ' + url)

        return result

    def isScriptPublished(self, script) :
        result = True
        if 'script_ignore' in self.manifest :
            result = script not in self.manifest['script_ignore']
        elif 'script' in self.manifest :
            result = script in self.manifest['script']
        return result


class Controller :
    window = 0
    def setWindow(self, window) :
        self.window = window
        
    # def printMessage(self, message) :
        # print(message)

    # def showMessage(self) :
        # window.setProperty("msg", "show") # you cannot return a value from a signal, you have to set a qml property and, then read its value from the qml event

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

github = GitHub('aoloe', 'scribus-script-repository')
github.readManifest()

app = QGuiApplication(sys.argv)
# engine = QQmlApplicationEngine("ui/main.qml")
engine = QQmlApplicationEngine()
repositoryType = [
    { "text": "GitHub" }
]
# TODO: read the list of defined repositories from a conf file
repository = [
    { "text": "Unofficial script collection" }
]
# TODO: read the list of installed scripts per repo from a conf file
context = engine.rootContext()
context.setContextProperty("pythonRepositoryTypeModel", repositoryType)
context.setContextProperty("pythonRepositoryListModel", repository)
context.setContextProperty("pythonScriptListModel", github.getScriptList())
engine.load("ui/main.qml")
# import pdb; pdb.set_trace()

try:
    window = engine.rootObjects()[0]
except Exception as e:
    print("The QML file has not been correctly loaded");
    sys.exit();

window.show()

controller = Controller()
controller.setWindow(window)

# window.printMessage.connect(controller.printMessage) # i think it should be after window.show(); and signal must be defined in the root element
# window.showMessage.connect(controller.showMessage)


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
