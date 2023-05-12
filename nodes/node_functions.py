import copy

import torch
from diffusers import StableDiffusionPipeline

def load_diffusers(node=None):
    if not node.loaded:
        pipeline = StableDiffusionPipeline.from_pretrained("stablediffusionapi/illuminati-diffusion", torch_dtype=torch.float16).to("cuda")
        pipeline.enable_model_cpu_offload()
        return pipeline, None
    else:
        return node.parent.values[node.node_id], None

def run_diffusers(node=None):
    node_id = node.get_input_node().node_id
    images = node.parent.values[node_id](prompt=node.args['prompt'], num_inference_steps=node.args['steps'], width=768, height=768).images
    return images, "send"

def stableDiffusionNode(node=None):
    if not node.loaded:
        node.pipeline = StableDiffusionPipeline.from_pretrained("stablediffusionapi/illuminati-diffusion", torch_dtype=torch.float16)
        node.pipeline.enable_model_cpu_offload()
        node.loaded = True
    images = node.pipeline(prompt=node.args['prompt'], num_inference_steps=int(node.args['num_inference_steps']), width=768, height=768).images
    return_imgs = []
    for image in images:
        return_imgs.append(image)
    #node.pipeline.to("cpu")
    #node.set_output(0, copy.deepcopy(images))

    return return_imgs, None

def imageNode(node=None):
    node_id = node.get_input_node().node_id
    images = node.parent.values[node_id]
    return images, "send"

functions = {
    "load_diffusers": load_diffusers,
    "run_diffusers": run_diffusers,
    "stableDiffusionNode":stableDiffusionNode,
    "imageNode": imageNode
}
