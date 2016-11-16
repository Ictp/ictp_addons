# -*- coding: UTF-8 -*-
# stdlib imports
from datetime import datetime

import pytz
from flask import request
from indico.MaKaC.webinterface import internalPagesMgr
from indico.core.extpoint import Component
from indico.core.extpoint.events import IObjectLifeCycleListener
import indico.MaKaC.webinterface.displayMgr as displayMgr
from zope.interface import implements



class MyChangeListener(Component):
    """
    This component listens for events and directs them to the MPT.
    Implements ``IObjectLifeCycleListener``
    """

    implements(IObjectLifeCycleListener)

    def deleted(self, obj, oldOwner):
        return

    def createPage(self, obj):
        pageTitle = "How to participate"
        pageContent = "<div><p></p><p>Participation in ICTP activities is by application. If you wish to apply to this activity, " \
                      "please click on the \"Apply here\" link in the left menu. You will be notified about the outcome " \
                      "of your application in due time.</p><p>There are no registration fees, unless otherwise " \
                      "indicated.</p><p>Accommodation is available on a first-come first-served basis in the ICTP " \
                      "Guesthouses on campus. Room rates and other details can be found " \
                      "<a href=\"https://www.ictp.it/visit-ictp/accommodation/guesthouses.aspx\" target=\"_blank\">" \
                      "here</a>. If you are selected for participation you will receive instructions regarding " \
                      "accommodation in the invitation letter.</p><p>Participants from developing countries " \
                      "(see list <a href=\"http://www.ictp.it/visit-ictp/developingcountries.aspx\" target=\"_blank\">" \
                      "here</a>, particularly those at the early stages of their career, can apply for grants to " \
                      "support their participation. Grants can cover local costs and/or travel costs, as " \
                      "indicated in the application form. ICTP encourages the participation of female scientists." \
                      "</p><p>If your country is not included in the list above but you believe there are good " \
                      "reasons for you to be considered for a travel grant, please mention it in the \"comments\" " \
                      "field at the end of the application form.</p><p>Some countries have signed agreements" \
                      " with ICTP to make available, for their own nationals, a small number of travel grants, " \
                      "for participation in various ICTP activities. These grants are listed " \
                      "<a href=\"https://www.ictp.it/travel-fellowships.aspx\" target=\"_blank\">here</a>. </p></div>"

        intPagesMgr=internalPagesMgr.InternalPagesMgrRegistery().getInternalPagesMgr(obj)
        if pageTitle not in [page.getTitle() for page in intPagesMgr.getPagesList()]:
            intPage=internalPagesMgr.InternalPage(obj)
            intPage.setTitle(pageTitle)
            intPage.setContent(pageContent)
            intPagesMgr.addPage(intPage)
            #create the link
            name = pageTitle
            if name.strip()=="":
                name="[empty name]"
            content = pageContent
            displayTarget = ""
            menu = displayMgr.ConfDisplayMgrRegistery().getDisplayMgr(obj).getMenu()
            target = menu
            link = displayMgr.PageLink(name, intPage)
            link.setCaption(name)
            link.setDisplayTarget(displayTarget)
            target.addLink(link)
        return


    def created(self, obj, owner):
        if type(obj).__name__ == 'Conference':
            # Only if IN "ICTP activities in Trieste" or "ICTP activities outside Trieste" or "Test"
            if obj.getOwner().getId() in ['2l131', '2l132', '1']:
                # Only if StartDate >= 1/1/2017
                rf = request.form
                startDate = datetime( int(rf.getlist('sYear')[0]), int(rf.getlist('sMonth')[0]), int(rf.getlist('sDay')[0]) )
                if startDate >= datetime(2017, 1, 1):
                    self.createPage(obj)
        return
        
    def moved(self, obj, fromOwner, toOwner):
        return

