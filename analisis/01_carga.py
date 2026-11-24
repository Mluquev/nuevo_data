from pathlib import Path
import warnings

import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_CSV = RAIZ_PROYECTO / "datos" / "crudo" / "temperatura.csv"
RUTA_INFORME = RAIZ_PROYECTO / "docs" / "carga.md"


def crear_informe(datos=None, error=None, avisos=None):
    lineas = [
        "# Informe de carga de temperatura.csv",
        "",
        f"Archivo: `{RUTA_CSV.relative_to(RAIZ_PROYECTO)}`",
        "",
        "## Problemas de lectura",
    ]

    if error is not None:
        lineas.extend(
            [
                f"No se pudo leer el archivo ({type(error).__name__}): `{error}`.",
                "",
                "## Dimensiones",
                "No disponibles porque el archivo no se pudo leer.",
                "",
                "## Columnas",
                "No disponibles porque el archivo no se pudo leer.",
                "",
                "## Primeras 5 filas",
                "No disponibles porque el archivo no se pudo leer.",
                "",
                "## Tipos de datos",
                "No disponibles porque el archivo no se pudo leer.",
                "",
                "## Posibles valores nulos",
                "No disponibles porque el archivo no se pudo leer.",
                "",
            ]
        )
        return "\n".join(lineas)

    if avisos:
        lineas.extend(f"- {aviso}" for aviso in avisos)
    else:
        lineas.append("No se produjeron avisos durante la lectura.")

    n_filas, n_columnas = datos.shape
    lineas.extend(
        [
            "",
            "## Dimensiones",
            f"- Filas: {n_filas}",
            f"- Columnas: {n_columnas}",
            "",
            "## Columnas",
        ]
    )
    lineas.extend(f"- `{columna}`" for columna in datos.columns)

    lineas.extend(
        [
            "",
            "## Primeras 5 filas",
            "```text",
            datos.head(5).to_string(index=False),
            "```",
            "",
            "## Tipos de datos",
        ]
    )
    lineas.extend(
        f"- `{columna}`: `{tipo}`"
        for columna, tipo in datos.dtypes.items()
    )

    nulos_por_columna = datos.isna().sum()
    lineas.extend(
        [
            "",
            "## Posibles valores nulos",
            "Conteo de valores que pandas reconoce como nulos por columna:",
        ]
    )
    lineas.extend(
        f"- `{columna}`: {cantidad}"
        for columna, cantidad in nulos_por_columna.items()
    )
    lineas.extend(
        [
            f"- Filas con al menos un valor nulo: {int(datos.isna().any(axis=1).sum())}",
            f"- Total de valores nulos: {int(nulos_por_columna.sum())}",
            "",
        ]
    )
    return "\n".join(lineas)


def main():
    try:
        with warnings.catch_warnings(record=True) as advertencias:
            warnings.simplefilter("always")
            datos = pd.read_csv(RUTA_CSV)
    except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as error:
        RUTA_INFORME.write_text(crear_informe(error=error), encoding="utf-8")
        raise

    avisos = [
        f"{advertencia.category.__name__}: {advertencia.message}"
        for advertencia in advertencias
    ]
    RUTA_INFORME.write_text(
        crear_informe(datos=datos, avisos=avisos),
        encoding="utf-8",
    )
    print(f"Informe guardado en {RUTA_INFORME}")


if __name__ == "__main__":
    main()
