import os
import io
import requests
import numpy as np
from rembg import remove
from PIL import Image

# ---------- CONFIG ----------
image_url = "https://www.luxjoias.com/images/ld20-22_1.jpg"
output_folder = r"D:\Documentos\NAME\desktop"
basename = "ld20-22_fixed_inner_white"
output_path = os.path.join(output_folder, basename + ".png")
# ----------------------------

os.makedirs(output_folder, exist_ok=True)

try:
    print("1) Baixando imagem...")
    resp = requests.get(image_url, timeout=20)
    resp.raise_for_status()
    orig_pil = Image.open(io.BytesIO(resp.content)).convert("RGBA")

    print("2) Removendo fundo com rembg...")
    no_bg_pil = remove(orig_pil)  # PIL RGBA

    # Separar canais
    r, g, b, a = no_bg_pil.split()

    # Criar máscara binária do objeto
    mask = np.array(a) > 128  # True = objeto, False = fundo

    # Criar imagem final com fundo branco
    white_bg = np.ones((no_bg_pil.height, no_bg_pil.width, 3), dtype=np.uint8) * 255
    obj_pixels = np.array(no_bg_pil)[..., :3]

    # Substituir pixels do objeto pelos originais, fundo branco
    final_array = white_bg.copy()
    final_array[mask] = obj_pixels[mask]

    # Salvar resultado
    final_img = Image.fromarray(final_array)
    final_img.save(output_path, "PNG", optimize=True)
    print(f"Processamento finalizado. Imagem salva em:\n{output_path}")

except Exception as ex:
    print("Erro durante o processamento:", ex)
