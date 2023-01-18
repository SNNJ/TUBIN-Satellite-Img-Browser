# this is for checking the filtering and these things
import pandas as pd
import geopy.distance
class Cdb:
    def __init__(self):
        self.namingDic = {'slon': 'siteLon',
             'slat': 'siteLat',
             'sspace': 'siteLat',
             # for now it checks for zero value on siteLat, but later, another column like haveIntersection is required
             'squality': 'imgQuality',
             'scloud': 'cloudCoverage',
             'swater': 'waterCoverage',
             'smoon': 'moonLookingAngle',
             'sfire': 'imgFire',
             'snight': 'DayNight',
             'stime': 'localHour',  # localHour
             'localDate': 'localDateTime',  # local Full date
             'ssun': 'Elevation',
             'sgain': 'Gain',
             'sir': 'camera',
             'svis': 'camera',
             'slook': 'lookAngle'}
        self.db = pd.read_excel('./appdata/tuBinMetaData.xlsx')
        # Filtering for valid AdcsStateValid that is AdcsStateValid ==1
        self.db = self.db.query('AdcsStateValid == 1')
        self.fdb = self.db
        self.fdb[self.namingDic['stime']] = self.fdb[self.namingDic['localDate']].dt.hour


    def fdbfilter(self,condition):
        db = self.fdb
            # condition = {'type':'query', 'colName':'sspace', 'query':'%s.isnull()'}
            # condition = {'type':'query', 'colName':'scloud', 'query':'%s == 3'}
            # condition = {'type':'query', 'colName':'smoon', 'query':'%s == 0'}
            # condition = {'type':'query', 'colName':'smoon', 'query':'%s == 0'}
            # condition = {'type':'dist', 'sceneLoc' : [54,68], 'query':' <2000 '}
            # condition = {'type':'query', 'colName':'stime', 'query':' 2< %s <= 5 '}

        def fdist(imgC, selC):  # row of image contaitning coordinates and selected coordinate
            return geopy.distance.geodesic(imgC, selC).km

        if condition['type'] == "query":
            print(" Inside query filtering")
            if self.namingDic[condition['colName']] in db.columns and db.shape[0] > 0:
                db = db.query(condition['query']%self.namingDic[condition['colName']])
                print(db.head(5)[self.namingDic[condition['colName']]])
        elif condition['type'] == "dist":
            print(" the distance function")
            if self.namingDic['slat'] in db.columns and self.namingDic['slon'] in db.columns and db.shape[0] > 0:
                db = db.query('%s.isnull() == False'%self.namingDic['slat'])
                ldist = db.apply(lambda row: fdist((row[self.namingDic['slat']], row[self.namingDic['slon']]), tuple(condition['sceneLoc'])), axis=1)
                # ldist = db.apply(lambda row: geopy.distance.geodesic((23,45), (54,68)).km, axis=1)
                # print(type(ldist))
                db['ldist'] = ldist
                db = db.query('ldist %s'% condition['query'])
                print(db.head(5)['ldist'])
        elif condition['type'] == "sparse":
                print(" the sparse function")
                if self.namingDic['slat'] in db.columns and self.namingDic['slon'] in db.columns and db.shape[0] > 0:
                    db = db.query('%s.isnull() == False' % self.namingDic['slat'])
                    db['sparse'] = round(db.siteLat.iloc[:]) * 1000 + round(db.siteLon.iloc[:])
                    db.drop_duplicates(subset=['sparse'], inplace=True)

        else:
            print("some error regarding type of search")

        self.fdb =db


if __name__ == "__main__":

    db = Cdb()
    # db.fdbfilter({'type': 'query', 'colName': 'sspace', 'query': '%s.isnull()'})
    db.fdbfilter(condition = {'type':'dist', 'sceneLoc' : [54,68], 'query':' <2000 '})