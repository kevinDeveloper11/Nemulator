import os
import json
import inspect

# La carpeta de ROMs debe ser relativa a la raíz del proyecto.
# Vercel ejecuta el script en el contexto de la aplicación,
# por lo que 'roms' es el path correcto si está en la raíz del repo.
ROM_FOLDER = "roms"

# Extensiones soportadas por consola
EXTENSIONES = {
    "NES": (".nes", ".fds"),
    "SNES": (".sfc", ".smc"),
    "GB": (".gb",),
    "GBC": (".gbc",),
    "GBA": (".gba",),
    "VB": (".vb",),
    "N64": (".z64",),
    "NDS": (".nds",),
    "PSX": (".bin", ".cue", ".iso", ".img", ".pbp", ".ecm"),
}

# Orden deseado
ORDEN = ["NES", "SNES", "GB", "GBC", "GBA", "VB", "N64", "NDS", "PSX"]

def get_roms_list():
    roms_list = []
    
    # Comprobar si la carpeta de ROMs existe en el entorno de Vercel
    if not os.path.isdir(ROM_FOLDER):
        # Útil para debug si la carpeta no se encuentra
        return [f"ERROR: Carpeta '{ROM_FOLDER}' no encontrada. Path actual: {os.getcwd()}"]

    # Clasificar y añadir en el orden deseado
    for consola in ORDEN:
        exts = EXTENSIONES[consola]
        
        # Listar y filtrar archivos dentro de la carpeta ROM_FOLDER
        archivos = [f for f in os.listdir(ROM_FOLDER) 
                    # Aseguramos que sea un archivo y que termine con la extensión correcta
                    if os.path.isfile(os.path.join(ROM_FOLDER, f)) and f.lower().endswith(exts)]
        
        # Añadimos el path relativo completo para que JavaScript sepa dónde buscar la ROM
        roms_list.extend([f"{ROM_FOLDER}/{archivo}" for archivo in archivos])
        
    return roms_list


# La función principal que Vercel llama para manejar la solicitud HTTP
def handler(request):
    try:
        roms_list = get_roms_list()
        
        # 1. Serializar la lista a JSON
        json_content = json.dumps(roms_list, ensure_ascii=False, indent=2)
        
        # 2. Devolver la respuesta en el formato de Vercel
        return (
            json_content, 
            200, 
            {'Content-Type': 'application/json'}
        )
        
    except Exception as e:
        # Manejo de errores
        return (
            json.dumps({"error": f"Error interno: {str(e)}", "cwd": os.getcwd()}),
            500,
            {'Content-Type': 'application/json'}
        )

# Si el entorno no es Vercel, esto ayuda a probar localmente
if __name__ == "__main__":
    # La prueba local debe crear una carpeta 'roms' y poner archivos dentro.
    print(json.dumps(get_roms_list(), indent=2))
