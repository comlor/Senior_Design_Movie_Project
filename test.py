import math


def unitize(v):
    r = math.sqrt((v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2]))
    return v[0]/r, v[1]/r, v[2]/r


def azimuth(u):
    r = math.sqrt((u[0] * u[0]) + (u[1] * u[1]))
    azi = math.acos(u[0] / r)
    if math.atan2(u[1], u[0]) < 0:
        return 0 - azi
    else:
        return azi


def zenith(u):
    return math.atan2(u[0], u[2])


def main():
    sun = (132631314.56085943, 172288379.69373861, 75440807.460148022)
    uv = unitize(sun)
    print("Sun Unit Vector: " + str(uv))
    z_ang = zenith(uv)
    az_ang = azimuth(uv)

    print("Zenith: " + str(z_ang * (180 / math.pi)))
    print("Azimuth: " + str(az_ang * (180 / math.pi)))

if __name__ == "__main__":
    main()
