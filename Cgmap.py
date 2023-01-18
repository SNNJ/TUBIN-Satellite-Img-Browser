import shutil
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtWebEngineWidgets, QtWidgets
import folium
import io
import os
import ee
from PIL import Image
from folium import plugins


class CfoliumMap(folium.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.currentImg=imgaddr
        # self.lat, self.lon = 45.77, 4.855

    def add_ee_layer(self, ee_image_object, vis_params, name):
        """Adds a method for displaying Earth Engine image tiles to folium map."""
        map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
        folium.raster_layers.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
            name=name,
            overlay=True,
            control=True
        ).add_to(self)



class Secondwindow(QMainWindow):

    def __init__(self, img4map):
        super(Secondwindow, self).__init__()
        self.img4map =img4map
        # print(img4map)
        # print("the vlaue of lat is valid ? %s"% isinstance(self.img4map["lat"], (int, float)))
        self.setWindowTitle("Layered view (Map + Google Image collection)")
        # self.lat, self.lon = lat , lon

        layout = QVBoxLayout()

        # layout.addWidget(Color('red'))

        # layout.addWidget(self.mapgen())
        layout.addWidget(self.gmap())

        widget = QWidget()
        widget.setLayout(layout)
        # widget = Color('blue')

        self.setCentralWidget(widget)
        # self.gmap()


    def gmap(self):

        # Create a map.
        lat, lon = self.img4map['lat'], self.img4map['lon']
        m = CfoliumMap(location=[lat, lon], zoom_start=3, tiles="Stamen Terrain")

        try:
            keydata = "Here private key data must be inserted"
            
            service_account = "tubin-cloud-test@gifted-object-368314.iam.gserviceaccount.com"
            # credentials = ee.ServiceAccountCredentials(service_account, 'key.json')
            credentials = ee.ServiceAccountCredentials(service_account, key_data=keydata)
            ee.Initialize(credentials)
            googleMapFalse = True
        except:
            print("either authentication or internet conecction error")
            googleMapFalse = False

        if googleMapFalse :
            ############### My own tile #########################
            # collection = ee.ImageCollection('LANDSAT/LE07/C01/T1').filterDate('2000-04-01', '2000-07-01')
            collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterDate('2017-05-01', '2017-07-01')
            median = collection.median()
            # result = median.select('B3', 'B2', 'B1')
            result = median.select('B4', 'B3', 'B2')


            image_viz_params = { 'max': 0.4, "gamma": 1.6}
            ######

            l8_filtered = ee.ImageCollection('LANDSAT/LC08/C01/T1').filterDate(
                '2015-1-1', '2015-7-1');
            composite = ee.Algorithms.Landsat.simpleComposite(collection=l8_filtered, asFloat = True)

            viz_param  = {
                "bands": ['B6', 'B5', 'B4'], "max": [0.3, 0.4, 0.3]
            }
             ###

            col2 = ee.ImageCollection('BNU/FGS/CCNL/v1').filterDate('2010-01-01', '2010-12-31').median().select('b1')


            ch_param = {
                "min" : 3,
                "max":60
            }
            ##############  finish of My own Tile ################

            ee_tiles = [col2, composite, result]

            # Arrange visualization parameters inside a list.
            ee_vis_params = [ch_param, viz_param, image_viz_params]

            # Arrange layer names inside a list.
            ee_tiles_names = ['Nighttime Light', 'LandSat Composite', 'LandSat T1_TOA']

            # Add layers to the map using a loop.
            for tile, vis_param, name in zip(ee_tiles, ee_vis_params, ee_tiles_names):
                m.add_ee_layer(tile, vis_param, name)
        #### end of IF/// checking google MAp status



        ##### adding the image #######
        bound = [[ self.img4map['lat']-3, self.img4map['lon']-3 ], [self.img4map['lat']+3, self.img4map['lon']+3 ]]

        folium.raster_layers.ImageOverlay(
            image= self.img4map['fileAddr'],
            # image=os.path.join(self.img4map),
            name="image_opacity 0.7",
            # bounds=[[0,0],[10,10]],
            bounds=bound,
            opacity=0.7,
            interactive=False,
            cross_origin=False,
            zindex=1,
            alt="Wikipedia File:Mercator projection SW.jpg",
        ).add_to(m)
        # folium.LayerControl().add_to(m)
        m.add_child(folium.LatLngPopup())



        ###### end of Add image

        # Add a layer control panel to the map.

        folium.LayerControl(collapsed=False).add_to(m)
        # m.add_child(folium.LayerControl(collapsed=False))



        # folium.LayerControl().add_to(m)


        data = io.BytesIO()
        m.save(data, close_file=False)

        w = QtWebEngineWidgets.QWebEngineView()
        w.setHtml(data.getvalue().decode())
        w.resize(800, 600)

        return w



    def mapgen(self):

        m = folium.Map(location=[5, 5], zoom_start=5, tiles="Stamen Terrain")

        folium.raster_layers.ImageOverlay(
            # image=os.path.join("./temp/", self.img4map),
            image= "./appdata/test.png",
            name="image_opacity 0.7",
            bounds=[[0, 0], [10, 10]],
            opacity=0.7,
            interactive=False,
            cross_origin=False,
            zindex=1,
            alt="Wikipedia File:Mercator projection SW.jpg",
        ).add_to(m)
        folium.LayerControl().add_to(m)


        m.add_child(folium.LatLngPopup())

        data = io.BytesIO()
        m.save(data, close_file=False)

        w = QtWebEngineWidgets.QWebEngineView()
        w.setHtml(data.getvalue().decode())
        w.resize(800, 600)

        return w



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Secondwindow({'fileAddr': './temp/img4mapTUBIN_VIS_20210709_125820_676_2.png', 'lat': 74.6543105082167, 'lon': 22.1445811329384})
    # window = Secondwindow("./temp/img4mapTUBIN_VIS_20210709_125920_700_2.png")
    window.show()

    sys.exit(app.exec_())