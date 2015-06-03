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
import xlwt
from flask import Response
import StringIO
from MaKaC.conference import ConferenceHolder

from MaKaC.webinterface.rh.conferenceModif import RHConferenceModifBase
import datetime

from MaKaC.schedule import  BreakTimeSchEntry

class RHIctpaddonsHtdocs(RHHtdocs):
    """Static file handler for Importer plugin"""

    _local_path = pkg_resources.resource_filename(indico.ext.ictp_addons.__name__, "htdocs")


        
class RHexportTimetableXLS(RHConferenceModifBase):

    def _checkProtection(self):
        pass

    def _checkParams(self, params):
        pass
        
    def _process(self):
        confId = self._reqParams['confId']
        ch = ConferenceHolder()       
        conf = ch.getById(confId)
        
        headers=["Start Date","End Date","Event Type","Title","Repno","Start Time","Duration","Speaker","Affiliation","Room","Comment"]
        book = xlwt.Workbook(encoding="utf-8")
        styleBold = xlwt.easyxf('font: bold True;')
        styleHM = xlwt.XFStyle()
        
        #styleHM.num_format_str = 'h:mm:ss'
        styleHM.num_format_str = 'h:mm' 
        styleDate = xlwt.XFStyle()
        styleDate.num_format_str = 'yyyy/mm/dd'  
                
        # HEADERS
        sheet1 = book.add_sheet("agenda_tool")
        sheet1.write(0, 0, "TIMETABLE-START",styleBold)
        pos = 0
        for head in headers:
            sheet1.write(1, pos, head, styleBold)
            pos+=1
        # Hide End Date and Repno column
        sheet1.col(1).hidden = True
        sheet1.col(4).hidden = True

        # CONTENTS
        row = 1
        defaultRoom = conf.getRoom().getName()
        for session in conf.getSessionListSorted():
            row+=1
            sheet1.write(row, 0, session.getStartDate().date(), styleDate)
            sheet1.write(row, 2, 'SESSION')
            sheet1.write(row, 3, session.getTitle())

            #sheet1.write(row, 5, session.getStartDate().strftime('%H:%M:00'), styleHM)
            sheet1.write(row, 5, session.getStartDate().time(), styleHM)
 
            firstEntry = True
            for slot in session.getSortedSlotList():
                for slotEntry in slot.getSchedule().getEntries():
                    entryType = 'TALK'
                    if isinstance(slotEntry, BreakTimeSchEntry):
                        entryType = 'BREAK'
                    row+=1
                    sheet1.write(row, 2, entryType)
                    sheet1.write(row, 3, slotEntry.getTitle())
                    if firstEntry:
                        sheet1.write(row, 5, slotEntry.getStartDate().time(), styleHM)
                        firstEntry = False
                    td = slotEntry.getDuration()                    
                    sheet1.write(row, 6, (datetime.datetime.min + td).time(), styleHM)
                    
                    if entryType == 'TALK':
                        speakers = slotEntry.getOwner().getSpeakerList()
                        if len(speakers) == 1:
                            value = speakers[0].getValues()
                            name = value['firstName']
                            if value['familyName']: name+= " " + value['familyName']
                            sheet1.write(row, 7, name) 
                            if value['affilation']:
                                sheet1.write(row, 8, value['affilation'])
                        elif speakers:
                            i=1
                            name = ''                                                         
                            for speaker in speakers:
                                value = speaker.getValues()
                                name += value['firstName']
                                if value['familyName']: name+= " " + value['familyName']
                                if value['affilation']: name+= " (" + value['affilation'] + ")"
                                if i<len(speakers): name += ", "
                                i += 1
                            sheet1.write(row, 7, name)  
                                    
                    room = slotEntry.getRoom().getName()
                    if room and room != defaultRoom:
                        sheet1.write(row, 9, slotEntry.getRoom().getName())     
                    
                    

        f = StringIO.StringIO() # create a file-like object 
        book.save(f)

        
        response = Response(f.getvalue(),  mimetype='application/ms-excel')
        response.headers['Content-Type'] = "application/vnd.ms-excel"
        response.headers.add('Content-Disposition', 'attachment', filename='timetable-'+confId+'.xls')
        
        return response





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
            #"ictp_addons.exportXLS" : exportXLS,
            "ictp_addons.deleteAllTimetable" : deleteAllTimetable,
            "ictp_addons.changeProtectionTimetable" : changeProtectionTimetable,
             } 