class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []
        self.states = set()

    def add(self, node, state):
        self.frontier.append(node)
        self.states.add(state)

    def contains_state(self, state):
        return state in self.states
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier.pop()
            self.states.remove(node.state)
            return node
        

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier.pop(0)
            self.states.remove(node.state)
            return node