import os
from PIL import Image

def rotate_horizontal_images_in_folder(folder_path):
    # Obtener lista de archivos en la carpeta
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not image_files:
        print(f"No se encontraron archivos en la carpeta especificada: {folder_path}")
        return
    
    # Filtrar solo archivos con extensiones jpeg, jpg, png
    image_files = [f for f in image_files if f.lower().endswith(('jpeg', 'jpg', 'png'))]

    if not image_files:
        print("No se encontraron archivos de imagen en la carpeta especificada.")
        return

    # Procesar cada archivo de imagen
    for image_file in image_files:
        img_path = os.path.join(folder_path, image_file)
        img = Image.open(img_path)

        # Rotar la imagen si es horizontal
        if img.width > img.height:
            img = img.rotate(90, expand=True)
            img.save(img_path)  # Sobrescribe la imagen rotada

            print(f"Imagen rotada: {image_file}")

    print("Proceso completado.")

# Ejemplo de uso
if __name__ == "__main__":
    # Carpeta donde se encuentra el script (ruta completa)
    folder_path = os.path.dirname(os.path.abspath(__file__))
    rotate_horizontal_images_in_folder(folder_path)
