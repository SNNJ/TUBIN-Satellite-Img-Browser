import shutil

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import folium
from Cgmap import Secondwindow
# import pandas as pd
from Cdbfilter import Cdb
from CtubCloud import downloader
from CimgResize import CimgResize

from folium.plugins import MarkerCluster

import urllib

def fnotConnected(host='http://google.com'):
    try:
        urllib.request.urlopen(host, timeout=1)
        return False
    except:
        return True




# db = pd.read_excel('./appdata/tuBinMetaData.xlsx')

ui, _ = loadUiType('TuFinal.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        # self.Show_ImageName()
        self.db = Cdb()
        self.cloud = downloader()
        self.Imgresize = CimgResize()
        self.currentImg = ''
        self.lastSavedImg = {"fileAdrr":self.currentImg, "lat":'', "lon":''}


        layout = QVBoxLayout()
        layout.addWidget(self.mapgen())
        self.ssmap.setLayout(layout)

    def Handle_UI_Change(self):
        pass
    def Handle_Buttons(self):
        # print("success")
        self.sfilter.clicked.connect(self.fsfilter)
        self.smap.clicked.connect(self.fsmap)
        self.slookmax.sliderReleased.connect(self.fsetminSlook)
        self.slookmin.sliderReleased.connect(self.fsetmaxSlook)

        self.snofilter.toggled.connect(self.fsnofilter)
        self.sfire.toggled.connect(self.fsfire)
        self.sspace.toggled.connect(self.fsspace)
        self.smoon.toggled.connect(self.fsmoon)
        self.stable.cellClicked.connect(self.fselectedImg)
        self.sBdwn.clicked.connect(self.fsBdwn)
        self.sBsrt.clicked.connect(self.fsBsrt)
        self.sBdel.clicked.connect(self.fsBdel)
        self.actionQuit.triggered.connect(lambda : QApplication.quit())
        self.actionAbout.triggered.connect(lambda : self.faboutPopup())

    def faboutPopup(self):
        msg = QMessageBox()
        msg.setText("TuBin Catalog v 0.1\n \nThis application is developed within a short period of time in the secend half of WS 22/23 by User Segment team.\n"
                    "Developers believe that enhanced user interface with TuBin Data plays an important role in algorithm development and \n"
                    "educational performance and hopefully this effort shall evolve into more enahced and capable by gradual contribution of students.\n"
                    "----\n"
                    "Tanishqa JK : www.linkedin.com/in/tanishqa-jk\n"
                    "Penghuy S. : www.linkedin.com/in/penghuy-srean\n"
                    "Aleksandar Minic \n"
                    "Siamak NJ : www.linkedin.com/in/siamak-nj-438b05137\n")
        #msg.informativeText()

        x= msg.exec_()
    def fsBdel(self):
        import os
        import shutil

        for root, dirs, files in os.walk('./temp'):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


    def fsBdwn(self):

        nrow = self.stable.rowCount()
        print(nrow)

        if fnotConnected():
            self.statusBar().showMessage("Connection to Internet error, Check internet connectivity", 3000)
            return


        if nrow > 1:
            if self.sCdwn.currentText() == "All":
                self.stable.selectAll()
            rows = []
            for idx in self.stable.selectedIndexes():
                rows.append(idx.row())

            if nrow-1 in rows:
                rows.remove(nrow - 1)

            rows = self.db.fdb.imgFileAddr.iloc[rows].to_list()
            self.cloud.flinks(rows)
            print(rows)



        print(self.sCdwn.currentText())

    def fsBsrt(self):
        pass
        namePairs = {'Name': 'imgFileAddr', 'Camera': 'camera', 'Look angle':'lookAngle',  'Sun elevation': 'sunElv', 'Local time':'localTime', 'Geo. distance':'ldist'}
        selSort = self.sCsrt.currentText()
        if selSort in namePairs:
            if namePairs[selSort] in self.db.fdb.columns and self.db.fdb.shape[0] > 0:
                self.db.fdb.sort_values(by = [namePairs[selSort]], inplace=True)
                self.Show_ImageName()
            else:
                print('either zero rows or the name is not there yet')
        else:
            print('the name is entered incorrectly')

    def fselectedImg(self,row, col):

        print("ROw is %d and the col is %d "%(row, col))
        if self.db.fdb.shape[0] >0:
            # print(self.db.fdb.imgFileAddr.iloc[row])
            # self.textMeta.setText(self.db.fdb.iloc[row].to_json())
            self.textMeta.setText(self.db.fdb.iloc[row].to_string())
            try:
                savedfile = self.cloud.flink(self.db.fdb.imgFileAddr.iloc[row])
                pixmap = QPixmap(savedfile).scaled(self.ssat.width(), self.ssat.height(),
                                                   aspectRatioMode=Qt.KeepAspectRatio,
                                                   transformMode=Qt.SmoothTransformation)
                self.ssat.setPixmap(pixmap)
                # self.Imgresize.fimgResize(savedfile)
                self.currentImg = savedfile
                self.lastSavedImg = {"fileAddr": self.currentImg, "lat": '' if self.db.fdb.isnull().siteLat.iloc[row] else self.db.fdb.siteLat.iloc[row]
                    , "lon": '' if self.db.fdb.isnull().siteLon.iloc[row] else self.db.fdb.siteLon.iloc[row]}
            except:
                self.statusBar().showMessage("File cannot be downloaded or drawn, Check Internet connection or Temp Folder", 3000)
        # pixmap.scaled(640,480)
        # pixmap.scaled(640, 480, Qt.KeepAspectRatio)

        # self.ssat.setPixmap(QPixmap('modified.png'))
        # rows = []
        # print(self.stable.selectedIndexes())
        # for idx in self.stable.selectedIndexes():
        #     rows.append(idx.row())
        # print(rows)
        # pass

    def fsmoon(self):
        if self.smoon.isChecked():
            self.swater.setEnabled(False)
            self.scloud.setEnabled(False)
            self.sfire.setEnabled(False)
        elif not self.sspace.isChecked():
            self.swater.setEnabled(True)
            self.scloud.setEnabled(True)
            self.sfire.setEnabled(True)

    def fsspace(self):
        if self.sspace.isChecked():
            self.sfire.setEnabled(False)
        elif not self.smoon.isChecked():
            self.sfire.setEnabled(True)

    def fsfire(self):
        # print("sdfd")
        if self.sfire.isChecked():
            self.sspace.setEnabled(False)
            # print("1")
            # print("1")
        elif not self.snofilter.isChecked():
            self.sspace.setEnabled(True)
    def fsnofilter(self):

        # if self.snofilter.isChecked():
        #     print("inside the loop that is chcked")
        # else:
        #     print("not checked")
        if self.sfire.isChecked():
            if self.snofilter.isChecked():
                # self.sspace.setEnabled(False)
                self.srad.setEnabled(False)
            else:
                # self.sspace.setEnabled(True)
                self.srad.setEnabled(True)
        else:

            if self.sspace.isChecked():
                # print("I am here")
                self.sspace.click()
                if self.smoon.isChecked():
                    self.scloud.setEnabled(False)
                    self.swater.setEnabled(False)
                    self.sfire.setEnabled(False)

            if self.snofilter.isChecked():
                self.sspace.setEnabled(False)
                self.srad.setEnabled(False)
            else:
                self.sspace.setEnabled(True)
                self.srad.setEnabled(True)




    def fsetmaxSlook(self):
        temp = self.slookmin.value()
        if self.slookmax.value() < temp:
            self.slookmax.setValue(temp + 2)

    def fsetminSlook(self):
        temp = self.slookmax.value()
        if temp <= 2:
            self.slookmin.setValue(0)
        elif self.slookmin.value() > temp:
            self.slookmin.setValue(temp-2)


    def fsfilter(self):

        # making filtered data equlas to all available db
        self.db.fdb = self.db.db

        # condition = {'type':'query', 'colName':'scloud', 'query':'%s == 3'}
        # condition = {'type':'query', 'colName':'smoon', 'query':'%s == 0'}
        # condition = {'type':'query', 'colName':'smoon', 'query':'%s == 0'}

        # condition = {'type':'query', 'colName':'stime', 'query':' 2< %s <= 5 '}

        ## Scene Center
        slon =self.slon.value()
        slat = self.slat.value()
        srad = self.srad.value()
        sspace = self.sspace.isChecked()
        snofilter = self.snofilter.isChecked()

        ## filterin for scene center
        if self.srad.isEnabled():
            condition = {'type': 'dist', 'sceneLoc': [slat, slon], 'query': ' < %s '%srad}
            self.db.fdbfilter(condition)
            print("the function for scene center")
        if self.sspace.isChecked():
            condition = {'type':'query', 'colName':'sspace', 'query':'%s.isnull()'}
            self.db.fdbfilter(condition)
            print(" function for sspace ")
            print(self.db.fdb.shape)

        #Image Content
        squality = self.squality.isChecked()
        squalityval = self.squalityval.value()
        scloud = self.scloud.isChecked()
        scloudval = self.scloudval.value()
        swater = self.swater.isChecked()
        swaterval = self.swaterval.value()
        smoon = self.smoon.isChecked()
        sfire = self.sfire.isChecked()


        ## filtering for image content
        if self.squality.isEnabled() and self.squality.isChecked() :
            condition = {'type': 'query', 'colName': 'squality', 'query': '%s == ' + str(squalityval)}
            self.db.fdbfilter(condition)
            # print(condition)
        if self.scloud.isEnabled() and self.scloud.isChecked() :
            condition = {'type': 'query', 'colName': 'scloud', 'query': '%s == ' + str(scloudval)}
            self.db.fdbfilter(condition)
        if self.swater.isEnabled() and self.swater.isChecked() :
            condition = {'type': 'query', 'colName': 'swater', 'query': '%s == ' + str(swaterval)}
            self.db.fdbfilter(condition)
        if self.smoon.isEnabled() and self.smoon.isChecked() :
            # condition = {'type': 'query', 'colName': 'smoon', 'query': '%s == 1'}
            condition = {'type': 'query', 'colName': 'smoon', 'query': '0 < %s <0.4'}
            self.db.fdbfilter(condition)
        if self.sfire.isEnabled() and self.sfire.isChecked() :
            condition = {'type': 'query', 'colName': 'sfire', 'query': '%s == 1'}
            self.db.fdbfilter(condition)

        # #Image Environment
        snight = self.snight.isChecked()
        stime = self.stime.isChecked()
        stimemin = self.stimemin.value()
        stimemax = self.stimemax.value()
        ssun = self.ssun.isChecked()
        ssunmin = self.ssunmin.value()
        ssunmax = self.ssunmax.value()
        ## the filtering goes here

        if self.snight.isChecked() :
            condition = {'type': 'query', 'colName': 'snight', 'query': '%s == "night"'}
            self.db.fdbfilter(condition)
        if self.stime.isChecked():
            condition = {'type': 'query', 'colName': 'stime', 'query': str(stimemin) + ' <= %s <= ' + str(stimemax)}
            self.db.fdbfilter(condition)
        if self.ssun.isChecked():
            condition = {'type': 'query', 'colName': 'stime', 'query': str(ssunmin) + ' <= %s <= ' + str(ssunmax)}
            self.db.fdbfilter(condition)


        # #Sensor Parameter
        sir = self.sir.isChecked()
        svis = self.svis.isChecked()
        slook = self.slook.isChecked()
        slookmin = self.slookmin.value()
        slookmax = self.slookmax.value()

        # The filtering goes here
        if self.sir.isChecked() and self.svis.isChecked():
            condition = {'type': 'query', 'colName': 'sir', 'query': '%s in ("IR1","IR2","VIS")'}
            self.db.fdbfilter(condition)
        elif self.sir.isChecked():
            condition = {'type': 'query', 'colName': 'sir', 'query': '%s in ("IR1","IR2")'}
            self.db.fdbfilter(condition)
        elif self.svis.isChecked():
            condition = {'type': 'query', 'colName': 'svis', 'query': '%s in ("VIS")'}
            self.db.fdbfilter(condition)
        if self.slook.isChecked():
            condition = {'type': 'query', 'colName': 'slook', 'query': str(slookmin / 180) + ' <= %s <= ' + str(slookmax / 180)}
            self.db.fdbfilter(condition)
        ## Filtering logic

        self.Show_ImageName()

        # print(stimemax,stimemin,ssun,ssunmax,ssunmin,sir,svis)
        # # self.ssat.setPixmap(QPixmap('modified.png'))
        # print(snight,stime)
        # print(slong,slat,srad)

    def Show_ImageName(self):
        self.stable.setRowCount(0)
        nrows = self.db.fdb.shape[0]
        self.statusBar().showMessage("Filtering returned " + str(nrows) + " results", 5000)

        if nrows > 0:
            self.tabWidget.setCurrentIndex(1)
            # x=list(range(1,100))
            self.stable.insertRow(0)
            self.stable.setItem(0,0,QTableWidgetItem("first"))

            for row,val in enumerate(range(nrows)):
                self.stable.setItem(row, 0, QTableWidgetItem(self.db.fdb.imgName_y.iloc[row]))
                row_position = self.stable.rowCount()
                self.stable.insertRow(row_position)


    def fsmap(self):
        # # Secondwindow()
        # self.window = Secondwindow()
        # self.window.show()
        # pass ./temp/TUBIN_VIS_20210709_125900_692_2.png
        try:
            self.Imgresize.fimgResize(self.currentImg)
            self.lastSavedImg["fileAddr"] = "./temp/"+"img4map"+self.currentImg.split('/')[-1]
        except:
            self.statusBar().showMessage("Problem converting image for map", 1000)
            return

        if fnotConnected():
            self.statusBar().showMessage("Connection to Internet error, Check internet connectivity", 3000)
            return

        if isinstance(self.lastSavedImg["lat"], (int, float)) and isinstance(self.lastSavedImg["lon"], (int, float)):
            self.window = Secondwindow(self.lastSavedImg)
            self.window.show()
        else:
            self.statusBar().showMessage("the image has no long & lat", 1000)

    def mapgen(self):
        import io
        from PyQt5 import QtWebEngineWidgets, QtWidgets

        listSparseImg = Cdb()
        condition = {'type': 'sparse'}
        listSparseImg.fdbfilter(condition)
        points = listSparseImg.fdb[['siteLat','siteLon']].to_numpy().tolist()

        m = folium.Map(location=[33.7, 53.61], zoom_start=5, tiles="Stamen Terrain")
        MarkerCluster(points).add_to(m)
        m.add_child(folium.LatLngPopup())
        data = io.BytesIO()
        m.save(data, close_file=False)

        w = QtWebEngineWidgets.QWebEngineView()
        w.setHtml(data.getvalue().decode())
        w.resize(800, 600)
        return w
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ =="__main__":
    main()





