class ActionComp:
    def __init__(self, speed):
        self.speed = speed
        self.action_stack = []
        self.delay = 0

    def top_action(self):
        action_stack = self.action_stack
        if action_stack:
            return action_stack[-1]
        return None

    def push_action(self, action):
        self.action_stack.append(action)

    def swap_action(self, action):
        action_stack = self.action_stack
        if action_stack:
            action_stack.pop()
        action_stack.append(action)

    def pop_action(self):
        action_stack = self.action_stack
        if action_stack:
            action_stack.pop()