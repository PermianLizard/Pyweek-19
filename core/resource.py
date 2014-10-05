import os


class ResourceCache(object):
    def __init__(self):
        self._cache = {}

    def register(self, name, loader):
        self._cache[name] = loader(name)

    def get(self, name):
        return self._cache[name]


class FileResourceCache(ResourceCache):
    def __init__(self, root_directory):
        super(FileResourceCache, self).__init__()
        self.root_directory = root_directory

    def register(self, name, loader):
        self._cache[name] = loader(os.path.join(self.root_directory, name))


class TiledImageResourceCache(FileResourceCache):
    def __init__(self, root_directory, tile_size=None):
        super(TiledImageResourceCache, self).__init__(root_directory)
        self.tile_size = tile_size

    def get_tile(self, name, pos, tile_size=None):
        if tile_size is None:
            tile_size = self.tile_size
        img = self.get(name)
        tw, th = tile_size
        return img.subsurface((pos[0] * tw, pos[1] * th, tw, th))


class FontResourceCache(object):
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self._cache = {}

    def register(self, name, loader, font_size):
        self._cache['%s-%s' % (name, font_size)] = loader(os.path.join(self.root_directory, name), font_size)

    def get(self, name, font_size):
        return self._cache['%s-%s' % (name, font_size)]