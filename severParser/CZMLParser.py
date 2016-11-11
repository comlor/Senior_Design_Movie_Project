import json

class CZMLParser(object):
    path = "";

    def __init__(self):
        path = self;

    def openFile(path):
        '''
        param path: the file path
        type path: str
        return: Czml database
        rtype: python object
        '''
        with open(path) as czml_file:
            czml_data = json.load(czml_file)
        return czml_data

    def movie_Properties(path):
        '''
        param path: the file path
        type path: str
        return: movie properties dictionary
        rtype: dictionary
        '''
        czml_data = openFile(path)

        movie_properties = {'format': czml_data["movieProperties"]["format"],
                            'quality': czml_data["movieProperties"]["quality"],
                            'resolution': czml_data["movieProperties"]["resolution"],
                            'email': czml_data["movieProperties"]["email"]}

        return movie_properties

    def camera_Postion(path):
        '''
        param path: the file path
        type path: str
        return: camera Postion dictionary
        rtype: dictionary
        '''
        czml_data = open_file(path)

        cameraPosition = {'interpolationAlgorithm': czml_data["czml"][1]["position"]["interpolationAlgorithm"],
                          'interpolationDegree': czml_data["czml"][1]["position"]["interpolationDegree"],
                          'epoc': czml_data["czml"][1]["position"]["epoc"],
                          'cartographicRadian': czml_data["czml"][1]["position"]["cartographicRadian"]}

        return cameraPostion

    def sun_Postion(path):
        '''
        param path: the file path
        type path: str
        return: sun Postion dictionary
        rtype: dictionary
        '''
        czml_data = open_file(path)

        sunPosition = {'interpolationAlgorithm': czml_data["czml"][2]["position"]["interpolationAlgorithm"],
                       'interpolationDegree': czml_data["czml"][2]["position"]["interpolationDegree"],
                       'epoc': czml_data["czml"][2]["position"]["epoc"],
                       'cartographicRadian': czml_data["czml"][2]["position"]["cartographicRadian"]}

        return sunPostion

    def camera_Orientation(path):
        '''
        param path: the file path
        type path: str
        return: camera Orientation dictionary
        rtype: dictionary
        '''
        czml_data = open_file(path)

        cameraOrientation = {'interpolationAlgorithm': czml_data["czml"][1]["orientation"]["interpolationAlgorithm"],
                             'interpolationDegree': czml_data["czml"][1]["orientation"]["interpolationDegree"],
                             'epoc': czml_data["czml"][1]["orientation"]["epoc"],
                             'cartographicRadian': czml_data["czml"][1]["orientation"]["unitQuaternion"]}

        return cameraOrientation

    def sun_Orientation(path):
        '''
        param path: the file path
        type path: str
        return: sun Orientation dictionary
        rtype: dictionary
        '''
        czml_data = openFile(path)

        sunOrientation = {'interpolationAlgorithm': czml_data["czml"][2]["orientation"]["interpolationAlgorithm"],
                          'interpolationDegree': czml_data["czml"][2]["orientation"]["interpolationDegree"],
                          'epoc': czml_data["czml"][2]["orientation"]["epoc"],
                          'cartographicRadian': czml_data["czml"][2]["orientation"]["unitQuaternion"]}

        return sunOrientation

    def cesium_version(path):
        '''
        param path: the file path
        type path: str
        return: cesium version
        rtype: str
        '''
        czml_data = openFile(path)

        cesium_version = czml_data["czml"][1]["version"]

        return cesium_version

    def path(path):
        '''
        param path: the file path
        type path: str
        return: path info(material, width, leadTime, trailTime, resolution) and every
            associated info with each element
        rtype: nested tuple
        '''
        czml_data = openFile(path)

        color = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["color"]["rgba"]
        outlineColor = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["outlineColor"]["rgba"]
        outlineWidth = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["outlineWidth"]
        polylineOutline = color, outlineColor, outlineWidth
        material = polylineOutline, ''
        path = polylineOutline, czml_data["czml"][0]["path"]["width"], czml_data["czml"][0]["path"]["leadTime"], \
               czml_data["czml"][0]["path"]["trailTime"], czml_data["czml"][0]["path"]["resolution"]

        return path