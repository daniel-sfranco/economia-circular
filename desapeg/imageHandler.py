# utils.py
import os
import uuid
from PIL import Image

def compress_and_save_image(upload_file, upload_folder):
    filename = str(uuid.uuid4()) + ".webp"
    filepath = os.path.join(upload_folder, filename)
    
    img = Image.open(upload_file)
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    img.thumbnail((800, 800))
    
    img.save(filepath, format="WEBP", quality=80)
    
    return filename