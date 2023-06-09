from typing import List, Dict, Any

from starlette.websockets import WebSocket

from . import create_pack, functions, nodes, DEBUG
class Graph:
    """
    A graph that represents a computation and its dependencies.

    The graph is composed of nodes and edges, where each node represents a function
    and each edge represents a data dependency between nodes.

    The graph is created by adding nodes to it and connecting them via their inputs and outputs.

    Once the graph is constructed, it can be executed by invoking the `run` method, which
    traverses the graph starting from a specified node and runs each node in the correct order.

    The graph can be updated by calling the `sync` method, which updates the existing nodes
    with new data and adds new nodes if necessary.
    """
    def __init__(self):
        self.send_images = None
        self.sid = None
        self.ws = None
        self.nodes = {}
        self.values = {}


    def add_node(self, node_id: str, node_type: str) -> None:
        """
        Adds a new node to the graph.

        Args:
            node_id (str): The unique identifier for the node.
            node_type (str): The type of the node, which determines its behavior.
            fn (callable): The function that the node represents.

        Returns:
            None
        """
        if DEBUG:
            print(f"Adding node with attrs:\n    node_id:{node_id}\n    {node_type}")
        node = nodes[node_type]
        self.nodes[node_id] = node(self, node_id, node_type)


    async def run(self, start_node_id:str) -> None:
        """
        Traverses the graph starting from the specified node and runs each node in the correct order.

        Args:
            start_node_id (str): The unique identifier of the node to start the traversal from.

        Returns:
            None
        """
        # Initialize visited set and stack for DFS traversal
        visited = set()
        stack = [start_node_id]

        if DEBUG:
            print(f"Running graph starting from node: {start_node_id}")
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

            # Run node only if it has at least one output:
            answer = None
            print("Running Node", node.node_id)
            self.values[node.node_id], answer = node.run()

            if answer:
                if answer == "send":
                    images = self.values[node.node_id]
                    await self.send_images(self.sid, node_id, images)
                    """images = self.values[node.node_id]
                    for image in images:
                        pack = create_pack(image, node_id)
                        print("Sending back pack", image)
                        await self.ws.send(pack)"""

            # Add connected nodes to the stack for traversal
            if node.outputs:
                for output_id in node.outputs:
                    output_node = self.nodes[output_id]
                    stack.append(output_node.node_id)
    def sync(self, json_data: List[Dict[str, Any]]):
        """
        Updates the existing nodes with new data and adds new nodes if necessary.

        Args:
            json_data (list): A list of dictionaries representing the updated nodes.

        Returns:
            None
        """
        existing_nodes = set(self.nodes.keys())

        for node_data in json_data:
            node_id = node_data['id']
            node_type = node_data['fn']
            inputs = node_data['inputs']
            outputs = node_data['outputs']
            args = node_data.get('args')
            #try:
            #    fn = functions[node_type]
            #except:
            #    fn = None
            if node_id in self.nodes:
                node = self.nodes[node_id]
                node.update(node_type, inputs, outputs, args)
                existing_nodes.remove(node_id)
            else:
                self.add_node(node_id, node_type)
                node = self.nodes[node_id]
                node.update(None, inputs, outputs, args)
        # Remove nodes that don't exist in the JSON data
        for node_id in existing_nodes:
            self.remove_node(node_id)
    def remove_node(self, node_id):
        del self.nodes[node_id]
        try:
            self.values[node_id].to("cpu")
        except:
            pass # We tried anyways
        del self.values[node_id]
        self.values[node_id] = None