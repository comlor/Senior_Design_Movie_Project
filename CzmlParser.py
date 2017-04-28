import json
import os

file = 'sample_json.json'

class CZML_Parser:

    def __init__(self, json_file):
        self.__path = json_file

    def open_file(self):
        '''
        param path: the file path
        type path: str
        return: Czml database
        rtype: python object
        '''
        with open(self.__path) as json_file:
            json_data = json.load(json_file)
        return json_data

    def epoch(self):
        '''
        param path: the file path
        type path: str
        return:Get the epoch of the camera
        rtype:str
        '''
        json_data = self.open_file()

        epoch = json_data[1]["position"]["epoch"]
        return epoch
    #epoch(file)

    def interpolationAlgorithm(self):
        '''
        param path: the file path
        type path: str
        return:Get the interpolation Algorithm
        rtype:str
        '''
        json_data = self.open_file()

        iAlgo = json_data[1]["position"]["interpolationAlgorithm"]
        return iAlgo
    #interpolationAlgorithm(file)

    def interpolationDegree(self):
        '''
        param path: the file path
        type path: str
        return:Get the interpolation Degree
        rtype:str
        '''
        json_data = self.open_file()

        iDegree = json_data[1]["position"]["interpolationDegree"]
        return iDegree
    #interpolationDegree(file)

    def position(self):
        '''
        param path: the file path
        type path: str
        return: list positions
        rtype: list
        '''
        json_data = self.open_file()

        position = json_data[1]["position"]["cartographicDegrees"]
        return position
    #position(file)

    def orientation(self):
        '''
        param path: the file path
        type path: str
        return: list orientation
        rtype: list
        '''
        json_data = self.open_file()

        orientation = json_data[1]["orientation"]["unitQuaternion"]
        return orientation
    #orientation(file)

    def blenderCamera(self):
        '''
        param path: 
        type path: 
        return: Position(timeOffset,long,lat,alt) groups by point
                Orientation-()groups by point
        rtype: list of postions and orientations
        '''

        o = self.orientation()
        p = self.position()

        finalPosition = [p[x:x+4] for x in range(0, len(p), 4)]
        finalOrientation = [o[x:x+4] for x in range(0, len(o), 4)]

        temp = (finalPosition, finalOrientation)

        return temp
    
    def email(self):
        '''
        param path: 
        type path: 
        return: Position(timeOffset,long,lat,alt) groups by point
                Orientation-()groups by point
        rtype: list of postions and orientations
        '''
        json_data = self.open_file()

        email =  json_data[2]["email"]
        return email
    
    def sundata(self):
        '''
        param path: the file path
        type path: str
        return: Position(timeOffset,long,lat,alt) groups by point
            Orientation-()groups by point
        rtype: list of postions and orientations
        '''
        json_data = self.open_file()

        sun =  json_data[2]["sunData"]#need to find exact key names
    
        return sun
    
def main():
    json = CZML_Parser(file)
    
    print(json.sundata())
    print(json.email())

if __name__ == '__main__':
     main()