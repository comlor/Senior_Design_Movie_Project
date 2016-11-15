

def inter(points):
    result = [[points[0][0], points[0][1], points[0][2]],]
    num_points = len(points)

    for pt in range(num_points):
        if pt+1 < num_points:
            dif_x = points[pt+1][0] - points[pt][0]
            dif_y = points[pt+1][1] - points[pt][1]
            dif_z = points[pt+1][2] - points[pt][2]
            print("dif_x: " + str(dif_x) + "   dif_y: " + str(dif_y) + "   dif_z: " + str(dif_z))
            offset = ( points[pt+1][3] - points[pt][3] ) * 24
            print("offset: " + str(offset))
            delta_x = dif_x / offset
            delta_y = dif_y / offset
            delta_z = dif_z / offset
            print("delta_x: " + str(dif_x) + "   delta_y: " + str(dif_y) + "   delta_z: " + str(dif_z))
            new_x = points[pt][0]
            new_y = points[pt][1]
            new_z = points[pt][2]

            for i in range(offset):
                new_x += delta_x
                new_y += delta_y
                new_z += delta_z
                result.append([new_x, new_y, new_z])
    return result

def main():
    points = [[150.000, -85.000, 100.000, 0], [150.000, -85.000, 200.000, 30], [225.000, -85.000, 225.000, 60], [300.000, -85.000, 275.000, 90]]

    the_path = inter(points)
    print(the_path)


if __name__ == "__main__":
    main()
