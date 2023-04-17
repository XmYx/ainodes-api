import torch
from diffusers import StableDiffusionPipeline

def load_diffusers(args=None):
    pipeline = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    return pipeline, None

def run_diffusers(node=None):

    input_node = node.inputs[0]
    node_id = node.parent.nodes[input_node].node_id

    pipeline = node.parent.values[node_id]
    pipeline.to("cuda")
    print(node.args)
    images = pipeline(prompt=node.args['prompt'], num_inference_steps=node.args['steps']).images
    pipeline.to("cpu")
    del pipeline
    print(node.inputs[0])
    return images, "send"



functions = {
    "load_diffusers": load_diffusers,
    "run_diffusers": run_diffusers,
}
