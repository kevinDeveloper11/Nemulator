import os
import json

# Directorio actual (la raíz del proyecto Vercel)
ROM_FOLDER = "." 

# Extensiones soportadas por consola
EXTENSIONES = {
    "NES": (".nes", ".fds"), "SNES": (".sfc", ".smc"),
    "GB": (".gb",), "GBC": (".gbc",), "GBA": (".gba",),
    "VB": (".vb",), "N64": (".z64",), "NDS": (".nds",),
    "PSX": (".bin", ".cue", ".iso", ".img", ".pbp", ".ecm"),
}

# Orden deseado
ORDEN = ["NES", "SNES", "GB", "GBC", "GBA", "VB", "N64", "NDS", "PSX"]

def get_roms_list():
    roms_list = []
    
    if not os.path.isdir(ROM_FOLDER):
        return []

    for consola in ORDEN:
        exts = EXTENSIONES[consola]
        
        # Filtrado de archivos en el directorio actual
        archivos = [f for f in os.listdir(ROM_FOLDER) 
                    if os.path.isfile(os.path.join(ROM_FOLDER, f)) 
                    and f.lower().endswith(exts)
                    # Excluir archivos del proyecto para evitar errores
                    and f not in ('list.json', 'rom_list.py', 'index.txt')] 
        
        roms_list.extend(archivos) 
        
    return roms_list

# La función que Vercel llama para manejar la solicitud HTTP
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
            json.dumps({"error": f"Error interno en Python: {str(e)}", "path_actual": os.getcwd()}),
            500,
            {'Content-Type': 'application/json'}
        )
