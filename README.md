# TUBIN-Satellite-Img-Browser
TUBIN Nanosatellite Image Browser based on Metadata Catalog
This application compile into executable with Pyqt interface to download and manage cloud based satellite image repositories.
The user interface of the application is shown in the figure 1 with the sequence of windows from
one to three. Window 1 is the welcoming window which consists of two main sections, on the left
side of the window, some metadata parameters are provided as search queries. The parameters only
include a subsection of all parameters, otherwise it becomes very cluttered. The chosen parameters
are the most significant ones and in-line with what satellite image providers offer. It comprises 4
subsections. First, geo distance from location of interest and desired radius. As there are cases for
which VIS camera direction has no intersection with earth ellipsoid, therefore space looking images
are defined.
The next section is related to image content. Although there is no metadata now available for
these parameters, the capability is embedded into the program, and therefore, for a metadata catalog
that has the corresponding columns, the same application will work. For the “only moon” checkbox,
an algorithm is used to calculate the look angle to the moon, and the result is partially correct and
includes moon images, further investigation by checking the image content is required.
The next section is the imaging environment, which filters based on local time (night and sun
elevation) of the geo location of the central latitude and longitude of a scene. The use cases may
include investigating different sun lighting on earth and corresponding images.
Finally, the sensor parameters, which gives the ability to choose between IR or VIS Camera,
and also, the look angle of VIS Camera. The apply filter button, goes through the metadata catalog
and finds the relevant images. On the right side there are two tabs, one is static map (without any
interaction with files) that shows some representative locations of images to provide users with some
guidance choosing relevant locations to search, and the other tab, dynamic tab on window (2) is
a file explorer that shows the result of filtering, in forms of list of images. By clicking a name, the
program downloads the image from the cloud repository into a temporary folder, and shows it in the
application. Beneath the image there is a small text box that shows all related metadata, it is very
helpful to track errors and to investigate wrong calculations. There is also an option to select many
images and download them. The images are downloaded inside the download folder. And there is
also, a button “Empty temp. folder” to empty temporary images in the temp folder.
Finally, there is an option to overlay or check the satellite images of the corresponding location
on earth. If there is a latitude and longitude associated with an image, the “show on map” tab will
open up a map with an access to google image collection server on the internet. The possibilities of
google image collections are enormous and it is definitely a valuable asset to investigate the validity
and make comparisons. There are three collections already added, namely night time light, Landsat
composite and RGB images. Users can activate layers as desired. There is also an optional but not
accurate overlay of selected images on the google map, as shown in the figure 1. These capabilities are
just demonstrations of the features that can be extended and enhanced later.
 
