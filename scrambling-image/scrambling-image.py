# -*- coding: utf-8 -*-
# © 2014.06.26 ale rimoldi <ale@graphicslab.org>
# This program is free software under the MIT license.
"""
USAGE
 
You must have a document open.
WARNING: this script replaces all your images on all pages.
You would be wise to work on a copy of the original to avoid 
accidentally saving this scrambled version only to lose the original.
"""

#import scribus

import random, urllib2, re

# inspired by http://megasnippets.com/en/source-codes/python/get_random_interesting_image_flickr
def getFreeFlickrUrls(query=None):
    ''' Returns a list of paths to random free (cc-by) images from Flickr.com.
        Input:
            query (string): An optional query word.
                 If query is not provided, "test" will be used.
        
        Output:
            (string) List of urls
                     An empty list if no images are not found.
    '''
    if not query:
        query = 'test'

    # url = 'http://flickr.com/explore/interesting/%s/page%d/' % (randomDay.strftime('%Y/%m/%d'),random.randint(1,20))
    url = 'https://www.flickr.com/search/?q=%s&l=commderiv&ct=0&mt=all&adv=1' % (query)
    urlfile = urllib2.urlopen(url)
    html = urlfile.read(500000)
    urlfile.close()
    print url
    # print html

    # text_file = open("output.txt", "w")
    # text_file.write(html)
    # text_file.close()

    #                         data-defer-src="https://farm4.staticflickr.com/3715/9197345028_8c352de0ed.jpg"
    re_imageurl = re.compile('src="(https://farm\d+.staticflickr.com/\w+/\w+.jpg)', re.IGNORECASE|re.DOTALL)
    urls = re_imageurl.findall(html)
    # print urls
    return urls

# inspired by http://megasnippets.com/en/source-codes/python/get_random_interesting_image_flickr
def getFreeFlickrImage(url) :
    filein = urllib2.urlopen(url)
    try:
        image = filein.read(5000000)
    except MemoryError: # I sometimes get this exception. Why ?
        return None
        
    filein.close()
    
    # Check it.
    if len(image)==0:
        return None  # Sometimes flickr returns nothing.
    if len(image)==5000000:
        return None  # Image too big. Discard it.        
    if image.startswith('GIF89a'):
        return None # "This image is not available" image.
    
    # Save to disk.
    filename = url[url.rindex('/')+1:]
    fileout = open(filename,'w+b')
    fileout.write(image)
    fileout.close()
    return filename

urls = getFreeFlickrUrls()
url = random.choice(urls)
print url
imagePath = getFreeFlickrImage(url)
print imagePath

"""
#
 
if scribus.haveDoc():
    c = 0
 
else:
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)
scribus.messagebarText("Getting ready to process Page 1")  # a bit kludgey maybe, but gives an initial message about Page 1
scribus.redrawAll()
 
warnresult = scribus.valueDialog('Warning!', 'This script is going to irreversibly alter the text in your document.\nChange this default value to abort', 'Ok!')
 
if (warnresult != 'Ok!'):
    sys.exit(2)
 
page = 1
pagenum = scribus.pageCount()
while (page <= pagenum):
  scribus.gotoPage(page)
  scribus.messagebarText("Processing Page "+str(page)) # New Feature! - sends a message to message bar 
  scribus.redrawAll()                                  # this allows the message to show
 
  pageitems = scribus.getPageItems()
 
  for item in pageitems:
    if (item[1] == 4):
      c = 0
      textbox = item[0]
      scribus.selectObject(textbox)
      contents = scribus.getTextLength(textbox)
 
      while 1:
	  if ((c == contents) or (c > contents)): break
	  if ((c + 1) > contents - 1):
	      nextchar = ' '
	  else:
	      scribus.selectText(c+1, 1, textbox)
	      nextchar = scribus.getText(textbox)
	  scribus.selectText(c, 1, textbox)
	  char = scribus.getText(textbox)
	  if (len(char) != 1):   # here is where you skip over any nonprinting characters
	      c += 1
	      continue
	  alpha = random.randint(1,26)
	  letter = chr(alpha + 96)
	  LETTER = chr(alpha + 64)
	  if ((ord(char)>96)and(ord(char)<123)):
	      scribus.deleteText(textbox)
	      scribus.insertText(letter, c, textbox)
	  if ((ord(char)>64)and(ord(char)<91)):
	      scribus.deleteText(textbox)
	      scribus.insertText(LETTER, c, textbox)
 
	  c += 1
	  contents = scribus.getTextLength(textbox)
  page += 1
 
scribus.setRedraw(1)
scribus.docChanged(1)
scribus.messageBox("Finished", "That should do it!",icon=0,button1=1)
"""
