# -*- coding: utf-8 -*-
# © 2014, MIT license, Ale Rimoldi <a.l.e@graphicslab.org>
"""
USAGE
 
You must have a document open, and at least one text frame selected.
 
"""

import urllib2
import json

# TODO: manage url not found
 
# gh_url = 'https://api.github.com'
# gh_url = 'https://raw.github.com/$user/$repository/$branch/'
# gh_url = 'https://raw.github.com/aoloe/scribus-script-repository/master/'
gh_url = 'https://api.github.com/repos/aoloe/scribus-script-repository/git/trees/master?recursive=1'
req = urllib2.Request(gh_url)
 
# password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
# password_manager.add_password(None, gh_url, 'user', 'pass')
 
# auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
# opener = urllib2.build_opener(auth_manager)
 
# urllib2.install_opener(opener)
 
try:
    handler = urllib2.urlopen(req)
    response_code = handler.getcode()
except urllib2.URLError, e:
    if not hasattr(e, "code"):
        raise
    response_code = e.code
 
if response_code == 200 :
    print handler.headers.getheader('content-type')
    print handler.headers["X-RateLimit-Limit"]
    response = handler.read()
    # print response
    file_list = json.loads(response)
    # print file_list
    # {u'url': u'https://api.github.com/repos/aoloe/scribus-script-repository/git/trees/caf72ddee55ae345862879bcf2559cf32ccd4a93', u'path': u'CopyPaste', u'type': u'tree', u'mode': u'040000', u'sha': u'caf72ddee55ae345862879bcf2559cf32ccd4a93'}
    # print file_list['tree']
    for file in file_list['tree'] :
        print file['type']
        print file['path']
        # print file['url']
elif response_code :
    print 'repository URL is not valid ' + gh_url
