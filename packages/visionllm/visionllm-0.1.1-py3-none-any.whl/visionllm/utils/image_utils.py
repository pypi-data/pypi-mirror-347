"""
Utility functions for image processing.
"""

import os
from typing import Optional, Tuple, Union

try:
    from PIL import Image
    import numpy as np
except ImportError:
    raise ImportError(
        "Image processing utilities require Pillow and NumPy. "
        "Please install them with: pip install pillow numpy"
    )


def load_image(
    path_or_image: Union[str, "Image.Image", np.ndarray]
) -> "Image.Image":
    """
    Load an image from a file path or convert from numpy array.
    
    Args:
        path_or_image: File path, PIL Image, or numpy array
        
    Returns:
        PIL Image object
    """
    if isinstance(path_or_image, str):
        if not os.path.exists(path_or_image):
            raise FileNotFoundError(f"Image file not found: {path_or_image}")
        return Image.open(path_or_image).convert("RGB")
    elif isinstance(path_or_image, np.ndarray):
        return Image.fromarray(path_or_image.astype("uint8")).convert("RGB")
    elif hasattr(path_or_image, "mode"):  # Likely a PIL image
        return path_or_image.convert("RGB")
    else:
        raise TypeError(f"Unsupported image type: {type(path_or_image)}")


def save_image(
    image: "Image.Image", output_path: str, format: Optional[str] = None
) -> str:
    """
    Save an image to a file.
    
    Args:
        image: PIL Image to save
        output_path: Path to save the image to
        format: Optional image format override
        
    Returns:
        Path to the saved image
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    image.save(output_path, format=format)
    return output_path


def resize_image(
    image: "Image.Image", size: Tuple[int, int], keep_aspect: bool = True
) -> "Image.Image":
    """
    Resize an image to the specified dimensions.
    
    Args:
        image: PIL Image to resize
        size: Target (width, height)
        keep_aspect: Whether to maintain aspect ratio
        
    Returns:
        Resized PIL Image
    """
    if keep_aspect:
        image.thumbnail(size, Image.LANCZOS)
        return image
    else:
        return image.resize(size, Image.LANCZOS) 