from bottle import get, post, run, route, request, response

import spiceypy as spy
import  json




@route('/spiceoutput')
def spiceoutput():
    print(spy.tkvrsn('TOOLKIT'))
    # dir(spiceypy)
    # help(spiceypy)
    ABCORR = "NONE"
    FRAME = "J2000"
    #
    SPK = "C:\\Users\\Angel Jimenez\\Downloads\\de405.bsp"
    # ET0 represents the date 2000 Jan 1 12:00:00 TDB.
    ET0 = 0.0  #
    OBSERVER = "Mars"
    TARGET = "Sun"
    spy.furnsh(SPK)
    return str(spy.spkezr(TARGET, ET0, FRAME, ABCORR, OBSERVER))


@route('/hello')
def hello():
    return "Hello World!"


@get('/login')
def login():
    username = request.params.username
    password = request.params.password
    a = request.params.a;

    # insert spice function here and output the result as json array
    return str(username + " " + password)


run(host='localhost', port=8080, debug=True)
