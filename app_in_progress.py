from bottle import get, post, run, route, request, response, hook, abort, put
from jpl_conf import FilePaths
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
    add_cors_headers()


@hook('before_request')
def enable_cors_after_request_hook():
    add_cors_headers()


def add_cors_headers():
    if True:
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
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
        # Must put the path to these files
        SPK = ["spice/de405.bsp"
            , "spice/pck00008.tpc.txt"
            , "spice/naif0012.txt"]
        spy.furnsh(SPK)


    def spherToCart(self, lon, lat, alt, velocity, planet):
        self.spkFiles()

        input_state = [lon, lat, alt, velocity[0], velocity[1], velocity[2]]
        input_coord_sys = 'PLANETOGRAPHIC'
        output_corrd_sys = 'RECTANGULAR'

        temp = spy.xfmsta(input_state, input_coord_sys, output_corrd_sys, planet)

        list = temp[0], temp[1], temp[2]

        FilePaths().log_events("Sun Data - Sphere to Cart: " + str(list) + "\n")
        return list


    def sunData(self):
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

        # get the velocity of planet
        templist = spy.spkezr(self.planet, et3, frame, abcorr, target)
        velocity = templist[0][3], templist[0][4], templist[0][5]

        # converts into x,y,z from lon,lat,alt
        xyz = self.spherToCart(self.lon, self.lat, self.alt, velocity, self.planet)

        temp0 = spy.spkcpo(target, et3, frame, refloc, abcorr, xyz, self.planet, frame)
        sunPos = temp0[0][0], temp0[0][1], temp0[0][2]
        FilePaths().log_events("Sun Data - Sun Position: " + str(sunPos) + "\n")
        return json.dumps(sunPos)


@route('/SunData')
def SunData():
    lon = request.params.lon
    lat = request.params.lat
    alt = request.params.alt
    et = request.params.et
    planet = request.params.planet

    lon = str(lon)
    lat = str(lat)
    alt = str(alt)
    lon = lon.replace('p','.')
    lat = lat.replace('p', '.')
    alt = alt.replace('p','.')

    sun = Spice(lon, lat, alt, et, planet)

    dataString = sun.sunData()
    FilePaths().log_events("Sun Data - Data String: " + str(dataString) + "\n")

    return dataString


def base_str():
    return string.ascii_lowercase + string.ascii_uppercase + string.digits


def key_gen(KEY_LEN=20):
    keylist = [random.choice(base_str()) for i in range(KEY_LEN)]
    return "".join(keylist)


@post('/getData')
def getData():
    json_text = request.json
    #temp = json.loads(json_text)
    email = json_text[2]["email"]
    check_availablity(key_gen(20), email, json_text)


@get('/temp')
def doTemp():
    randomid = key_gen(20)
    check_availablity(randomid, "fake@gmail.com")


def check_availablity(randomid, email, json_text):
    FilePaths().log_events("\n\n****************JOB BEGIN " + randomid + "********************\n\n")
    entity = posts.find_one({'vid': randomid})
    if not entity:
        # TODO: EDIT PATH ON LINUX SYSTEM
        mypath = FilePaths().get_job_dir() + str(randomid)
        FilePaths().log_events("Current Job Path: " + mypath + "\n")
        if not os.path.isdir(mypath):
            FilePaths().log_events("Creating Directory: " + mypath + "\n")
            os.makedirs(mypath)
        try:
            output_path = FilePaths().get_final_output_dir() + randomid
            FilePaths().log_events("Ouput Directory: " + output_path + "\n")
            if not os.path.isdir(output_path):
                FilePaths().log_events("Creating Output Directory: " + output_path + "\n")
                os.makedirs(output_path)

            FilePaths().log_events("Insert Database Record: " + randomid + ", Email: " + email + ", JobPath: " +
                                   mypath + ", OutputPath: " + output_path + "\n")
            posts.insert_one({'vid': randomid, 'email': email, 'path': mypath, 'output': output_path})

            FilePaths().log_events("Save JSON to File in job directory: " + mypath + "/liveJson.JSON\n")
            with open(mypath + "/liveJson.JSON", 'w') as outfile:
                json.dump(json_text, outfile)

            server_dir = FilePaths().get_abs_path_project()
            FilePaths().log_events("Server Directory: " + server_dir + "\n")

            alt = "python3 "
            alt += server_dir
            alt += "program_driver.py "
            alt += mypath
            alt += "/liveJson.JSON "
            alt += mypath
            alt += " "
            alt += output_path
            alt += " "
            alt += randomid

            FilePaths().log_events("Execute Command: " + alt + "\n")
            sub = subprocess.Popen([alt], shell=True)

        except Exception as e:
            print(e)
    else:
        check_availablity(key_gen(20), email, json_text)


# SEND THE MOVIE NAME HERE
@post('/completed')
def sendEmail():
    postdata = str(request.body.read())
    postdata = postdata[2:-1]
    entity = posts.find_one({'vid': postdata})
    if not entity:
        abort(404, "No such video")
        FilePaths().log_events("VIDEO NOT FOUND\n")
    else:
        FilePaths().log_events("Preparing Email Link --> ")
        temp = json.dumps(entity, sort_keys=True, indent=4, default=json_util.default)
        temp1 = json.loads(temp)
        to = temp1["email"]
        text = temp1["output"] + "/" + postdata + ".avi"
        FilePaths().log_events("Video Name: " + text + "\n")
        sendMail('testaddress4454543@gmail.com', to, 'Your Movie from MarsTrek has completed!', text, 'smtp.gmail.com')


def sendMail(FROM, TO, SUBJECT, TEXT, SERVER):
    msg = MIMEText(TEXT)
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    server = smtplib.SMTP(SERVER)
    server.starttls()
    #login paramters -> username,password
    FilePaths().log_events("Send Email --> ")
    server.login('testaddress4454543', 'Planetaryflyovergroup')
    server.sendmail(FROM, TO, msg.as_string())
    FilePaths().log_events("Email Sent to: " + TO + "\n")
    server.quit()
    FilePaths().log_events("\n\n****************JOB COMPLETE " + TEXT + "********************\n\n")

run(host='localhost', port=8281, debug=True)
