import random
import pygame
import util


class GenInfo:
    def __init__(self, passability_map, room_areas):
        self.passability_map = passability_map
        self.room_areas = room_areas


class BspNode(object):
    def __init__(self, area, parent=None):
        self.area = area
        self.parent = parent
        self.left_child = None
        self.right_child = None
        self.room_area = None
        self.connections = {}

    @property
    def size(self):
        return self.area[2:]

    def connect(self, other, path):
        self.connections[other] = path
        other.connections[self] = list(reversed(path))

    def disconnect(self, other):
        del self.connections[other]
        del other.connections[self]

    def is_leaf(self):
        return self.left_child is None and self.right_child is None

    def get_sibling(self):
        parent = self.parent
        if parent is None:
            return None
        if self is parent.left_child:
            return parent.right_child
        if self is parent.right_child:
            return parent.left_child

    def grow(self, min_dimension, split_horiz=True):
        area = self.area

        if split_horiz:
            if area.width <= min_dimension:
                return
            split_line = int(area.width * random.uniform(0.45, 0.55))

            left_area = pygame.Rect(area.x, area.y, split_line, area.height)
            right_area = pygame.Rect(area.x + split_line, area.y, area.width - split_line, area.height)
        else:
            if area.height <= min_dimension:
                return
            split_line = int(area.height * random.uniform(0.45, 0.55))

            left_area = pygame.Rect(area.x, area.y, area.width, split_line)
            right_area = pygame.Rect(area.x, area.y + split_line, area.width, area.height - split_line)

        self.left_child = BspNode(left_area, self)
        self.right_child = BspNode(right_area, self)

        self.left_child.grow(min_dimension, not split_horiz)
        self.right_child.grow(min_dimension, not split_horiz)

    def make_rooms(self, coll=None):
        if coll is None:
            coll = []
        if self.is_leaf():
            self.room_area = self.area.inflate(-3, -3)
            coll.append(self.room_area)
        else:
            if self.left_child:
                self.left_child.make_rooms(coll)
            if self.right_child:
                self.right_child.make_rooms(coll)
        return coll

    def cull_rooms(self, min_rooms):
        leaves = self.collect_leaves()
        random.shuffle(leaves)
        while len(leaves) > min_rooms:
            leaves.pop().room_area = None

    def connect_rooms(self, max_distance, connect_chance):
        if self.is_leaf():
            sibling = self.get_sibling()
            if self.room_area is not None and sibling.room_area is not None:
                if sibling not in self.connections.keys():
                    path = get_path(self.room_area, sibling.room_area)
                    self.connect(sibling, path)
        else:
            if self.left_child is not None:
                self.left_child.connect_rooms(max_distance, connect_chance)

            if self.right_child is not None:
                self.right_child.connect_rooms(max_distance, connect_chance)

            if self.parent:
                a_leaves = self.collect_leaves()
                b_leaves = self.get_sibling().collect_leaves()

                if len(a_leaves) == 0 or len(b_leaves) == 0:
                    return

                pairs = []
                for a_leaf in a_leaves:
                    if a_leaf.room_area is None:
                        continue

                    for b_leaf in b_leaves:
                        if b_leaf.room_area is None:
                            continue

                        a_area = a_leaf.area
                        b_area = b_leaf.area

                        dist = util.distance(a_area.center, b_area.center)
                        pairs.append((a_leaf, b_leaf, dist))

                pairs.sort(key=lambda x: x[2])

                if len(pairs):
                    pair = pairs[0]
                    a, b, dist = pair
                    del pairs[0]
                    path = get_path(a.room_area, b.room_area)
                    a.connect(b, path)

                for pair in pairs:
                    a, b, dist = pair
                    if dist > max_distance:
                        break
                    if random.random() < connect_chance:
                        path = get_path(a.room_area, b.room_area)
                        a.connect(b, path)

    def clean_crappy_connections(self):
        leaves = self.collect_leaves()

        leaf_padded_rooms = {}
        for leaf in leaves:
            if leaf.room_area:
                leaf_padded_rooms[leaf] = leaf.room_area.inflate(2, 2)

        for leaf in leaves:
            to_remove = set()
            for other, path in leaf.connections.iteritems():
                for owner_leaf, padded_room in leaf_padded_rooms.iteritems():
                    if owner_leaf is leaf or owner_leaf is other:
                        continue

                    for point in path:
                        if padded_room.collidepoint(point):
                            to_remove.add(other)

            for other in to_remove:
                leaf.disconnect(other)

    def get_data(self):
        data = create_matrix(self.size)
        self.imprint_rooms(data)
        self.imprint_connections(data)
        return data

    def imprint_rooms(self, data):
        leaves = self.collect_leaves()
        for leaf in leaves:
            if leaf.room_area:
                imprint_matrix(data, leaf.room_area, True)

    def imprint_connections(self, data):
        if self.left_child is not None:
            self.left_child.imprint_connections(data)
        if self.right_child is not None:
            self.right_child.imprint_connections(data)

        for other, path in self.connections.iteritems():
            imprint_path(data, path, True)

    def collect_leaves(self, coll=None):
        if coll is None:
            coll = []
        if self.left_child is not None:
            self.left_child.collect_leaves(coll)
        if self.right_child is not None:
            self.right_child.collect_leaves(coll)
        if self.is_leaf():
            coll.append(self)
        return coll

    def collect_rooms(self, coll=None):
        if coll is None:
            coll = []
        if self.left_child is not None:
            self.left_child.collect_rooms(coll)
        if self.right_child is not None:
            self.right_child.collect_rooms(coll)
        if self.is_leaf() and self.room_area is not None:
            coll.append(self.room_area)
        return coll


def generate(size, min_node_area=12, room_cull=0.4, room_connect_chance=0.75, seed=None):
    if seed is not None:
        random.seed(seed)

    root = BspNode(pygame.Rect((0, 0) + size))
    root.grow(min_node_area)

    rooms = root.make_rooms()
    root.cull_rooms(int(len(rooms) * room_cull))

    max_room_connect_distance = min_node_area * 2

    root.connect_rooms(max_room_connect_distance, room_connect_chance)
    root.clean_crappy_connections()

    passability_map = root.get_data()
    room_areas = root.collect_rooms()

    return GenInfo(passability_map, room_areas)


def imprint_horiz(data, x1, x2, y, value):
    path = get_horiz_path(x1, x2, y)
    for x, y in path:
        data[y][x] = value


def imprint_vert(data, y1, y2, x, value):
    path = get_vert_path(y1, y2, x)
    for x, y in path:
        data[y][x] = value


def imprint_path(data, path, value):
    for x, y in path:
        data[y][x] = value


def imprint_matrix(data, area, value):
    for y in xrange(area.top, area.bottom):
        for x in xrange(area.left, area.right):
            data[y][x] = value


def get_path(a_area, b_area):
    path = []

    if a_area.centerx == b_area.centerx:
        path = get_vert_path(a_area.centery, b_area.centery, a_area.centerx)
    elif a_area.centery == b_area.centery:
        path = get_horiz_path(a_area.centerx, b_area.centerx, a_area.centery)
    else:
        a_xs = set(range(a_area.left, a_area.right))
        b_xs = set(range(b_area.left, b_area.right))

        a_ys = set(range(a_area.top, a_area.bottom))
        b_ys = set(range(b_area.top, b_area.bottom))

        x_intersect = a_xs.intersection(b_xs)
        y_intersect = a_ys.intersection(b_ys)

        if len(x_intersect) > 0:
            x_list = list(sorted(x_intersect))
            x = x_list[len(x_list) // 2]
            ys = (a_area.centery, b_area.centery)
            start_y = min(ys)
            end_y = max(ys)
            path = get_vert_path(start_y, end_y, x)
        elif len(y_intersect) > 0:
            y_list = list(sorted(y_intersect))
            y = y_list[len(y_list) // 2]
            xs = (a_area.centerx, b_area.centerx)
            start_x = min(xs)
            end_x = max(xs)
            path = get_horiz_path(start_x, end_x, y)
        else:
            dx = a_area.centerx - b_area.centerx
            dy = a_area.centery - b_area.centery
            if abs(dx) > abs(dy):
                if dx < 0:
                    return path
                path = get_horiz_path(a_area.centerx, b_area.centerx, a_area.centery)
                path += get_vert_path(a_area.centery, b_area.centery, b_area.centerx)
            else:
                if dy < 0:
                    return path
                path = get_vert_path(a_area.centery, b_area.centery, a_area.centerx)
                path += get_horiz_path(a_area.centerx, b_area.centerx, b_area.centery)

    return path


def get_horiz_path(x1, x2, y):
    path = []
    if x1 > x2:
        x_start = x2
        x_end = x1
    elif x1 < x2:
        x_start = x1
        x_end = x2
    else:
        return path

    for x in xrange(x_start, x_end):
        path.append((x, y))

    return path


def get_vert_path(y1, y2, x):
    path = []
    if y1 > y2:
        y_start = y2
        y_end = y1
    elif y1 < y2:
        y_start = y1
        y_end = y2
    else:
        return path

    for y in xrange(y_start, y_end):
        path.append((x, y))

    return path


def create_matrix(size, value=False):
    data = []
    for y in xrange(size[1]):
        row = []
        for x in xrange(size[0]):
            row.append(value)
        data.append(row)
    return data
