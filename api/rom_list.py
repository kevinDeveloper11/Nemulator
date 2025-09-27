import os
import json
import inspect

# ¡CAMBIO CLAVE AQUÍ! Directorio actual (la raíz del proyecto Vercel)
# El punto "." indica al script que liste los archivos en el mismo nivel que index.txt
ROM_FOLDER = "." 

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
    
    if not os.path.isdir(ROM_FOLDER):
        return [f"ERROR: Directorio '{ROM_FOLDER}' no encontrado. Asegúrate de que los archivos estén en la raíz."]

    for consola in ORDEN:
        exts = EXTENSIONES[consola]
        
        archivos = [f for f in os.listdir(ROM_FOLDER) 
                    if os.path.isfile(os.path.join(ROM_FOLDER, f)) 
                    and f.lower().endswith(exts)
                    # Excluir el propio list.json si existe o el script de Python si lo tienes en la raíz (buena práctica)
                    and f not in ('list.json', 'roms_list.py')] 
        
        # Añade SÓLO el nombre del archivo, ya que está en la raíz
        roms_list.extend(archivos) 
        
    return roms_list


# La función principal que Vercel llama (el resto del código handler permanece igual)
def handler(request):
    try:
        roms_list = get_roms_list()
        
        json_content = json.dumps(roms_list, ensure_ascii=False, indent=2)
        
        return (
            json_content, 
            200, 
            {'Content-Type': 'application/json'}
        )
        
    except Exception as e:
        return (
            json.dumps({"error": f"Error interno: {str(e)}", "cwd": os.getcwd()}),
            500,
            {'Content-Type': 'application/json'}
        )
