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

import indico.ext.ictp_addons
from MaKaC.webinterface.rh.conferenceModif import RHConferenceModifBase
from indico.util import json
from indico.ext.ictp_addons.register import AddonsRegister
from MaKaC.services.implementation.base import ServiceBase
from indico.web.handlers import RHHtdocs
from MaKaC import conference



class RHIctpaddonsHtdocs(RHHtdocs):
    """Static file handler for Importer plugin"""

    _local_path = pkg_resources.resource_filename(indico.ext.ictp_addons.__name__, "htdocs")
        


class deleteAllTimetable(ServiceBase):
    """
    """
    
    def _checkParams(self):
        ServiceBase._checkParams(self)
        self._confId = self._params['confId']

    def _getAnswer(self):        
        ch = conference.ConferenceHolder()
        conf = ch.getById(self._confId)

        # remove ALL sessions
        for session in conf.getSessionList():
            conf.removeSession(session, deleteContributions=True)

        # remove all Contributions
        for contribution in conf.getContributionList():
            conf.removeContribution(contribution)   

        # remove all Breaks
        for b in conf.getBreakList():
            b.delete()

        return json.dumps({'status': 'OK', 'info': 'ok'})

class changeProtectionTimetable(ServiceBase):
    """
    """
    
    def _checkParams(self):
        ServiceBase._checkParams(self)
        self._confId = self._params['confId']
        self._action = self._params['action']

    def _getAnswer(self):        
        ch = conference.ConferenceHolder()
        conf = ch.getById(self._confId)
        pValue = -1 # Public
        if self._action == 'restrict': pValue = 1
        if self._action == 'inherit': pValue = 0
        if self._action == 'noAction': return json.dumps({'status': 'KO', 'info': 'No action taken'})   

        # set ALL sessions
        for session in conf.getSessionList():
            session.setProtection(pValue)
            for contribution in session.getContributionList():
                contribution.setProtection(pValue)
                contribution.notifyModification()

        # set all Contributions
        for contribution in conf.getContributionList():
            contribution.setProtection(pValue)
            contribution.notifyModification()

        # note: Breaks do not have protection level

        return json.dumps({'status': 'OK', 'info': 'ok'})        

methodMap = {
            "ictp_addons.deleteAllTimetable" : deleteAllTimetable,
            "ictp_addons.changeProtectionTimetable" : changeProtectionTimetable,
             } 