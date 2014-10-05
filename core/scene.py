class SceneLayer(object):
    def __init__(self):
        self.scene = None

    def enter(self, **kwargs):
        pass

    def exit(self):
        pass

    def pause(self):
        pass

    def resume(self, **kwargs):
        pass

    def update(self, dt):
        pass

    def draw(self, surf):
        pass

    def on_key_down(self, key, mod):
        pass

    def on_key_up(self, key, mod):
        pass

    def on_mouse_motion(self, pos, rel, buttons):
        pass

    def on_mouse_button_down(self, pos, button):
        pass

    def on_mouse_button_up(self, pos, button):
        pass

class Scene(object):
    def __init__(self, layers=[]):
        self.layers = layers[:]

    def enter(self, **kwargs):
        print '%s: enter' % self.__class__.__name__
        for layer in self.layers:
            layer.enter(**kwargs)

    def exit(self):
        print '%s: exit' % self.__class__.__name__
        for layer in self.layers:
            layer.exit()

    def pause(self):
        print '%s: pause' % self.__class__.__name__
        for layer in self.layers:
            layer.pause()

    def resume(self, **kwargs):
        print '%s: resume' % self.__class__.__name__
        for layer in self.layers:
            layer.resume(**kwargs)

    def update(self, dt):
        for layer in self.layers:
            layer.update(dt)

    def draw(self, surf):
        for layer in self.layers:
            layer.draw(surf)

    def on_key_down(self, key, mod):
        for layer in self.layers:
            layer.on_key_down(key, mod)

    def on_key_up(self, key, mod):
        for layer in self.layers:
            layer.on_key_up(key, mod)

    def on_mouse_motion(self, pos, rel, buttons):
        for layer in self.layers:
            layer.on_mouse_motion(pos, rel, buttons)

    def on_mouse_button_down(self, pos, button):
        for layer in self.layers:
            layer.on_mouse_button_down(pos, button)

    def on_mouse_button_up(self, pos, button):
        for layer in self.layers:
            layer.on_mouse_button_up(pos, button)


class SceneDirector(object):
    def __init__(self):
        self.stack = []

    def top(self):
        return self.stack[-1] if self.stack else None

    def push(self, scene, **kwargs):
        top = self.top()
        if top:
            top.pause()
        self.stack.append(scene)
        scene.enter(**kwargs)

    def pop(self, **kwargs):
        popped = None
        if self.top():
            popped = self.stack.pop()
            popped.exit()
        top = self.top()
        if top:
            top.resume(**kwargs)
        return popped

    def swap(self, scene, **kwargs):
        old = self.stack.pop() if self.stack else None
        if old:
            old.exit()
        self.stack.append(scene)
        scene.enter(**kwargs)
        return old