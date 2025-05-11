import click
import torch
from torchvision import models
from .visualizer import visualize_layers

def get_model(model_name):
    # Simple model loader for demo (expand as needed)
    if model_name == 'resnet18':
        return models.resnet18(pretrained=True)
    raise ValueError(f"Unknown model: {model_name}")

@click.command()
@click.option('--model', required=True, help='Model name, e.g. resnet18')
@click.option('--image', required=True, help='Path to input image')
def main(model, image):
    model_obj = get_model(model)
    visualize_layers(model=model_obj, input_image=image)

if __name__ == '__main__':
    main() 