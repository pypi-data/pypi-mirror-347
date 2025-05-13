# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSignal, Qt, QStringListModel, QEvent, pyqtSlot, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QHeaderView
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QApplication, QLabel

from ui_mainwindow import Ui_MainWindow

from pr22 import exceptions, imaging, processing, task, util
from pr22 import DocumentReaderDevice, Event
from pr22.processing import FieldSource, FieldId, Field, FieldReference


class StrCon:
    """ This class makes string concatenation with spaces and prefixes. """

    def __init__(self, bounder=None):
        self.cstr = (bounder+" ") if bounder else ""
        self.fstr = ""

    def __add__(self, arg):
        """  StrCon + arg """
        if arg: arg = self.cstr + arg
        if self.fstr and arg and arg[0] != ',': self.fstr += " "
        return self.fstr + arg

    def __radd__(self, arg):
        """  arg + StrCon  """
        self.fstr = arg
        return self


class EventHandler(QObject):

    Connection           = pyqtSignal(list)
    DocFrameFound        = pyqtSignal(int)
    ScanFinished         = pyqtSignal()
    ImageScanned         = pyqtSignal(int, imaging.Light)
    PresenceStateChanged = pyqtSignal(util.PresenceState)

    def __init__(self, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)

    def register_events(self, dr_dev):
        dr_dev.add_event_handler(Event.Connection, self.on_connection)
        dr_dev.add_event_handler(Event.PresenceDetection, self.on_presence_state_changed)
        dr_dev.add_event_handler(Event.ImageScanned, self.on_image_scanned)
        dr_dev.add_event_handler(Event.ScanFinished, self.on_scan_finished)
        dr_dev.add_event_handler(Event.DocFrameFound, self.on_doc_frame_found)

    def on_connection(self, device, dr_dev):
        # This raises only when no device is used or when the currently
        # used device is disconnected.
        devlist = dr_dev.list_devices(dr_dev)
        self.Connection.emit(devlist)

    def on_doc_frame_found(self, page, dr_dev):
        # To rotate the document to upside down direction the analyze()
        # method should be called.
        self.DocFrameFound.emit(page)

    def on_scan_finished(self, page, status, dr_dev):
        self.ScanFinished.emit()

    def on_image_scanned(self, page, light, dr_dev):
        self.ImageScanned.emit(page, light)

    def on_presence_state_changed(self, state, dr_dev):
        # To raise this event FreerunTask.detection() has to be started.
        if state == util.PresenceState.Present:
            self.PresenceStateChanged.emit(util.PresenceState(state))

# ---------------------------------------------------------------------------- #


class MainWindow(QMainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QApplication.instance().installEventFilter(self)

        self.setFixedSize(self.width(), self.height())

        try:
            self.pr = DocumentReaderDevice()
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)
            exit(1)

        evh = EventHandler()

        evh.Connection.connect(self.slotGetDeviceModel)
        evh.ImageScanned.connect(self.slotDrawImage)
        evh.ScanFinished.connect(self.slotAnalyze)
        evh.ScanFinished.connect(self.slotCloseScan)
        evh.DocFrameFound.connect(self.slotRunDocFrameFound)
        evh.PresenceStateChanged.connect(self.on_PresenceStateChanged)

        evh.register_events(self.pr)

        strlist = ["MRZ", "VIZ", "BCR"]
        for field in strlist:
            item = QListWidgetItem(field + " fields", self.ui.listWidgetOCR)
            item.setFlags(item.flags() or Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

        self.modelGrid = QStandardItemModel()
        self.modelGrid.setHorizontalHeaderItem(0, QStandardItem("Field ID"))
        self.modelGrid.setHorizontalHeaderItem(1, QStandardItem("Value"))
        self.modelGrid.setHorizontalHeaderItem(2, QStandardItem("Status"))
        self.modelGrid.setHorizontalHeaderItem(3, QStandardItem("ID"))

        self.ui.tableViewGrid.setModel(self.modelGrid)
        self.ui.tableViewGrid.setColumnWidth(0, 160)

        self.ui.tableViewGrid.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.tableViewGrid.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.ui.tableViewGrid.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableViewGrid.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableViewGrid.setColumnHidden(3, True)

        self.listModel = None
        self.ScanCtrl  = None
        self.AnalyzeResult = None
        self.DeviceIsConnected = False

    def closeEvent(self, event):
        if self.DeviceIsConnected:
            self.slotCloseScan()
            QApplication.processEvents()
            self.pr.close_device()

# region Connection
# ---------------------------------------------------------------------------- #

    @pyqtSlot(list)
    def slotGetDeviceModel(self, devlist):
        del self.listModel
        self.listModel = QStringListModel(devlist, None)
        self.ui.listViewDevices.setModel(self.listModel)

    @pyqtSlot()
    def on_pushButtonConnect_clicked(self):
        index = self.ui.listViewDevices.currentIndex()
        item =  index.data(Qt.DisplayRole)

        if not item: return

        self.ui.pushButtonConnect.setEnabled(False)
        self.ui.pushButtonConnect.repaint()
        self.setCursor(Qt.WaitCursor)
        try:
            self.pr.use_device(item)

            self.DeviceIsConnected = True
            self.pr.scanner.start_task(task.FreerunTask.detection())
            self.ui.pushButtonDisconnect.setEnabled(True)
            for light in self.pr.scanner.info.list_lights():
                lightName = imaging.Light.compat_str(light)
                item = QListWidgetItem(lightName, self.ui.listWidgetLights)
                item.setFlags(item.flags() or Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
            self.ui.pushButtonStart.setEnabled(True)

        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)
            self.on_pushButtonDisconnect_clicked()
        self.setCursor(Qt.ArrowCursor)

    @pyqtSlot()
    def on_pushButtonDisconnect_clicked(self):
        if self.DeviceIsConnected:
            self.slotCloseScan()
            QApplication.processEvents()
            self.pr.close_device()
            self.DeviceIsConnected = False
        self.ui.pushButtonConnect.setEnabled(True)
        self.ui.pushButtonDisconnect.setEnabled(False)
        self.ui.pushButtonStart.setEnabled(False)
        self.ui.listWidgetLights.clear()
        self.RemoveTabs()
        self.RemoveGridRows()
        self.ClearOCRData()
        self.ClearDataPage()

# endregion

# region Scanning
# ---------------------------------------------------------------------------- #

    @pyqtSlot(util.PresenceState)
    def on_PresenceStateChanged(self, state):
        self.on_pushButtonStart_clicked()

    @pyqtSlot()
    def on_pushButtonStart_clicked(self):
        self.RemoveTabs()
        self.RemoveGridRows()
        self.ClearOCRData()
        self.ClearDataPage()

        scantask = task.DocScannerTask()

        count = 0
        for item in self.ui.listWidgetLights.findItems('*', Qt.MatchWildcard):
            if item.checkState() == Qt.Checked:
                self.AddTabPage(item.text())
                scantask.add(imaging.Light.parse(item.text()))
                count += 1
        if count == 0:
            QMessageBox.information(self, "Info", "No light selected to scan!")
            return

        self.ui.pushButtonStart.setEnabled(False)
        try:
            self.ScanCtrl = self.pr.scanner.start_scanning(scantask, imaging.PagePosition.First)
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)

    @pyqtSlot(int)
    def slotRunDocFrameFound(self, page):
        if not self.ui.checkBoxDocView.isChecked(): return

        for ix in range(self.ui.tabWidgetRight.count()):
            label = self.ui.tabWidgetRight.widget(ix)
            if isinstance(label, QLabel) and label.pixmap():
                light = imaging.Light.parse(self.ui.tabWidgetRight.tabText(ix))
                self.slotDrawImage(page, light)

    @pyqtSlot(int, imaging.Light)
    def slotDrawImage(self, page, light):
        docimage = self.pr.scanner.get_page(page).select(light)
        lightname = imaging.Light.compat_str(light)

        for ix in range(self.ui.tabWidgetRight.count()):
            if self.ui.tabWidgetRight.tabText(ix) == lightname:
                pm = None
                if self.ui.checkBoxDocView.isChecked():
                    try:
                        pm = docimage.doc_view().get_image().to_qimage(QPixmap)
                    except exceptions.General:
                        pass
                if not pm: pm = docimage.get_image().to_qimage(QPixmap)

                self.DrawImage(self.ui.tabWidgetRight.widget(ix), pm)

    @pyqtSlot()
    def slotCloseScan(self):
        try:
            if self.ScanCtrl: self.ScanCtrl.wait()
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)

        self.ScanCtrl = None
        self.ui.pushButtonStart.setEnabled(True)

# endregion

# region Analyzing
# ---------------------------------------------------------------------------- #

    @pyqtSlot()
    def slotAnalyze(self):
        ocrtask = task.EngineTask()

        if self.ui.listWidgetOCR.item(0).checkState() == Qt.Checked:
            ocrtask.add(FieldSource.Mrz, FieldId.All)
        if self.ui.listWidgetOCR.item(1).checkState() == Qt.Checked:
            ocrtask.add(FieldSource.Viz, FieldId.All)
        if self.ui.listWidgetOCR.item(2).checkState() == Qt.Checked:
            ocrtask.add(FieldSource.Barcode, FieldId.All)

        try:
            page = self.pr.scanner.get_page(0)
        except exceptions.General: return
        try:
            self.AnalyzeResult = self.pr.engine.analyze(page, ocrtask)
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)
            return

        self.FillOcrDataGrid()
        self.FillDataPage()

    def FillOcrDataGrid(self):
        fields = self.AnalyzeResult.list_fields()
        for ix in range(0,  len(fields)):
            try:
                field = self.AnalyzeResult.get_field(fields[ix])

                self.modelGrid.setItem(ix, 3, QStandardItem(str(ix)))
                fieldid = fields[ix].to_string(" ") + StrCon() + self.GetAmid(field)
                self.modelGrid.setItem(ix, 0, QStandardItem(fieldid))

                try:
                    value = u'\u202d' + field.get_best_string_value()
                except exceptions.InvalidParameter:
                    value = self.print_binary(field.get_binary_value(), 0, 16)
                except exceptions.General:
                    value = ""
                self.modelGrid.setItem(ix, 1, QStandardItem(value))

                self.modelGrid.setItem(ix, 2, QStandardItem(
                    processing.FieldStatus.compat_str(field.get_status())))
            except exceptions.General:
                pass

    def UpdateFieldDisplay(self):
        select = self.ui.tableViewGrid.selectionModel()
        if not select.hasSelection(): return

        self.ClearOCRData()

        ix = select.selection().indexes()[0].row()
        ix = int(self.modelGrid.data(self.modelGrid.index(ix, 3)))

        selectedfield = self.AnalyzeResult.list_fields()[ix]
        field = self.AnalyzeResult.get_field(selectedfield)
        try:
            self.ui.labelRAWValue.setText(u'\u202d' + field.get_raw_string_value())
        except exceptions.General:
            pass
        try:
            self.ui.labelFormattedValue.setText(field.get_formatted_string_value())
        except exceptions.General:
            pass
        try:
            self.ui.labelStandardizedValue.setText(field.get_standardized_string_value())
        except exceptions.General:
            pass
        try:
            pm = field.get_image().to_qimage(QPixmap)
            self.DrawImage(self.ui.labelFieldImagePicture, pm)
        except exceptions.General:
            pass

    def FillDataPage(self):
        name = self.GetFieldValue(FieldId.Surname)
        self.ui.labelTabNameValue.setText(name)
        if name:
            self.ui.labelTabNameValue.setText(name + " " + self.GetFieldValue(FieldId.Surname2))
            self.ui.labelTabNameValue2.setText(self.GetFieldValue(FieldId.Givenname)
                                  + StrCon() + self.GetFieldValue(FieldId.MiddleName))
        else:
            self.ui.labelTabNameValue.setText(self.GetFieldValue(FieldId.Name))

        self.ui.labelTabBirthValue.setText(StrCon("on") + self.GetFieldValue(FieldId.BirthDate)
                                         + StrCon("in") + self.GetFieldValue(FieldId.BirthPlace))

        self.ui.labelTabNationalityValue.setText(self.GetFieldValue(FieldId.Nationality))

        self.ui.labelTabSexValue.setText(self.GetFieldValue(FieldId.Sex))

        self.ui.labelTabIssuerValue.setText(self.GetFieldValue(FieldId.IssueCountry)
                               + StrCon() + self.GetFieldValue(FieldId.IssueState))

        self.ui.labelTabTypeValue.setText(self.GetFieldValue(FieldId.DocType)
                             + StrCon() + self.GetFieldValue(FieldId.DocTypeDisc))
        if not self.ui.labelTabTypeValue.text():
            self.ui.labelTabTypeValue.setText(self.GetFieldValue(FieldId.Type))

        self.ui.labelTabPageValue.setText(self.GetFieldValue(FieldId.DocPage))

        self.ui.labelTabNumberValue.setText(self.GetFieldValue(FieldId.DocumentNumber))

        self.ui.labelTabValidValue.setText(StrCon("from") + self.GetFieldValue(FieldId.IssueDate)
                                         + StrCon("to") + self.GetFieldValue(FieldId.ExpiryDate))

        try:
            pm = self.AnalyzeResult.get_field(FieldSource.Viz,
                                              FieldId.Face).get_image().to_qimage(QPixmap)
            self.DrawImage(self.ui.labelTabFacePhotoPic, pm)
        except exceptions.General:
            pass

        try:
            pm = self.AnalyzeResult.get_field(FieldSource.Viz,
                                              FieldId.Signature).get_image().to_qimage(QPixmap)
            self.DrawImage(self.ui.labelTabSignaturePic, pm)
        except exceptions.General:
            pass

# endregion

# region General tools
# ---------------------------------------------------------------------------- #

    def GetAmid(self, field: Field):
        try:
            return field.to_variant().get_child(util.VariantId.AMID, 0).to_string()
        except exceptions.General:
            return ""
        
    def GetFieldValue(self, idv: processing.FieldId):
        filt = FieldReference(FieldSource.All, idv)
        fields = self.AnalyzeResult.list_fields(filt)
        for field in fields:
            try:
                value = self.AnalyzeResult.get_field(field).get_best_string_value()
                if value:
                    return value
            except exceptions.EntryNotFound:
                pass
        return ""

    @staticmethod
    def print_binary(arr, pos, szv, split=True):
        """ Print a hexa dump line from a part of an array into a string.

        :param arr:     The whole array.
        :param pos:     Position of the first item to print.
        :param szv:     Number of items to print.
        :param split:   Put extra space character to middle of hex array and
                        between hex and ascii values.
        """
        str1, str2, epos = "", "", min(len(arr), pos+szv)
        for p0v in range(pos, epos):
            str1 += f"{arr[p0v] & 0xff:02x} "
            str2 += chr(arr[p0v]) if 0x21 <= arr[p0v] <= 0x7e else "."

        for p0v in range(epos, pos+szv):
            str1 += "   "
            str2 += " "
        if split:
            str1 = str1[:szv//2*3] + " " + str1[szv//2*3:] + " "
        return str1 + str2

    def AddTabPage(self, lightname):
        lb = QLabel()
        lb.setObjectName(lightname)
        lb.setFixedWidth(self.ui.tabWidgetRight.widget(0).width())
        lb.setFixedHeight(self.ui.tabWidgetRight.widget(0).height())
        lb.setStyleSheet("QLabel {background-color: black;}")
        self.ui.tabWidgetRight.addTab(lb, lightname)

    def DrawImage(self, lbl, pm):
        lbl.setPixmap(pm.scaled(lbl.width(), lbl.height(), Qt.KeepAspectRatio))

    def ClearOCRData(self):
        self.ui.labelFieldImagePicture.clear()
        self.ui.labelRAWValue.setText("")
        self.ui.labelFormattedValue.setText("")
        self.ui.labelStandardizedValue.setText("")

    def ClearDataPage(self):
        self.ui.labelTabNameValue.setText("")
        self.ui.labelTabNameValue2.setText("")
        self.ui.labelTabBirthValue.setText("")
        self.ui.labelTabNationalityValue.setText("")
        self.ui.labelTabSexValue.setText("")
        self.ui.labelTabIssuerValue.setText("")
        self.ui.labelTabTypeValue.setText("")
        self.ui.labelTabPageValue.setText("")
        self.ui.labelTabNumberValue.setText("")
        self.ui.labelTabValidValue.setText("")
        self.ui.labelTabSignaturePic.clear()
        self.ui.labelTabFacePhotoPic.clear()

    def RemoveTabs(self):
        for ix in range(self.ui.tabWidgetRight.count()-1, 1, -1):
            label = self.ui.tabWidgetRight.widget(ix)
            self.ui.tabWidgetRight.removeTab(ix)
            label.clear()
            del label

    def RemoveGridRows(self):
        self.ui.tableViewGrid.model().removeRows(0, self.ui.tableViewGrid.model().rowCount())

    @pyqtSlot(QModelIndex)
    def on_tableViewGrid_clicked(self, index):
        self.UpdateFieldDisplay()

    def eventFilter(self, obj, ev):
        if obj == self.ui.tableViewGrid and (ev.type() == QEvent.KeyRelease):
            self.UpdateFieldDisplay()

        return super().eventFilter(obj, ev)

# endregion

    pass
