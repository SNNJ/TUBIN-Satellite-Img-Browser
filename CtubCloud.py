import shutil
import owncloud
import os


class downloader:
    def __init__(self):
        self.tuburl = "https://tubcloud.tu-berlin.de/s/4xWGAgX5wdRZqJD"
        self.activeLink = owncloud.Client.from_public_link(self.tuburl)
        if not os.path.exists("./download") :
            try:
                os.mkdir("./download")
            except OSError as error:
                print(error)
        if not os.path.exists("./temp") :
            try:
                os.mkdir("./temp")
            except OSError as error:
                print(error)

    def flink(self,link,where2save ='./temp'):
        self.imgName = link.split("/")[-1]

        if not os.path.exists("./temp/" + self.imgName) and not os.path.exists("./download/" + self.imgName):
            status = self.activeLink.get_file(link , where2save + "/" + self.imgName)
            print("downloading %s"%status)
        elif os.path.exists("./temp/" + self.imgName) and where2save == "./download":
            shutil.copy("./temp/" + self.imgName, "./download/" + self.imgName)
        elif os.path.exists("./download/" + self.imgName):
                where2save = "./download"

        return where2save + "/" + self.imgName
        # self.activeLink.get_file("/210706_first_light/TUBIN_IR2_20210706_133848_892_9.png", 'C:/Users/MakMac/Desktop/MSE Courses Semester 2/space sensors and instrument/pythonUserSegment/temp')
    def flinks(self, links):

        for i in links:
            print( " it is downloaind")
            self.flink(link=i, where2save='./download')




if __name__ == "__main__":
    db = downloader()
    savedin = db.flink("/210706_first_light/TUBIN_IR2_20210706_133848_892_9.png")
    print(savedin)