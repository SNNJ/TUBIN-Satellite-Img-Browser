from PIL import Image
import os
import shutil

class CimgResize:
    def __init__(self):
        pass
        # self.file = {'found':False, 'name':""}
    def fimgResize(self, fileAddr=''):
        self.img2reduce = fileAddr
        if self.img2reduce == '':
            return
        if len(self.img2reduce.split('/')) > 0:
            self.img2reduce = self.img2reduce.split('/')[-1]

        fileStatuse = self.fsearch()

        if fileStatuse[0] == True  and self.img2reduce == fileStatuse[1].split("img4map")[-1]:
            return

        this_image = Image.open("./temp/" + self.img2reduce)
        width, height = this_image.size
        if os.stat("./temp/"+self.img2reduce).st_size/(1024 *1024) > 0.5: ### reducing bit dpeth as well
            TARGET_WIDTH = 640
            coefficient = width / TARGET_WIDTH
            new_height = height / coefficient
            this_image = this_image.resize((int(TARGET_WIDTH), int(new_height)), Image.Resampling.LANCZOS)
            # imgdata = io.BytesIO()
            this_image.save("./temp/img4map%s" % self.img2reduce, quality=90, format="png")
            # encoded = base64.b64encode(imgdata.getvalue())
            # this_image.save("modified.png", quality=50)
        else:
            shutil.copy("./temp/" + self.img2reduce, "./temp/img4map%s" % self.img2reduce)


        # This is to get the directory that the program


    def fsearch(self):        # is currently running in.
        for root, dirs, files in os.walk('./temp'):
            for file in files:
                # change the extension from '.mp3' to
                # the one of your choice.
                if file.startswith('img4map' + self.img2reduce):
                    print(root + '/' + str(file))
                    return (True,str(file))
                    break


        return (False,"")

if __name__ == "__main__":

    app = CimgResize()
    # app = CimgResize()
    # app.fimgResize("TUBIN_VIS_20210709_125940_712_2.png")
    app.fimgResize("TUBIN_VIS_20210709_130701_028_1.png")