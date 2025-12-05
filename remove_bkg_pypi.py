import os
import requests
import subprocess

def baixar_e_remover_fundo(url_imagem, caminho_destino):
    # Cria pasta caso não exista
    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

    # Nome e pasta
    pasta, arquivo = os.path.split(caminho_destino)
    nome, ext = os.path.splitext(arquivo)

    # Arquivo de saída sempre PNG (transparência)
    arquivo_sem_fundo = os.path.join(pasta, f"{nome}_nofundo.png")

    try:
        print("Baixando imagem da URL...")
        response = requests.get(url_imagem)
        response.raise_for_status()

        # Salvar a imagem original no caminho especificado
        with open(caminho_destino, "wb") as f:
            f.write(response.content)

        print("Removendo fundo com backgroundremover...")

        # Executar o comando do backgroundremover
        subprocess.run([
            "backgroundremover",
            "-i", caminho_destino,
            "-o", arquivo_sem_fundo,
            "-m", "u2net"       # modelo de maior qualidade
        ], check=True)

        print("Pronto!")
        print("Imagem salva sem fundo em:", arquivo_sem_fundo)

    except Exception as e:
        print("Erro:", e)


# EXEMPLO DE USO
if __name__ == "__main__":
    url = "https://www.luxjoias.com/images/ld20-22_1.jpg"
    destino = r"D:\Documentos\NAME\desktop\ld20-22_1.jpg"

    baixar_e_remover_fundo(url, destino)
