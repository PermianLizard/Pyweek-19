class Scene(object):
    def __init__(self):
        pass

    def enter(self, **kwargs):
        print '%s: enter' % self.__class__.__name__

    def exit(self):
        print '%s: exit' % self.__class__.__name__

    def pause(self):
        print '%s: pause' % self.__class__.__name__

    def resume(self, **kwargs):
        print '%s: resume' % self.__class__.__name__

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