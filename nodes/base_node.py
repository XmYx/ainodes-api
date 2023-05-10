class Node():
    def __init__(self, parent= None, node_id:str = None, node_type:str = None, fn = None):
        self.parent = parent
        self.node_id = node_id
        self.node_type = node_type
        self.fn = fn
    def update(self, node_type, inputs, outputs, fn, args):
        if node_type is not None:
            self.node_type = node_type
        self.inputs = inputs
        self.outputs = outputs
        self.fn = fn
        self.args = args
    def run(self):
        if self.fn:
            return self.fn(self)

    def set_output(self, index, value):
        self.parent.values[f"{self.node_id}_{index}"] = value

    def get_output(self, index):
        return self.parent.values[f"{self.node_id}_{index}"]

    def get_input_node(self):
        input_node = self.inputs[0]
        node = self.parent.nodes[input_node]
        return node

class DiffusersNode(Node):
    def __init__(self, parent=None, node_id=None, node_type=None, fn=None):
        super().__init__(parent=parent, node_id=node_id, node_type=node_type, fn=fn)
        self.loaded = None

class SD_Node(Node):
    def __init__(self, parent=None, node_id=None, node_type=None, fn=None):
        super().__init__(parent=parent, node_id=node_id, node_type=node_type, fn=fn)
        self.loaded = None



nodes = {"load_diffusers": DiffusersNode,
         "run_diffusers": Node,
         "imageNode": Node,
         "stableDiffusionNode": SD_Node}
