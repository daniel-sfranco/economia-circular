# utils.py
import os
import uuid
from PIL import Image
from flask import current_app

def compress_and_save_image(upload_file, upload_folder):
    filename = str(uuid.uuid4()) + ".webp"
    filepath = os.path.join(upload_folder, filename)
    
    img = Image.open(upload_file)
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    img.thumbnail((800, 800))
    
    img.save(filepath, format="WEBP", quality=80)
    
    return filename

def delete_product_images(image_paths_string):
    if not image_paths_string:
        return
        
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
    imagens = image_paths_string.split(',')
    
    for imagem in imagens:
        caminho = os.path.join(upload_path, imagem)
        if os.path.exists(caminho):
            os.remove(caminho)

def process_and_save_images(images_list):
    if not images_list or not images_list[0].filename:
        return ""
        
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    
    saved_names = []
    for file in images_list:
        if file and file.filename != '':
            # Chama a sua função existente para comprimir e salvar
            saved_filename = compress_and_save_image(file, upload_path)
            saved_names.append(saved_filename)
            
    return ",".join(saved_names)