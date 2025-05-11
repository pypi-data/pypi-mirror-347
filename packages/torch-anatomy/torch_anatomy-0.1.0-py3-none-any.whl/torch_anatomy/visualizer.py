import torch
import torchvision
import matplotlib
matplotlib.use('Agg')  # Set backend to non-interactive
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
from .utils import load_image

def get_activation(name):
    """Hook to get activations from a layer"""
    def hook(model, input, output):
        activations[name] = output.detach()
    return hook

def visualize_layers(
    model,
    input_image,
    layers_to_show=None,
    save_dir=None,
    show=True,
    channels_per_layer=4,
    colormap='viridis',
    show_colorbar=False
):
    """
    Visualize intermediate activations of a PyTorch CNN model layer-by-layer.
    Args:
        model: PyTorch model (nn.Module)
        input_image: Path to image or PIL.Image or np.ndarray
        layers_to_show: List of layer names/types to visualize (default: Conv, ReLU, Pool)
        save_dir: If provided, saves images to this directory
        show: If True, displays the plots
        channels_per_layer: Number of channels to show per layer (default: 4)
        colormap: Matplotlib colormap to use (default: 'viridis')
        show_colorbar: Whether to show colorbar (default: False)
    """
    global activations
    activations = {}
    
    # Default layers to show if none specified
    if layers_to_show is None:
        layers_to_show = ['Conv2d', 'ReLU', 'MaxPool2d']
    
    # Register hooks for all layers
    hooks = []
    for name, layer in model.named_modules():
        if any(layer_type in str(type(layer)) for layer_type in layers_to_show):
            hooks.append(layer.register_forward_hook(get_activation(name)))
    
    # Load and preprocess image
    input_tensor = load_image(input_image)
    
    # Forward pass
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
    
    # Remove hooks
    for hook in hooks:
        hook.remove()
    
    # Create visualization
    n_layers = len(activations)
    if n_layers == 0:
        print("No matching layers found!")
        return
    
    # Prepare input image for display
    if isinstance(input_image, str):
        img_disp = Image.open(input_image).convert('RGB')
    elif isinstance(input_image, np.ndarray):
        img_disp = Image.fromarray(input_image)
    else:
        img_disp = input_image
    
    # Calculate grid size
    n_cols = channels_per_layer
    n_rows = n_layers + 1  # +1 for input image
    
    plt.figure(figsize=(4*n_cols, 4*n_rows))
    
    # Plot input image
    plt.subplot(n_rows, n_cols, 1)
    plt.imshow(img_disp)
    plt.title('Input Image')
    plt.axis('off')
    if show_colorbar:
        plt.colorbar()
    # Fill rest of first row with blanks if channels_per_layer > 1
    for i in range(2, n_cols+1):
        plt.subplot(n_rows, n_cols, i)
        plt.axis('off')
    
    # Plot each layer's activations (top N channels)
    for row_idx, (name, activation) in enumerate(activations.items(), 1):
        n_ch = activation.shape[1]
        for ch in range(min(channels_per_layer, n_ch)):
            plt.subplot(n_rows, n_cols, row_idx*n_cols + ch + 1)
            act = activation[0, ch].cpu().numpy()
            act = (act - act.min()) / (act.max() - act.min() + 1e-8)
            im = plt.imshow(act, cmap=colormap)
            plt.title(f'{name}\nChannel {ch} | Shape: {activation.shape}')
            plt.axis('off')
            if show_colorbar:
                plt.colorbar(im, fraction=0.046, pad=0.04)
        # If channels_per_layer > n_ch, fill rest with blanks
        for ch in range(n_ch, channels_per_layer):
            plt.subplot(n_rows, n_cols, row_idx*n_cols + ch + 1)
            plt.axis('off')
    
    plt.tight_layout()
    
    # Save if directory provided
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        plt.savefig(os.path.join(save_dir, 'layer_visualizations.png'))
        print(f"Visualizations saved to {save_dir}/layer_visualizations.png")
    
    # Show plot
    if show:
        try:
            plt.show()
        except Exception as e:
            print(f"Could not display plot: {e}")
            print("But the visualization has been saved to the output directory!")
    else:
        plt.close() 