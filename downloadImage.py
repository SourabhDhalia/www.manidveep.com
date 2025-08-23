import os
import requests
from bs4 import BeautifulSoup

# Directory to save images
IMAGE_DIR = "assets/images"

# Automatically generate the list of HTML files in the current directory and subdirectories
HTML_FILES = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            HTML_FILES.append(os.path.join(root, file))

# Base URL of your GitHub Pages site
BASE_URL = "https://sourabhdhalia.github.io/www.manidveep.com/"

# Function to download an image

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as out_file:
                for chunk in response.iter_content(1024):
                    out_file.write(chunk)
            print(f"Downloaded: {image_url} -> {save_path}")
        else:
            print(f"Failed to download: {image_url} (Status code: {response.status_code})")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")


# Function to process an HTML file

def process_html_file(file_path):
    # Use the HTML file's name (without extension) as the subdirectory name
    page_name = os.path.splitext(os.path.basename(file_path))[0]
    local_image_dir = os.path.join(IMAGE_DIR, page_name)

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all image tags and process those linking to Wix
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url and img_url.startswith("https://static.wixstatic.com/media/"):
            image_name = os.path.basename(img_url)
            local_image_path = os.path.join(local_image_dir, image_name)
            
            # Download the image
            download_image(img_url, local_image_path)
            
            # Update the image src attribute to point to the new local path (relative path recommended)
            img_tag["src"] = f"{IMAGE_DIR}/{page_name}/{image_name}"

    # Save the updated HTML back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Processed: {file_path}")


def main():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    for html_file in HTML_FILES:
        process_html_file(html_file)


if __name__ == "__main__":
    main()