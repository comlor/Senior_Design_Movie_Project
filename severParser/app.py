from bottle import get, post, run, route, request, response

import spiceypy as spy
import os
import  json


def spkFiles():
    '''
    Loads the kernel that are needed for dertermining the calculations

    param: NONE
    return: none
    '''
    cwd = os.getcwd()
    spicedir = cwd + "\\spice"
    SPK = [spicedir+"\\de405.bsp", spicedir+"\\pck00008.tpc.txt"]
    spy.furnsh(SPK)

@route('/spiceoutput')
def spiceoutput():
    print(spy.tkvrsn('TOOLKIT'))
    # dir(spiceypy)
    # help(spiceypy)
    ABCORR = "NONE"
    FRAME = "J2000"
    #
    SPK = "C:/Users/Shawn/PycharmProjects/School/spice/de405.bsp"
    # ET0 represents the date 2000 Jan 1 12:00:00 TDB.
    ET0 = 0.0  #
    OBSERVER = "Mars"
    TARGET = "Sun"
    spy.furnsh(SPK)
    return json.dumps(spy.spkezr(TARGET, ET0, FRAME, ABCORR, OBSERVER))

@route('/centermarstosun')
def center_marsToSun():
    '''
    Finds the position of the sun from the center of mars.
    Need the kernel that knows all the positions of the planets, satillites, ect

    param: NONE
    return: list (x,y,z) in km and light speed distance from target to observer
    rtype: list
    '''
    Abcorr = "NONE"
    Frame = "J2000"
    spkFiles()
    Et0 = 0.0
    Observer = "Mars"
    Target = "Sun"

    list = spy.spkezr(Observer, Et0, Frame, Abcorr, Target)
    postionList = (list[0][0], list[0][1], list[0][2], list[1])
    return json.dumps(postionList)


# center_marsToSun()

@get('/sphertocart')
def spherToCart():
    long = request.params.long
    lat = request.params.lat
    alt = request.params.alt
    '''
    Changes spherical(long,lat,alt) to cartensian(x,y,z) in km

    param: long, lat, alt type: float, float, float
    return: x,y,z return type: 6-Element Array of floats
    '''
    spkFiles()

    input_state = [float(long), float(lat), float(alt), 1.1626723557311027, 23.918409779910249, 10.939171726577502]
    input_coord_sys = 'PLANETOGRAPHIC'
    output_coord_sys = 'RECTANGULAR'
    body = 'Mars'

    tempList = spy.xfmsta(input_state, input_coord_sys, output_coord_sys, body)

    finalList = tempList[0], tempList[1], tempList[2]
    return json.dumps(finalList)


@get('/carttospher')
def cartToSpher():
    x = request.params.x
    y = request.params.y
    z = request.params.z
    '''
    Changes cartensian(x,y,z) in km to spherical(long,lat,alt)

    param: long, lat, alt type: float, float, float
    return: long,lat alt return type: 6-Element Array of floats
    '''
    spkFiles()

    input_state = [float(x), float(y), float(z), 1.1626723557311027, 23.918409779910249, 10.939171726577502]
    input_coord_sys = 'RECTANGULAR'
    output_coord_sys = 'PLANETOGRAPHIC'
    body = 'Mars'

    tempList = spy.xfmsta(input_state, input_coord_sys, output_coord_sys, body)

    finalList = tempList[0], tempList[1], tempList[2]
    return json.dumps(finalList)


# cartToSpher(3.44619000e+03,0,0)

@get('/marstosun')
def marsToSun():
    x = request.params.x
    y = request.params.y
    z = request.params.z
    '''
    Finds the direction of the sun in respect to a point on mars

    param obspos: Observer position relative to center of motion.
    type obspos: 3-Element Array of floats
    return: State of target with respect to observer, One way light time between target and observer.
    rtype:  list, direction of the sun in respect to a planet and light time
    '''
    spkFiles()

    Target = 'Sun'
    Et0 = 0.0
    outref = 'J2000'
    refloc = 'TARGET'
    Abcorr = "NONE"
    obspos = (float(x), float(y), float(z))
    obsctr = 'Mars'
    obsref = 'J2000'

    list = spy.spkcpo(Target, Et0, outref, refloc, Abcorr, obspos, obsctr, obsref)
    postionList = (list[0][0], list[0][1], list[0][2], list[1])
    return json.dumps(postionList)


# marsToSun(3446.1900000000001, -0.0, 0.0)

@route('/centerearthtosun')
def center_earthToSun():
    '''
    Finds the position of the sun from the center of earth.
    Need the kernel that knows all the positions of the planets, satillites, ect

    param: NONE
    return: list (x,y,z) in km and light speed distance from target to observer
    rtype: list
    '''
    Abcorr = "NONE"  #
    Frame = "J2000"  #
    spkFiles()
    Et0 = 0.0  #
    Observer = "Earth"  #
    Target = "Sun"  #

    list = spy.spkezr(Observer, Et0, Frame, Abcorr, Target)
    postionList = (list[0][0], list[0][1], list[0][2], list[1])
    return json.dumps(postionList)
 

# center_earthToSun()

@route('/sphertocartearth')
def spherToCartEarth():
    long = request.params.long
    lat = request.params.lat
    alt = request.params.alt
    '''
    Changes spherical(long,lat,alt) to cartensian(x,y,z) in km

    param: long, lat, alt type: float, float, float
    return: x,y,z return type: 6-Element Array of floats
    '''
    spkFiles()

    input_state = [float(long), float(lat), float(alt), 1.1626723557311027, 23.918409779910249, 10.939171726577502]
    input_coord_sys = 'PLANETOGRAPHIC'
    output_coord_sys = 'RECTANGULAR'
    body = 'Earth'

    tempList = spy.xfmsta(input_state, input_coord_sys, output_coord_sys, body)

    finalList = tempList[0], tempList[1], tempList[2]
    return json.dumps(finalList)

''''
@route('/earthtosun')
def earthToSun():
    spkFiles()
    Target = 'Sun'
    time = '2016 SEP 15 012:00:00.000000 UTC'
    outref = 'J2000'
    refloc = 'TARGET'
    Abcorr = "NONE"

    obspos = (6428.1400000000003, 0.0, 0.0)
    obsctr = 'Earth'
    obsref = 'J2000'

    Et0 = spy.str2et(time)
    list = spy.spkcpo(Target, Et0, outref, refloc, Abcorr, obspos, obsctr, obsref)
    postionList = (list[0][0], list[0][1], list[0][2], list[1])
    return str(postionList)
'''

run(host='localhost', port=8080, debug=True)
