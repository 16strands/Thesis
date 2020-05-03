


tree = Tree()
node = EIGNode(self.initialValue, [self], 0)
tree.create_node("root", "root", data=node)
for process in network.getProcesses():
    if process.name != self.name:
        node = EIGNode(None, [process], 0)
        tree.create_node(process.name, process.name, data=node)