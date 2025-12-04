import os
from PIL import Image, ImageFilter

# Pasta com as imagens originais
input_dir = r"D:\Documentos\NAME\desktop\_imgs"

# Pasta de saída para as imagens processadas
output_dir = r"D:\Documentos\NAME\desktop\_imgsresize"

# Cria a pasta de saída se não existir
os.makedirs(output_dir, exist_ok=True)

# Função para upscale e sharpen
def upscale_and_sharpen_image(image_path, target_size=1500):
    try:
        img = Image.open(image_path)
        
        # Calcula novo tamanho mantendo proporção
        width, height = img.size
        if width > height:
            new_width = target_size
            new_height = int((target_size / width) * height)
        else:
            new_height = target_size
            new_width = int((target_size / height) * width)
        
        # Redimensiona com alta qualidade
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Aplica sharpen
        img_sharpened = img_resized.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        
        # Define caminho de saída mantendo o nome do arquivo
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)
        
        # Salva a imagem processada
        img_sharpened.save(output_path, quality=95)
        print(f"Imagem salva: {output_path}")
    
    except Exception as e:
        print(f"Erro ao processar {image_path}: {e}")

# Processa todas as imagens da pasta
for file in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file)
    if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        upscale_and_sharpen_image(file_path)
