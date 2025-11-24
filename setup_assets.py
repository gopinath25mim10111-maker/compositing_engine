import os
import urllib.request

# 1. Define where we want to save the images
folder = "backgrounds"
if not os.path.exists(folder):
    os.makedirs(folder)
    print(f"[OK] Created folder: {folder}/")
else:
    print(f"[OK] Folder found: {folder}/")

# 2. List of professional images (Direct URLs from Unsplash/Pexels)
images = {
    "cyber_city.jpg": "https://images.unsplash.com/photo-1515630278258-407f66498911?w=640&q=80",
    "deep_space.jpg": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=640&q=80",
    "forest_mist.jpg": "https://images.unsplash.com/photo-1511497584788-876760111969?w=640&q=80"
}

print("--- Starting Asset Download ---")

# 3. Download Loop
for filename, url in images.items():
    file_path = os.path.join(folder, filename)
    
    # Check if we already have it
    if os.path.exists(file_path):
        print(f"[SKIP] {filename} already exists.")
    else:
        print(f"[DOWNLOADING] {filename}...")
        try:
            # This line downloads the image from the web and saves it
            urllib.request.urlretrieve(url, file_path)
            print(f"   -> Saved to {file_path}")
        except Exception as e:
            print(f"   [ERROR] Could not download {filename}: {e}")

print("-------------------------------")
print("SUCCESS! Images are ready.")
print("Run 'py main.py' and use 'a'/'d' to switch backgrounds.")