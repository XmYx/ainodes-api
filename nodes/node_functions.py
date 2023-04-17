import torch
from diffusers import StableDiffusionPipeline

def load_diffusers(node=None):
    if not node.loaded:
        pipeline = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        return pipeline, None
    else:
        return node.parent.values[node.node_id], None

def run_diffusers(node=None):

    node_id = node.get_input_node().node_id

    node.parent.values[node_id].to("cuda")

    images = node.parent.values[node_id](prompt=node.args['prompt'], num_inference_steps=node.args['steps']).images

    node.parent.values[node_id].to("cpu")

    return images, "send"



functions = {
    "load_diffusers": load_diffusers,
    "run_diffusers": run_diffusers,
}
