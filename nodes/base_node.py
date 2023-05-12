import torch
from diffusers import StableDiffusionPipeline
from platform import platform


class Node():
    def __init__(self, parent= None, node_id:str = None, node_type:str = None):
        self.parent = parent
        self.node_id = node_id
        self.node_type = node_type
    def update(self, node_type, inputs, outputs, args):
        if node_type is not None:
            self.node_type = node_type
        self.inputs = inputs
        self.outputs = outputs
        self.args = args
    def run(self):
        if self.fn:
            return self.fn()

    def set_output(self, index, value):
        self.parent.values[f"{self.node_id}_{index}"] = value

    def get_output(self, index):
        return self.parent.values[f"{self.node_id}_{index}"]

    def get_input_node(self):
        input_node = self.inputs[0]
        node = self.parent.nodes[input_node]
        return node

class DiffusersNode(Node):
    def __init__(self, parent=None, node_id=None, node_type=None):
        super().__init__(parent=parent, node_id=node_id, node_type=node_type)
        self.loaded = None

class SD_Node(Node):
    def __init__(self, parent=None, node_id=None, node_type=None):
        super().__init__(parent=parent, node_id=node_id, node_type=node_type)
        self.loaded = None
    
    def fn(self, args=None, **kwargs):
        if not self.loaded:
            mac = None
            if "MacOS" in platform():
                dtype = torch.float32
                mac = True
            else:
                dtype = torch.float16

            self.pipeline = StableDiffusionPipeline.from_pretrained("stablediffusionapi/illuminati-diffusion",
                                                                    torch_dtype=dtype)
            if mac:
                self.pipeline.to("mps")
                self.pipeline.enable_attention_slicing()
            else:
                self.pipeline.enable_model_cpu_offload()
            self.loaded = True
        images = self.pipeline(prompt=self.args['prompt'], num_inference_steps=int(self.args['num_inference_steps']),
                               width=768, height=768).images
        return_imgs = []
        for image in images:
            return_imgs.append(image)
        # node.pipeline.to("cpu")
        # node.set_output(0, copy.deepcopy(images))

        return return_imgs, None

class imageNode(Node):

    def __init__(self, parent=None, node_id=None, node_type=None):
        super().__init__(parent=parent, node_id=node_id, node_type=node_type)
        self.loaded = None

    def fn(self, args=None, **kwargs):
        node_id = self.get_input_node().node_id
        images = self.parent.values[node_id]
        return images, "send"


nodes = {"load_diffusers": DiffusersNode,
         "run_diffusers": Node,
         "imageNode": imageNode,
         "stableDiffusionNode": SD_Node}
