# -*- coding: utf-8 -*-
##
##
## This file is part of Indico
## Copyright (C) 2002 - 2014 European Organization for Nuclear Research (CERN)
##
## Indico is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico.  If not, see <http://www.gnu.org/licenses/>.

from MaKaC.common.logger import Logger
from MaKaC.plugins.base import PluginsHolder, extension_point
from indico.ext.register import Register



class AddonsRegister(Register):
    """
    This register acts as both a wrapper against the legacy PluginsHolder
    and a quick-access object for injecting tracking codes etc into the
    extension points of Indico.
    """

    def _buildRegister(self):
        """
        Static mapping attributes for plugin implementations in register.
        Append lines to add further implementations.
        """
        self._registeredImplementations =  dict((key, value) for (key, value) in extension_point("getPluginImplementation"))



