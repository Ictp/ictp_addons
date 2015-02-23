# -*- coding: utf-8 -*-
##
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
import pkg_resources

# legacy imports
#from MaKaC.services.implementation.base import ServiceBase
#from MaKaC.plugins.base import PluginsHolder

# indico imports
from indico.web.handlers import RHHtdocs
from MaKaC.webinterface.urlHandlers import URLHandler
import MaKaC.webinterface.urlHandlers as urlHandlers
#from indico.ext.importer.helpers import ImporterHelper
#import indico.ext.importer.ictp_xlsimporter
import indico.ext.ictp_addons
import indico.ext.ictp_addons.sponsor_management
import os
#from MaKaC.webinterface.rh.conferenceModif import RHConferenceModifBase
from MaKaC.webinterface.rh.conferenceBase import RHSubmitMaterialBase
from MaKaC.webinterface.rh.admins import RHAdminPluginsSaveOptionsBase

#from MaKaC.conference import LocalFile
from indico.util import json
#import xlrd
#import datetime
#from MaKaC.services.implementation.base import ServiceBase
from MaKaC.webinterface.rh.conferenceModif import RHConferenceModifBase
#from MaKaC.webinterface.rh.base import RHProtected

from MaKaC.plugins.base import PluginsHolder
from indico.core.config import Config

from os import listdir
from os.path import isfile, join


#import logging, transaction


import zope.interface
from MaKaC.plugins.base import Observable
from indico.core.extpoint import Component
from indico.core.extpoint.plugins import IPluginImplementationContributor
from MaKaC.services.implementation.base import ServiceBase
from MaKaC.services.implementation.plugins import PluginOptionsBase


class UHLogoUpload(URLHandler):
    _endpoint = '.sponsor_management-upload'


class RHLogoUpload(RHConferenceModifBase):
    _uh = UHLogoUpload
    

    def _checkProtection(self):
        pass

    def _checkParams(self, params):
        pass
        
    def _process(self):
        #print "PROCESSING..."
        htdocsDir = Config.getInstance().getHtdocsDir()
        logoDir = "/css/ICTP/images/sponsor-logo/"
        
        try:
            # lets UPLOAD the file and SAVE it in a custom FOLDER
            fileEntry = self._reqParams['file']
            fileName = fileEntry.filename
            filePath = htdocsDir + logoDir + fileName          
            fileData = fileEntry.read()             
            if os.path.isfile(filePath):
                return json.dumps({'status': 'KO','info': 'ERROR: File EXIST, delete it first.'}) 
                                   
            file = open(filePath, "wb")                                    
            file.write(fileData)
            file.close()
        except:
            return json.dumps({'status': 'KO','info': 'ERROR: File NOT uploaded'})            
            
        return json.dumps({'status': 'OK','info': fileName})








# class UploadOverwrite(ServiceBase):
#     """
#     """
#     
#     def _checkParams(self):
#         pass
#         
#     def _getAnswer(self):        
#         #entries = json.loads(self._data)['data']
#         fileData = self._reqParams['fileData']
#         filePath = self._reqParams['filePath']
#         try:
#             os.remove(filePath)
#             print "removed=",filePath
#         except OSError:
#             pass
#         file = open(filePath, "wb")                                    
#         file.write(fileData)
#         file.close()
#         
#         return json.dumps({'success': True, 'info': self._filePath})




# class Export(ServiceBase):
#     """
#     """
#     
#     def _checkParams(self):
#         ServiceBase._checkParams(self)
#         self._data = self._params['data']
# 
#     def _getAnswer(self):        
#         #entries = json.loads(self._data)['data']
#         return json.dumps({'success': True, 'info': self._data})




# class UHSponsorSave(URLHandler):
#     _endpoint = '.sponsor_management-save'
# 
# class RHSponsorPluginsSaveOptions(RHAdminPluginsSaveOptionsBase):
#     """ Saves values for options of a Plugin or executes an action for this Plugin.
#     """
#     _uh = UHSponsorSave
# 
#     def _checkParams(self, params):
#         plugin = PluginsHolder().getPluginType('ictp_addons').getPlugin("sponsor_management")
#         sponsors_array = plugin.getOptions()["sponsors"].getValue()
#         params["pluginType"]='ictp_addons'
#         params["pluginId"]='sponsor_management'
#         params['ictp_addons.sponsor_management.sponsors'] = sponsors_array
#         
#         # remove deleted files from filesystem
#         htdocsDir = Config.getInstance().getHtdocsDir()
#         logoDir = "/css/ICTP/images/sponsor-logo/"
#         mypath = htdocsDir + logoDir
#         onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
#         logos = []
#         for l in sponsors_array:
#             logos.append(l['logo'])          
#         for fname in onlyfiles:
#             if not fname in logos:
#                 try:
#                     os.remove(mypath + fname)
#                     print "removed=",fname
#                 except OSError:
#                     pass
#         
#         RHAdminPluginsSaveOptionsBase._checkParams(self, params)
#         if self._pluginId is None:
#             raise PluginError(_("pluginId not set"))
#         self._storeParams(params)
# 
#         self._target = self._ph.getPluginType(self._pluginType).getPlugin(self._pluginId)
# 


class PluginImplementationContributor(Component, Observable):
    """
    Adds interface extension to plugins's implementation.
    """

    zope.interface.implements(IPluginImplementationContributor)
        
    def getPluginImplementation(self, obj):
        plugin = PluginsHolder().getPluginType('ictp_addons').getPlugin("sponsor_management")
        return ("sponsor_management", '')



class LoadDefault(PluginOptionsBase):
    """
    """
    
    def _checkParams(self):
        PluginOptionsBase._checkParams(self)
        #self._data = self._params['data']
        #self._confId = self._params['confId']
        for p in self._params.keys():
        	setattr(self, '_link'+p.capitalize(), self._params.get(p, None))        
        

    def _getAnswer(self):        
        #entries = json.loads(self._data)['data']
        try:
            from indico.util.ICTP_available_sponsors import ocirne_dictionary as available_sponsors
        except:
            available_sponsors = {}

        # init sponsor vocabulary
        plugin = PluginsHolder().getPluginType('ictp_addons').getPlugin("sponsor_management")
        #sponsors_array = plugin.getOptions()["sponsors"].getValue()
        sponsors_array = []

        if plugin.isActive():
            for k in available_sponsors.keys():
                d = available_sponsors[k]
                logo = ''
                if d.has_key('logo'):
                    logo = d['logo']
                elem = {
                    'name': k, 
                    'title': d['title'], 
                    'country': d['country'], 
                    'logo': logo,
                    'optionname': 'ictp_addons.sponsor_management.sponsors', 
                    'structure': d['url'],
                    }
                sponsors_array.append(elem)
            
            
        

        #return json.dumps({'success': True, 'table': sponsors_array})


        #print "addLink sponsors_array=",sponsors_array

        self._targetOption.setValue(sponsors_array)
        self._targetOption._notifyModification()
        #plugin.getOption("sponsors").setValue(sponsors_array)
        #print "addLink targetOption+",self._targetOption.getValue()
        
        return {'success': True, 'table': sponsors_array}






methodMap = {
            "sponsor_management.loadDefault" : LoadDefault,
#            "sponsor_management.uploadOverwrite" : UploadOverwrite,
#            "sponsor_management.export" : Export,
             } 