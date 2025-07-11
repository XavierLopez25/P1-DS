import chardet
import pandas as pd
from io import StringIO
import glob, os

def html_sin_prefijo(path):
    raw = open(path, "rb").read()
    # detectamos encoding aproximado
    guess = chardet.detect(raw)
    enc   = guess["encoding"] or "cp1252"
    # opcionalmente saltamos un BOM de UTF-8
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
        enc = "utf-8"
    # buscamos el <table> que interesa
    start = raw.lower().find(b"<table")
    if start == -1:
        raise ValueError(f"No hallé <table> en {path!r}")
    fragment = raw[start:]
    # decodificamos con la codificación detectada
    text = fragment.decode(enc, errors="replace")
    return text, enc

def xls_a_csv(html_path, csv_path):
    html_clean, used_enc = html_sin_prefijo(html_path)
    print(f"{os.path.basename(html_path)} → decodificado como {used_enc}")
    # extraemos la tabla por su id
    dfs = pd.read_html(
        StringIO(html_clean),
        attrs={"id": "_ctl0_ContentPlaceHolder1_dgResultado"},
        flavor="bs4"
    )
    if not dfs:
        raise ValueError(f"No encontré la tabla en {html_path}")
    df = dfs[0]
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"  ✔ {csv_path}")

if __name__ == "__main__":
    os.makedirs("csvs", exist_ok=True)
    for xls in glob.glob("data/*.xls"):
        nombre = os.path.splitext(os.path.basename(xls))[0]
        xls_a_csv(xls, f"csv/{nombre}.csv")
