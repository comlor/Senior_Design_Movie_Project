from bottle import get, post, run, route, request, response, hook

import spiceypy as spy
import  json

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/spiceoutput')
class Spice():
    def __init__(self, lon, lat, alt, et, planet):
        self.lon = float(lon)
        self.lat = float(lat)
        self.alt = float(alt)
        self.et = et
        self.planet = planet

    def spkFiles(self):
        '''
        Loads the kernel that are needed for dertermining the calculations

        param: NONE
        return: none
        '''

        # Must put the path to these files
        SPK = ["spice/de405.bsp"
            , "spice/pck00008.tpc.txt"
            , "spice/naif0012.txt"]
        spy.furnsh(SPK)

    def spherToCart(self, lon, lat, alt, velocity, planet):
        '''

        :param lon:
        :param lat:
        :param alt:
        :param velocity:
        :param planet:
        :return:
        '''

        self.spkFiles()

        input_state = [lon, lat, alt, velocity[0], velocity[1], velocity[2]]
        input_coord_sys = 'PLANETOGRAPHIC'
        output_corrd_sys = 'RECTANGULAR'

        temp = spy.xfmsta(input_state, input_coord_sys, output_corrd_sys, planet)

        list = temp[0], temp[1], temp[2]

        return list

    def sunData(self):
        '''

        :param lon:
        :param lat:
        :param alt:
        :param et:
        :param planet:
        :return:
        '''
        frame = "J2000"
        abcorr = "None"
        target = "Sun"
        refloc = 'TARGET'

        # get the files required
        self.spkFiles()

        # gets correct time format
        et0 = self.et
        et1 = et0.replace('T', ' ')
        et2 = et1.replace('Z', '')
        et3 = spy.str2et(et2)

        # print(et3)

        # get the velocity of planet
        templist = spy.spkezr(self.planet, et3, frame, abcorr, target)
        velocity = templist[0][3], templist[0][4], templist[0][5]

        # converts into x,y,z from lon,lat,alt
        xyz = self.spherToCart(self.lon, self.lat, self.alt, velocity, self.planet)

        temp0 = spy.spkcpo(target, et3, frame, refloc, abcorr, xyz, self.planet, frame)
        sunPos = temp0[0][0], temp0[0][1], temp0[0][2]
        return json.dumps(sunPos)

@route('/SunData')
def SunData():
    lon = request.params.lon
    lat = request.params.lat
    alt = request.params.alt
    et = request.params.et
    planet = request.params.planet

    print(alt)

    lon = str(lon)
    lat = str(lat)
    alt = str(alt)
    lon = lon.replace('p','.')
    lat = lat.replace('p', '.')
    alt = alt.replace('p','.')


    sun = Spice(lon,lat,alt,et,planet)

    #URL I tested it on
    #http://localhost:8281/SunData?lon=29p001&lat=26p2121&alt=52p999&et=2012-08-04T10:00:00Z&planet=Mars
    dataString = sun.sunData()
    return dataString

run(host='localhost', port=8281, debug=True)
