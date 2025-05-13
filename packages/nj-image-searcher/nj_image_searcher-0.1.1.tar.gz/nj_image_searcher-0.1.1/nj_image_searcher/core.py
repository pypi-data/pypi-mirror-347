import requests
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from pathlib import Path


class ImageFinder:
    """A class to search and download images from the web based on a topic."""
    
    def __init__(self, output_dir="downloaded_images", max_images=10):
        """Initialize the image finder with output directory and max images to download."""
        self.output_dir = output_dir
        self.max_images = max_images
        self.ensure_output_dir()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def ensure_output_dir(self):
        """Create the output directory if it doesn't exist."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
    def search_images(self, query):
        """Search for images based on the provided query."""
        encoded_query = quote_plus(query)
        search_url = f"https://www.bing.com/images/search?q={encoded_query}&form=HDRSC2&first=1"
        
        try:
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()
            
            # Extract image URLs from the response
            image_urls = self._extract_image_urls(response.text)
            print(f"Found {len(image_urls)} images for '{query}'")
            return image_urls[:self.max_images]
            
        except requests.RequestException as e:
            print(f"Error searching for images: {e}")
            return []
    
    def _extract_image_urls(self, html_content):
        """Extract image URLs from HTML content."""
        image_urls = []
        # Look for image URLs in the HTML content
        start_markers = ['murl":"', '"contentUrl":"']
        for marker in start_markers:
            start_index = 0
            while True:
                start_index = html_content.find(marker, start_index)
                if start_index == -1:
                    break
                
                start_index += len(marker)
                end_index = html_content.find('"', start_index)
                
                if end_index != -1:
                    url = html_content[start_index:end_index].replace('\\', '')
                    if url.startswith('http') and (url.endswith('.jpg') or 
                                                  url.endswith('.jpeg') or 
                                                  url.endswith('.png') or 
                                                  url.endswith('.gif')):
                        image_urls.append(url)
                    start_index = end_index
                else:
                    break
        
        return list(set(image_urls))  # Remove duplicates
    
    def download_image(self, url, index, query):
        """Download an image from the given URL."""
        try:
            response = requests.get(url, headers=self.headers, stream=True, timeout=10)
            response.raise_for_status()
            
            # Get file extension from URL or content type
            if 'content-type' in response.headers and 'image' in response.headers['content-type']:
                ext = response.headers['content-type'].split('/')[-1]
                if ext == 'jpeg':
                    ext = 'jpg'
            else:
                ext = url.split('.')[-1]
                if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
                    ext = 'jpg'
            
            # Create filename and save the image
            sanitized_query = "".join(c if c.isalnum() else "_" for c in query)
            filename = f"{sanitized_query}_{index + 1}.{ext}"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Successfully downloaded: {filename}")
            return filepath
            
        except Exception as e:
            print(f"Error downloading image {index + 1}: {e}")
            return None
    
    def search_and_download(self, query):
        """Search for images and download them based on the query."""
        image_urls = self.search_images(query)
        
        if not image_urls:
            print(f"No images found for '{query}'")
            return []
        
        downloaded_files = []
        
        # Download images using a thread pool
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.download_image, url, i, query) 
                      for i, url in enumerate(image_urls)]
            
            for future in futures:
                result = future.result()
                if result:
                    downloaded_files.append(result)
                # Add a small delay to avoid being blocked
                time.sleep(random.uniform(0.5, 1.5))
        
        print(f"Downloaded {len(downloaded_files)} images for '{query}'")
        return downloaded_files