import os
from PIL import Image, ImageFilter

# Pastas
input_dir = r"D:\Documentos\NAME\desktop\_imgs"
output_dir = r"D:\Documentos\NAME\desktop\_imgsresize"
os.makedirs(output_dir, exist_ok=True)

def upscale_and_sharpen_image(image_path, target_size=1200):
    try:
        img = Image.open(image_path).convert("RGB")  # evita JPG com canal alfa

        # Remove metadados (EXIF), reduz bastante o tamanho do arquivo
        img_clean = Image.new(img.mode, img.size)
        img_clean.putdata(list(img.getdata()))

        # Calcula novo tamanho mantendo proporção
        w, h = img_clean.size
        if w > h:
            new_w = target_size
            new_h = int((target_size / w) * h)
        else:
            new_h = target_size
            new_w = int((target_size / h) * w)

        # Upscale com qualidade máxima
        img_resized = img_clean.resize((new_w, new_h), Image.LANCZOS)

        # Sharpen suave (não cria ruído)
        img_sharpened = img_resized.filter(
            ImageFilter.UnsharpMask(radius=1.5, percent=130, threshold=2)
        )

        # Mantém o nome original
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)

        # Salva como JPG leve + otimizado
        img_sharpened.save(
            output_path,
            format="JPEG",
            quality=88,         # excelente equilíbrio entre peso e nitidez
            optimize=True,      # deixa o arquivo menor
            progressive=True    # melhora compressão para web
        )

        print(f"Imagem salva: {output_path}")

    except Exception as e:
        print(f"Erro ao processar {image_path}: {e}")

# Processa todas as imagens
for file in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file)
    if os.path.isfile(file_path) and file.lower().endswith(('.jpg', '.jpeg', '.png')):
        upscale_and_sharpen_image(file_path)
