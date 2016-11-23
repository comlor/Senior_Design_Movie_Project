import json

class CZMLParser(object):

    def __init__(self, path):
        self.path = path;

    def openFile(self, path):
        '''
        param path: the file path
        type path: str
        return: Czml database
        rtype: python object
        '''
        with open(path) as czml_file:
            czml_data = json.load(czml_file)
        return czml_data

    def movie_Properties(self):
        '''
        param path: the file path
        type path: str
        return: movie properties dictionary
        rtype: dictionary
        '''
        czml_data = self.openFile(self.path)

        movie_properties = {'format': czml_data["movieProperties"]["format"],
                            'quality': czml_data["movieProperties"]["quality"],
                            'resolution': czml_data["movieProperties"]["resolution"],
                            'email': czml_data["movieProperties"]["email"]}

        return movie_properties

    def camera_Postion(self):
        '''
        param path: the file path
        type path: str
        return: camera Postion dictionary
        rtype: dictionary
        '''
        czml_data = self.openFile(self.path)

        cameraPosition = {'interpolationAlgorithm': czml_data["czml"][1]["position"]["interpolationAlgorithm"],
                          'interpolationDegree': czml_data["czml"][1]["position"]["interpolationDegree"],
                          'epoc': czml_data["czml"][1]["position"]["epoc"],
                          'cartographicRadian': czml_data["czml"][1]["position"]["cartographicRadian"]}

        return cameraPosition

    def sun_Postion(self):
        '''
        param path: the file path
        type path: str
        return: sun Postion dictionary
        rtype: dictionary
        '''
        czml_data = self.openFile(self.path)

        sunPosition = {'interpolationAlgorithm': czml_data["czml"][2]["position"]["interpolationAlgorithm"],
                       'interpolationDegree': czml_data["czml"][2]["position"]["interpolationDegree"],
                       'epoc': czml_data["czml"][2]["position"]["epoc"],
                       'cartographicRadian': czml_data["czml"][2]["position"]["cartographicRadian"]}

        return sunPosition

    def camera_Orientation(self):
        '''
        param path: the file path
        type path: str
        return: camera Orientation dictionary
        rtype: dictionary
        '''
        czml_data = self.openFile(self.path)

        cameraOrientation = {'interpolationAlgorithm': czml_data["czml"][1]["orientation"]["interpolationAlgorithm"],
                             'interpolationDegree': czml_data["czml"][1]["orientation"]["interpolationDegree"],
                             'epoc': czml_data["czml"][1]["orientation"]["epoc"],
                             'cartographicRadian': czml_data["czml"][1]["orientation"]["unitQuaternion"]}

        return cameraOrientation

    def sun_Orientation(self):
        '''
        param path: the file path
        type path: str
        return: sun Orientation dictionary
        rtype: dictionary
        '''
        czml_data = self.openFile(self.path)

        sunOrientation = {'interpolationAlgorithm': czml_data["czml"][2]["orientation"]["interpolationAlgorithm"],
                          'interpolationDegree': czml_data["czml"][2]["orientation"]["interpolationDegree"],
                          'epoc': czml_data["czml"][2]["orientation"]["epoc"],
                          'cartographicRadian': czml_data["czml"][2]["orientation"]["unitQuaternion"]}

        return sunOrientation

    def cesium_version(self):
        '''
        param path: the file path
        type path: str
        return: cesium version
        rtype: str
        '''
        czml_data = self.openFile(self.path)

        cesium_version = czml_data["czml"][1]["version"]

        return cesium_version

    def my_path(self):
        '''
        param path: the file path
        type path: str
        return: path info(material, width, leadTime, trailTime, resolution) and every
            associated info with each element
        rtype: nested tuple
        '''
        czml_data = self.openFile(self.path)

        color = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["color"]["rgba"]
        outlineColor = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["outlineColor"]["rgba"]
        outlineWidth = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["outlineWidth"]
        polylineOutline = color, outlineColor, outlineWidth
        material = polylineOutline, ''
        path = polylineOutline, czml_data["czml"][0]["path"]["width"], czml_data["czml"][0]["path"]["leadTime"], \
               czml_data["czml"][0]["path"]["trailTime"], czml_data["czml"][0]["path"]["resolution"]

        return path

    def blenderCamera(self):
        '''
        param path: the file path
        type path: str
        return: CameraPosition CameraOrientation
        rtype: list
        '''
        czml_data = self.openFile(self.path)
        orientation = self.camera_Orientation()
        position = self.camera_Postion()

        orientation = orientation['unitQuaternion']
        position = position['cartographicRadian']

        finalPosition = [position[x:x + 4] for x in range(0, len(position), 4)]
        finalOrientation = [orientation[x:x + 5] for x in range(0, len(orientation), 5)]

        temp = (finalPosition, finalOrientation)

        return temp


def main():
    the_parser = CZMLParser('/home/chrisomlor/MovieDemo/GitClones/JSON/sample_format.czml')
    print(the_parser.blenderCamera())

if __name__ == "__main__":
    main()
