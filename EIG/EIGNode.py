## EIG Node ##

# This isn't a tree in the typical sense but this seems to be what the paper does

class EIGNode():
    def __init__(self, val, parents):
        self.val = val # Value transmitted
        self.parents = parents # List of processes who signed off on this value
        self.children = []

    def __repr__(self):
        rep = "val: " + str(self.val) + ", parents: " + str(self.parents)
        return rep

    def updateChildren(self, node):
        self.children.append(node)

    def getChildren(self):
        if len(self.children) > 0:
            return self.children
        else:
            return False

class EIGTree():
    def __init__(self, initialNode):
        self.tree = [[initialNode]]

    def __repr__(self):
        rep = ""
        for i in range(0, len(self.tree)):
            rep += "Level " + str(i) + ": " + str(self.tree[i]) + "\n"
        return rep

    def getRoot(self):
        return self.tree[0][0]

    def addLevel(self, nodes):
        self.tree.append(nodes)

    def getLevel(self, level):
        return self.tree[level]