import argparse
from .core import ImageFinder

def main():
    """Command-line interface for the image finder package."""
    parser = argparse.ArgumentParser(description='Search and download images based on a topic')
    parser.add_argument('query', type=str, help='The search query/topic for images')
    parser.add_argument('--output', '-o', type=str, default='downloaded_images', 
                        help='Output directory for downloaded images')
    parser.add_argument('--max', '-m', type=int, default=10, 
                        help='Maximum number of images to download')
    
    args = parser.parse_args()
    
    finder = ImageFinder(output_dir=args.output, max_images=args.max)
    finder.search_and_download(args.query)

if __name__ == "__main__":
    main()