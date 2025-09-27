import os
import json

# Directorio actual (la raíz del proyecto Vercel)
ROM_FOLDER = "." 

# Definición de extensiones y orden (sin cambios)
EXTENSIONES = {
    "NES": (".nes", ".fds"), "SNES": (".sfc", ".smc"),
    "GB": (".gb",), "GBC": (".gbc",), "GBA": (".gba",),
    "VB": (".vb",), "N64": (".z64",), "NDS": (".nds",),
    "PSX": (".bin", ".cue", ".iso", ".img", ".pbp", ".ecm"),
}
ORDEN = ["NES", "SNES", "GB", "GBC", "GBA", "VB", "N64", "NDS", "PSX"]

def get_roms_list():
    roms_list = []
    
    if not os.path.isdir(ROM_FOLDER):
        return []

    for consola in ORDEN:
        exts = EXTENSIONES[consola]
        
        archivos = [f for f in os.listdir(ROM_FOLDER) 
                    if os.path.isfile(os.path.join(ROM_FOLDER, f)) 
                    and f.lower().endswith(exts)
                    # Asegúrate de excluir index.txt/index.html y el propio script
                    and f not in ('list.json', 'rom_list.py', 'index.txt', 'index.html', '.gitignore')] 
        
        roms_list.extend(archivos) 
        
    return roms_list


# 🚨 CAMBIO CLAVE: Usamos 'vercel_handler' como nombre de función.
# Esta convención evita conflictos con el auto-descubrimiento de clases base.
def vercel_handler(request):
    try:
        roms_list = get_roms_list()
        json_content = json.dumps(roms_list, ensure_ascii=False, indent=2)
        
        # El resultado de la función Vercel debe ser una tupla (contenido, estado, headers)
        return (
            json_content, 
            200, 
            {'Content-Type': 'application/json',
             # Añadimos cabeceras CORS por si acaso (aunque no suelen ser necesarias en Vercel)
             'Access-Control-Allow-Origin': '*'} 
        )
        
    except Exception as e:
        # Esto te ayudará a ver el error específico en los logs de Vercel
        return (
            json.dumps({"error": f"Error FATAL: {str(e)}", "path_actual": os.getcwd()}),
            500,
            {'Content-Type': 'application/json'}
        )

# Mapeamos 'handler' a 'vercel_handler' para que Vercel lo encuentre sin problemas de tipado.
handler = vercel_handler
