from html import escape
from pathlib import Path
import re
import unicodedata

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_EXCEL = RAIZ_PROYECTO / "datos" / "crudo" / "data_1787673487.xlsx"
RUTA_INFORME = RAIZ_PROYECTO / "docs" / "inventario.md"
HOJA = "datos"

VALORES_ORDINALES = (
    ("muy bajo", "bajo", "medio", "alto", "muy alto"),
    ("muy mala", "mala", "regular", "buena", "muy buena"),
    ("muy malo", "malo", "regular", "bueno", "muy bueno"),
    ("very low", "low", "medium", "high", "very high"),
    ("low", "medium", "high"),
    ("small", "medium", "large"),
    ("nunca", "rara vez", "a veces", "frecuentemente", "siempre"),
)


def normalizar_texto(valor):
    texto = unicodedata.normalize("NFKD", str(valor).casefold())
    return "".join(
        caracter for caracter in texto if not unicodedata.combining(caracter)
    )


def es_temporal(nombre, serie):
    if is_datetime64_any_dtype(serie.dtype):
        return True

    nombre_normalizado = normalizar_texto(nombre)
    return bool(
        re.search(
            r"(?:^|[^a-z])(?:fecha|date|datetime|timestamp|anos?|years?)(?:$|[^a-z])",
            nombre_normalizado,
        )
    )


def clasificar_variable(nombre, serie):
    if es_temporal(nombre, serie):
        return "temporal"
    if is_numeric_dtype(serie.dtype):
        return "numérica"

    valores = {
        normalizar_texto(valor)
        for valor in serie.dropna()
    }
    if len(valores) > 1 and any(
        valores.issubset(orden) for orden in VALORES_ORDINALES
    ):
        return "categórica ordinal"
    return "categórica nominal"


def formatear_valor(valor):
    texto = str(valor).replace("\r", " ").replace("\n", " ")
    return f"<code>{escape(texto).replace('|', '&#124;')}</code>"


def crear_inventario(datos):
    lineas = [
        "# Inventario de datos",
        "",
        f"Archivo: `{RUTA_EXCEL.relative_to(RAIZ_PROYECTO)}`",
        f"Hoja analizada: `{HOJA}`",
        "",
        "El tipo de dato corresponde al detectado por pandas al leer la hoja. "
        "La clasificación de variable es descriptiva; los datos no se "
        "transformaron ni limpiaron.",
        "",
        "| Nombre exacto | Tipo de dato detectado | Clasificación de variable | "
        "Valores nulos | Valores distintos | Tres ejemplos de valores |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]

    for nombre in datos.columns:
        serie = datos[nombre]
        ejemplos = serie.dropna().drop_duplicates().head(3)
        texto_ejemplos = ", ".join(formatear_valor(valor) for valor in ejemplos)
        if not texto_ejemplos:
            texto_ejemplos = "—"

        nombre_visible = escape(str(nombre)).replace("|", "&#124;")
        lineas.append(
            f"| `{nombre_visible}` | `{serie.dtype}` "
            f"| {clasificar_variable(nombre, serie)} "
            f"| {int(serie.isna().sum())} "
            f"| {int(serie.nunique(dropna=True))} | {texto_ejemplos} |"
        )

    lineas.append("")
    return "\n".join(lineas)


def main():
    RUTA_INFORME.parent.mkdir(parents=True, exist_ok=True)
    try:
        datos = pd.read_excel(RUTA_EXCEL, sheet_name=HOJA)
    except (OSError, ImportError, ValueError, pd.errors.ParserError) as error:
        RUTA_INFORME.write_text(
            (
                "# Inventario de datos\n\n"
                f"Archivo: `{RUTA_EXCEL.relative_to(RAIZ_PROYECTO)}`\n"
                f"Hoja analizada: `{HOJA}`\n\n"
                f"No se pudo leer el archivo "
                f"({type(error).__name__}): `{error}`.\n"
            ),
            encoding="utf-8",
        )
        raise

    RUTA_INFORME.write_text(crear_inventario(datos), encoding="utf-8")
    print(f"Inventario guardado en {RUTA_INFORME}")


if __name__ == "__main__":
    main()
