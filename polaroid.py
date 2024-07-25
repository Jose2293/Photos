import os
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def create_polaroid_frame(image):
    # Tamaño del marco polaroid
    frame_width = image.width + 40
    frame_height = image.height + 100

    # Crear un nuevo lienzo blanco (color del marco)
    framed_image = Image.new("RGB", (frame_width, frame_height), "white")

    # Pegar la imagen en el marco
    framed_image.paste(image, (20, 20))

    # Dibujar un borde negro alrededor del marco
    draw = ImageDraw.Draw(framed_image)
    border_width = 5
    for i in range(border_width):
        draw.rectangle([i, i, frame_width - i - 1, frame_height - i - 1], outline="black")

    return framed_image

def create_pdf_from_images(folder_path, output_filename):
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

    # Ordenar archivos por nombre (opcional)
    image_files.sort()

    # Imprimir archivos encontrados en la carpeta
    print("Archivos encontrados en la carpeta:")
    for file in image_files:
        print(file)

    # Crear un nuevo archivo PDF
    c = canvas.Canvas(output_filename, pagesize=letter)

    # Configurar dimensiones para las miniaturas de las imágenes con marco
    thumbnail_width = 3.875 * inch
    thumbnail_height = 5.125 * inch

    # Configurar la disposición en el PDF (4 imágenes por página)
    images_per_page = 4
    x_positions = [0, thumbnail_width]
    y_positions = [letter[1] - thumbnail_height, letter[1] - 2 * thumbnail_height]

    current_image_index = 0
    for image_file in image_files:
        # Abrir la imagen
        img_path = os.path.join(folder_path, image_file)
        img = Image.open(img_path)

        # Rotar la imagen si es horizontal
        if img.width > img.height:
            img = img.rotate(-90, expand=True)

        # Escalar la imagen al tamaño deseado
        img.thumbnail((thumbnail_width - 40, thumbnail_height - 100), Image.LANCZOS)

        # Crear un marco polaroid para la imagen
        framed_img = create_polaroid_frame(img)

        # Guardar la imagen con el marco temporalmente en memoria
        framed_img_path = os.path.join(folder_path, f"temp_framed_img_{current_image_index}.jpg")
        framed_img.save(framed_img_path)

        # Calcular la posición en la página
        x = x_positions[current_image_index % 2]
        y = y_positions[current_image_index // 2 % 2]

        # Agregar la imagen con marco al PDF
        c.drawImage(framed_img_path, x, y, width=thumbnail_width, height=thumbnail_height)
        current_image_index += 1

        # Si se alcanza el número máximo de imágenes por página, crear nueva página
        if current_image_index % images_per_page == 0:
            c.showPage()

        # Eliminar la imagen temporal
        if os.path.exists(framed_img_path):
            os.remove(framed_img_path)

    # Guardar el archivo PDF
    c.save()

    # Mensaje de confirmación
    print(f"Se ha creado el archivo PDF '{output_filename}' en la carpeta especificada.")
    input("Presione Enter para terminar...")

# Ejemplo de uso
if __name__ == "__main__":
    # Carpeta donde se encuentra el script (ruta completa)
    folder_path = os.path.dirname(os.path.abspath(__file__))
    # Nombre del archivo PDF de salida (se guarda en la misma carpeta)
    output_filename = os.path.join(folder_path, "output.pdf")
    create_pdf_from_images(folder_path, output_filename)
