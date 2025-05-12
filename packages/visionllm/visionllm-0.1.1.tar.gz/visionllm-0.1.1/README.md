# VisionLLM

A modular Python library for vision-based interactions with AI systems, providing text-to-image, image-to-image, text-to-video, and image-to-video capabilities.

CAUTION : this project is under development and contains mostly placeholder. Please do not use yet.

## Features

* **Text-to-Image**: Generate images from text prompts
* **Image-to-Image**: Transform images based on text guidance
* **Text-to-Video**: Create videos from text descriptions
* **Image-to-Video**: Animate still images into videos
* **Modular Design**: Easily integrate with any text generation system
* **MLX Integration**: Special optimizations for Apple Silicon

## Installation

```bash
# Install from PyPI
pip install visionllm

# Or clone the repository
git clone https://github.com/lpalbou/visionllm.git
cd visionllm
pip install -e .
```

### Development Installation

```bash
# Install with development dependencies
pip install "visionllm[dev]"
```

## Quick Start

```python
from visionllm import VisionManager

# Initialize vision manager
vision_manager = VisionManager(debug_mode=False)

# Text to image
image = vision_manager.text_to_image(
    "A beautiful sunset over mountains with a lake in the foreground"
)

# Image to video
video = vision_manager.image_to_video(
    image, 
    prompt="Add gentle ripples to the lake and clouds moving slowly",
    duration=5.0
)

# Clean up
vision_manager.cleanup()
```

## Command Line Usage

VisionLLM provides a command-line interface for quick access to its capabilities:

```bash
# Generate an image from text
visionllm text2image "A beautiful sunset over mountains" --output sunset.png

# Transform an image
visionllm image2image input.png --prompt "Make it look like winter" --output winter.png

# Generate a video from text
visionllm text2video "A timelapse of a blooming flower" --duration 10.0 --output flower.mp4

# Animate an image into a video
visionllm image2video portrait.png --prompt "Make the subject smile" --output smile.mp4
```

## Integration with AbstractLLM

VisionLLM is designed to work seamlessly with AbstractLLM for unified access to various AI models:

```python
from abstractllm import LLMClient
from visionllm import VisionManager

# Initialize components
llm_client = LLMClient(provider="openai", model="gpt-4")
vision_manager = VisionManager()

# Generate an image based on LLM output
prompt = "Describe a fantasy landscape"
description = llm_client.generate(prompt)
image = vision_manager.text_to_image(description)

# Process the image further
video = vision_manager.image_to_video(image, prompt="Add magical effects")
```

## License

VisionLLM is licensed under the MIT License.

## Acknowledgments

This project is inspired by [VoiceLLM](https://github.com/lpalbou/VoiceLLM) and is designed to work as a companion library focusing on vision-based AI interactions.

## Author

Laurent-Philippe Albou (24249870+lpalbou@users.noreply.github.com)

## Version

Current version: 0.1.1 