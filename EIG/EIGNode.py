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

    def getParents(self):
        return self.parents

class EIGTree():
    def __init__(self, initialNode):
        self.tree = [[initialNode]]

    def __repr__(self):
        rep = ""
        for i in range(0, len(self.tree)):
            rep += "Level " + str(i) + ": " + str(self.tree[i]) + "\n"
        return rep

    def getNodeFromParents(self, parents):
        thisNode = self.getRoot()
        thisParents = None
        for i in range(1, len(parents)+1):
            thisParents = parents[:i]
            if thisNode.getChildren() == False:
                return thisNode
            for node in thisNode.getChildren():
                if node.getParents() == thisParents:
                    thisNode = node
        return thisNode



    def getRoot(self):
        return self.tree[0][0]

    def addLevel(self, nodes):
        self.tree.append(nodes)

    def getLevel(self, level):
        return self.tree[level]

    def printVals(self):
        for i in range(len(self.tree)):
            valList = []
            for node in self.tree[i]:
                valList.append(node.val)
            print("Level " + str(i) + ":  " + str(valList) + "\n")

    def printValsParents(self):
        for i in range(len(self.tree)):
            valList = []
            for node in self.tree[i]:
                parents = []
                for parent in node.getParents():
                    parents.append(parent.name)
                valList.append([node.val, parents])
            print("Level " + str(i) + ":  " + str(valList) + "\n")

    def printValsParentsInitialVals(self):
        for i in range(len(self.tree)):
            valList = []
            for node in self.tree[i]:
                parents = []
                for parent in node.parents():
                    parents.append(parent)
                valList.append([node.val, parents])
            print("Level " + str(i) + ":  " + str(valList) + "\n")