#!/usr/bin/env python2
# -*- coding: utf8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""Example script which uses WebdavMirror."""

import subprocess
import sys
import fnmatch
import os
from WebdavMirror import WebdavMirror

mirrorDir = "/path/to/mirrordir"
username = 'hans'
password = 'wurst'

webFolders = [
(2896, "Semester-2", "Algorithmen und Datenstrukturen"),
]

# Mirror
for webFolder in webFolders:
    mirrorPath = "%s/%s/%s" % (mirrorDir, webFolder[1], webFolder[2])
    if not os.path.exists(mirrorPath):
        os.makedirs(mirrorPath)
    WebdavMirror('https://read.mi.hs-rm.de/webdav.php/', '/readmi/ref_%d/' % webFolder[0], username, password, mirrorPath)
    f.close()
