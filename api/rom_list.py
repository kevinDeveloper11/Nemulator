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
        # Esto solo se ejecutaría si Vercel no encuentra la carpeta (improbable)
        return []

    for consola in ORDEN:
        exts = EXTENSIONES[consola]
        
        # Listamos y filtramos archivos en el directorio actual
        archivos = [f for f in os.listdir(ROM_FOLDER) 
                    if os.path.isfile(os.path.join(ROM_FOLDER, f)) 
                    and f.lower().endswith(exts)
                    # Excluimos archivos del proyecto para evitar errores o listados indeseados
                    and f not in ('list.json', 'rom_list.py', 'index.txt', 'index.html')] 
        
        roms_list.extend(archivos) 
        
    return roms_list


# La función handler debe devolver una tupla: (contenido, estado, headers)
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
        # Devuelve un 500 con un JSON de error si algo falla
        return (
            json.dumps({"error": f"Error interno en Python: {str(e)}"}),
            500,
            {'Content-Type': 'application/json'}
        )
