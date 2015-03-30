# -*- coding: utf-8 -*-
##
## $id$
##
## This file is part of Indico.
## Copyright (C) 2002 - 2014 European Organization for Nuclear Research (CERN).
##
## Indico is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico;if not, see <http://www.gnu.org/licenses/>.

# stdlib imports
import zope.interface
import os

# legacy imports
from MaKaC.plugins.base import Observable

# indico imports
from indico.core.extpoint import Component
from indico.core.extpoint.events import IObjectLifeCycleListener


from zope.interface import implements
from indico.core.config import Config




class ObjectChangeListener(Component):
    """
    This component listens for events and directs them to the MPT.
    Implements ``IObjectLifeCycleListener``
    Check if you a POSTER is going to be deleted and, in this case, 
    remove the thumbnail, if available.
    """

    implements(IObjectLifeCycleListener)

    def deleted(self, obj, oldOwner):
        print "****DELETED CALL OBJ=",obj, oldOwner
        objType = obj.getFileType().lower()
        objName = obj.getFileName().lower()
        objClass = type(oldOwner).__name__
        objClassTitle = oldOwner.getTitle().lower()
        print "objName:",objName
        print "objType:",objType
        print "objClass:",objClass
        print "objClassTitle:",oldOwner.getTitle().lower()

        if objClass == 'Poster':
            if objName.find('poster') > -1 and objType == 'pdf' and objName.find('list_of_poster') == -1 and objName.find('session') == -1:
                # If POSTER is present, remove it
                tempDir = Config.getInstance().getSharedTempDir()
                postersDir = tempDir+"/posters"
                if os.path.isdir(postersDir):
                    confId = str(oldOwner.owner.getId())
                    thumbPath = postersDir + "/poster_" + confId
                    if os.path.isfile(thumbPath):
                        print "eccolo:",thumbPath
                        os.remove(thumbPath)
        else:
            if (objClassTitle.find('photo') > -1 or objClassTitle.find('picture') > -1 or objClassTitle.find('group') > -1) and objType == 'jpg':
                # If Group Photo is present, remove it
                tempDir = Config.getInstance().getSharedTempDir()
                photoDir = tempDir+"/photos"
                if os.path.isdir(photoDir):
                    confId = str(oldOwner.owner.getId())
                    thumbPath = photoDir + "/photo_" + confId + "_" + objName
                    if os.path.isfile(thumbPath):
                        print "eccolo:",thumbPath
                        os.remove(thumbPath)
            


                    



    def created(self, obj, owner):
        pass
        
    def moved(self, obj, fromOwner, toOwner):
        pass

