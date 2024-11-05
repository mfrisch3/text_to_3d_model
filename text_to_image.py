from diffusers import StableDiffusionPipeline
import torch

class TextToImage:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4").to("cuda")


    # Disable safety checker
        self.pipe.safety_checker = None
    def generate_image(self, prompt, output_path="generated_image.png"):
        # Generate an image from text prompt
        image = self.pipe(prompt).images[0]
        image.save(output_path)
        return output_path
