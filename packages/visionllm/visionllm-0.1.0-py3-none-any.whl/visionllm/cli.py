"""
Command-line interface for VisionLLM.
"""

import argparse
import sys
from .vision_manager import VisionManager

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="VisionLLM - Vision-based AI interactions")
    
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--version", action="store_true", help="Show version information")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Text to image command
    t2i_parser = subparsers.add_parser("text2image", help="Generate image from text")
    t2i_parser.add_argument("prompt", help="Text prompt for image generation")
    t2i_parser.add_argument("--output", "-o", help="Output file path")
    
    # Image to image command
    i2i_parser = subparsers.add_parser("image2image", help="Transform an image")
    i2i_parser.add_argument("image", help="Input image path")
    i2i_parser.add_argument("--prompt", "-p", help="Optional text prompt for guidance")
    i2i_parser.add_argument("--output", "-o", help="Output file path")
    
    # Text to video command
    t2v_parser = subparsers.add_parser("text2video", help="Generate video from text")
    t2v_parser.add_argument("prompt", help="Text prompt for video generation")
    t2v_parser.add_argument("--duration", "-d", type=float, default=5.0, help="Video duration in seconds")
    t2v_parser.add_argument("--output", "-o", help="Output file path")
    
    # Image to video command
    i2v_parser = subparsers.add_parser("image2video", help="Generate video from image")
    i2v_parser.add_argument("image", help="Input image path")
    i2v_parser.add_argument("--prompt", "-p", help="Optional text prompt for guidance")
    i2v_parser.add_argument("--duration", "-d", type=float, default=5.0, help="Video duration in seconds")
    i2v_parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    # Handle version display
    if args.version:
        from . import __version__
        print(f"VisionLLM version {__version__}")
        return 0
    
    # Initialize vision manager
    vision_manager = VisionManager(debug_mode=args.debug)
    
    # Handle commands
    if args.command == "text2image":
        print(f"Text-to-image: {args.prompt}")
        print("This functionality is not yet implemented.")
    elif args.command == "image2image":
        print(f"Image-to-image: {args.image} with prompt: {args.prompt}")
        print("This functionality is not yet implemented.")
    elif args.command == "text2video":
        print(f"Text-to-video: {args.prompt}, duration: {args.duration}s")
        print("This functionality is not yet implemented.")
    elif args.command == "image2video":
        print(f"Image-to-video: {args.image} with prompt: {args.prompt}, duration: {args.duration}s")
        print("This functionality is not yet implemented.")
    else:
        parser.print_help()
    
    # Clean up resources
    vision_manager.cleanup()
    return 0

if __name__ == "__main__":
    sys.exit(main()) 