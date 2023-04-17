class Node():
    def __init__(self, parent= None, node_id:str = None, node_type:str = None, fn = None):
        self.parent = parent
        self.node_id = node_id
        self.node_type = node_type
        self.fn = fn

    def run(self):
        if self.fn:
            return self.fn(self)

    def set_output(self, index, value):
        self.parent.values[f"{self.node_id}_{index}"] = value

    def get_output(self, index):
        return self.parent.values[f"{self.node_id}_{index}"]