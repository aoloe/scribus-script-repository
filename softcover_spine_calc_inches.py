#/usr/bin/env python
# -*- coding: utf-8 -*-

import scribus
import math  


from scribus import *


P = scribus.valueDialog('Book Cover Calculator','Enter Number of pages')
P = float(P)
G = scribus.valueDialog('Book Cover Calculator','Enter Paper Weight (ppi)')
G = float(G)
W = scribus.valueDialog('Book Cover Calculator','Enter Page Width in Inches')
W = float(W)
H = scribus.valueDialog('Book Cover Calculator','Enter Page Height in Inches')
H = float(H)
R = scribus.valueDialog('Book Cover Calculator','Enter Cover Paper thickness (ppi)')
R = float(R)
S = (P/G) + ((2/R)*2)
S = float(S)
W2 = W + S + W + 0.079
scribus.newDocument((W2,H), (0.375, 0.375, 0.375, 0.375), scribus.PORTRAIT, 1, scribus.UNIT_INCHES, scribus.PAGE_1, 0, 1) 
scribus.setVGuides([W, (W/2), (W + S/2), (W + S), (W + S + W/2)])
createText((W+S), 0, H, S, "spinetext")
rotateObject(270, "spinetext") 
S = round(S,3)
S=str(S)
zoomDocument(-100)

end = scribus.messageBox('Book Spine Width, Inches:', S, ICON_WARNING, BUTTON_OK)
