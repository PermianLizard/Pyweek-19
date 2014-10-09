mult = [
    [1, 0, 0, -1, -1, 0, 0, 1],
    [0, 1, -1, 0, 0, -1, 1, 0],
    [0, 1, 1, 0, 0, -1, -1, 0],
    [1, 0, 0, 1, -1, 0, 0, -1]
]


def do_fov(x, y, radius, data, sdata):
    map = Map(data)
    smap = Map(sdata)

    for oct in range(8):
        _cast_light(x, y, 1, 1.0, 0.0, radius,
                         mult[0][oct], mult[1][oct],
                         mult[2][oct], mult[3][oct], 0, map, smap)


def _cast_light(cx, cy, row, start, end, radius, xx, xy, yx, yy, id, map, smap):
    if start < end:
        return
    radius_squared = radius * radius
    for j in range(row, radius + 1):
        dx, dy = -j - 1, -j
        blocked = False
        while dx <= 0:
            dx += 1
            X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
            l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
            if start < r_slope:
                continue
            elif end > l_slope:
                break
            else:
                if dx * dx + dy * dy < radius_squared:
                    smap.set_tile(X, Y, True)

                tile = map.get_tile(X, Y)

                if blocked:
                    if not tile:
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        start = new_start
                else:
                    if not tile and j < radius:
                        blocked = True
                        _cast_light(cx, cy, j + 1, start, l_slope,
                                    radius, xx, xy, yx, yy, id + 1, map, smap)
                        new_start = r_slope
        if blocked:
            break


class Map:
    def __init__(self, data):
        self.data = data

    def get_tile(self, x, y):
        try:
            return self.data[y][x]
        except IndexError:
            return None

    def set_tile(self, x, y, value):
        try:
            self.data[y][x] = value
        except IndexError:
            pass

    def show(self):
        data = self.data
        for y in xrange(len(data)):
            for x in xrange(len(data[0])):
                if data[y][x]:
                    print '.',
                else:
                    print '#',
            print ''


def create_matrix(size, value=False):
    data = []
    for y in xrange(size[1]):
        row = []
        for x in xrange(size[0]):
            row.append(value)
        data.append(row)
    return data


if __name__ == '__main__':
    data = create_matrix((11, 11), True)
    sdata = create_matrix((11, 11))

    #data[1][1] = False
    data[4][4] = False
    data[3][4] = False
    data[4][3] = False
    data[6][6] = False

    do_fov(5, 5, 6, data, sdata)

    Map(data).show()
    print '---'
    Map(sdata).show()
