from . import create_pack, functions, Node
class Graph:
    def __init__(self, ws):

        self.ws = ws
        self.nodes = {}
        self.values = {}

    def add_node(self, node_id, node_type, fn):
        self.nodes[node_id] = Node(self, node_id, node_type, fn)

    async def run(self, start_node_id):
        # Initialize visited set and stack for DFS traversal
        visited = set()
        stack = [start_node_id]

        # Traverse the graph from the start node
        while stack:
            # Get the next node from the stack
            node_id = stack.pop()

            # Skip if node has already been visited
            if node_id in visited:
                continue

            # Mark node as visited and run it
            visited.add(node_id)
            node = self.nodes[node_id]

            # Run node only if it has at least one output and all its inputs have values
            #if node.outputs:
            self.values[node.node_id], answer = node.run()
            print(type(self.values[node.node_id]))

            if answer == 'send':
                images = self.values[node.node_id]
                for image in images:
                    pack = create_pack(image, node_id)
                    await self.ws.send_bytes(pack)

            # Add connected nodes to the stack for traversal
            for output_id in node.outputs:
                output_node = self.nodes[output_id]
                stack.append(output_node.node_id)
    def sync(self, json_data):
        existing_nodes = set(self.nodes.keys())

        for node_data in json_data:
            args = None
            node_id = node_data['id']
            node_type = node_data['type']
            inputs = node_data['inputs']
            outputs = node_data['outputs']
            fn_name = node_data['fn']
            if "args" in node_data:
                args = node_data['args']
            fn = functions[fn_name]
            if node_id in self.nodes:
                node = self.nodes[node_id]
                node.args = args
                node.node_type = node_type
                node.inputs = []
                for input in inputs:
                    node.inputs.append(input)
                node.outputs = []
                for output in outputs:
                    node.outputs.append(output)
                node.fn = fn
                existing_nodes.remove(node_id)
            else:
                self.add_node(node_id, node_type, fn)
                node = self.nodes[node_id]
                node.args = args
                node.inputs = inputs
                node.outputs = outputs
        # Remove nodes that don't exist in the JSON data
        for node_id in existing_nodes:
            del self.nodes[node_id]
            try:
                self.values[node_id].to("cpu")
            except:
                pass # We tried anyways
            del self.values[node_id]
            self.values[node_id] = None