# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UnifiedEdit
                                 A QGIS plugin
 Replaces the layer toggle edit button with a unique edit button that toggles editing on all layers, backed by a transaction.
                             -------------------
        begin                : 2015-11-12
        copyright            : (C) 2015 by Matthias Kuhn, OPENGIS.ch LLC
        email                : matthias@opengis.ch
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load UnifiedEdit class from file UnifiedEdit.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .unified_edit import UnifiedEdit
    return UnifiedEdit(iface)
