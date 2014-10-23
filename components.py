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
import os
import zope.interface
from webassets import Bundle

# legacy imports
from MaKaC.plugins.base import Observable
from indico.core.config import Config
from MaKaC.common.info import HelperMaKaCInfo

# indico imports
from indico.web.assets import PluginEnvironment
from indico.core.extpoint import Component
from indico.core.extpoint.events import ITimetableContributor
from indico.core.extpoint.plugins import IPluginDocumentationContributor
from indico.ext.importer.pages import WPluginHelp


class Ictp_addonsContributor(Component, Observable):
    """
    Adds interface extension to event's timetable modification websites.
    """

    zope.interface.implements(ITimetableContributor)

    @classmethod
    def includeTimetableJSFiles(cls, obj, params={}):
        """
        Includes additional javascript file.
        """
        info = HelperMaKaCInfo.getMaKaCInfoInstance()
        asset_env = PluginEnvironment('ictp_addons', os.path.dirname(__file__), '/ictp_addons')
        asset_env.debug = info.isDebugActive()
        asset_env.register('ictp_addons_js', Bundle('js/ictp_addons.js',
                                                 filters='rjsmin',
                                                 output="ictp_addons__%(version)s.min.js"))
        params['paths'].extend(asset_env['ictp_addons_js'].urls())
        



    @classmethod
    def customTimetableLinks(cls, obj, params={}):
        """
        Inserts customized links in a timetable header.
        """
        params.update({"Delete Timetable" : "createDeleteAllDialog","Set Entries Protection" : "createTimetableProtectionDialog"})


class PluginDocumentationContributor(Component):

    zope.interface.implements(IPluginDocumentationContributor)

    def providePluginDocumentation(self, obj):
        return