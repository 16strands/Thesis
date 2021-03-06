##############
## EIG Tree ##
##############

class EIGNode():
    def __init__(self, val, parents, round):
        self.val = val # Value transmitted
        self.parents = parents # List of processes who signed off on this value
        self.round = round

    def __repr__(self):
        rep = "val: " + str(self.val) + ", parents: " + str(self.parents)
        return rep

    # def __repr__(self):
    #     rep = "val: " + str(self.val) + ", round: " + str(self.round)
    #     return rep

    # def __repr__(self):
    #     return str(self.val)

    def getParents(self):
        return self.parents

    def getParentsString(self):
        ret = ""
        for parent in self.parents:
            ret = ret + str(parent.name)
        return ret

    def getGrandparentsString(self):
        ret = ""
        if (len(self.parents) == 1):
            return "root"
        for i in range(len(self.parents) - 1):
            ret = ret + str(self.parents[i].name)
        return ret

    def getGreatGrandparentsString(self):
        ret = ""
        if (len(self.parents) <= 2):
            return "root"
        for i in range(len(self.parents) - 2):
            ret = ret + str(self.parents[i].name)
        return ret