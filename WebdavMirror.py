# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
"""A simple Webdav mirror based on https://launchpad.net/python-webdav-lib

@author Markus Tacker <m@tacker.org>"""

from webdav import *
from webdav.WebdavClient import *
import logging
import os
from urllib import unquote
from time import mktime
import sys

class WebdavMirror(object):
    def __init__(self, url, basedir, username = None, password = None, targetdir = './'):
        """Mirror the ressources found at url to the local targetdir.
           basedir is the webdav folder name to start from.
           If username and password are given they're used for authentication."""
        if url[-1] == '/':
            url = url[0:-1]
        self._url = url
        if basedir[-1] != '/':
            basedir = basedir + '/'
        if basedir[0] != '/':
            basedir = '/' + basedir
        self._basedir = basedir
        self._username = username
        self._password = password
        if not os.path.isdir(targetdir):
            raise Exception('Not a directory %s' % targetdir)
        self._targetdir = os.path.realpath(targetdir) + os.sep

        self.mirrorContents()

    def mirrorContents(self, url = None):
        "Recursive mirror the contents of the given url"
        if url is None:
            url = self._url + self._basedir

        webdavConnection = CollectionStorer(url, validateResourceNames=False)
        webdavConnection.connection.logger.setLevel(logging.WARN)
        
        authFailures = 0
        while authFailures < 2:
            try:
                for resource, properties in webdavConnection.getCollectionContents():
                    if properties.getResourceType() == 'collection':
                        newurl = self._url + str(properties.properties['displayname'])
                        if newurl == url:
                            # Recursion
                            continue
                        self.mirrorContents(newurl)
                    else:
                        target = self._targetdir + unquote(str(properties.properties['displayname'])).replace(self._basedir, '')
                        mtime = mktime(properties.getLastModified())
                        if not os.path.isdir(os.path.dirname(target)):
                            os.makedirs(os.path.dirname(target))
                        if os.path.isfile(target):
                            stats = os.stat(target)
                            if stats.st_size == properties.getContentLength() and stats.st_mtime == mtime:
                                continue
                        resource.downloadFile(target)
                        os.utime(target, (mtime, mtime))
                
                break # break out of the authorization failure counter
            except AuthorizationError, e:
                if e.authType == "Basic":
                    webdavConnection.connection.addBasicAuthorization(self._username, self._password)
                elif e.authType == "Digest":
                    info = parseDigestAuthInfo(e.authInfo)
                    webdavConnection.connection.addDigestAuthorization(self._username, self._password, realm=info["realm"], qop=info["qop"], nonce=info["nonce"])
                else:
                    raise
                authFailures += 1

if __name__ == "__main__":
    import sys
 
    webdavUrl = sys.argv[1]
    basedir = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    targetdir = sys.argv[5]

    WebdavMirror(webdavUrl, basedir, username, password, targetdir)

