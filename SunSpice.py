import spiceypy as spy

def spkFiles():
    '''
    Loads the kernel that are needed for dertermining the calculations
    
    param: NONE
    return: none 
    '''
    
    SPK = ["C:\\Users\\Angel Jimenez\\Downloads\\de405.bsp"
           ,"C:\\Users\\Angel Jimenez\\Documents\\Senior Design\\pck00008.tpc.txt"]
    spy.furnsh(SPK)
    

def center_marsToSun():
    '''
    Finds the position of the sun from the center of mars.
    Need the kernel that knows all the positions of the planets, satillites, ect
    
    param: NONE 
    return: list (x,y,z) in km and light speed distance from target to observer
    rtype: list
    '''
    Abcorr = "NONE" 
    Frame  = "J2000" 
    spkFiles()
    Et0 = 0.0 
    Observer = "Mars" 
    Target = "Sun" 

    list = spy.spkezr( Observer, Et0, Frame, Abcorr, Target)
    postionList = (list[0][0],list[0][1], list[0][2], list[1])
    print(postionList)

#center_marsToSun()

def spherToCart(long, lat, alt):
    '''
    Changes spherical(long,lat,alt) to cartensian(x,y,z) in km
    
    param: long, lat, alt type: float, float, float
    return: x,y,z return type: 6-Element Array of floats
    '''
    spkFiles()
    
    input_state = [long,lat, alt ,1.1626723557311027, 23.918409779910249, 10.939171726577502]
    input_coord_sys = 'PLANETOGRAPHIC'
    output_coord_sys = 'RECTANGULAR'
    body = 'Mars'
    
    tempList = spy.xfmsta(input_state, input_coord_sys, output_coord_sys, body)
    
    finalList = tempList[0], tempList[1], tempList[2]
    print(finalList)

#spherToCart(0,0,50)

def cartToSpher(x,y,z):
    '''
    Changes cartensian(x,y,z) in km to spherical(long,lat,alt)
    
    param: long, lat, alt type: float, float, float
    return: long,lat alt return type: 6-Element Array of floats
    '''
    spkFiles()
    
    input_state = [x,y,z,1.1626723557311027, 23.918409779910249, 10.939171726577502]
    input_coord_sys = 'RECTANGULAR'
    output_coord_sys = 'PLANETOGRAPHIC'
    body = 'Mars'
    
    tempList = spy.xfmsta(input_state, input_coord_sys, output_coord_sys, body)
    
    finalList = tempList[0], tempList[1], tempList[2]
    print(finalList)
	
#cartToSpher(3.44619000e+03,0,0)

def marsToSun(x,y,z):
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
    obspos = (x,y,z)
    obsctr = 'Mars'
    obsref = 'J2000'
    
    list = spy.spkcpo(Target, Et0, outref, refloc, Abcorr, obspos, obsctr, obsref)
    postionList = (list[0][0],list[0][1], list[0][2], list[1])
    print(postionList)
    
#marsToSun(3446.1900000000001, -0.0, 0.0)

def center_earthToSun():
    '''
    Finds the position of the sun from the center of earth.
    Need the kernel that knows all the positions of the planets, satillites, ect
    
    param: NONE 
    return: list (x,y,z) in km and light speed distance from target to observer
    rtype: list
    '''
    Abcorr = "NONE" #
    Frame  = "J2000" #
    spkFiles()
    Et0 = 0.0 #
    Observer = "Earth" #
    Target = "Sun" #

    
    
    list = spy.spkezr( Observer, Et0, Frame, Abcorr, Target)
    postionList = (list[0][0],list[0][1], list[0][2], list[1])
    print(postionList)
    print(list)

#center_earthToSun()

def spherToCartEarth(long, lat, alt):
    '''
    Changes spherical(long,lat,alt) to cartensian(x,y,z) in km
    
    param: long, lat, alt type: float, float, float
    return: x,y,z return type: 6-Element Array of floats
    '''
    spkFiles()
    
    input_state = [long,lat, alt ,1.1626723557311027, 23.918409779910249, 10.939171726577502]
    input_coord_sys = 'PLANETOGRAPHIC'
    output_coord_sys = 'RECTANGULAR'
    body = 'Earth'
    
    tempList = spy.xfmsta(input_state, input_coord_sys, output_coord_sys, body)
    
    finalList = tempList[0], tempList[1], tempList[2]
    print(finalList)
	
spherToCartEarth(0,0,50)

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
    postionList = (list[0][0],list[0][1], list[0][2], list[1])
    print(postionList)

earthToSun()