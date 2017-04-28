from bottle import get, post, run, route, request, response, hook, abort, put
import spiceypy as spy
import random
import json
import string
import os
from pymongo import MongoClient
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId
import smtplib
from email.mime.text import MIMEText
import subprocess
from CzmlParser import CZML_Parser

connection = MongoClient('localhost', 27017)
db = connection['documents']
posts = db.posts

@route('/<:re:.*>', method='OPTIONS')
def enable_cors_generic_route():
	"""
	This route takes priority over all others. So any request with an OPTIONS
	method will be handled by this function.

	See: https://github.com/bottlepy/bottle/issues/402

	NOTE: This means we won't 404 any invalid path that is an OPTIONS request.
	"""
	add_cors_headers()	
	
@hook('before_request')
def enable_cors_after_request_hook():
	"""
	This executes after every route. We use it to attach CORS headers when
	applicable.
	"""
	add_cors_headers()
	
def add_cors_headers():
	if True:  # You don't have to gate this
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = \
			'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = \
			'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
			
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

def base_str():
    return string.ascii_lowercase + string.ascii_uppercase + string.digits


def key_gen(KEY_LEN=20):
    keylist = [random.choice(base_str()) for i in range(KEY_LEN)]
    return "".join(keylist)

@post('/getData')
def getData():
    json_text = request.json
    print("**************************************************************")
    print(json_text)
    print("**************************************************************")
    json_str = json.dumps(json_text)
    print(json_str)
    print("***************************************************************")
    temp = json.loads(json_str)
    email = temp["email"]
    check_availablity(key_gen(20), email, json_text)

    #alt = "python3 /home/chrisomlor/MovieDemo/program_driver.py /home/chrisomlor/MovieDemo/Assets/liveJson.JSON"
    #sub = subprocess.Popen([alt], shell=True)


@get('/temp')
def doTemp():
    randomid = key_gen(20)
    print(randomid)
    check_availablity(randomid, "fake@gmail.com")


def check_availablity(randomid, email, json_text):
    entity = posts.find_one({'vid': randomid})
    print(entity)
    if not entity:
        # TODO: EDIT PATH ON LINUX SYSTEM
        mypath = '/home/chrisomlor/MovieDemo/jobs/' + str(randomid)
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        try:
            abspath = "/home/chrisomlor/MovieDemo/output/" + randomid
            posts.insert_one({'vid': randomid, 'email': email, 'path': mypath, 'output': abspath})
            with open(mypath + "Assets/liveJson.JSON", 'w') as outfile:
                json.dump(json_text, outfile)

            alt = "python3 /home/chrisomlor/MovieDemo/program_driver.py /home/chrisomlor/MovieDemo/Assets/liveJson.JSON "
            alt += mypath
            alt += " "
            alt += abspath
            alt += " "
            alt += randomid
            sub = subprocess.Popen([alt], shell=True)

        except RuntimeError:
            pass
    else:
        check_availablity(key_gen(20), email, json_text)

# SEND THE MOVIE NAME HERE
@post('/completed')
def sendEmail():
    postdata = request.body.read()
    print(postdata)
    entity = json.loads(posts.find_one({'vid': postdata}))
    if not entity:
        abort(404,"No such video")
    else:
        temp = json.dumps(entity, sort_keys=True, indent=4, default=json_util.default)
        temp1 = json.loads(temp)
        to = temp1["email"]
        text = temp1["output"]
        sendMail('temp@gmail.com', to, 'Your Movie from MarsTrek has completed!', text, 'smtp.gmail.com')


def sendMail(FROM, TO, SUBJECT, TEXT, SERVER):
    import smtplib
    """this is some test documentation in the function"""
    message = """\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    # Send the mail
    server = smtplib.SMTP(SERVER)
    "New part"
    server.starttls()
    server.login('username', 'password')
    server.sendmail(FROM, TO, message)
    server.quit()

run(host='localhost', port=8281, debug=True)
