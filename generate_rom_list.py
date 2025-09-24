import os
import json

# Carpeta donde están tus ROMs
rom_folder = "roms"

# Extensiones soportadas por consola
extensiones = {
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
orden = ["NES", "SNES", "GB", "GBC", "GBA", "VB", "N64", "NDS", "PSX"]

# Lista final de ROMs
roms_list = []

# Clasificar y añadir en el orden deseado
for consola in orden:
    exts = extensiones[consola]
    archivos = [f for f in os.listdir(rom_folder) if f.lower().endswith(exts)]
    # Añadir en orden
    roms_list.extend(archivos)

# Guardar como un array plano en list.json
with open(os.path.join(rom_folder, "list.json"), "w", encoding="utf-8") as f:
    json.dump(roms_list, f, ensure_ascii=False, indent=2)

print(f"✅ list.json generado con {len(roms_list)} ROM(s) .")
