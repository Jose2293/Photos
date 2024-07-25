import os

def remove_empty_directories(path):
    # Obtener lista de todas las subcarpetas en el directorio dado
    directories = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    for directory in directories:
        # Llamar recursivamente a la función para verificar subcarpetas
        remove_empty_directories(directory)

        # Verificar si la carpeta está vacía después de procesar subcarpetas
        if not os.listdir(directory):
            # Eliminar la carpeta vacía
            os.rmdir(directory)
            print(f"Carpeta eliminada: {directory}")

if __name__ == "__main__":
    # Carpeta donde se encuentra el script (ruta completa)
    folder_path = os.path.dirname(os.path.abspath(__file__))
    
    # Llamar a la función para eliminar carpetas vacías
    remove_empty_directories(folder_path)
    
    print("Proceso completado.")
    input("Presione Enter para terminar...")
