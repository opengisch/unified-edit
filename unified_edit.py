# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UnifiedEdit
                                 A QGIS plugin
 Replaces the layer toggle edit button with a unique edit button that toggles editing on all layers, backed by a transaction.
                              -------------------
        begin                : 2015-11-12
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Matthias Kuhn, OPENGIS.ch LLC
        email                : matthias@opengis.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.core import QgsMapLayerRegistry, QgsTransaction
# Initialize Qt resources from file resources.py
import resources
import os.path


class UnifiedEdit:

    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'UnifiedEdit_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.toolbar = self.iface.digitizeToolBar()

        self.toggleEditSession = QAction(QIcon(':/edit.svg'), 'Start Transaction', self.toolbar)
        self.toggleEditSession.toggled.connect(self.toggleEditSessionToggled)

        self.transaction = None

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.toggleEditSession.setCheckable(True)
        self.toolbar.insertAction(
            self.iface.actionToggleEditing(), self.toggleEditSession)
        self.toolbar.removeAction(self.iface.actionToggleEditing())

    def toggleEditSessionToggled(self, checked):
        if checked:
            self.beginTransaction()
        else:
            self.commitChanges()

    def beginTransaction(self):
            layers = list()
            for l in QgsMapLayerRegistry.instance().mapLayers().keys():
                if not self.transaction:
                    self.transaction = QgsTransaction.create([l])
                    if self.transaction:
                        layers.append(l)
                else:
                    if self.transaction.addLayer(l):
                        layers.append(l)

            if self.transaction:
                self.transaction.begin()

                for l in layers:
                    QgsMapLayerRegistry.instance().mapLayer(l).startEditing()

                self.toggleEditSession.setIcon(QIcon(':commit-end.svg'))

    def commitChanges(self):
        for l in  QgsMapLayerRegistry.instance().mapLayers().values():
            l.commitChanges()

        self.transaction.commit()
        self.toggleEditSession.setIcon(QIcon(':edit.svg'))

    def rollbak(self):
        self.transaction.rollBack()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.toolbar.insertAction(
            self.toggleEditSession, self.iface.actionToggleEditing())

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
