from PIL import Image
import numpy as np
import torch
import torchvision.transforms as T

def load_image(img, size=224):
    """
    Loads and preprocesses an image for a PyTorch model.
    Accepts file path, PIL.Image, or np.ndarray.
    Returns a torch.Tensor of shape (1, C, H, W)
    """
    if isinstance(img, str):
        img = Image.open(img).convert('RGB')
    elif isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    # Resize and normalize
    transform = T.Compose([
        T.Resize((size, size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    tensor = transform(img).unsqueeze(0)
    return tensor 