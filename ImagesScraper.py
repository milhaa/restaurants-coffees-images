import json
import os
import requests
import re


# def sanitize_folder_name(name):
#     return re.sub(r'[\\/*?:"<>|]', "_", name)

# Load the dataset
json_path = r'dataset path'
print(f"Loading data from: {json_path}")

try:
    with open(json_path, 'r', encoding='utf-8') as file:
        restaurants = json.load(file)
        print(f" Loaded {len(restaurants)} places from the dataset")
except Exception as e:
    print(f" Failed to load JSON file: {e}")
    exit()

# Count how many have images
imageful = [place for place in restaurants if len(place.get("imageUrls", [])) > 0]
print(f" {len(imageful)} place have at least 1 image.\n")

# directory for storing images
base_dir = r'directory path'
os.makedirs(base_dir, exist_ok=True)

# Download images per restaurant folder
downloaded_count = 0
for idx, place in enumerate(imageful):
    title = place.get('title', f'Restaurant_{idx+1}')
    folder_name = sanitize_folder_name(title)
    restaurant_dir = os.path.join(base_dir, folder_name)
    os.makedirs(restaurant_dir, exist_ok=True)

    images = place.get('imageUrls', [])
    print(f" Downloading {len(images)} images for: {title}")

    for i, url in enumerate(images):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_name = os.path.join(restaurant_dir, f"image_{i+1}.jpg")
                with open(file_name, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"    Saved: {file_name}")
                downloaded_count += 1
            else:
                print(f"    Failed to download (status {response.status_code}): {url}")
        except Exception as e:
            print(f"    Error downloading {url}: {e}")

print(f"\n Completed. Total images downloaded: {downloaded_count}")
