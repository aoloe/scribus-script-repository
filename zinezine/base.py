#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scribus as s

if not s.haveDoc():
    s.newDocument((105,148.5), (0,0,0,0),s.PORTRAIT,1,s.UNIT_MILLIMETERS,s.PAGE_2,0,8)
    s.setDocType(s.FACINGPAGES,s.FIRSTPAGERIGHT)
    s.gotoPage(1)
