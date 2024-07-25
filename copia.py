import os
import shutil
import win32com.client

def copiar_imagenes_desde_mtp(origen, destino):
    # Obtener el objeto Shell de COM
    shell = win32com.client.Dispatch("Shell.Application")
    carpeta_origen = shell.NameSpace(origen)
    
    if not carpeta_origen:
        print(f"No se pudo acceder a la carpeta: {origen}")
        return
    
    extensiones_imagenes = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')
    items = carpeta_origen.Items()
    
    for item in items:
        if item.IsFolder:
            continue
        if not any(item.Name.lower().endswith(ext) for ext in extensiones_imagenes):
            continue
        
        ruta_destino = os.path.join(destino, item.Name)
        shutil.copy2(item.Path, ruta_destino)
        print(f"Copiado: {item.Name} a {ruta_destino}")

def obtener_ruta_telefono(nombre_telefono):
    shell = win32com.client.Dispatch("Shell.Application")
    mi_pc = shell.Namespace(17)  # 17 es el namespace para "Este equipo"
    
    for item in mi_pc.Items():
        if nombre_telefono in item.Name:
            for subitem in item.GetFolder.Items():
                if "Almacenamiento" in subitem.Name:
                    return subitem.Path
    return None

if __name__ == "__main__":
    nombre_telefono = "Galaxy S20 FE"
    ruta_telefono = obtener_ruta_telefono(nombre_telefono)
    
    if ruta_telefono:
        print(f"Ruta del teléfono encontrada: {ruta_telefono}")
        subcarpeta = input("Ingrese la subcarpeta de imágenes en el teléfono (por ejemplo, 'DCIM\\Camera'): ")
        path_origen = os.path.join(ruta_telefono, subcarpeta)
        path_destino = os.path.dirname(os.path.abspath(__file__))
        
        if os.path.exists(path_origen):
            copiar_imagenes_desde_mtp(path_origen, path_destino)
            print("Copia completada.")
        else:
            print(f"La subcarpeta {path_origen} no existe.")
    else:
        print("No se pudo encontrar el teléfono conectado.")
