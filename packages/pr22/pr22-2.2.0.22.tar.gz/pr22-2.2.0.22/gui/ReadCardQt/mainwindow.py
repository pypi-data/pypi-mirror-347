# -*- coding: utf-8 -*-

from os import path, listdir
from fnmatch import fnmatch

from PyQt5.QtCore import QObject, pyqtSignal, Qt, QSettings, QStringListModel, QPoint, pyqtSlot, QTimer
from PyQt5.QtGui import QColor, QCursor,  QPixmap
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox, QMenu
from PyQt5.QtWidgets import QApplication,  QFileDialog

from ui_mainwindow import Ui_MainWindow

from pr22 import ecardhandling, exceptions, task, imaging
from pr22.processing import BinData, FieldReference, FieldSource, FieldId, Document
from pr22 import DocumentReaderDevice, Event
from pr22.ecardhandling import AuthProcess
import pr22

Black  = "black"
Red    = "red"
Green  = "green"
Yellow = "yellow"


class EventHandler(QObject):

    Connection       = pyqtSignal(list)
    AuthBegin        = pyqtSignal(ecardhandling.AuthProcess)
    AuthFinished     = pyqtSignal(tuple)
    AuthWaitForInput = pyqtSignal(ecardhandling.AuthProcess)
    ReadBegin        = pyqtSignal(ecardhandling.File)
    ReadFinished     = pyqtSignal(ecardhandling.File, exceptions.ErrorCodes)
    FileChecked      = pyqtSignal(ecardhandling.File, exceptions.ErrorCodes)

    def __init__(self, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)

    def register_events(self, dr_dev: DocumentReaderDevice):
        dr_dev.add_event_handler(Event.Connection, self.on_connection)
        dr_dev.add_event_handler(Event.AuthBegin, self.on_auth_begin)
        dr_dev.add_event_handler(Event.AuthFinished, self.on_auth_finished)
        dr_dev.add_event_handler(Event.AuthWaitForInput, self.on_auth_wait_for_input)
        dr_dev.add_event_handler(Event.ReadBegin, self.on_read_begin)
        dr_dev.add_event_handler(Event.ReadFinished, self.on_read_finished)
        dr_dev.add_event_handler(Event.FileChecked, self.on_file_checked)

    def on_connection(self, device, dr_dev):
        # This raises only when no device is used or when the currently
        # used device is disconnected.
        devlist = dr_dev.list_devices(dr_dev)
        self.Connection.emit(devlist)

    def on_auth_begin(self, authentication, dr_dev):
        self.AuthBegin.emit(authentication)

    def on_auth_finished(self, authentication, status, dr_dev):
        self.AuthFinished.emit((authentication, status))

    def on_auth_wait_for_input(self, authentication, dr_dev):
        self.AuthWaitForInput.emit(authentication)

    def on_read_begin(self, file, dr_dev):
        self.ReadBegin.emit(file)

    def on_read_finished(self, file, status, dr_dev):
        self.ReadFinished.emit(file, status)

    def on_file_checked(self, file, status, dr_dev):
        self.FileChecked.emit(file, status)

# ---------------------------------------------------------------------------- #


class MainWindow(QMainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        try:
            self.pr = DocumentReaderDevice()
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)
            exit(1)

        evh = EventHandler()

        evh.Connection.connect(self.slotGetDeviceModel)
        evh.AuthBegin.connect(self.slotAuthBegin)
        evh.AuthFinished.connect(self.slotAuthFinished)
        evh.AuthWaitForInput.connect(self.slotAuthWaitForInput)
        evh.ReadBegin.connect(self.slotReadBegin)
        evh.ReadFinished.connect(self.slotReadFinished)
        evh.FileChecked.connect(self.slotFileChecked)

        evh.register_events(self.pr)

        for fid in ecardhandling.FileId:
            qstr = fid.name
            item = QListWidgetItem(qstr, self.ui.listWidgetFiles)
            item.setFlags(item.flags() or Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

        for fid in ecardhandling.AuthLevel:
            self.ui.comboBoxAuthSel.addItem(fid.name)

        self.ui.comboBoxAuthSel.setCurrentIndex(1)
        self.card = None

        self.ui.listWidgetFiles.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listModel = None
        self.faceDoc   = None
        self.readCtrl  = None
        self.DeviceIsConnected = False
        self.vizResult = None

        QTimer.singleShot(100, self.formLoadEvent)

    def formLoadEvent(self):
        self.ui.textEditMsgs.setText("Loading certificates...")
        QApplication.processEvents()
        self.ui.textEditMsgs.clear()
        self.setCursor(Qt.WaitCursor)
        settings = QSettings("ReadCard.config", QSettings.IniFormat)
        self.load_certificates(settings.value("CertDir", ""))
        self.setCursor(Qt.ArrowCursor)

    def closeEvent(self, event):
        if self.readCtrl:
            self.readCtrl.stop().wait()
            QApplication.processEvents()
        if self.DeviceIsConnected:
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
        item  = index.data(Qt.DisplayRole)

        if not item: return

        self.ui.pushButtonConnect.setEnabled(False)
        self.ui.pushButtonConnect.repaint()
        self.setCursor(Qt.WaitCursor)
        try:
            self.pr.use_device(item)

            self.DeviceIsConnected = True
            self.ui.pushButtonDisconnect.setEnabled(True)
            for reader in self.pr.readers:
                hwt = reader.info.hw_type
                item = QListWidgetItem(hwt.name, self.ui.listWidgetReaders)
                item.setFlags(item.flags() or Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
            self.ui.pushButtonRead.setEnabled(True)

        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)
            self.on_pushButtonDisconnect_clicked()
        self.setCursor(Qt.ArrowCursor)

    @pyqtSlot()
    def on_pushButtonDisconnect_clicked(self):
        if self.DeviceIsConnected:
            if self.readCtrl:
                self.readCtrl.stop().wait()
                self.readCtrl = None
                QApplication.processEvents()
            if self.card:
                self.card.disconnect()
                self.card = None
            self.pr.close_device()
            self.DeviceIsConnected = False
        self.ui.pushButtonConnect.setEnabled(True)
        self.ui.pushButtonDisconnect.setEnabled(False)
        self.ui.pushButtonRead.setEnabled(False)
        self.ui.listWidgetReaders.clear()
        self.ui.textEditMsgs.setText("")

# endregion

# region Reading
# ---------------------------------------------------------------------------- #

    @pyqtSlot()
    def on_pushButtonRead_clicked(self):
        self.ui.textEditMsgs.setText("")
        self.ClearControls()

        if self.readCtrl:
            self.readCtrl.wait()
            self.readCtrl = None
        if self.card:
            try:
                self.card.disconnect()
            except exceptions.General:
                pass
            self.card = None

        cardreader = None
        for cnt in range(self.ui.listWidgetReaders.count()):
            item = self.ui.listWidgetReaders.item(cnt)
            if item.checkState() == Qt.Checked:
                reader = self.pr.readers[cnt]
                try:
                    if reader.list_cards():
                        self.card = reader.connect_card(0)
                        cardreader = reader
                        break
                except exceptions.General as ex:
                    QMessageBox.critical(self, "Error", ex.message)

        if cardreader and self.card:
            self.StartRead(cardreader)

    def StartRead(self, cardreader: pr22.ECardReader):
        self.ClearControls()
        self.ui.pushButtonRead.setEnabled(False)

        self.ui.textEditMsgs.append("Scanning")
        self.ui.textEditMsgs.repaint()
        scantask = task.DocScannerTask()
        scantask.add(imaging.Light.Infra).add(imaging.Light.White)

        try:
            page = self.pr.scanner.scan(scantask, imaging.PagePosition.First)
        except exceptions.General:
            page = None

        self.ui.textEditMsgs.append("Analyzing")
        self.ui.textEditMsgs.repaint()
        enginetask = task.EngineTask()
        enginetask.add(FieldSource.Mrz, FieldId.All)
        enginetask.add(FieldSource.Viz, FieldId.CAN)

        facefieldid = FieldReference(FieldSource.Viz, FieldId.Face)
        enginetask.add(facefieldid)
        signaturefieldid = FieldReference(FieldSource.Viz, FieldId.Signature)
        enginetask.add(signaturefieldid)

        try:
            self.vizResult = self.pr.engine.analyze(page, enginetask)
        except exceptions.General:
            pass
        self.faceDoc = None

        try:
            self.DrawImage(self.ui.labelFacesPic2, self.vizResult.get_field(
                facefieldid).get_image().to_qimage(QPixmap))
        except exceptions.General:
            pass
        try:
            self.DrawImage(self.ui.labelSignPic2, self.vizResult.get_field(
                signaturefieldid).get_image().to_qimage(QPixmap))
        except exceptions.General:
            pass

        cardtask = task.ECardTask()
        cardtask.authlevel = ecardhandling.AuthLevel[self.ui.comboBoxAuthSel.currentText()]

        for cnt in range(self.ui.listWidgetFiles.count()):
            item = self.ui.listWidgetFiles.item(cnt)
            if item.checkState() == Qt.Checked:
                cardtask.add(ecardhandling.File(ecardhandling.FileId[item.text()]))

        try:
            self.readCtrl = cardreader.start_read(self.card, cardtask)
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)

    @pyqtSlot(ecardhandling.AuthProcess)
    def slotAuthBegin(self, authentication):
        self.ui.textEditMsgs.append(f"Auth Begin: {authentication}")
        self.ColorAuthLabel(authentication, Yellow)

    @pyqtSlot(tuple)
    def slotAuthFinished(self, args):
        # authentication: ecardhandling.AuthProcess, status: exceptions.ErrorCodes
        authentication = args[0]
        status         = args[1]
        errstr = str(status) if isinstance(status, exceptions.ErrorCodes) else f"{status:04x}"

        self.ui.textEditMsgs.append(f"Auth Done: {authentication} status: {errstr}")
        ok = status == exceptions.ErrorCodes.NoErr
        self.ColorAuthLabel(authentication, Green if ok else Red)

    @pyqtSlot(ecardhandling.AuthProcess)
    def slotAuthWaitForInput(self, authentication: ecardhandling.AuthProcess):
        try:
            self.ui.textEditMsgs.append(f"Auth Wait For Input: {authentication}")
            self.ColorAuthLabel(authentication, Yellow)

            authdata = BinData()
            selector = 0

            if authentication in [AuthProcess.BAC, AuthProcess.PACE, AuthProcess.BAP]:
                fr = FieldReference(FieldSource.Mrz, FieldId.All)
                authfields = self.vizResult.list_fields(fr)
                selector = 1
                if not authfields:
                    fr = FieldReference(FieldSource.Viz, FieldId.CAN)
                    authfields = self.vizResult.list_fields(fr)
                    selector = 2
                if authfields:
                    authdata.set_string(self.vizResult.get_field(fr).get_best_string_value())
            else:
                pass

            self.card.authenticate(authentication, authdata, selector)
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)

    @pyqtSlot(ecardhandling.File)
    def slotReadBegin(self, file):
        self.ui.textEditMsgs.append(f"Read Begin: {file}")

    @pyqtSlot(ecardhandling.File, exceptions.ErrorCodes)
    def slotReadFinished(self, file: ecardhandling.File, status: exceptions.ErrorCodes):
        errstr = str(status) if isinstance(status, exceptions.ErrorCodes) else f"{status:04x}"

        self.ui.textEditMsgs.append(f"Read End: {file} result: {errstr}")

        if file.id_v == ecardhandling.FileId.All:
            self.ProcessAfterAllRead()
            self.ui.pushButtonRead.setEnabled(True)
        elif status != exceptions.ErrorCodes.NoErr:
            self.ColorFileName(file, Red)
        else:
            self.ColorFileName(file, "blue")
            self.ProcessAfterFileRead(file)

    def ProcessAfterAllRead(self):
        try:
            mrz = self.vizResult.get_field(FieldSource.Mrz, FieldId.All).get_raw_string_value()
            dg1 = self.ui.textEditMrz.toPlainText()
            if len(dg1) > 40:
                self.ColorLabel(self.ui.labelMrz, (Green if mrz == dg1 else Red))
        except exceptions.General:
            pass
        try:
            facecmp = self.vizResult + self.faceDoc
            fcl = facecmp.get_field_compare_list()
            for item in fcl:
                if item.field1.id_v == FieldId.Face and item.field2.id_v == FieldId.Face:
                    col = Yellow
                    if item.confidence < 300: col = Red
                    elif item.confidence > 600: col = Green
                    self.ColorLabel(self.ui.labelFace, col)
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)

    def ProcessAfterFileRead(self, file: ecardhandling.File):
        try:
            rawfilecontent   = self.card.get_file(file)
            filedoc          = self.pr.engine.analyze(rawfilecontent)

            facefieldid      = FieldReference(FieldSource.ECard, FieldId.Face)
            mrzfieldid       = FieldReference(FieldSource.ECard, FieldId.CompositeMrz)
            signaturefieldid = FieldReference(FieldSource.ECard, FieldId.Signature)
            fingerfieldid    = FieldReference(FieldSource.ECard, FieldId.Fingerprint)

            if filedoc.list_fields(facefieldid):
                self.faceDoc = filedoc
                self.DrawImage(self.ui.labelFacesPic1, filedoc.get_field(
                    facefieldid).get_image().to_qimage(QPixmap))
            if filedoc.list_fields(mrzfieldid):
                mrz = filedoc.get_field(mrzfieldid).get_raw_string_value()
                if len(mrz) == 90:
                    mrz = mrz[:30] + '\n' + mrz[30:60] + '\n' + mrz[60:]
                elif len(mrz) > 50:
                    mrz = mrz[:mrz.length() / 2] + '\n' + mrz[mrz.length() / 2:]
                self.ui.textEditMrz.setAlignment(Qt.AlignCenter)
                self.ui.textEditMrz.append(mrz)
            if filedoc.list_fields(signaturefieldid):
                try:
                    self.DrawImage(self.ui.labelSignPic1, filedoc.get_field(
                        signaturefieldid).get_image().to_qimage(QPixmap))
                except exceptions.General:
                    pass
            if filedoc.list_fields(fingerfieldid):
                try:
                    self.DrawImage(self.ui.labelFingerprintsPic1, filedoc.get_field(
                        FieldSource.ECard, FieldId.Fingerprint, 0).get_image().to_qimage(QPixmap))
                    self.DrawImage(self.ui.labelFingerprintsPic2, filedoc.get_field(
                        FieldSource.ECard, FieldId.Fingerprint, 1).get_image().to_qimage(QPixmap))
                except exceptions.General:
                    pass
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)

    @pyqtSlot(ecardhandling.File, exceptions.ErrorCodes)
    def slotFileChecked(self, file: ecardhandling.File, status: exceptions.ErrorCodes):
        self.ui.textEditMsgs.append(f"File Checked: {file}")
        ok = status == exceptions.ErrorCodes.NoErr
        self.ColorFileName(file, Green if ok else Yellow)

# endregion

# region General tools
# ---------------------------------------------------------------------------- #

    def ColorFileName(self, file: ecardhandling.File, color):
        hdrnam = self.ui.listWidgetFiles.findItems(str(file), Qt.MatchFixedString)
        if not list:
            try:
                file = self.card.convertFileId(file)
            except exceptions.General:
                pass
            hdrnam = self.ui.listWidgetFiles.findItems(str(file), Qt.MatchFixedString)
        if hdrnam:
            hdrnam[0].setForeground(QColor(color))

    @pyqtSlot(QPoint)
    def on_listWidgetFiles_customContextMenuRequested(self, pos):
        lwi = self.ui.listWidgetFiles.itemAt(pos)
        lwi.setSelected(True)

        fgcolor = lwi.foreground().color()
        if fgcolor not in [QColor(Black), QColor(Red)] and fgcolor.isValid():
            menu = QMenu()
            menu.addAction("Save")
            action = menu.exec(QCursor.pos())
            if action:
                self.SaveFile(lwi.text())

    def SaveFile(self, text):
        if not self.card: return

        file = ecardhandling.FileId.parse(text)
        try:
            filename = QFileDialog.getSaveFileName(self, "Save", text, "XML files (*.xml);;Binary files (*.bin)")
            if len(filename[0]) > 0:
                filedata = self.card.get_file(file)
                if filename[0].lower().endswith(".bin"):
                    filedata.save(filename[0])
                elif filename[0].lower().endswith(".xml"):
                    self.pr.engine.analyze(filedata).save(Document.FileFormat.Xml).save(filename[0])
        except exceptions.General as ex:
            QMessageBox.critical(self, "Error", ex.message)

    def list_files(self, directory, mask):
        files = []
        if not path.isdir(directory): return []
        for fname in listdir(directory):
            fpath = directory + path.sep + fname
            if path.isdir(fpath):
                files.extend(self.list_files(fpath, mask))
            elif fnmatch(fname, mask):
                files.append(fpath)

        return files

    def load_certificates(self, dirpath):
        """ Load certificates from a directory. """
        cnt = 0
        for ext in ["*.cer", "*.crt", "*.der", "*.pem", "*.crl", "*.cvcert", "*.ldif", "*.ml"]:
            for file_name in self.list_files(dirpath, ext):
                try:
                    priv = BinData()
                    if ext == "*.cvcert":
                        # Searching for private key
                        pknam = file_name[:file_name.rfind(".")+1] + "pkcs8"
                        if path.isfile(pknam): priv.load(pknam)
                    self.pr.global_certificate_manager.load(BinData().load(file_name), priv)
                    cnt += 1
                except exceptions.General as ex:
                    self.ui.textEditMsgs.append(f"Error at loading {file_name} : {ex.message}")
        self.ui.textEditMsgs.append(f"{str(cnt) if cnt > 0 else 'No'} certificate"
                                    f"{'' if cnt == 1 else 's'} loaded from '{dirpath}'")

# endregion

# region Display
# ---------------------------------------------------------------------------- #

    def ColorAuthLabel(self, auth: ecardhandling.AuthProcess, color):
        if    auth == AuthProcess.BAC or \
              auth == AuthProcess.BAP: label = self.ui.labelBac
        elif  auth == AuthProcess.PACE: label = self.ui.labelPace
        elif  auth == AuthProcess.Chip: label = self.ui.labelCa
        elif  auth == AuthProcess.Terminal: label = self.ui.labelTa
        elif  auth == AuthProcess.Passive: label = self.ui.labelPa
        elif  auth == AuthProcess.Active: label = self.ui.labelTa
        else: return
        self.ColorLabel(label, color)

    def ColorLabel(self, label, color):
        label.setStyleSheet("QLabel {color: %s;}" % color)

    def DrawImage(self, lbl, pm):
        lbl.setPixmap(pm.scaled(lbl.width(), lbl.height(), Qt.KeepAspectRatio))

    def ClearControls(self):
        self.ui.textEditMrz.setText('')
        self.ui.labelFacesPic1.clear()
        self.ui.labelFacesPic2.clear()
        self.ui.labelSignPic1.clear()
        self.ui.labelSignPic2.clear()
        self.ui.labelFingerprintsPic1.clear()
        self.ui.labelFingerprintsPic2.clear()

        self.ColorLabel(self.ui.labelBac, Black)
        self.ColorLabel(self.ui.labelPace, Black)
        self.ColorLabel(self.ui.labelCa, Black)
        self.ColorLabel(self.ui.labelTa, Black)
        self.ColorLabel(self.ui.labelPa, Black)
        self.ColorLabel(self.ui.labelAa, Black)
        self.ColorLabel(self.ui.labelMrz, Black)
        self.ColorLabel(self.ui.labelFace, Black)

        for item in self.ui.listWidgetFiles.items(None):
            item.setTextColor(Qt.black)

        self.ui.listWidgetFiles.repaint()

# endregion

    pass
