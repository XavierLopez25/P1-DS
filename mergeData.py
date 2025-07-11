import pandas as pd
import glob
import os

# patrón de entrada y archivo de salida
input_pattern = os.path.join("CSV", "establecimiento_*.csv")
output_file   = "all_data.csv"

columns = [
    "CODIGO","DISTRITO","DEPARTAMENTO","MUNICIPIO","ESTABLECIMIENTO",
    "DIRECCION","TELEFONO","SUPERVISOR","DIRECTOR","NIVEL","SECTOR",
    "AREA","STATUS","MODALIDAD","JORNADA","PLAN","DEPARTAMENTAL"
]

dfs = []
for path in sorted(glob.glob(input_pattern)):
    df = pd.read_csv(
        path,
        skiprows=2,      # SALTA las 2 filas de header
        header=None,     
        names=columns,   # aplicar nombres de columnas
        encoding="utf-8" 
    )
    # limpia filas vacías 
    df = df.dropna(how="all")
    dfs.append(df)

all_data = pd.concat(dfs, ignore_index=True)

all_data.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Unidos {len(dfs)} archivos → '{output_file}' con {len(all_data)} filas.")
